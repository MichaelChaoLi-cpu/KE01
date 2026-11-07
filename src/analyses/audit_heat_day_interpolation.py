"""Read-only-input diagnostics for mortality-model heat-day interpolation."""
from pathlib import Path
import sys
import json
import hashlib
import numpy as np
import pandas as pd
import geopandas as gpd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_cooling_loss_mortality_scenario as health
OUT=ROOT/'data/exp/revision_heat_diagnostics'

def main():
    paths=[health.HEAT_SOURCE,health.OUTPUT]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    daily=pd.read_parquet(health.HEAT_SOURCE)
    keys=['Station ID','Historical Year','Event Day']
    assert not daily.duplicated(keys).any()
    sizes=daily.groupby(keys[:2]).size()
    assert sizes.eq(30).all() and len(sizes)==85
    columns=['Daily Maximum Air Temperature C','Daily Minimum Air Temperature C','Hot Day Indicator','Hot Night Indicator']
    missing={c:int(daily[c].isna().sum()) for c in columns}
    unknown=daily['Hot Day Indicator'].isna()&daily['Hot Night Indicator'].isna()
    assert daily['Hot Day Indicator'].isna().equals(daily['Hot Night Indicator'].isna())
    # Explicitly reproduce the archived lower-bound treatment, not observed cool weather.
    daily['high_heat']=(daily['Hot Day Indicator'].fillna(0).astype(bool)|daily['Hot Night Indicator'].fillna(0).astype(bool)).astype(int)
    daily['high_heat_upper']=daily['high_heat'].where(~unknown,1)
    yearly=daily.groupby(['Station ID','Historical Year']).high_heat.sum().unstack()
    stations=health.station_high_heat_days().reset_index(drop=True)
    upper_values=daily.groupby('Station ID').high_heat_upper.sum()/5
    xy=np.column_stack([stations.geometry.x,stations.geometry.y])
    distance=np.linalg.norm(xy[:,None,:]-xy[None,:,:],axis=2)
    values=stations['Expected High-Heat Scenario Days'].to_numpy(float)
    predictions=[]
    for i in range(len(stations)):
        order=np.argsort(np.where(np.arange(len(stations))==i,np.inf,distance[i]))[:health.IDW_NEIGHBORS]
        assert np.all(distance[i,order]>0)
        predictions.append(np.average(values[order],weights=distance[i,order]**(-health.IDW_POWER)))
    errors=np.asarray(predictions)-values
    station_table=pd.DataFrame({'station':stations['Station ID'],'name':stations['Station Name'],'archived_lower_bound_mean_days':values,'loo_predicted_days':predictions,'error_days':errors})
    municipalities=gpd.read_parquet(health.OUTPUT).to_crs(health.MAP_CRS)
    estimates=health.interpolate_high_heat_days(municipalities,stations)
    upper_stations=stations.copy()
    upper_stations['Expected High-Heat Scenario Days']=upper_stations['Station ID'].map(upper_values)
    upper_estimates=health.interpolate_high_heat_days(municipalities,upper_stations)
    np.testing.assert_allclose(estimates,municipalities['Expected High-Heat Scenario Days'],rtol=0,atol=1e-9)
    centers=municipalities.geometry.centroid
    hull=stations.geometry.union_all().convex_hull
    distances=np.array([stations.geometry.distance(p).min()/1000 for p in centers])
    outside=np.array([not hull.covers(p) for p in centers])
    # IDW weights are fixed in time; compare mean of annual interpolations to interpolation of mean.
    annual=[]
    for year in yearly.columns:
        s=stations.copy()
        s['Expected High-Heat Scenario Days']=s['Station ID'].map(yearly[year])
        assert s['Expected High-Heat Scenario Days'].notna().all()
        annual.append(health.interpolate_high_heat_days(municipalities,s))
    np.testing.assert_allclose(np.mean(annual,axis=0),estimates,rtol=0,atol=1e-10)
    mt=pd.DataFrame({'Municipality Code':municipalities['Municipality Code'],'mean_heat_days':estimates,'missing_day_upper_bound':upper_estimates,'nearest_station_km':distances,'outside_station_convex_hull':outside})
    for year,x in zip(yearly.columns,annual):mt[f'heat_days_{year}']=x
    report={'daily_rows':len(daily),'stations':len(stations),'station_years':len(sizes),'days_each':30,'missing':missing,'years':list(map(int,yearly.columns)),
            'loo_mean_heat_days_mae':float(np.abs(errors).mean()),'loo_mean_heat_days_rmse':float(np.sqrt(np.mean(errors**2))),'loo_max_absolute_error_days':float(np.abs(errors).max()),
            'outside_hull_municipal_centroids':int(outside.sum()),'municipalities':len(mt),'nearest_station_max_km':float(distances.max()),
            'municipal_mean_heat_days_range':[float(estimates.min()),float(estimates.max())],
            'annual_heat_days_range':[float(np.min(annual)),float(np.max(annual))],
            'missing_day_max_municipal_mean_difference':float((upper_estimates-estimates).max()),
            'protected_hashes':hashes,'limits':'LOO concerns five-year mean threshold-day counts, not temperature or MODIS calibration accuracy. Hull test is geometric, not proof of inaccurate values. No mortality effect or baseline validation, no production modification.'}
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    OUT.mkdir(parents=True,exist_ok=True)
    daily.loc[unknown,keys+['Station Name','Historical Source Date']].to_parquet(OUT/'missing_station_days.parquet',index=False)
    station_table.to_parquet(OUT/'station_heat_day_loo.parquet',index=False)
    mt.to_parquet(OUT/'municipal_annual_heat_days.parquet',index=False)
    (OUT/'heat_day_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
