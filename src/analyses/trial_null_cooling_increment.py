"""Approved R1/C6 null-interaction benchmark; never writes formal outputs."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from trial_protected_heat_multiplier import risk

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_null_cooling_increment'


def main():
    integrated = ROOT / 'data/exp/revision_integrated_calculation/municipal_health.parquet'
    source = ROOT / 'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet'
    protected = [integrated] + [p for folder in ['data/processed', 'data/results']
                               for p in (ROOT / folder).rglob('*') if p.is_file()]
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    f = pd.read_parquet(source).set_index('Municipality Code')
    m = pd.read_parquet(integrated)
    m = m.loc[m.demographic_scenario.eq('older_households') &
              m.health_scenario.eq('main_lower_missing')].set_index('Municipality Code')
    assert f.index.is_unique and m.index.is_unique and len(f) == len(m) == 45
    assert set(f.index) == set(m.index)
    m = m.loc[f.index]
    p = f['Baseline Daily Mortality Probability'].to_numpy(float)
    h = f['Expected High-Heat Scenario Days'].to_numpy(float)
    n = m.older_exposure.to_numpy(float)
    assert np.all(np.isfinite(p)) and np.all((p > 0) & (p < 1))
    assert np.all(np.isfinite(h)) and np.all((h >= 0) & (h <= 30))
    assert np.all(np.isfinite(n)) and np.all(n >= 0)
    rp = risk(p, h, 1.03)
    main = risk(p, h, 1.03 * 1.08)
    np.testing.assert_allclose(rp, m.protected_risk, rtol=0, atol=1e-12)
    np.testing.assert_allclose(main, m.unprotected_risk, rtol=0, atol=1e-12)
    null = risk(p, h, 1.03 * 1.0)
    assert np.array_equal(rp, null) and np.all(rp > 0)
    table = pd.DataFrame({'Municipality Code': f.index, 'older_exposure': n,
                          'protected_risk': rp, 'null_unprotected_risk': null,
                          'incremental_risk_per100000': (null-rp)*1e5,
                          'relative_burden_increase_percent': (null/rp-1)*100,
                          'expected_excess_deaths': n*(null-rp)})
    report = {'decision': 'KILA-D-20261003-003', 'municipalities': len(f),
              'population_total': float(n.sum()), 'rho': 1.0, 'protected_heat_or': 1.03,
              'expected_deaths_each_state': float(np.sum(n*rp)),
              'expected_excess_deaths': float(np.sum(n*(null-rp))),
              'aggregate_relative_increment_percent': float(np.sum(n*(null-rp))/np.sum(n*rp)*100),
              'main_expected_excess_deaths_reproduced': float(np.sum(n*(main-rp))),
              'main_relative_increment_percent_reproduced': float(np.sum(n*(main-rp))/np.sum(n*rp)*100),
              'interpretation': 'Algebraic no-increment benchmark, not zero total mortality, local effect validation, a confidence interval or rank robustness.',
              'protected_hashes': hashes}
    assert hashes == {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    OUT.mkdir(parents=True, exist_ok=True)
    table.to_parquet(OUT / 'municipal_null_benchmark.parquet', index=False)
    (OUT / 'validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'protected_hashes'}, indent=2))


if __name__ == '__main__':
    main()
