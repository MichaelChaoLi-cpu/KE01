"""Isolated demographic update with unchanged engineering parameter bundles."""
from pathlib import Path
import sys
import json
import hashlib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src/preprocessing'))
import preprocess_emergency_cooling_power_scenarios as engineering
SOURCE=ROOT/'data/exp/revision_age_allocation/age_allocation_exposure_municipalities.parquet'
OUT=ROOT/'data/exp/revision_engineering_trial'

def main():
    protected=[SOURCE,Path(engineering.__file__),engineering.SOURCE,engineering.OUTPUT]
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    population=pd.read_parquet(SOURCE)
    assert len(population)==135
    assert not population.duplicated(['scenario','Municipality Code']).any()
    frames=[]
    for params in engineering.SCENARIOS:
        t=population[['scenario','Municipality Code','name','older_exposure']].copy()
        area=engineering.MINIMUM_SHELTER_AREA_M2_PER_PERSON
        density=params['Cooling Load Density W per m2']
        cop=params['Scenario Cooling System COP']
        factor=params['Scenario Peak Load Diversity Factor']
        hours=params['Scenario Cooling Operating Hours per Day']
        t['engineering_scenario']=params['Power Demand Scenario']
        t['area_m2_per_person']=area
        t['load_density_W_per_m2']=density
        t['cop']=cop
        t['diversity_factor']=factor
        t['assumed_hours_per_day']=hours
        t['thermal_kW']=t.older_exposure*area*density/1000
        t['electric_kW']=t.thermal_kW*factor/cop
        t['daily_kWh']=t.electric_kW*hours
        np.testing.assert_allclose(t.electric_kW,t.older_exposure*(area*density*factor/cop/1000),rtol=1e-12)
        assert t[['thermal_kW','electric_kW','daily_kWh']].ge(0).all().all()
        for _,group in t.groupby('scenario'):
            assert group.electric_kW.rank().equals(group.older_exposure.rank())
        frames.append(t)
    result=pd.concat(frames,ignore_index=True)
    assert len(result)==405
    totals=result.groupby(['scenario','engineering_scenario'])[['older_exposure','thermal_kW','electric_kW','daily_kWh']].sum()
    assert len(totals)==9
    for demographic in population.scenario.unique():
        subset=totals.loc[demographic]
        assert subset.loc['Low','electric_kW']<subset.loc['Central','electric_kW']<subset.loc['High','electric_kW']
        assert subset.loc['Low','daily_kWh']<subset.loc['Central','daily_kWh']<subset.loc['High','daily_kWh']
    primary=totals.loc[('older_households','Central')]
    sensitivity=totals.loc[('residual_capacity','Central')]
    previous=totals.loc[('previous_all_resident_rule','Central')]
    report={'rows':len(result),'bundles':9,'protected_sha256':hashes,
            'primary_central':primary.to_dict(),'sensitivity_central':sensitivity.to_dict(),
            'same_structural_model_previous_age_central':previous.to_dict(),
            'primary_vs_previous_age_percent_change':float((primary.electric_kW/previous.electric_kW-1)*100),
            'sensitivity_vs_primary_percent_change':float((sensitivity.electric_kW/primary.electric_kW-1)*100),
            'interpretation':'Unchanged engineering assumptions; simplified constant scenario power over assumed hours. Not measured electricity or verified supply deficit. Rankings follow population mechanically under spatially uniform positive engineering multipliers. Prior-age comparator uses the same newly selected structural model, not archived production.'}
    assert hashes=={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    OUT.mkdir(parents=True,exist_ok=True)
    result.to_parquet(OUT/'municipal_cooling_power_trial.parquet',index=False)
    totals.reset_index().to_parquet(OUT/'cooling_power_trial_totals.parquet',index=False)
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(totals.to_string())
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
