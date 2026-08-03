"""Generate Figure 2: Minami Ward shelter and cooling risk screening."""

from __future__ import annotations

from pathlib import Path
from zoneinfo import ZoneInfo

import geopandas as gpd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MaxNLocator


ROOT = Path(__file__).resolve().parents[2]
BOUNDARY_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
POPULATION_PATH = (
    ROOT / "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet"
)
SHELTER_PATH = (
    ROOT / "data/processed/kumamoto_designated_shelters_geospatial_preprocessed.parquet"
)
EVIDENCE_PATH = (
    ROOT / "data/processed/kumamoto_damage_evidence_registry_preprocessed.parquet"
)
DISRUPTION_PATH = (
    ROOT / "data/processed/kumamoto_service_disruption_snapshots_preprocessed.parquet"
)
OUTPUT_DIR = ROOT / "data/results/figures"
OUTPUT_PNG = OUTPUT_DIR / "Figure_02_minami_ward_shelter_cooling_risk_screening.png"
OUTPUT_PDF = OUTPUT_DIR / "Figure_02_minami_ward_shelter_cooling_risk_screening.pdf"


def _longitude(value: float, _: int) -> str:
    return f"{value:.2f}°E"


def _latitude(value: float, _: int) -> str:
    return f"{value:.2f}°N"


def _load_spatial_layers() -> tuple[gpd.GeoDataFrame, ...]:
    boundaries = gpd.read_file(BOUNDARY_PATH).to_crs(6668)
    minami = boundaries.loc[boundaries["CITY_NAME"].eq("熊本市南区")].copy()
    if minami.empty:
        raise ValueError("Minami Ward boundary was not found.")

    minami_outline = gpd.GeoDataFrame(
        {"name": ["Minami Ward"]},
        geometry=[minami.geometry.union_all()],
        crs=minami.crs,
    )
    damage_context = minami.loc[
        minami["S_NAME"].str.startswith(("富合町", "城南町"), na=False)
    ].copy()

    population = gpd.read_parquet(POPULATION_PATH).to_crs(minami.crs)
    population = gpd.clip(population, minami_outline)
    population = population.loc[population.geometry.notna() & ~population.geometry.is_empty]

    shelters = gpd.read_parquet(SHELTER_PATH).to_crs(minami.crs)
    shelters = shelters.loc[shelters["Address"].str.contains("熊本市南区", na=False)].copy()

    evidence = pd.read_parquet(EVIDENCE_PATH)
    closed = evidence.loc[
        evidence["Asset Type"].eq("shelter")
        & evidence["Latitude"].notna()
        & evidence["Longitude"].notna()
    ].copy()
    closed = gpd.GeoDataFrame(
        closed,
        geometry=gpd.points_from_xy(closed["Longitude"], closed["Latitude"]),
        crs=6668,
    )
    return minami_outline, damage_context, population, shelters, closed


def _add_scale_and_north_arrow(ax: plt.Axes, bounds: np.ndarray) -> None:
    minx, miny, maxx, maxy = bounds
    mean_lat = (miny + maxy) / 2
    km_per_lon_degree = 111.32 * np.cos(np.deg2rad(mean_lat))
    five_km_lon = 5 / km_per_lon_degree
    start_x = minx + 0.055 * (maxx - minx)
    start_y = miny + 0.205 * (maxy - miny)
    ax.plot(
        [start_x, start_x + five_km_lon],
        [start_y, start_y],
        color="#202020",
        linewidth=3,
        solid_capstyle="butt",
        zorder=20,
    )
    ax.plot(
        [start_x, start_x, start_x + five_km_lon, start_x + five_km_lon],
        [start_y - 0.0012, start_y + 0.0012, start_y - 0.0012, start_y + 0.0012],
        color="#202020",
        linewidth=1,
        zorder=20,
    )
    ax.text(
        start_x + five_km_lon / 2,
        start_y + 0.0025,
        "5 km",
        ha="center",
        va="bottom",
        fontsize=8,
        color="#202020",
    )
    ax.annotate(
        "N",
        xy=(0.955, 0.90),
        xytext=(0.955, 0.80),
        xycoords="axes fraction",
        textcoords="axes fraction",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        arrowprops={"arrowstyle": "-|>", "color": "#202020", "lw": 1.2},
    )


