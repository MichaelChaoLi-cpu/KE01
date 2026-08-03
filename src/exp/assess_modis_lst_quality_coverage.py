#!/usr/bin/env python3
"""Assess MODIS LST quality coverage inside Kumamoto Prefecture.

The script reads Terra and Aqua MOD11A2-family HDF4 granules, clips pixel
centres to the prefecture boundary, decodes the official QC bit fields, and
reports strict and relaxed usable coverage. It does not interpolate or impute.
"""
from __future__ import annotations

import csv
from datetime import datetime
import json
from pathlib import Path
import re

import geopandas as gpd
import numpy as np
from pyhdf.SD import SD, SDC
from shapely import contains_xy


ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "data/raw/weather/modis_lst_8day_2021_2025"
BOUNDARY_PATH = ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
OUTPUT_DIR = ROOT / "data/exp/modis-heat-history"
COMPOSITE_PATH = OUTPUT_DIR / "qc_coverage_by_composite.csv"
SUMMARY_PATH = OUTPUT_DIR / "qc_coverage_summary.json"

MODIS_SINUSOIDAL = "+proj=sinu +R=6371007.181 +nadgrids=@null +wktext"
GLOBAL_X_MIN = -20015109.354
GLOBAL_Y_MAX = 10007554.677
TILE_SIZE_M = 1111950.519666
PIXEL_SIZE_M = TILE_SIZE_M / 1200
TILE_DIM = 1200
FILENAME_RE = re.compile(r"\.A(?P<year>\d{4})(?P<doy>\d{3})\.h(?P<h>\d{2})v(?P<v>\d{2})\.")


def load_prefecture_geometry():
    boundary = gpd.read_file(BOUNDARY_PATH, columns=["geometry"]).to_crs(MODIS_SINUSOIDAL)
    return boundary.geometry.union_all()


def tile_window_and_mask(h: int, v: int, prefecture_geometry):
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
    return row0, row1, col0, col1, inside


