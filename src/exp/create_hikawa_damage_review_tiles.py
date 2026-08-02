#!/usr/bin/env python3
"""Create full-resolution review tiles for the three most residential Hikawa photos."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_CSV = PROJECT_ROOT / "data/exp/gsi-imagery/triage/focal_imagery_review_index.csv"
OUTPUT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_damage_manual_tiles"
GRID_BY_ID = {
    "HIK-V-0013": (2, 3),
    "HIK-V-0014": (3, 2),
    "HIK-V-0018": (2, 3),
}

REVIEW_RESULTS = {
    ("HIK-V-0013", "r1c1"): ("not_applicable", "golf_course", "高尔夫球场和林地，无住宅倒塌判读对象"),
    ("HIK-V-0013", "r1c2"): ("no_obvious_damage", "cloud_edge", "少量云遮挡；道路、光伏板和零散建筑轮廓完整"),
    ("HIK-V-0013", "r2c1"): ("no_obvious_damage", "residential", "聚落和道路连续，未见成片瓦砾或屋顶缺失"),
    ("HIK-V-0013", "r2c2"): ("no_obvious_damage", "mixed_rural", "互通、果园和零散住宅可辨，未见明确倒塌形态"),
    ("HIK-V-0013", "r3c1"): ("not_applicable", "forest_school", "以林地和学校设施为主，未见大型结构异常"),
    ("HIK-V-0013", "r3c2"): ("no_obvious_damage", "dense_residential", "住宅最密集切片；屋顶纹理总体连续，建议灾前图复核"),
    ("HIK-V-0014", "r1c1"): ("no_obvious_damage", "residential_river", "河流两侧住宅屋顶总体完整，未见连续瓦砾带"),
    ("HIK-V-0014", "r1c2"): ("needs_pre_event_review", "cloud_or_smoke_obscuration", "白色云/烟状区域遮挡建筑和农地；来源及遮挡下方情况无法判断"),
    ("HIK-V-0014", "r1c3"): ("no_obvious_damage", "dense_residential", "密集住宅、学校和设施屋顶总体连续"),
    ("HIK-V-0014", "r2c1"): ("not_applicable", "farmland", "以农地为主，山麓零散建筑未见明显异常"),
    ("HIK-V-0014", "r2c2"): ("not_applicable", "farmland", "以农地为主，北侧聚落未见明显成片异常"),
    ("HIK-V-0014", "r2c3"): ("no_obvious_damage", "rural_residential", "乡村住宅屋顶可辨，未见大型倒塌形态"),
    ("HIK-V-0018", "r1c1"): ("no_obvious_damage", "rural_residential", "农地间聚落轮廓连续，未见明确倒塌形态"),
    ("HIK-V-0018", "r1c2"): ("no_obvious_damage", "sparse_residential", "农地和山麓零散住宅未见明显异常"),
    ("HIK-V-0018", "r2c1"): ("no_obvious_damage", "residential_river", "河流两岸住宅连续，未见大型瓦砾场"),
    ("HIK-V-0018", "r2c2"): ("not_applicable", "forest_orchard", "主要为林地、果园及墓地状重复纹理，不是倒塌候选"),
    ("HIK-V-0018", "r3c1"): ("no_obvious_damage", "dense_residential", "密集住宅和商业设施屋顶总体完整，建议灾前图复核"),
    ("HIK-V-0018", "r3c2"): ("no_obvious_damage", "residential_infrastructure", "住宅、河道和高速设施完整，未见成片结构破坏"),
}


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        indexed = {row["review_id"]: row for row in csv.DictReader(handle)}

    manifest = []
    for photo_id, (columns, rows) in GRID_BY_ID.items():
        source = indexed[photo_id]
        source_path = PROJECT_ROOT / source["full_photo_path"]
        photo_dir = OUTPUT_DIR / photo_id
        photo_dir.mkdir(parents=True, exist_ok=True)
        with Image.open(source_path) as opened:
            image = opened.convert("RGB")
            width, height = image.size
            overview = image.copy()
            draw = ImageDraw.Draw(overview)
            for row in range(rows):
                for column in range(columns):
                    left = round(column * width / columns)
                    top = round(row * height / rows)
                    right = round((column + 1) * width / columns)
                    bottom = round((row + 1) * height / rows)
                    tile_id = f"r{row + 1}c{column + 1}"
                    tile_path = photo_dir / f"{photo_id}_{tile_id}.jpg"
                    image.crop((left, top, right, bottom)).save(tile_path, quality=97)
                    draw.rectangle((left, top, right - 1, bottom - 1), outline="red", width=max(3, width // 1000))
                    draw.text((left + 12, top + 12), tile_id, fill="red", stroke_width=2, stroke_fill="white")
                    review_status, candidate_type, review_note = REVIEW_RESULTS[(photo_id, tile_id)]
                    manifest.append(
                        {
                            "photo_id": photo_id,
                            "tile_id": tile_id,
                            "left_px": left,
                            "top_px": top,
                            "right_px": right,
                            "bottom_px": bottom,
                            "tile_path": str(tile_path.relative_to(PROJECT_ROOT)),
                            "review_status": review_status,
                            "candidate_type": candidate_type,
                            "review_note": review_note,
                        }
                    )
            overview.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            overview.save(photo_dir / f"{photo_id}_grid_overview.jpg", quality=94)

    fields = list(manifest[0])
    with (OUTPUT_DIR / "tile_review_manifest.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(manifest)
    print(f"Created {len(manifest)} full-resolution review tiles")


if __name__ == "__main__":
    main()
