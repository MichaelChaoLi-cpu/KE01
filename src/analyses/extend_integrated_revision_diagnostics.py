"""Reconnect approved structural alternatives and audit MODIS spatial support."""
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd
import geopandas as gpd
from recalculate_integrated_revision import ROOT, AGE, OUT, housing, health, digest
from analyze_denominator_correction import redistribute
import analyze_shaking_sensitivity as shaking
import figure_historical_modis_and_station_calibrated_heat_spatial_heterogeneity as modis


def structural():
    g = gpd.read_parquet(housing.SOURCE)
    a = pd.read_parquet(AGE / 'bounded_grid_age65_estimates.parquet').set_index('Disclosure Group Code').loc[g['Disclosure Group Code']]
    h = g['General Households'].to_numpy(float)
    n = a['representative_point__older_households'].to_numpy(float)
    codes = a['Municipality Code'].to_numpy()
    distance = housing.epicentral_distance_km(g)
    scenarios = housing.scenario_surfaces(g, distance, 181, 245)
    corrected = np.array([redistribute(s, h > 0, s.sum()) for s in scenarios])
    median = np.median(corrected, axis=0)
    hybrid = np.clip(median * 303.5 / median.sum(), corrected.min(axis=0), corrected.max(axis=0))
    primary = h * np.exp(-distance / 20)
    primary = primary / primary.sum() * 303.5
    variants = [('primary', primary, 303.5), ('corrected_hybrid', hybrid, 303.5),
                ('later_snapshot_primary', primary * (2270 + .5 * 6357) / 303.5, 2270 + .5 * 6357)]
    # Reuse the approved coordinate and nearest-category conventions; no refitting.
    assert shaking.coordinate_gate()['passed']
    stations = sorted(json.loads((shaking.OUT / 'sources/jma_event_20260728162715.json').read_text())['res']['int'], key=lambda r: r['code'])
    points = gpd.GeoSeries(gpd.points_from_xy([float(r['lon']) for r in stations], [float(r['lat']) for r in stations]), crs=4326).to_crs(6670)
    centers = g.to_crs(6670).geometry.representative_point()
    indices = shaking.nearest(np.column_stack([centers.x, centers.y]), np.column_stack([points.x, points.y]))
    categories = np.array([shaking.CATEGORIES.index(r['int']) for r in stations])[indices]
    for shape, (mu, sigma) in shaking.SHAPES.items():
        for endpoint, values in [('lower', shaking.LOW), ('upper_limit', shaking.HIGH)]:
            weight = np.array([.5 * math.erfc(-(v-mu)/sigma/math.sqrt(2)) for v in values])[categories]
            for proxy in shaking.PROXIES:
                for theta in [0., .5, 1.]:
                    total = 181 + 245 * theta
                    label = f'{shape}|{endpoint}|{shaking.PROXIES.index(proxy)}|{theta}'
                    variants.append((label, shaking.allocate(g[proxy].to_numpy(float)*weight, h, total), total))
    health_frame = pd.read_parquet(OUT / 'municipal_health.parquet')
    health_frame = health_frame.loc[health_frame.demographic_scenario.eq('older_households') & health_frame.health_scenario.eq('main_lower_missing')].set_index('Municipality Code')
    tables, summaries = [], []
    reference = None
    for label, loss, total in variants:
        assert np.all((loss >= 0) & (loss <= h + 1e-9)) and np.all(loss[h == 0] == 0)
        np.testing.assert_allclose(loss.sum(), total, rtol=0, atol=1e-8)
        exposure = n * np.divide(loss, h, out=np.zeros_like(h), where=h > 0)
        t = pd.DataFrame({'Municipality Code': codes, 'functional_loss': loss, 'older_exposure': exposure}).groupby('Municipality Code').sum().reindex(health_frame.index)
        assert len(t) == 45 and t.notna().all().all()
        t['central_electric_kW'] = t.older_exposure * 3.5 * 134 / 1000 * .9 / 3
        t['central_daily_kWh'] = t.central_electric_kW * 18
        t['expected_protected_deaths'] = t.older_exposure * health_frame.protected_risk
        t['expected_excess_deaths'] = t.older_exposure * (health_frame.unprotected_risk - health_frame.protected_risk)
        if reference is None:
            reference = t.copy()
            np.testing.assert_allclose(t.older_exposure, health_frame.older_exposure, atol=1e-10)
        row = {'scenario': label, **t.sum().to_dict()}
        row['relative_burden_increase_percent'] = t.expected_excess_deaths.sum() / t.expected_protected_deaths.sum() * 100
        for metric in ['older_exposure', 'expected_excess_deaths']:
            row[metric + '_spearman'] = float(t[metric].rank().corr(reference[metric].rank()))
            row[metric + '_max_rank_shift'] = float((t[metric].rank()-reference[metric].rank()).abs().max())
            row[metric + '_top5_overlap'] = len(set(t[metric].nlargest(5).index) & set(reference[metric].nlargest(5).index))
        t['scenario'] = label
        tables.append(t.reset_index()); summaries.append(row)
    assert len(summaries) == 57
    combined = pd.concat(tables, ignore_index=True)
    indexed = combined.set_index(['scenario', 'Municipality Code'])
    previous = pd.read_csv(shaking.OUT / 'scenario_municipalities.csv', dtype={'Municipality Code': str}).set_index(['scenario', 'Municipality Code'])
    np.testing.assert_allclose(indexed.loc[previous.index, 'functional_loss'], previous.loss, rtol=1e-10, atol=1e-10)
    previous = pd.read_csv(ROOT / 'data/exp/revision_denominator_correction/municipality_comparison.csv', dtype={'Municipality Code': str})
    previous = previous.loc[previous.variant.eq('rebuilt_corrected_hybrid')].set_index('Municipality Code')
    np.testing.assert_allclose(indexed.loc['corrected_hybrid'].loc[previous.index, 'functional_loss'], previous.loss, rtol=1e-10, atol=1e-10)
    combined.to_parquet(OUT / 'structural_municipalities.parquet', index=False)
    pd.DataFrame(summaries).to_parquet(OUT / 'structural_totals.parquet', index=False)
    return summaries


