#!/usr/bin/env python3
"""Construct an early cooling-protection planning scenario by population grid.

The output converts the modeled older-person housing-loss exposure into a 30-day
demand-side bound that assumes no verified effective cooled placement. It does not
infer that shelter capacity is zero and does not estimate the actual placement gap.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/processed/kumamoto_grid_exposure_estimates_preprocessed.parquet"
OUTPUT = ROOT / (
    "data/processed/"
    "kumamoto_cooling_protection_need_scenarios_preprocessed.parquet"
)
PLANNING_HORIZON_DAYS = 30

SOURCE_COLUMNS = [
    "Disclosure Group Code",
    "geometry",
    "Estimated Affected Population Age 65+",
    "Estimated Affected Population Age 65+ Lower Bound",
    "Estimated Affected Population Age 65+ Upper Bound",
    "Nearest Designated Shelter ID",
    "Nearest Designated Shelter Distance m",
    "Damage Evidence Cutoff",
    "Estimation Status",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_scenario() -> gpd.GeoDataFrame:
    require(SOURCE.is_file(), f"Missing source: {SOURCE}")
    source = gpd.read_parquet(SOURCE)
    missing = sorted(set(SOURCE_COLUMNS) - set(source.columns))
    require(not missing, f"Source is missing columns: {missing}")

    output = source[SOURCE_COLUMNS].copy()
    population_columns = (
        "Estimated Affected Population Age 65+",
        "Estimated Affected Population Age 65+ Lower Bound",
        "Estimated Affected Population Age 65+ Upper Bound",
    )
    for column in population_columns:
        output[column] = pd.to_numeric(output[column], errors="raise")

    output["Cooling Protection Planning Horizon Days"] = PLANNING_HORIZON_DAYS
    output["No-Placement Unprotected Older-Person-Days"] = (
        output["Estimated Affected Population Age 65+"] * PLANNING_HORIZON_DAYS
    )
    output["No-Placement Unprotected Older-Person-Days Lower Bound"] = (
        output["Estimated Affected Population Age 65+ Lower Bound"]
        * PLANNING_HORIZON_DAYS
    )
    output["No-Placement Unprotected Older-Person-Days Upper Bound"] = (
        output["Estimated Affected Population Age 65+ Upper Bound"]
        * PLANNING_HORIZON_DAYS
    )

    # These fields are deliberately missing. No verified placement or operational
    # cooled-capacity observations are available, so zero would be false precision.
    output["Effective Cooled Capacity"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Cooling Capacity Gap"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Cooling Protection Scenario Status"] = (
        "no_verified_placement_demand_side_bound"
    )
    output["Notes"] = (
        "Thirty-day demand-side planning bound under no verified effective cooled "
        "placement. This is not observed unprotected exposure, proof of zero shelter "
        "capacity, or an estimate of the actual cooling capacity gap."
    )
    return gpd.GeoDataFrame(output, geometry="geometry", crs=source.crs)


def validate(frame: gpd.GeoDataFrame) -> None:
    require(len(frame) > 0, "Scenario output is empty")
    require(frame["Disclosure Group Code"].is_unique, "Disclosure groups are duplicated")
    require(frame.geometry.notna().all(), "Geometry is missing")
    require(
        frame["Cooling Protection Planning Horizon Days"].eq(
            PLANNING_HORIZON_DAYS
        ).all(),
        "Planning horizon is inconsistent",
    )

    central = frame["Estimated Affected Population Age 65+"]
    lower = frame["Estimated Affected Population Age 65+ Lower Bound"]
    upper = frame["Estimated Affected Population Age 65+ Upper Bound"]
    require(((lower <= central) & (central <= upper)).all(), "Population bounds fail")

    person_day_triplets = (
        (
            "Estimated Affected Population Age 65+",
            "No-Placement Unprotected Older-Person-Days",
        ),
        (
            "Estimated Affected Population Age 65+ Lower Bound",
            "No-Placement Unprotected Older-Person-Days Lower Bound",
        ),
        (
            "Estimated Affected Population Age 65+ Upper Bound",
            "No-Placement Unprotected Older-Person-Days Upper Bound",
        ),
    )
    for population_column, person_days_column in person_day_triplets:
        expected = frame[population_column].to_numpy(dtype=float) * PLANNING_HORIZON_DAYS
        actual = frame[person_days_column].to_numpy(dtype=float)
        require(
            np.allclose(actual, expected, rtol=0, atol=1e-10),
            f"Incorrect construction for {person_days_column}",
        )
    require(
        frame["Effective Cooled Capacity"].isna().all(),
        "Unverified effective cooled capacity must remain missing",
    )
    require(
        frame["Cooling Capacity Gap"].isna().all(),
        "Actual cooling capacity gap must remain missing",
    )


def main() -> int:
    frame = build_scenario()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    total_need = frame["Estimated Affected Population Age 65+"].sum()
    total_person_days = frame[
        "No-Placement Unprotected Older-Person-Days"
    ].sum()
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    print(f"central older-person cooling-assessment population: {total_need:.1f}")
    print(f"30-day no-placement demand-side bound: {total_person_days:.1f} person-days")
    print("actual effective cooled capacity and cooling capacity gap: missing by design")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
