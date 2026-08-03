#!/usr/bin/env python3
"""Preprocess the prefecture-wide JMA summer station baseline.

Daily observations are calendar-matched to the 30-day post-earthquake study
window (July 28 through August 26) for each historical year, 2021-2025.
"""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "data/raw/weather/jma_daily_html"
MANIFEST_PATH = (
    ROOT
    / "data/raw/_manifests/kumamoto_jma_historical_spatial_stations_2021_2025.csv"
)
STATION_PATH = (
    ROOT
    / "data/raw/weather/jma_amedas/stations/amedastable_2026-08-02.json"
)
OUTPUT_PATH = (
    ROOT
    / "data/processed/kumamoto_jma_historical_heat_spatial_stations_preprocessed.parquet"
)
EVENT_DATE = date(2026, 7, 28)
SCENARIO_END = date(2026, 8, 26)
HOT_DAY_THRESHOLD_C = 35.0
HOT_NIGHT_THRESHOLD_C = 25.0

VALUE_INDEX = {
    "a1": {
        "mean_temperature": 4,
        "maximum_temperature": 5,
        "minimum_temperature": 6,
        "mean_humidity": 7,
    },
    "s1": {
        "mean_temperature": 6,
        "maximum_temperature": 7,
        "minimum_temperature": 8,
        "mean_humidity": 9,
    },
}


def coordinate(parts: list[float]) -> float:
    return float(parts[0]) + float(parts[1]) / 60.0


def cell_text(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(without_tags).split())


def number(value: str) -> float | None:
    if not value or value in {"--", "///"}:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)
    return float(match.group()) if match else None


def table_rows(path: Path) -> list[list[str]]:
    document = path.read_text(encoding="utf-8")
    table_match = re.search(
        r"<table[^>]+id=['\"]tablefix1['\"][^>]*>(.*?)</table>",
        document,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not table_match:
        raise ValueError(f"JMA daily table not found: {path}")
    rows: list[list[str]] = []
    for row_html in re.findall(
        r"<tr[^>]*>(.*?)</tr>", table_match.group(1), flags=re.IGNORECASE | re.DOTALL
    ):
        cells = [
            cell_text(cell)
            for cell in re.findall(
                r"<t[dh][^>]*>(.*?)</t[dh]>",
                row_html,
                flags=re.IGNORECASE | re.DOTALL,
            )
        ]
        if cells and cells[0].isdigit():
            rows.append(cells)
    return rows


def threshold(value: float | None, cutoff: float) -> bool | pd._libs.missing.NAType:
    return pd.NA if value is None else bool(value >= cutoff)


def main() -> int:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(
            "Run src/data/download_jma_historical_spatial_stations.py first."
        )
    manifest = pd.read_csv(MANIFEST_PATH, dtype={"station_id": "string"})
    station_definitions = manifest[
        ["station_id", "station_slug", "etrn_page_type"]
    ].drop_duplicates()
    if len(station_definitions) != 17:
        raise ValueError(f"Expected 17 stations, found {len(station_definitions)}")

    metadata = json.loads(STATION_PATH.read_text(encoding="utf-8"))
    rows: list[dict[str, object]] = []
    for station in station_definitions.itertuples(index=False):
        station_metadata = metadata[station.station_id]
        indices = VALUE_INDEX[station.etrn_page_type]
        for path in sorted((SOURCE_ROOT / station.station_slug).glob("20??_??.html")):
            year, month = (int(part) for part in path.stem.split("_"))
            if year not in range(2021, 2026) or month not in (7, 8):
                continue
            for cells in table_rows(path):
                historical_date = date(year, month, int(cells[0]))
                matched_date = date(2026, month, int(cells[0]))
                if not EVENT_DATE <= matched_date <= SCENARIO_END:
                    continue

                mean_temperature = number(cells[indices["mean_temperature"]])
                maximum_temperature = number(cells[indices["maximum_temperature"]])
                minimum_temperature = number(cells[indices["minimum_temperature"]])
                mean_humidity = number(cells[indices["mean_humidity"]])
                rows.append(
                    {
                        "Station ID": station.station_id,
                        "Station Name": station_metadata["enName"],
                        "Station Name Japanese": station_metadata["kjName"],
                        "Latitude": coordinate(station_metadata["lat"]),
                        "Longitude": coordinate(station_metadata["lon"]),
                        "Altitude m": float(station_metadata["alt"]),
                        "Historical Year": year,
                        "Historical Source Date": pd.Timestamp(historical_date),
                        "Scenario Date": pd.Timestamp(matched_date),
                        "Event Day": (matched_date - EVENT_DATE).days,
                        "Daily Mean Air Temperature C": mean_temperature,
                        "Daily Maximum Air Temperature C": maximum_temperature,
                        "Daily Minimum Air Temperature C": minimum_temperature,
                        "Daily Mean Relative Humidity %": mean_humidity,
                        "Hot Day Indicator": threshold(
                            maximum_temperature, HOT_DAY_THRESHOLD_C
                        ),
                        "Hot Night Indicator": threshold(
                            minimum_temperature, HOT_NIGHT_THRESHOLD_C
                        ),
                        "Temperature Record Complete": all(
                            value is not None
                            for value in (
                                mean_temperature,
                                maximum_temperature,
                                minimum_temperature,
                            )
                        ),
                        "Heat Exposure Status": "historical_observed",
                    }
                )

    historical = pd.DataFrame(rows).sort_values(
        ["Station Name", "Historical Year", "Event Day"]
    )
    expected_rows = len(station_definitions) * 5 * 30
    if len(historical) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, found {len(historical)}")

    for column in ("Hot Day Indicator", "Hot Night Indicator"):
        historical[column] = pd.array(historical[column], dtype="Int8")
    for column in (
        "Station ID",
        "Station Name",
        "Station Name Japanese",
        "Heat Exposure Status",
    ):
        historical[column] = historical[column].astype("string")
    historical["Temperature Record Complete"] = historical[
        "Temperature Record Complete"
    ].astype("boolean")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    historical.to_parquet(OUTPUT_PATH, index=False)

    complete = int(historical["Temperature Record Complete"].sum())
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(historical):,}; stations: {historical['Station ID'].nunique()}")
    print(
        f"Complete temperature records: {complete:,}/{len(historical):,} "
        f"({complete / len(historical):.1%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
