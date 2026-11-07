"""Isolated retrospective snapshot diagnostic; never overwrite production outputs."""
from pathlib import Path
import sys
import hashlib
import json
from unittest.mock import patch

import numpy as np
import pandas as pd
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/preprocessing"))
import preprocess_grid_exposure_estimates as model
import preprocess_emergency_cooling_power_scenarios as power
import preprocess_cooling_loss_mortality_scenario as health

OUT = ROOT / "data/exp/revision_snapshot_sensitivity"
SOURCE_URL = "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin65.pdf"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    protected = [model.OUTPUT, model.DAMAGE_SNAPSHOTS, health.OUTPUT,
                 health.MORTALITY_SOURCE, health.HEAT_SOURCE, health.COOLING_NEED_SOURCE]
    before = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    snapshots = pd.read_parquet(model.DAMAGE_SNAPSHOTS)
    later = model.latest_prefecture_damage().copy()
    later["Observation Time"] = "2026-09-24T17:00:00+09:00"
    later["Full Collapse Buildings"] = 2270
    later["Half Collapse Buildings"] = 6357
    augmented = pd.concat([snapshots, later.to_frame().T], ignore_index=True)
    with patch.object(model.pd, "read_parquet", return_value=augmented):
        selected = model.latest_prefecture_damage()
        assert pd.Timestamp(selected["Observation Time"]) == pd.Timestamp(model.MAIN_DAMAGE_CUTOFF)
    frames = {"early": model.build_estimates(), "retrospective": model.build_estimates(later)}
    existing = gpd.read_parquet(model.OUTPUT)
    cols = ["Expected Functionally Lost Residences", "Estimated Affected Population Age 65+"]
    old = existing.set_index("Disclosure Group Code")
    regenerated = frames["early"].set_index("Disclosure Group Code").loc[old.index]
    for col in cols:
        np.testing.assert_allclose(regenerated[col], old[col], rtol=1e-10, atol=1e-10)
    baseline = health.build_scenario()
    health.validate(baseline)
    baseline = baseline.set_index("Municipality Code").sort_index()
    saved_health = gpd.read_parquet(health.OUTPUT).set_index("Municipality Code").loc[baseline.index]
    risk_columns = [c for c in baseline if "30-Day Mortality Risk" in c]
    for c in risk_columns:
        np.testing.assert_allclose(baseline[c], saved_health[c], rtol=1e-10, atol=1e-12)
    municipalities = baseline.reset_index()[["Municipality Code", "geometry"]]
    summaries, engineering, municipal, health_summaries, health_rows = [], [], {}, [], []
    for label, frame in frames.items():
        model.validate(frame)
        loss, older = (float(frame[c].sum()) for c in cols)
        summaries.append({"snapshot": label, "functional_loss": loss, "older_exposure": older,
                          "person_days_30": older * 30,
                          "groups_above_household_cap": int((frame[cols[0]] > frame["General Households"]).sum())})
        assigned = health.assign_municipalities(frame, municipalities)
        municipal[label] = assigned.groupby("Municipality Code")[cols].sum().reindex(baseline.index)
        assert len(municipal[label]) == 45 and municipal[label].notna().all().all()
        for c in cols:
            np.testing.assert_allclose(municipal[label][c].sum(), frame[c].sum())
        exposure = municipal[label][cols[1]]
        if label == "early":
            np.testing.assert_allclose(exposure, baseline["No-Placement Unprotected Older-Person-Days"]/30,
                                       rtol=1e-10, atol=1e-10)
        cool = baseline["Effective-Cooling 30-Day Mortality Risk"]
        for effect, suffix in [("lower", " Lower 95% CI"), ("central", ""), ("upper", " Upper 95% CI")]:
            no_cool = baseline["No-Effective-Cooling 30-Day Mortality Risk"+suffix]
            excess = exposure * (no_cool-cool)
            if label == "early":
                np.testing.assert_allclose(excess, saved_health["Incremental Cooling-Loss-Related Excess Deaths"+suffix],
                                           rtol=1e-10, atol=1e-12)
            health_summaries.append({"snapshot": label, "effect": effect,
                                    "effective_cooling_expected_deaths": float((exposure*cool).sum()),
                                    "no_cooling_expected_deaths": float((exposure*no_cool).sum()),
                                    "incremental_expected_deaths": float(excess.sum()),
                                    "relative_burden_increase_percent": float(100*excess.sum()/(exposure*cool).sum())})
            for code in baseline.index:
                health_rows.append({"snapshot": label, "effect": effect, "Municipality Code": code,
                                    "Municipality": baseline.loc[code,"Municipality"],
                                    "older_exposure": float(exposure.loc[code]),
                                    "incremental_expected_deaths": float(excess.loc[code]),
                                    "incremental_risk_per_100000": float((no_cool.loc[code]-cool.loc[code])*100000),
                                    "relative_burden_increase_percent": float(100*(no_cool.loc[code]/cool.loc[code]-1))})
        for p in power.SCENARIOS:
            kw = older * power.MINIMUM_SHELTER_AREA_M2_PER_PERSON * p["Cooling Load Density W per m2"] / 1000 * p["Scenario Peak Load Diversity Factor"] / p["Scenario Cooling System COP"]
            engineering.append({"snapshot": label, "bundle": p["Power Demand Scenario"],
                                "peak_kw": kw, "daily_kwh": kw*p["Scenario Cooling Operating Hours per Day"]})
    comparison = municipal["early"].join(municipal["retrospective"], lsuffix="_early", rsuffix="_retrospective")
    for c in cols:
        comparison[c+"_rank_early"] = comparison[c+"_early"].rank(ascending=False, method="min")
        comparison[c+"_rank_retrospective"] = comparison[c+"_retrospective"].rank(ascending=False, method="min")
    pd.DataFrame(summaries).to_csv(OUT/"prefecture_comparison.csv", index=False)
    pd.DataFrame(engineering).to_csv(OUT/"engineering_comparison.csv", index=False)
    comparison.to_csv(OUT/"municipality_comparison.csv")
    pd.DataFrame(health_summaries).to_csv(OUT/"health_prefecture_comparison.csv", index=False)
    pd.DataFrame(health_rows).to_csv(OUT/"health_municipality_comparison.csv", index=False)
    ranking = {}
    for c in cols:
        early_rank = comparison[c+"_rank_early"]
        later_rank = comparison[c+"_rank_retrospective"]
        ranking[c] = {"changed_ranks": int((early_rank != later_rank).sum()),
                      "max_rank_shift": float((early_rank-later_rank).abs().max()),
                      "spearman": float(comparison[c+"_early"].rank().corr(comparison[c+"_retrospective"].rank())),
                      "top5_overlap": len(set(comparison[c+"_early"].nlargest(5).index) &
                                          set(comparison[c+"_retrospective"].nlargest(5).index))}
    after = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert before == after, "Production inputs/outputs changed"
    report = {"decision": "KILA-D-20261001-001", "later_source": SOURCE_URL,
              "source_hashes": before, "foundation_sha256": sha(model.SOURCE),
              "production_unchanged": True, "early_reproduction_passed": True,
              "cutoff_with_future_row_test_passed": True,
              "scope": "fixed-method snapshot sensitivity; fixed heat, mortality baseline and effect parameters; not independent geographic validation",
              "municipalities": 45, "health_baseline_reproduction_passed": True,
              "municipal_individual_risks_unchanged_by_design": True,
              "rank_diagnostics": ranking,
              "health_summaries": health_summaries, "summaries": summaries}
    (OUT/"validation.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
