"""Approved hypothetical shape sensitivity; never a validated damage prediction."""
import hashlib
import json
import math
from pathlib import Path
import sys
import geopandas as gpd
import numpy as np
import pandas as pd
from check_shaking_coordinate_gate import main as coordinate_gate, nearest

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/revision_shaking'
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health

CATEGORIES=['震度１','震度２','震度３','震度４','震度５弱','震度５強','震度６弱','震度６強','震度７']
LOW=np.array([.5,1.5,2.5,3.5,4.5,5,5.5,6,6.5])
HIGH=np.array([1.5,2.5,3.5,4.5,5,5.5,6,6.5,np.inf])
SHAPES={'wooden':(6.87,.73),'steel':(7.25,.63),'light_steel':(7.24,.60)}
PROXIES=['General Households','Mapped Building Count','Mapped Building Footprint Area m2']

def allocate(q,h,total):
    assert np.isfinite(q).all() and np.isfinite(h).all() and (q>=0).all() and (h>=0).all()
    q=np.where(h>0,q,0)
    if h[q>0].sum()<total: raise ValueError('Insufficient positive-weight capacity')
    hi=total/q.sum()
    while np.minimum(h,hi*q).sum()<total: hi*=2
    lo=0.
    for _ in range(100):
        mid=(lo+hi)/2
        if np.minimum(h,mid*q).sum()<total: lo=mid
        else: hi=mid
    result=np.minimum(h,hi*q)
    np.testing.assert_allclose(result.sum(),total,atol=1e-8,rtol=0)
    assert (result<=h).all()
    return result

