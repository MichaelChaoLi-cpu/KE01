#!/usr/bin/env python3
"""Preprocess JMA daily HTML into 2021-2025 matched heat scenarios."""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "data/raw/weather/jma_daily_html"
STATION_PATH = (
    ROOT
    / "data/raw/weather/jma_amedas/stations/amedastable_2026-08-02.json"
)
OUTPUT_PATH = (
    ROOT
    / "data/processed/kumamoto_jma_historical_heat_scenarios_preprocessed.parquet"
)
EVENT_DATE = date(2026, 7, 28)
SCENARIO_END = date(2026, 8, 26)
HOT_DAY_THRESHOLD_C = 35.0
HOT_NIGHT_THRESHOLD_C = 25.0

STATIONS = {
    "kumamoto": {
        "id": "86141",
        "mean_temperature_index": 6,
        "maximum_temperature_index": 7,
        "minimum_temperature_index": 8,
        "mean_humidity_index": 9,
    },
    "misumi": {
        "id": "86216",
        "mean_temperature_index": 4,
        "maximum_temperature_index": 5,
        "minimum_temperature_index": 6,
        "mean_humidity_index": 7,
    },
    "kosa": {
        "id": "86236",
        "mean_temperature_index": 4,
        "maximum_temperature_index": 5,
        "minimum_temperature_index": 6,
        "mean_humidity_index": 7,
    },
    "matsushima": {
        "id": "86271",
        "mean_temperature_index": 4,
        "maximum_temperature_index": 5,
        "minimum_temperature_index": 6,
        "mean_humidity_index": 7,
    },
    "yatsushiro": {
        "id": "86336",
        "mean_temperature_index": 4,
        "maximum_temperature_index": 5,
        "minimum_temperature_index": 6,
        "mean_humidity_index": 7,
    },
}


def _coordinate(parts: list[float]) -> float:
    return float(parts[0]) + float(parts[1]) / 60.0


def _cell_text(fragment: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", fragment)
    return " ".join(html.unescape(without_tags).split())


def _number(value: str) -> float | None:
    if not value or value in {"--", "///"}:
        return None
    match = re.search(r"[-+]?\d+(?:\.\d+)?", value)
    return float(match.group()) if match else None


def _table_rows(path: Path) -> list[list[str]]:
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
            _cell_text(cell)
            for cell in re.findall(
                r"<t[dh][^>]*>(.*?)</t[dh]>",
                row_html,
                flags=re.IGNORECASE | re.DOTALL,
            )
        ]
        if cells and cells[0].isdigit():
            rows.append(cells)
    return rows


def _threshold(value: float | None, cutoff: float) -> bool | pd._libs.missing.NAType:
    return pd.NA if value is None else bool(value >= cutoff)


def main() -> None:
    metadata = json.loads(STATION_PATH.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for station_slug, definition in STATIONS.items():
        station = metadata[definition["id"]]
        for path in sorted((SOURCE_DIR / station_slug).glob("20??_??.html")):
            year, month = (int(part) for part in path.stem.split("_"))
            if year not in range(2021, 2026) or month not in (7, 8):
                continue
            for cells in _table_rows(path):
                source_date = date(year, month, int(cells[0]))
                scenario_date = date(2026, month, int(cells[0]))
                if not EVENT_DATE <= scenario_date <= SCENARIO_END:
                    continue
                mean_temperature = _number(
                    cells[definition["mean_temperature_index"]]
                )
                maximum_temperature = _number(
                    cells[definition["maximum_temperature_index"]]
                )
                minimum_temperature = _number(
                    cells[definition["minimum_temperature_index"]]
                )
                mean_humidity = _number(cells[definition["mean_humidity_index"]])
                rows.append(
                    {
                        "Station ID": definition["id"],
                        "Station Name": station["enName"],
                        "Latitude": _coordinate(station["lat"]),
                        "Longitude": _coordinate(station["lon"]),
                        "Altitude m": float(station["alt"]),
                        "Historical Year": year,
                        "Historical Source Date": pd.Timestamp(source_date),
                        "Scenario Date": pd.Timestamp(scenario_date),
                        "Event Day": (scenario_date - EVENT_DATE).days,
                        "Daily Mean Air Temperature C": mean_temperature,
                        "Daily Maximum Air Temperature C": maximum_temperature,
                        "Daily Minimum Air Temperature C": minimum_temperature,
                        "Daily Mean Relative Humidity %": mean_humidity,
                        "Hot Day Indicator": _threshold(
                            maximum_temperature, HOT_DAY_THRESHOLD_C
                        ),
                        "Hot Night Indicator": _threshold(
                            minimum_temperature, HOT_NIGHT_THRESHOLD_C
                        ),
                        "Heat Exposure Status": "historical_observed",
                    }
                )

    historical = pd.DataFrame(rows).sort_values(
        ["Station Name", "Historical Year", "Event Day"]
    )
    expected_rows = len(STATIONS) * 5 * 30
    if len(historical) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} matched historical rows, found {len(historical)}."
        )
    if historical["Station ID"].nunique() != len(STATIONS):
        raise ValueError("Historical event-window station coverage is incomplete.")
    expected_per_day = len(STATIONS) * 5
    for column in (
        "Daily Maximum Air Temperature C",
        "Daily Minimum Air Temperature C",
    ):
        counts = historical.groupby("Event Day", observed=True)[column].count()
        if not counts.reindex(range(30)).eq(expected_per_day).all():
            raise ValueError(
                f"Expected {expected_per_day} observations per event day for {column}."
            )
    historical["Hot Day Indicator"] = pd.array(
        historical["Hot Day Indicator"], dtype="Int8"
    )
    historical["Hot Night Indicator"] = pd.array(
        historical["Hot Night Indicator"], dtype="Int8"
    )
    historical["Station ID"] = historical["Station ID"].astype("string")
    historical["Station Name"] = historical["Station Name"].astype("string")
    historical["Heat Exposure Status"] = historical["Heat Exposure Status"].astype(
        "string"
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    historical.to_parquet(OUTPUT_PATH, index=False)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(historical):,}; columns: {len(historical.columns)}")
    print(
        "Historical years: "
        f"{historical['Historical Year'].min()}-"
        f"{historical['Historical Year'].max()}"
    )
    print(
        "Scenario window: "
        f"{historical['Scenario Date'].min().date()} to "
        f"{historical['Scenario Date'].max().date()}"
    )


if __name__ == "__main__":
    main()
