"""Isolated approved primary chain and one-factor sensitivities (no production writes)."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/preprocessing'))
import preprocess_grid_exposure_estimates as housing
import preprocess_cooling_loss_mortality_scenario as health
import preprocess_emergency_cooling_power_scenarios as power
from check_heat_risk_aggregation import risk

OUT = ROOT / 'data/exp/revision_integrated_calculation'
AGE = ROOT / 'data/exp/revision_age_allocation'
HEAT = ROOT / 'data/exp/revision_heat_diagnostics/municipal_annual_heat_days.parquet'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    inputs = [housing.SOURCE, AGE / 'bounded_grid_age65_estimates.parquet',
              AGE / 'official_municipal_age65_controls.parquet', HEAT,
              health.MORTALITY_SOURCE, health.HEAT_SOURCE]
    # Protect every existing formal processed/result asset, not only directly read inputs.
    protected = sorted(set(inputs + [p for folder in ['data/processed', 'data/results']
                                    for p in (ROOT / folder).rglob('*') if p.is_file()]))
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in protected}
    g = gpd.read_parquet(housing.SOURCE)
    a = pd.read_parquet(inputs[1]).set_index('Disclosure Group Code')
    assert a.index.is_unique and g['Disclosure Group Code'].is_unique
    assert set(a.index) == set(g['Disclosure Group Code'])
    a = a.loc[g['Disclosure Group Code']].reset_index()
    h = g['General Households'].to_numpy(float)
    w = h * np.exp(-housing.epicentral_distance_km(g) / 20)
    loss = w / w.sum() * 303.5
    share = np.divide(loss, h, out=np.zeros(len(h)), where=h > 0)
    assert np.all(loss[h == 0] == 0) and np.all(loss <= h)
    np.testing.assert_allclose(loss.sum(), 303.5, atol=1e-9)
    control = pd.read_parquet(inputs[2]).set_index('Municipality Code')
    heat = pd.read_parquet(HEAT).set_index('Municipality Code')
    baseline = pd.read_parquet(health.MORTALITY_SOURCE)
    baseline = baseline.loc[baseline['Age Group'].eq('65+')].set_index('Municipality Code')
    assert heat.index.is_unique and baseline.index.is_unique and len(heat) == len(baseline) == 45
    assert set(heat.index) == set(baseline.index) == set(a['Municipality Code'])
    grid_frames, municipal_frames, power_frames, risk_frames = [], [], [], []
    for demographic in ['older_households', 'residual_capacity']:
        population = a['representative_point__' + demographic].to_numpy(float)
        exposure = population * share
        assert np.all((exposure >= 0) & (exposure <= population))
        np.testing.assert_allclose(population.sum(), 495748, atol=1e-7)
        grid = a[['Disclosure Group Code', 'Municipality Code']].copy()
        grid['demographic_scenario'] = demographic
        grid['general_household_age65_estimate'] = population
        grid['functional_loss'] = loss
        grid['older_exposure'] = exposure
        grid['no_placement_person_days'] = exposure * 30
        grid['effective_cooled_capacity'] = np.nan
        grid['verified_capacity_gap'] = np.nan
        grid_frames.append(grid)
        m = grid.groupby('Municipality Code')[['functional_loss', 'older_exposure',
                                              'no_placement_person_days']].sum()
        m['name'] = control['name']
        m['demographic_scenario'] = demographic
        m['effective_cooled_capacity'] = np.nan
        m['verified_capacity_gap'] = np.nan
        municipal_frames.append(m.reset_index())
        for params in power.SCENARIOS:
            t = m.reset_index().copy()
            t['engineering_scenario'] = params['Power Demand Scenario']
            t['thermal_kW'] = t.older_exposure * 3.5 * params['Cooling Load Density W per m2'] / 1000
            t['electric_kW'] = t.thermal_kW * params['Scenario Peak Load Diversity Factor'] / params['Scenario Cooling System COP']
            t['daily_kWh'] = t.electric_kW * params['Scenario Cooling Operating Hours per Day']
            power_frames.append(t)
        p = baseline.loc[m.index, 'Baseline Mortality Rate per 100,000'].to_numpy(float) / 100000 / 365.25
        days = heat.loc[m.index, 'mean_heat_days'].to_numpy(float)
        upper = heat.loc[m.index, 'missing_day_upper_bound'].to_numpy(float)
        years = heat.loc[m.index, [f'heat_days_{y}' for y in range(2021, 2026)]].to_numpy(float)
        assert np.all((p > 0) & (p < 1)) and np.all((days >= 0) & (days <= upper) & (upper <= 30))
        cases = [('main_lower_missing', 1.03, 1.08, days),
                 ('missing_all_hot', 1.03, 1.08, upper),
                 ('ror_low', 1.03, 1.01, days), ('ror_high', 1.03, 1.15, days),
                 ('protected_or_0.98', .98, 1.08, days),
                 ('protected_or_1.00', 1., 1.08, days),
                 ('protected_or_1.07', 1.07, 1.08, days),
                 ('mean_annual_risk', 1.03, 1.08, years)]
        # Demographic sensitivity is one factor only: no crossed uncertainty envelope.
        for label, effect, ror, heat_days in cases if demographic == 'older_households' else cases[:1]:
            daily = p[:, None] if heat_days.ndim == 2 else p
            rp, ru = risk(daily, heat_days, effect), risk(daily, heat_days, effect * ror)
            if heat_days.ndim == 2:
                rp, ru = rp.mean(axis=1), ru.mean(axis=1)
            assert np.all((rp > 0) & (ru >= rp) & (ru < 1))
            t = m.reset_index().copy()
            t['health_scenario'] = label
            t['protected_heat_or'], t['ror'] = effect, ror
            t['protected_risk'], t['unprotected_risk'] = rp, ru
            t['incremental_risk_per100000'] = (ru - rp) * 100000
            t['relative_burden_increase_percent'] = (ru / rp - 1) * 100
            t['expected_protected_deaths'] = t.older_exposure * rp
            t['expected_excess_deaths'] = t.older_exposure * (ru - rp)
            risk_frames.append(t)
    municipal = pd.concat(municipal_frames, ignore_index=True)
    engineering = pd.concat(power_frames, ignore_index=True)
    mortality = pd.concat(risk_frames, ignore_index=True)
    primary = municipal.loc[municipal.demographic_scenario.eq('older_households')]
    central = engineering.loc[engineering.demographic_scenario.eq('older_households') & engineering.engineering_scenario.eq('Central')]
    main_risk = mortality.loc[mortality.demographic_scenario.eq('older_households') & mortality.health_scenario.eq('main_lower_missing')]
    np.testing.assert_allclose(primary.older_exposure.sum(), 202.04193624297827, atol=1e-8)
    np.testing.assert_allclose(central.electric_kW.sum(), 28.42730042962604, atol=1e-6)
    np.testing.assert_allclose(main_risk.expected_excess_deaths.sum(), .035650857, atol=1e-9)
    assert len(municipal) == 90 and len(engineering) == 270 and len(mortality) == 405
    assert municipal.verified_capacity_gap.isna().all()
    summaries = mortality.groupby(['demographic_scenario', 'health_scenario'])[['expected_protected_deaths', 'expected_excess_deaths']].sum()
    summaries['aggregate_relative_burden_increase_percent'] = summaries.expected_excess_deaths / summaries.expected_protected_deaths * 100
    assert hashes == {str(p.relative_to(ROOT)): digest(p) for p in protected}
    OUT.mkdir(parents=True, exist_ok=True)
    pd.concat(grid_frames, ignore_index=True).to_parquet(OUT / 'grid_chain.parquet', index=False)
    municipal.to_parquet(OUT / 'municipal_need.parquet', index=False)
    engineering.to_parquet(OUT / 'municipal_power.parquet', index=False)
    mortality.to_parquet(OUT / 'municipal_health.parquet', index=False)
    summaries.reset_index().to_parquet(OUT / 'health_totals.parquet', index=False)
    report = {'decision': 'KILA-D-20261002-011', 'protected_sha256': hashes,
              'code_sha256': {str(p.relative_to(ROOT)): digest(p) for p in [Path(__file__), Path(housing.__file__), Path(power.__file__), Path(health.__file__), ROOT / 'src/analyses/check_heat_risk_aggregation.py']},
              'primary_exposure': float(primary.older_exposure.sum()),
              'central_electric_kW': float(central.electric_kW.sum()),
              'central_daily_kWh': float(central.daily_kWh.sum()),
              'primary_expected_excess_deaths': float(main_risk.expected_excess_deaths.sum()),
              'formal_assets_unchanged': True,
              'pending': ['Structural hybrid/shaking and later-snapshot reconnection', 'MODIS-specific coverage diagnostic', 'Formal figure/table reconciliation', 'Exact manuscript proposal approval'],
              'interpretation': 'Conditional screening scenarios, not observed deaths or verified cooling-capacity deficits. Annual all-resident baseline and externally transferred interaction require stated assumptions. Separate one-factor sensitivities are not a joint CI.'}
    (OUT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(summaries.to_string())
    print(json.dumps({k: v for k, v in report.items() if 'sha256' not in k}, indent=2))


if __name__ == '__main__':
    main()
