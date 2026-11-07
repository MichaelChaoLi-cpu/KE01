"""Compare feasible demographic trials under the approved fixed housing scenario."""
from pathlib import Path
import sys
import json
import hashlib
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_grid_exposure_estimates as model
OUT=ROOT/'data/exp/revision_age_allocation'

def main():
    paths=[model.SOURCE,model.OUTPUT,OUT/'bounded_grid_age65_estimates.parquet']
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    g=gpd.read_parquet(model.SOURCE)
    a=pd.read_parquet(paths[2]).set_index('Disclosure Group Code')
    assert a.index.is_unique and set(a.index)==set(g['Disclosure Group Code'])
    a=a.loc[g['Disclosure Group Code']].reset_index()
    h=g['General Households'].to_numpy(float)
    weights=h*np.exp(-model.epicentral_distance_km(g)/20.)
    loss=weights/weights.sum()*(181+.5*245)
    assert np.all(loss<=h+1e-10) and np.all(loss[h==0]==0)
    np.testing.assert_allclose(loss.sum(),303.5,rtol=0,atol=1e-9)
    share=np.divide(loss,h,out=np.zeros(len(h)),where=h>0)
    variants={'previous_all_resident_rule':g['Population Age 65+'].to_numpy(float),
              'older_households':a['representative_point__older_households'].to_numpy(float),
              'residual_capacity':a['representative_point__residual_capacity'].to_numpy(float)}
    names=pd.read_parquet(OUT/'official_municipal_age65_controls.parquet').set_index('Municipality Code')['name']
    grids=a[['Disclosure Group Code','Municipality Code']].copy()
    grids['functional_loss']=loss
    tables={}
    summaries={}
    for key,pop in variants.items():
        exposure=pop*share
        assert np.isfinite(exposure).all() and np.all(exposure>=0) and np.all(exposure<=pop+1e-9)
        grids[key]=exposure
        t=pd.DataFrame({'Municipality Code':a['Municipality Code'],'older_exposure':exposure,'functional_loss':loss}).groupby('Municipality Code').sum()
        assert len(t)==45
        t['rank']=t.older_exposure.rank(ascending=False,method='min')
        t['name']=t.index.map(names)
        tables[key]=t
        summaries[key]={'older_exposure_total':float(exposure.sum()),'top5':t.nlargest(5,'older_exposure')[['name','older_exposure']].to_dict('index')}
    ref=tables['older_households']
    for key,t in tables.items():
        summaries[key].update(spearman_vs_household=float(t.older_exposure.rank().corr(ref.older_exposure.rank())),max_rank_shift_vs_household=float((t['rank']-ref['rank']).abs().max()),changed_ranks_vs_household=int(t['rank'].ne(ref['rank']).sum()),top5_overlap_vs_household=len(set(t.nlargest(5,'older_exposure').index)&set(ref.nlargest(5,'older_exposure').index)))
    report={'housing_loss_total':float(loss.sum()),'scenario':'households, 20 km decay, theta 0.5, early snapshot 181/245','summaries':summaries,'protected_hashes':hashes,'interpretation':'Fractional model-expected older-person exposure, not observed displaced people. Two calibrated scenarios are assumption sensitivities, not confidence bounds. Prior all-resident rule retained only as a comparator.'}
    for p in paths:
        assert hashes[str(p.relative_to(ROOT))]==hashlib.sha256(p.read_bytes()).hexdigest()
    grids.to_parquet(OUT/'age_allocation_exposure_groups.parquet',index=False)
    pd.concat(tables,names=['scenario']).reset_index().to_parquet(OUT/'age_allocation_exposure_municipalities.parquet',index=False)
    (OUT/'age_allocation_exposure_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