def modis_support():
    grid = gpd.read_parquet(modis.MODIS_PATH).to_crs(modis.MAP_CRS)
    daily = pd.read_parquet(modis.STATION_PATH)
    population = gpd.read_parquet(modis.POPULATION_PATH).to_crs(modis.MAP_CRS)
    population_weights = modis.assign_population_to_grid(grid, population)
    reports, station_frames = [], []
    for spec in modis.PERIODS:
        result = modis.calibrate_period(grid, daily, population_weights, spec)
        s = result.stations
        xy = np.column_stack([s.geometry.x, s.geometry.y])
        target = s['Station Target Air Temperature C'].to_numpy(float)
        lst = s['Sampled Land Surface Temperature C'].to_numpy(float)
        predicted = modis.candidate_predictions(xy, lst, target, result.model_name)
        error = predicted - target
        np.testing.assert_allclose(np.sqrt(np.mean(error**2)), result.selected_rmse)
        # Boundary stations: outside the convex hull of all remaining stations.
        boundary = np.array([not s.drop(s.index[i]).geometry.union_all().convex_hull.covers(s.geometry.iloc[i]) for i in range(len(s))])
        t = s.drop(columns='geometry').copy()
        t['period'] = spec.key; t['loo_error_C'] = error; t['boundary_station'] = boundary
        station_frames.append(t)
        display = result.grid.copy()
        centers = display.geometry.centroid
        hull = s.geometry.union_all().convex_hull
        outside = ~centers.map(hull.covers).to_numpy()
        distance = np.sqrt(((np.column_stack([centers.x, centers.y])[:, None, :] - xy[None, :, :])**2).sum(axis=2)).min(axis=1)/1000
        weights = display['Population Weight'].to_numpy(float)
        report = {'period': spec.key, 'model': result.model_name, 'supported': bool(result.supported),
                  'display_pixels': len(display), 'full_grid_pixels': len(grid),
                  'selected_loo_rmse_C': result.selected_rmse, 'mean_only_rmse_C': result.benchmark_rmse,
                  'boundary_station_count': int(boundary.sum()),
                  'boundary_station_rmse_C': float(np.sqrt(np.mean(error[boundary]**2))),
                  'interior_station_rmse_C': float(np.sqrt(np.mean(error[~boundary]**2))),
                  'outside_hull_pixel_fraction': float(outside.mean()),
                  'outside_hull_represented_population_fraction': float(weights[outside].sum()/weights.sum()),
                  'represented_population': float(weights.sum()),
                  'max_nearest_station_km': float(distance.max()),
                  'low_support_pixel_fraction': float(display['LST Low Support'].mean()),
                  'outside_station_lst_range_pixel_fraction': float(display[result.extrapolation_column].mean())}
        display['outside_station_hull'] = outside
        display['nearest_station_km'] = distance
        display.drop(columns='geometry_centroid').to_parquet(OUT / f'modis_{spec.key}_support.parquet', index=False)
        reports.append(report)
    pd.concat(station_frames, ignore_index=True).to_parquet(OUT / 'modis_station_diagnostics.parquet', index=False)
    return reports


def main():
    manifest = json.loads((OUT / 'validation.json').read_text())
    hashes = manifest['protected_sha256']
    assert all(digest(ROOT / p) == sha for p, sha in hashes.items())
    extra = [modis.MODIS_PATH, modis.STATION_PATH, modis.POPULATION_PATH,
             shaking.OUT / 'sources/jma_event_20260728162715.json',
             ROOT / 'src/analyses/analyze_damage_snapshot_sensitivity.py',
             ROOT / 'Rev/docs/snapshot-verification.md',
             shaking.OUT / 'scenario_municipalities.csv',
             ROOT / 'data/exp/revision_denominator_correction/municipality_comparison.csv',
             ROOT / 'src/analyses/analyze_denominator_correction.py', Path(shaking.__file__), Path(modis.__file__), Path(__file__)]
    source_hashes = {str(p.relative_to(ROOT)): digest(p) for p in extra}
    structures = structural()
    reports = modis_support()
    assert all(digest(ROOT / p) == sha for p, sha in {**hashes, **source_hashes}.items())
    output = {'structural_scenarios': len(structures), 'municipal_rows': len(structures)*45,
              'modis_diagnostics': reports, 'source_sha256': source_hashes, 'formal_assets_unchanged': True,
              'limitations': 'No independent damage validation; shaking curves are hypothetical. Later snapshot is a total-only retrospective sensitivity. MODIS LOO errors are conditional on model selection using the same LOO scores, not nested independent validation. Pixel fractions are not area fractions; population fractions concern represented population only. Neither geometric extrapolation nor predictor extrapolation proves local error. MODIS calibration is separate from mortality heat-day IDW.'}
    (OUT / 'extended_validation.json').write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))
    print(pd.DataFrame(structures).iloc[:3].to_string(index=False))


if __name__ == '__main__':
    main()
