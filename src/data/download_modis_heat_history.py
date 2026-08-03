#!/usr/bin/env python3
"""Download the assessed 2021-2025 MODIS heat-history granules.

Inputs are fixed by ``assess_modis_heat_history.py``. NASA Earthdata
credentials are read by earthaccess from the user's existing netrc file.
"""
from __future__ import annotations

import csv
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlparse

import earthaccess


ROOT = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "data/exp/modis-heat-history/granule_inventory.csv"
OUTPUT_ROOT = ROOT / "data/raw/weather/modis_lst_8day_2021_2025"
MANIFEST_PATH = ROOT / "data/raw/_manifests/kumamoto_modis_lst_2021_2025.csv"


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if not INVENTORY_PATH.exists():
        raise FileNotFoundError(
            "Run src/data/assess_modis_heat_history.py before downloading."
        )

    with INVENTORY_PATH.open(encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle))
    if not inventory:
        raise ValueError("The MODIS assessment inventory is empty.")

    auth = earthaccess.login(strategy="netrc")
    if not auth.authenticated:
        raise RuntimeError("NASA Earthdata authentication failed.")

    for short_name in sorted({row["short_name"] for row in inventory}):
        product_rows = [row for row in inventory if row["short_name"] == short_name]
        product_dir = OUTPUT_ROOT / short_name
        product_dir.mkdir(parents=True, exist_ok=True)
        urls = [row["hdf_url"] for row in product_rows]
        downloaded = earthaccess.download(
            urls,
            local_path=product_dir,
            provider="LPCLOUD",
            threads=4,
            show_progress=True,
        )
        if len(downloaded) != len(urls):
            raise RuntimeError(
                f"Expected {len(urls)} {short_name} files, received {len(downloaded)}."
            )

    manifest_rows: list[dict[str, object]] = []
    for row in inventory:
        filename = Path(urlparse(row["hdf_url"]).path).name
        path = OUTPUT_ROOT / row["short_name"] / filename
        if not path.exists() or path.stat().st_size == 0:
            raise FileNotFoundError(f"Missing downloaded granule: {path}")
        manifest_rows.append(
            {
                "short_name": row["short_name"],
                "version": row["version"],
                "historical_year": row["historical_year"],
                "window_start": row["window_start"],
                "window_end": row["window_end"],
                "granule_id": row["granule_id"],
                "source_url": row["hdf_url"],
                "relative_path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": file_sha256(path),
                "status": "downloaded_or_kept",
            }
        )

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]))
        writer.writeheader()
        writer.writerows(manifest_rows)

    total_bytes = sum(int(row["bytes"]) for row in manifest_rows)
    print(f"Saved: {MANIFEST_PATH.relative_to(ROOT)}")
    print(
        f"Downloaded or kept {len(manifest_rows)} HDF files "
        f"({total_bytes / 1024 / 1024:.1f} MiB)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
