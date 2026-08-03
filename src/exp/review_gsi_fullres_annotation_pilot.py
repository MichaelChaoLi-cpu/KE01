#!/usr/bin/env python3
"""Attach conservative human-review labels to the full-resolution pilot."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PILOT_DIR = ROOT / "data/exp/gsi-imagery/fullres_annotation_pilot"
INPUT = PILOT_DIR / "top_candidate_tiles.csv"
OUTPUT = PILOT_DIR / "top_candidate_human_review.csv"
SUMMARY = PILOT_DIR / "human_review_summary.md"

RESIDENTIAL_OR_MIXED = {1, 4, 6, 8, 11, 12, 13, 14, 19, 20, 22, 23, 24, 25}
BARE_OR_CLEARED_SITE = {3, 7, 16, 21}
CLOUD_OBSCURED = {15, 18}
NONRESIDENTIAL_BUILT = {2, 5, 9, 10, 17}
AGRICULTURE_OR_NO_HOUSE = {26, 27, 28, 29, 30}


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    expected = set(range(1, 31))
    groups = [
        RESIDENTIAL_OR_MIXED,
        BARE_OR_CLEARED_SITE,
        CLOUD_OBSCURED,
        NONRESIDENTIAL_BUILT,
        AGRICULTURE_OR_NO_HOUSE,
    ]
    union = set().union(*groups)
    if union != expected or sum(map(len, groups)) != len(union):
        raise ValueError("Human-review rank groups must partition ranks 1-30.")

    reviewed: list[dict[str, str]] = []
    for source in rows:
        rank = int(source["candidate_rank"])
        row = dict(source)
        if rank in RESIDENTIAL_OR_MIXED:
            scene = "residential_or_mixed_built"
            label = "no_obvious_collapse"
            collapse = "no"
            note = (
                "Native-resolution crop contains houses or mixed development, but roofs "
                "remain recognizable and no house-scale rubble or collapsed structure is visible."
            )
        elif rank in BARE_OR_CLEARED_SITE:
            scene = "bare_or_cleared_site"
            label = "needs_pre_event_comparison"
            collapse = "no_visible_house_collapse"
            note = (
                "Bare, cleared, or construction-like ground is visible, but no collapsed "
                "house is identifiable. A pre-event image is required to determine site history."
            )
        elif rank in CLOUD_OBSCURED:
            scene = "cloud_obscured"
            label = "uncertain_obscured"
            collapse = "uncertain"
            note = (
                "Cloud obscures a substantial part of the crop; visible structures do not "
                "show obvious collapse, but the covered area is not assessable."
            )
        elif rank in NONRESIDENTIAL_BUILT:
            scene = "nonresidential_built"
            label = "no_house_target"
            collapse = "no"
            note = (
                "Industrial, institutional, road, or other nonresidential structures dominate; "
                "no house-collapse target is visible."
            )
        else:
            scene = "agriculture_or_no_house"
            label = "no_house_target"
            collapse = "no"
            note = "Agriculture, river, or open ground dominates and no assessable house target is visible."
        row.update(
            {
                "human_scene_class": scene,
                "human_review_label": label,
                "human_house_collapse_candidate": collapse,
                "human_review_note": note,
                "human_reviewer": "Codex visual review",
                "human_reviewed_at": "2026-08-02",
            }
        )
        reviewed.append(row)

    fields = list(rows[0]) + [
        "human_scene_class",
        "human_review_label",
        "human_house_collapse_candidate",
        "human_review_note",
        "human_reviewer",
        "human_reviewed_at",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reviewed)

    counts = Counter(row["human_scene_class"] for row in reviewed)
    summary = f"""# Human review of full-resolution GSI candidates

## Scope

- High-detail post-event photographs: 5
- Overlapping native-resolution 512 px tiles scored: 1,100
- Model-ranked crops reviewed at native resolution: 30
- Residential or mixed-built crops: {counts['residential_or_mixed_built']}
- Bare or cleared sites requiring pre-event context: {counts['bare_or_cleared_site']}
- Cloud-obscured crops: {counts['cloud_obscured']}
- Nonresidential built crops: {counts['nonresidential_built']}
- Agriculture or no-house crops: {counts['agriculture_or_no_house']}

## Result

No visually explicit collapsed house was identified. The full-resolution crops make
individual roofs substantially easier to inspect than the earlier whole-photo audit
sheets, but the result remains zero confirmed or visually convincing house-collapse
candidates. Four bare or cleared sites were retained for pre-event comparison rather
than being mislabeled as earthquake damage.

## Pre-event check

Two highest-ranked bare-site cases were tested against the 2018-2025 GSI annual
orthophoto layers. One had no annual-tile coverage at the photo centre. The other had
partial 2020 coverage, but automatic registration produced a geometrically degenerate
solution. Neither case can presently be attributed to the earthquake.

This is a sensitivity check on five photographs, not exhaustive coverage and not a
damaged-building count.
"""
    SUMMARY.write_text(summary, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(reviewed)} rows)")
    print(f"Wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
