#!/usr/bin/env python3
"""Write conservative visual labels for GSI annotation batch 001."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
BATCH_DIR = ROOT / "data/exp/gsi-imagery/triage/annotation_batches/batch_001_stratified"
QUEUE = BATCH_DIR / "annotation_queue.csv"
RESULTS = BATCH_DIR / "annotation_results.csv"
SUMMARY = BATCH_DIR / "annotation_summary.md"
REVIEWER = "Codex visual review"
REVIEWED_AT = "2026-08-02"


LABELS = {
    "YAT-V-0120": (
        "good",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "medium",
        "A1,B1",
        "Clear vertical view of dense urban, residential, industrial, and agricultural areas; no localized roof collapse, house-scale rubble, or major structural displacement visible. Small cloud affects agricultural area in B3.",
    ),
    "YAT-V-0177": (
        "good",
        "residential",
        "no_obvious_severe",
        "no",
        "medium",
        "A2,B1,B3",
        "Clear vertical view of extensive residential districts on both sides of the river; roofs appear broadly intact and no localized collapse or rubble concentration is visible.",
    ),
    "UKI-V-0127": (
        "good",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "medium",
        "A1,B1",
        "Clear vertical view dominated by forest and agriculture with sparse settlements; no obvious severe structural damage is visible in the residential strips.",
    ),
    "YAT-O-0117": (
        "limited",
        "nonresidential",
        "uncertain",
        "no",
        "low",
        "",
        "Low-resolution oblique view dominated by a waterfront industrial complex; no localized collapse candidate is visible, but residential structural damage is not assessable.",
    ),
    "YAT-O-0143": (
        "limited",
        "mixed_built",
        "uncertain",
        "no",
        "low",
        "",
        "Low-resolution oblique mountain and valley-settlement view; no localized collapse candidate is visible, but individual residential structures are too small for reliable exclusion.",
    ),
    "HIK-O-0010": (
        "limited",
        "mixed_built",
        "uncertain",
        "no",
        "low",
        "",
        "Low-resolution oblique mountain settlement view with small cloud; no localized collapse candidate is visible, but building-level condition is not reliably assessable.",
    ),
    "UKI-V-0225": (
        "limited",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "low",
        "A1,B2",
        "Medium-resolution portrait vertical image of agriculture, forest, and sparse settlements; no obvious severe damage is visible, but small buildings limit confidence.",
    ),
    "HIK-V-0009": (
        "limited",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "low",
        "A2,A3",
        "Medium-resolution portrait vertical image of rural settlements and fields; no obvious severe damage or rubble concentration is visible, with limited building detail.",
    ),
    "HIK-V-0014": (
        "limited",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "medium",
        "A1,A3,B3",
        "High-resolution vertical view of rural settlements and agriculture; visible roofs show no obvious severe damage. Cloud obscures part of A2, so the complete image cannot be assessed.",
    ),
    "HIK-O-0016": (
        "limited",
        "mixed_built",
        "uncertain",
        "no",
        "low",
        "",
        "Low-resolution oblique mountain and valley-settlement view; no localized collapse candidate is visible, but individual buildings are not reliably assessable.",
    ),
    "UKI-O-0009": (
        "good",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "medium",
        "A1,B1,B2",
        "Clear high-resolution oblique view of residential clusters and agricultural land; no localized collapsed roofs, house-scale rubble, or major structural displacement visible.",
    ),
    "UKI-O-0010": (
        "good",
        "mixed_built",
        "no_obvious_severe",
        "no",
        "medium",
        "A3,B2",
        "Clear high-resolution oblique view dominated by agriculture with several residential clusters; no obvious severe structural damage or localized collapse candidate visible.",
    ),
}


def main() -> int:
    queue = pd.read_csv(QUEUE, dtype={"photo_number": "string"})
    annotation_columns = [
        "annotation_status",
        "assessability",
        "scene_class",
        "damage_class",
        "collapse_candidate",
        "confidence",
        "evidence_tile",
        "evidence_note",
        "reviewer",
        "reviewed_at",
        "earthquake_attribution",
    ]
    for column in annotation_columns:
        queue[column] = queue[column].astype("string")
    if set(queue["review_id"]) != set(LABELS):
        raise ValueError("Annotation queue and label dictionary contain different review IDs")

    for review_id, values in LABELS.items():
        assessability, scene, damage, collapse, confidence, tile, note = values
        mask = queue["review_id"].eq(review_id)
        queue.loc[mask, "annotation_status"] = "reviewed"
        queue.loc[mask, "assessability"] = assessability
        queue.loc[mask, "scene_class"] = scene
        queue.loc[mask, "damage_class"] = damage
        queue.loc[mask, "collapse_candidate"] = collapse
        queue.loc[mask, "confidence"] = confidence
        queue.loc[mask, "evidence_tile"] = tile
        queue.loc[mask, "evidence_note"] = note
        queue.loc[mask, "reviewer"] = REVIEWER
        queue.loc[mask, "reviewed_at"] = REVIEWED_AT

    queue.to_csv(RESULTS, index=False)
    assessability = Counter(queue["assessability"])
    scenes = Counter(queue["scene_class"])
    damage = Counter(queue["damage_class"])
    confidence = Counter(queue["confidence"])
    summary = f"""# GSI annotation batch 001 summary

## Coverage

- Review date: {REVIEWED_AT}
- Complete aerial photographs reviewed: {len(queue)}
- Municipalities: Hikawa, Uki, and Yatsushiro
- Sampling: two previously unreviewed photographs per municipality × photo-type stratum

## Results

| Field | Category | Count |
|---|---|---:|
| Assessability | good | {assessability['good']} |
| Assessability | limited | {assessability['limited']} |
| Assessability | not assessable | {assessability['not_assessable']} |
| Scene | residential | {scenes['residential']} |
| Scene | mixed built | {scenes['mixed_built']} |
| Scene | nonresidential | {scenes['nonresidential']} |
| Damage | no obvious severe damage | {damage['no_obvious_severe']} |
| Damage | uncertain | {damage['uncertain']} |
| Damage | possible severe damage | {damage['possible_severe']} |
| Damage | possible collapse | {damage['possible_collapse']} |
| Collapse candidate | yes | {(queue['collapse_candidate'] == 'yes').sum()} |
| Confidence | medium | {confidence['medium']} |
| Confidence | low | {confidence['low']} |

## Interpretation

No localized house-collapse candidate was identified in this batch. Four low-resolution
oblique photographs were coded `damage_class=uncertain`; three additional photographs
had limited confidence because of resolution or partial cloud. The remaining negative
labels mean only that no obvious severe structural damage was visible in the reviewed
post-event image. They do not establish absence of damage or earthquake attribution.

This batch is suitable for audit and screening-method development, but it is not a
balanced training set because it contains no confirmed positive damage examples.
"""
    SUMMARY.write_text(summary, encoding="utf-8")
    print(f"Saved {RESULTS.relative_to(ROOT)} ({len(queue)} rows)")
    print(f"Saved {SUMMARY.relative_to(ROOT)}")
    print("Damage labels:", dict(damage))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
