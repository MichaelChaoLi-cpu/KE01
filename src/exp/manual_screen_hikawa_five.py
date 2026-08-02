#!/usr/bin/env python3
"""Document a conservative visual screen of five Hikawa post-event photos."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_CSV = PROJECT_ROOT / "data/exp/gsi-imagery/triage/focal_imagery_review_index.csv"
OUTPUT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_prepost_manual_check"

REVIEWS = [
    {
        "review_id": "HIK-V-0013",
        "scene": "高速互通、丘陵、农地与住宅",
        "post_event_screen": "未见成片屋顶消失、大型瓦砾场或道路被建筑残骸阻断",
        "historical_support": "2023 年度正射影像部分覆盖；高速互通可确认同一场景，但未达到单栋配准",
        "screening_class": "未发现明显大范围倒塌",
        "priority": "中",
        "limitation": "灾后图分辨率较低；不能排除单栋或局部损坏",
        "figure_note": "No obvious large debris field; 2023 partial context",
    },
    {
        "review_id": "HIK-V-0014",
        "scene": "河流、农地与密集住宅",
        "post_event_screen": "多数屋顶轮廓连续；中上部存在白色云/烟状遮挡，来源无法由单张照片确定",
        "historical_support": "2018–2025 年度图层中心点无覆盖",
        "screening_class": "局部遮挡，需灾前影像复核",
        "priority": "高",
        "limitation": "遮挡区域及单栋建筑无法判断",
        "figure_note": "Residential scene; cloud/smoke-like obscuration",
    },
    {
        "review_id": "HIK-V-0018",
        "scene": "河流、平原农地、山麓与密集住宅",
        "post_event_screen": "未见明显成片倒塌或连续瓦砾带；主要道路和住宅纹理总体连续",
        "historical_support": "2018–2025 年度图层中心点无覆盖",
        "screening_class": "未发现明显大范围倒塌",
        "priority": "高",
        "limitation": "住宅数量多，仍需高分辨率灾前单幅航拍逐区核对",
        "figure_note": "Dense housing; no obvious large collapse pattern",
    },
    {
        "review_id": "HIK-V-0022",
        "scene": "高速公路、林地、果园与少量聚落",
        "post_event_screen": "可见多处裸地、林道和施工/整地状纹理，但缺少建筑倒塌形态",
        "historical_support": "2018–2025 年度图层中心点无覆盖",
        "screening_class": "疑似土地整理或林业变化，非房屋倒塌候选",
        "priority": "低",
        "limitation": "裸地成因需历史影像确认；住宅暴露较少",
        "figure_note": "Earthworks/forestry patterns; low housing relevance",
    },
    {
        "review_id": "HIK-V-0034",
        "scene": "高速公路、山地、山麓聚落与农地",
        "post_event_screen": "山地存在零散裸土切口；山麓住宅区未见明显成片瓦砾",
        "historical_support": "2020 年度正射影像部分覆盖；GPS 几何指向同一走廊，自动精配准失败",
        "screening_class": "未发现明显大范围倒塌；裸土需复核",
        "priority": "中",
        "limitation": "历史底图空洞较大，无法进行可靠像素差分",
        "figure_note": "Scattered bare soil; no obvious residential debris field",
    },
]


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        indexed = {row["review_id"]: row for row in csv.DictReader(handle)}

    rows = []
    figure, axes = plt.subplots(2, 3, figsize=(16, 11), constrained_layout=True)
    for axis, review in zip(axes.flat, REVIEWS, strict=False):
        source = indexed[review["review_id"]]
        path = PROJECT_ROOT / source["full_photo_path"]
        with Image.open(path) as opened:
            image = opened.convert("RGB")
            image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
            axis.imshow(image)
        axis.set_title(f"{review['review_id']}\n{review['figure_note']}", fontsize=10)
        axis.axis("off")
        rows.append(
            {
                **{key: value for key, value in review.items() if key != "figure_note"},
                "longitude": source["longitude"],
                "latitude": source["latitude"],
                "source_post_path": source["full_photo_path"],
            }
        )
    axes.flat[-1].axis("off")
    figure.suptitle(
        "Hikawa 2026 post-event visual screen — screening only, not damage labels",
        fontsize=15,
    )
    figure.savefig(OUTPUT_DIR / "five_photo_manual_screen.png", dpi=180, facecolor="white")
    plt.close(figure)

    fields = list(rows[0])
    with (OUTPUT_DIR / "manual_review.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    readme = """# Hikawa five-photo manual screen

This is a conservative visual screening record, not a building-damage inventory.
The reviewer checked whether each 2026 photograph contains an obvious large,
spatially coherent collapse signature such as a broad debris field, many missing
roof planes, or roads blocked by structural debris. Absence of such a visible
signature does not establish absence of damage.

Main screening result: none of the five photographs shows an unambiguous large-area
residential-collapse pattern. HIK-V-0014 and HIK-V-0018 remain the highest-priority
residential scenes for historical single-photo comparison. HIK-V-0014 also contains
a white cloud/smoke-like obscuration whose source cannot be determined from this
image alone.

See `manual_review.csv` for the photo-by-photo audit trail and
`five_photo_manual_screen.png` for the visual contact sheet.
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")
    print(f"Wrote {len(rows)} review rows to {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
