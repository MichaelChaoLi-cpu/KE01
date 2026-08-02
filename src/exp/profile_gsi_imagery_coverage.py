#!/usr/bin/env python3
"""Profile and map GSI post-earthquake aerial-photo camera locations."""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from pyproj import Transformer
from shapely.geometry import LineString


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = (
    ROOT / "data/raw/imagery/gsi_2026_kumamoto/catalog/photo_catalog.csv"
)
BOUNDARY_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_DIR = ROOT / "data/exp/gsi-imagery"
FIGURE_PATH = OUTPUT_DIR / "gsi_event_imagery_coverage.png"
TABLE_PATH = OUTPUT_DIR / "coverage_by_municipality.csv"
MAP_CRS = "EPSG:6670"
FOCAL_AREAS = {"202": "Yatsushiro", "213": "Uki", "468": "Hikawa"}


def values(lower: float, upper: float, step: float) -> list[float]:
    start = math.ceil(lower / step) * step
    stop = math.floor(upper / step) * step
    return list(np.arange(start, stop + step / 2, step))


def add_graticule(
    ax: plt.Axes, geographic_bounds: tuple[float, float, float, float]
) -> None:
    lon_min, lat_min, lon_max, lat_max = geographic_bounds
    longitudes = values(lon_min, lon_max, 0.25)
    latitudes = values(lat_min, lat_max, 0.25)
    lines = [
        LineString([(lon, lat_min - 0.25), (lon, lat_max + 0.25)])
        for lon in longitudes
    ] + [
        LineString([(lon_min - 0.25, lat), (lon_max + 0.25, lat)])
        for lat in latitudes
    ]
    gpd.GeoSeries(lines, crs=4326).to_crs(MAP_CRS).plot(
        ax=ax,
        color="#81909A",
        linewidth=0.45,
        linestyle=(0, (2.5, 3.5)),
        alpha=0.5,
        zorder=1,
    )
    transformer = Transformer.from_crs(4326, MAP_CRS, always_xy=True)
    middle_lon = (lon_min + lon_max) / 2
    middle_lat = (lat_min + lat_max) / 2
    for longitude in longitudes:
        x, _ = transformer.transform(longitude, middle_lat)
        ax.text(
            x,
            -0.012,
            f"{longitude:.2f}°E",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=7,
            color="#46515A",
            clip_on=False,
        )
    for latitude in latitudes:
        _, y = transformer.transform(middle_lon, latitude)
        ax.text(
            -0.01,
            y,
            f"{latitude:.2f}°N",
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="center",
            fontsize=7,
            color="#46515A",
            clip_on=False,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("#303A40")
        spine.set_linewidth(0.85)


def main() -> int:
    photos = pd.read_csv(CATALOG_PATH, dtype={"photo_number": "string"})
    photos["photo_type"] = np.where(
        photos["category"].str.contains("斜め写真"), "Oblique", "Vertical"
    )
    points = gpd.GeoDataFrame(
        photos,
        geometry=gpd.points_from_xy(photos["longitude"], photos["latitude"]),
        crs=4326,
    ).to_crs(MAP_CRS)
    small_areas = gpd.read_file(
        BOUNDARY_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(MAP_CRS)
    municipalities = small_areas.dissolve(
        by=["CITY", "CITY_NAME"], as_index=False
    )
    joined = gpd.sjoin(
        points, municipalities[["CITY", "CITY_NAME", "geometry"]],
        how="left", predicate="within"
    )

    counts = (
        joined.dropna(subset=["CITY"])
        .groupby(["CITY", "CITY_NAME", "photo_type"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for photo_type in ["Vertical", "Oblique"]:
        if photo_type not in counts:
            counts[photo_type] = 0
    counts["Total"] = counts["Vertical"] + counts["Oblique"]
    counts = counts.sort_values(["Total", "CITY"], ascending=[False, True])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    counts.to_csv(TABLE_PATH, index=False)

    fig, ax = plt.subplots(figsize=(9.2, 9.2))
    municipality_bounds = municipalities.total_bounds
    x_pad = 0.025 * (municipality_bounds[2] - municipality_bounds[0])
    y_pad = 0.025 * (municipality_bounds[3] - municipality_bounds[1])
    ax.set_xlim(municipality_bounds[0] - x_pad, municipality_bounds[2] + x_pad)
    ax.set_ylim(municipality_bounds[1] - y_pad, municipality_bounds[3] + y_pad)
    geographic_bounds = tuple(municipalities.to_crs(4326).total_bounds)
    add_graticule(ax, geographic_bounds)

    municipalities.boundary.plot(
        ax=ax, color="#A4ACB3", linewidth=0.42, zorder=2
    )
    vertical = points.loc[points["photo_type"] == "Vertical"]
    oblique = points.loc[points["photo_type"] == "Oblique"]
    vertical.plot(
        ax=ax,
        color="#2166AC",
        markersize=4.2,
        alpha=0.42,
        linewidth=0,
        zorder=3,
    )
    oblique.plot(
        ax=ax,
        color="#D95F0E",
        marker="^",
        markersize=7,
        alpha=0.55,
        linewidth=0,
        zorder=4,
    )

    focal = municipalities.loc[municipalities["CITY"].isin(FOCAL_AREAS)].copy()
    focal.boundary.plot(ax=ax, color="#102A43", linewidth=1.6, zorder=5)
    offsets = {"202": (-20, -12), "213": (14, 13), "468": (22, -1)}
    for row in focal.itertuples(index=False):
        point = row.geometry.representative_point()
        ax.annotate(
            FOCAL_AREAS[row.CITY],
            xy=(point.x, point.y),
            xytext=offsets[row.CITY],
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=8,
            color="#102A43",
            arrowprops={"arrowstyle": "-", "color": "#102A43", "linewidth": 0.7},
            bbox={
                "boxstyle": "round,pad=0.16",
                "facecolor": "white",
                "edgecolor": "#102A43",
                "linewidth": 0.6,
                "alpha": 0.92,
            },
            zorder=6,
        )

    legend = [
        Line2D(
            [0], [0], marker="o", linestyle="", color="#2166AC", markersize=6,
            label=f"Vertical camera locations (n={len(vertical):,})"
        ),
        Line2D(
            [0], [0], marker="^", linestyle="", color="#D95F0E", markersize=7,
            label=f"Oblique camera locations (n={len(oblique):,})"
        ),
        Line2D(
            [0], [0], color="#102A43", linewidth=1.8,
            label="Focal municipality boundary"
        ),
    ]
    ax.legend(
        handles=legend,
        loc="upper right",
        frameon=True,
        framealpha=0.95,
        fontsize=8,
    )
    ax.set_aspect("equal")
    ax.set_title(
        "GSI Post-Earthquake Aerial Photography Camera Locations, 2026",
        loc="left",
        fontsize=14,
        pad=12,
    )
    ax.text(
        0.01,
        0.012,
        f"Camera centres fall within {counts['CITY'].nunique()} of {municipalities['CITY'].nunique()} "
        "municipality units; image footprints may extend beyond these points.",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=8,
        color="#46515A",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.88, "pad": 2},
        zorder=7,
    )
    fig.text(
        0.08,
        0.02,
        "Source: Geospatial Information Authority of Japan. Camera locations are not image footprints. "
        "The rapid orthophoto is available only for the Yatsushiro district.",
        ha="left",
        va="bottom",
        fontsize=8,
        color="#46515A",
    )
    fig.subplots_adjust(left=0.09, right=0.98, top=0.93, bottom=0.075)
    fig.savefig(FIGURE_PATH, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(fig)

    print(f"Saved {FIGURE_PATH.relative_to(ROOT)}")
    print(f"Saved {TABLE_PATH.relative_to(ROOT)}")
    print(f"Municipality units with camera centres: {counts['CITY'].nunique()} / {municipalities['CITY'].nunique()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
