"""Isolated fixed-total eligibility correction, preserving original production files."""
from pathlib import Path
import sys
import hashlib
import json
import geopandas as gpd
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_grid_exposure_estimates as model
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_denominator_correction'

def redistribute(values,eligible,total):
    weights=np.where(eligible,values,0.)
    assert weights.sum()>0
    result=weights*(total/weights.sum())
    np.testing.assert_allclose(result.sum(),total,atol=1e-9,rtol=0)
    assert (result[~eligible]==0).all()
    return result

def main():
    OUT.mkdir(exist_ok=True,parents=True)
    paths=[model.SOURCE,model.OUTPUT,model.DAMAGE_SNAPSHOTS,health.OUTPUT]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p.relative_to(ROOT)):sha(p) for p in paths}
    frame=gpd.read_parquet(model.SOURCE); h=frame['General Households'].to_numpy(float)
    assert np.isfinite(h).all() and (h>=0).all()
    eligible=h>0
    damage=model.latest_prefecture_damage(); full=float(damage['Full Collapse Buildings']); half=float(damage['Half Collapse Buildings'])
    total=full+.5*half
    old=model.scenario_surfaces(frame,model.epicentral_distance_km(frame),full,half)
    new=np.array([redistribute(row,eligible,row.sum()) for row in old])
    assert (new<=h+1e-10).all(), 'Correction exceeds positive household capacity; stop for review'
    saved=gpd.read_parquet(model.OUTPUT).set_index('Disclosure Group Code').loc[frame['Disclosure Group Code']]
    original=saved['Expected Functionally Lost Residences'].to_numpy(float)
    # Distinguish correcting the final surface from rebuilding the full ensemble.
    direct=redistribute(original,eligible,total)
    med=np.median(new,axis=0); normalized=med*total/med.sum()
    rebuilt=np.clip(normalized,new.min(axis=0),new.max(axis=0))
    np.testing.assert_allclose(rebuilt.sum(),total,rtol=0,atol=1e-9)
    assert (rebuilt[~eligible]==0).all() and (rebuilt<=h+1e-10).all()
    variants={'original_hybrid':original,'corrected_final_hybrid':direct,'rebuilt_corrected_hybrid':rebuilt}
    for p in range(3):
      for s,scale in enumerate(model.DISTANCE_DECAY_SCALES_KM):
        variants[f'corrected_proxy{p}_{scale:g}km']=new[p*9+s*3+1]
    geo=gpd.read_parquet(health.OUTPUT)[['Municipality Code','geometry']]
    assigned=health.assign_municipalities(frame,geo)
    assert assigned['Disclosure Group Code'].tolist()==frame['Disclosure Group Code'].tolist()
    tables={}; summaries=[]; rows=[]
    for name,loss in variants.items():
        older=model.affected_population(frame['Population Age 65+'],h,loss)
        table=pd.DataFrame({'Municipality Code':assigned['Municipality Code'].to_numpy(),'loss':loss,'older':older}).groupby('Municipality Code').sum().sort_index()
        assert len(table)==45 and table.notna().all().all()
        tables[name]=table
        summaries.append({'variant':name,'loss':float(loss.sum()),'older':float(older.sum()),'loss_zero_households':float(loss[~eligible].sum()),'groups_exceeding_capacity':int((loss>h+1e-10).sum())})
    base=tables['original_hybrid']
    for summary in summaries:
        table=tables[summary['variant']]
        for metric in ['loss','older']:
            a,b=table[metric],base[metric]
            summary[metric+'_rho']=float(a.rank().corr(b.rank()))
            shift=a.rank(ascending=False,method='min')-b.rank(ascending=False,method='min')
            summary[metric+'_max_rank_shift']=float(shift.abs().max())
            summary[metric+'_changed_ranks']=int((shift!=0).sum())
            summary[metric+'_top5_overlap']=len(set(a.nlargest(5).index)&set(b.nlargest(5).index))
            table[metric+'_rank_shift']=shift
        for code,row in table.iterrows(): rows.append({'variant':summary['variant'],'Municipality Code':code,**row.to_dict()})
    pd.DataFrame(summaries).to_csv(OUT/'summary.csv',index=False)
    pd.DataFrame(rows).to_csv(OUT/'municipality_comparison.csv',index=False)
    report={'original_scenarios':27,'corrected_scenarios':27,'corrected_scenario_totals_conserved':True,'all_corrected_capacity_checks_pass':True,'rebuilt_clipped_groups':int((rebuilt!=normalized).sum()),'protected_hashes':before,'protected_unchanged':before=={str(p.relative_to(ROOT)):sha(p) for p in paths},'method':'Zero ineligible weights and renormalize each scenario, then rebuild median; also separately correct final original hybrid.'}
    assert report['protected_unchanged']
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(pd.DataFrame(summaries).to_string(index=False));print(json.dumps(report,indent=2))

if __name__=='__main__': main()