def _plot_map(ax: plt.Axes) -> None:
    minami, damage_context, population, shelters, closed = _load_spatial_layers()
    bounds = minami.total_bounds

    older = pd.to_numeric(population["Population Age 65+"], errors="coerce")
    vmax = float(np.nanpercentile(older, 95))
    norm = Normalize(vmin=0, vmax=vmax)
    cmap = plt.get_cmap("YlOrRd")

    population.plot(
        ax=ax,
        column="Population Age 65+",
        cmap=cmap,
        norm=norm,
        linewidth=0,
        zorder=1,
    )
    minami.boundary.plot(ax=ax, color="#222222", linewidth=1.0, zorder=8)
    damage_context.plot(
        ax=ax,
        facecolor="none",
        edgecolor="#8c2d04",
        linewidth=1.15,
        hatch="////",
        zorder=9,
    )
    shelters.plot(
        ax=ax,
        marker="o",
        facecolor="#ffffff",
        edgecolor="#2471a3",
        linewidth=0.65,
        markersize=18,
        alpha=0.9,
        zorder=10,
    )
    closed.plot(
        ax=ax,
        marker="X",
        facecolor="#7f0000",
        edgecolor="#ffffff",
        linewidth=0.7,
        markersize=82,
        zorder=12,
    )

    label_offsets = {
        "Kumanosho Elementary School shelter": (0.006, 0.008, "Kumanosho ES\nwater + AC failure"),
        "Miyuki Elementary School shelter": (0.005, 0.006, "Miyuki ES\nwater outage"),
    }
    for _, row in closed.iterrows():
        place = row["Place Description"]
        if place in label_offsets:
            dx, dy, label = label_offsets[place]
        else:
            if "Kumanosho" in str(place):
                dx, dy, label = 0.006, 0.008, "Kumanosho ES\nwater + AC failure"
            else:
                dx, dy, label = 0.005, 0.006, "Miyuki ES\nwater outage"
        ax.annotate(
            label,
            xy=(row.geometry.x, row.geometry.y),
            xytext=(row.geometry.x + dx, row.geometry.y + dy),
            fontsize=8.4,
            ha="left",
            va="center",
            color="#4a0000",
            arrowprops={"arrowstyle": "-", "color": "#7f0000", "lw": 0.8},
            bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#bb7777", "alpha": 0.98},
            zorder=15,
        )

    legend_handles = [
        Line2D(
            [0], [0], marker="o", color="none", markerfacecolor="white",
            markeredgecolor="#2471a3", markersize=6, label="Designated shelter (operation unverified)"
        ),
        Line2D(
            [0], [0], marker="X", color="none", markerfacecolor="#7f0000",
            markeredgecolor="white", markersize=8, label="Confirmed unavailable shelter"
        ),
        Patch(facecolor="white", edgecolor="#8c2d04", hatch="////", label="Tomiai / Jonan context"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left",
        bbox_to_anchor=(0.015, 0.015),
        frameon=True,
        framealpha=0.98,
        fontsize=8.0,
        borderpad=0.6,
    )

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = ax.figure.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.040, pad=0.075)
    cbar.set_label("Residents age 65+ per disclosure group (color capped at 95th percentile)", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    xpad = 0.025 * (bounds[2] - bounds[0])
    ypad = 0.025 * (bounds[3] - bounds[1])
    ax.set_xlim(bounds[0] - xpad, bounds[2] + xpad)
    ax.set_ylim(bounds[1] - ypad, bounds[3] + ypad)
    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.yaxis.set_major_locator(MaxNLocator(5))
    ax.xaxis.set_major_formatter(FuncFormatter(_longitude))
    ax.yaxis.set_major_formatter(FuncFormatter(_latitude))
    ax.tick_params(labelsize=8.5)
    ax.grid(True, color="#9e9e9e", linewidth=0.45, linestyle="--", alpha=0.65, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_color("#333333")
    ax.set_xlabel("Longitude", fontsize=9.5)
    ax.set_ylabel("Latitude", fontsize=9.5)
    ax.set_title("a  Spatial screening", loc="left", fontsize=11.5, fontweight="bold")
    _add_scale_and_north_arrow(ax, bounds)


def _plot_operational_series(ax: plt.Axes) -> None:
    disruption = pd.read_parquet(DISRUPTION_PATH)
    times = pd.to_datetime(disruption["Observation Time"], utc=True).dt.tz_convert("Asia/Tokyo")
    disruption = disruption.assign(_time=times)

    evacuees = disruption.loc[
        disruption["Disruption Type"].eq("shelter_occupancy")
        & disruption["Municipality"].eq("Kumamoto City")
        & disruption["Observed Evacuee Count"].notna()
    ].sort_values("_time")
    minami_latest = disruption.loc[
        disruption["Disruption Type"].eq("shelter_occupancy")
        & disruption["Municipality"].eq("Kumamoto City, Minami Ward")
    ].sort_values("_time")
    water = disruption.loc[
        disruption["Disruption Type"].eq("water_outage")
        & disruption["Observed Water Outage Households"].notna()
    ].sort_values("_time")

    color_evac = "#2471a3"
    color_water = "#a93226"
    ax.plot(
        evacuees["_time"],
        evacuees["Observed Evacuee Count"].astype(float),
        color=color_evac,
        marker="o",
        markersize=4.5,
        linewidth=1.8,
        label="Kumamoto City public-shelter occupants",
        zorder=4,
    )
    if not minami_latest.empty:
        row = minami_latest.iloc[-1]
        ax.scatter(
            row["_time"],
            float(row["Observed Evacuee Count"]),
            marker="D",
            s=38,
            color="#154360",
            edgecolor="white",
            linewidth=0.6,
            zorder=6,
            label="Minami Ward occupants (latest)",
        )
        ax.annotate(
            f"Minami Ward: {int(row['Observed Evacuee Count']):,}",
            xy=(row["_time"], float(row["Observed Evacuee Count"])),
            xytext=(-102, -34),
            textcoords="offset points",
            fontsize=8.4,
            color="#154360",
            arrowprops={"arrowstyle": "-", "color": "#154360", "lw": 0.8},
            bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
        )

    peak = evacuees.loc[evacuees["Observed Evacuee Count"].astype(float).idxmax()]
    ax.annotate(
        f"Peak: {int(peak['Observed Evacuee Count']):,}",
        xy=(peak["_time"], float(peak["Observed Evacuee Count"])),
        xytext=(18, -48),
        textcoords="offset points",
        fontsize=8.4,
        color=color_evac,
        arrowprops={"arrowstyle": "-", "color": color_evac, "lw": 0.8},
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.9},
    )

    ax2 = ax.twinx()
    ax2.plot(
        water["_time"],
        water["Observed Water Outage Households"].astype(float),
        color=color_water,
        marker="s",
        markersize=5,
        linewidth=1.8,
        linestyle="--",
        label="Jonan water-outage households",
        zorder=5,
    )
    for _, row in water.iterrows():
        ax2.annotate(
            f"{int(row['Observed Water Outage Households']):,}",
            xy=(row["_time"], float(row["Observed Water Outage Households"])),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=8.2,
            color=color_water,
            bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.85},
        )

    ax.set_ylim(0, 2850)
    ax2.set_ylim(0, 10200)
    ax.set_ylabel("Observed public-shelter occupants", color=color_evac, fontsize=9.5)
    ax2.set_ylabel("Observed water-outage households", color=color_water, fontsize=9.5)
    ax.tick_params(axis="y", labelcolor=color_evac, labelsize=8.5)
    ax2.tick_params(axis="y", labelcolor=color_water, labelsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d", tz=ZoneInfo("Asia/Tokyo")))
    ax.tick_params(axis="x", labelsize=8.5, rotation=0)
    ax.grid(True, axis="both", color="#bdbdbd", linewidth=0.5, linestyle="--", alpha=0.65)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.9)
        spine.set_color("#333333")
    ax2.spines["right"].set_linewidth(0.9)
    ax2.spines["right"].set_color("#333333")
    ax.set_title("b  Operational observations (JST)", loc="left", fontsize=11.5, fontweight="bold")

    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper right",
        frameon=True,
        framealpha=0.95,
        fontsize=8.0,
        borderpad=0.6,
    )
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlecolor": "#202020",
            "axes.labelcolor": "#303030",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(13.2, 6.4),
        gridspec_kw={"width_ratios": [1.12, 0.88]},
    )
    _plot_map(axes[0])
    _plot_operational_series(axes[1])
    fig.subplots_adjust(left=0.065, right=0.935, top=0.92, bottom=0.10, wspace=0.26)
    fig.savefig(OUTPUT_PNG, dpi=400, bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT_PDF, dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"saved: {OUTPUT_PNG}")
    print(f"saved: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
