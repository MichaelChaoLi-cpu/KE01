#!/usr/bin/env python3
"""Estimate structural functional-housing-loss scenarios by population grid.

The model allocates official residence-loss totals using an ensemble of
epicentral-distance decay and exposure-denominator specifications. It is a
scenario nowcast, not an observed building-damage classification. Confirmed
residences are not assigned to a grid unless their location is supported.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / (
    "data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet"
)
DAMAGE_SNAPSHOTS = (
    ROOT / "data/processed/kumamoto_housing_damage_snapshots_preprocessed.parquet"
)
OUTPUT = ROOT / "data/processed/kumamoto_grid_exposure_estimates_preprocessed.parquet"

MAP_CRS = "EPSG:6670"
EPICENTER_LATITUDE = 32.6
EPICENTER_LONGITUDE = 130.7
DISTANCE_DECAY_SCALES_KM = (10.0, 20.0, 40.0)
HALF_COLLAPSE_FUNCTIONAL_LOSS_WEIGHTS = (0.0, 0.5, 1.0)
EXPOSURE_PROXY_COLUMNS = (
    "General Households",
    "Mapped Building Count",
    "Mapped Building Footprint Area m2",
)

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


def latest_prefecture_damage() -> pd.Series:
    require(DAMAGE_SNAPSHOTS.is_file(), f"Missing source: {DAMAGE_SNAPSHOTS}")
    snapshots = pd.read_parquet(DAMAGE_SNAPSHOTS)
    required = {
        "Observation Time",
        "Geographic Level",
        "Full Collapse Buildings",
        "Half Collapse Buildings",
    }
    missing = sorted(required - set(snapshots.columns))
    require(not missing, f"Housing snapshots are missing columns: {missing}")
    eligible = snapshots.loc[
        snapshots["Geographic Level"].eq("prefecture")
        & snapshots["Full Collapse Buildings"].notna()
        & snapshots["Half Collapse Buildings"].notna()
    ].copy()
    require(not eligible.empty, "No prefecture snapshot reports full and half collapse")
    eligible["Observation Time"] = pd.to_datetime(
        eligible["Observation Time"], utc=True, errors="raise"
    )
    return eligible.sort_values("Observation Time").iloc[-1]


def epicentral_distance_km(frame: gpd.GeoDataFrame) -> np.ndarray:
    points = gpd.GeoSeries(
        frame.geometry.representative_point(), crs=frame.crs
    ).to_crs(MAP_CRS)
    epicenter = gpd.GeoSeries(
        [Point(EPICENTER_LONGITUDE, EPICENTER_LATITUDE)], crs="EPSG:4326"
    ).to_crs(MAP_CRS).iloc[0]
    return points.distance(epicenter).to_numpy(dtype=float) / 1_000.0


def scenario_surfaces(
    frame: gpd.GeoDataFrame,
    distance_km: np.ndarray,
    full_collapse: float,
    half_collapse: float,
) -> np.ndarray:
    scenarios: list[np.ndarray] = []
    for column in EXPOSURE_PROXY_COLUMNS:
        require(frame[column].notna().all(), f"{column} contains missing values")
        exposure = frame[column].to_numpy(dtype=float)
        require((exposure >= 0).all(), f"{column} must be nonnegative")
        for scale_km in DISTANCE_DECAY_SCALES_KM:
            raw_weight = exposure * np.exp(-distance_km / scale_km)
            require(raw_weight.sum() > 0, f"Zero allocation weight for {column}")
            allocation_weight = raw_weight / raw_weight.sum()
            for half_weight in HALF_COLLAPSE_FUNCTIONAL_LOSS_WEIGHTS:
                total = full_collapse + half_weight * half_collapse
                scenarios.append(total * allocation_weight)
    return np.vstack(scenarios)


def affected_population(
    population: pd.Series,
    general_households: np.ndarray,
    expected_loss: np.ndarray,
) -> np.ndarray:
    residence_loss_share = np.divide(
        expected_loss,
        general_households,
        out=np.zeros(len(expected_loss), dtype=float),
        where=general_households > 0,
    )
    residence_loss_share = np.clip(residence_loss_share, 0.0, 1.0)
    return population.to_numpy(dtype=float) * residence_loss_share


def build_estimates() -> gpd.GeoDataFrame:
    require(SOURCE.is_file(), f"Missing source: {SOURCE}")
    source = gpd.read_parquet(SOURCE)
    missing = sorted(set(BASE_COLUMNS) - set(source.columns))
    require(not missing, f"Spatial foundation is missing columns: {missing}")

    damage = latest_prefecture_damage()
    full_collapse = float(damage["Full Collapse Buildings"])
    half_collapse = float(damage["Half Collapse Buildings"])
    central_total = full_collapse + 0.5 * half_collapse

    output = source[BASE_COLUMNS].copy()
    distance_km = epicentral_distance_km(output)
    surfaces = scenario_surfaces(
        output,
        distance_km,
        full_collapse=full_collapse,
        half_collapse=half_collapse,
    )
    scenario_median = np.median(surfaces, axis=0)
    require(scenario_median.sum() > 0, "Scenario median has zero total")
    central_loss = scenario_median * central_total / scenario_median.sum()
    lower_loss = np.min(surfaces, axis=0)
    upper_loss = np.max(surfaces, axis=0)
    central_loss = np.clip(central_loss, lower_loss, upper_loss)
    allocation_weight = central_loss / central_loss.sum()

    output["Epicentral Distance km"] = np.round(distance_km, 3)
    output["Housing Loss Allocation Weight"] = allocation_weight
    output["Housing Loss Scenario Count"] = surfaces.shape[0]
    output["Distance Decay Scenario Set km"] = "10;20;40"
    output["Half-Collapse Functional Loss Weight Set"] = "0;0.5;1"
    output["Housing Exposure Proxy Set"] = (
        "General Households;Mapped Building Count;Mapped Building Footprint Area m2"
    )
    output["Structural Housing Loss Central Total Residences"] = central_total
    output["Functional Housing Loss Status"] = np.where(
        output["General Households"].to_numpy(dtype=float) > 0,
        "structural_scenario_estimated",
        "no_residential_exposure_denominator",
    )
    output["Expected Functionally Lost Residences"] = central_loss
    output["Expected Functionally Lost Residences Lower Bound"] = lower_loss
    output["Expected Functionally Lost Residences Upper Bound"] = upper_loss
    output["Confirmed Functionally Lost Residences"] = pd.Series(
        pd.NA, index=output.index, dtype="Float64"
    )

    households = output["General Households"].to_numpy(dtype=float)
    population_columns = {
        "Total Population": "Estimated Affected Population",
        "Population Age 65+": "Estimated Affected Population Age 65+",
        "Population Age 75+": "Estimated Affected Population Age 75+",
        "Population Age 85+": "Estimated Affected Population Age 85+",
    }
    for population_column, output_column in population_columns.items():
        output[output_column] = affected_population(
            output[population_column], households, central_loss
        )
        output[f"{output_column} Lower Bound"] = affected_population(
            output[population_column], households, lower_loss
        )
        output[f"{output_column} Upper Bound"] = affected_population(
            output[population_column], households, upper_loss
        )

    output["Heat Exposure Status"] = "pending_event_grid_heat_input"
    output["Estimation Status"] = "scenario_estimated_epicentral_distance_exposure"
    output["Damage Evidence Cutoff"] = pd.to_datetime(
        damage["Observation Time"], utc=True
    )
    output["Notes"] = (
        "Scenario allocation constrained to official residence totals; not observed "
        "building damage or displacement. Confirmed residences remain unallocated."
    )
    return gpd.GeoDataFrame(output, geometry="geometry", crs=source.crs)


def validate(frame: gpd.GeoDataFrame) -> None:
    require(len(frame) > 0, "The grid estimate is empty")
    require(frame["Disclosure Group Code"].is_unique, "Disclosure groups are duplicated")
    require(frame.geometry.notna().all(), "Geometry is missing")
    require((frame["Epicentral Distance km"] >= 0).all(), "Distance must be nonnegative")
    require(
        np.isclose(frame["Housing Loss Allocation Weight"].sum(), 1.0),
        "Allocation weights must sum to one",
    )
    expected = frame["Expected Functionally Lost Residences"]
    lower = frame["Expected Functionally Lost Residences Lower Bound"]
    upper = frame["Expected Functionally Lost Residences Upper Bound"]
    require((lower <= expected).all(), "Expected loss is below its lower bound")
    require((expected <= upper).all(), "Expected loss exceeds its upper bound")
    require(
        np.isclose(expected.sum(), frame["Structural Housing Loss Central Total Residences"].iloc[0]),
        "Central grid loss does not sum to its constrained residence total",
    )
    require(
        frame["Confirmed Functionally Lost Residences"].isna().all(),
        "Do not allocate confirmed residences without geolocated evidence",
    )
    for age in ("", " Age 65+", " Age 75+", " Age 85+"):
        population_column = "Total Population" if not age else f"Population{age}"
        affected_column = "Estimated Affected Population" + age
        require(
            (frame[affected_column] <= frame[population_column] + 1e-9).all(),
            f"{affected_column} exceeds its population denominator",
        )


def main() -> int:
    frame = build_estimates()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    print(
        "expected functionally lost residences: "
        f"{frame['Expected Functionally Lost Residences'].sum():.1f}; "
        "scenario count: "
        f"{int(frame['Housing Loss Scenario Count'].iloc[0])}"
    )
    print(
        "estimated affected population age 65+: "
        f"{frame['Estimated Affected Population Age 65+'].sum():.1f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
