#!/usr/bin/env python3
"""Compile the completed visual review of the top-50 GSI pilot batch.

The source review queue remains unchanged.  This script writes a separate,
auditable result table and a short summary of the pilot findings.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRIAGE_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/triage"
PILOT_DIR = TRIAGE_DIR / "pilot_review"
INPUT_CSV = TRIAGE_DIR / "top50_priority_review.csv"
ASSET_CSV = PILOT_DIR / "review_asset_manifest.csv"
OUTPUT_CSV = PILOT_DIR / "top50_pilot_review_results.csv"
SUMMARY_MD = PILOT_DIR / "pilot_summary.md"

REVIEWER = "Codex visual pilot"
REVIEWED_AT = "2026-08-02"
INTERPRETATION_LIMIT = (
    "Post-event-only visual screening; absence of an obvious candidate is not "
    "evidence of no damage and does not establish earthquake attribution."
)


SCENE_DESCRIPTIONS = {
    1: "Mixed residential, agricultural, and mountain terrain; clear view.",
    2: "Mixed residential, port, and mountain terrain; clear view.",
    3: "Mixed residential, agricultural, and mountain terrain; clear view.",
    4: "Mixed residential, agricultural, and urban terrain; localized haze/cloud.",
    5: "Dense residential and mixed terrain; small cloud; excavation appears pre-existing.",
    6: "Mixed agricultural and residential terrain; clear view.",
    7: "Dense urban, residential, and industrial terrain; clear view.",
    8: "Mountain-dominated low-resolution oblique view; residential structures not assessable.",
    9: "Mixed agricultural and residential terrain; clear view.",
    10: "Mixed urban, agricultural, and forest terrain; localized haze.",
    11: "Mixed rural and residential high-resolution oblique view; clear.",
    12: "Mountain-dominated low-resolution oblique view with cloud.",
    13: "Residential and urban terrain; minor haze at most.",
    14: "Residential and urban terrain; clear view.",
    15: "Residential and urban terrain; clear view.",
    16: "Residential and urban terrain; clear view.",
    17: "Mixed residential and mountain terrain; small cloud; excavation appears pre-existing.",
    18: "Mixed urban and agricultural terrain; clear view.",
    19: "Mixed urban and agricultural terrain; clear view.",
    20: "Mixed urban, agricultural, and forest terrain; clear view.",
    21: "Mixed residential, agricultural, and solar-facility terrain; clear view.",
    22: "Mountain-dominated low-resolution oblique view; residential structures not assessable.",
    23: "Mixed residential low-resolution oblique view; clear but structurally limited.",
    24: "Residential and mixed urban terrain; clear view.",
    25: "Agriculture-dominated terrain with settlement; clear view.",
    26: "Urban and residential terrain; clear view.",
    27: "Port and mountain terrain with a narrow settlement strip; low residential relevance.",
    28: "Agriculture and greenhouses with a small settlement; low residential relevance.",
    29: "Mixed agricultural and urban terrain; localized cloud over fields.",
    30: "Residential and urban low-resolution oblique view; clear but structurally limited.",
    31: "Urban and residential terrain; clear view.",
    32: "Agriculture-dominated terrain with a small settlement; low residential relevance.",
    33: "Urban and residential terrain; clear view.",
    34: "Agriculture, greenhouses, and town edge; cloud at the eastern side.",
    35: "Urban and residential terrain; clear view.",
    36: "Port, agricultural, and industrial terrain with little residential coverage.",
    37: "Urban and residential terrain; clear view.",
    38: "Mountain-dominated low-resolution oblique view; residential structures not assessable.",
    39: "Mountain-dominated low-resolution oblique view with cloud.",
    40: "Mixed industrial, agricultural, and urban terrain; clear view.",
    41: "Mixed river, residential, and mountain terrain; clear view.",
    42: "Urban, agricultural, and residential terrain; clear view.",
    43: "Mixed rural and residential high-resolution oblique view; clear.",
    44: "Urban and residential low-resolution oblique view with partial cloud.",
    45: "Mixed residential low-resolution oblique view; clear but structurally limited.",
    46: "Urban, residential, river, and mountain terrain; localized cloud.",
    47: "Mountain-dominated low-resolution oblique view with a small valley settlement and cloud.",
    48: "Urban and mixed terrain; clear view.",
    49: "Mixed agricultural, residential, and mountain terrain; clear view.",
    50: "Mixed urban and residential low-resolution oblique view; clear but structurally limited.",
}

RESIDENTIAL_SCENES = {
    7, 13, 14, 15, 16, 24, 26, 30, 31, 33, 35, 37, 42, 44, 45, 46, 48, 50
}
IRRELEVANT_SCENES = {8, 12, 22, 38, 39}
NONRESIDENTIAL_SCENES = {36}
LOW_RESIDENTIAL_VISIBILITY = {27, 28, 32, 34, 47}
PARTIAL_OBSTRUCTION = {4, 5, 10, 12, 17, 29, 34, 39, 44, 46, 47}
LOW_RESOLUTION_OBLIQUE = {8, 12, 22, 23, 30, 38, 39, 44, 45, 47, 50}
STRUCTURAL_NOT_ASSESSABLE = LOW_RESOLUTION_OBLIQUE | NONRESIDENTIAL_SCENES


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def scene_relevance(rank: int) -> str:
    if rank in RESIDENTIAL_SCENES:
        return "residential"
    if rank in IRRELEVANT_SCENES:
        return "irrelevant"
    if rank in NONRESIDENTIAL_SCENES:
        return "nonresidential"
    return "mixed"


def residential_visibility(rank: int) -> str:
    if rank in IRRELEVANT_SCENES or rank in NONRESIDENTIAL_SCENES:
        return "not_applicable"
    if rank in LOW_RESIDENTIAL_VISIBILITY:
        return "low"
    if rank in RESIDENTIAL_SCENES:
        return "high"
    return "medium"


def main() -> None:
    review_rows = read_rows(INPUT_CSV)
    asset_rows = read_rows(ASSET_CSV)
    assets = {row["review_id"]: row for row in asset_rows}

    if len(review_rows) != 50 or len({row["review_id"] for row in review_rows}) != 50:
        raise ValueError("Expected exactly 50 unique rows in the pilot queue.")
    if set(assets) != {row["review_id"] for row in review_rows}:
        raise ValueError("Review queue and asset manifest do not contain the same review IDs.")

    result_rows: list[dict[str, str]] = []
    for source in review_rows:
        rank = int(source["global_priority_rank"])
        asset = assets[source["review_id"]]
        structural_damage = "uncertain" if rank in STRUCTURAL_NOT_ASSESSABLE else "no"
        confidence = "low" if rank in STRUCTURAL_NOT_ASSESSABLE else "medium"
        detail_reviewed = "yes" if asset["detail_page_path"] else "no"

        row = dict(source)
        row.update(
            {
                "screening_status": "reviewed",
                "collapse_candidate": "no",
                "visible_structural_damage": structural_damage,
                "view_obstruction": "partial" if rank in PARTIAL_OBSTRUCTION else "none",
                "reviewer": REVIEWER,
                "reviewed_at": REVIEWED_AT,
                "notes": (
                    SCENE_DESCRIPTIONS[rank]
                    + " No obvious severe structural damage or localized collapse candidate "
                    + "was visible at the pilot review resolution."
                ),
                "scene_relevance": scene_relevance(rank),
                "residential_visibility": residential_visibility(rank),
                "review_confidence": confidence,
                "candidate_tile": "",
                "overview_page_path": asset["overview_page_path"],
                "detail_page_path": asset["detail_page_path"],
                "detail_page_reviewed": detail_reviewed,
                "interpretation_limit": INTERPRETATION_LIMIT,
            }
        )
        result_rows.append(row)

    result_rows.sort(key=lambda row: int(row["global_priority_rank"]))
    extra_fields = [
        "scene_relevance",
        "residential_visibility",
        "review_confidence",
        "candidate_tile",
        "overview_page_path",
        "detail_page_path",
        "detail_page_reviewed",
        "interpretation_limit",
    ]
    fieldnames = list(review_rows[0]) + extra_fields
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(result_rows)

    relevance_counts = Counter(row["scene_relevance"] for row in result_rows)
    obstruction_counts = Counter(row["view_obstruction"] for row in result_rows)
    structural_counts = Counter(row["visible_structural_damage"] for row in result_rows)
    detail_count = sum(row["detail_page_reviewed"] == "yes" for row in result_rows)
    municipality_counts = Counter(row["municipality"] for row in result_rows)

    summary = f"""# Top-50 population-exposure pilot review summary

