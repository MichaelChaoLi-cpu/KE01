"""Verify archived round-one outputs for round-two clarification; no model rerun.

Run with the project's Python environment (pandas, numpy and pyarrow required).
Only verification receipts under data/exp/rev2_retrospective_verification are written.
"""
from pathlib import Path
import ast
import argparse
import hashlib
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'data/exp/revision_integrated_calculation'
AGE = ROOT / 'data/exp/revision_age_allocation'
OUT = ROOT / 'data/exp/rev2_retrospective_verification'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reader', choices=['pandas', 'duckdb'], default='pandas')
    args = parser.parse_args()
    def read_parquet(path):
        if args.reader == 'pandas':
            return pd.read_parquet(path)
        import duckdb
        with duckdb.connect() as connection:
            result = connection.execute('SELECT * FROM read_parquet(?)', [str(path)])
            return pd.DataFrame(result.fetchall(), columns=[c[0] for c in result.description])
    files = [BASE / n for n in ['structural_totals.parquet',
             'structural_municipalities.parquet', 'grid_chain.parquet',
             'municipal_power.parquet', 'validation.json', 'extended_validation.json']]
    files += [AGE / 'bounded_grid_age65_estimates.parquet',
              AGE / 'official_municipal_age65_controls.parquet',
              ROOT / 'src/analyses/extend_integrated_revision_diagnostics.py',
              ROOT / 'src/analyses/recalculate_integrated_revision.py',
              ROOT / 'src/preprocessing/preprocess_emergency_cooling_power_scenarios.py',
              ROOT / 'Rev/docs/snapshot-verification.md',
              ROOT / 'Rev2/origin/KE01.docx',
              ROOT / 'Rev2/revision/KE01.rev2.markup.docx']
    before = {str(p.relative_to(ROOT)): sha(p) for p in files}
    main_manifest = json.loads((BASE / 'validation.json').read_text())
    extra_manifest = json.loads((BASE / 'extended_validation.json').read_text())
    for p in files:
        key = str(p.relative_to(ROOT))
        expected = (main_manifest.get('protected_sha256', {}).get(key)
                    or main_manifest.get('code_sha256', {}).get(key)
                    or extra_manifest.get('source_sha256', {}).get(key))
        if expected:
            assert before[key] == expected, f'Historical source mismatch: {key}'

    totals = read_parquet(BASE / 'structural_totals.parquet').set_index('scenario')
    municipal = read_parquet(BASE / 'structural_municipalities.parquet')
    grid = read_parquet(BASE / 'grid_chain.parquet')
    grid = grid.loc[grid.demographic_scenario.eq('older_households')].copy()
    age = read_parquet(AGE / 'bounded_grid_age65_estimates.parquet')
    age = age.set_index('Disclosure Group Code').loc[grid['Disclosure Group Code']]
    assert age.index.is_unique and grid['Disclosure Group Code'].is_unique
    controls = read_parquet(AGE / 'official_municipal_age65_controls.parquet')
    population = age['representative_point__older_households'].to_numpy(float)
    households = age['General Households'].to_numpy(float)
    np.testing.assert_allclose(population, grid.general_household_age65_estimate)
    estimated = pd.Series(population, index=grid['Municipality Code']).groupby(level=0).sum()
    target = controls.set_index('Municipality Code').loc[estimated.index, 'general_household_age65']
    np.testing.assert_allclose(estimated, target, atol=1e-7, rtol=0)
    assert len(estimated) == 45
    assert np.all(population >= age['Households with Member Age 65+'].to_numpy(float) - 1e-7)
    assert np.all(population <= age['Population Age 65+'].to_numpy(float) + 1e-7)

    # Read parameter definitions without importing or executing production scripts.
    tree = ast.parse(files[10].read_text())
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for name in node.targets:
                if isinstance(name, ast.Name) and name.id in {'MINIMUM_SHELTER_AREA_M2_PER_PERSON', 'SCENARIOS'}:
                    constants[name.id] = ast.literal_eval(node.value)
    central = next(p for p in constants['SCENARIOS'] if p['Power Demand Scenario'] == 'Central')
    area = constants['MINIMUM_SHELTER_AREA_M2_PER_PERSON']
    assert area == 3.5
    assert [central[k] for k in ['Cooling Load Density W per m2',
            'Scenario Cooling System COP', 'Scenario Peak Load Diversity Factor',
            'Scenario Cooling Operating Hours per Day']] == [134., 3., .9, 18.]
    per_person_kw = area * 134 / 1000 * .9 / 3
    factor = (2270 + .5 * 6357) / (181 + .5 * 245)
    rows = []
    for label, multiplier, loss_total in [('primary', 1., 303.5),
            ('later_snapshot_primary', factor, 5448.5)]:
        loss = grid.functional_loss.to_numpy(float) * multiplier
        assert np.all(loss >= 0) and np.all(loss <= households + 1e-9)
        assert np.all(loss[households == 0] == 0)
        share = np.divide(loss, households, out=np.zeros_like(loss), where=households > 0)
        exposure = population * np.minimum(share, 1.)
        np.testing.assert_allclose(loss.sum(), loss_total, atol=1e-8, rtol=0)
        expected = pd.DataFrame({'Municipality Code': grid['Municipality Code'].to_numpy(),
                 'functional_loss': loss, 'older_exposure': exposure})
        expected = expected.groupby('Municipality Code').sum()
        expected['central_electric_kW'] = expected.older_exposure * per_person_kw
        expected['central_daily_kWh'] = expected.central_electric_kW * 18
        archived = municipal.loc[municipal.scenario.eq(label)].set_index('Municipality Code')
        assert len(archived) == 45 and archived.index.is_unique
        for col in expected:
            np.testing.assert_allclose(expected[col], archived.loc[expected.index, col], atol=1e-8, rtol=1e-10)
            np.testing.assert_allclose(expected[col].sum(), totals.loc[label, col], atol=1e-8, rtol=1e-10)
        rows.append({'scenario': label, **expected.sum().to_dict(),
                     'maximum_household_loss_share': float(share.max()),
                     'household_cap_violations': int(np.sum(loss > households + 1e-9)),
                     'municipalities_checked': len(expected)})
    base = rows[0]
    for key, displayed in [('functional_loss', 303.5), ('older_exposure', 202.042),
                           ('central_electric_kW', 28.427), ('central_daily_kWh', 511.691)]:
        assert round(base[key], 3) == displayed, (key, base[key], displayed)
    for key in ['functional_loss', 'older_exposure', 'central_electric_kW', 'central_daily_kWh']:
        np.testing.assert_allclose(rows[1][key] / rows[0][key], factor, atol=1e-10)
    power = read_parquet(BASE / 'municipal_power.parquet')
    power = power.loc[power.demographic_scenario.eq('older_households') & power.engineering_scenario.eq('Central')]
    np.testing.assert_allclose(power.electric_kW.sum(), base['central_electric_kW'])
    np.testing.assert_allclose(power.daily_kWh.sum(), base['central_daily_kWh'])
    assert before == {str(p.relative_to(ROOT)): sha(p) for p in files}
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'generated_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Read-only verification of archived fixed-method scenarios, not a new fitted analysis.',
              'source_sha256': before, 'inputs_unchanged': True,
              'main_snapshot': '2026-08-01 17:00 JST',
              'later_snapshot': '2026-09-24 17:00 JST; FDMA Report 65',
              'snapshot_factor': factor, 'central_parameters': central,
              'reader': args.reader,
              'area_m2_per_person': area, 'municipal_controls_reproduced': True,
              'main_manuscript_numbers_reproduced': True, 'rows': rows,
              'limitations': 'Fixed spatial weights, bounded age allocation and engineering inputs. Later counts remain provisional; proportionality here follows from nonbinding caps and does not validate damage geography or actual supply.'}
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['snapshot_factor', 'rows', 'inputs_unchanged']}, indent=2))


if __name__ == '__main__':
    main()
