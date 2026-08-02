#!/usr/bin/env python3
"""Prepare high-resolution overview and detail pages for the top-50 pilot review."""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
TRIAGE_DIR = ROOT / "data/exp/gsi-imagery/triage"
TOP50_PATH = TRIAGE_DIR / "top50_priority_review.csv"
OUTPUT_DIR = TRIAGE_DIR / "pilot_review"
OVERVIEW_DIR = OUTPUT_DIR / "overview_pages"
DETAIL_DIR = OUTPUT_DIR / "detail_pages"
ASSET_MANIFEST_PATH = OUTPUT_DIR / "review_asset_manifest.csv"
PROTOCOL_PATH = OUTPUT_DIR / "review_protocol.md"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    properties = font_manager.FontProperties(
        family="DejaVu Sans", weight="bold" if bold else "normal"
    )
    return ImageFont.truetype(font_manager.findfont(properties), size=size)


TITLE_FONT = font(24, bold=True)
SUBTITLE_FONT = font(15)
CARD_TITLE_FONT = font(18, bold=True)
CARD_TEXT_FONT = font(14)
TILE_FONT = font(18, bold=True)


def draw_overview_card(sheet: Image.Image, item: pd.Series, x: int, y: int) -> None:
    draw = ImageDraw.Draw(sheet)
    card_width, card_height = 1600, 1120
    draw.rounded_rectangle(
        (x + 4, y + 4, x + card_width - 5, y + card_height - 5),
        radius=8,
        fill="#F7F9FA",
        outline="#9EABB4",
        width=2,
    )
    image_box = (x + 12, y + 12, x + card_width - 12, y + 948)
    with Image.open(ROOT / item["full_photo_path"]) as source:
        image = ImageOps.contain(
            source.convert("RGB"),
            (image_box[2] - image_box[0], image_box[3] - image_box[1]),
            method=Image.Resampling.LANCZOS,
        )
    paste_x = image_box[0] + (image_box[2] - image_box[0] - image.width) // 2
    paste_y = image_box[1] + (image_box[3] - image_box[1] - image.height) // 2
    sheet.paste(image, (paste_x, paste_y))
    draw.text(
        (x + 15, y + 958),
        f"#{int(item['global_priority_rank']):02d}  {item['review_id']}  |  "
        f"{item['municipality']}  |  {item['photo_type'].title()}",
        font=CARD_TITLE_FONT,
        fill="#102A43",
    )
    draw.text(
        (x + 15, y + 992),
        f"Priority {item['priority_score']:.1f}  |  Nearby population {item['nearby_total_population_est']:.0f}  |  "
        f"Age 65+ {item['nearby_population_age_65_plus_est']:.0f}",
        font=CARD_TEXT_FONT,
        fill="#374957",
    )
    draw.text(
        (x + 15, y + 1022),
        f"{float(item['longitude']):.5f}E, {float(item['latitude']):.5f}N  |  "
        "Review ID links this page to the coding table",
        font=CARD_TEXT_FONT,
        fill="#374957",
    )


