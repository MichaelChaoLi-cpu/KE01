"""Four approved municipal-constrained demographic allocation experiments."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_age_allocation'

def bounded(lower, upper, weight, target):
    """Solve x=L+min(U-L, lambda*w) without rescaling controls."""
    lower,upper,weight=map(lambda x:np.asarray(x,dtype=float),(lower,upper,weight))
    cap=upper-lower
    assert np.all(cap>=0) and np.all(weight>=0)
    residual=target-lower.sum()
    reachable=cap[weight>0].sum()
    if residual < -1e-8 or residual > reachable+1e-8:
        raise ValueError(f'Infeasible control: {target}, bounds {lower.sum()}, {lower.sum()+reachable}')
    if residual<=1e-8:
        return lower.copy()
    positive=weight>0
    hi=float(np.max(cap[positive]/weight[positive]))
    lo=0.
    for _ in range(100):
        mid=(lo+hi)/2
        if np.minimum(cap,mid*weight).sum()<residual:
            lo=mid
        else:
            hi=mid
    result=lower+np.minimum(cap,((lo+hi)/2)*weight)
    assert abs(result.sum()-target)<1e-6
    assert np.all(result>=lower-1e-9) and np.all(result<=upper+1e-9)
    return result

def main():
    # Boundary cases for the numerical solver.
    assert np.allclose(bounded([1,1],[2,5],[1,1],6),[2,4])
    assert np.allclose(bounded([0],[0],[0],0),[0])
    assert np.allclose(bounded([1,1],[2,5],[1,1],7),[2,5])
    try:
        bounded([0],[0],[0],1)
    except ValueError:
        pass
    else:
        raise AssertionError('Infeasible control accepted')
    gp=ROOT/'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet'
    mp=ROOT/'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet'
    cp=OUT/'official_municipal_age65_controls.parquet'
    bp=OUT/'boundary_groups.parquet'
    paths=[gp,mp,cp,bp]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    g=gpd.read_parquet(gp)
    ids=g['Disclosure Group Code'].tolist()
    g=health.assign_municipalities(g,gpd.read_parquet(mp)).reset_index(drop=True)
    assert ids==g['Disclosure Group Code'].tolist()
    boundaries=pd.read_parquet(bp).set_index('Disclosure Group Code')
    g['largest_area']=g['Disclosure Group Code'].map(boundaries.largest_area_municipality).fillna(g['Municipality Code'])
    controls=pd.read_parquet(cp).set_index('Municipality Code')
    lower=g['Households with Member Age 65+'].to_numpy(float)
    older=g['Population Age 65+'].to_numpy(float)
    upper=np.where(lower>0,older,0.)
    rows=[]
    infeasible=[]
    results=g[['Disclosure Group Code','Municipality Code','largest_area','Population Age 65+','General Households','Households with Member Age 65+']].copy()
    estimates={}
    for geography,column in [('representative_point','Municipality Code'),('largest_area','largest_area')]:
        for method,weights in [('older_households',lower),('residual_capacity',upper-lower)]:
            name=f'{geography}__{method}'
            x=np.full(len(g),np.nan)
            failures=[]
            for municipality,index in g.groupby(column).groups.items():
                index=np.asarray(index)
                target=float(controls.loc[municipality,'general_household_age65'])
                if not lower[index].sum()<=target<=upper[index].sum():
                    failures.append({'scenario':name,'municipality':municipality,'target':target,'lower':float(lower[index].sum()),'upper':float(upper[index].sum())})
            if failures:
                infeasible.extend(failures)
                continue
            for municipality,index in g.groupby(column).groups.items():
                index=np.asarray(index)
                target=float(controls.loc[municipality,'general_household_age65'])
                x[index]=bounded(lower[index],upper[index],weights[index],target)
                rows.append({'scenario':name,'municipality':municipality,'target':target,'estimate':float(x[index].sum()),'error':float(x[index].sum()-target),'lower':float(lower[index].sum()),'upper':float(upper[index].sum())})
            assert np.isfinite(x).all() and abs(x.sum()-495748)<1e-6
            assert np.all(x[g['General Households'].eq(0)]==0)
            results[name]=x
            results[name+'__fraction_of_all_age65']=np.divide(x,older,out=np.full(len(x),np.nan),where=older>0)
            estimates[name]=x
    checks=pd.DataFrame(rows)
    assert len(checks)==45*len(estimates) and checks.error.abs().max()<1e-6
    reference=estimates['representative_point__older_households']
    comparisons={name:{'sum':float(x.sum()),'groups_changed_from_reference':int((np.abs(x-reference)>1e-6).sum()),'half_sum_absolute_difference_from_reference':float(np.abs(x-reference).sum()/2),'max_group_difference_from_reference':float(np.abs(x-reference).max()),'groups_at_upper_bound':int(((upper>0)&np.isclose(x,upper,atol=1e-8,rtol=0)).sum())} for name,x in estimates.items()}
    report={'decision':'KILA-D-20261002-007','groups':len(g),'requested_scenario_count':4,'completed_scenario_count':len(estimates),'infeasible_scenarios':infeasible,'municipal_checks':len(checks),'maximum_control_error':float(checks.error.abs().max()),'input_sha256':hashes,'scenarios':comparisons,'interpretation':'Estimated general-household age65 counts; no observed individual institutional status. Geography is approximate. Fractions undefined where all-age65 count is zero. Not displaced-person estimates or uncertainty confidence intervals. Infeasible scenarios have no fitted output; official totals and grid bounds are unchanged.'}
    for p in paths:
        assert hashes[str(p.relative_to(ROOT))]==hashlib.sha256(p.read_bytes()).hexdigest()
    results.to_parquet(OUT/'bounded_grid_age65_estimates.parquet',index=False)
    checks.to_parquet(OUT/'bounded_municipal_checks.parquet',index=False)
    (OUT/'bounded_allocation_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'},indent=2))

if __name__=='__main__': main()
