#!/usr/bin/env python3
"""Functional Housing Loss and Older-Person Exposure.

Plan: separate reported residence-loss evidence at its disclosed geography from the
total-constrained structural residence-loss scenario and associated older-person exposure.
Framework: AnaSOP Sections 5-7, especially workflow steps 11-15 and the 27-scenario
epicentral-distance/exposure allocation model.
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
GRID_PATH = (
    ROOT / "data/processed/kumamoto_grid_exposure_estimates_preprocessed.parquet"
)
HOUSING_PATH = (
    ROOT / "data/processed/kumamoto_housing_damage_snapshots_preprocessed.parquet"
)
EVIDENCE_PATH = (
    ROOT / "data/processed/kumamoto_damage_evidence_registry_preprocessed.parquet"
)
SMALL_AREA_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PATH = (
    ROOT
    / "data/results/figures/Figure_functional_housing_loss_and_older_person_exposure.png"
)

MAP_CRS = "EPSG:6670"  # JGD2011 / Japan Plane Rectangular CS II
GEOGRAPHIC_CRS = "EPSG:4326"
EPICENTER_LATITUDE = 32.6
EPICENTER_LONGITUDE = 130.7
MINAMI_WARD_CODE = "104"
HIKAWA_TOWN_CODE = "468"


def load_inputs() -> tuple[
    gpd.GeoDataFrame,
    pd.DataFrame,
    pd.DataFrame,
    gpd.GeoDataFrame,
]:
    """Load analysis-ready inputs without changing processed data."""
    grid = gpd.read_parquet(GRID_PATH).to_crs(MAP_CRS)
    housing = pd.read_parquet(HOUSING_PATH)
    evidence = pd.read_parquet(EVIDENCE_PATH)
    small_areas = gpd.read_file(
        SMALL_AREA_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(by=["CITY", "CITY_NAME"], as_index=False)

    required_grid = {
        "Expected Functionally Lost Residences",
        "Expected Functionally Lost Residences Lower Bound",
        "Expected Functionally Lost Residences Upper Bound",
        "Estimated Affected Population Age 65+",
        "Estimated Affected Population Age 65+ Lower Bound",
        "Estimated Affected Population Age 65+ Upper Bound",
        "Epicentral Distance km",
        "Functional Housing Loss Status",
        "Estimation Status",
        "Damage Evidence Cutoff",
    }
    missing = sorted(required_grid.difference(grid.columns))
    if missing:
        raise ValueError(f"Missing planned grid variables: {missing}")
    if not {MINAMI_WARD_CODE, HIKAWA_TOWN_CODE}.issubset(set(municipalities["CITY"])):
        raise ValueError("Minami Ward or Hikawa Town boundary is missing")
    return grid, housing, evidence, municipalities


def latest_official_snapshot(housing: pd.DataFrame) -> pd.Series:
    """Select the latest prefecture snapshot with full- and half-collapse totals."""
    candidates = housing.loc[
        housing["Geographic Level"].eq("prefecture")
        & housing["Full Collapse Buildings"].notna()
        & housing["Half Collapse Buildings"].notna()
    ].copy()
    if candidates.empty:
        raise ValueError("No usable prefecture housing-damage snapshot")
    return candidates.sort_values("Observation Time").iloc[-1]


def minami_snapshot(housing: pd.DataFrame) -> pd.Series:
    """Select the latest disclosed Minami Ward housing-damage snapshot."""
    candidates = housing.loc[
        housing["Geographic Level"].eq("city_ward")
        & housing["Municipality"].eq("Kumamoto City, Minami Ward")
    ].copy()
    if candidates.empty:
        raise ValueError("No Minami Ward housing-damage snapshot")
    return candidates.sort_values("Observation Time").iloc[-1]


def hikawa_probable_count(evidence: pd.DataFrame) -> int:
    """Read the latest non-superseded Hikawa residential functional-loss evidence."""
    candidates = evidence.loc[
        evidence["Municipality"].eq("Hikawa Town")
        & evidence["Functional Housing Loss Status"].eq("probable_functional_loss")
    ].sort_values("Observation Time")
    if candidates.empty:
        return 0
    value = pd.to_numeric(
        candidates.iloc[-1]["Reported Affected Asset Count"], errors="coerce"
    )
    return 0 if pd.isna(value) else int(value)


def graticule_values(lower: float, upper: float, step: float) -> list[float]:
    """Return stable interior graticule values."""
    start = math.ceil((lower - 1e-9) / step) * step
    stop = math.floor((upper + 1e-9) / step) * step
    count = int(round((stop - start) / step)) + 1
    return [round(start + i * step, 8) for i in range(max(0, count))]


def add_graticule(
    ax: plt.Axes,
    geographic_bounds: tuple[float, float, float, float],
    step: float = 0.25,
) -> None:
    """Draw a labelled longitude/latitude graticule and a complete map frame."""
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
        color="#7D8992",
        linewidth=0.42,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.45,
        zorder=2,
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
    """Add a projected-distance scale bar inside the lower-left map frame."""
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    length = length_km * 1_000
    x0 = xmin + 0.07 * (xmax - xmin)
    y0 = ymin + 0.06 * (ymax - ymin)
    tick_height = 750
    ax.plot([x0, x0 + length], [y0, y0], color="#263238", linewidth=2.0, zorder=15)
    ax.plot(
        [x0, x0], [y0 - tick_height, y0 + tick_height],
        color="#263238", linewidth=1.1, zorder=15,
    )
    ax.plot(
        [x0 + length, x0 + length],
        [y0 - tick_height, y0 + tick_height],
        color="#263238", linewidth=1.1, zorder=15,
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


def add_epicenter(ax: plt.Axes, epicenter: gpd.GeoDataFrame) -> None:
    """Add the common earthquake epicenter marker."""
    epicenter.plot(
        ax=ax,
        marker="*",
        markersize=105,
        facecolor="#19A7AE",
        edgecolor="white",
        linewidth=0.9,
        zorder=13,
    )


def add_distance_rings(ax: plt.Axes, epicenter: gpd.GeoDataFrame) -> None:
    """Show the three decay-distance scales used in the scenario ensemble."""
    centre = epicenter.geometry.iloc[0]
    for distance_km in (10, 20, 40):
        ring = gpd.GeoSeries(
            [centre.buffer(distance_km * 1_000).boundary], crs=MAP_CRS
        )
        ring.plot(
            ax=ax,
            color="#50748A",
            linewidth=0.72,
            linestyle=(0, (3, 3)),
            alpha=0.65,
            zorder=7,
        )
        ax.text(
            centre.x,
            centre.y + distance_km * 1_000,
            f"{distance_km} km",
            ha="center",
            va="bottom",
            fontsize=6.7,
            color="#35586C",
            bbox={
                "boxstyle": "round,pad=0.08",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.75,
            },
            zorder=8,
        )


def positive_log_norm(values: pd.Series) -> LogNorm:
    """Create a robust logarithmic map scale while preserving zeros as no estimate."""
    numeric = pd.to_numeric(values, errors="coerce")
    positive = numeric.loc[numeric.gt(0)]
    if positive.empty:
        raise ValueError("Map variable contains no positive values")
    vmin = float(positive.quantile(0.01))
    vmax = float(positive.quantile(0.995))
    return LogNorm(vmin=max(vmin, np.finfo(float).tiny), vmax=max(vmax, vmin * 2), clip=True)


def plot_scenario_map(
    ax: plt.Axes,
    fig: plt.Figure,
    grid: gpd.GeoDataFrame,
    municipalities: gpd.GeoDataFrame,
    column: str,
    cmap_name: str,
    colorbar_label: str,
) -> None:
    """Plot a central scenario variable and add a compact horizontal colorbar."""
    values = pd.to_numeric(grid[column], errors="coerce")
    norm = positive_log_norm(values)
    visible = grid.assign(_plot_value=values.mask(values.le(0)))
    municipalities.plot(ax=ax, color="#F0F1F1", edgecolor="none", zorder=0)
    visible.plot(
        ax=ax,
        column="_plot_value",
        cmap=cmap_name,
        norm=norm,
        linewidth=0,
        missing_kwds={"color": "#E3E5E5"},
        rasterized=True,
        zorder=1,
    )
    municipalities.boundary.plot(
        ax=ax, color="#56636C", linewidth=0.34, alpha=0.78, zorder=6
    )
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=cmap_name)
    colorbar = fig.colorbar(
        mappable,
        ax=ax,
        orientation="horizontal",
        fraction=0.040,
        pad=0.035,
        extend="both",
    )
    colorbar.set_label(colorbar_label, fontsize=8.0, labelpad=3)
    colorbar.ax.tick_params(labelsize=7.0, length=2.5)


def draw_reported_evidence_panel(
    ax: plt.Axes,
    municipalities: gpd.GeoDataFrame,
    prefecture_snapshot: pd.Series,
    ward_snapshot: pd.Series,
    hikawa_count: int,
) -> None:
    """Map official evidence only at its disclosed geographic level."""
    municipalities.plot(
        ax=ax,
        color="#F3F4F4",
        edgecolor="#68737D",
        linewidth=0.36,
        zorder=1,
    )
    minami = municipalities.loc[municipalities["CITY"].eq(MINAMI_WARD_CODE)]
    hikawa = municipalities.loc[municipalities["CITY"].eq(HIKAWA_TOWN_CODE)]
    minami.plot(
        ax=ax, color="#3D7EA6", edgecolor="#174A68", linewidth=1.0, alpha=0.90, zorder=5
    )
    hikawa.plot(
        ax=ax, color="#F0A35E", edgecolor="#9B5622", linewidth=1.0, alpha=0.95, zorder=5
    )

    minami_point = minami.geometry.iloc[0].representative_point()
    hikawa_point = hikawa.geometry.iloc[0].representative_point()
    ward_full = int(ward_snapshot["Full Collapse Buildings"])
    ward_affected = int(ward_snapshot["Reported Affected Buildings"])
    ax.annotate(
        f"Minami Ward\n{ward_full} full collapse; {ward_affected} affected",
        xy=(minami_point.x, minami_point.y),
        xytext=(-70, 31),
        textcoords="offset points",
        ha="center",
        va="bottom",
        fontsize=7.2,
        color="#174A68",
        arrowprops={"arrowstyle": "-", "color": "#174A68", "linewidth": 0.75},
        bbox={
            "boxstyle": "round,pad=0.22",
            "facecolor": "white",
            "edgecolor": "#3D7EA6",
            "linewidth": 0.6,
            "alpha": 0.95,
        },
        zorder=12,
    )
    ax.annotate(
        f"Hikawa Town\n{hikawa_count} probable functional losses",
        xy=(hikawa_point.x, hikawa_point.y),
        xytext=(48, -25),
        textcoords="offset points",
        ha="left",
        va="top",
        fontsize=7.2,
        color="#7C4018",
        arrowprops={"arrowstyle": "-", "color": "#9B5622", "linewidth": 0.75},
        bbox={
            "boxstyle": "round,pad=0.22",
            "facecolor": "white",
            "edgecolor": "#F0A35E",
            "linewidth": 0.6,
            "alpha": 0.95,
        },
        zorder=12,
    )

    observation = pd.Timestamp(prefecture_snapshot["Observation Time"])
    if observation.tzinfo is not None:
        observation = observation.tz_convert("Asia/Tokyo")
    full = int(prefecture_snapshot["Full Collapse Buildings"])
    half = int(prefecture_snapshot["Half Collapse Buildings"])
    ax.text(
        0.035,
        0.965,
        f"Prefecture snapshot: {full} full collapse + {half} half collapse\n"
        f"{observation:%Y-%m-%d %H:%M JST}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=7.5,
        color="#303A40",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "white",
            "edgecolor": "#AAB2B7",
            "linewidth": 0.6,
            "alpha": 0.96,
        },
        zorder=12,
    )


def make_figure(
    grid: gpd.GeoDataFrame,
    housing: pd.DataFrame,
    evidence: pd.DataFrame,
    municipalities: gpd.GeoDataFrame,
) -> plt.Figure:
    """Build the three-panel reported/modelled exposure figure."""
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(16.2, 7.1), constrained_layout=False)

    prefecture_snapshot = latest_official_snapshot(housing)
    ward_snapshot = minami_snapshot(housing)
    hikawa_count = hikawa_probable_count(evidence)
    epicenter = gpd.GeoDataFrame(
        {"label": ["Epicenter"]},
        geometry=[Point(EPICENTER_LONGITUDE, EPICENTER_LATITUDE)],
        crs=GEOGRAPHIC_CRS,
    ).to_crs(MAP_CRS)

    draw_reported_evidence_panel(
        axes[0], municipalities, prefecture_snapshot, ward_snapshot, hikawa_count
    )
    plot_scenario_map(
        axes[1],
        fig,
        grid,
        municipalities,
        "Expected Functionally Lost Residences",
        "YlOrRd",
        "Expected functionally lost residences per grid (central)",
    )
    plot_scenario_map(
        axes[2],
        fig,
        grid,
        municipalities,
        "Estimated Affected Population Age 65+",
        "magma_r",
        "Estimated affected population age 65+ per grid (central)",
    )
    add_distance_rings(axes[1], epicenter)

    map_bounds = municipalities.total_bounds
    geographic_bounds = tuple(municipalities.to_crs(GEOGRAPHIC_CRS).total_bounds)
    x_padding = 0.025 * (map_bounds[2] - map_bounds[0])
    y_padding = 0.025 * (map_bounds[3] - map_bounds[1])
    for ax in axes:
        ax.set_xlim(map_bounds[0] - x_padding, map_bounds[2] + x_padding)
        ax.set_ylim(map_bounds[1] - y_padding, map_bounds[3] + y_padding)
        add_graticule(ax, geographic_bounds)
        add_epicenter(ax, epicenter)
        ax.set_aspect("equal")

    panel_labels = (
        ("a", "Reported residence-loss evidence"),
        ("b", "Expected structural residence loss"),
        ("c", "Associated older-person exposure"),
    )
    for ax, (letter, label) in zip(axes, panel_labels, strict=True):
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
            label,
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=9.4,
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
        Patch(
            facecolor="#3D7EA6",
            edgecolor="#174A68",
            label="Official ward-level report",
        ),
        Patch(
            facecolor="#F0A35E",
            edgecolor="#9B5622",
            label="Probable municipality-level evidence",
        ),
        Line2D(
            [0],
            [0],
            color="#50748A",
            linestyle=(0, (3, 3)),
            linewidth=0.9,
            label="Scenario distance scale",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.018),
        ncol=4,
        frameon=False,
        fontsize=7.8,
        handlelength=1.8,
        columnspacing=1.9,
    )
    fig.subplots_adjust(
        left=0.045,
        right=0.992,
        top=0.925,
        bottom=0.115,
        wspace=0.10,
    )
    return fig


def validate_figure_inputs(grid: gpd.GeoDataFrame) -> None:
    """Assert the central totals and pointwise scenario ordering used by the figure."""
    expected = pd.to_numeric(
        grid["Expected Functionally Lost Residences"], errors="coerce"
    )
    central_total = float(
        pd.to_numeric(
            grid["Structural Housing Loss Central Total Residences"], errors="coerce"
        ).dropna().iloc[0]
    )
    if not np.isclose(expected.sum(), central_total, atol=1e-8):
        raise ValueError("Expected residence-loss map does not sum to its central total")
    for central, lower, upper in (
        (
            "Expected Functionally Lost Residences",
            "Expected Functionally Lost Residences Lower Bound",
            "Expected Functionally Lost Residences Upper Bound",
        ),
        (
            "Estimated Affected Population Age 65+",
            "Estimated Affected Population Age 65+ Lower Bound",
            "Estimated Affected Population Age 65+ Upper Bound",
        ),
    ):
        c = pd.to_numeric(grid[central], errors="coerce")
        lo = pd.to_numeric(grid[lower], errors="coerce")
        hi = pd.to_numeric(grid[upper], errors="coerce")
        if not ((lo <= c) & (c <= hi)).all():
            raise ValueError(f"Pointwise scenario order failed for {central}")


def main() -> int:
    grid, housing, evidence, municipalities = load_inputs()
    validate_figure_inputs(grid)
    figure = make_figure(grid, housing, evidence, municipalities)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PATH, dpi=400, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
