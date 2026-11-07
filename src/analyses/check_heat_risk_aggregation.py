"""Check archived missing cells and nonlinear risk aggregation without new effects."""
from pathlib import Path
import sys
import json
import hashlib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health
import preprocess_jma_historical_heat_spatial_stations as jma
OUT=ROOT/'data/exp/revision_heat_diagnostics'

def risk(p,h,multiplier):
    odds=p/(1-p)*multiplier
    q=odds/(1+odds)
    return -np.expm1((30-h)*np.log1p(-p)+h*np.log1p(-q))

def main():
    raw=[]
    paths=[health.OUTPUT,OUT/'municipal_annual_heat_days.parquet']
    for slug,year,days,kind in [('hitoyoshi',2025,[16,17,18],'s1'),('taimei',2024,[25],'a1')]:
        path=ROOT/f'data/raw/weather/jma_daily_html/{slug}/{year}_08.html'
        paths.append(path)
        for cells in jma.table_rows(path):
            if int(cells[0]) in days:
                ix=jma.VALUE_INDEX[kind]
                row={'station':slug,'date':f'{year}-08-{int(cells[0]):02d}','raw_maximum_cell':cells[ix['maximum_temperature']],'raw_minimum_cell':cells[ix['minimum_temperature']]}
                row['max_parses_missing']=jma.number(row['raw_maximum_cell']) is None
                row['min_parses_missing']=jma.number(row['raw_minimum_cell']) is None
                raw.append(row)
    assert len(raw)==4
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    original=pd.read_parquet(health.OUTPUT).set_index('Municipality Code')
    heat=pd.read_parquet(paths[1]).set_index('Municipality Code').loc[original.index]
    p=original['Baseline Daily Mortality Probability'].to_numpy(float)
    h=heat['mean_heat_days'].to_numpy(float)
    years=heat[[f'heat_days_{y}' for y in range(2021,2026)]].to_numpy(float)
    protected=health.WITH_AC_EXTREME_HEAT_OR
    unprotected=protected*health.NO_AC_VS_AC_RELATIVE_OR
    rp=risk(p,h,protected); ru=risk(p,h,unprotected)
    np.testing.assert_allclose(rp,original['Effective-Cooling 30-Day Mortality Risk'],rtol=0,atol=1e-12)
    np.testing.assert_allclose(ru,original['No-Effective-Cooling 30-Day Mortality Risk'],rtol=0,atol=1e-12)
    ap=risk(p[:,None],years,protected).mean(axis=1)
    au=risk(p[:,None],years,unprotected).mean(axis=1)
    delta=(ru-rp)*100000
    annual_delta=(au-ap)*100000
    mean_day_relative=(ru/rp-1)*100
    ratio_mean_relative=(au/ap-1)*100
    average_relative=((risk(p[:,None],years,unprotected)/risk(p[:,None],years,protected)-1)*100).mean(axis=1)
    upper=heat['missing_day_upper_bound'].to_numpy(float)
    upper_delta=(risk(p,upper,unprotected)-risk(p,upper,protected))*100000
    result=pd.DataFrame({'Municipality Code':original.index,'mean_day_incremental_risk_per100000':delta,'mean_annual_incremental_risk_per100000':annual_delta,'annual_minus_mean_day_per100000':annual_delta-delta,'missing_hot_upper_incremental_risk_per100000':upper_delta})
    result['mean_day_relative_increase_percent']=mean_day_relative
    result['ratio_of_mean_risks_increase_percent']=ratio_mean_relative
    result['mean_annual_relative_increase_percent']=average_relative
    report={'raw_cells':raw,'maximum_absolute_annual_aggregation_difference_per100000':float(np.max(np.abs(annual_delta-delta))),
            'maximum_relative_annual_aggregation_difference_percent':float(np.max(np.abs(annual_delta/delta-1))*100),
            'incremental_risk_rank_changes':int((pd.Series(delta).rank()!=pd.Series(annual_delta).rank()).sum()),
            'max_ratio_of_mean_relative_difference_percentage_points':float(np.max(np.abs(ratio_mean_relative-mean_day_relative))),
            'max_mean_annual_relative_difference_percentage_points':float(np.max(np.abs(average_relative-mean_day_relative))),
            'missing_day_max_incremental_risk_difference_per100000':float(np.max(upper_delta-delta)),
            'protected_hashes':hashes,
            'scope':'Arithmetic diagnostic conditional on existing effects, baseline and lower-bound missing-day treatment. Ratios of average risks are distinct from averages of annual risk ratios. No external validity claim, imputation or production change.'}
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result.to_parquet(OUT/'annual_risk_aggregation_comparison.parquet',index=False)
    (OUT/'risk_aggregation_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
