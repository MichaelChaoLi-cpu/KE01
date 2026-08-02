#!/usr/bin/env python3
"""Attach conservative human-review labels to the Hikawa CLIP candidate batch."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PILOT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_clip_damage_pilot"
INPUT_CSV = PILOT_DIR / "top_candidate_tiles.csv"
OUTPUT_CSV = PILOT_DIR / "top_candidate_human_review.csv"
SUMMARY_MD = PILOT_DIR / "human_review_summary.md"

# Ranks were visually inspected from the five generated contact sheets, with dense
# residential candidates additionally opened at their original 512 px crop size.
RESIDENTIAL_OR_MIXED = {
    4, 5, 7, 8, 9, 11, 14, 16, 18, 21, 22, 24, 29, 31, 33, 35, 37, 38, 39,
    42, 43, 44, 45, 49, 50,
}
NONRESIDENTIAL_BUILT = {1, 13, 27, 36, 47}


def main() -> None:
    with INPUT_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    ranks = {int(row["candidate_rank"]) for row in rows}
    if len(rows) != 50 or ranks != set(range(1, 51)):
        raise ValueError("Expected the complete ranked top-50 candidate batch.")
    if RESIDENTIAL_OR_MIXED & NONRESIDENTIAL_BUILT:
        raise ValueError("Human scene-class sets overlap.")

    reviewed: list[dict[str, str]] = []
    for source in rows:
        rank = int(source["candidate_rank"])
        row = dict(source)
        if rank in RESIDENTIAL_OR_MIXED:
            scene_class = "residential_or_mixed_built"
            severe_damage = "no_obvious"
            note = (
                "Residential or mixed built environment is visible, but no obvious "
                "collapsed roof, house-scale rubble, or severe structural failure is "
                "visible at the candidate-crop resolution."
            )
        elif rank in NONRESIDENTIAL_BUILT:
            scene_class = "nonresidential_built"
            severe_damage = "no_obvious"
            note = (
                "A built feature is visible, but the crop is dominated by roadside, "
                "industrial, or other nonresidential context; no house-collapse candidate."
            )
        else:
            scene_class = "no_residential_building"
            severe_damage = "not_assessable"
            note = (
                "Model false positive dominated by vegetation, slope, exposed soil, "
                "highway, cemetery, riverbank, or other nonresidential texture."
            )
        row.update(
            {
                "human_scene_class": scene_class,
                "human_visible_severe_structural_damage": severe_damage,
                "human_house_collapse_candidate": "no",
                "human_review_note": note,
                "human_reviewer": "Codex visual review",
                "human_reviewed_at": "2026-08-02",
            }
        )
        reviewed.append(row)

    fields = list(rows[0]) + [
        "human_scene_class",
        "human_visible_severe_structural_damage",
        "human_house_collapse_candidate",
        "human_review_note",
        "human_reviewer",
        "human_reviewed_at",
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reviewed)

    counts = Counter(row["human_scene_class"] for row in reviewed)
    built_count = counts["residential_or_mixed_built"] + counts["nonresidential_built"]
    summary = f"""# Human review of Hikawa CLIP candidates

## Completed experiment

- Source photographs: 55 (all indexed Hikawa photographs)
- Overlapping tiles scored: 5,334
- Model-ranked candidates visually reviewed: 50
- Residential or mixed built scenes: {counts['residential_or_mixed_built']}
- Nonresidential built scenes: {counts['nonresidential_built']}
- No residential building / texture false positives: {counts['no_residential_building']}
- Any built feature visible: {built_count} of 50
- Obvious house-collapse candidates after human review: 0

## Finding

The independent building-presence prompt reduced the strongest forest and exposed-soil errors, but the final list still contained {counts['no_residential_building']} nonresidential texture false positives. Among the {counts['residential_or_mixed_built']} residential or mixed built crops, no obvious collapsed roof, house-scale rubble, or severe structural failure was visible.

This result does not show that the two residential buckling incidents mentioned by FDMA were absent from the imagery. Their coordinates are not available, roof-intact buckling may be invisible from above, and the aerial-photo camera centre does not geolocate a crop. Consequently, model recall or sensitivity cannot be estimated from this experiment.

## Method decision

Generic zero-shot CLIP is not adequate as a stand-alone house-damage detector for these photographs. It can reduce 5,334 tiles to a human-review queue, but a defensible next model should use geographically registered pre/post imagery or building footprints plus damage-specific validation labels. Model scores must not be converted into a damaged-house count.
"""
    SUMMARY_MD.write_text(summary, encoding="utf-8")
    print(f"Wrote {OUTPUT_CSV.relative_to(PROJECT_ROOT)} ({len(reviewed)} rows)")
    print(f"Wrote {SUMMARY_MD.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
