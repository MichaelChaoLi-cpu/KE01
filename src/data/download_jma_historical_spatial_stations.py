#!/usr/bin/env python3
"""Download 2021-2025 summer daily observations for Kumamoto stations.

The station set is restricted to active JMA sites in Kumamoto Prefecture that
reported air temperature during the full study baseline.  Existing non-empty
files are retained, and every source file is recorded with a SHA-256 digest.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "data/raw/weather/jma_daily_html"
MANIFEST_PATH = (
    ROOT
    / "data/raw/_manifests/kumamoto_jma_historical_spatial_stations_2021_2025.csv"
)
USER_AGENT = "KE01-research-data-acquisition/1.0"

# slug: (AMeDAS station ID, ETRN page type, ETRN block number)
STATIONS = {
    "kahoku": ("86006", "a1", "0832"),
    "minami-oguni": ("86066", "a1", "0833"),
    "taimei": ("86086", "a1", "0834"),
    "kikuchi": ("86101", "a1", "0835"),
    "aso-otohime": ("86111", "a1", "1240"),
    "kumamoto": ("86141", "s1", "47819"),
    "mashiki": ("86146", "a1", "0923"),
    "takamori": ("86161", "a1", "0840"),
    "misumi": ("86216", "a1", "1081"),
    "kosa": ("86236", "a1", "0842"),
    "matsushima": ("86271", "a1", "0843"),
    "hondo": ("86316", "a1", "0845"),
    "yatsushiro": ("86336", "a1", "0846"),
    "minamata": ("86451", "a1", "0924"),
    "hitoyoshi": ("86467", "s1", "47824"),
    "ue": ("86477", "a1", "0926"),
    "ushibuka": ("86491", "s1", "47838"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_size > 0:
        return "kept"

    temporary = destination.with_suffix(destination.suffix + ".part")
    curl = shutil.which("curl")
    if not curl:
        raise RuntimeError("curl is required for JMA acquisition")
    result = subprocess.run(
        [
            curl,
            "--fail",
            "--location",
            "--silent",
            "--show-error",
            "--retry",
            "2",
            "--connect-timeout",
            "30",
            "--max-time",
            "180",
            "--user-agent",
            USER_AGENT,
            "--output",
            str(temporary),
            url,
        ],
        check=False,
    )
    if result.returncode != 0 or not temporary.is_file() or temporary.stat().st_size == 0:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"JMA download failed ({result.returncode}): {url}")
    temporary.replace(destination)
    return "downloaded"


def main() -> int:
    rows: list[dict[str, object]] = []
    retrieved_at = datetime.now().astimezone().isoformat(timespec="seconds")
    for slug, (station_id, page_type, block_no) in STATIONS.items():
        for year in range(2021, 2026):
            for month in (7, 8):
                url = (
                    "https://www.data.jma.go.jp/stats/etrn/view/"
                    f"daily_{page_type}.php?prec_no=86&block_no={block_no}"
                    f"&year={year}&month={month}&day=&view=p1"
                )
                path = OUTPUT_ROOT / slug / f"{year}_{month:02d}.html"
                status = download(url, path)
                rows.append(
                    {
                        "station_id": station_id,
                        "station_slug": slug,
                        "etrn_page_type": page_type,
                        "etrn_block_no": block_no,
                        "year": year,
                        "month": month,
                        "source_url": url,
                        "relative_path": str(path.relative_to(ROOT)),
                        "status": status,
                        "retrieved_at": retrieved_at,
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path),
                    }
                )

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved: {MANIFEST_PATH.relative_to(ROOT)}")
    print(
        f"Stations: {len(STATIONS)}; files: {len(rows)}; "
        f"bytes: {sum(int(row['bytes']) for row in rows):,}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