def qc_masks(qc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mandatory = qc & 0b11
    data_quality = (qc >> 2) & 0b11
    lst_error = (qc >> 6) & 0b11
    strict = (mandatory == 0) & (data_quality == 0) & (lst_error == 0)
    relaxed = (mandatory <= 1) & (data_quality == 0) & (lst_error <= 1)
    return strict, relaxed


def main() -> int:
    prefecture_geometry = load_prefecture_geometry()
    tile_cache: dict[tuple[int, int], tuple[int, int, int, int, np.ndarray] | None] = {}
    accumulators: dict[tuple[str, str, str], dict[str, object]] = {}

    files = sorted(RAW_ROOT.glob("*/*.hdf"))
    if not files:
        raise FileNotFoundError(f"No HDF files found under {RAW_ROOT}")

    for path in files:
        match = FILENAME_RE.search(path.name)
        if not match:
            raise ValueError(f"Cannot parse MODIS granule name: {path.name}")
        year = int(match.group("year"))
        doy = int(match.group("doy"))
        h = int(match.group("h"))
        v = int(match.group("v"))
        composite_start = datetime.strptime(f"{year}{doy:03d}", "%Y%j").date().isoformat()
        product = path.parent.name

        if (h, v) not in tile_cache:
            tile_cache[(h, v)] = tile_window_and_mask(h, v, prefecture_geometry)
        window = tile_cache[(h, v)]
        if window is None:
            continue
        row0, row1, col0, col1, inside = window

        hdf = SD(str(path), SDC.READ)
        try:
            for period in ("Day", "Night"):
                raw = np.asarray(
                    hdf.select(f"LST_{period}_1km")[row0:row1, col0:col1],
                    dtype=np.uint16,
                )
                qc = np.asarray(
                    hdf.select(f"QC_{period}")[row0:row1, col0:col1],
                    dtype=np.uint8,
                )
                raw_valid = (raw >= 7500) & (raw != 0) & inside
                strict_qc, relaxed_qc = qc_masks(qc)
                strict = raw_valid & strict_qc
                relaxed = raw_valid & relaxed_qc
                values_c = raw.astype(np.float64) * 0.02 - 273.15

                key = (product, composite_start, period.lower())
                accumulator = accumulators.setdefault(
                    key,
                    {
                        "product": product,
                        "historical_year": year,
                        "composite_start": composite_start,
                        "period": period.lower(),
                        "tiles": set(),
                        "prefecture_pixels": 0,
                        "raw_valid_pixels": 0,
                        "strict_valid_pixels": 0,
                        "relaxed_valid_pixels": 0,
                        "strict_temperature_sum_c": 0.0,
                        "relaxed_temperature_sum_c": 0.0,
                    },
                )
                accumulator["tiles"].add(f"h{h:02d}v{v:02d}")
                accumulator["prefecture_pixels"] += int(inside.sum())
                accumulator["raw_valid_pixels"] += int(raw_valid.sum())
                accumulator["strict_valid_pixels"] += int(strict.sum())
                accumulator["relaxed_valid_pixels"] += int(relaxed.sum())
                accumulator["strict_temperature_sum_c"] += float(values_c[strict].sum())
                accumulator["relaxed_temperature_sum_c"] += float(values_c[relaxed].sum())
        finally:
            hdf.end()

    rows: list[dict[str, object]] = []
    for key in sorted(accumulators):
        accumulator = accumulators[key]
        denominator = int(accumulator["prefecture_pixels"])
        strict_count = int(accumulator["strict_valid_pixels"])
        relaxed_count = int(accumulator["relaxed_valid_pixels"])
        rows.append(
            {
                "product": accumulator["product"],
                "historical_year": accumulator["historical_year"],
                "composite_start": accumulator["composite_start"],
                "period": accumulator["period"],
                "tiles": ";".join(sorted(accumulator["tiles"])),
                "prefecture_pixels": denominator,
                "raw_valid_pixels": accumulator["raw_valid_pixels"],
                "strict_valid_pixels": strict_count,
                "relaxed_valid_pixels": relaxed_count,
                "strict_coverage_pct": round(100 * strict_count / denominator, 3),
                "relaxed_coverage_pct": round(100 * relaxed_count / denominator, 3),
                "strict_mean_lst_c": (
                    round(float(accumulator["strict_temperature_sum_c"]) / strict_count, 3)
                    if strict_count
                    else None
                ),
                "relaxed_mean_lst_c": (
                    round(float(accumulator["relaxed_temperature_sum_c"]) / relaxed_count, 3)
                    if relaxed_count
                    else None
                ),
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with COMPOSITE_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    groups: dict[str, dict[str, object]] = {}
    for product in sorted({str(row["product"]) for row in rows}):
        for period in ("day", "night"):
            selected = [
                row for row in rows if row["product"] == product and row["period"] == period
            ]
            strict = np.asarray([row["strict_coverage_pct"] for row in selected], dtype=float)
            relaxed = np.asarray([row["relaxed_coverage_pct"] for row in selected], dtype=float)
            groups[f"{product}_{period}"] = {
                "composites": len(selected),
                "strict_coverage_mean_pct": round(float(strict.mean()), 3),
                "strict_coverage_median_pct": round(float(np.median(strict)), 3),
                "strict_coverage_min_pct": round(float(strict.min()), 3),
                "strict_composites_at_least_50_pct": int((strict >= 50).sum()),
                "relaxed_coverage_mean_pct": round(float(relaxed.mean()), 3),
                "relaxed_coverage_median_pct": round(float(np.median(relaxed)), 3),
                "relaxed_coverage_min_pct": round(float(relaxed.min()), 3),
            }

    summary = {
        "files_read": len(files),
        "composite_period_rows": len(rows),
        "strict_qc_rule": (
            "mandatory QA good, data quality good, and reported LST error <= 1 K"
        ),
        "relaxed_qc_rule": (
            "mandatory QA good or other quality, data quality good, and reported LST error <= 2 K"
        ),
        "missing_value_treatment": "No imputation; invalid and cloud-affected pixels remain missing.",
        "coverage": groups,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"Saved: {COMPOSITE_PATH.relative_to(ROOT)}")
    print(f"Saved: {SUMMARY_PATH.relative_to(ROOT)}")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
