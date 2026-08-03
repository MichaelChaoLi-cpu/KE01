#!/usr/bin/env python3
"""Refresh official JMA AMeDAS event-window blocks for one JST date.

Available blocks replace earlier partial snapshots atomically. Blocks that JMA
has not published yet are skipped, so an in-progress day remains explicitly
partial in the downstream daily dataset.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "data/raw/weather/jma_amedas/event_window"
MANIFEST_PATH = ROOT / "data/raw/_manifests/kumamoto_jma_event_window_refresh.csv"
USER_AGENT = "KE01-research-data-acquisition/1.0"
JST = ZoneInfo("Asia/Tokyo")
STATIONS = {
    "kumamoto": "86141",
    "misumi": "86216",
    "kosa": "86236",
    "matsushima": "86271",
    "yatsushiro": "86336",
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fetch(url: str) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    if not payload:
        return None
    parsed = json.loads(payload)
    if not isinstance(parsed, dict):
        raise ValueError(f"Unexpected JMA response: {url}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        default=datetime.now(JST).date().isoformat(),
        help="JST observation date in YYYY-MM-DD format",
    )
    args = parser.parse_args()
    observation_date = date.fromisoformat(args.date)
    day = observation_date.strftime("%Y%m%d")
    retrieved_at = datetime.now(JST).isoformat(timespec="seconds")
    rows: list[dict[str, object]] = []

    for station_slug, station_id in STATIONS.items():
        for block_hour in range(0, 24, 3):
            block = f"{block_hour:02d}"
            url = (
                "https://www.jma.go.jp/bosai/amedas/data/point/"
                f"{station_id}/{day}_{block}.json"
            )
            payload = fetch(url)
            destination = OUTPUT_ROOT / station_slug / f"{day}_{block}.json"
            status = "unavailable"
            if payload is not None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                temporary = destination.with_suffix(".json.part")
                temporary.write_bytes(payload)
                temporary.replace(destination)
                status = "refreshed"
            rows.append(
                {
                    "station_id": station_id,
                    "station_slug": station_slug,
                    "observation_date": observation_date.isoformat(),
                    "block_hour": block,
                    "source_url": url,
                    "relative_path": str(destination.relative_to(ROOT)),
                    "status": status,
                    "retrieved_at": retrieved_at,
                    "bytes": len(payload) if payload is not None else "",
                    "sha256": sha256(payload) if payload is not None else "",
                }
            )

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    refreshed = sum(row["status"] == "refreshed" for row in rows)
    print(f"Saved: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Refreshed blocks: {refreshed}/{len(rows)} for {observation_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