## Review coverage

- Review date: {REVIEWED_AT}
- Images screened: {len(result_rows)} of 50
- Overview pages inspected: 13
- Full-image detail grids inspected: {detail_count}
- Municipality composition: Yatsushiro {municipality_counts['Yatsushiro']}, Hikawa {municipality_counts['Hikawa']}, Uki {municipality_counts['Uki']}

## Coding results

| Field | Category | Count |
|---|---|---:|
| Scene relevance | residential | {relevance_counts['residential']} |
| Scene relevance | mixed | {relevance_counts['mixed']} |
| Scene relevance | nonresidential | {relevance_counts['nonresidential']} |
| Scene relevance | irrelevant | {relevance_counts['irrelevant']} |
| View obstruction | none | {obstruction_counts['none']} |
| View obstruction | partial | {obstruction_counts['partial']} |
| Visible structural damage | yes | {structural_counts['yes']} |
| Visible structural damage | no obvious severe damage | {structural_counts['no']} |
| Visible structural damage | uncertain/not assessable | {structural_counts['uncertain']} |
| Collapse candidate | yes | 0 |
| Collapse candidate | no localized candidate | 50 |

## Interpretation

No visually convincing house-collapse candidate was identified in this pilot batch. This is a screening result, not a finding that the imaged areas were undamaged. Eleven low-resolution oblique images and one predominantly nonresidential image were coded `visible_structural_damage=uncertain`; all other `no` codes mean only that no obvious severe structural damage was visible at the available review resolution.

The batch was ranked by nearby older-population exposure and image visibility, not by the probability of building damage. The zero-candidate outcome therefore indicates that population exposure alone is not an efficient damage-candidate detector. A subsequent batch should add independent damage-probability evidence, such as reported damage locations, seismic intensity, or pre/post image change, while retaining older-population exposure for consequence prioritization.

Post-event imagery alone cannot establish whether a visible condition was caused by the earthquake. The detailed row-level coding and paths to each review asset are in `top50_pilot_review_results.csv`.
"""
    SUMMARY_MD.write_text(summary, encoding="utf-8")

    print(f"Wrote {OUTPUT_CSV.relative_to(PROJECT_ROOT)} ({len(result_rows)} rows)")
    print(f"Wrote {SUMMARY_MD.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
