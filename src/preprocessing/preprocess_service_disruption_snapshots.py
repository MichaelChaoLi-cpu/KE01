#!/usr/bin/env python3
"""Build time-stamped service and occupancy-disruption evidence.

An evacuation-order population is a policy coverage count, not an observed count
of evacuees or households that lost cooling. The distinction is explicit here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
REPORT_26 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_26_2026-08-01.pdf"
)
REPORT_28 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_28_2026-08-01_1700.pdf"
)
KUMAMOTO_CITY_MEETINGS = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/kumamoto_city/"
    "kumamoto_city_disaster_hq_meetings_2026-08-02.html"
)
KUMAMOTO_CITY_MEETING_09 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/kumamoto_city/"
    "kumamoto_city_disaster_hq_meeting_09_2026-08-02.pdf"
)
OUTPUT = ROOT / (
    "data/processed/kumamoto_service_disruption_snapshots_preprocessed.parquet"
)
REPORT_26_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin26.pdf"
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
            "Disruption Snapshot ID": "FDMA26-KUMAMOTO-EVACUATION-INSTRUCTION",
            "Observation Time": "2026-08-01T07:00:00+09:00",
            "Geographic Level": "multi_municipality_official_total",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Disruption Type": "evacuation_instruction",
            "Service Status": "instruction_in_effect",
            "Heat Protection Loss Mechanism": "unsafe_occupancy_or_evacuation",
            "Reported Municipality Count": 7,
            "Reported Affected Households": 116909,
            "Reported Affected People": 246540,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_aggregate",
            "Verification Status": "official_preliminary_scope_count",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 26,
            "Source Page": 2,
            "Source URL": REPORT_26_URL,
            "Source Relative Path": str(REPORT_26.relative_to(ROOT)),
            "Notes": (
                "Three cities and four towns were covered. The household and people "
                "counts are instruction coverage, not observed evacuation or cooling loss."
            ),
        },
        {
            "Disruption Snapshot ID": "FDMA28-KUMAMOTO-EVACUATION-INSTRUCTION",
            "Observation Time": "2026-08-01T17:00:00+09:00",
            "Geographic Level": "multi_municipality_official_total",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Disruption Type": "evacuation_instruction",
            "Service Status": "instruction_in_effect",
            "Heat Protection Loss Mechanism": "unsafe_occupancy_or_evacuation",
            "Reported Municipality Count": 7,
            "Reported Affected Households": 116909,
            "Reported Affected People": 246540,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_aggregate",
            "Verification Status": "official_preliminary_scope_count",
            "Source Organization": "Fire and Disaster Management Agency",
            "Source Type": "official_situation_report",
            "Source Report Number": 28,
            "Source Page": 2,
            "Source URL": REPORT_28_URL,
            "Source Relative Path": str(REPORT_28.relative_to(ROOT)),
            "Notes": (
                "Three cities and four towns were covered. Counts were unchanged from "
                "report 26 and still represent instruction coverage, not observed evacuation."
            ),
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ02-SHELTER-OCCUPANCY",
            "Observation Time": "2026-07-28T21:00:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "181_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 1512,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 2,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "858 households in 181 open shelters; public shelters only.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ03-SHELTER-OCCUPANCY",
            "Observation Time": "2026-07-29T00:30:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "182_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 2344,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 3,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "1,299 households in 182 open shelters; public shelters only.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ03-POWER-OUTAGE",
            "Observation Time": "2026-07-29T00:30:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "power_outage",
            "Service Status": "outage_in_effect",
            "Heat Protection Loss Mechanism": "electric_cooling_unavailable",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": 2570,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": True,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_approximate_outage_count",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 3,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "Approximate city total; about 2,500 customers were in Minami Ward.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ03-WATER-OUTAGE",
            "Observation Time": "2026-07-29T00:30:00+09:00",
            "Geographic Level": "district",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City, Jonan",
            "Disruption Type": "water_outage",
            "Service Status": "outage_in_effect",
            "Heat Protection Loss Mechanism": "household_water_unavailable",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": 8970,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_approximate_outage_count",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 3,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "Kawashiri also had low water pressure affecting about 12,000 households.",
        },
        {
            "Disruption Snapshot ID": "KCITY-PEAK-SHELTER-OCCUPANCY",
            "Observation Time": "2026-07-29T03:00:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "observed_peak",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 2487,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_peak_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 8,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Notes": "Maximum reported public-shelter occupancy; excludes other displacement modes.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ04-SHELTER-OCCUPANCY",
            "Observation Time": "2026-07-29T09:50:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "183_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 1470,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 4,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "799 households in 183 open shelters; public shelters only.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ07-SHELTER-OCCUPANCY",
            "Observation Time": "2026-07-31T15:00:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "180_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 807,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting_webpage",
            "Source Report Number": 7,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "443 households in 180 open shelters; public shelters only.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ08-SHELTER-OCCUPANCY",
            "Observation Time": "2026-08-01T14:30:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "63_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 704,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 8,
            "Source Page": pd.NA,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETINGS.relative_to(ROOT)),
            "Notes": "419 households in 63 open shelters; public shelters only.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ09-SHELTER-OCCUPANCY",
            "Observation Time": "2026-08-02T13:00:00+09:00",
            "Geographic Level": "municipality",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "56_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 657,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 8,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Notes": (
                "402 households in 56 open shelters. The same meeting separately states "
                "676 people at 12:00; the later 13:00 headcount is retained."
            ),
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ09-MINAMI-SHELTER-OCCUPANCY",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Geographic Level": "city_ward",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City, Minami Ward",
            "Disruption Type": "shelter_occupancy",
            "Service Status": "19_shelters_open",
            "Heat Protection Loss Mechanism": "observed_displacement_to_public_shelter",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": 430,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_ward_observation",
            "Verification Status": "official_shelter_headcount",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 87,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Notes": "221 households in 19 open shelters in Minami Ward.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ09-POWER-RESTORED",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Geographic Level": "prefecture",
            "Prefecture": "Kumamoto",
            "Municipality": pd.NA,
            "Disruption Type": "power_outage",
            "Service Status": "restored",
            "Heat Protection Loss Mechanism": "electric_cooling_service_restored",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": 0,
            "Observed Water Outage Households": pd.NA,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_summary",
            "Verification Status": "official_reported_full_restoration",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 7,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Notes": "The city meeting reported that prefecture-wide electricity service was restored.",
        },
        {
            "Disruption Snapshot ID": "KCITY-HQ09-JONAN-WATER-OUTAGE",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Geographic Level": "district",
            "Prefecture": "Kumamoto",
            "Municipality": "Kumamoto City, Jonan",
            "Disruption Type": "water_outage",
            "Service Status": "outage_in_effect",
            "Heat Protection Loss Mechanism": "household_water_unavailable",
            "Reported Municipality Count": pd.NA,
            "Reported Affected Households": pd.NA,
            "Reported Affected People": pd.NA,
            "Observed Evacuee Count": pd.NA,
            "Observed Power Outage Customers": pd.NA,
            "Observed Water Outage Households": 900,
            "Cooling Loss Confirmed": False,
            "Evidence Tier": "A_official_municipal_observation",
            "Verification Status": "official_approximate_outage_count",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 7,
            "Source URL": KUMAMOTO_CITY_MEETINGS_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Notes": "Approximate remaining water outage in Jonan; Tomiai low pressure had resolved.",
        },
    ]
    frame = pd.DataFrame.from_records(records)
    frame["Observation Time"] = pd.to_datetime(frame["Observation Time"], utc=True)
    frame = frame.sort_values(["Observation Time", "Disruption Snapshot ID"]).reset_index(
        drop=True
    )
    integer_columns = [
        "Reported Municipality Count",
        "Reported Affected Households",
        "Reported Affected People",
        "Observed Evacuee Count",
        "Observed Power Outage Customers",
        "Observed Water Outage Households",
        "Source Report Number",
        "Source Page",
    ]
    for column in integer_columns:
        frame[column] = frame[column].astype("Int64")
    frame["Cooling Loss Confirmed"] = frame["Cooling Loss Confirmed"].astype("boolean")
    for column in frame.columns.difference(
        ["Observation Time", "Cooling Loss Confirmed", *integer_columns]
    ):
        frame[column] = frame[column].astype("string")
    return frame


def validate(frame: pd.DataFrame) -> None:
    require(REPORT_26.is_file(), f"Missing source: {REPORT_26}")
    require(REPORT_28.is_file(), f"Missing source: {REPORT_28}")
    require(KUMAMOTO_CITY_MEETINGS.is_file(), f"Missing source: {KUMAMOTO_CITY_MEETINGS}")
    require(
        KUMAMOTO_CITY_MEETING_09.is_file(),
        f"Missing source: {KUMAMOTO_CITY_MEETING_09}",
    )
    require(
        frame["Disruption Snapshot ID"].is_unique,
        "Disruption Snapshot ID must be unique",
    )
    row = frame.loc[
        frame["Disruption Snapshot ID"] == "FDMA26-KUMAMOTO-EVACUATION-INSTRUCTION"
    ].iloc[0]
    require(pd.isna(row["Observed Evacuee Count"]), "Do not infer observed evacuees")
    require(not bool(row["Cooling Loss Confirmed"]), "Instruction does not confirm cooling loss")
    require(
        int(row["Reported Affected People"]) == 246540,
        "Evacuation-instruction coverage was transcribed incorrectly",
    )
    peak = frame.loc[
        frame["Disruption Snapshot ID"] == "KCITY-PEAK-SHELTER-OCCUPANCY",
        "Observed Evacuee Count",
    ].iloc[0]
    require(int(peak) == 2487, "Peak Kumamoto City shelter occupancy is incorrect")
    latest_water = frame.loc[
        frame["Disruption Snapshot ID"] == "KCITY-HQ09-JONAN-WATER-OUTAGE",
        "Observed Water Outage Households",
    ].iloc[0]
    require(int(latest_water) == 900, "Latest Jonan water-outage count is incorrect")


def main() -> int:
    frame = build_snapshots()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
