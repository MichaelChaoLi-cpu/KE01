#!/usr/bin/env python3
"""Build strict- and relaxed-QA historical MODIS heat grids for Kumamoto.

Terra and Aqua product means are given equal weight so that unequal cloud
availability does not allow one satellite to dominate the climatological mean.
The coverage-optimized field uses the strict-QA mean whenever available and the
relaxed-QA mean only where every strict-QA observation is missing. Cloud-
affected observations remain missing; no spatial interpolation is performed.
"""

from __future__ import annotations

import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from pyhdf.SD import SD, SDC
from shapely import box, contains_xy


ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "data/raw/weather/modis_lst_8day_2021_2025"
BOUNDARY_PATH = (
    ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PATH = (
    ROOT
    / "data/processed/kumamoto_modis_historical_heat_spatial_grid_preprocessed.parquet"
)

MODIS_SINUSOIDAL = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext"
GLOBAL_X_MIN = -20015109.354
GLOBAL_Y_MAX = 10007554.677
TILE_SIZE_M = 1111950.519666
PIXEL_SIZE_M = TILE_SIZE_M / 1200
TILE_DIM = 1200
PRODUCTS = ("MOD11A2", "MYD11A2")
PERIODS = ("Day", "Night")
FILENAME_RE = re.compile(r"\.h(?P<h>\d{2})v(?P<v>\d{2})\.")


def strict_qc_mask(qc: np.ndarray) -> np.ndarray:
    mandatory = qc & 0b11
    data_quality = (qc >> 2) & 0b11
    lst_error = (qc >> 6) & 0b11
    return (mandatory == 0) & (data_quality == 0) & (lst_error == 0)


def relaxed_qc_mask(qc: np.ndarray) -> np.ndarray:
    mandatory = qc & 0b11
    data_quality = (qc >> 2) & 0b11
    lst_error = (qc >> 6) & 0b11
    return (mandatory <= 1) & (data_quality == 0) & (lst_error <= 1)


def tile_window(h: int, v: int, prefecture_geometry):
    tile_x_min = GLOBAL_X_MIN + h * TILE_SIZE_M
    tile_y_max = GLOBAL_Y_MAX - v * TILE_SIZE_M
    min_x, min_y, max_x, max_y = prefecture_geometry.bounds
    col0 = max(0, int(np.floor((min_x - tile_x_min) / PIXEL_SIZE_M)) - 1)
    col1 = min(TILE_DIM, int(np.ceil((max_x - tile_x_min) / PIXEL_SIZE_M)) + 1)
    row0 = max(0, int(np.floor((tile_y_max - max_y) / PIXEL_SIZE_M)) - 1)
    row1 = min(TILE_DIM, int(np.ceil((tile_y_max - min_y) / PIXEL_SIZE_M)) + 1)
    if row0 >= row1 or col0 >= col1:
        return None

    xs = tile_x_min + (np.arange(col0, col1) + 0.5) * PIXEL_SIZE_M
    ys = tile_y_max - (np.arange(row0, row1) + 0.5) * PIXEL_SIZE_M
    xx, yy = np.meshgrid(xs, ys)
    inside = contains_xy(prefecture_geometry, xx, yy)
    if not inside.any():
        return None
    return {
        "row0": row0,
        "row1": row1,
        "col0": col0,
        "col1": col1,
        "inside": inside,
        "xx": xx,
        "yy": yy,
    }


def empty_accumulator(shape: tuple[int, int]) -> dict[str, np.ndarray]:
    return {
        "sum": np.zeros(shape, dtype=np.float64),
        "sum_of_squares": np.zeros(shape, dtype=np.float64),
        "count": np.zeros(shape, dtype=np.uint16),
    }


def safe_mean(total: np.ndarray, count: np.ndarray) -> np.ndarray:
    return np.divide(
        total,
        count,
        out=np.full(total.shape, np.nan, dtype=np.float64),
        where=count > 0,
    )


def main() -> int:
    files = sorted(RAW_ROOT.glob("*/*.hdf"))
    if len(files) != 80:
        raise ValueError(f"Expected 80 MODIS files, found {len(files)}")

    boundary = gpd.read_file(BOUNDARY_PATH, columns=["geometry"]).to_crs(
        MODIS_SINUSOIDAL
    )
    prefecture_geometry = boundary.geometry.union_all()
    states: dict[tuple[int, int], dict[str, object]] = {}

    for path in files:
        match = FILENAME_RE.search(path.name)
        if not match:
            raise ValueError(f"Cannot parse MODIS tile: {path.name}")
        h = int(match.group("h"))
        v = int(match.group("v"))
        key = (h, v)
        if key not in states:
            window = tile_window(h, v, prefecture_geometry)
            if window is None:
                continue
            shape = window["inside"].shape
            window["accumulators"] = {
                (quality, product, period): empty_accumulator(shape)
                for quality in ("Strict", "Relaxed")
                for product in PRODUCTS
                for period in PERIODS
            }
            states[key] = window

        state = states[key]
        row0 = state["row0"]
        row1 = state["row1"]
        col0 = state["col0"]
        col1 = state["col1"]
        inside = state["inside"]
        product = path.parent.name
        hdf = SD(str(path), SDC.READ)
        try:
            for period in PERIODS:
                raw = np.asarray(
                    hdf.select(f"LST_{period}_1km")[row0:row1, col0:col1],
                    dtype=np.uint16,
                )
                qc = np.asarray(
                    hdf.select(f"QC_{period}")[row0:row1, col0:col1],
                    dtype=np.uint8,
                )
                values_c = raw.astype(np.float64) * 0.02 - 273.15
                raw_valid = inside & (raw >= 7500) & (raw != 0)
                quality_masks = {
                    "Strict": raw_valid & strict_qc_mask(qc),
                    "Relaxed": raw_valid & relaxed_qc_mask(qc),
                }
                for quality, valid in quality_masks.items():
                    accumulator = state["accumulators"][(quality, product, period)]
                    accumulator["sum"][valid] += values_c[valid]
                    accumulator["sum_of_squares"][valid] += values_c[valid] ** 2
                    accumulator["count"][valid] += 1
        finally:
            hdf.end()

    frames: list[gpd.GeoDataFrame] = []
    for (h, v), state in sorted(states.items()):
        inside = state["inside"]
        rows, cols = np.where(inside)
        global_rows = rows + state["row0"]
        global_cols = cols + state["col0"]
        xs = state["xx"][inside]
        ys = state["yy"][inside]

        data: dict[str, object] = {
            "MODIS Pixel ID": [
                f"h{h:02d}v{v:02d}r{row:04d}c{col:04d}"
                for row, col in zip(global_rows, global_cols, strict=True)
            ],
            "MODIS Tile": f"h{h:02d}v{v:02d}",
            "MODIS Row": global_rows,
            "MODIS Column": global_cols,
        }

        for period in PERIODS:
            label = "Daytime" if period == "Day" else "Nighttime"
            summaries: dict[str, dict[str, np.ndarray]] = {}
            for quality in ("Strict", "Relaxed"):
                product_means = []
                total_sum = np.zeros(inside.shape, dtype=np.float64)
                total_squares = np.zeros(inside.shape, dtype=np.float64)
                total_count = np.zeros(inside.shape, dtype=np.uint16)
                for product in PRODUCTS:
                    accumulator = state["accumulators"][(quality, product, period)]
                    product_means.append(
                        safe_mean(accumulator["sum"], accumulator["count"])
                    )
                    total_sum += accumulator["sum"]
                    total_squares += accumulator["sum_of_squares"]
                    total_count += accumulator["count"]

                stacked_means = np.stack(product_means)
                available_products = np.sum(~np.isnan(stacked_means), axis=0)
                combined_mean = np.divide(
                    np.nansum(stacked_means, axis=0),
                    available_products,
                    out=np.full(inside.shape, np.nan, dtype=np.float64),
                    where=available_products > 0,
                )
                numerator = total_squares - np.divide(
                    total_sum**2,
                    total_count,
                    out=np.zeros(inside.shape, dtype=np.float64),
                    where=total_count > 0,
                )
                standard_deviation = np.sqrt(
                    np.divide(
                        np.maximum(numerator, 0),
                        total_count - 1,
                        out=np.full(inside.shape, np.nan, dtype=np.float64),
                        where=total_count > 1,
                    )
                )
                summaries[quality] = {
                    "mean": combined_mean,
                    "count": total_count,
                    "sd": standard_deviation,
                    "products": available_products,
                }

                prefix = "" if quality == "Strict" else "Relaxed-QA "
                data[f"{prefix}Historical {label} Land Surface Temperature C"] = (
                    combined_mean[inside]
                )
                data[f"{prefix}MODIS {label} Valid Observation Count"] = (
                    total_count[inside]
                )
                data[f"{prefix}Historical {label} Land Surface Temperature SD C"] = (
                    standard_deviation[inside]
                )
                data[f"{prefix}MODIS {label} Available Product Count"] = (
                    available_products[inside]
                )

            strict = summaries["Strict"]
            relaxed = summaries["Relaxed"]
            strict_primary = (
                ~np.isnan(strict["mean"])
                & (strict["count"] >= 5)
                & (strict["products"] == 2)
            )
            strict_limited = ~np.isnan(strict["mean"])
            relaxed_only = np.isnan(strict["mean"]) & ~np.isnan(relaxed["mean"])
            coverage_mean = np.where(
                ~np.isnan(strict["mean"]), strict["mean"], relaxed["mean"]
            )
            support = np.full(inside.shape, "missing", dtype=object)
            support[relaxed_only] = "relaxed_only"
            support[strict_limited] = "strict_limited"
            support[strict_primary] = "strict_primary"
            data[f"Coverage-Optimized Historical {label} Land Surface Temperature C"] = (
                coverage_mean[inside]
            )
            data[f"Historical {label} LST Support Tier"] = support[inside]

        half = PIXEL_SIZE_M / 2
        geometries = [
            box(x - half, y - half, x + half, y + half)
            for x, y in zip(xs, ys, strict=True)
        ]
        frame = gpd.GeoDataFrame(data, geometry=geometries, crs=MODIS_SINUSOIDAL)
        frames.append(frame)

    grid = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=MODIS_SINUSOIDAL)
    grid = grid.to_crs("EPSG:4326")
    centroids = grid.to_crs("EPSG:6670").geometry.centroid.to_crs("EPSG:4326")
    grid.insert(4, "Latitude", centroids.y)
    grid.insert(5, "Longitude", centroids.x)
    for column in grid.columns:
        if "Temperature C" in column or "Temperature SD C" in column:
            grid[column] = grid[column].round(3)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    grid.to_parquet(OUTPUT_PATH, index=False)

    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Pixels: {len(grid):,}; tiles: {grid['MODIS Tile'].nunique()}")
    for label in ("Daytime", "Nighttime"):
        count = grid[f"MODIS {label} Valid Observation Count"]
        available = grid[f"Historical {label} Land Surface Temperature C"].notna()
        coverage = grid[
            f"Coverage-Optimized Historical {label} Land Surface Temperature C"
        ].notna()
        support = grid[f"Historical {label} LST Support Tier"].value_counts()
        print(
            f"{label}: {available.sum():,}/{len(grid):,} pixels with strict-QC data; "
            f"{coverage.sum():,}/{len(grid):,} with strict-first relaxed-QA fallback; "
            f"median strict observations={count[available].median():.0f}; "
            f"support tiers={support.to_dict()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
