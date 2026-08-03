#!/usr/bin/env python3
"""Compare two bare-site full-resolution candidates with pre-event GSI imagery."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps

import pilot_hikawa_prepost_registration as registration


ROOT = Path(__file__).resolve().parents[2]
ANNOTATIONS = (
    ROOT
    / "data/exp/gsi-imagery/triage/annotation_batches/batch_001_stratified"
    / "annotation_results.csv"
)
CANDIDATES = ROOT / "data/exp/gsi-imagery/fullres_annotation_pilot/top_candidate_tiles.csv"
RAW_DIR = ROOT / "data/raw/imagery/gsi_historical/fullres_candidate_pre_event"
OUTPUT_DIR = ROOT / "data/exp/gsi-imagery/fullres_candidate_pre_event"
TARGET_RANKS = [3, 7]


def transform_candidate_polygon(row: pd.Series, result: dict) -> np.ndarray:
    scale = float(result["post_scale"])
    points = np.float32(
        [
            [float(row["x0"]) * scale, float(row["y0"]) * scale],
            [float(row["x1"]) * scale, float(row["y0"]) * scale],
            [float(row["x1"]) * scale, float(row["y1"]) * scale],
            [float(row["x0"]) * scale, float(row["y1"]) * scale],
        ]
    ).reshape(-1, 1, 2)
    return cv2.perspectiveTransform(points, result["homography"])[:, 0]


def save_comparison(
    rank: int,
    row: pd.Series,
    pre_rgb: np.ndarray,
    polygon: np.ndarray,
) -> str:
    source = Image.open(ROOT / str(row["source_path"])).convert("RGB")
    post_crop = source.crop(
        (int(row["x0"]), int(row["y0"]), int(row["x1"]), int(row["y1"]))
    )

    marked = Image.fromarray(pre_rgb.copy())
    draw = ImageDraw.Draw(marked)
    points = [(float(x), float(y)) for x, y in polygon]
    draw.line(points + [points[0]], fill="red", width=8)
    left = max(0, int(np.floor(polygon[:, 0].min())) - 180)
    top = max(0, int(np.floor(polygon[:, 1].min())) - 180)
    right = min(marked.width, int(np.ceil(polygon[:, 0].max())) + 180)
    bottom = min(marked.height, int(np.ceil(polygon[:, 1].max())) + 180)
    pre_context = marked.crop((left, top, right, bottom))

    canvas = Image.new("RGB", (1600, 850), "white")
    font = ImageFont.load_default(size=24)
    small = ImageFont.load_default(size=18)
    post_panel = ImageOps.contain(post_crop, (740, 700), Image.Resampling.LANCZOS)
    pre_panel = ImageOps.contain(pre_context, (740, 700), Image.Resampling.LANCZOS)
    canvas.paste(post_panel, (30 + (740 - post_panel.width) // 2, 80))
    canvas.paste(pre_panel, (830 + (740 - pre_panel.width) // 2, 80))
    canvas_draw = ImageDraw.Draw(canvas)
    canvas_draw.text(
        (30, 20),
        f"Candidate #{rank:02d} {row['review_id']}: post-event vs pre-event context",
        fill="black",
        font=font,
    )
    canvas_draw.text((30, 795), "Post-event native 512 px crop", fill="black", font=small)
    canvas_draw.text(
        (830, 795),
        "Pre-event annual orthophoto; red polygon is registered candidate footprint",
        fill="black",
        font=small,
    )
    destination = OUTPUT_DIR / f"rank{rank:03d}_{row['review_id']}_prepost.jpg"
    canvas.save(destination, quality=94)
    return str(destination.relative_to(ROOT))


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    annotations = pd.read_csv(ANNOTATIONS).set_index("review_id")
    candidates = pd.read_csv(CANDIDATES)
    targets = candidates.loc[candidates["candidate_rank"].isin(TARGET_RANKS)].copy()
    if set(targets["candidate_rank"]) != set(TARGET_RANKS):
        raise ValueError("Expected both selected candidate ranks.")

    output_rows: list[dict] = []
    for _, row in targets.sort_values("candidate_rank").iterrows():
        rank = int(row["candidate_rank"])
        review_id = str(row["review_id"])
        source = annotations.loc[review_id]
        lon, lat = float(source["longitude"]), float(source["latitude"])
        centre_x, centre_y = registration.lonlat_to_tile(lon, lat, registration.ZOOM)
        year, checks = registration.latest_available_year(centre_x, centre_y)
        output: dict = {
            "candidate_rank": rank,
            "review_id": review_id,
            "selected_pre_event_year": year or "",
            "registration_status": "no_pre_event_annual_tile_2018_2025",
            "comparison_path": "",
            "interpretation": "not_assessable",
        }
        if year is None:
            output_rows.append(output)
            continue

        registration.RAW_DIR = RAW_DIR
        pre_rgb, valid_mask, metadata = registration.build_mosaic(
            review_id, year, centre_x, centre_y
        )
        with Image.open(ROOT / str(source["full_photo_path"])) as opened:
            post_rgb = np.asarray(opened.convert("RGB"))
        result = registration.register(post_rgb, pre_rgb, valid_mask)
        output.update(
            {
                "registration_status": result["status"],
                "available_mosaic_tiles": metadata["available_tiles"],
                "inliers": result.get("inliers", ""),
                "rmse_px": result.get("rmse_px", ""),
                "projected_area_ratio": result.get("projected_area_ratio", ""),
            }
        )
        if result["status"] in {
            "good_global_match",
            "usable_global_match",
            "tentative_global_match",
        }:
            polygon = transform_candidate_polygon(row, result)
            output["comparison_path"] = save_comparison(rank, row, pre_rgb, polygon)
            output["interpretation"] = "requires_visual_prepost_review"
        output_rows.append(output)
        print(
            f"rank {rank:02d} {review_id}: pre={year}, status={result['status']}, "
            f"tiles={metadata['available_tiles']}/81",
            flush=True,
        )

    fields: list[str] = []
    for row in output_rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with (OUTPUT_DIR / "comparison_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    (OUTPUT_DIR / "experiment_config.json").write_text(
        json.dumps(
            {
                "target_ranks": TARGET_RANKS,
                "pre_event_years_checked": registration.YEARS,
                "zoom": registration.ZOOM,
                "mosaic_radius_tiles": registration.RADIUS_TILES,
                "warning": "registration diagnostics are not earthquake-damage labels",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