def main():
    assert coordinate_gate()['passed'], 'Coordinate gate failed; stop for human review'
    sources=[ROOT/'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet',
             OUT/'sources/jma_event_20260728162715.json',
             ROOT/'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet',
             ROOT/'data/exp/revision_snapshot_sensitivity/municipality_comparison.csv',
             ROOT/'data/processed/kumamoto_grid_exposure_estimates_preprocessed.parquet',
             ROOT/'data/exp/revision_spatial_validation/municipality_damage_20260731.csv',
             ROOT/'data/exp/revision_spatial_validation/municipality_damage_20260929.csv',
             OUT/'sources/suto_2019.pdf',ROOT/'Rev/docs/shaking-sensitivity-specification.md']
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p.relative_to(ROOT)):digest(p) for p in sources}
    np.testing.assert_allclose(allocate(np.array([1.,1.,0]),np.array([.1,10,0]),1),[.1,.9,0])
    try: allocate(np.array([0.,1.]),np.array([10.,.1]),1)
    except ValueError: pass
    else: raise AssertionError('Feasibility test failed')
    assert nearest(np.array([[0.,0.]]),np.array([[1.,0.],[-1.,0.]])).item()==0
    frame=gpd.read_parquet(sources[0])
    geometry=gpd.read_parquet(sources[2])[['Municipality Code','geometry']]
    assigned=health.assign_municipalities(frame,geometry)
    assert len(assigned)==len(frame)
    assert assigned['Disclosure Group Code'].tolist()==frame['Disclosure Group Code'].tolist()
    codes=assigned['Municipality Code'].to_numpy()
    assert len(set(codes))==45
    rows=sorted(json.loads(sources[1].read_text())['res']['int'],key=lambda r:r['code'])
    station_categories=np.array([CATEGORIES.index(r['int']) for r in rows])
    pts=gpd.GeoSeries(gpd.points_from_xy([float(r['lon']) for r in rows],[float(r['lat']) for r in rows]),crs=4326).to_crs(6670)
    sxy=np.column_stack([pts.x,pts.y])
    p=frame.to_crs(6670).geometry.representative_point()
    idx=nearest(np.column_stack([p.x,p.y]),sxy)
    category=station_categories[idx]
    confusion=np.zeros((9,9),dtype=int); errors=[]; distances=[]
    for i,r in enumerate(rows):
        if not r['code'].startswith('74'): continue
        d=((sxy-sxy[i])**2).sum(axis=1)
        d[d<=1e-12]=np.inf
        j=d.argmin(); a,b=station_categories[i],station_categories[j]
        confusion[a,b]+=1; errors.append(abs(int(a)-int(b))); distances.append(float(np.sqrt(d[j])/1000))
    loo={'categories':CATEGORIES,'confusion_actual_rows_predicted_columns':confusion.tolist(),
         'stations':len(errors),'exact_agreement':float(np.mean(np.array(errors)==0)),
         'within_one_category':float(np.mean(np.array(errors)<=1)), 'ordinal_step_mae':float(np.mean(errors)),
         'distance_km_quantiles':np.quantile(distances,[0,.5,.95,1]).tolist()}
    baseline=pd.read_csv(sources[3],dtype={'Municipality Code':str}).set_index('Municipality Code')
    h=frame['General Households'].to_numpy(float); n=frame['Population Age 65+'].to_numpy(float)
    population=frame['Total Population'].to_numpy(float)
    assert np.isfinite(n).all() and (n>=0).all()
    report_tables={date:pd.read_csv(ROOT/f'data/exp/revision_spatial_validation/municipality_damage_{date}.csv',dtype={'Municipality Code':str}).set_index('Municipality Code') for date in ['20260731','20260929']}
    summaries=[]; municipal=[]; comparisons=[]
    for shape,(mu,sigma) in SHAPES.items():
      for endpoint,values in [('lower',LOW),('upper_limit',HIGH)]:
        weights=np.array([.5*math.erfc(-(v-mu)/sigma/math.sqrt(2)) for v in values])
        assert (np.diff(weights)>=0).all() and ((weights>=0)&(weights<=1)).all()
        if endpoint=='upper_limit': assert weights[-1]==1
        for proxy in PROXIES:
          q=frame[proxy].to_numpy(float)*weights[category]
          for theta in [0.,.5,1.]:
            sid=f'{shape}|{endpoint}|{PROXIES.index(proxy)}|{theta}'
            total=181+245*theta; loss=allocate(q,h,total)
            older=n*np.divide(loss,h,out=np.zeros_like(loss),where=h>0)
            agg=pd.DataFrame({'code':codes,'loss':loss,'older':older}).groupby('code').sum().reindex(baseline.index)
            assert len(agg)==45 and agg.notna().all().all()
            np.testing.assert_allclose(agg.loss.sum(),total)
            result={'scenario':sid,'shape':shape,'endpoint':endpoint,'proxy':proxy,'theta':theta,'loss':float(loss.sum()),'older':float(older.sum()),'binding_caps':int(((h>0)&(loss==h)).sum()),'low_intensity_loss_share':float(loss[category<4].sum()/total)}
            for metric,col in [('loss','Expected Functionally Lost Residences_early'),('older','Estimated Affected Population Age 65+_early')]:
                a,b=agg[metric],baseline[col]
                result[metric+'_rank_rho']=float(a.rank().corr(b.rank()))
                result[metric+'_max_rank_shift']=float((a.rank(ascending=False,method='min')-b.rank(ascending=False,method='min')).abs().max())
                result[metric+'_top5_overlap']=len(set(a.nlargest(5).index)&set(b.nlargest(5).index))
                agg[metric+'_share']=a/a.sum()
                agg[metric+'_rank']=a.rank(ascending=False,method='min')
                agg[metric+'_rank_shift']=agg[metric+'_rank']-b.rank(ascending=False,method='min')
            summaries.append(result)
            for code,row in agg.iterrows(): municipal.append({'scenario':sid,'Municipality Code':code,**row.to_dict()})
            for date,reported in report_tables.items():
              for field in ['full','broad_half','full_or_half']:
                observed=reported[field].reindex(agg.index); share=observed/observed.sum()
                comparisons.append({'scenario':sid,'snapshot':date,'category':field,'tvd':float(abs(share-agg.loss_share).sum()/2),'rank_rho':float(observed.rank().corr(agg.loss.rank())),'top5_overlap':len(set(observed.nlargest(5).index)&set(agg.loss.nlargest(5).index)) if (observed>0).sum()>=5 else None})
    assert len(summaries)==54 and len(municipal)==54*45
    pd.DataFrame(summaries).to_csv(OUT/'scenario_summary.csv',index=False)
    pd.DataFrame(municipal).to_csv(OUT/'scenario_municipalities.csv',index=False)
    pd.DataFrame(comparisons).to_csv(OUT/'reported_damage_comparisons.csv',index=False)
    assert before=={str(p.relative_to(ROOT)):digest(p) for p in sources}
    report={'scenarios':54,'municipality_rows':len(municipal),'protected_hashes_unchanged':True,'sha256':before,'loo':loo,
            'low_intensity_population_share':float(population[category<4].sum()/population.sum()),'low_intensity_household_share':float(h[category<4].sum()/h.sum()),
            'interpretation':'Hypothetical full-collapse-shape allocation of fixed functional-loss totals; not validated damage probabilities or actual vulnerability composition.',
            'tests':'coordinate gate, tie, feasibility, zero capacity, saturation, coefficients as approved, ordered endpoints, category7 limit, totals and caps passed'}
    (OUT/'scenario_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
