"""Extract archived official controls and test grid allocation feasibility.

No population allocation or production artifact is changed.
Source: https://www.e-stat.go.jp/dbview?sid=0003445263 (2020 Census 7-2).
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health

OUT = ROOT / 'data/exp/revision_age_allocation'

def main():
    source = OUT / 'sources/estat_0003445263_kumamoto_age65.json'
    result = json.loads(source.read_text())
    records = []
    for row in re.findall(r'<tr>(.*?)</tr>', result['table'], re.S):
        match = re.search(r'data-unique="(43\d{3})">\s*([^<]+)', row)
        if not match:
            continue
        values = re.findall(r'<td[^>]*>\s*([\d,]+)\s*</td>', row)
        assert len(values) == 3
        records.append([match[1], match[2].strip(), *[int(x.replace(',', '')) for x in values]])
    counts = ['all_age65', 'general_household_age65', 'institutional_household_age65']
    official = pd.DataFrame(records, columns=['Municipality Code', 'name', *counts])
    assert len(official) == 51 and official['Municipality Code'].is_unique
    assert (official[counts[0]] == official[counts[1]] + official[counts[2]]).all()
    wards = official['Municipality Code'].isin([f'4310{i}' for i in range(1, 6)])
    assert (official.loc[wards, counts].sum() == official.set_index('Municipality Code').loc['43100', counts]).all()
    municipal = official.loc[~wards & official['Municipality Code'].ne('43000')].copy()
    assert len(municipal) == 45
    assert (municipal[counts].sum() == official.set_index('Municipality Code').loc['43000', counts]).all()
    official['general_household_share_age65'] = official[counts[1]] / official[counts[0]]
    official.to_parquet(OUT / 'official_municipal_age65_controls.parquet', index=False)

    grid_path = ROOT / 'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet'
    frame = gpd.read_parquet(grid_path)
    polygons = gpd.read_parquet(ROOT / 'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet')
    frame = health.assign_municipalities(frame, polygons)
    # Each household containing an older person implies >=1 older general-household resident.
    frame['lower'] = frame['Households with Member Age 65+']
    # Groups without older general households cannot contain older general-household residents.
    frame['upper'] = frame['Population Age 65+'].where(frame['lower'].gt(0), 0)
    grouped = frame.groupby('Municipality Code')[['lower', 'upper', 'Population Age 65+']].sum().reset_index()
    checked = municipal.merge(grouped, on='Municipality Code', how='outer', validate='one_to_one', indicator=True)
    assert checked['_merge'].eq('both').all()
    checked = checked.drop(columns='_merge')
    checked['grid_minus_official_all_age65'] = checked['Population Age 65+'] - checked['all_age65']
    checked['feasible'] = checked['general_household_age65'].between(checked['lower'], checked['upper'])
    checked.to_parquet(OUT / 'municipal_age65_control_feasibility.parquet', index=False)
    report = {
        'source_url': 'https://www.e-stat.go.jp/dbview?sid=0003445263',
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'grid_sha256': hashlib.sha256(grid_path.read_bytes()).hexdigest(),
        'official_prefecture': dict(zip(counts, map(int, municipal[counts].sum()))),
        'municipalities': len(checked),
        'feasible_municipalities': int(checked['feasible'].sum()),
        'nonmatching_grid_municipal_totals': int(checked['grid_minus_official_all_age65'].ne(0).sum()),
        'max_absolute_municipal_difference': float(checked['grid_minus_official_all_age65'].abs().max()),
        'grid_all_age65_sum': int(frame['Population Age 65+'].sum()),
        'infeasible': checked.loc[~checked['feasible']].to_dict('records'),
        'interpretation': 'Feasibility only. Representative-point municipality assignment is not a census crosswalk. Grid estimates and allocation weights are not yet fitted.'
    }
    (OUT / 'municipal_control_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
