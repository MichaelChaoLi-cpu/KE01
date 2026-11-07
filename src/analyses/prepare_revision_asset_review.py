"""Build isolated, source-reusing revision figures/tables; never replace production.

Run: .venv/bin/python src/analyses/prepare_revision_asset_review.py
The distance-ensemble envelope retains the existing pointwise convention with
zero-household eligibility corrected. Shaking and later totals remain separate.
"""
from pathlib import Path
import json
import importlib
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.text import Text
from openpyxl import load_workbook
from PIL import Image
from recalculate_integrated_revision import ROOT, OUT as INPUT, housing, power, digest
from analyze_denominator_correction import redistribute
import municipality_table_common as common

OUT = ROOT / 'data/exp/revision_asset_review'
LOSS = 'Expected Functionally Lost Residences'
OLDER = 'Estimated Affected Population Age 65+'
DAYS = 'No-Placement Unprotected Older-Person-Days'
REL = 'Cooling-Loss Relative 30-Day Mortality Burden Increase %'
RISK = 'Cooling-Loss Incremental Mortality Risk per 100,000'
EXCESS = 'Incremental Cooling-Loss-Related Excess Deaths'
UNCOOLED = 'No-Effective-Cooling 30-Day Mortality Risk'


def read_primary(name):
    d = pd.read_parquet(INPUT / (name + '.parquet'))
    return d.loc[d.demographic_scenario.eq('older_households')].copy()


def build_inputs():
    base = gpd.read_parquet(housing.SOURCE)
    chain = read_primary('grid_chain').set_index('Disclosure Group Code')
    assert chain.index.is_unique and set(chain.index) == set(base['Disclosure Group Code'])
    chain = chain.loc[base['Disclosure Group Code']]
    h = base['General Households'].to_numpy(float)
    old = housing.scenario_surfaces(base, housing.epicentral_distance_km(base), 181, 245)
    scenarios = np.array([redistribute(s, h > 0, s.sum()) for s in old])
    assert scenarios.shape == (27, len(base)) and np.all(scenarios <= h + 1e-10)
    age_per_household = np.divide(chain.general_household_age65_estimate.to_numpy(float), h,
                                 out=np.zeros(len(h)), where=h > 0)
    # Keep only compatible descriptive fields, never stale old-model results.
    saved = gpd.read_parquet(common.GRID_SOURCE).set_index('Disclosure Group Code').loc[chain.index]
    grid = saved[['geometry', 'Nearest Designated Shelter ID',
                  'Nearest Designated Shelter Distance m', 'Damage Evidence Cutoff',
                  'Epicentral Distance km']].reset_index()
    grid['Municipality Code'] = chain['Municipality Code'].to_numpy()
    grid[LOSS] = chain.functional_loss.to_numpy()
    grid[OLDER] = chain.older_exposure.to_numpy()
    for suffix, values in [(' Lower Bound', scenarios.min(axis=0)),
                           (' Upper Bound', scenarios.max(axis=0))]:
        grid[LOSS + suffix] = values
        grid[OLDER + suffix] = values * age_per_household
    for suffix in ['', ' Lower Bound', ' Upper Bound']:
        grid[DAYS + suffix] = grid[OLDER + suffix] * 30
    grid['Structural Housing Loss Central Total Residences'] = 303.5
    grid['Functional Housing Loss Status'] = 'conditional_primary_allocation'
    grid['Estimation Status'] = 'housing_loss_related_older_population'
    grid['Effective Cooled Capacity'] = np.nan
    grid['Cooling Capacity Gap'] = np.nan
    grid['Cooling Protection Scenario Status'] = 'no_verified_placement_demand_side_bound'
    np.testing.assert_allclose(grid[LOSS].sum(), 303.5, atol=1e-8)
    np.testing.assert_allclose(grid[OLDER].sum(), 202.04193624297827, atol=1e-8)
    for col in [LOSS, OLDER]:
        assert (grid[col+' Lower Bound'] <= grid[col]+1e-12).all()
        assert (grid[col] <= grid[col+' Upper Bound']+1e-12).all()
    original_health = gpd.read_parquet(common.MORTALITY_SOURCE).set_index('Municipality Code')
    geo = original_health[['Municipality', 'geometry']].copy()
    health = read_primary('municipal_health')
    main = health.loc[health.health_scenario.eq('main_lower_missing')].set_index('Municipality Code').loc[geo.index]
    mortality = geo.copy()
    heat = pd.read_parquet(ROOT/'data/exp/revision_heat_diagnostics/municipal_annual_heat_days.parquet').set_index('Municipality Code')
    mortality['Expected High-Heat Scenario Days'] = heat.mean_heat_days
    mortality['Baseline Mortality Rate per 100,000'] = original_health['Baseline Mortality Rate per 100,000']
    mortality[DAYS] = main.no_placement_person_days
    mortality['Effective-Cooling 30-Day Mortality Risk'] = main.protected_risk
    for label, suffix in [('main_lower_missing', ''), ('ror_low', ' Lower 95% CI'), ('ror_high', ' Upper 95% CI')]:
        d = health.loc[health.health_scenario.eq(label)].set_index('Municipality Code').loc[geo.index]
        for target, source in [(UNCOOLED, 'unprotected_risk'), (RISK, 'incremental_risk_per100000'),
                               (REL, 'relative_burden_increase_percent'), (EXCESS, 'expected_excess_deaths')]:
            mortality[target+suffix] = d[source]
    mortality['Cooling-Loss Mortality Scenario Status'] = 'literature_anchored_no_verified_placement_planning_scenario'
    mortality = mortality.reset_index()
    p = read_primary('municipal_power').merge(geo.reset_index(), on='Municipality Code', validate='many_to_one')
    p = p.rename(columns={'engineering_scenario':'Power Demand Scenario', 'older_exposure':OLDER,
                         'thermal_kW':'Cooling Thermal Load kW', 'electric_kW':'Required Peak Cooling Electric Power kW',
                         'daily_kWh':'Required Daily Cooling Electricity kWh'})
    for params in power.SCENARIOS:
        mask = p['Power Demand Scenario'].eq(params['Power Demand Scenario'])
        for key,value in params.items():
            p.loc[mask,key] = value
    p['Minimum Shelter Living Area m2 per Person'] = 3.5
    p['Cooling Thermal Load W per Person'] = 3.5*p['Cooling Load Density W per m2']
    p['Cooling Power Scenario Status'] = 'demand_side_only_no_verified_supply'
    p['Verified Available Electric Power kW'] = np.nan
    p['Emergency Cooling Power Gap kW'] = np.nan
    p = gpd.GeoDataFrame(p, geometry='geometry', crs=geo.crs)
    for name,frame in [('grid',grid),('power',p),('health',mortality)]:
        frame.to_parquet(OUT/'inputs'/f'{name}.parquet', index=False)
    master = mortality.drop(columns='geometry').merge(
        grid.groupby('Municipality Code')[common.HOUSING_COLUMNS].sum(),on='Municipality Code',validate='one_to_one')
    central = p.loc[p['Power Demand Scenario'].eq('Central')].set_index('Municipality Code')
    for col in ['Required Peak Cooling Electric Power kW','Required Daily Cooling Electricity kWh']:
        master[col+' (Central)'] = master['Municipality Code'].map(central[col])
    assert len(master)==45 and master[common.HOUSING_COLUMNS+common.HEALTH_COLUMNS].notna().all().all()
    check = read_primary('municipal_need').set_index('Municipality Code')
    np.testing.assert_allclose(master.set_index('Municipality Code').loc[check.index,OLDER],check.older_exposure)
    return grid,p,mortality,master,geo.reset_index()


