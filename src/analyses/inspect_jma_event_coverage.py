"""Validate downloaded JMA event records; no intensity interpolation or model fitting."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_shaking'
SRC = OUT / 'sources'


def main():
    event_path = SRC / 'jma_event_20260728162715.json'
    event = json.loads(event_path.read_text())['res']
    cities = {x['code']: x['name'] for x in json.loads((SRC / 'jma_city_catalog.json').read_text())}
    catalog = {x['code']: x for x in json.loads((SRC / 'jma_station_catalog.json').read_text())}
    rows = event['int']
    assert event['hyp'][0]['id'] == '20260728162715'
    assert len({x['code'] for x in rows}) == len(rows)
    valid_categories = {'震度１','震度２','震度３','震度４','震度５弱','震度５強','震度６弱','震度６強','震度７'}
    for row in rows:
        assert row['int'] in valid_categories
        assert -90 <= float(row['lat']) <= 90 and -180 <= float(row['lon']) <= 180
    # JMA's prefecture selector assigns 74 to Kumamoto (not a JIS municipality code).
    local = [dict(x, city_name=cities[x['code'][:5]]) for x in rows if x['code'].startswith('74')]
    assert not any('富合' in x['name'] for x in local)
    covered = {x['code'][:5] for x in local}
    report = {
        'generated_utc': datetime.now(timezone.utc).isoformat(),
        'source': 'https://www.data.jma.go.jp/eqdb/data/shindo/index.html#20260728162715',
        'request': {'url':'https://www.data.jma.go.jp/eqdb/data/shindo/api/', 'method':'POST', 'form':{'mode':'event','id':'20260728162715'}},
        'hypocenter': event['hyp'],
        'total_event_station_records': len(rows),
        'kumamoto_station_records': len(local),
        'kumamoto_categories': dict(Counter(x['int'] for x in local)),
        'kumamoto_reporting_units': len(covered),
        'covered_reporting_units': {k:cities[k] for k in sorted(covered)},
        'catalog_units_without_event_record': {k:v for k,v in cities.items() if k.startswith('74') and k not in covered},
        'event_codes_not_in_catalog': [x['code'] for x in rows if x['code'] not in catalog],
        'tomiai_withdrawn_record_absent': True,
        'valid_coordinates': True,
        'sha256': {p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(SRC.glob('*.json'))},
        'limitations': [
            'Returned observations are not a census of all functioning sensors; no record is not zero intensity.',
            'Station catalog includes historical sites and has no event-date activity interval; it is not a completeness denominator.',
            'Categorical intensity only; no continuous instrumental intensity inferred.',
            'Coordinates are taken directly from the event API; datum not declared in this response.',
            'Current retrieval may incorporate revisions after the early-information cutoff.',
            'Reporting units include Kumamoto wards; do not treat them as independent municipalities.',
        ],
    }
    (OUT / 'kumamoto_event_stations.json').write_text(json.dumps(local, ensure_ascii=False, indent=2)+'\n')
    (OUT / 'coverage_validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['total_event_station_records','kumamoto_station_records','kumamoto_categories','kumamoto_reporting_units','catalog_units_without_event_record','event_codes_not_in_catalog']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
