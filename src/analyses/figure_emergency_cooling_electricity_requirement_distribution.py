#!/usr/bin/env python3
"""Emergency Cooling Electricity Requirement Distribution.

Plan: map Central-scenario municipality peak power and daily electricity with
distinct unit-specific palettes, then compare demand across approved bundles.
Framework: AnaSOP Sections 5-7 demand-side equations q, Q, P_req, and E_req.
Verified supply and the actual emergency power gap remain unidentified.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pyproj import Transformer
from shapely.geometry import LineString, Point


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_PATH = ROOT / (
    "data/processed/kumamoto_emergency_cooling_power_scenarios_preprocessed.parquet"
)
SMALL_AREA_PATH = ROOT / (
    "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PATH = ROOT / (
    "data/results/figures/"
    "Figure_emergency_cooling_electricity_requirement_distribution.png"
)

MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:4326"
EPICENTER_LATITUDE = 32.6
EPICENTER_LONGITUDE = 130.7
SCENARIO_ORDER = ["Low", "Central", "High"]
SCENARIO_COLORS = ["#6BAED6", "#F28E2B", "#C33C32"]


def load_inputs() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    if not SCENARIO_PATH.is_file():
        raise FileNotFoundError(f"Missing scenario input: {SCENARIO_PATH}")
    if not SMALL_AREA_PATH.is_file():
        raise FileNotFoundError(f"Missing boundary input: {SMALL_AREA_PATH}")
    scenarios = gpd.read_parquet(SCENARIO_PATH).to_crs(MAP_CRS)
    small_areas = gpd.read_file(
        SMALL_AREA_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(
        by=["CITY", "CITY_NAME"], as_index=False
    ).rename(columns={"CITY": "Municipality Code", "CITY_NAME": "Municipality"})
    municipalities["Municipality Code"] = municipalities[
        "Municipality Code"
    ].astype("string")
    return scenarios, municipalities


def validate_inputs(scenarios: gpd.GeoDataFrame) -> None:
    required = {
        "Municipality Code",
        "Municipality",
        "Estimated Affected Population Age 65+",
        "Power Demand Scenario",
        "Minimum Shelter Living Area m2 per Person",
        "Cooling Load Density W per m2",
        "Cooling Thermal Load W per Person",
        "Scenario Cooling System COP",
        "Scenario Peak Load Diversity Factor",
        "Scenario Cooling Operating Hours per Day",
        "Cooling Thermal Load kW",
        "Required Peak Cooling Electric Power kW",
        "Required Daily Cooling Electricity kWh",
        "Cooling Power Scenario Status",
        "Verified Available Electric Power kW",
        "Emergency Cooling Power Gap kW",
    }
    missing = sorted(required - set(scenarios.columns))
    if missing:
        raise ValueError(f"Power scenario data are missing variables: {missing}")
    if set(scenarios["Power Demand Scenario"]) != set(SCENARIO_ORDER):
        raise ValueError("Low, Central, and High scenarios are required")
    if not scenarios["Cooling Power Scenario Status"].eq(
        "demand_side_only_no_verified_supply"
    ).all():
        raise ValueError("Unexpected power scenario status")
    for column in (
        "Verified Available Electric Power kW",
        "Emergency Cooling Power Gap kW",
    ):
        if not scenarios[column].isna().all():
            raise ValueError(f"{column} must remain missing")
    population_totals = scenarios.groupby("Power Demand Scenario")[
        "Estimated Affected Population Age 65+"
    ].sum()
    if not np.allclose(population_totals, population_totals.iloc[0]):
        raise ValueError("Engineering scenarios do not use the same population")
    peak = scenarios.groupby("Power Demand Scenario")[
        "Required Peak Cooling Electric Power kW"
    ].sum().reindex(SCENARIO_ORDER)
    energy = scenarios.groupby("Power Demand Scenario")[
        "Required Daily Cooling Electricity kWh"
    ].sum().reindex(SCENARIO_ORDER)
    if not peak.is_monotonic_increasing or not energy.is_monotonic_increasing:
        raise ValueError("Power scenario totals must increase from Low to High")


def aggregate_municipalities(
    scenarios: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    central = scenarios.loc[
        scenarios["Power Demand Scenario"].eq("Central")
    ].copy()
    totals = (
        central.groupby("Municipality Code", as_index=False)[
            [
                "Estimated Affected Population Age 65+",
                "Cooling Thermal Load kW",
                "Required Peak Cooling Electric Power kW",
                "Required Daily Cooling Electricity kWh",
            ]
        ]
        .sum()
    )
    mapped = municipalities.merge(totals, on="Municipality Code", how="left")
    value_columns = [
        "Estimated Affected Population Age 65+",
        "Cooling Thermal Load kW",
        "Required Peak Cooling Electric Power kW",
        "Required Daily Cooling Electricity kWh",
    ]
    mapped[value_columns] = mapped[value_columns].fillna(0.0)
    if not np.isclose(
        mapped["Required Peak Cooling Electric Power kW"].sum(),
        central["Required Peak Cooling Electric Power kW"].sum(),
    ):
        raise ValueError("Municipality peak-power aggregation changed the total")
    return gpd.GeoDataFrame(mapped, geometry="geometry", crs=MAP_CRS)


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + i * step, 8) for i in range(max(0, count))]


def add_graticule(
    ax: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    step: float = 0.25,
) -> None:
    lon_min, lat_min, lon_max, lat_max = geographic_bounds
    lon_values = graticule_values(lon_min, lon_max, step)
    lat_values = graticule_values(lat_min, lat_max, step)
    samples = 160
    lines: list[LineString] = []
    for longitude in lon_values:
        lines.append(
            LineString(
                zip(
                    np.full(samples, longitude),
                    np.linspace(lat_min - step, lat_max + step, samples),
                    strict=True,
                )
            )
        )
    for latitude in lat_values:
        lines.append(
            LineString(
                zip(
                    np.linspace(lon_min - step, lon_max + step, samples),
                    np.full(samples, latitude),
                    strict=True,
                )
            )
        )
    gpd.GeoSeries(lines, crs=GEOGRAPHIC_CRS).to_crs(MAP_CRS).plot(
        ax=ax,
        color="#77838C",
        linewidth=0.42,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.43,
        zorder=4,
    )
    transformer = Transformer.from_crs(GEOGRAPHIC_CRS, MAP_CRS, always_xy=True)
    centre_latitude = (lat_min + lat_max) / 2
    centre_longitude = (lon_min + lon_max) / 2
    label_style = {"fontsize": 7.0, "color": "#46515A", "clip_on": False}
    for longitude in lon_values:
        x_position, _ = transformer.transform(longitude, centre_latitude)
        ax.text(
            x_position,
            -0.014,
            f"{longitude:.2f}°E",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            **label_style,
        )
    for latitude in lat_values:
        _, y_position = transformer.transform(centre_longitude, latitude)
        ax.text(
            -0.012,
            y_position,
            f"{latitude:.2f}°N",
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="center",
            **label_style,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#303A40")
        spine.set_linewidth(0.85)
        spine.set_zorder(20)


def add_scale_bar(ax: plt.Axes, length_km: int = 25) -> None:
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    length = length_km * 1_000
    x0 = xmin + 0.07 * (xmax - xmin)
    y0 = ymin + 0.065 * (ymax - ymin)
    tick_height = 750
    ax.plot([x0, x0 + length], [y0, y0], color="#263238", linewidth=2, zorder=15)
    for x_position in (x0, x0 + length):
        ax.plot(
            [x_position, x_position],
            [y0 - tick_height, y0 + tick_height],
            color="#263238",
            linewidth=1.1,
            zorder=15,
        )
    ax.text(
        x0 + length / 2,
        y0 + 1_650,
        f"{length_km} km",
        ha="center",
        va="bottom",
        fontsize=7.6,
        color="#263238",
        zorder=15,
    )


def positive_log_norm(values: pd.Series) -> LogNorm:
    positive = pd.to_numeric(values, errors="coerce").loc[lambda x: x.gt(0)]
    if positive.empty:
        raise ValueError("Municipality map has no positive values")
    vmin = float(positive.min())
    vmax = float(positive.max())
    return LogNorm(vmin=vmin, vmax=max(vmax, vmin * 2), clip=True)


def plot_municipality_map(
    ax: plt.Axes,
    fig: plt.Figure,
    municipalities: gpd.GeoDataFrame,
    column: str,
    cmap_name: str,
    colorbar_label: str,
) -> None:
    values = pd.to_numeric(municipalities[column], errors="coerce")
    norm = positive_log_norm(values)
    visible = municipalities.assign(_plot_value=values.mask(values.le(0)))
    visible.plot(
        ax=ax,
        column="_plot_value",
        cmap=cmap_name,
        norm=norm,
        edgecolor="#5D6870",
        linewidth=0.42,
        missing_kwds={"color": "#DDE1E2"},
        zorder=1,
    )
    colorbar = fig.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap_name),
        ax=ax,
        orientation="horizontal",
        fraction=0.040,
        pad=0.035,
        extend="both",
    )
    colorbar.set_label(colorbar_label, fontsize=8.0, labelpad=3)
    colorbar.ax.tick_params(labelsize=7.0, length=2.5)


def plot_scenario_sensitivity(ax: plt.Axes, scenarios: gpd.GeoDataFrame) -> None:
    totals = (
        scenarios.groupby("Power Demand Scenario")
        .agg(
            peak_kw=("Required Peak Cooling Electric Power kW", "sum"),
            daily_kwh=("Required Daily Cooling Electricity kWh", "sum"),
            load_density=("Cooling Load Density W per m2", "first"),
            cop=("Scenario Cooling System COP", "first"),
            diversity=("Scenario Peak Load Diversity Factor", "first"),
            hours=("Scenario Cooling Operating Hours per Day", "first"),
        )
        .reindex(SCENARIO_ORDER)
    )
    positions = np.arange(len(totals))
    bars = ax.bar(
        positions,
        totals["daily_kwh"],
        width=0.62,
        color=SCENARIO_COLORS,
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    y_padding = float(totals["daily_kwh"].max()) * 0.045
    for bar, (_, row) in zip(bars, totals.iterrows(), strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + y_padding,
            f"{row['daily_kwh']:,.0f} kWh/day\nPeak {row['peak_kw']:.1f} kW",
            ha="center",
            va="bottom",
            fontsize=8.0,
            color="#263238",
        )
    tick_labels = [
        f"{name}\n{row.load_density:.0f} W/m² · COP {row.cop:.1f}\n"
        f"f={row.diversity:.1f} · {row.hours:.0f} h/day"
        for name, row in totals.iterrows()
    ]
    ax.set_xticks(positions, tick_labels)
    ax.tick_params(axis="x", labelsize=7.8, length=0, pad=7)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.set_ylabel(
        "Prefecture daily cooling electricity (kWh/day)",
        fontsize=8.4,
        labelpad=2,
    )
    ax.set_ylim(0, float(totals["daily_kwh"].max()) * 1.22)
    ax.grid(axis="y", color="#CCD3D7", linewidth=0.55, linestyle=(0, (2, 3)))
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#303A40")
        spine.set_linewidth(0.85)


def add_panel_title(ax: plt.Axes, letter: str, title: str) -> None:
    ax.text(
        0.0,
        1.012,
        letter,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#20262B",
        clip_on=False,
    )
    ax.text(
        0.055,
        1.012,
        title,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.2,
        color="#20262B",
        clip_on=False,
    )


def make_figure(
    scenarios: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
) -> plt.Figure:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(16.2, 7.1),
        constrained_layout=False,
        gridspec_kw={"width_ratios": [1.0, 1.0, 0.92]},
    )
    mapped = aggregate_municipalities(scenarios, municipalities)
    plot_municipality_map(
        axes[0],
        fig,
        mapped,
        "Required Peak Cooling Electric Power kW",
        "YlOrRd",
        "Required peak cooling electric power (kW; Central)",
    )
    plot_municipality_map(
        axes[1],
        fig,
        mapped,
        "Required Daily Cooling Electricity kWh",
        "YlGnBu",
        "Required daily cooling electricity (kWh/day; Central)",
    )
    plot_scenario_sensitivity(axes[2], scenarios)

    epicenter = gpd.GeoDataFrame(
        {"label": ["Official epicenter"]},
        geometry=[Point(EPICENTER_LONGITUDE, EPICENTER_LATITUDE)],
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)
    map_bounds = municipalities.total_bounds
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    for ax in axes[:2]:
        ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
        ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
        add_graticule(ax, geographic_bounds)
        epicenter.plot(
            ax=ax,
            marker="*",
            markersize=105,
            facecolor="#19A7AE",
            edgecolor="white",
            linewidth=0.9,
            zorder=12,
        )
        ax.set_aspect("equal")

    add_panel_title(axes[0], "a", "Municipality peak power demand (Central scenario)")
    add_panel_title(axes[1], "b", "Municipality daily electricity demand (Central scenario)")
    add_panel_title(axes[2], "c", "Prefecture demand sensitivity")
    add_scale_bar(axes[0])

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="*",
            markerfacecolor="#19A7AE",
            markeredgecolor="white",
            color="none",
            markersize=10,
            label="Official epicenter",
        ),
        Patch(
            facecolor="#DDE1E2",
            edgecolor="#AAB2B7",
            label="Zero or no modeled cooling-electricity demand",
        ),
        Line2D(
            [0],
            [0],
            color="none",
            label="Demand-side scenarios only; verified supply and power gap not estimated",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.017),
        ncol=3,
        frameon=False,
        fontsize=7.6,
        handlelength=1.8,
        columnspacing=2.2,
    )
    fig.subplots_adjust(
        left=0.045,
        right=0.988,
        top=0.925,
        bottom=0.135,
        wspace=0.17,
    )
    return fig


def main() -> int:
    scenarios, municipalities = load_inputs()
    validate_inputs(scenarios)
    figure = make_figure(scenarios, municipalities)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=400, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
