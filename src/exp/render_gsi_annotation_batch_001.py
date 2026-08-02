#!/usr/bin/env python3
"""Render photo-level labels directly onto batch-001 audit sheets."""

from __future__ import annotations

import math
import textwrap
from pathlib import Path

import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
BATCH_DIR = ROOT / "data/exp/gsi-imagery/triage/annotation_batches/batch_001_stratified"
RESULTS = BATCH_DIR / "annotation_results.csv"
OUTPUT_DIR = BATCH_DIR / "labeled_pages"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    properties = font_manager.FontProperties(
        family="DejaVu Sans", weight="bold" if bold else "normal"
    )
    return ImageFont.truetype(font_manager.findfont(properties), size=size)


TITLE = font(28, bold=True)
SUBTITLE = font(17)
CARD_TITLE = font(20, bold=True)
LABEL = font(16, bold=True)
TEXT = font(15)
NOTE = font(14)

COLORS = {
    "no_obvious_severe": (34, 139, 94),
    "uncertain": (217, 119, 6),
    "possible_severe": (202, 62, 62),
    "possible_collapse": (153, 27, 27),
}


def draw_card(sheet: Image.Image, row: pd.Series, x: int, y: int) -> None:
    draw = ImageDraw.Draw(sheet)
    width, height = 1600, 1135
    damage_color = COLORS[str(row["damage_class"])]
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=10,
        fill="#F8FAFC",
        outline="#64748B",
        width=2,
    )
    draw.rectangle((x, y, x + 16, y + height), fill=damage_color)

    image_box = (x + 28, y + 22, x + width - 24, y + 760)
    with Image.open(ROOT / row["full_photo_path"]) as source:
        preview = ImageOps.contain(
            source.convert("RGB"),
            (image_box[2] - image_box[0], image_box[3] - image_box[1]),
            method=Image.Resampling.LANCZOS,
        )
    paste_x = image_box[0] + (image_box[2] - image_box[0] - preview.width) // 2
    paste_y = image_box[1] + (image_box[3] - image_box[1] - preview.height) // 2
    sheet.paste(preview, (paste_x, paste_y))

    draw.text(
        (x + 30, y + 775),
        f"Item {int(row['batch_item']):02d}  {row['review_id']}  |  "
        f"{row['municipality']}  |  {str(row['photo_type']).title()}",
        font=CARD_TITLE,
        fill="#0F172A",
    )
    label_y = y + 815
    fields = [
        ("Assessability", row["assessability"]),
        ("Scene", row["scene_class"]),
        ("Damage", row["damage_class"]),
        ("Collapse candidate", row["collapse_candidate"]),
        ("Confidence", row["confidence"]),
    ]
    left = x + 30
    for index, (name, value) in enumerate(fields):
        column = index % 3
        line = index // 3
        field_x = left + column * 505
        field_y = label_y + line * 36
        draw.text((field_x, field_y), f"{name}:", font=LABEL, fill="#334155")
        value_x = field_x + draw.textlength(f"{name}: ", font=LABEL)
        draw.text((value_x, field_y), str(value), font=TEXT, fill="#0F172A")

    note_y = y + 895
    evidence = "" if pd.isna(row["evidence_tile"]) else str(row["evidence_tile"])
    draw.text(
        (x + 30, note_y),
        f"Evidence tile(s): {evidence or 'overview only'}",
        font=LABEL,
        fill="#334155",
    )
    wrapped = textwrap.wrap(str(row["evidence_note"]), width=118)[:4]
    for line_number, line in enumerate(wrapped):
        draw.text(
            (x + 30, note_y + 34 + line_number * 24),
            line,
            font=NOTE,
            fill="#334155",
        )


def main() -> int:
    results = pd.read_csv(RESULTS).sort_values("batch_item")
    if len(results) != 12 or not results["annotation_status"].eq("reviewed").all():
        raise ValueError("Expected 12 completed annotation records")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for page_number, start in enumerate(range(0, len(results), 4), start=1):
        page = results.iloc[start : start + 4]
        sheet = Image.new("RGB", (3280, 2445), "white")
        draw = ImageDraw.Draw(sheet)
        draw.text(
            (28, 18),
            "Kumamoto GSI aerial-photo annotation — batch 001",
            font=TITLE,
            fill="#0F172A",
        )
        draw.text(
            (28, 60),
            f"Labeled audit sheet {page_number}/{math.ceil(len(results) / 4)} | "
            "Photo-level screening; earthquake attribution unverified",
            font=SUBTITLE,
            fill="#475569",
        )
        for position, (_, row) in enumerate(page.iterrows()):
            card_x = 20 + (position % 2) * 1620
            card_y = 105 + (position // 2) * 1155
            draw_card(sheet, row, card_x, card_y)
        output = OUTPUT_DIR / f"batch001_labeled_p{page_number:02d}.jpg"
        sheet.save(output, format="JPEG", quality=94, optimize=True)
        print(f"Saved {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
