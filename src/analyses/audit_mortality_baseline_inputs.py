"""Reconcile baseline deaths against archived raw tables, without rewriting inputs."""
from pathlib import Path
import sys
import hashlib
import json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_municipality_mortality_baseline as source
OUT=ROOT/'data/exp/revision_mortality_audit'

def main():
    paths=[source.BASELINE_OUTPUT,source.ANNUAL_OUTPUT,*sorted(ROOT.glob(source.RAW_PATTERN))]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    parsed=source.parse_annual_deaths()
    saved=pd.read_parquet(source.ANNUAL_OUTPUT)
    keys=['Municipality Code','Calendar Year','Age Group']
    a=parsed.set_index(keys)['All-Cause Deaths'].sort_index()
    b=saved.set_index(keys)['All-Cause Deaths'].sort_index()
    pd.testing.assert_series_equal(a,b,check_dtype=False)
    baseline=pd.read_parquet(source.BASELINE_OUTPUT)
    calculated=baseline['All-Cause Deaths']/baseline['Population at Risk']/5*100000
    np.testing.assert_allclose(calculated,baseline['Baseline Mortality Rate per 100,000'],rtol=1e-12)
    older=baseline.loc[baseline['Age Group'].eq('65+')]
    assert len(older)==45 and older['Municipality Code'].is_unique
    totals=parsed.loc[parsed['Age Group'].eq('65+')].groupby('Calendar Year')['All-Cause Deaths'].sum()
    report={'annual_rows_reproduced':len(a),'baseline_rows':len(baseline),'age65_municipalities':len(older),
            'annual_age65_deaths':{str(k):int(v) for k,v in totals.items()},
            'age65_population_denominator_total':float(older['Population at Risk'].sum()),
            'age65_annual_rate_per100000_range':[float(older['Baseline Mortality Rate per 100,000'].min()),float(older['Baseline Mortality Rate per 100,000'].max())],
            'input_sha256':hashes,
            'limits':'Arithmetic and archived-table reconciliation only. Deaths among Japanese nationals versus all-resident census denominator; fixed 2020 population over 2020-2024; annual not seasonal, all-resident not general-household-specific baseline. No new numerator/denominator chosen.'}
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'baseline_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'},indent=2))

if __name__=='__main__':main()
