"""One-factor effect diagnostic, not joint uncertainty or transport validation."""
from pathlib import Path
import sys
import json
import hashlib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_mortality_audit'

def risk(p,h,m):
    odds=p/(1-p)*m
    q=odds/(1+odds)
    return -np.expm1((30-h)*np.log1p(-p)+h*np.log1p(-q))

def main():
    exposure_path=ROOT/'data/exp/revision_age_allocation/age_allocation_exposure_municipalities.parquet'
    paths=[health.OUTPUT,exposure_path]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    f=pd.read_parquet(health.OUTPUT).set_index('Municipality Code')
    e=pd.read_parquet(exposure_path)
    e=e.loc[e.scenario.eq('older_households')].set_index('Municipality Code')
    assert f.index.is_unique and e.index.is_unique and set(e.index)==set(f.index)
    n=e.loc[f.index,'older_exposure'].to_numpy(float)
    p=f['Baseline Daily Mortality Probability'].to_numpy(float)
    h=f['Expected High-Heat Scenario Days'].to_numpy(float)
    rows=[]; summaries=[]; metrics={}
    for multiplier in [.98,1.,1.03,1.07]:
        protected=risk(p,h,multiplier)
        unprotected=risk(p,h,multiplier*health.NO_AC_VS_AC_RELATIVE_OR)
        delta=unprotected-protected
        relative=(unprotected/protected-1)*100
        assert np.all((protected>0)&(unprotected<1)&(delta>=0))
        if multiplier==1.03:
            np.testing.assert_allclose(protected,f['Effective-Cooling 30-Day Mortality Risk'],rtol=0,atol=1e-12)
            np.testing.assert_allclose(unprotected,f['No-Effective-Cooling 30-Day Mortality Risk'],rtol=0,atol=1e-12)
        t=pd.DataFrame({'Municipality Code':f.index,'protected_heat_or':multiplier,'population':n,'protected_risk':protected,'unprotected_risk':unprotected,'incremental_risk_per100000':delta*1e5,'relative_burden_increase_percent':relative,'expected_excess_deaths':n*delta})
        metrics[multiplier]=t
        rows.append(t)
        summaries.append({'protected_heat_or':multiplier,'expected_protected_deaths':float(np.sum(n*protected)),'expected_excess_deaths':float(np.sum(n*delta)),'aggregate_relative_burden_increase_percent':float(np.sum(n*delta)/np.sum(n*protected)*100)})
    base=metrics[1.03]
    for s in summaries:
        t=metrics[s['protected_heat_or']]
        s['excess_deaths_change_percent']=float((t.expected_excess_deaths.sum()/base.expected_excess_deaths.sum()-1)*100)
        s['max_municipal_relative_change_percentage_points']=float((t.relative_burden_increase_percent-base.relative_burden_increase_percent).abs().max())
        for column in ['incremental_risk_per100000','expected_excess_deaths','relative_burden_increase_percent']:
            s[column+'_rank_changes']=int(t[column].rank().ne(base[column].rank()).sum())
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    OUT.mkdir(exist_ok=True,parents=True)
    pd.concat(rows,ignore_index=True).to_parquet(OUT/'protected_heat_multiplier_municipalities.parquet',index=False)
    report={'summaries':summaries,'protected_hashes':hashes,'population_total':float(n.sum()),'fixed_ror':health.NO_AC_VS_AC_RELATIVE_OR,'scope':'One-factor diagnostic at 0.98, 1.00, 1.03, 1.07. Source limits are not a joint CI or a Japanese-population effect range. Baseline and heat remain archived assumptions. Expected counts use newly selected demographic/structural experiment, not archived production counts.'}
    (OUT/'protected_heat_multiplier_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summaries,indent=2))

if __name__=='__main__': main()
