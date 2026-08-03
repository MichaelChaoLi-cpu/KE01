#!/usr/bin/env python3
"""Preprocess JMA AMeDAS event-window observations to daily heat indicators.

The source consists of official three-hour JSON blocks containing ten-minute
observations. Missing observations remain missing. Daily threshold indicators
are not set to false for an incomplete current day.
"""

from __future__ import annotations

import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "data/raw/weather/jma_amedas/event_window"
STATION_PATH = (
    ROOT
    / "data/raw/weather/jma_amedas/stations/amedastable_2026-08-02.json"
)
OUTPUT_PATH = (
    ROOT / "data/processed/kumamoto_jma_event_heat_daily_preprocessed.parquet"
)
EVENT_DATE = pd.Timestamp("2026-07-28")
EXPECTED_OBSERVATIONS_PER_DAY = 144
HOT_DAY_THRESHOLD_C = 35.0
HOT_NIGHT_THRESHOLD_C = 25.0
JST = ZoneInfo("Asia/Tokyo")

STATION_IDS = {
    "kumamoto": "86141",
    "misumi": "86216",
    "kosa": "86236",
    "matsushima": "86271",
    "yatsushiro": "86336",
}


def _coordinate(parts: list[float]) -> float:
    """Convert JMA degree/minute coordinate pairs to decimal degrees."""
    return float(parts[0]) + float(parts[1]) / 60.0


def _measurement(record: dict, key: str) -> tuple[float | None, int | None]:
    value = record.get(key)
    if not isinstance(value, list) or not value or value[0] is None:
        return None, None
    quality = int(value[1]) if len(value) > 1 and value[1] is not None else None
    return float(value[0]), quality


def _load_observations() -> pd.DataFrame:
    metadata = json.loads(STATION_PATH.read_text(encoding="utf-8"))
    rows: list[dict] = []
    for station_dir in sorted(path for path in SOURCE_DIR.iterdir() if path.is_dir()):
        station_slug = station_dir.name
        station_id = STATION_IDS[station_slug]
        station = metadata[station_id]
        for path in sorted(station_dir.glob("*.json")):
            block = json.loads(path.read_text(encoding="utf-8"))
            for timestamp, record in block.items():
                temperature, temperature_quality = _measurement(record, "temp")
                humidity, humidity_quality = _measurement(record, "humidity")
                rows.append(
                    {
                        "Station ID": station_id,
                        "Station Name": station["enName"],
                        "Latitude": _coordinate(station["lat"]),
                        "Longitude": _coordinate(station["lon"]),
                        "Altitude m": float(station["alt"]),
                        "Observation Time": pd.to_datetime(
                            timestamp, format="%Y%m%d%H%M%S"
                        ).tz_localize(JST),
                        "Air Temperature C": temperature,
                        "Temperature Quality Flag": temperature_quality,
                        "Relative Humidity %": humidity,
                        "Humidity Quality Flag": humidity_quality,
                    }
                )

    observations = pd.DataFrame(rows)
    if observations.empty:
        raise ValueError(f"No JMA observations found under {SOURCE_DIR}")
    observations = observations.drop_duplicates(
        subset=["Station ID", "Observation Time"], keep="last"
    ).sort_values(["Station ID", "Observation Time"])
    if not observations["Temperature Quality Flag"].dropna().eq(0).all():
        raise ValueError("Non-zero JMA temperature quality flags require review.")
    if not observations["Humidity Quality Flag"].dropna().eq(0).all():
        raise ValueError("Non-zero JMA humidity quality flags require review.")
    observations["Observation Date"] = observations["Observation Time"].dt.date
    return observations


def _threshold_indicator(
    value: float | None, threshold: float, complete: bool, *, confirm_above: bool
) -> bool | pd._libs.missing.NAType:
    if pd.isna(value):
        return pd.NA
    if complete:
        return bool(value >= threshold)
    if confirm_above and value >= threshold:
        return True
    return pd.NA


def main() -> None:
    observations = _load_observations()
    station_columns = [
        "Station ID",
        "Station Name",
        "Latitude",
        "Longitude",
        "Altitude m",
        "Observation Date",
    ]
    daily = (
        observations.groupby(station_columns, as_index=False, dropna=False)
        .agg(
            **{
                "Daily Mean Air Temperature C": ("Air Temperature C", "mean"),
                "Daily Maximum Air Temperature C": ("Air Temperature C", "max"),
                "Daily Minimum Air Temperature C": ("Air Temperature C", "min"),
                "Daily Mean Relative Humidity %": ("Relative Humidity %", "mean"),
                "Temperature Observation Count": ("Air Temperature C", "count"),
                "Humidity Observation Count": ("Relative Humidity %", "count"),
                "Latest Observation Time": ("Observation Time", "max"),
            }
        )
        .sort_values(["Observation Date", "Station Name"])
        .reset_index(drop=True)
    )
    daily["Observation Date"] = pd.to_datetime(daily["Observation Date"])
    daily["Event Day"] = (daily["Observation Date"] - EVENT_DATE).dt.days
    daily["Daily Observation Completeness %"] = (
        daily["Temperature Observation Count"]
        .div(EXPECTED_OBSERVATIONS_PER_DAY)
        .mul(100)
        .clip(upper=100)
    )
    complete = daily["Temperature Observation Count"].ge(
        EXPECTED_OBSERVATIONS_PER_DAY
    )
    daily["Daily Record Status"] = complete.map(
        {True: "complete", False: "partial"}
    )
    daily["Heat Exposure Status"] = complete.map(
        {True: "observed_complete", False: "observed_partial"}
    )
    daily["Hot Day Indicator"] = pd.array(
        [
            _threshold_indicator(value, HOT_DAY_THRESHOLD_C, is_complete, confirm_above=True)
            for value, is_complete in zip(
                daily["Daily Maximum Air Temperature C"], complete, strict=True
            )
        ],
        dtype="Int8",
    )
    daily["Hot Night Indicator"] = pd.array(
        [
            _threshold_indicator(value, HOT_NIGHT_THRESHOLD_C, is_complete, confirm_above=False)
            for value, is_complete in zip(
                daily["Daily Minimum Air Temperature C"], complete, strict=True
            )
        ],
        dtype="Int8",
    )

    float_columns = [
        "Latitude",
        "Longitude",
        "Altitude m",
        "Daily Mean Air Temperature C",
        "Daily Maximum Air Temperature C",
        "Daily Minimum Air Temperature C",
        "Daily Mean Relative Humidity %",
        "Daily Observation Completeness %",
    ]
    daily[float_columns] = daily[float_columns].astype("float64")
    daily["Station ID"] = daily["Station ID"].astype("string")
    daily["Station Name"] = daily["Station Name"].astype("string")
    daily["Daily Record Status"] = daily["Daily Record Status"].astype("string")
    daily["Heat Exposure Status"] = daily["Heat Exposure Status"].astype("string")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    daily.to_parquet(OUTPUT_PATH, index=False)
    print(f"Saved: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Rows: {len(daily):,}; columns: {len(daily.columns)}")
    print(
        "Coverage: "
        f"{daily['Observation Date'].min().date()} to "
        f"{daily['Observation Date'].max().date()}"
    )
    print(f"Record status: {daily['Daily Record Status'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
