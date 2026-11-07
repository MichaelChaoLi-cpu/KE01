"""Reviewer 3/C8: fixed-model neighboring-station test; isolated experimental IO."""
from pathlib import Path
import argparse
import concurrent.futures
import json
import re
import sys
import urllib.request
from unittest.mock import patch
import numpy as np
import pandas as pd
import geopandas as gpd
from recalculate_integrated_revision import ROOT, digest
import figure_historical_modis_and_station_calibrated_heat_spatial_heterogeneity as fig
sys.path.insert(0, str(ROOT / 'src/preprocessing'))
import preprocess_modis_historical_heat_spatial_grid as satellite
import preprocess_jma_historical_heat_spatial_stations as jma

OUT = ROOT / 'data/exp/revision_expanded_modis_support'


def fetch(url, path):
    if not path.exists():
        with urllib.request.urlopen(url, timeout=40) as response:
            data = response.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return path


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    boundary = gpd.read_file(fig.BOUNDARY_PATH, columns=['geometry']).to_crs(6670).geometry.union_all()
    records = []
    for pref in ['82', '83', '84', '85', '87', '88']:
        url = f'https://www.data.jma.go.jp/stats/etrn/select/prefecture.php?prec_no={pref}&block_no=&year=2025&month=8&day=&view=p1'
        html = fetch(url, OUT / 'sources' / f'prefecture_{pref}.html').read_text()
        seen = set()
        for call in re.findall(r"viewPoint\(([^)]*)\)", html):
            args = re.findall(r"'([^']*)'", call)
            if len(args) < 18 or args[1] in seen or args[11] != '1':
                continue
            seen.add(args[1])
            if int(args[15]) < 2026:
                continue
            lat, lon = float(args[4])+float(args[5])/60, float(args[6])+float(args[7])/60
            point = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs=4326).to_crs(6670).iloc[0]
            distance = boundary.distance(point)/1000
            if distance <= 50:
                records.append({'id': pref+'-'+args[1], 'pref': pref, 'block': args[1], 'kind': args[0]+'1', 'name': args[2], 'lat': lat, 'lon': lon, 'distance_km': distance, 'directory_url': url})
    assert records
    (OUT / 'station_inventory.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    jobs = []
    for station in records:
        for year in range(2021, 2026):
            for month in [7, 8]:
                url = f"https://www.data.jma.go.jp/stats/etrn/view/daily_{station['kind']}.php?prec_no={station['pref']}&block_no={station['block']}&year={year}&month={month}&day=&view=p1"
                jobs.append((url, OUT / 'sources' / station['id'] / f'{year}_{month:02d}.html'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(lambda job: fetch(*job), jobs))
    rows = []
    for station in records:
        for year in range(2021, 2026):
            for month in [7, 8]:
                for cells in jma.table_rows(OUT / 'sources' / station['id'] / f'{year}_{month:02d}.html'):
                    day = int(cells[0])
                    if (month == 7 and day < 28) or (month == 8 and day > 26):
                        continue
                    ix = jma.VALUE_INDEX[station['kind']]
                    rows.append({**station, 'year': year, 'month': month, 'day': day,
                                 'maximum': jma.number(cells[ix['maximum_temperature']]),
                                 'minimum': jma.number(cells[ix['minimum_temperature']])})
    daily = pd.DataFrame(rows)
    assert not daily.duplicated(['id', 'year', 'month', 'day']).any()
    daily.to_parquet(OUT / 'neighbor_daily.parquet', index=False)
    # Reuse archived complete HDF tiles and all existing QA/averaging rules.
    expanded = gpd.GeoDataFrame(geometry=[boundary.buffer(50000)], crs=6670)
    destination = OUT / 'expanded_modis.parquet'
    with patch.object(satellite.gpd, 'read_file', return_value=expanded), patch.object(satellite, 'OUTPUT_PATH', destination):
        satellite.main()
    print(f'Prepared {len(records)} neighboring stations, {len(daily)} days and expanded MODIS grid.', flush=True)


def evaluate():
    original = gpd.read_parquet(fig.MODIS_PATH).to_crs(6670)
    expanded = gpd.read_parquet(OUT / 'expanded_modis.parquet').to_crs(6670)
    baseline_grid = original.set_index('MODIS Pixel ID')
    expanded_grid = expanded.set_index('MODIS Pixel ID')
    assert baseline_grid.index.is_unique and expanded_grid.index.is_unique
    assert set(baseline_grid.index) <= set(expanded_grid.index)
    for spec in fig.PERIODS:
        for column in [spec.lst_column, spec.count_column, spec.product_column, spec.display_lst_column]:
            np.testing.assert_allclose(baseline_grid[column], expanded_grid.loc[baseline_grid.index, column], equal_nan=True)
    daily = pd.read_parquet(fig.STATION_PATH)
    neighbors = pd.read_parquet(OUT / 'neighbor_daily.parquet')
    results, station_outputs, eligibility = [], [], []
    for spec, model, variable in zip(fig.PERIODS, ['combined_p2_q5', 'satellite_only'], ['maximum', 'minimum']):
        original_stations = fig.station_targets(daily, spec)
        eligible = expanded.loc[expanded[spec.lst_column].notna() & expanded[spec.count_column].ge(5) & expanded[spec.product_column].eq(2)]
        centers = eligible.geometry.centroid
        xy = np.column_stack([centers.x, centers.y])
        lst_values = eligible[spec.lst_column].to_numpy(float)
        # Equal comparison: retain original county sampling, sample only new stations outside.
        eligible_original = original.loc[original[spec.lst_column].notna() & original[spec.count_column].ge(5) & original[spec.product_column].eq(2)]
        oc = eligible_original.geometry.centroid
        oxy = np.column_stack([oc.x, oc.y])
        sx = np.column_stack([original_stations.geometry.x, original_stations.geometry.y])
        nearest = ((sx[:, None]-oxy[None, :])**2).sum(axis=2).argmin(axis=1)
        slst = eligible_original[spec.lst_column].to_numpy(float)[nearest]
        target = original_stations['Station Target Air Temperature C'].to_numpy(float)
        usable = neighbors.loc[neighbors.maximum.notna() & neighbors.minimum.notna()]
        counts = usable.groupby(['id', 'year']).size().unstack(fill_value=0)
        # Require all 150 days for new stations to avoid introducing availability imbalance.
        approved = counts.index[counts.reindex(columns=range(2021, 2026), fill_value=0).eq(30).all(axis=1)]
        new = usable.loc[usable.id.isin(approved)].groupby('id').agg(lat=('lat','first'),lon=('lon','first'),distance_km=('distance_km','first'),target=(variable,'mean'))
        points = gpd.GeoSeries(gpd.points_from_xy(new.lon, new.lat),crs=4326).to_crs(6670)
        nx = np.column_stack([points.x, points.y])
        distances = np.sqrt(((nx[:, None]-xy[None, :])**2).sum(axis=2))
        nearest = distances.argmin(axis=1)
        new['lst'] = lst_values[nearest]
        new['pixel_distance_m'] = distances[np.arange(len(new)), nearest]
        new['x'], new['y'] = nx[:, 0], nx[:, 1]
        eligibility.append({'period': spec.key, 'directory_candidates': int(neighbors.id.nunique()), 'complete_150_day_stations': len(new), 'eligible_pixel_within5km': int(new.pixel_distance_m.le(5000).sum())})
        new.to_parquet(OUT / f'{spec.key}_neighbor_eligibility.parquet')
        baseline_pred = fig.candidate_predictions(sx, slst, target, model)
        boundary = np.array([not original_stations.drop(original_stations.index[i]).geometry.union_all().convex_hull.covers(original_stations.geometry.iloc[i]) for i in range(17)])
        display = original.loc[original[spec.display_lst_column].notna()]
        dc = display.geometry.centroid
        for radius in [0, 30, 50]:
            selected = new.loc[(new.distance_km <= radius) & (new.pixel_distance_m <= 5000)] if radius else new.iloc[:0]
            extra_xy = selected[['x','y']].to_numpy(float)
            prediction = []
            for held in range(17):
                keep = np.arange(17) != held
                train_xy = np.vstack([sx[keep], extra_xy])
                train_lst = np.r_[slst[keep], selected.lst]
                train_target = np.r_[target[keep], selected.target]
                prediction.append(fig.fit_predict_surface(train_xy, train_lst, train_target, sx[[held]], slst[[held]], model)[0])
            prediction = np.array(prediction)
            if radius == 0:
                np.testing.assert_allclose(prediction, baseline_pred, atol=1e-10)
            error = prediction-target
            all_xy = np.vstack([sx, extra_xy])
            hull = gpd.GeoSeries(gpd.points_from_xy(all_xy[:,0], all_xy[:,1]),crs=6670).union_all().convex_hull
            all_lst = np.r_[slst, selected.lst]
            values = display[spec.display_lst_column]
            results.append({'period': spec.key, 'radius_km': radius, 'additional_stations': len(selected),
                            'county_rmse_C': float(np.sqrt(np.mean(error**2))), 'county_mae_C': float(np.abs(error).mean()),
                            'boundary_rmse_C': float(np.sqrt(np.mean(error[boundary]**2))),
                            'outside_hull_pixel_fraction': float((~dc.map(hull.covers)).mean()),
                            'outside_sampled_lst_fraction': float(((values<all_lst.min())|(values>all_lst.max())).mean())})
            station_outputs.append(pd.DataFrame({'station': original_stations['Station ID'], 'period':spec.key, 'radius_km':radius, 'error_C':error, 'boundary_station':boundary}))
    pd.concat(station_outputs, ignore_index=True).to_parquet(OUT / 'county_heldout_errors.parquet',index=False)
    protected = json.loads((ROOT/'data/exp/revision_integrated_calculation/validation.json').read_text())['protected_sha256']
    assert all(digest(ROOT/p)==sha for p,sha in protected.items())
    report={'results':results, 'eligibility': eligibility, 'original_modis_values_reproduced':True, 'formal_assets_unchanged':True, 'limits':'Fixed existing models, original 17 county targets held out one at a time; not independent model-selection validation. New stations require complete 150-day temperature pairs. Current station directory does not certify historic location stability. No production or mortality-model change.'}
    report['source_hashes']={str(p.relative_to(ROOT)):digest(p) for p in (OUT/'sources').rglob('*.html')}
    report['script_sha256']=digest(Path(__file__))
    (OUT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(results,indent=2),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true')
    args=parser.parse_args()
    if args.prepare: prepare()
    evaluate()