def align_review_frames(fig, kind):
    """Align visible frames after equal-aspect maps and colorbars settle."""
    fig.canvas.draw()
    panels = fig.axes[:3]
    reference = panels[1].get_position().frozen()
    for ax in panels:
        box = ax.get_position().frozen()
        if kind == 0:
            ax.set_position([box.x0, reference.y0, reference.width, reference.height])
        elif ax is panels[2]:
            # Reduce the bar panel footprint while sharing the map frame edges.
            ax.set_position([box.x0 + 0.025, reference.y0,
                             box.width - 0.025, reference.height])
        ax.set_frame_on(True)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#303A40')
            spine.set_linewidth(0.85)
    fig.canvas.draw()
    bounds = [ax.get_position() for ax in panels]
    assert np.ptp([b.y0 for b in bounds]) < 1e-8
    assert np.ptp([b.y1 for b in bounds]) < 1e-8


def figures(grid,p,mortality,geo, selected=None):
    slugs = ['functional_housing_loss_and_older_person_exposure',
             'older_person_cooling_protection_need_and_placement_deficit',
             'emergency_cooling_electricity_requirement_distribution',
             'cooling_loss_related_incremental_mortality_risk_distribution']
    for i,slug in enumerate(slugs):
        if selected is not None and i not in selected:
            continue
        m = importlib.import_module('figure_'+slug)
        if i==0:
            m.GRID_PATH = OUT/'inputs/grid.parquet'
            args = m.load_inputs();m.validate_figure_inputs(args[0]); fig=m.make_figure(*args)
            snapshot=m.latest_official_snapshot(args[1])
            assert snapshot['Full Collapse Buildings']==181 and snapshot['Half Collapse Buildings']==245
        elif i==1:
            m.SCENARIO_PATH=OUT/'inputs/grid.parquet'
            args=m.load_inputs();m.validate_inputs(args[0],args[1]);fig=m.make_figure(*args)
        elif i==2:
            m.validate_inputs(p); fig=m.make_figure(p,geo.to_crs(m.MAP_CRS))
        else:
            m.validate_inputs(mortality);fig=m.make_figure(mortality.to_crs(m.MAP_CRS))
        for obj in fig.findobj(match=Text):
            text=obj.get_text().replace('95% effect CI:', 'Effect-parameter range:')
            text=text.replace('(central)', '(primary)').replace('central total', 'primary total')
            obj.set_text(text)
        if i in (0, 2):
            align_review_frames(fig, i)
        path=OUT/'figures'/('Figure_'+slug+'.png')
        fig.savefig(path,dpi=400,bbox_inches='tight');plt.close(fig)
        with Image.open(path) as im:
            assert min(im.info['dpi'])>399
            im.thumbnail((1800,900));im.save(OUT/'previews'/(slug+'.png'))
        print('Figure:',slug,flush=True)


