#!/usr/bin/env python3
"""Rank full-resolution tiles from five high-detail GSI batch-001 photographs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from PIL import Image

import run_hikawa_clip_damage_pilot as clip


ROOT = Path(__file__).resolve().parents[2]
ANNOTATIONS = (
    ROOT
    / "data/exp/gsi-imagery/triage/annotation_batches/batch_001_stratified"
    / "annotation_results.csv"
)
OUTPUT_DIR = ROOT / "data/exp/gsi-imagery/fullres_annotation_pilot"
SELECTED_IDS = [
    "YAT-V-0120",
    "YAT-V-0177",
    "HIK-V-0014",
    "UKI-O-0009",
    "UKI-O-0010",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile-size", type=int, default=512)
    parser.add_argument("--stride", type=int, default=384)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--top-k", type=int, default=30)
    parser.add_argument("--max-per-image", type=int, default=6)
    parser.add_argument("--nms-iou", type=float, default=0.30)
    return parser.parse_args()


def read_selected_rows() -> list[dict[str, str]]:
    frame = pd.read_csv(ANNOTATIONS, dtype={"photo_number": "string"})
    selected = frame.loc[frame["review_id"].isin(SELECTED_IDS)].copy()
    order = {review_id: index for index, review_id in enumerate(SELECTED_IDS)}
    selected["selection_order"] = selected["review_id"].map(order)
    selected = selected.sort_values("selection_order")
    missing = set(SELECTED_IDS) - set(selected["review_id"])
    if missing:
        raise ValueError(f"Missing selected review IDs: {sorted(missing)}")

    rows: list[dict[str, str]] = []
    for source in selected.to_dict("records"):
        path = ROOT / str(source["full_photo_path"])
        with Image.open(path) as image:
            width, height = image.size
        if width < 4000 or height < 2800:
            raise ValueError(
                f"Selected source {source['review_id']} is not high-detail: {width}x{height}"
            )
        source["source_width_px"] = str(width)
        source["source_height_px"] = str(height)
        rows.append({key: str(value) for key, value in source.items()})
    return rows


def write_documentation(
    args: argparse.Namespace,
    source_rows: list[dict[str, str]],
    tile_count: int,
    candidate_count: int,
) -> None:
    config = {
        "model": clip.MODEL_NAME,
        "purpose": "full-resolution missed-collapse sensitivity check",
        "source_review_ids": SELECTED_IDS,
        "source_dimensions_px": {
            row["review_id"]: [
                int(row["source_width_px"]),
                int(row["source_height_px"]),
            ]
            for row in source_rows
        },
        "tile_size_px": args.tile_size,
        "stride_px": args.stride,
        "tile_count": tile_count,
        "top_k": candidate_count,
        "max_candidates_per_image": args.max_per_image,
        "score_interpretation": "relative screening score, not damage probability",
    }
    (OUTPUT_DIR / "experiment_config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    readme = f"""# GSI full-resolution annotation pilot

## Purpose

Test whether whole-photo downsampling hid localized building-collapse evidence. Five of
the highest-detail photographs from annotation batch 001 are screened as overlapping
native-resolution crops.

## Inputs and method

- Source photographs: {len(source_rows)}
- Native-resolution tiles scored: {tile_count:,}
- Tile size / stride: {args.tile_size} / {args.stride} pixels
- Candidate crops retained for human review: {candidate_count}
- Ranking model: `{clip.MODEL_NAME}`

The model only prioritizes crops. Scores are not probabilities and cannot establish
earthquake attribution. Every retained crop must be inspected at its saved native pixel
resolution before assigning a damage label.
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    args = parse_args()
    Image.MAX_IMAGE_PIXELS = None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source_rows = read_selected_rows()
    scored = clip.score_tiles(args, source_rows)
    candidates = clip.select_candidates(
        scored, args.top_k, args.max_per_image, args.nms_iou
    )
    clip.save_candidate_assets(
        candidates,
        args,
        output_dir=OUTPUT_DIR,
        sheet_title="GSI full-resolution candidate review",
    )
    clip.write_csv(OUTPUT_DIR / "all_tile_scores.csv", scored)
    clip.write_csv(OUTPUT_DIR / "top_candidate_tiles.csv", candidates)
    write_documentation(args, source_rows, len(scored), len(candidates))
    print(
        f"Scored {len(scored):,} native-resolution tiles; "
        f"saved {len(candidates)} candidates to {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()
