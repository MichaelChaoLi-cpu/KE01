#!/usr/bin/env python3
"""Zero-shot visual triage of all post-event GSI photographs covering Hikawa.

This experiment uses CLIP prompt matching to rank image tiles for human review.
Scores are relative screening scores, not damage probabilities or official counts.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import torch
from PIL import Image, ImageDraw, ImageFont, ImageOps
from transformers import CLIPModel, CLIPProcessor


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_CSV = PROJECT_ROOT / "data/exp/gsi-imagery/triage/focal_imagery_review_index.csv"
OUTPUT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_clip_damage_pilot"
MODEL_CACHE = PROJECT_ROOT / "data/raw/models/huggingface"
MODEL_NAME = "openai/clip-vit-base-patch32"

PROMPTS = {
    "damage": [
        "an aerial photograph of a collapsed house after an earthquake",
        "an aerial photograph of earthquake rubble and destroyed buildings",
        "an aerial photograph of a severely damaged roof and building debris",
    ],
    "intact": [
        "an aerial photograph of intact houses in a residential neighborhood",
        "an aerial photograph of undamaged buildings and roofs",
    ],
    "confounder": [
        "an aerial photograph of a construction site",
        "an aerial photograph of a quarry or exposed soil",
        "an aerial photograph of farmland and greenhouses",
        "an aerial photograph of forest or mountains",
        "an aerial photograph of water or a river",
        "an aerial photograph of an industrial facility",
    ],
}

BUILDING_PROMPTS = {
    "building_present": [
        "an aerial photograph containing houses and buildings",
        "an overhead photograph of a residential neighborhood with many rooftops",
        "an aerial photograph of houses next to roads",
    ],
    "building_absent": [
        "an aerial photograph of forest with no buildings",
        "an aerial photograph of farmland with no buildings",
        "an aerial photograph of exposed soil with no buildings",
        "an aerial photograph of water with no buildings",
    ],
}


@dataclass(frozen=True)
class Tile:
    review_id: str
    photo_type: str
    source_path: str
    camera_longitude: str
    camera_latitude: str
    x0: int
    y0: int
    x1: int
    y1: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile-size", type=int, default=512)
    parser.add_argument("--stride", type=int, default=448)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--max-per-image", type=int, default=3)
    parser.add_argument("--nms-iou", type=float, default=0.30)
    parser.add_argument("--limit-images", type=int, default=None)
    return parser.parse_args()


def positions(length: int, tile_size: int, stride: int) -> list[int]:
    if length <= tile_size:
        return [0]
    values = list(range(0, length - tile_size + 1, stride))
    last = length - tile_size
    if values[-1] != last:
        values.append(last)
    return values


def batched(values: list, batch_size: int) -> Iterable[list]:
    for start in range(0, len(values), batch_size):
        yield values[start : start + batch_size]


def logmeanexp(values: torch.Tensor, indices: list[int]) -> torch.Tensor:
    selected = values[:, indices]
    return torch.logsumexp(selected, dim=1) - math.log(len(indices))


def iou(a: dict, b: dict) -> float:
    left = max(int(a["x0"]), int(b["x0"]))
    top = max(int(a["y0"]), int(b["y0"]))
    right = min(int(a["x1"]), int(b["x1"]))
    bottom = min(int(a["y1"]), int(b["y1"]))
    intersection = max(0, right - left) * max(0, bottom - top)
    area_a = (int(a["x1"]) - int(a["x0"])) * (int(a["y1"]) - int(a["y0"]))
    area_b = (int(b["x1"]) - int(b["x0"])) * (int(b["y1"]) - int(b["y0"]))
    union = area_a + area_b - intersection
    return intersection / union if union else 0.0


def select_candidates(rows: list[dict], top_k: int, max_per_image: int, threshold: float) -> list[dict]:
    selected: list[dict] = []
    per_image: dict[str, list[dict]] = {}
    for row in sorted(rows, key=lambda item: float(item["damage_priority_score"]), reverse=True):
        prior = per_image.setdefault(row["review_id"], [])
        if len(prior) >= max_per_image:
            continue
        if any(iou(row, kept) > threshold for kept in prior):
            continue
        candidate = dict(row)
        prior.append(candidate)
        selected.append(candidate)
        if len(selected) == top_k:
            break
    for rank, row in enumerate(selected, start=1):
        row["candidate_rank"] = rank
    return selected


def read_hikawa_rows(limit: int | None) -> list[dict[str, str]]:
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["municipality"] == "Hikawa"]
    rows.sort(key=lambda row: row["review_id"])
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        raise ValueError("No Hikawa photographs found in the focal imagery index.")
    return rows


def load_model() -> tuple[CLIPModel, CLIPProcessor, torch.device]:
    MODEL_CACHE.mkdir(parents=True, exist_ok=True)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    # The experiment is intentionally reproducible from the project-local cache after
    # the one-time model download.  The official repository's main revision provides
    # PyTorch weights, so explicitly avoid a network probe for safetensors on each run.
    model = CLIPModel.from_pretrained(
        MODEL_NAME,
        cache_dir=MODEL_CACHE,
        local_files_only=True,
        use_safetensors=False,
    )
    processor = CLIPProcessor.from_pretrained(
        MODEL_NAME, cache_dir=MODEL_CACHE, local_files_only=True
    )
    model.eval().to(device)
    return model, processor, device


def score_tiles(args: argparse.Namespace, source_rows: list[dict[str, str]]) -> list[dict]:
    model, processor, device = load_model()
    prompt_list = [prompt for group in PROMPTS.values() for prompt in group]
    group_indices: dict[str, list[int]] = {}
    cursor = 0
    for name, prompts in PROMPTS.items():
        group_indices[name] = list(range(cursor, cursor + len(prompts)))
        cursor += len(prompts)
    building_indices: dict[str, list[int]] = {}
    for name, prompts in BUILDING_PROMPTS.items():
        building_indices[name] = list(range(cursor, cursor + len(prompts)))
        prompt_list.extend(prompts)
        cursor += len(prompts)

    text_inputs = processor(text=prompt_list, return_tensors="pt", padding=True)
    text_inputs = {key: value.to(device) for key, value in text_inputs.items()}
    with torch.inference_mode():
        text_features = model.get_text_features(**text_inputs).pooler_output
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        logit_scale = model.logit_scale.exp().clamp(max=100)

    scored: list[dict] = []
    for image_number, source in enumerate(source_rows, start=1):
        source_path = PROJECT_ROOT / source["full_photo_path"]
        with Image.open(source_path) as opened:
            image = opened.convert("RGB")
        xs = positions(image.width, args.tile_size, args.stride)
        ys = positions(image.height, args.tile_size, args.stride)
        tile_records: list[Tile] = []
        crops: list[Image.Image] = []
        for y0 in ys:
            for x0 in xs:
                x1 = min(x0 + args.tile_size, image.width)
                y1 = min(y0 + args.tile_size, image.height)
                crop = image.crop((x0, y0, x1, y1))
                if crop.width != args.tile_size or crop.height != args.tile_size:
                    crop = ImageOps.pad(crop, (args.tile_size, args.tile_size), color=(128, 128, 128))
                crops.append(crop)
                tile_records.append(
                    Tile(
                        review_id=source["review_id"],
                        photo_type=source["photo_type"],
                        source_path=source["full_photo_path"],
                        camera_longitude=source["longitude"],
                        camera_latitude=source["latitude"],
                        x0=x0,
                        y0=y0,
                        x1=x1,
                        y1=y1,
                    )
                )

        offset = 0
        for crop_batch in batched(crops, args.batch_size):
            image_inputs = processor(images=crop_batch, return_tensors="pt")
            pixel_values = image_inputs["pixel_values"].to(device)
            with torch.inference_mode():
                image_features = model.get_image_features(pixel_values=pixel_values).pooler_output
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                logits = logit_scale * image_features @ text_features.T
                category_logits = torch.stack(
                    [logmeanexp(logits, group_indices[name]) for name in PROMPTS], dim=1
                )
                category_scores = category_logits.softmax(dim=1).cpu()
                building_logits = torch.stack(
                    [logmeanexp(logits, building_indices[name]) for name in BUILDING_PROMPTS],
                    dim=1,
                )
                building_scores = building_logits.softmax(dim=1).cpu()
                prompt_scores = logits.softmax(dim=1).cpu()

            for local_index in range(len(crop_batch)):
                tile = tile_records[offset + local_index]
                category = category_scores[local_index]
                prompts = prompt_scores[local_index]
                damage_score = category[0].item()
                intact_score = category[1].item()
                confounder_score = category[2].item()
                building_score = building_scores[local_index, 0].item()
                scored.append(
                    {
                        "review_id": tile.review_id,
                        "photo_type": tile.photo_type,
                        "source_path": tile.source_path,
                        "camera_longitude": tile.camera_longitude,
                        "camera_latitude": tile.camera_latitude,
                        "x0": tile.x0,
                        "y0": tile.y0,
                        "x1": tile.x1,
                        "y1": tile.y1,
                        "damage_priority_score": f"{damage_score * building_score:.8f}",
                        "damage_margin_score": f"{damage_score - max(intact_score, confounder_score):.8f}",
                        "damage_prompt_score": f"{damage_score:.8f}",
                        "intact_prompt_score": f"{intact_score:.8f}",
                        "confounder_prompt_score": f"{confounder_score:.8f}",
                        "building_prompt_score": f"{building_score:.8f}",
                        "top_prompt": prompt_list[int(prompts.argmax().item())],
                        "candidate_geolocation_available": "no_camera_centre_only",
                    }
                )
            offset += len(crop_batch)
        print(
            f"[{image_number:02d}/{len(source_rows):02d}] {source['review_id']} "
            f"{image.width}x{image.height}: {len(crops)} tiles",
            flush=True,
        )
    return scored


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write to {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save_candidate_assets(
    candidates: list[dict],
    args: argparse.Namespace,
    output_dir: Path = OUTPUT_DIR,
    sheet_title: str = "Hikawa CLIP damage-candidate triage",
) -> None:
    crops_dir = output_dir / "candidate_crops"
    sheets_dir = output_dir / "contact_sheets"
    crops_dir.mkdir(parents=True, exist_ok=True)
    sheets_dir.mkdir(parents=True, exist_ok=True)
    # These folders contain only deterministic outputs from this script. Remove stale
    # assets from a preceding smoke test before writing the complete run.
    for stale in crops_dir.glob("rank*.jpg"):
        stale.unlink()
    for stale in sheets_dir.glob("candidate_contact_sheet_p*.jpg"):
        stale.unlink()
    font = ImageFont.load_default(size=22)
    small_font = ImageFont.load_default(size=16)

    source_cache: dict[str, Image.Image] = {}
    for row in candidates:
        source = row["source_path"]
        if source not in source_cache:
            with Image.open(PROJECT_ROOT / source) as opened:
                source_cache[source] = opened.convert("RGB")
        crop = source_cache[source].crop(
            (int(row["x0"]), int(row["y0"]), int(row["x1"]), int(row["y1"]))
        )
        rank = int(row["candidate_rank"])
        name = f"rank{rank:03d}_{row['review_id']}_x{row['x0']}_y{row['y0']}.jpg"
        crop_path = crops_dir / name
        crop.save(crop_path, quality=94)
        row["candidate_crop_path"] = str(crop_path.relative_to(PROJECT_ROOT))

    per_page = 12
    cell_w, cell_h = 520, 430
    for page_index, start in enumerate(range(0, len(candidates), per_page), start=1):
        page_rows = candidates[start : start + per_page]
        canvas = Image.new("RGB", (cell_w * 3, cell_h * 4 + 90), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text(
            (20, 18),
            f"{sheet_title} — page {page_index}",
            fill="black",
            font=font,
        )
        draw.text(
            (20, 52),
            "Relative prompt scores only; every candidate requires human review.",
            fill=(80, 80, 80),
            font=small_font,
        )
        for panel_index, row in enumerate(page_rows):
            col, grid_row = panel_index % 3, panel_index // 3
            left, top = col * cell_w, 90 + grid_row * cell_h
            crop = Image.open(PROJECT_ROOT / row["candidate_crop_path"]).convert("RGB")
            preview = ImageOps.contain(crop, (cell_w - 20, 330))
            canvas.paste(preview, (left + (cell_w - preview.width) // 2, top + 5))
            label = (
                f"#{int(row['candidate_rank']):02d} {row['review_id']}  "
                f"priority={float(row['damage_priority_score']):+.3f}  "
                f"damage={float(row['damage_prompt_score']):.3f}  "
                f"building={float(row['building_prompt_score']):.3f}"
                f"conf={float(row['confounder_prompt_score']):.3f}"
            )
            draw.text((left + 10, top + 342), label, fill="black", font=small_font)
            draw.text(
                (left + 10, top + 370),
                f"pixel ({row['x0']}, {row['y0']})  {row['photo_type']}",
                fill=(70, 70, 70),
                font=small_font,
            )
        sheet_path = sheets_dir / f"candidate_contact_sheet_p{page_index:02d}.jpg"
        canvas.save(sheet_path, quality=92)


def write_documentation(args: argparse.Namespace, source_count: int, tile_count: int, candidates: list[dict]) -> None:
    config = {
        "model": MODEL_NAME,
        "method": "zero-shot CLIP prompt matching",
        "tile_size_px": args.tile_size,
        "stride_px": args.stride,
        "images": source_count,
        "tiles": tile_count,
        "top_k_after_within_image_nms": len(candidates),
        "max_candidates_per_image": args.max_per_image,
        "nms_iou": args.nms_iou,
        "prompts": PROMPTS,
        "building_prompts": BUILDING_PROMPTS,
        "score_interpretation": "relative prompt-match score, not a calibrated probability",
    }
    (OUTPUT_DIR / "experiment_config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    readme = f"""# Hikawa zero-shot image-recognition pilot