def tables(master):
    slugs=['municipality_housing_loss_and_older_person_cooling_need_summary',
           'municipality_cooling_electricity_planning_summary',
           'municipality_cooling_loss_health_risk_summary']
    for slug in slugs:
        m=importlib.import_module('table_'+slug)
        m.build_master_summary=lambda: master.copy()
        m.OUTPUT=OUT/'tables'/('Table_'+slug+'.xlsx')
        m.main()
        wb=load_workbook(m.OUTPUT)
        for ws in wb:
            for row in ws:
                for cell in row:
                    if isinstance(cell.value,str):
                        cell.value=cell.value.replace('Lower 95% CI','Lower Effect Scenario').replace('Upper 95% CI','Upper Effect Scenario')
                        cell.value=cell.value.replace('(Central)', '(Primary)') if 'housing_loss' in slug else cell.value
            if ws.title=='Definitions':
                for row in range(2,ws.max_row+1):ws.row_dimensions[row].height=70
        defs=wb['Definitions']
        defs.append(['Scenario provenance','', 'Primary: household proxy, 20 km decay, half-collapse weight 0.5; bounded older-household demographic allocation.',
                     'Housing ranges sum corrected 27-distance-ensemble pointwise bounds; not municipal scenario extrema. Health range varies ROR 1.01–1.15 only; not total uncertainty.'])
        from openpyxl.styles import Alignment
        for cell in defs[defs.max_row]:cell.alignment=Alignment(wrap_text=True,vertical='top')
        defs.row_dimensions[defs.max_row].height=80
        wb.save(m.OUTPUT)
        common.validate_workbook(m.OUTPUT,[c.value for c in wb['Municipal Summary'][1]])
        # Exact numeric round-trip: no change to scientific values during styling.
        data=pd.read_excel(m.OUTPUT,sheet_name='Municipal Summary')
        assert data.shape==(45,6) and data.iloc[:,0].is_unique
        if 'housing_loss' in slug:np.testing.assert_allclose(data.iloc[:,3].sum(),master[OLDER].sum())
        elif 'electricity' in slug:np.testing.assert_allclose(data.iloc[:,4].sum(),master['Required Peak Cooling Electric Power kW (Central)'].sum())
        else:np.testing.assert_allclose(data.iloc[:,2].sum(),master[EXCESS].sum())


def main():
    protected={str(p.relative_to(ROOT)):digest(p) for folder in ['data/processed','data/results','Rev/revision']
               for p in (ROOT/folder).rglob('*') if p.is_file()}
    for file,keys in [('validation.json',['protected_sha256','code_sha256']),('extended_validation.json',['source_sha256'])]:
        manifest=json.loads((INPUT/file).read_text())
        for key in keys:
            for path,sha in manifest[key].items():
                assert digest(ROOT/path)==sha, f'Stale evidence: {path}'
    for folder in ['inputs','figures','tables','previews']:(OUT/folder).mkdir(parents=True,exist_ok=True)
    grid,p,health,master,geo=build_inputs()
    figures(grid,p,health,geo);tables(master)
    assert all(digest(ROOT/path)==sha for path,sha in protected.items())
    report={'production_and_manuscript_unchanged':True,'protected_sha256':protected,
            'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in INPUT.glob('*.parquet')},
            'script_sha256':digest(Path(__file__)), 'older_exposure':float(grid[OLDER].sum()),
            'central_kW':float(master['Required Peak Cooling Electric Power kW (Central)'].sum()),
            'central_kWh_day':float(master['Required Daily Cooling Electricity kWh (Central)'].sum()),
            'incremental_expected_deaths':float(health[EXCESS].sum()),
            'figures':4,'tables':3,'dpi':400,
            'status':'isolated review assets; not manuscript-approved',
            'limits':'Pointwise distance ranges are not joint CI or coherent municipal extremes; shaking alternatives separate. Legacy internal CI column names retained only for renderer compatibility; visible labels corrected.'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if 'sha256' not in k},indent=2))


if __name__=='__main__':main()
