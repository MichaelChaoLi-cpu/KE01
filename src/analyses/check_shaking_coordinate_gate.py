"""Stop allocation if plausible coordinate-datum interpretations change categories."""
import json
from pathlib import Path
import numpy as np
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'data/exp/revision_shaking'

def nearest(xy, stations):
    return np.concatenate([((xy[k:k+512,None,:]-stations[None,:,:])**2).sum(axis=2).argmin(axis=1)
                           for k in range(0,len(xy),512)])

def main():
    frame=gpd.read_parquet(ROOT/'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet')
    points=frame.to_crs(6670).geometry.representative_point()
    xy=np.column_stack([points.x,points.y])
    rows=sorted(json.loads((OUT/'sources/jma_event_20260728162715.json').read_text())['res']['int'],key=lambda r:r['code'])
    cats=np.array([r['int'] for r in rows])
    results={}
    base=None
    for crs in [4326,4612,6668]:
        pts=gpd.GeoSeries(gpd.points_from_xy([float(r['lon']) for r in rows],[float(r['lat']) for r in rows]),crs=crs).to_crs(6670)
        idx=nearest(xy,np.column_stack([pts.x,pts.y]))
        if base is None: base=idx
        changed=cats[idx]!=cats[base]
        results[str(crs)]={'changed_station_groups':int((idx!=base).sum()),'changed_category_groups':int(changed.sum()),
            'population_in_changed_groups':float(frame.loc[changed,'Total Population'].sum()),
            'changed_groups':[{'code':str(frame.iloc[i]['Disclosure Group Code']),'baseline_station':rows[base[i]]['code'],'alternative_station':rows[idx[i]]['code'],'baseline_category':cats[base[i]],'alternative_category':cats[idx[i]]} for i in np.flatnonzero(changed)]}
    report={'passed':all(v['changed_category_groups']==0 for v in results.values()),'comparisons_to_epsg4326':results,'interpretation':'Sensitivity check, not verification of source datum.'}
    (OUT/'coordinate_gate.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__': main()
