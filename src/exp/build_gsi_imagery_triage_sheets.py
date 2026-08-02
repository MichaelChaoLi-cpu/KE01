#!/usr/bin/env python3
"""Build focal-municipality contact sheets for GSI earthquake imagery triage."""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
IMAGERY_ROOT = ROOT / "data/raw/imagery/gsi_2026_kumamoto"
CATALOG_DIR = IMAGERY_ROOT / "catalog"
BOUNDARY_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_DIR = ROOT / "data/exp/gsi-imagery/triage"
SHEET_DIR = OUTPUT_DIR / "contact_sheets"
REVIEW_INDEX_PATH = OUTPUT_DIR / "focal_imagery_review_index.csv"
SHEET_MANIFEST_PATH = OUTPUT_DIR / "contact_sheet_manifest.csv"
README_PATH = OUTPUT_DIR / "README.md"

FOCAL_AREAS = {
    "202": ("Yatsushiro", "YAT"),
    "213": ("Uki", "UKI"),
    "468": ("Hikawa", "HIK"),
}
PHOTO_TYPE_LABELS = {"vertical": "Vertical", "oblique": "Oblique"}
SHEET_COLUMNS = 6
SHEET_ROWS = 5
PHOTOS_PER_SHEET = SHEET_COLUMNS * SHEET_ROWS
CARD_WIDTH = 220
CARD_HEIGHT = 390
TITLE_HEIGHT = 105
MARGIN = 20
IMAGE_PADDING = 8


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    properties = font_manager.FontProperties(
        family="DejaVu Sans", weight="bold" if bold else "normal"
    )
    path = font_manager.findfont(properties, fallback_to_default=True)
    return ImageFont.truetype(path, size=size)


TITLE_FONT = font(25, bold=True)
SUBTITLE_FONT = font(16)
CARD_TITLE_FONT = font(14, bold=True)
CARD_TEXT_FONT = font(12)


def normalize_captured_at(value: object) -> str:
    """Convert official Japanese and camera timestamp formats to ISO-like ASCII."""
    text = str(value).strip()
    japanese = re.fullmatch(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日\s+(\d{1,2})時(\d{1,2})分(\d{1,2})秒",
        text,
    )
    if japanese:
        year, month, day, hour, minute, second = map(int, japanese.groups())
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    camera = re.fullmatch(
        r"(\d{4}):(\d{2}):(\d{2})-(\d{2}):(\d{2}):(\d{2})", text
    )
    if camera:
        year, month, day, hour, minute, second = map(int, camera.groups())
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return text


