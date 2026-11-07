"""Audit administrative attribution; area shares are geometric, not population."""
from pathlib import Path
import sys
import json
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_age_allocation'

def main():
    g=gpd.read_parquet(ROOT/'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet').to_crs(health.MAP_CRS)
    m=gpd.read_parquet(ROOT/'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet')[['Municipality Code','geometry']].to_crs(g.crs)
    g=health.assign_municipalities(g,m).reset_index(drop=True)
    g['gid']=np.arange(len(g))
    parts=gpd.overlay(g[['gid','geometry']],m,how='intersection',keep_geom_type=True)
    parts['area']=parts.area
    parts=parts.loc[parts.area.gt(0)].copy()
    area=parts.groupby('gid')['area'].sum()
    parts['share']=parts.area/parts.gid.map(area)
    counts=parts.groupby('gid').size()
    # Report both all positive fragments and >=1% fragments, avoiding sliver claims.
    substantive=parts.loc[parts.share.ge(.01)].groupby('gid').size()
    largest=parts.sort_values(['gid','area','Municipality Code']).drop_duplicates('gid',keep='last').set_index('gid')['Municipality Code']
    assert len(largest)==len(g)
    g['largest_area_municipality']=g.gid.map(largest)
    g['intersected_municipalities']=g.gid.map(counts)
    g['municipalities_at_least_one_percent']=g.gid.map(substantive)
    official=pd.read_parquet(OUT/'official_municipal_age65_controls.parquet').set_index('Municipality Code')
    reports={}
    for label,col in [('representative_point','Municipality Code'),('largest_area','largest_area_municipality')]:
        v=g.groupby(col)['Population Age 65+'].sum()
        difference=v-official.loc[v.index,'all_age65']
        relative=difference/official.loc[v.index,'all_age65']
        reports[label]={'nonmatching':int(difference.ne(0).sum()),'maximum_absolute_difference':float(difference.abs().max()),'sum_absolute_differences':float(difference.abs().sum()),'maximum_absolute_relative_difference':float(relative.abs().max())}
    crossing=g.intersected_municipalities.gt(1)
    changed=g['Municipality Code'].ne(g.largest_area_municipality)
    report={'groups':len(g),'cross_boundary_groups_any_positive_area':int(crossing.sum()),'cross_boundary_groups_at_least_one_percent':int(g.municipalities_at_least_one_percent.gt(1).sum()),'age65_in_any_cross_boundary_groups':float(g.loc[crossing,'Population Age 65+'].sum()),'groups_with_changed_assignment':int(changed.sum()),'age65_in_changed_groups':float(g.loc[changed,'Population Age 65+'].sum()),'comparison':reports,'source_has_municipality_code':False,'conclusion':'Neither geometric rule is an exact population crosswalk. Intersection area is not population share. No grid population was allocated or official total rescaled.'}
    g.loc[crossing|changed,['Disclosure Group Code','Municipality Code','largest_area_municipality','intersected_municipalities','municipalities_at_least_one_percent','Population Age 65+','General Households','Households with Member Age 65+']].to_parquet(OUT/'boundary_groups.parquet',index=False)
    parts[['gid','Municipality Code','area','share']].to_parquet(OUT/'boundary_intersections.parquet',index=False)
    (OUT/'boundary_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
