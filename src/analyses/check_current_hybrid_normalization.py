"""Read-only input diagnostic: normalization ranks under current demographics."""
from pathlib import Path
import sys, json, hashlib
import numpy as np
import pandas as pd
import geopandas as gpd
sys.path.insert(0,str(Path(__file__).resolve().parent))
from recalculate_integrated_revision import ROOT, AGE, housing
from analyze_denominator_correction import redistribute

g=gpd.read_parquet(housing.SOURCE)
a=pd.read_parquet(AGE/'bounded_grid_age65_estimates.parquet').set_index('Disclosure Group Code').loc[g['Disclosure Group Code']]
h=g['General Households'].to_numpy(float)
n=a['representative_point__older_households'].to_numpy(float)
s=housing.scenario_surfaces(g,housing.epicentral_distance_km(g),181,245)
s=np.array([redistribute(row,h>0,row.sum()) for row in s])
raw=np.median(s,axis=0);factor=303.5/raw.sum();scaled=raw*factor
clipped=np.clip(scaled,s.min(axis=0),s.max(axis=0))
assert np.array_equal(scaled,clipped)
assert (scaled<=h+1e-9).all()
tables=[]
for loss in [raw,scaled]:
    t=pd.DataFrame({'municipality':a['Municipality Code'].to_numpy(),'loss':loss,
        'older':n*np.divide(loss,h,out=np.zeros_like(h),where=h>0)}).groupby('municipality').sum()
    tables.append(t)
assert all(tables[0][c].rank().equals(tables[1][c].rank()) for c in ['loss','older'])
current=pd.read_parquet(ROOT/'data/exp/revision_integrated_calculation/structural_municipalities.parquet')
current=current.loc[current.scenario.eq('corrected_hybrid')].set_index('Municipality Code').reindex(tables[1].index)
np.testing.assert_allclose(tables[1].loss,current.functional_loss,rtol=1e-10,atol=1e-10)
np.testing.assert_allclose(tables[1].older,current.older_exposure,rtol=1e-10,atol=1e-10)
report=dict(raw_total=float(raw.sum()),normalization_factor=float(factor),scaled_total=float(scaled.sum()),
    current_older_exposure=float(tables[1].older.sum()),clipped_groups=0,municipalities=len(tables[1]),
    housing_ranks_unchanged=True,older_exposure_ranks_unchanged=True,current_saved_hybrid_reproduced=True,
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [housing.SOURCE,AGE/'bounded_grid_age65_estimates.parquet',ROOT/'data/exp/revision_integrated_calculation/structural_municipalities.parquet']},
    limitation='Positive scalar rank invariance is conditional on fixed demographics, linear aggregation and nonbinding caps; not evidence of external accuracy.')
out=ROOT/'data/exp/revision_hybrid_normalization_check';out.mkdir(exist_ok=True)
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
