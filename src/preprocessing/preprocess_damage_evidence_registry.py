#!/usr/bin/env python3
"""Build the geolocation-aware damage evidence registry.

The registry unit is an evidence claim at one time and spatial resolution, not
necessarily one building. Official but ungeolocated incident descriptions are
therefore retained without invented coordinates.
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
REPORT_28 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/fdma/"
    "fdma_report_28_2026-08-01_1700.pdf"
)
KUMAMOTO_CITY_MEETING_09 = ROOT / (
    "data/raw/earthquake/2026-07-28_kumamoto/kumamoto_city/"
    "kumamoto_city_disaster_hq_meeting_09_2026-08-02.pdf"
)
OUTPUT = ROOT / "data/processed/kumamoto_damage_evidence_registry_preprocessed.parquet"

REPORT_15_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin15.pdf"
)
REPORT_26_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin26.pdf"
)
REPORT_28_URL = (
    "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin28.pdf"
)
KUMAMOTO_CITY_MEETING_09_URL = (
    "https://www.city.kumamoto.jp/kiji00372080/index.html"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_registry() -> pd.DataFrame:
    common = {
        "Source Organization": "Fire and Disaster Management Agency",
        "Source Type": "official_situation_report",
        "Source Page": 1,
        "Latitude": pd.NA,
        "Longitude": pd.NA,
        "Coordinate Precision": "municipality_only",
        "Coordinate Uncertainty m": pd.NA,
        "Evidence Tier": "B_official_incident_approximate",
        "Verification Status": "official_reported_not_geolocated",
    }
    records = [
        {
            **common,
            "Evidence ID": "FDMA15-YAT-CHIMNEY-001",
            "Event ID": "YAT-CHIMNEY-001",
            "Observation Time": "2026-07-29T11:00:00+09:00",
            "Source Report Number": 15,
            "Source URL": REPORT_15_URL,
            "Source Relative Path": str(REPORT_15.relative_to(ROOT)),
            "Municipality": "Yatsushiro City",
            "Place Description": "Factory chimney collapse in Yatsushiro City",
            "Asset Type": "industrial",
            "Observed Damage Type": "chimney_collapse",
            "Structural Damage Class": "confirmed_collapse",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "not_applicable_nonresidential",
            "Heat Protection Loss Mechanism": "structural_collapse",
            "Reported Affected Asset Count": 1,
            "Supersedes Evidence ID": pd.NA,
            "Notes": "Official rescue incident; exact factory and coordinates not reported.",
        },
        {
            **common,
            "Evidence ID": "FDMA15-KAS-COMMERCIAL-001",
            "Event ID": "KAS-COMMERCIAL-001",
            "Observation Time": "2026-07-29T11:00:00+09:00",
            "Source Report Number": 15,
            "Source URL": REPORT_15_URL,
            "Source Relative Path": str(REPORT_15.relative_to(ROOT)),
            "Municipality": "Kashima Town",
            "Place Description": "Second-floor collapse at a commercial facility",
            "Asset Type": "commercial",
            "Observed Damage Type": "floor_collapse",
            "Structural Damage Class": "confirmed_collapse",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "not_applicable_nonresidential",
            "Heat Protection Loss Mechanism": "structural_collapse",
            "Reported Affected Asset Count": 1,
            "Supersedes Evidence ID": pd.NA,
            "Notes": "Official rescue incident; exact facility and coordinates not reported.",
        },
        {
            **common,
            "Evidence ID": "FDMA15-HIK-RESIDENTIAL-001",
            "Event ID": "HIK-RESIDENTIAL-001",
            "Observation Time": "2026-07-29T11:00:00+09:00",
            "Source Report Number": 15,
            "Source URL": REPORT_15_URL,
            "Source Relative Path": str(REPORT_15.relative_to(ROOT)),
            "Municipality": "Hikawa Town",
            "Place Description": "Two residential buckling incidents",
            "Asset Type": "residential",
            "Observed Damage Type": "structural_buckling",
            "Structural Damage Class": "confirmed_severe_damage",
            "Functional Housing Loss Status": "probable_functional_loss",
            "Habitability Status": "likely_uninhabitable_pending_inspection",
            "Heat Protection Loss Mechanism": "structural_unsafety",
            "Reported Affected Asset Count": 2,
            "Supersedes Evidence ID": pd.NA,
            "Notes": (
                "One aggregate evidence claim for two houses; the report does not "
                "provide separate addresses or inspection outcomes."
            ),
        },
        {
            **common,
            "Evidence ID": "FDMA26-KAS-COMMERCIAL-001",
            "Event ID": "KAS-COMMERCIAL-001",
            "Observation Time": "2026-08-01T07:00:00+09:00",
            "Source Report Number": 26,
            "Source URL": REPORT_26_URL,
            "Source Relative Path": str(REPORT_26.relative_to(ROOT)),
            "Municipality": "Kashima Town",
            "Place Description": "Second-floor collapse at a commercial facility",
            "Asset Type": "commercial",
            "Observed Damage Type": "floor_collapse",
            "Structural Damage Class": "confirmed_collapse",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "not_applicable_nonresidential",
            "Heat Protection Loss Mechanism": "structural_collapse",
            "Reported Affected Asset Count": 1,
            "Supersedes Evidence ID": "FDMA15-KAS-COMMERCIAL-001",
            "Notes": "The rescue response remained active in report 26.",
        },
        {
            **common,
            "Evidence ID": "FDMA28-KAS-COMMERCIAL-001",
            "Event ID": "KAS-COMMERCIAL-001",
            "Observation Time": "2026-08-01T17:00:00+09:00",
            "Source Report Number": 28,
            "Source URL": REPORT_28_URL,
            "Source Relative Path": str(REPORT_28.relative_to(ROOT)),
            "Municipality": "Kashima Town",
            "Place Description": "Second-floor collapse at a commercial facility",
            "Asset Type": "commercial",
            "Observed Damage Type": "floor_collapse",
            "Structural Damage Class": "confirmed_collapse",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "not_applicable_nonresidential",
            "Heat Protection Loss Mechanism": "structural_collapse",
            "Reported Affected Asset Count": 1,
            "Supersedes Evidence ID": "FDMA26-KAS-COMMERCIAL-001",
            "Notes": "Search and rescue activity was reported complete on August 1.",
        },
        {
            **common,
            "Evidence ID": "KCITY09-MINAMI-HOUSING-CLUSTER",
            "Event ID": "KCITY-MINAMI-HOUSING-CLUSTER",
            "Observation Time": "2026-08-02T09:00:00+09:00",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 22,
            "Source URL": KUMAMOTO_CITY_MEETING_09_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Municipality": "Kumamoto City",
            "Place Description": "Minami Ward, especially Tomiai and Jonan",
            "Coordinate Precision": "district_cluster",
            "Asset Type": "residential",
            "Observed Damage Type": "mixed_full_and_half_collapse_cluster",
            "Structural Damage Class": "confirmed_mixed_severe_damage_cluster",
            "Functional Housing Loss Status": "probable_functional_loss_cluster",
            "Habitability Status": "mixed_pending_inspection",
            "Heat Protection Loss Mechanism": "structural_unsafety_and_ground_damage",
            "Reported Affected Asset Count": pd.NA,
            "Evidence Tier": "A_official_preassessment_cluster",
            "Verification Status": "official_citywide_preassessment_completed",
            "Supersedes Evidence ID": pd.NA,
            "Notes": (
                "City pre-assessment found severe residential damage concentrated in "
                "Tomiai and Jonan and ground damage in part of Tomiai. At 09:00, 742 "
                "damage-certificate inspection applications had been received, including "
                "434 in Minami Ward; applications are not treated as damaged-building counts."
            ),
        },
        {
            **common,
            "Evidence ID": "KCITY09-KUMANOSHO-SHELTER-CLOSED",
            "Event ID": "KCITY-KUMANOSHO-SHELTER",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 87,
            "Source URL": KUMAMOTO_CITY_MEETING_09_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Municipality": "Kumamoto City",
            "Place Description": "Kumanosho Elementary School shelter",
            "Latitude": 32.708173,
            "Longitude": 130.726723,
            "Coordinate Precision": "official_facility_point",
            "Coordinate Uncertainty m": 30.0,
            "Asset Type": "shelter",
            "Observed Damage Type": "closed_due_to_water_outage_and_ac_failure",
            "Structural Damage Class": "not_assessable",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "shelter_unavailable",
            "Heat Protection Loss Mechanism": "shelter_cooling_and_water_unavailable",
            "Reported Affected Asset Count": 1,
            "Evidence Tier": "A_official_geolocated_facility_status",
            "Verification Status": "official_operational_status",
            "Supersedes Evidence ID": pd.NA,
            "Notes": "Shelter closed with no evacuees present at closure.",
        },
        {
            **common,
            "Evidence ID": "KCITY09-MIYUKI-SHELTER-CLOSED",
            "Event ID": "KCITY-MIYUKI-SHELTER",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 87,
            "Source URL": KUMAMOTO_CITY_MEETING_09_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Municipality": "Kumamoto City",
            "Place Description": "Miyuki Elementary School shelter",
            "Latitude": 32.754308,
            "Longitude": 130.716055,
            "Coordinate Precision": "official_facility_point",
            "Coordinate Uncertainty m": 30.0,
            "Asset Type": "shelter",
            "Observed Damage Type": "closed_due_to_water_outage",
            "Structural Damage Class": "not_assessable",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "shelter_unavailable",
            "Heat Protection Loss Mechanism": "shelter_water_unavailable",
            "Reported Affected Asset Count": 1,
            "Evidence Tier": "A_official_geolocated_facility_status",
            "Verification Status": "official_operational_status",
            "Supersedes Evidence ID": pd.NA,
            "Notes": "Shelter closed with no evacuees present at closure.",
        },
        {
            **common,
            "Evidence ID": "KCITY09-MINAMI-OTHER-SHELTERS-UNAVAILABLE",
            "Event ID": "KCITY-MINAMI-OTHER-SHELTERS-UNAVAILABLE",
            "Observation Time": "2026-08-02T15:30:00+09:00",
            "Source Organization": "Kumamoto City",
            "Source Type": "official_disaster_headquarters_meeting",
            "Source Report Number": 9,
            "Source Page": 87,
            "Source URL": KUMAMOTO_CITY_MEETING_09_URL,
            "Source Relative Path": str(KUMAMOTO_CITY_MEETING_09.relative_to(ROOT)),
            "Municipality": "Kumamoto City",
            "Place Description": "Five additional unavailable shelters in Minami Ward",
            "Coordinate Precision": "ward_only",
            "Asset Type": "shelter",
            "Observed Damage Type": "unavailable_due_to_damage_water_or_no_ac",
            "Structural Damage Class": "not_assessable",
            "Functional Housing Loss Status": "not_applicable_nonresidential",
            "Habitability Status": "shelter_unavailable",
            "Heat Protection Loss Mechanism": "shelter_damage_water_or_cooling_unavailable",
            "Reported Affected Asset Count": 5,
            "Evidence Tier": "A_official_aggregate_facility_status",
            "Verification Status": "official_operational_status_not_individually_named",
            "Supersedes Evidence ID": pd.NA,
            "Notes": (
                "Together with the two named closures, seven shelters were unavailable "
                "because of building damage, water outage, or lack of air conditioning."
            ),
        },
    ]
    frame = pd.DataFrame.from_records(records)
    frame["Observation Time"] = pd.to_datetime(frame["Observation Time"], utc=True)
    integer_columns = [
        "Source Report Number",
        "Source Page",
        "Reported Affected Asset Count",
    ]
    float_columns = ["Latitude", "Longitude", "Coordinate Uncertainty m"]
    for column in integer_columns:
        frame[column] = frame[column].astype("Int64")
    for column in float_columns:
        frame[column] = frame[column].astype("Float64")
    for column in frame.columns.difference(
        ["Observation Time", *integer_columns, *float_columns]
    ):
        frame[column] = frame[column].astype("string")
    return frame


def validate(frame: pd.DataFrame) -> None:
    require(REPORT_15.is_file(), f"Missing source: {REPORT_15}")
    require(REPORT_26.is_file(), f"Missing source: {REPORT_26}")
    require(REPORT_28.is_file(), f"Missing source: {REPORT_28}")
    require(
        KUMAMOTO_CITY_MEETING_09.is_file(),
        f"Missing source: {KUMAMOTO_CITY_MEETING_09}",
    )
    require(frame["Evidence ID"].is_unique, "Evidence ID must be unique")
    reported_counts = frame["Reported Affected Asset Count"].dropna()
    require((reported_counts > 0).all(), "Reported affected asset counts must be positive")
    one_coordinate_missing = frame["Latitude"].isna() ^ frame["Longitude"].isna()
    require(not one_coordinate_missing.any(), "Latitude and longitude must be paired")
    hikawa = frame["Evidence ID"].eq("FDMA15-HIK-RESIDENTIAL-001")
    require(hikawa.sum() == 1, "Expected the Hikawa residential incident claim")
    require(
        int(frame.loc[hikawa, "Reported Affected Asset Count"].iloc[0]) == 2,
        "The Hikawa residential claim must retain its aggregate count of two",
    )


def main() -> int:
    frame = build_registry()
    validate(frame)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"wrote {len(frame):,} rows to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
