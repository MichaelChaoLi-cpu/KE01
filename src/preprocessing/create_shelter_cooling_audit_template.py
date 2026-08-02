#!/usr/bin/env python3
"""Create a field-verification template for effective cooled shelter capacity."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/processed/kumamoto_designated_shelters_preprocessed.parquet"
OUTPUT = ROOT / "data/exp/rapid-assessment/shelter_cooling_audit_template.csv"

REFERENCE_COLUMNS = [
    "Common ID",
    "Facility Name",
    "Address",
    "Latitude",
    "Longitude",
    "Accepted Persons",
    "Municipal Conditions",
    "Notes",
]

AUDIT_COLUMNS = [
    "Municipality",
    "Verification Status",
    "Verified At",
    "Verification Source",
    "Facility Contact",
    "Currently Open",
    "Current Occupancy",
    "Nominal Capacity",
    "Accessible Cooled Floor Area m2",
    "Functional Air Conditioning",
    "HVAC Coverage Percent",
    "Backup Power",
    "Generator Fuel Hours",
    "Potable Water",
    "Medical Support",
    "Mobility Accessible",
    "Operating Hours",
    "Effective Cooled Capacity Persons",
    "Confidence Grade",
    "Audit Notes",
]


def main() -> int:
    shelters = pd.read_parquet(SOURCE)
    audit = shelters[REFERENCE_COLUMNS].copy()
    for column in AUDIT_COLUMNS:
        audit[column] = ""
    audit["Verification Status"] = "unverified"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(OUTPUT, index=False, encoding="utf-8-sig")
    print(f"Saved {len(audit):,} rows x {len(audit.columns)} cols -> {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
