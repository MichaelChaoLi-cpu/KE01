#!/usr/bin/env python3
"""Prepare a stratified, previously unreviewed GSI photo annotation batch."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from prepare_gsi_top50_pilot_review import build_detail_page, build_overview_pages


ROOT = Path(__file__).resolve().parents[2]
TRIAGE_DIR = ROOT / "data/exp/gsi-imagery/triage"
PRIORITY_SOURCE = TRIAGE_DIR / "focal_imagery_priority_scores.csv"
PREVIOUS_REVIEW = TRIAGE_DIR / "pilot_review/top50_pilot_review_results.csv"
BATCH_DIR = TRIAGE_DIR / "annotation_batches/batch_001_stratified"
OVERVIEW_DIR = BATCH_DIR / "overview_pages"
DETAIL_DIR = BATCH_DIR / "detail_pages"
QUEUE_OUTPUT = BATCH_DIR / "annotation_queue.csv"
MANIFEST_OUTPUT = BATCH_DIR / "review_asset_manifest.csv"
PROTOCOL_OUTPUT = BATCH_DIR / "annotation_protocol.md"
SELECTION_PER_STRATUM = 2


def select_batch() -> pd.DataFrame:
    priority = pd.read_csv(PRIORITY_SOURCE, dtype={"photo_number": "string"})
    reviewed = set(pd.read_csv(PREVIOUS_REVIEW)["review_id"])
    eligible = priority.loc[~priority["review_id"].isin(reviewed)].copy()
    eligible = eligible.sort_values("global_priority_rank")
    selected = (
        eligible.groupby(["municipality", "photo_type"], sort=True, group_keys=False)
        .head(SELECTION_PER_STRATUM)
        .sort_values("global_priority_rank")
        .reset_index(drop=True)
    )
    expected = 3 * 2 * SELECTION_PER_STRATUM
    if len(selected) != expected:
        raise ValueError(f"Expected {expected} selected photos, found {len(selected)}")
    if selected["review_id"].duplicated().any():
        raise ValueError("Selected review IDs are not unique")
    selected.insert(0, "batch_item", range(1, len(selected) + 1))
    return selected


def write_protocol() -> None:
    PROTOCOL_OUTPUT.write_text(
        """# GSI aerial-photo annotation protocol — batch 001

## Unit of annotation

One complete post-event aerial photograph. This is photo-level screening, not a
building-level damage label and not an estimate of destroyed houses.

## Required coding order

1. `assessability`: `good`, `limited`, or `not_assessable`.
2. `scene_class`: `residential`, `mixed_built`, `nonresidential`, `natural`, or `uncertain`.
3. `damage_class`: `no_obvious_severe`, `possible_severe`, `possible_collapse`, or `uncertain`.
4. `collapse_candidate`: `yes`, `no`, or `uncertain`.
5. `confidence`: `high`, `medium`, or `low`.
6. Record the detail-grid tile and a concise visible-evidence note.

Use `possible_collapse` only for localized roof collapse, house-scale rubble, major
structural displacement, or an equivalent visible feature. Construction, demolition,
bare soil, greenhouses, shadows, clouds, and image artifacts are confounders. Code
uncertainty instead of forcing a damage decision.

## Interpretation boundary

Earthquake attribution remains `unverified` for every photo-level label. A possible
positive requires independent confirmation from pre-event imagery, a registered
orthophoto, field evidence, or an official damage record.
""",
        encoding="utf-8",
    )


def main() -> int:
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    selected = select_batch()
    _, overview_by_id = build_overview_pages(
        selected,
        output_dir=OVERVIEW_DIR,
        title="GSI annotation batch 001 — stratified unreviewed photos",
    )
    detail_by_id: dict[str, str] = {}
    for _, item in selected.iterrows():
        path = build_detail_page(item, output_dir=DETAIL_DIR)
        detail_by_id[str(item["review_id"])] = (
            str(path.relative_to(ROOT)) if path else ""
        )

    selected["overview_page_path"] = selected["review_id"].map(overview_by_id)
    selected["detail_page_path"] = selected["review_id"].map(detail_by_id)
    selected[
        [
            "batch_item",
            "global_priority_rank",
            "review_id",
            "municipality",
            "photo_type",
            "full_photo_path",
            "overview_page_path",
            "detail_page_path",
        ]
    ].to_csv(MANIFEST_OUTPUT, index=False)

    queue = selected.copy()
    queue["annotation_status"] = "unreviewed"
    queue["assessability"] = "unknown"
    queue["scene_class"] = "unknown"
    queue["damage_class"] = "unknown"
    queue["collapse_candidate"] = "unknown"
    queue["confidence"] = "unknown"
    queue["evidence_tile"] = ""
    queue["evidence_note"] = ""
    queue["reviewer"] = ""
    queue["reviewed_at"] = ""
    queue["earthquake_attribution"] = "unverified"
    queue.to_csv(QUEUE_OUTPUT, index=False)
    write_protocol()
    print(f"Prepared {len(queue)} photos")
    print(queue.groupby(["municipality", "photo_type"]).size().to_string())
    print(f"Saved {QUEUE_OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
