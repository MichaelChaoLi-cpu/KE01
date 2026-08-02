#!/usr/bin/env python3
"""Create a two-panel QC map for the Kumamoto spatial foundation."""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import mercantile
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from shapely.geometry import box


ROOT = Path(__file__).resolve().parents[2]
BUILDINGS = ROOT / "data/processed/kumamoto_gsi_buildings_z15_preprocessed.parquet"
GROUPS = ROOT / "data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet"
SHELTERS = ROOT / "data/processed/kumamoto_designated_shelters_geospatial_preprocessed.parquet"
MEDICAL = ROOT / "data/processed/kumamoto_mlit_medical_institutions_preprocessed.parquet"
BOUNDARY = ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
OUTPUT = ROOT / "data/exp/spatial-foundation/kumamoto_spatial_foundation_qc.png"


def building_tile_density() -> gpd.GeoDataFrame:
    table = pq.read_table(
        BUILDINGS, columns=["Source Tile X", "Source Tile Y", "Source Zoom"]
    ).to_pandas()
    counts = (
        table.groupby(["Source Tile X", "Source Tile Y", "Source Zoom"])
        .size()
        .rename("Mapped Building Count")
        .reset_index()
    )
    geometry = []
    for x, y, z in counts[
        ["Source Tile X", "Source Tile Y", "Source Zoom"]
    ].itertuples(index=False, name=None):
        bounds = mercantile.bounds(int(x), int(y), int(z))
        geometry.append(box(bounds.west, bounds.south, bounds.east, bounds.north))
    return gpd.GeoDataFrame(counts, geometry=geometry, crs=6668)


def frame_map(ax, boundary: gpd.GeoDataFrame) -> None:
    min_x, min_y, max_x, max_y = boundary.total_bounds
    margin_x = (max_x - min_x) * 0.025
    margin_y = (max_y - min_y) * 0.025
    ax.set_xlim(min_x - margin_x, max_x + margin_x)
    ax.set_ylim(min_y - margin_y, max_y + margin_y)
    ax.set_xticks(np.arange(np.floor(min_x * 5) / 5, max_x + 0.2, 0.2))
    ax.set_yticks(np.arange(np.floor(min_y * 5) / 5, max_y + 0.2, 0.2))
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.grid(color="#9aa0a6", linewidth=0.45, alpha=0.55, linestyle="--")
    ax.set_axisbelow(True)
    ax.set_aspect(1 / np.cos(np.deg2rad((min_y + max_y) / 2)))
    for spine in ax.spines.values():
        spine.set_color("#1f2933")
        spine.set_linewidth(1.1)


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    boundary = gpd.read_file(BOUNDARY)[["geometry"]].to_crs(6668).dissolve()
    tiles = gpd.clip(building_tile_density(), boundary)
    groups = gpd.read_parquet(GROUPS).to_crs(6668)
    shelters = gpd.read_parquet(SHELTERS).to_crs(6668)
    medical = gpd.read_parquet(MEDICAL).to_crs(6668)
    disaster_hospitals = medical.loc[
        medical["Disaster Base Hospital Class"].isin([1, 2])
    ]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 12,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(15.2, 8.2), constrained_layout=True)

    tiles.plot(
        ax=axes[0],
        column="Mapped Building Count",
        cmap="viridis",
        norm=LogNorm(vmin=1, vmax=max(tiles["Mapped Building Count"].max(), 2)),
        linewidth=0,
        legend=True,
        legend_kwds={"label": "Mapped building polygons per z15 tile (log scale)", "shrink": 0.7},
    )
    boundary.boundary.plot(ax=axes[0], color="#111827", linewidth=0.8)
    axes[0].set_title("A. Kumamoto-wide mapped-building coverage")
    frame_map(axes[0], boundary)

    groups.plot(
        ax=axes[1],
        column="Population Age 65+ Share",
        cmap="YlOrRd",
        vmin=0,
        vmax=0.65,
        linewidth=0,
        legend=True,
        legend_kwds={"label": "Population age 65+ share", "shrink": 0.7},
        missing_kwds={"color": "#e5e7eb"},
    )
    shelters.plot(
        ax=axes[1], color="#2563eb", markersize=2.2, alpha=0.55, linewidth=0
    )
    disaster_hospitals.plot(
        ax=axes[1],
        color="#111827",
        marker="+",
        markersize=28,
        linewidth=0.9,
    )
    boundary.boundary.plot(ax=axes[1], color="#111827", linewidth=0.8)
    axes[1].legend(
        handles=[
            Line2D(
                [0], [0], marker="o", color="none", markerfacecolor="#2563eb",
                markeredgecolor="none", markersize=5, label="Designated shelter"
            ),
            Line2D(
                [0], [0], marker="+", color="#111827", linestyle="none",
                markersize=8, label="Disaster base hospital"
            ),
        ],
        loc="lower left",
        frameon=True,
        fontsize=8,
    )
    axes[1].set_title("B. Older-population geography and support locations")
    frame_map(axes[1], boundary)

    fig.suptitle(
        "Kumamoto spatial foundation — quality-control map",
        fontsize=16,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.005,
        "QC only — building polygons are not damage labels; facility locations do not confirm post-earthquake operation or cooling capacity.",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#374151",
    )
    fig.savefig(OUTPUT, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {OUTPUT.relative_to(ROOT)}")
    print(
        f"Mapped buildings: {len(pq.read_table(BUILDINGS, columns=['Building ID'])):,}; "
        f"shelters: {len(shelters):,}; disaster base hospitals: {len(disaster_hospitals):,}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
