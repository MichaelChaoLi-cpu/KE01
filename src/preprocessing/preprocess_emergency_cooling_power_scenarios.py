#!/usr/bin/env python3
"""Construct demand-side emergency cooling electricity scenarios.

The three parameter bundles estimate thermal load, peak electric power, and daily
electricity for the central older-person cooling-assessment population. Verified
facility supply and the actual emergency power gap remain missing by design.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / (
    "data/processed/kumamoto_cooling_protection_need_scenarios_preprocessed.parquet"
)
BOUNDARY_SOURCE = ROOT / (
    "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT = ROOT / (
    "data/processed/kumamoto_emergency_cooling_power_scenarios_preprocessed.parquet"
)

MAP_CRS = "EPSG:6670"
MINIMUM_SHELTER_AREA_M2_PER_PERSON = 3.5
SPACE_STANDARD_SOURCE = (
    "Cabinet Office, Government of Japan, Shelter Establishment Guidance"
)
SPACE_STANDARD_URL = "https://www.bousai.go.jp/oyakudachi/pdf/kyuujo_c1.pdf"
COOLING_LOAD_SOURCE = "Ministry of Land, Infrastructure, Transport and Tourism, Gymnasium HVAC Load Case"
COOLING_LOAD_URL = (
    "https://www.mlit.go.jp/sogoseisaku/kanminrenkei/content/001761551.pdf"
)
COP_DEFINITION_SOURCE = "Agency for Natural Resources and Energy, Air-Conditioner Efficiency Method"
COP_DEFINITION_URL = (
    "https://www.enecho.meti.go.jp/category/saving_and_new/saving/"
    "enterprise/equipment/council/pdf/060705air_condioners.pdf"
)

SCENARIOS = (
    {
        "Power Demand Scenario": "Low",
        "Cooling Load Density W per m2": 127.0,
        "Scenario Cooling System COP": 4.0,
        "Scenario Peak Load Diversity Factor": 0.8,
        "Scenario Cooling Operating Hours per Day": 12.0,
    },
    {
        "Power Demand Scenario": "Central",
        "Cooling Load Density W per m2": 134.0,
        "Scenario Cooling System COP": 3.0,
        "Scenario Peak Load Diversity Factor": 0.9,
        "Scenario Cooling Operating Hours per Day": 18.0,
    },
    {
        "Power Demand Scenario": "High",
        "Cooling Load Density W per m2": 141.0,
        "Scenario Cooling System COP": 2.5,
        "Scenario Peak Load Diversity Factor": 1.0,
        "Scenario Cooling Operating Hours per Day": 24.0,
    },
)

BASE_COLUMNS = [
    "Disclosure Group Code",
    "geometry",
    "Estimated Affected Population Age 65+",
    "Damage Evidence Cutoff",
    "Cooling Protection Scenario Status",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def assign_municipalities(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Assign each disclosure group to a municipality by representative point."""
    require(BOUNDARY_SOURCE.is_file(), f"Missing boundary source: {BOUNDARY_SOURCE}")
    small_areas = gpd.read_file(
        BOUNDARY_SOURCE, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(
        by=["CITY", "CITY_NAME"], as_index=False
    )
    projected = frame.to_crs(MAP_CRS).copy()
    points = gpd.GeoDataFrame(
        {"_row_id": np.arange(len(projected))},
        geometry=projected.geometry.representative_point(),
        crs=MAP_CRS,
    )
    joined = gpd.sjoin(
        points,
        municipalities[["CITY", "CITY_NAME", "geometry"]],
        how="left",
        predicate="within",
    ).sort_values("_row_id")
    require(len(joined) == len(projected), "Municipality join changed row count")
    unmatched = joined["CITY"].isna()
    if unmatched.any():
        nearest = gpd.sjoin_nearest(
            joined.loc[unmatched, ["_row_id", "geometry"]],
            municipalities[["CITY", "CITY_NAME", "geometry"]],
            how="left",
            max_distance=100,
            distance_col="Municipality Assignment Distance m",
        )
        nearest = (
            nearest.sort_values(["_row_id", "Municipality Assignment Distance m"])
            .drop_duplicates("_row_id")
            .set_index("_row_id")
        )
        require(
            nearest["CITY"].notna().all(),
            "Some disclosure groups are farther than 100 m from a municipality",
        )
        require(
            nearest["Municipality Assignment Distance m"].max() <= 100,
            "Nearest municipality assignment exceeds 100 m",
        )
        joined = joined.set_index("_row_id")
        joined.loc[nearest.index, "CITY"] = nearest["CITY"]
        joined.loc[nearest.index, "CITY_NAME"] = nearest["CITY_NAME"]
        joined = joined.reset_index().sort_values("_row_id")
    require(joined["CITY"].notna().all(), "Some disclosure groups lack municipality")
    projected["Municipality Code"] = joined["CITY"].astype("string").to_numpy()
    projected["Municipality"] = joined["CITY_NAME"].astype("string").to_numpy()
    return projected


def build_scenarios() -> gpd.GeoDataFrame:
    require(SOURCE.is_file(), f"Missing source: {SOURCE}")
    source = gpd.read_parquet(SOURCE)
    missing = sorted(set(BASE_COLUMNS) - set(source.columns))
    require(not missing, f"Cooling-protection source is missing columns: {missing}")
    base = assign_municipalities(source[BASE_COLUMNS].copy())
    base["Estimated Affected Population Age 65+"] = pd.to_numeric(
        base["Estimated Affected Population Age 65+"], errors="raise"
    )

    scenario_frames: list[gpd.GeoDataFrame] = []
    for parameters in SCENARIOS:
        scenario = base.copy()
        for name, value in parameters.items():
            scenario[name] = value
        scenario["Minimum Shelter Living Area m2 per Person"] = (
            MINIMUM_SHELTER_AREA_M2_PER_PERSON
        )
        scenario["Cooling Thermal Load W per Person"] = (
            scenario["Minimum Shelter Living Area m2 per Person"]
            * scenario["Cooling Load Density W per m2"]
        )
        scenario["Cooling Thermal Load kW"] = (
            scenario["Estimated Affected Population Age 65+"]
            * scenario["Cooling Thermal Load W per Person"]
            / 1_000
        )
        scenario["Required Peak Cooling Electric Power kW"] = (
            scenario["Cooling Thermal Load kW"]
            * scenario["Scenario Peak Load Diversity Factor"]
            / scenario["Scenario Cooling System COP"]
        )
        scenario["Required Daily Cooling Electricity kWh"] = (
            scenario["Required Peak Cooling Electric Power kW"]
            * scenario["Scenario Cooling Operating Hours per Day"]
        )
        scenario["Cooling Power Scenario Status"] = (
            "demand_side_only_no_verified_supply"
        )
        scenario["Minimum Shelter Living Area Source"] = SPACE_STANDARD_SOURCE
        scenario["Minimum Shelter Living Area Source URL"] = SPACE_STANDARD_URL
        scenario["Cooling Load Density Source"] = COOLING_LOAD_SOURCE
        scenario["Cooling Load Density Source URL"] = COOLING_LOAD_URL
        scenario["COP Definition Source"] = COP_DEFINITION_SOURCE
        scenario["COP Definition Source URL"] = COP_DEFINITION_URL
        for column in (
            "Verified Available Grid Power kW",
            "Backup Generator Capacity kW",
            "Non-Cooling Critical Load kW",
            "Verified Available Electric Power kW",
            "Emergency Cooling Power Gap kW",
        ):
            scenario[column] = pd.Series(pd.NA, index=scenario.index, dtype="Float64")
        scenario_frames.append(scenario)

    combined = pd.concat(scenario_frames, ignore_index=True)
    return gpd.GeoDataFrame(combined, geometry="geometry", crs=MAP_CRS)


def validate(frame: gpd.GeoDataFrame) -> None:
    expected_rows = len(gpd.read_parquet(SOURCE)) * len(SCENARIOS)
    require(len(frame) == expected_rows, "Unexpected scenario row count")
    require(frame.geometry.notna().all(), "Scenario geometry is missing")
    require(
        set(frame["Power Demand Scenario"]) == {"Low", "Central", "High"},
        "Power scenarios are incomplete",
    )
    require(
        frame.groupby("Power Demand Scenario").size().nunique() == 1,
        "Power scenarios have unequal row counts",
    )
    require(
        frame["Estimated Affected Population Age 65+"].ge(0).all(),
        "Cooling-assessment population must be nonnegative",
    )
    for column in (
        "Cooling Thermal Load kW",
        "Required Peak Cooling Electric Power kW",
        "Required Daily Cooling Electricity kWh",
    ):
        require(frame[column].ge(0).all(), f"{column} must be nonnegative")
    for column in (
        "Verified Available Grid Power kW",
        "Backup Generator Capacity kW",
        "Non-Cooling Critical Load kW",
        "Verified Available Electric Power kW",
        "Emergency Cooling Power Gap kW",
    ):
        require(frame[column].isna().all(), f"{column} must remain missing")

    expected_per_person = (
        frame["Minimum Shelter Living Area m2 per Person"]
        * frame["Cooling Load Density W per m2"]
    )
    require(
        np.allclose(
            frame["Cooling Thermal Load W per Person"], expected_per_person
        ),
        "Per-person thermal load construction failed",
    )
    population_totals = frame.groupby("Power Demand Scenario")[
        "Estimated Affected Population Age 65+"
    ].sum()
    require(
        np.allclose(population_totals, population_totals.iloc[0]),
        "Engineering scenarios must use the same central assessment population",
    )


def main() -> int:
    frame = build_scenarios()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    totals = frame.groupby("Power Demand Scenario", sort=False)[
        [
            "Estimated Affected Population Age 65+",
            "Cooling Thermal Load kW",
            "Required Peak Cooling Electric Power kW",
            "Required Daily Cooling Electricity kWh",
        ]
    ].sum()
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    print(totals.round(2).to_string())
    print("verified supply and emergency power gap: missing by design")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