## Purpose

Screen all {source_count} available GSI post-event aerial photographs assigned to Hikawa Town and rank visually unusual tiles for manual review. The official FDMA report mentions two residential buckling incidents in Hikawa but provides no coordinates; this experiment tests candidate recall, not official-count estimation.

## Method

- Model: `{MODEL_NAME}`
- Input: {source_count} photographs ({tile_count:,} overlapping {args.tile_size} px tiles)
- Ranking: damage prompt score multiplied by an independent building-presence prompt score
- Deduplication: within-image non-maximum suppression at IoU {args.nms_iou:.2f}, maximum {args.max_per_image} candidates per image
- Output: top {len(candidates)} candidate crops for human review

`damage_prompt_score` is a relative score conditional on the selected prompts. It is not a calibrated probability, a building count, or confirmation of earthquake damage.

## Interpretation limits

The source photographs are post-event-only camera images rather than a uniform orthophoto. Image overlap, viewpoint, clouds, construction sites, exposed soil, greenhouses, and industrial facilities can produce false positives. Roof-intact buckling and internal damage may be invisible from above. Camera longitude and latitude are retained for source-photo context but do not geolocate an individual candidate tile.

The appropriate endpoint is a human-reviewed candidate list. Estimating total damaged houses requires pre-event imagery, building footprints, geographic registration, and validation labels or official inspection records.
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    args = parse_args()
    Image.MAX_IMAGE_PIXELS = None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source_rows = read_hikawa_rows(args.limit_images)
    scored = score_tiles(args, source_rows)
    candidates = select_candidates(scored, args.top_k, args.max_per_image, args.nms_iou)
    save_candidate_assets(candidates, args)
    write_csv(OUTPUT_DIR / "all_tile_scores.csv", scored)
    write_csv(OUTPUT_DIR / "top_candidate_tiles.csv", candidates)
    write_documentation(args, len(source_rows), len(scored), candidates)
    print(f"Scored {len(scored):,} tiles; saved {len(candidates)} candidates to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
