#!/usr/bin/env python3
"""Prepare the full-prefecture grid exposure estimation scaffold.

Population and mapped-building denominators are preserved at the finest official
disclosure geography. Housing-loss and heat-exposure estimates remain missing
until damage localization and heat inputs exist; the script never spreads a
prefecture total uniformly across grids.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / (
    "data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet"
)
OUTPUT = ROOT / "data/processed/kumamoto_grid_exposure_estimates_preprocessed.parquet"

BASE_COLUMNS = [
    "Disclosure Group Code",
    "geometry",
    "Disclosure Group Size",
    "Total Population",
    "Population Age 65+",
    "Population Age 75+",
    "Population Age 85+",
    "Total Households",
    "General Households",
    "Older Single-Person Households",
    "Older Couple Households",
    "Mapped Building Count",
    "Mapped Building Footprint Area m2",
    "Nearest Designated Shelter ID",
    "Nearest Designated Shelter Distance m",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_scaffold() -> gpd.GeoDataFrame:
    require(SOURCE.is_file(), f"Missing source: {SOURCE}")
    source = gpd.read_parquet(SOURCE)
    missing = sorted(set(BASE_COLUMNS) - set(source.columns))
    require(not missing, f"Spatial foundation is missing columns: {missing}")

    output = source[BASE_COLUMNS].copy()
    output["Functional Housing Loss Status"] = "not_yet_estimated"
    output["Expected Functionally Lost Buildings"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Confirmed Functionally Lost Buildings"] = pd.Series(
        pd.NA, index=output.index, dtype="Int64"
    )
    output["Estimated Affected Population"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Estimated Affected Population Age 65+"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Estimated Affected Population Age 75+"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Estimated Affected Population Age 85+"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )
    output["Heat Exposure Status"] = "pending_heat_input"
    output["Estimation Status"] = "pending_damage_localization"
    output["Damage Evidence Cutoff"] = pd.to_datetime(
        "2026-08-02T15:30:00+09:00", utc=True
    )
    output["Notes"] = (
        "Baseline only; official prefecture totals have not been allocated to this group."
    )
    return gpd.GeoDataFrame(output, geometry="geometry", crs=source.crs)


def validate(frame: gpd.GeoDataFrame) -> None:
    require(len(frame) > 0, "The grid scaffold is empty")
    require(frame["Disclosure Group Code"].is_unique, "Disclosure groups are duplicated")
    require(frame.geometry.notna().all(), "Geometry is missing")
    require((frame["Total Population"] >= 0).all(), "Population must be nonnegative")
    require((frame["Population Age 65+"] >= 0).all(), "Older population must be nonnegative")
    require(
        frame["Expected Functionally Lost Buildings"].isna().all(),
        "Do not allocate the prefecture housing-loss total without spatial evidence",
    )
    require(
        frame["Estimated Affected Population Age 65+"].isna().all(),
        "Do not estimate affected older residents before housing loss is localized",
    )


def main() -> int:
    frame = build_scaffold()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