def build_overview_pages(
    top50: pd.DataFrame,
    output_dir: Path = OVERVIEW_DIR,
    title: str = "GSI top-50 full-resolution pilot review — overview",
) -> tuple[list[Path], dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    page_by_review_id: dict[str, str] = {}
    for page_number, start in enumerate(range(0, len(top50), 4), start=1):
        page = top50.iloc[start : start + 4]
        sheet = Image.new("RGB", (3260, 2390), "white")
        draw = ImageDraw.Draw(sheet)
        draw.text(
            (25, 14),
            title,
            font=TITLE_FONT,
            fill="#102A43",
        )
        draw.text(
            (25, 52),
            f"Page {page_number}/{math.ceil(len(top50) / 4)} | Overview screening; use detail pages for candidate verification",
            font=SUBTITLE_FONT,
            fill="#46515A",
        )
        for position, (_, item) in enumerate(page.iterrows()):
            x = 20 + (position % 2) * 1610
            y = 100 + (position // 2) * 1135
            draw_overview_card(sheet, item, x, y)
        destination = output_dir / f"overview_p{page_number:02d}.jpg"
        sheet.save(destination, format="JPEG", quality=94, optimize=True)
        outputs.append(destination)
        for review_id in page["review_id"]:
            page_by_review_id[str(review_id)] = str(destination.relative_to(ROOT))
    return outputs, page_by_review_id


def build_detail_page(item: pd.Series, output_dir: Path = DETAIL_DIR) -> Path | None:
    source_path = ROOT / item["full_photo_path"]
    with Image.open(source_path) as source:
        image = source.convert("RGB")
        if image.width <= 2500 and image.height <= 2500:
            return None
        columns, rows = 3, 2
        crop_width = math.ceil(image.width / columns)
        crop_height = math.ceil(image.height / rows)
        tile_width, tile_height = 1020, 760
        title_height, margin = 105, 18
        sheet = Image.new(
            "RGB",
            (margin * 2 + columns * tile_width, title_height + rows * tile_height + margin),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        draw.text(
            (margin, 14),
            f"#{int(item['global_priority_rank']):02d} {item['review_id']} — full-image detail grid",
            font=TITLE_FONT,
            fill="#102A43",
        )
        draw.text(
            (margin, 52),
            "Six non-overlapping tiles cover the complete source image; labels run west/left to east/right, then north/top to south/bottom.",
            font=SUBTITLE_FONT,
            fill="#46515A",
        )
        for row in range(rows):
            for column in range(columns):
                left = column * crop_width
                top = row * crop_height
                right = min((column + 1) * crop_width, image.width)
                bottom = min((row + 1) * crop_height, image.height)
                crop = image.crop((left, top, right, bottom))
                tile = ImageOps.contain(
                    crop,
                    (tile_width - 16, tile_height - 16),
                    method=Image.Resampling.LANCZOS,
                )
                x = margin + column * tile_width
                y = title_height + row * tile_height
                draw.rectangle(
                    (x + 3, y + 3, x + tile_width - 4, y + tile_height - 4),
                    fill="#F7F9FA",
                    outline="#9EABB4",
                    width=1,
                )
                paste_x = x + (tile_width - tile.width) // 2
                paste_y = y + (tile_height - tile.height) // 2
                sheet.paste(tile, (paste_x, paste_y))
                label = f"{chr(65 + row)}{column + 1}"
                draw.text(
                    (x + 12, y + 10),
                    label,
                    font=TILE_FONT,
                    fill="white",
                    stroke_width=3,
                    stroke_fill="#102A43",
                )
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / (
        f"rank{int(item['global_priority_rank']):02d}_{item['review_id']}_detail.jpg"
    )
    sheet.save(destination, format="JPEG", quality=94, optimize=True)
    return destination


def write_protocol() -> None:
    text = """# Top-50 full-resolution pilot review protocol

## Purpose

Test whether the post-event GSI imagery can produce reproducible candidate evidence of
housing damage in older-population exposure areas. This is not an estimate of collapsed
homes and does not establish earthquake attribution.

## Coding sequence

1. Review the overview page and code `scene_relevance` as `residential`, `mixed`,
   `nonresidential`, `irrelevant`, or `uncertain`.
2. Code `view_obstruction` as `none`, `partial`, or `severe` for cloud, haze, blur,
   extreme obliqueness, or other obstruction.
3. For residential or mixed scenes, inspect the detail page or original image.
4. Code `visible_structural_damage` and `collapse_candidate` as `yes`, `no`, or
   `uncertain`. A candidate requires a localized visual feature, not simply a high
   population-priority score.
5. Record the detail tile, a short observation, and confidence (`low`, `medium`, `high`).

## Interpretation boundary

Post-event imagery alone cannot distinguish earthquake damage from pre-existing
deterioration, demolition, construction, roof materials, greenhouses, shadows, or image
artifacts. Every positive candidate requires independent validation from official damage
records, pre-event imagery, orthophotos, or field information.
"""
    PROTOCOL_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    top50 = pd.read_csv(TOP50_PATH, dtype={"photo_number": "string"})
    if len(top50) != 50:
        raise ValueError(f"Expected 50 pilot images, found {len(top50)}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    overviews, page_by_id = build_overview_pages(top50)
    detail_by_id: dict[str, str] = {}
    for _, item in top50.iterrows():
        destination = build_detail_page(item)
        detail_by_id[str(item["review_id"])] = (
            str(destination.relative_to(ROOT)) if destination else ""
        )
    assets = top50[
        ["global_priority_rank", "review_id", "full_photo_path"]
    ].copy()
    assets["overview_page_path"] = assets["review_id"].map(page_by_id)
    assets["detail_page_path"] = assets["review_id"].map(detail_by_id)
    assets.to_csv(ASSET_MANIFEST_PATH, index=False)
    write_protocol()
    print(f"Overview pages: {len(overviews)}")
    print(f"Detail pages: {(assets['detail_page_path'] != '').sum()}")
    print(f"Saved {ASSET_MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Saved {PROTOCOL_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
