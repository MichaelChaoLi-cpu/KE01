#!/usr/bin/env python3
"""Rank focal GSI photos for review using nearby older-population exposure."""

from __future__ import annotations

import math
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MultipleLocator
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
TRIAGE_DIR = ROOT / "data/exp/gsi-imagery/triage"
REVIEW_INDEX_PATH = TRIAGE_DIR / "focal_imagery_review_index.csv"
GROUP_PATH = (
    ROOT / "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet"
)
BOUNDARY_PATH = (
    ROOT
    / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
OUTPUT_PATH = TRIAGE_DIR / "focal_imagery_priority_scores.csv"
TOP50_PATH = TRIAGE_DIR / "top50_priority_review.csv"
TOP50_SHEET_DIR = TRIAGE_DIR / "top50_contact_sheets"
MAP_PATH = TRIAGE_DIR / "top50_population_exposure_priority_map.png"
METHOD_PATH = TRIAGE_DIR / "priority_method.md"

MAP_CRS = "EPSG:6670"
BUFFER_METERS = 750
FOCAL_AREAS = {
    "202": "Yatsushiro",
    "213": "Uki",
    "468": "Hikawa",
}
WEIGHTS = {
    "older_population": 0.45,
    "older_share": 0.20,
    "total_population": 0.15,
    "visibility": 0.15,
    "geometry_reliability": 0.05,
}


def image_metrics(path: Path) -> tuple[float, float, float, float]:
    """Return brightness, contrast, cloud proxy, and edge strength."""
    with Image.open(path) as source:
        rgb_image = ImageOps.contain(source.convert("RGB"), (160, 160))
        rgb = np.asarray(rgb_image, dtype=np.float32) / 255.0
        gray_image = ImageOps.grayscale(rgb_image)
        gray = np.asarray(gray_image, dtype=np.float32) / 255.0
        edges = np.asarray(
            gray_image.filter(ImageFilter.FIND_EDGES), dtype=np.float32
        ) / 255.0
    brightness = float(gray.mean())
    contrast = float(gray.std())
    channel_range = rgb.max(axis=2) - rgb.min(axis=2)
    cloud_proxy = float(((gray > 0.78) & (channel_range < 0.15)).mean())
    if min(edges.shape) > 8:
        edges = edges[4:-4, 4:-4]
    edge_strength = float(edges.mean())
    return brightness, contrast, cloud_proxy, edge_strength


def add_image_metrics(review: pd.DataFrame) -> pd.DataFrame:
    metrics = [image_metrics(ROOT / path) for path in review["thumbnail_path"]]
    output = review.copy()
    output[[
        "image_brightness",
        "image_contrast",
        "cloud_obstruction_proxy",
        "edge_strength",
    ]] = pd.DataFrame(metrics, index=output.index)
    contrast_rank = output["image_contrast"].rank(pct=True, method="average")
    edge_rank = output["edge_strength"].rank(pct=True, method="average")
    cloud_clear = 1.0 - np.clip(output["cloud_obstruction_proxy"] / 0.50, 0, 1)
    output["visibility_score"] = (
        0.35 * contrast_rank + 0.35 * edge_rank + 0.30 * cloud_clear
    ).clip(0, 1)
    output["visibility_class"] = pd.cut(
        output["visibility_score"],
        bins=[-np.inf, 0.40, 0.67, np.inf],
        labels=["low", "medium", "high"],
    ).astype("string")
    return output


def add_nearby_population(review: pd.DataFrame) -> pd.DataFrame:
    points = gpd.GeoDataFrame(
        review.copy(),
        geometry=gpd.points_from_xy(review["longitude"], review["latitude"]),
        crs=4326,
    ).to_crs(MAP_CRS)
    groups = gpd.read_parquet(GROUP_PATH).to_crs(MAP_CRS)
    groups = groups.loc[
        groups["Total Population"].notna() & groups["Population Age 65+"].notna()
    ].copy()
    groups["group_area_m2"] = groups.geometry.area
    spatial_index = groups.sindex

    nearby_total: list[float] = []
    nearby_older: list[float] = []
    group_counts: list[int] = []
    for point in points.geometry:
        buffer = point.buffer(BUFFER_METERS)
        candidates = list(spatial_index.query(buffer, predicate="intersects"))
        if not candidates:
            nearby_total.append(0.0)
            nearby_older.append(0.0)
            group_counts.append(0)
            continue
        local = groups.iloc[candidates]
        fractions = local.geometry.intersection(buffer).area / local["group_area_m2"]
        nearby_total.append(float((local["Total Population"].astype(float) * fractions).sum()))
        nearby_older.append(float((local["Population Age 65+"].astype(float) * fractions).sum()))
        group_counts.append(len(local))

    output = pd.DataFrame(points.drop(columns="geometry"))
    output["population_buffer_m"] = BUFFER_METERS
    output["nearby_total_population_est"] = nearby_total
    output["nearby_population_age_65_plus_est"] = nearby_older
    output["nearby_population_age_65_plus_share_est"] = np.divide(
        output["nearby_population_age_65_plus_est"],
        output["nearby_total_population_est"],
        out=np.zeros(len(output), dtype=float),
        where=output["nearby_total_population_est"].to_numpy() > 0,
    )
    output["intersecting_disclosure_groups"] = group_counts
    return output


def add_priority_score(review: pd.DataFrame) -> pd.DataFrame:
    output = review.copy()
    output["older_population_component"] = output[
        "nearby_population_age_65_plus_est"
    ].rank(pct=True, method="average")
    output["older_share_component"] = output[
        "nearby_population_age_65_plus_share_est"
    ].rank(pct=True, method="average")
    output["total_population_component"] = output[
        "nearby_total_population_est"
    ].rank(pct=True, method="average")
    output["visibility_component"] = output["visibility_score"]
    output["geometry_reliability_component"] = output["photo_type"].map(
        {"vertical": 1.0, "oblique": 0.80}
    )
    output["priority_score"] = 100 * sum(
        WEIGHTS[name] * output[f"{name}_component"] for name in WEIGHTS
    )
    output = output.sort_values(
        ["priority_score", "nearby_population_age_65_plus_est", "review_id"],
        ascending=[False, False, True],
    ).reset_index(drop=True)
    output["global_priority_rank"] = np.arange(1, len(output) + 1)
    output["municipality_priority_rank"] = (
        output.groupby("municipality")["priority_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    return output


def image_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    properties = font_manager.FontProperties(
        family="DejaVu Sans", weight="bold" if bold else "normal"
    )
    return ImageFont.truetype(font_manager.findfont(properties), size=size)


def build_top50_sheets(top50: pd.DataFrame) -> list[Path]:
    TOP50_SHEET_DIR.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    columns, rows_per_page = 5, 5
    card_width, card_height = 260, 390
    margin, title_height = 22, 110
    title_font = image_font(25, bold=True)
    subtitle_font = image_font(15)
    card_title_font = image_font(13, bold=True)
    card_text_font = image_font(12)

    for page_number, start in enumerate(range(0, len(top50), 25), start=1):
        page = top50.iloc[start : start + 25]
        sheet = Image.new(
            "RGB",
            (
                margin * 2 + columns * card_width,
                title_height + rows_per_page * card_height + margin,
            ),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        draw.text(
            (margin, 16),
            "Top-50 population-exposure imagery review",
            font=title_font,
            fill="#102A43",
        )
        draw.text(
            (margin, 55),
            f"Page {page_number}/2 | Priority rank is for screening, not confirmed damage",
            font=subtitle_font,
            fill="#46515A",
        )
        for position, (_, item) in enumerate(page.iterrows()):
            column = position % columns
            row = position // columns
            x = margin + column * card_width
            y = title_height + row * card_height
            draw.rounded_rectangle(
                (x + 4, y + 4, x + card_width - 5, y + card_height - 5),
                radius=6,
                fill="#F7F9FA",
                outline="#A9B3BA",
                width=1,
            )
            image_box = (x + 9, y + 9, x + card_width - 9, y + 290)
            with Image.open(ROOT / item["thumbnail_path"]) as source:
                thumbnail = ImageOps.contain(
                    source.convert("RGB"),
                    (image_box[2] - image_box[0], image_box[3] - image_box[1]),
                    method=Image.Resampling.LANCZOS,
                )
            paste_x = image_box[0] + (image_box[2] - image_box[0] - thumbnail.width) // 2
            paste_y = image_box[1] + (image_box[3] - image_box[1] - thumbnail.height) // 2
            sheet.paste(thumbnail, (paste_x, paste_y))
            draw.text(
                (x + 10, y + 296),
                f"#{int(item['global_priority_rank']):02d}  {item['review_id']}  S{item['priority_score']:.1f}",
                font=card_title_font,
                fill="#102A43",
            )
            draw.text(
                (x + 10, y + 320),
                f"{item['municipality']} | {item['photo_type'][0].upper()} | vis. {item['visibility_class']}",
                font=card_text_font,
                fill="#374957",
            )
            draw.text(
                (x + 10, y + 342),
                f"Nearby pop. {item['nearby_total_population_est']:.0f}; age 65+ {item['nearby_population_age_65_plus_est']:.0f}",
                font=card_text_font,
                fill="#374957",
            )
            draw.text(
                (x + 10, y + 363),
                f"{float(item['longitude']):.5f}E, {float(item['latitude']):.5f}N",
                font=card_text_font,
                fill="#374957",
            )
        destination = TOP50_SHEET_DIR / f"top50_priority_p{page_number:02d}.jpg"
        sheet.save(destination, format="JPEG", quality=93, optimize=True)
        outputs.append(destination)
    return outputs


def make_map(scores: pd.DataFrame, top50: pd.DataFrame) -> None:
    boundaries = gpd.read_file(
        BOUNDARY_PATH, columns=["CITY", "CITY_NAME", "geometry"]
    ).to_crs(4326)
    boundaries["CITY"] = boundaries["CITY"].astype(str).str.zfill(3)
    focal = boundaries.loc[boundaries["CITY"].isin(FOCAL_AREAS)].dissolve(
        by=["CITY", "CITY_NAME"], as_index=False
    )

    fig, ax = plt.subplots(figsize=(9.5, 9.0))
    focal.plot(ax=ax, color="#F5F7F8", edgecolor="#52636F", linewidth=1.0, zorder=1)
    ax.scatter(
        scores["longitude"], scores["latitude"], s=9, color="#AAB4BB", alpha=0.38,
        linewidths=0, zorder=2,
    )
    points = ax.scatter(
        top50["longitude"], top50["latitude"],
        c=top50["priority_score"], cmap="plasma", s=45,
        edgecolors="white", linewidths=0.55, zorder=3,
    )
    for item in top50.head(10).itertuples(index=False):
        ax.annotate(
            f"#{item.global_priority_rank}",
            (item.longitude, item.latitude), xytext=(4, 4), textcoords="offset points",
            fontsize=7, color="#18242C", zorder=4,
        )
    for item in focal.itertuples(index=False):
        point = item.geometry.representative_point()
        ax.text(
            point.x, point.y, FOCAL_AREAS[item.CITY], ha="center", va="center",
            fontsize=9, color="#102A43", weight="bold", zorder=5,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.76, "pad": 1.5},
        )
    bounds = focal.total_bounds
    xpad = (bounds[2] - bounds[0]) * 0.07
    ypad = (bounds[3] - bounds[1]) * 0.07
    ax.set_xlim(bounds[0] - xpad, bounds[2] + xpad)
    ax.set_ylim(bounds[1] - ypad, bounds[3] + ypad)
    middle_latitude = float((bounds[1] + bounds[3]) / 2)
    ax.set_aspect(1 / math.cos(math.radians(middle_latitude)))
    ax.xaxis.set_major_locator(MultipleLocator(0.05))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.2f}°E"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.2f}°N"))
    ax.grid(color="#80909A", linewidth=0.45, linestyle=(0, (3, 4)), alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color("#303A40")
        spine.set_linewidth(0.9)
    ax.tick_params(labelsize=8, colors="#46515A")
    colorbar = fig.colorbar(points, ax=ax, fraction=0.035, pad=0.025)
    colorbar.set_label("Population-exposure review priority score", fontsize=9)
    handles = [
        Line2D([0], [0], marker="o", linestyle="", color="#AAB4BB", markersize=5,
               label="All focal camera centres"),
        Line2D([0], [0], marker="o", linestyle="", markerfacecolor="#D24B9B",
               markeredgecolor="white", markersize=7, label="Top-50 review batch"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize=8, framealpha=0.94)
    ax.set_title(
        "Top-50 Aerial Images for Older-Population Exposure Review",
        loc="left", fontsize=14, pad=12,
    )
    fig.text(
        0.08, 0.025,
        "Priority combines nearby 2020 Census older population, older share, total population, "
        "thumbnail usability, and camera-geometry reliability. Camera centres are not image footprints.",
        fontsize=8, color="#46515A", ha="left",
    )
    fig.subplots_adjust(left=0.09, right=0.93, top=0.92, bottom=0.09)
    fig.savefig(MAP_PATH, dpi=240, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def write_method(scores: pd.DataFrame, top50: pd.DataFrame) -> None:
    counts = top50.groupby(["municipality", "photo_type"]).size().unstack(fill_value=0)
    lines = [
        "# Population-exposure imagery review priority",
        "",
        "## Purpose",
        "",
        "Rank the 1,064 focal-area aerial photographs for manual review. A high score is not",
        "evidence of housing collapse; it indicates that an image should be reviewed early.",
        "",
        "## Score",
        "",
        "- 45%: percentile rank of estimated population age 65+ within 750 m of the camera centre.",
        "- 20%: percentile rank of the estimated age-65+ population share within 750 m.",
        "- 15%: percentile rank of estimated total population within 750 m.",
        "- 15%: thumbnail visibility proxy using contrast, edge strength, and bright low-saturation",
        "  pixels as a possible cloud-obstruction indicator.",
        "- 5%: camera-geometry reliability (1.0 vertical; 0.8 oblique).",
        "",
        "Population counts are area-weighted from the official disclosure-group polygons that",
        "intersect each 750 m buffer. This assumes uniform population within each disclosure group",
        "and is suitable only for prioritization. Oblique camera centres may be displaced from the",
        "visible ground area. Thumbnail visibility metrics can mistake bright roofs, greenhouses,",
        "water, or haze for cloud and require human review.",
        "",
        "## Top-50 composition",
        "",
        "| Municipality | Vertical | Oblique | Total |",
        "|---|---:|---:|---:|",
    ]
    for municipality in ["Yatsushiro", "Uki", "Hikawa"]:
        vertical = int(counts.get("vertical", pd.Series(dtype=int)).get(municipality, 0))
        oblique = int(counts.get("oblique", pd.Series(dtype=int)).get(municipality, 0))
        lines.append(f"| {municipality} | {vertical} | {oblique} | {vertical + oblique} |")
    lines.extend(
        [
            "",
            f"The full score table contains {len(scores):,} photographs. The initial review batch",
            f"contains {len(top50):,} photographs.",
            "",
        ]
    )
    METHOD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    review = pd.read_csv(
        REVIEW_INDEX_PATH,
        dtype={"municipality_code": "string", "photo_number": "string"},
    )
    if len(review) != 1_064 or not review["review_id"].is_unique:
        raise ValueError("The focal review index is incomplete or contains duplicate IDs")
    scores = add_image_metrics(review)
    scores = add_nearby_population(scores)
    scores = add_priority_score(scores)
    top50 = scores.head(50).copy()

    scores.to_csv(OUTPUT_PATH, index=False)
    top50.to_csv(TOP50_PATH, index=False)
    sheets = build_top50_sheets(top50)
    make_map(scores, top50)
    write_method(scores, top50)

    print(f"Ranked focal photos: {len(scores):,}")
    print(f"Top review batch: {len(top50):,}")
    print(f"Top-50 contact sheets: {len(sheets)}")
    print("Top-50 by municipality:")
    print(top50["municipality"].value_counts().to_string())
    print(f"Saved {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Saved {TOP50_PATH.relative_to(ROOT)}")
    print(f"Saved {MAP_PATH.relative_to(ROOT)}")
    print(f"Saved {METHOD_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
