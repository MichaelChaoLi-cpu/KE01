"""Compare existing 27-scenario hybrid with its coherent theta=.5 members."""
from pathlib import Path
import hashlib
import json
import sys
import geopandas as gpd
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_grid_exposure_estimates as model
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_central_surface'

def main():
    OUT.mkdir(exist_ok=True,parents=True)
    paths=[model.SOURCE,model.OUTPUT,model.DAMAGE_SNAPSHOTS,health.OUTPUT]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
    frame=gpd.read_parquet(model.SOURCE)
    damage=model.latest_prefecture_damage()
    full=float(damage['Full Collapse Buildings']); half=float(damage['Half Collapse Buildings'])
    total=full+.5*half
    distance=model.epicentral_distance_km(frame)
    surfaces=model.scenario_surfaces(frame,distance,full,half)
    median=np.median(surfaces,axis=0)
    normalized=median*total/median.sum()
    clipped=np.clip(normalized,surfaces.min(axis=0),surfaces.max(axis=0))
    saved=gpd.read_parquet(model.OUTPUT).set_index('Disclosure Group Code').loc[frame['Disclosure Group Code']]
    np.testing.assert_allclose(clipped,saved['Expected Functionally Lost Residences'],rtol=1e-10,atol=1e-10)
    variants={'raw_pointwise_median':median,'normalized_median':normalized,'saved_clipped_hybrid':clipped}
    for p,proxy in enumerate(model.EXPOSURE_PROXY_COLUMNS):
      for s,scale in enumerate(model.DISTANCE_DECAY_SCALES_KM):
        variants[f'coherent_proxy{p}_{scale:g}km_theta0.5']=surfaces[p*9+s*3+1]
    geo=gpd.read_parquet(health.OUTPUT)[['Municipality Code','geometry']]
    assigned=health.assign_municipalities(frame,geo)
    assert assigned['Disclosure Group Code'].tolist()==frame['Disclosure Group Code'].tolist()
    h=frame['General Households'].to_numpy(float)
    municipal={}; summaries=[]
    for label,loss in variants.items():
        older=model.affected_population(frame['Population Age 65+'],h,loss)
        table=pd.DataFrame({'Municipality Code':assigned['Municipality Code'].to_numpy(),'loss':loss,'older':older}).groupby('Municipality Code').sum().sort_index()
        assert len(table)==45 and table.notna().all().all()
        np.testing.assert_allclose(table.loss.sum(),loss.sum())
        municipal[label]=table
        summaries.append({'variant':label,'loss':float(loss.sum()),'older':float(older.sum()),'loss_in_zero_household_groups':float(loss[h==0].sum()),'groups_over_household_cap':int((loss>h).sum())})
    base=municipal['saved_clipped_hybrid']; output=[]
    for summary in summaries:
        label=summary['variant']; table=municipal[label]
        for metric in ['loss','older']:
            a,b=table[metric],base[metric]
            summary[metric+'_rank_rho']=float(a.rank().corr(b.rank()))
            summary[metric+'_max_rank_shift']=float((a.rank(ascending=False,method='min')-b.rank(ascending=False,method='min')).abs().max())
            summary[metric+'_top5_overlap']=len(set(a.nlargest(5).index)&set(b.nlargest(5).index))
            table[metric+'_rank']=a.rank(ascending=False,method='min')
        for code,row in table.iterrows(): output.append({'variant':label,'Municipality Code':code,**row.to_dict()})
    pd.DataFrame(summaries).to_csv(OUT/'summary.csv',index=False)
    pd.DataFrame(output).to_csv(OUT/'municipality_comparison.csv',index=False)
    report={'scenario_count':27,'compared_variants':len(variants),'normalization_factor':float(total/median.sum()),'clipped_groups':int((normalized!=clipped).sum()),'saved_baseline_reproduced':True,'protected_hashes':hashes,'protected_unchanged':hashes=={str(p.relative_to(ROOT)):sha(p) for p in paths},'interpretation':'Diagnostic only; no coherent scenario adopted and no main model changed.'}
    assert report['protected_unchanged']
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));print(pd.DataFrame(summaries).to_string(index=False))

if __name__=='__main__': main()
