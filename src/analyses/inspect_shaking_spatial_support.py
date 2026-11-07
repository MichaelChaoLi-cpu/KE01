"""Describe station proximity only; no hazard interpolation or loss estimation."""
import json
from hashlib import sha256
from pathlib import Path
import geopandas as gpd
import numpy as np
from shapely.geometry import MultiPoint

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_shaking'
SOURCE = ROOT / 'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet'


def main():
    frame = gpd.read_parquet(SOURCE)
    points = frame.to_crs(6670).geometry.representative_point()
    xy = np.column_stack([points.x, points.y])
    event = OUT / 'sources/jma_event_20260728162715.json'
    rows = json.loads(event.read_text())['res']['int']
    results = {}
    for label, subset in [('all_returned_stations', rows), ('kumamoto_only', [r for r in rows if r['code'].startswith('74')])]:
        # WGS84 assignment is provisional: source API does not declare datum.
        stations = gpd.GeoSeries(gpd.points_from_xy([float(r['lon']) for r in subset], [float(r['lat']) for r in subset]), crs=4326).to_crs(6670)
        station_xy = np.column_stack([stations.x, stations.y])
        distance = np.concatenate([
            np.sqrt(((xy[start:start+512, None, :] - station_xy[None, :, :])**2).sum(axis=2).min(axis=1))
            for start in range(0, len(xy), 512)
        ])
        distance = distance / 1000
        hull = MultiPoint(station_xy).convex_hull
        outside = np.array([not hull.covers(p) for p in points])
        results[label] = {
            'stations':len(subset),
            'nearest_station_distance_km_quantiles': dict(zip(['min','p50','p90','p95','max'],np.quantile(distance,[0,.5,.9,.95,1]).tolist())),
            'groups_outside_station_convex_hull':int(outside.sum()),
            'population_weighted_distance_km':float(np.average(distance, weights=frame['Total Population'])),
            'population_fraction_beyond_10km':float(frame.loc[distance>10,'Total Population'].sum()/frame['Total Population'].sum()),
            'older_population_fraction_beyond_10km':float(frame.loc[distance>10,'Population Age 65+'].sum()/frame['Population Age 65+'].sum()),
        }
    report = {'disclosure_groups':len(frame), 'source_crs':str(frame.crs), 'diagnostics':results,
              'caveats':['API coordinate datum unverified; WGS84 used provisionally for descriptive distances only.',
                         '10 km is a descriptive threshold, not a validated adequacy cutoff.',
                         'Convex-hull membership and proximity do not establish interpolation accuracy.',
                         'Representative points, not complete polygon coverage, are tested.'],
              'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in [SOURCE,event]}}
    (OUT/'spatial_support.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
