#!/usr/bin/env python3
"""Build versioned official housing-damage snapshots for the 2026 earthquake.

Blank cells in an official report are retained as missing rather than interpreted
as zero. Each row is one claim for one geographic unit at one report time.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
REPORT_15 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_15_2026-07-29.pdf"
)
REPORT_26 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_26_2026-08-01.pdf"
)
REPORT_27 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_27_2026-08-01_1130.pdf"
)
REPORT_28 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_28_2026-08-01_1700.pdf"
)
KUMAMOTO_CITY_MEETINGS = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/kumamoto_city/"
    "kumamoto_city_disaster_hq_meetings_2026-08-02.html"
)
OUTPUT = ROOT / "data/processed/kumamoto_housing_damage_snapshots_preprocessed.parquet"

REPORT_15_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin15.pdf"
)
REPORT_26_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin26.pdf"
)
REPORT_27_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin27.pdf"
)
REPORT_28_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin28.pdf"
)
KUMAMOTO_CITY_MEETINGS_URL = (
    "https://www.city.kumamoto.jp/kiji00372080/index.html"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_snapshots() -> pd.DataFrame:
    records = [
        {
            "Snapshot ID": "FDMA-15-KUMAMOTO-PREFECTURE",
            "Observation Time": "2026-07-29T11:00:00+09:00",
            "Geographic Level": "prefecture",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Full Collapse Buildings": pd.NA,
            "Half Collapse Buildings": pd.NA,
            "Partial Damage Buildings": pd.NA,
            "Reported Affected Buildings": pd.NA,
            "Data Status": "not_reported_in_damage_table",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 15,
            "Source Page": 1,
            "Source URL": REPORT_15_URL,
            "Source Relative Path": str(REPORT_15.relative_to(ROOT)),
            "Notes": (
                "The housing-damage table did not yet report a Kumamoto total. "
                "Separate incident text reported two residential buckling cases."
            ),
        },
        {
            "Snapshot ID": "FDMA-26-KUMAMOTO-PREFECTURE",
            "Observation Time": "2026-08-01T07:00:00+09:00",
            "Geographic Level": "prefecture",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Full Collapse Buildings": 179,
            "Half Collapse Buildings": 240,
            "Partial Damage Buildings": 1021,
            "Reported Affected Buildings": 1440,
            "Data Status": "official_preliminary_total",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 26,
            "Source Page": 1,
            "Source URL": REPORT_26_URL,
            "Source Relative Path": str(REPORT_26.relative_to(ROOT)),
            "Notes": "Preliminary counts; the report states that figures may change.",
        },
        {
            "Snapshot ID": "KUMAMOTO-CITY-HQ07-MINAMI-WARD",
            "Observation Time": "2026-07-31T15:00:00+09:00",
            "Geographic Level": "city_ward",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City, Minami Ward",
            "Full Collapse Buildings": 4,
            "Half Collapse Buildings": pd.NA,
            "Partial Damage Buildings": pd.NA,
            "Reported Affected Buildings": 39,
            "Data Status": "official_approximate_mixed_damage_classes",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 7,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": (
                "Four fully collapsed residences and approximately 35 residences "
                "ranging from partial damage to half collapse; the mixed group cannot "
                "be split into separate half-collapse and partial-damage counts."
            ),
        },
        {
            "Snapshot ID": "FDMA-27-KUMAMOTO-PREFECTURE",
            "Observation Time": "2026-08-01T11:30:00+09:00",
            "Geographic Level": "prefecture",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Full Collapse Buildings": 182,
            "Half Collapse Buildings": 245,
            "Partial Damage Buildings": 1034,
            "Reported Affected Buildings": 1461,
            "Data Status": "official_preliminary_total",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 27,
            "Source Page": 1,
            "Source URL": REPORT_27_URL,
            "Source Relative Path": str(REPORT_27.relative_to(ROOT)),
            "Notes": "Preliminary counts; the report states that figures may change.",
        },
        {
            "Snapshot ID": "FDMA-28-KUMAMOTO-PREFECTURE",
            "Observation Time": "2026-08-01T17:00:00+09:00",
            "Geographic Level": "prefecture",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Full Collapse Buildings": 181,
            "Half Collapse Buildings": 245,
            "Partial Damage Buildings": 1419,
            "Reported Affected Buildings": 1845,
            "Data Status": "official_preliminary_total",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 28,
            "Source Page": 1,
            "Source URL": REPORT_28_URL,
            "Source Relative Path": str(REPORT_28.relative_to(ROOT)),
            "Notes": "Preliminary counts; the report states that figures may change.",
        },
    ]
    frame = pd.DataFrame.from_records(records)
    frame["Observation Time"] = pd.to_datetime(frame["Observation Time"], utc=True)
    frame = frame.sort_values(["Observation Time", "Snapshot ID"]).reset_index(drop=True)
    integer_columns = [
        "Full Collapse Buildings",
        "Half Collapse Buildings",
        "Partial Damage Buildings",
        "Reported Affected Buildings",
        "Source Report Number",
        "Source Page",
    ]
    for column in integer_columns:
        frame[column] = frame[column].astype("Int64")
    for column in frame.columns.difference(["Observation Time", *integer_columns]):
        frame[column] = frame[column].astype("string")
    return frame


def validate(frame: pd.DataFrame) -> None:
    require(REPORT_15.is_file(), f"Missing source: {REPORT_15}")
    require(REPORT_26.is_file(), f"Missing source: {REPORT_26}")
    require(REPORT_27.is_file(), f"Missing source: {REPORT_27}")
    require(REPORT_28.is_file(), f"Missing source: {REPORT_28}")
    require(KUMAMOTO_CITY_MEETINGS.is_file(), f"Missing source: {KUMAMOTO_CITY_MEETINGS}")
    require(frame["Snapshot ID"].is_unique, "Snapshot ID must be unique")
    require(frame["Observation Time"].is_monotonic_increasing, "Snapshots are unordered")
    latest = frame.loc[frame["Snapshot ID"] == "FDMA-28-KUMAMOTO-PREFECTURE"].iloc[0]
    component_sum = int(
        latest[
            [
                "Full Collapse Buildings",
                "Half Collapse Buildings",
                "Partial Damage Buildings",
            ]
        ].sum()
    )
    require(
        component_sum == int(latest["Reported Affected Buildings"]),
        "Report 28 housing components do not sum to the reported total",
    )
    early = frame.loc[frame["Source Report Number"] == 15].iloc[0]
    require(
        pd.isna(early["Reported Affected Buildings"]),
        "An unreported early housing total must remain missing",
    )
    minami = frame.loc[frame["Snapshot ID"] == "KUMAMOTO-CITY-HQ07-MINAMI-WARD"].iloc[0]
    require(
        pd.isna(minami["Half Collapse Buildings"])
        and pd.isna(minami["Partial Damage Buildings"]),
        "Do not split the mixed Minami Ward damage category",
    )


def main() -> int:
    frame = build_snapshots()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
