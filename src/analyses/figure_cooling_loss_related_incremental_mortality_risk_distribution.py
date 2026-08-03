#!/usr/bin/env python3
"""Cooling-Loss-Related Incremental Mortality Risk Distribution.

Plan: map the five-year matching-period high-heat scenario, the modeled
cooling-loss mortality-risk contrast, and the relative increase in 30-day
mortality burden under the no-verified-placement demand-side bound.
Framework: AnaSOP Sections 5-7 cooled-versus-uncooled mortality contrast with
outdoor weather held fixed. Results are transferable planning scenarios, not
observed or earthquake-attributable deaths.
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
    "data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet"
)
OUTPUT_PATH = ROOT / (
    "data/results/figures/"
    "Figure_cooling_loss_related_incremental_mortality_risk_distribution.png"
)

MAP_CRS = "EPSG:6670"
GEOGRAPHIC_CRS = "EPSG:4326"
EPICENTER_LATITUDE = 32.6
EPICENTER_LONGITUDE = 130.7


def load_inputs() -> gpd.GeoDataFrame:
    if not SCENARIO_PATH.is_file():
        raise FileNotFoundError(f"Missing scenario input: {SCENARIO_PATH}")
    return gpd.read_parquet(SCENARIO_PATH).to_crs(MAP_CRS)


def validate_inputs(frame: gpd.GeoDataFrame) -> None:
    required = {
        "Municipality Code",
        "Municipality",
        "Expected High-Heat Scenario Days",
        "Baseline Mortality Rate per 100,000",
        "No-Placement Unprotected Older-Person-Days",
        "Cooling-Loss Incremental Mortality Risk per 100,000",
        "Cooling-Loss Incremental Mortality Risk per 100,000 Lower 95% CI",
        "Cooling-Loss Incremental Mortality Risk per 100,000 Upper 95% CI",
        "Incremental Cooling-Loss-Related Excess Deaths",
        "Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI",
        "Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI",
        "Effective-Cooling 30-Day Mortality Risk",
        "No-Effective-Cooling 30-Day Mortality Risk",
        "No-Effective-Cooling 30-Day Mortality Risk Lower 95% CI",
        "No-Effective-Cooling 30-Day Mortality Risk Upper 95% CI",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase %",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI",
        "Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI",
        "Cooling-Loss Mortality Scenario Status",
        "geometry",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Mortality scenario is missing variables: {missing}")
    if len(frame) != 45 or frame["Municipality Code"].nunique() != 45:
        raise ValueError("Expected one result for each of 45 municipalities")
    if not frame["Cooling-Loss Mortality Scenario Status"].eq(
        "literature_anchored_no_verified_placement_planning_scenario"
    ).all():
        raise ValueError("Unexpected mortality scenario status")
    if not frame["Expected High-Heat Scenario Days"].between(0, 30).all():
        raise ValueError("Expected high-heat days must be within the 30-day horizon")
    lower = frame["Incremental Cooling-Loss-Related Excess Deaths Lower 95% CI"]
    central = frame["Incremental Cooling-Loss-Related Excess Deaths"]
    upper = frame["Incremental Cooling-Loss-Related Excess Deaths Upper 95% CI"]
    if not ((lower <= central) & (central <= upper)).all():
        raise ValueError("Mortality interval ordering failed")


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
    y0 = ymin + 0.082 * (ymax - ymin)
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


def plot_map(
    ax: plt.Axes,
    fig: plt.Figure,
    frame: gpd.GeoDataFrame,
    column: str,
    cmap_name: str,
    colorbar_label: str,
    logarithmic: bool = False,
) -> None:
    values = pd.to_numeric(frame[column], errors="coerce")
    if logarithmic:
        positive = values[values > 0]
        norm: Normalize = LogNorm(
            vmin=float(positive.min()), vmax=float(positive.max()), clip=True
        )
        plot_values = values.mask(values <= 0)
    else:
        norm = Normalize(vmin=0.0, vmax=float(values.max()))
        plot_values = values
    frame.assign(_plot_value=plot_values).plot(
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
    )
    colorbar.set_label(colorbar_label, fontsize=8.0, labelpad=3)
    colorbar.ax.tick_params(labelsize=7.0, length=2.5)


def make_figure(frame: gpd.GeoDataFrame) -> plt.Figure:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(16.2, 7.1), constrained_layout=False)
    plot_map(
        axes[0],
        fig,
        frame,
        "Expected High-Heat Scenario Days",
        "YlOrRd",
        "Expected high-heat days in 30-day window",
    )
    plot_map(
        axes[1],
        fig,
        frame,
        "Cooling-Loss Incremental Mortality Risk per 100,000",
        "PuRd",
        "Incremental risk per 100,000 affected older persons",
    )
    plot_map(
        axes[2],
        fig,
        frame,
        "Cooling-Loss Relative 30-Day Mortality Burden Increase %",
        "magma_r",
        "Increase in 30-day mortality burden without cooling (%)",
    )

    epicenter = gpd.GeoDataFrame(
        {"label": ["Official epicenter"]},
        geometry=[Point(EPICENTER_LONGITUDE, EPICENTER_LATITUDE)],
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)
    map_bounds = frame.total_bounds
    geographic_bounds = tuple(frame.to_crs(GEOGRAPHIC_CRS).total_bounds)
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    for ax in axes:
        ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
        ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
        add_graticule(ax, geographic_bounds)
        epicenter.plot(
            ax=ax,
            marker="*",
            markersize=105,
            facecolor="#16A6AE",
            edgecolor="white",
            linewidth=0.9,
            zorder=12,
        )
        add_scale_bar(ax)
        ax.set_aspect("equal")

    add_panel_title(axes[0], "a", "Historical high-heat scenario")
    add_panel_title(axes[1], "b", "Cooling-loss incremental mortality risk")
    add_panel_title(axes[2], "c", "Relative mortality burden increase without cooling")

    affected_population = frame["No-Placement Unprotected Older-Person-Days"] / 30.0
    effective_deaths = (
        affected_population * frame["Effective-Cooling 30-Day Mortality Risk"]
    ).sum()
    central_no_cooling_deaths = (
        affected_population * frame["No-Effective-Cooling 30-Day Mortality Risk"]
    ).sum()
    lower_no_cooling_deaths = (
        affected_population
        * frame["No-Effective-Cooling 30-Day Mortality Risk Lower 95% CI"]
    ).sum()
    upper_no_cooling_deaths = (
        affected_population
        * frame["No-Effective-Cooling 30-Day Mortality Risk Upper 95% CI"]
    ).sum()
    central_increase = 100.0 * (central_no_cooling_deaths / effective_deaths - 1.0)
    lower_increase = 100.0 * (lower_no_cooling_deaths / effective_deaths - 1.0)
    upper_increase = 100.0 * (upper_no_cooling_deaths / effective_deaths - 1.0)
    axes[2].text(
        0.965,
        0.975,
        "Prefecture weighted increase\n"
        f"{central_increase:.2f}%\n"
        f"95% effect CI: {lower_increase:.2f}%–{upper_increase:.2f}%",
        transform=axes[2].transAxes,
        ha="right",
        va="top",
        fontsize=7.5,
        color="#263238",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "#9AA3A8",
            "linewidth": 0.6,
            "alpha": 0.91,
        },
        zorder=16,
    )

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="*",
            markerfacecolor="#16A6AE",
            markeredgecolor="white",
            color="none",
            markersize=10,
            label="Official epicenter",
        ),
        Patch(
            facecolor="#DDE1E2",
            edgecolor="#AAB2B7",
            label="Zero modeled value",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.017),
        ncol=2,
        frameon=False,
        fontsize=7.6,
        handlelength=1.8,
        columnspacing=2.2,
    )
    fig.subplots_adjust(left=0.045, right=0.988, top=0.925, bottom=0.135, wspace=0.13)
    return fig


def main() -> int:
    frame = load_inputs()
    validate_inputs(frame)
    figure = make_figure(frame)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=400, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
