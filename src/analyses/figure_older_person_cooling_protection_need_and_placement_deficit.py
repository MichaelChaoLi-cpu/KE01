#!/usr/bin/env python3
"""Older-Person Cooling Protection Need and Placement Deficit.

Early planning version: map modeled older-person cooling-assessment need, a 30-day
no-verified-placement demand-side bound, and nominal access to designated shelters.
No unverified facility cooling capacity is treated as zero.
"""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pyproj import Transformer
from shapely.geometry import LineString, Point


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_PATH = ROOT / (
    "data/processed/"
    "kumamoto_cooling_protection_need_scenarios_preprocessed.parquet"
)
SHELTER_PATH = (
    ROOT / "data/processed/kumamoto_designated_shelters_preprocessed.parquet"
)
SMALL_AREA_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PATH = ROOT / (
    "data/results/figures/"
    "Figure_older_person_cooling_protection_need_and_placement_deficit.png"
)

MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:4326"
EPICENTER_LATITUDE = 32.6
EPICENTER_LONGITUDE = 130.7


def load_inputs() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Load the scenario, designated shelters, and municipality boundaries."""
    if not SCENARIO_PATH.is_file():
        raise FileNotFoundError(f"Missing scenario input: {SCENARIO_PATH}")
    if not SHELTER_PATH.is_file():
        raise FileNotFoundError(f"Missing shelter input: {SHELTER_PATH}")
    if not SMALL_AREA_PATH.is_file():
        raise FileNotFoundError(f"Missing boundary input: {SMALL_AREA_PATH}")

    scenario = gpd.read_parquet(SCENARIO_PATH).to_crs(MAP_CRS)
    shelter_table = pd.read_parquet(SHELTER_PATH)
    shelters = gpd.GeoDataFrame(
        shelter_table.copy(),
        geometry=gpd.points_from_xy(
            shelter_table["Longitude"], shelter_table["Latitude"]
        ),
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)
    small_areas = gpd.read_file(
        SMALL_AREA_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(by=["CITY", "CITY_NAME"], as_index=False)
    return scenario, shelters, municipalities


def validate_inputs(scenario: gpd.GeoDataFrame, shelters: gpd.GeoDataFrame) -> None:
    """Enforce the interpretation limits required by the analytical framework."""
    required = {
        "Estimated Affected Population Age 65+",
        "Estimated Affected Population Age 65+ Lower Bound",
        "Estimated Affected Population Age 65+ Upper Bound",
        "No-Placement Unprotected Older-Person-Days",
        "No-Placement Unprotected Older-Person-Days Lower Bound",
        "No-Placement Unprotected Older-Person-Days Upper Bound",
        "Nearest Designated Shelter Distance m",
        "Effective Cooled Capacity",
        "Cooling Capacity Gap",
        "Cooling Protection Scenario Status",
    }
    missing = sorted(required - set(scenario.columns))
    if missing:
        raise ValueError(f"Scenario is missing planned variables: {missing}")
    if scenario.empty or shelters.empty:
        raise ValueError("Scenario and shelter inputs must be non-empty")
    if not scenario["Effective Cooled Capacity"].isna().all():
        raise ValueError("Unverified effective cooled capacity must remain missing")
    if not scenario["Cooling Capacity Gap"].isna().all():
        raise ValueError("Actual cooling capacity gap must remain missing")
    expected_status = "no_verified_placement_demand_side_bound"
    if not scenario["Cooling Protection Scenario Status"].eq(expected_status).all():
        raise ValueError("Unexpected cooling-protection scenario status")

    central = scenario["Estimated Affected Population Age 65+"]
    lower = scenario["Estimated Affected Population Age 65+ Lower Bound"]
    upper = scenario["Estimated Affected Population Age 65+ Upper Bound"]
    if not ((lower <= central) & (central <= upper)).all():
        raise ValueError("Older-person assessment-population bounds are invalid")
    if (scenario["Nearest Designated Shelter Distance m"] < 0).any():
        raise ValueError("Shelter distance cannot be negative")


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
    """Draw labelled longitude/latitude lines and a complete map frame."""
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
    """Add a projected scale bar above the figure-level legend."""
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
    """Use robust log scaling for highly skewed small-area scenario estimates."""
    numeric = pd.to_numeric(values, errors="coerce")
    positive = numeric.loc[numeric.gt(0)]
    if positive.empty:
        raise ValueError("Map variable contains no positive values")
    vmin = float(positive.quantile(0.01))
    vmax = float(positive.quantile(0.995))
    return LogNorm(
        vmin=max(vmin, np.finfo(float).tiny),
        vmax=max(vmax, vmin * 2),
        clip=True,
    )


def plot_scenario_map(
    ax: plt.Axes,
    fig: plt.Figure,
    scenario: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
    column: str,
    colorbar_label: str,
) -> None:
    values = pd.to_numeric(scenario[column], errors="coerce")
    norm = positive_log_norm(values)
    visible = scenario.assign(_plot_value=values.mask(values.le(0)))
    municipalities.plot(ax=ax, color="#ECEEEE", edgecolor="none", zorder=0)
    visible.plot(
        ax=ax,
        column="_plot_value",
        cmap="YlOrRd",
        norm=norm,
        linewidth=0,
        missing_kwds={"color": "#DDE1E2"},
        rasterized=True,
        zorder=1,
    )
    municipalities.boundary.plot(
        ax=ax, color="#58656D", linewidth=0.34, alpha=0.80, zorder=5
    )
    colorbar = fig.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap="YlOrRd"),
        ax=ax,
        orientation="horizontal",
        fraction=0.040,
        pad=0.035,
        extend="both",
    )
    colorbar.set_label(colorbar_label, fontsize=8.0, labelpad=3)
    colorbar.ax.tick_params(labelsize=7.0, length=2.5)


def plot_access_map(
    ax: plt.Axes,
    fig: plt.Figure,
    scenario: gpd.GeoDataFrame,
    shelters: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
) -> None:
    distance_km = pd.to_numeric(
        scenario["Nearest Designated Shelter Distance m"], errors="coerce"
    ) / 1_000
    vmax = float(distance_km.quantile(0.995))
    norm = Normalize(vmin=0, vmax=vmax, clip=True)
    visible = scenario.assign(_distance_km=distance_km)
    municipalities.plot(ax=ax, color="#ECEEEE", edgecolor="none", zorder=0)
    visible.plot(
        ax=ax,
        column="_distance_km",
        cmap="magma_r",
        norm=norm,
        linewidth=0,
        rasterized=True,
        zorder=1,
    )
    municipalities.boundary.plot(
        ax=ax, color="#58656D", linewidth=0.34, alpha=0.80, zorder=5
    )
    shelters.plot(
        ax=ax,
        marker="o",
        markersize=3.2,
        facecolor="#20BFC8",
        edgecolor="white",
        linewidth=0.20,
        alpha=0.82,
        rasterized=True,
        zorder=7,
    )
    colorbar = fig.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap="magma_r"),
        ax=ax,
        orientation="horizontal",
        fraction=0.040,
        pad=0.035,
        extend="max",
    )
    colorbar.set_label(
        "Straight-line distance to nearest designated shelter (km)",
        fontsize=8.0,
        labelpad=3,
    )
    colorbar.ax.tick_params(labelsize=7.0, length=2.5)


def make_figure(
    scenario: gpd.GeoDataFrame,
    shelters: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
) -> plt.Figure:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(16.2, 7.1), constrained_layout=False)
    central_total = scenario["Estimated Affected Population Age 65+"].sum()

    plot_scenario_map(
        axes[0],
        fig,
        scenario,
        municipalities,
        "Estimated Affected Population Age 65+",
        "Older-person cooling-assessment population per grid (central)",
    )
    plot_scenario_map(
        axes[1],
        fig,
        scenario,
        municipalities,
        "No-Placement Unprotected Older-Person-Days Upper Bound",
        "30-day no-placement older-person-days per grid (pointwise upper)",
    )
    plot_access_map(axes[2], fig, scenario, shelters, municipalities)

    epicenter = gpd.GeoDataFrame(
        {"label": ["Official epicenter"]},
        geometry=[Point(EPICENTER_LONGITUDE, EPICENTER_LATITUDE)],
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)
    for ax in axes[:2]:
        epicenter.plot(
            ax=ax,
            marker="*",
            markersize=105,
            facecolor="#19A7AE",
            edgecolor="white",
            linewidth=0.9,
            zorder=12,
        )

    map_bounds = municipalities.total_bounds
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    for ax in axes:
        ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
        ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
        add_graticule(ax, geographic_bounds)
        ax.set_aspect("equal")

    panel_titles = (
        ("a", f"Cooling-assessment population (central total {central_total:.0f})"),
        ("b", "30-day no-placement planning bound (pointwise high)"),
        ("c", "Nominal designated-shelter access (operation unverified)"),
    )
    for ax, (letter, title) in zip(axes, panel_titles, strict=True):
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
        Line2D(
            [0],
            [0],
            marker="o",
            markerfacecolor="#20BFC8",
            markeredgecolor="white",
            color="none",
            markersize=5.5,
            label="Designated shelter (operation and cooling unverified)",
        ),
        Patch(
            facecolor="#DDE1E2",
            edgecolor="#AAB2B7",
            label="Zero or no modeled cooling-assessment need",
        ),
        Line2D(
            [0],
            [0],
            color="none",
            label="Panel b is a local pointwise high scenario; values are not additive",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.015),
        ncol=4,
        frameon=False,
        fontsize=7.5,
        handlelength=1.8,
        columnspacing=1.6,
    )
    fig.subplots_adjust(
        left=0.045,
        right=0.992,
        top=0.925,
        bottom=0.115,
        wspace=0.10,
    )
    return fig


def main() -> int:
    scenario, shelters, municipalities = load_inputs()
    validate_inputs(scenario, shelters)
    figure = make_figure(scenario, shelters, municipalities)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=400, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
