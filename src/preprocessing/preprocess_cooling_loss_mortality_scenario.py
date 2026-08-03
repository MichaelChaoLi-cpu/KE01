#!/usr/bin/env python3
"""Construct the literature-anchored cooling-loss mortality planning scenario.

Outdoor heat is held common across effective-cooling and no-effective-cooling
states. The only health contrast is the published relative odds of death during
extreme heat in older residents of institutions without versus with air
conditioning. The result is a transferable planning scenario, not observed or
earthquake-attributable mortality.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
COOLING_NEED_SOURCE = ROOT / (
    "data/processed/kumamoto_cooling_protection_need_scenarios_preprocessed.parquet"
)
MORTALITY_SOURCE = ROOT / (
    "data/processed/kumamoto_municipality_mortality_baseline_preprocessed.parquet"
)
HEAT_SOURCE = ROOT / (
    "data/processed/kumamoto_jma_historical_heat_spatial_stations_preprocessed.parquet"
)
BOUNDARY_SOURCE = ROOT / (
    "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT = ROOT / (
    "data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet"
)

MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:4326"
PLANNING_HORIZON_DAYS = 30.0
IDW_NEIGHBORS = 4
IDW_POWER = 2.0

# Katz et al. (2025), JAMA Internal Medicine, lag 0 primary analysis.
# ROR compares the mortality odds on extreme-heat days in nursing homes
# without AC with those in homes with AC. The with-AC extreme-heat OR is used
# to translate the local reference-day mortality probability to the protected
# high-heat state before applying the ROR.
EFFECT_ESTIMATE_ID = "KATZ2025-OLDER-INSTITUTIONAL-EXTREME-HEAT-AC"
WITH_AC_EXTREME_HEAT_OR = 1.03
NO_AC_VS_AC_RELATIVE_OR = 1.08
NO_AC_VS_AC_RELATIVE_OR_LOWER_95 = 1.01
NO_AC_VS_AC_RELATIVE_OR_UPPER_95 = 1.15
EFFECT_SOURCE = "Katz et al. (2025), JAMA Internal Medicine"
EFFECT_SOURCE_URL = "https://doi.org/10.1001/jamainternmed.2025.6595"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load_municipalities() -> gpd.GeoDataFrame:
    require(BOUNDARY_SOURCE.is_file(), f"Missing boundary source: {BOUNDARY_SOURCE}")
    small = gpd.read_file(
        BOUNDARY_SOURCE, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    small["CITY"] = "43" + small["CITY"].astype("string").str.zfill(3)
    kumamoto_wards = {"43101", "43102", "43103", "43104", "43105"}
    is_kumamoto_ward = small["CITY"].isin(kumamoto_wards)
    small.loc[is_kumamoto_ward, "CITY"] = "43100"
    small.loc[is_kumamoto_ward, "CITY_NAME"] = "Kumamoto City"
    municipalities = small.dissolve(
        by=["CITY", "CITY_NAME"], as_index=False
    ).rename(columns={"CITY": "Municipality Code", "CITY_NAME": "Municipality Japanese"})
    municipalities["Municipality Code"] = municipalities[
        "Municipality Code"
    ].astype("string")
    return municipalities


def assign_municipalities(
    frame: gpd.GeoDataFrame, municipalities: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    projected = frame.to_crs(MAP_CRS).copy()
    points = gpd.GeoDataFrame(
        {"_row_id": np.arange(len(projected))},
        geometry=projected.geometry.representative_point(),
        crs=MAP_CRS,
    )
    joined = gpd.sjoin(
        points,
        municipalities[["Municipality Code", "geometry"]],
        how="left",
        predicate="within",
    ).sort_values("_row_id")
    require(len(joined) == len(projected), "Municipality join changed row count")
    unmatched = joined["Municipality Code"].isna()
    if unmatched.any():
        nearest = gpd.sjoin_nearest(
            joined.loc[unmatched, ["_row_id", "geometry"]],
            municipalities[["Municipality Code", "geometry"]],
            how="left",
            max_distance=100,
            distance_col="Municipality Assignment Distance m",
        )
        nearest = (
            nearest.sort_values(["_row_id", "Municipality Assignment Distance m"])
            .drop_duplicates("_row_id")
            .set_index("_row_id")
        )
        require(nearest["Municipality Code"].notna().all(), "Unassigned cooling grids")
        joined = joined.set_index("_row_id")
        joined.loc[nearest.index, "Municipality Code"] = nearest["Municipality Code"]
        joined = joined.reset_index().sort_values("_row_id")
    require(joined["Municipality Code"].notna().all(), "Unassigned cooling grids")
    projected["Municipality Code"] = joined["Municipality Code"].astype("string").to_numpy()
    return projected


def station_high_heat_days() -> gpd.GeoDataFrame:
    require(HEAT_SOURCE.is_file(), f"Missing heat source: {HEAT_SOURCE}")
    heat = pd.read_parquet(HEAT_SOURCE)
    required = {
        "Station ID",
        "Station Name",
        "Latitude",
        "Longitude",
        "Historical Year",
        "Event Day",
        "Hot Day Indicator",
        "Hot Night Indicator",
    }
    missing = sorted(required - set(heat.columns))
    require(not missing, f"Heat source is missing variables: {missing}")
    heat["High-Heat Scenario Day"] = (
        heat["Hot Day Indicator"].fillna(0).astype(int).eq(1)
        | heat["Hot Night Indicator"].fillna(0).astype(int).eq(1)
    ).astype(int)
    per_year = (
        heat.groupby(
            ["Station ID", "Station Name", "Latitude", "Longitude", "Historical Year"],
            as_index=False,
        )["High-Heat Scenario Day"]
        .sum()
    )
    stations = (
        per_year.groupby(
            ["Station ID", "Station Name", "Latitude", "Longitude"], as_index=False
        )["High-Heat Scenario Day"]
        .mean()
        .rename(columns={"High-Heat Scenario Day": "Expected High-Heat Scenario Days"})
    )
    station_years = per_year.groupby("Station ID")["Historical Year"].nunique()
    require(station_years.eq(5).all(), "Each station must have five historical years")
    return gpd.GeoDataFrame(
        stations,
        geometry=gpd.points_from_xy(stations["Longitude"], stations["Latitude"]),
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)


def interpolate_high_heat_days(
    municipalities: gpd.GeoDataFrame, stations: gpd.GeoDataFrame
) -> np.ndarray:
    centroids = municipalities.geometry.centroid
    station_xy = np.column_stack((stations.geometry.x, stations.geometry.y))
    values = stations["Expected High-Heat Scenario Days"].to_numpy(dtype=float)
    estimates: list[float] = []
    for point in centroids:
        distances = np.hypot(station_xy[:, 0] - point.x, station_xy[:, 1] - point.y)
        order = np.argsort(distances)[:IDW_NEIGHBORS]
        nearest_distances = distances[order]
        if nearest_distances[0] < 1e-8:
            estimate = values[order[0]]
        else:
            weights = 1.0 / np.power(nearest_distances, IDW_POWER)
            estimate = np.average(values[order], weights=weights)
        estimates.append(float(np.clip(estimate, 0.0, PLANNING_HORIZON_DAYS)))
    return np.asarray(estimates)


def probability_from_odds(odds: pd.Series | np.ndarray) -> pd.Series | np.ndarray:
    return odds / (1.0 + odds)


def build_scenario() -> gpd.GeoDataFrame:
    for source in (COOLING_NEED_SOURCE, MORTALITY_SOURCE):
        require(source.is_file(), f"Missing source: {source}")
    municipalities = load_municipalities()
    cooling = gpd.read_parquet(COOLING_NEED_SOURCE)
    cooling = assign_municipalities(cooling, municipalities)
    demand_columns = [
        "No-Placement Unprotected Older-Person-Days",
        "No-Placement Unprotected Older-Person-Days Lower Bound",
        "No-Placement Unprotected Older-Person-Days Upper Bound",
    ]
    missing = sorted(set(demand_columns) - set(cooling.columns))
    require(not missing, f"Cooling source is missing variables: {missing}")
    demand = cooling.groupby("Municipality Code", as_index=False)[demand_columns].sum()

    mortality = pd.read_parquet(MORTALITY_SOURCE)
    mortality = mortality.loc[mortality["Age Group"].eq("65+")].copy()
    mortality["Municipality Code"] = mortality["Municipality Code"].astype("string")
    require(len(mortality) == 45, "Expected one age-65-plus mortality row per municipality")
    mortality_columns = [
        "Municipality Code",
        "Municipality",
        "Population at Risk",
        "All-Cause Deaths",
        "Baseline Period Start",
        "Baseline Period End",
        "Baseline Mortality Rate per 100,000",
        "Mortality Data Status",
        "Denominator Status",
    ]

    scenario = municipalities.merge(demand, on="Municipality Code", how="left").merge(
        mortality[mortality_columns], on="Municipality Code", how="left"
    )
    require(scenario["Municipality"].notna().all(), "Mortality baseline join failed")
    scenario[demand_columns] = scenario[demand_columns].fillna(0.0)
    stations = station_high_heat_days()
    scenario["Expected High-Heat Scenario Days"] = interpolate_high_heat_days(
        scenario, stations
    )
    scenario["High-Heat Scenario Definition"] = (
        "five_year_mean_days_with_jma_hot_day_or_hot_night"
    )
    scenario["Historical Heat Scenario Start Year"] = 2021
    scenario["Historical Heat Scenario End Year"] = 2025
    scenario["Cooling Protection Planning Horizon Days"] = PLANNING_HORIZON_DAYS

    annual_rate = pd.to_numeric(
        scenario["Baseline Mortality Rate per 100,000"], errors="raise"
    )
    scenario["Baseline Daily Mortality Probability"] = annual_rate / 100_000.0 / 365.25
    baseline_odds = scenario["Baseline Daily Mortality Probability"] / (
        1.0 - scenario["Baseline Daily Mortality Probability"]
    )
    protected_odds = baseline_odds * WITH_AC_EXTREME_HEAT_OR
    scenario["Effective-Cooling High-Heat Daily Mortality Probability"] = (
        probability_from_odds(protected_odds)
    )
    scenario["No-Effective-Cooling Relative Odds Ratio"] = NO_AC_VS_AC_RELATIVE_OR
    scenario["No-Effective-Cooling Relative Odds Ratio Lower 95% CI"] = (
        NO_AC_VS_AC_RELATIVE_OR_LOWER_95
    )
    scenario["No-Effective-Cooling Relative Odds Ratio Upper 95% CI"] = (
        NO_AC_VS_AC_RELATIVE_OR_UPPER_95
    )

    protected_probability = scenario[
        "Effective-Cooling High-Heat Daily Mortality Probability"
    ]
    protected_odds = protected_probability / (1.0 - protected_probability)
    high_heat_days = scenario["Expected High-Heat Scenario Days"]
    non_high_heat_days = PLANNING_HORIZON_DAYS - high_heat_days
    baseline_probability = scenario["Baseline Daily Mortality Probability"]
    scenario["Effective-Cooling 30-Day Mortality Risk"] = 1.0 - (
        np.power(1.0 - baseline_probability, non_high_heat_days)
        * np.power(1.0 - protected_probability, high_heat_days)
    )
    risk_contrasts: dict[str, float] = {
        "": NO_AC_VS_AC_RELATIVE_OR,
        " Lower 95% CI": NO_AC_VS_AC_RELATIVE_OR_LOWER_95,
        " Upper 95% CI": NO_AC_VS_AC_RELATIVE_OR_UPPER_95,
    }
    for suffix, relative_or in risk_contrasts.items():
        no_cooling_probability = probability_from_odds(protected_odds * relative_or)
        daily_difference = no_cooling_probability - protected_probability
        scenario[f"Cooling-Loss Daily Mortality Risk Contrast{suffix}"] = daily_difference
        no_cooling_30_day_risk = 1.0 - (
            np.power(1.0 - baseline_probability, non_high_heat_days)
            * np.power(1.0 - no_cooling_probability, high_heat_days)
        )
        scenario[f"No-Effective-Cooling 30-Day Mortality Risk{suffix}"] = (
            no_cooling_30_day_risk
        )
        scenario[
            f"Cooling-Loss Relative 30-Day Mortality Burden Increase %{suffix}"
        ] = (
            no_cooling_30_day_risk
            / scenario["Effective-Cooling 30-Day Mortality Risk"]
            - 1.0
        ) * 100.0
        scenario[f"Cooling-Loss Incremental Mortality Risk per 100,000{suffix}"] = (
            (
                no_cooling_30_day_risk
                - scenario["Effective-Cooling 30-Day Mortality Risk"]
            )
            * 100_000.0
        )
        scenario[f"Incremental Cooling-Loss-Related Excess Deaths{suffix}"] = (
            (
                no_cooling_30_day_risk
                - scenario["Effective-Cooling 30-Day Mortality Risk"]
            )
            * scenario["No-Placement Unprotected Older-Person-Days"]
            / PLANNING_HORIZON_DAYS
        )

    scenario["Cooling-Loss Effect Estimate ID"] = EFFECT_ESTIMATE_ID
    scenario["Cooling-Loss Effect Source"] = EFFECT_SOURCE
    scenario["Cooling-Loss Effect Source URL"] = EFFECT_SOURCE_URL
    scenario["Cooling-Loss Mortality Scenario Status"] = (
        "literature_anchored_no_verified_placement_planning_scenario"
    )
    scenario["Interpretation Limit"] = (
        "not_observed_or_earthquake_attributable_mortality; effect transferred from "
        "older institutional residents outside Japan; confidence interval covers only "
        "the published cooling-effect parameter"
    )
    return gpd.GeoDataFrame(scenario, geometry="geometry", crs=MAP_CRS)


def validate(frame: gpd.GeoDataFrame) -> None:
    require(len(frame) == 45, "Expected 45 municipality rows")
    require(frame.geometry.notna().all(), "Municipality geometry is missing")
    require(frame["Baseline Mortality Rate per 100,000"].notna().all(), "Missing mortality baseline")
    require(frame["Expected High-Heat Scenario Days"].between(0, 30).all(), "Invalid heat days")
    for column in (
        "Cooling-Loss Incremental Mortality Risk per 100,000",
        "Cooling-Loss Incremental Mortality Risk per 100,000 Lower 95% CI",
        "Cooling-Loss Incremental Mortality Risk per 100,000 Upper 95% CI",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase %",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI",
        "Incremental Cooling-Loss-Related Excess Deaths",
        "Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI",
        "Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI",
    ):
        require(frame[column].ge(0).all(), f"{column} must be nonnegative")
    require(
        (
            frame["Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI"]
            <= frame["Incremental Cooling-Loss-Related Excess Deaths"]
        ).all(),
        "Mortality lower interval exceeds the central estimate",
    )
    require(
        (
            frame["Incremental Cooling-Loss-Related Excess Deaths"]
            <= frame["Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI"]
        ).all(),
        "Mortality central estimate exceeds the upper interval",
    )
    require(
        (
            frame[
                "Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI"
            ]
            <= frame["Cooling-Loss Relative 30-Day Mortality Burden Increase %"]
        ).all(),
        "Relative mortality-burden lower interval exceeds the central estimate",
    )
    require(
        (
            frame["Cooling-Loss Relative 30-Day Mortality Burden Increase %"]
            <= frame[
                "Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI"
            ]
        ).all(),
        "Relative mortality-burden central estimate exceeds the upper interval",
    )


def main() -> int:
    frame = build_scenario()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    totals = frame[
        [
            "Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI",
            "Incremental Cooling-Loss-Related Excess Deaths",
            "Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI",
        ]
    ].sum()
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    print(
        "expected high-heat days: "
        f"{frame['Expected High-Heat Scenario Days'].min():.2f}-"
        f"{frame['Expected High-Heat Scenario Days'].max():.2f}"
    )
    print(totals.to_string(float_format=lambda value: f"{value:.6f}"))
    affected_population = frame["No-Placement Unprotected Older-Person-Days"] / 30.0
    effective_deaths = (
        affected_population * frame["Effective-Cooling 30-Day Mortality Risk"]
    ).sum()
    for label, column in (
        (
            "lower",
            "No-Effective-Cooling 30-Day Mortality Risk Lower 95% CI",
        ),
        ("central", "No-Effective-Cooling 30-Day Mortality Risk"),
        (
            "upper",
            "No-Effective-Cooling 30-Day Mortality Risk Upper 95% CI",
        ),
    ):
        no_cooling_deaths = (affected_population * frame[column]).sum()
        increase = 100.0 * (no_cooling_deaths / effective_deaths - 1.0)
        print(f"prefecture relative burden increase {label}: {increase:.3f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