def load_focal_photos() -> pd.DataFrame:
    photos = pd.read_csv(
        CATALOG_DIR / "photo_catalog.csv",
        dtype={"photo_number": "string", "layer_id": "string"},
    )
    thumbnails = pd.read_csv(
        CATALOG_DIR / "thumbnail_manifest.csv",
        dtype={"photo_number": "string", "layer_id": "string"},
    )[["layer_id", "photo_number", "relative_path", "status"]].rename(
        columns={
            "relative_path": "thumbnail_path",
            "status": "thumbnail_status",
        }
    )
    full_photos = pd.read_csv(
        CATALOG_DIR / "full_photo_manifest.csv",
        dtype={"photo_number": "string", "layer_id": "string"},
    )[["layer_id", "photo_number", "relative_path", "status"]].rename(
        columns={"relative_path": "full_photo_path", "status": "full_photo_status"}
    )
    photos = photos.merge(
        thumbnails, on=["layer_id", "photo_number"], how="left", validate="one_to_one"
    ).merge(
        full_photos, on=["layer_id", "photo_number"], how="left", validate="one_to_one"
    )
    if not photos["thumbnail_status"].eq("kept").all():
        raise ValueError("The thumbnail manifest contains unavailable focal-review inputs")
    if not photos["full_photo_status"].eq("kept").all():
        raise ValueError("The full-photo manifest contains unavailable focal-review inputs")

    photos["captured_at"] = photos["captured_at"].map(normalize_captured_at)

    photos["photo_type"] = photos["category"].str.contains("斜め写真").map(
        {True: "oblique", False: "vertical"}
    )
    points = gpd.GeoDataFrame(
        photos,
        geometry=gpd.points_from_xy(photos["longitude"], photos["latitude"]),
        crs=4326,
    )
    small_areas = gpd.read_file(
        BOUNDARY_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(4326)
    small_areas["CITY"] = small_areas["CITY"].astype(str).str.zfill(3)
    municipalities = small_areas.dissolve(by=["CITY", "CITY_NAME"], as_index=False)
    joined = gpd.sjoin(
        points,
        municipalities[["CITY", "CITY_NAME", "geometry"]],
        how="left",
        predicate="within",
    ).drop(columns=["index_right", "geometry"])
    focal = joined.loc[joined["CITY"].isin(FOCAL_AREAS)].copy()
    if len(focal) != 1_064:
        raise ValueError(f"Expected 1,064 focal photos, found {len(focal):,}")
    return pd.DataFrame(focal)


def draw_card(
    sheet: Image.Image, row: pd.Series, column_index: int, row_index: int
) -> None:
    x = MARGIN + column_index * CARD_WIDTH
    y = TITLE_HEIGHT + row_index * CARD_HEIGHT
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle(
        (x + 3, y + 3, x + CARD_WIDTH - 4, y + CARD_HEIGHT - 4),
        radius=6,
        fill="#F7F9FA",
        outline="#A9B3BA",
        width=1,
    )

    image_box = (
        x + IMAGE_PADDING,
        y + IMAGE_PADDING,
        x + CARD_WIDTH - IMAGE_PADDING,
        y + 308,
    )
    with Image.open(ROOT / str(row["thumbnail_path"])) as source:
        thumbnail = ImageOps.contain(
            source.convert("RGB"),
            (image_box[2] - image_box[0], image_box[3] - image_box[1]),
            method=Image.Resampling.LANCZOS,
        )
    image_x = image_box[0] + (image_box[2] - image_box[0] - thumbnail.width) // 2
    image_y = image_box[1] + (image_box[3] - image_box[1] - thumbnail.height) // 2
    sheet.paste(thumbnail, (image_x, image_y))

    draw.text(
        (x + 9, y + 314),
        f"{row['review_id']}  |  Photo {row['photo_number']}",
        font=CARD_TITLE_FONT,
        fill="#102A43",
    )
    draw.text(
        (x + 9, y + 337),
        f"{PHOTO_TYPE_LABELS[row['photo_type']]}  |  {row['captured_at']}",
        font=CARD_TEXT_FONT,
        fill="#374957",
    )
    draw.text(
        (x + 9, y + 358),
        f"{float(row['longitude']):.5f}E, {float(row['latitude']):.5f}N",
        font=CARD_TEXT_FONT,
        fill="#374957",
    )


def build_sheets(focal: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    review_rows: list[pd.DataFrame] = []
    sheet_rows: list[dict[str, object]] = []
    SHEET_DIR.mkdir(parents=True, exist_ok=True)

    for city_code, (municipality, prefix) in FOCAL_AREAS.items():
        for photo_type in ["vertical", "oblique"]:
            subset = focal.loc[
                (focal["CITY"] == city_code) & (focal["photo_type"] == photo_type)
            ].copy()
            subset = subset.sort_values(
                ["latitude", "longitude", "layer_id", "photo_number"],
                ascending=[False, True, True, True],
            ).reset_index(drop=True)
            subset["review_id"] = [
                f"{prefix}-{photo_type[0].upper()}-{index:04d}"
                for index in range(1, len(subset) + 1)
            ]
            subset["contact_sheet_page"] = (
                subset.index // PHOTOS_PER_SHEET + 1
            ).astype(int)
            subset["panel_position"] = (
                subset.index % PHOTOS_PER_SHEET + 1
            ).astype(int)
            review_rows.append(subset)

            total_pages = math.ceil(len(subset) / PHOTOS_PER_SHEET)
            for page_number in range(1, total_pages + 1):
                page = subset.loc[subset["contact_sheet_page"] == page_number]
                sheet = Image.new(
                    "RGB",
                    (
                        MARGIN * 2 + SHEET_COLUMNS * CARD_WIDTH,
                        TITLE_HEIGHT + SHEET_ROWS * CARD_HEIGHT + MARGIN,
                    ),
                    "white",
                )
                draw = ImageDraw.Draw(sheet)
                draw.text(
                    (MARGIN, 16),
                    f"{municipality} — {PHOTO_TYPE_LABELS[photo_type]} aerial-photo triage",
                    font=TITLE_FONT,
                    fill="#102A43",
                )
                draw.text(
                    (MARGIN, 55),
                    f"Page {page_number}/{total_pages}  |  Spatial order: north-to-south, then west-to-east  |  "
                    f"Camera centres only",
                    font=SUBTITLE_FONT,
                    fill="#46515A",
                )
                for position, (_, row) in enumerate(page.iterrows()):
                    draw_card(
                        sheet,
                        row,
                        column_index=position % SHEET_COLUMNS,
                        row_index=position // SHEET_COLUMNS,
                    )
                destination = (
                    SHEET_DIR
                    / f"{municipality.lower()}_{photo_type}_p{page_number:03d}.jpg"
                )
                sheet.save(destination, format="JPEG", quality=92, optimize=True)
                sheet_rows.append(
                    {
                        "municipality_code": city_code,
                        "municipality": municipality,
                        "photo_type": photo_type,
                        "page": page_number,
                        "page_count": total_pages,
                        "photo_count": len(page),
                        "review_id_first": page.iloc[0]["review_id"],
                        "review_id_last": page.iloc[-1]["review_id"],
                        "longitude_min": page["longitude"].min(),
                        "longitude_max": page["longitude"].max(),
                        "latitude_min": page["latitude"].min(),
                        "latitude_max": page["latitude"].max(),
                        "relative_path": str(destination.relative_to(ROOT)),
                    }
                )
    return pd.concat(review_rows, ignore_index=True), sheet_rows


def write_outputs(review: pd.DataFrame, sheets: list[dict[str, object]]) -> None:
    review = review.rename(columns={"CITY": "municipality_code"})
    review["municipality"] = review["municipality_code"].map(
        {code: values[0] for code, values in FOCAL_AREAS.items()}
    )
    review["screening_status"] = "unreviewed"
    review["collapse_candidate"] = "unknown"
    review["visible_structural_damage"] = "unknown"
    review["view_obstruction"] = "unknown"
    review["reviewer"] = ""
    review["reviewed_at"] = ""
    review["notes"] = ""
    fields = [
        "review_id",
        "municipality_code",
        "municipality",
        "photo_type",
        "contact_sheet_page",
        "panel_position",
        "layer_id",
        "photo_number",
        "captured_at",
        "longitude",
        "latitude",
        "thumbnail_path",
        "full_photo_path",
        "screening_status",
        "collapse_candidate",
        "visible_structural_damage",
        "view_obstruction",
        "reviewer",
        "reviewed_at",
        "notes",
    ]
    review[fields].to_csv(REVIEW_INDEX_PATH, index=False, quoting=csv.QUOTE_MINIMAL)
    pd.DataFrame(sheets).to_csv(SHEET_MANIFEST_PATH, index=False)

    counts = (
        review.groupby(["municipality", "photo_type"], sort=False)
        .size()
        .unstack(fill_value=0)
    )
    lines = [
        "# GSI focal-area imagery triage package",
        "",
        "This package supports manual screening of post-earthquake aerial photography.",
        "A camera-centre location is not an image footprint or a confirmed damage location.",
        "",
        "## Contents",
        "",
        "- `contact_sheets/`: JPEG contact sheets with 30 thumbnails per page.",
        "- `contact_sheet_manifest.csv`: page extents and review-ID ranges.",
        "- `focal_imagery_review_index.csv`: one row per focal photo with paths to the",
        "  thumbnail and full-resolution file plus blank review fields.",
        "- Downstream priority outputs are generated by",
        "  `src/exp/rank_gsi_imagery_population_priority.py`.",
        "",
        "## Counts",
        "",
        "| Municipality | Vertical | Oblique | Total |",
        "|---|---:|---:|---:|",
    ]
    for municipality in [values[0] for values in FOCAL_AREAS.values()]:
        vertical = int(counts.loc[municipality, "vertical"])
        oblique = int(counts.loc[municipality, "oblique"])
        lines.append(f"| {municipality} | {vertical} | {oblique} | {vertical + oblique} |")
    lines.extend(
        [
            "",
            "## Review coding",
            "",
            "Set `screening_status` to `reviewed` after inspection. Code the three evidence",
            "fields conservatively as `yes`, `no`, or `uncertain`; keep `unknown` until reviewed.",
            "Use `collapse_candidate=yes` only for a visually plausible candidate that should be",
            "checked in the full-resolution image. It is not a confirmed earthquake attribution.",
            "",
        ]
    )
    README_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    focal = load_focal_photos()
    review, sheets = build_sheets(focal)
    write_outputs(review, sheets)
    print(f"Focal photos indexed: {len(review):,}")
    print(f"Contact sheets created: {len(sheets):,}")
    print(f"Saved {REVIEW_INDEX_PATH.relative_to(ROOT)}")
    print(f"Saved {SHEET_MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Saved {README_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
