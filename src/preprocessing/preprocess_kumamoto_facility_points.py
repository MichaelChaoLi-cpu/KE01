#!/usr/bin/env python3
"""Standardize Kumamoto shelter and MLIT KSJ facility point layers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
RAW = ROOT / "data/raw/facilities/mlit_ksj_2026-08-02"
SUMMARY = ROOT / "data/exp/spatial-foundation/facility_preprocessing_summary.json"

SOURCES = {
    "Medical Institution": {
        "path": RAW
        / "mlit-ksj-P04-medical-institutions-kumamoto-2020/extracted/P04-20_43.geojson",
        "year": 2020,
        "prefix": "p04",
        "output": "kumamoto_mlit_medical_institutions_preprocessed.parquet",
        "rename": {
            "P04_001": "Medical Institution Class",
            "P04_002": "Facility Name",
            "P04_003": "Address",
            "P04_004": "Department 1",
            "P04_005": "Department 2",
            "P04_006": "Department 3",
            "P04_007": "Operator Class",
            "P04_008": "Bed Count",
            "P04_009": "Emergency Hospital Designation",
            "P04_010": "Disaster Base Hospital Class",
        },
    },
    "Welfare Facility": {
        "path": RAW
        / "mlit-ksj-P14-welfare-facilities-kumamoto-2023/extracted/P14-23_43.geojson",
        "year": 2023,
        "prefix": "p14",
        "output": "kumamoto_mlit_welfare_facilities_preprocessed.parquet",
        "rename": {
            "P14_001": "Prefecture Name",
            "P14_002": "Municipality Name",
            "P14_003": "Administrative Area Code",
            "P14_004": "Address Detail",
            "P14_005": "Welfare Facility Major Class",
            "P14_006": "Welfare Facility Medium Class",
            "P14_007": "Welfare Facility Minor Class",
            "P14_008": "Facility Name",
            "P14_009": "Operator Code",
            "P14_010": "Position Accuracy",
        },
    },
    "Public Office or Hall": {
        "path": RAW
        / "mlit-ksj-P05-public-offices-and-halls-kumamoto-2022/extracted/P05-22_43.geojson",
        "year": 2022,
        "prefix": "p05",
        "output": "kumamoto_mlit_public_offices_halls_preprocessed.parquet",
        "rename": {
            "P05_001": "Administrative Area Code",
            "P05_002": "Facility Class",
            "P05_003": "Facility Name",
            "P05_004": "Address",
        },
    },
    "School": {
        "path": RAW
        / "mlit-ksj-P29-schools-kumamoto-2023/extracted/P29-23_43.geojson",
        "year": 2023,
        "prefix": "p29",
        "output": "kumamoto_mlit_schools_preprocessed.parquet",
        "rename": {
            "P29_001": "Administrative Area Code",
            "P29_002": "School Code",
            "P29_003": "School Class",
            "P29_004": "Facility Name",
            "P29_005": "Address",
            "P29_006": "Operator Code",
            "P29_007": "Suspension Status",
            "P29_008": "Campus Code",
            "P29_009": "School Notes",
        },
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def clean_strings(frame: pd.DataFrame) -> pd.DataFrame:
    for column in frame.select_dtypes(include=["object", "string"]).columns:
        frame[column] = frame[column].astype("string").str.strip()
        frame[column] = frame[column].replace("", pd.NA)
    return frame


def point_id(prefix: str, name: object, address: object, geometry) -> str:
    text = f"{prefix}|{name}|{address}|{geometry.x:.7f}|{geometry.y:.7f}"
    return f"{prefix}-" + hashlib.blake2b(
        text.encode("utf-8"), digest_size=10
    ).hexdigest()


def write_shelter_geoparquet(source_name: str, output_name: str) -> dict:
    source = PROCESSED / source_name
    output = PROCESSED / output_name
    frame = clean_strings(pd.read_parquet(source))
    require(frame[["Longitude", "Latitude"]].notna().all().all(), f"Missing coordinates: {source}")
    geo = gpd.GeoDataFrame(
        frame,
        geometry=gpd.points_from_xy(frame["Longitude"], frame["Latitude"]),
        crs=6668,
    )
    require(geo.geometry.is_valid.all(), f"Invalid shelter point: {source}")
    geo.to_parquet(output, index=False)
    return {"output": str(output.relative_to(ROOT)), "rows": len(geo)}


def read_mlit_facility(facility_type: str, config: dict) -> gpd.GeoDataFrame:
    frame = gpd.read_file(config["path"]).rename(columns=config["rename"])
    require(frame.crs is not None, f"Missing CRS: {config['path']}")
    frame = frame.to_crs(6668)
    frame = clean_strings(frame)
    if facility_type == "Welfare Facility":
        frame["Address"] = (
            frame[["Prefecture Name", "Municipality Name", "Address Detail"]]
            .fillna("")
            .agg("".join, axis=1)
            .replace("", pd.NA)
        )
    frame.insert(0, "Support Facility Type", facility_type)
    frame.insert(1, "Source Reference Year", int(config["year"]))
    frame.insert(
        0,
        "Support Facility ID",
        [
            point_id(config["prefix"], name, address, geometry)
            for name, address, geometry in zip(
                frame["Facility Name"], frame["Address"], frame.geometry, strict=True
            )
        ],
    )
    require(frame["Support Facility ID"].is_unique, f"Non-unique IDs: {facility_type}")
    require(frame.geometry.notna().all(), f"Missing geometry: {facility_type}")
    require(frame.geometry.geom_type.eq("Point").all(), f"Non-point geometry: {facility_type}")
    return frame


def main() -> int:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "designated_shelters": write_shelter_geoparquet(
            "kumamoto_designated_shelters_preprocessed.parquet",
            "kumamoto_designated_shelters_geospatial_preprocessed.parquet",
        ),
        "emergency_evacuation_sites": write_shelter_geoparquet(
            "kumamoto_emergency_evacuation_sites_preprocessed.parquet",
            "kumamoto_emergency_evacuation_sites_geospatial_preprocessed.parquet",
        ),
    }

    common_frames = []
    for facility_type, config in SOURCES.items():
        frame = read_mlit_facility(facility_type, config)
        output = PROCESSED / config["output"]
        frame.to_parquet(output, index=False)
        summary[config["prefix"]] = {
            "output": str(output.relative_to(ROOT)),
            "rows": len(frame),
            "reference_year": config["year"],
        }
        common_frames.append(
            frame[
                [
                    "Support Facility ID",
                    "Support Facility Type",
                    "Source Reference Year",
                    "Facility Name",
                    "Address",
                    "geometry",
                ]
            ]
        )

    combined = gpd.GeoDataFrame(
        pd.concat(common_frames, ignore_index=True), geometry="geometry", crs=6668
    )
    combined_output = PROCESSED / "kumamoto_support_facilities_preprocessed.parquet"
    combined.to_parquet(combined_output, index=False)
    summary["combined_support_facilities"] = {
        "output": str(combined_output.relative_to(ROOT)),
        "rows": len(combined),
        "counts_by_type": combined["Support Facility Type"].value_counts().to_dict(),
    }
    with SUMMARY.open("w", encoding="utf-8") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
