#!/usr/bin/env python3
"""Download 2020-2024 Kumamoto municipality-by-age mortality tables.

The source is e-Stat Vital Statistics final data, prefectural retained table 1.
Files are kept byte-for-byte in CP932 encoding. Existing valid files are not
overwritten unless --force is supplied.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data/raw/_manifests/kumamoto_mortality_2020_2024.csv"
STAT_INF_IDS = {
    2020: "000032119560",
    2021: "000032243689",
    2022: "000040098534",
    2023: "000040206370",
    2024: "000040316738",
}


def target_path(year: int) -> Path:
    return ROOT / (
        f"data/raw/mortality/estat_vital_statistics_{year}_kumamoto/nc10043.csv"
    )


def source_url(stat_inf_id: str) -> str:
    return (
        "https://www.e-stat.go.jp/stat-search/file-download?"
        f"fileKind=1&statInfId={stat_inf_id}"
    )


def validate(path: Path) -> None:
    text = path.read_bytes().decode("cp932")
    if "死亡数" not in text or "熊本県" not in text or "市区町村" not in text:
        raise ValueError(f"Unexpected e-Stat table content: {path}")


def download(year: int, stat_inf_id: str, force: bool) -> dict[str, object]:
    path = target_path(year)
    path.parent.mkdir(parents=True, exist_ok=True)
    status = "kept"
    if force or not path.is_file():
        request = urllib.request.Request(
            source_url(stat_inf_id),
            headers={"User-Agent": "KE01-research-data-acquisition/1.0"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        path.write_bytes(payload)
        status = "downloaded"
    validate(path)
    payload = path.read_bytes()
    return {
        "year": year,
        "stat_inf_id": stat_inf_id,
        "source_url": source_url(stat_inf_id),
        "relative_path": str(path.relative_to(ROOT)),
        "status": status,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "encoding": "cp932",
        "table": (
            "Deaths by prefecture, health center/municipality, sex, and "
            "five-year age group"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    rows = [download(year, stat_id, args.force) for year, stat_id in STAT_INF_IDS.items()]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Validated {len(rows)} e-Stat files")
    print(f"Wrote {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
