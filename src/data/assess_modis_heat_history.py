#!/usr/bin/env python3
"""Assess the minimal MODIS LST archive needed for Kumamoto heat mapping.

This script queries NASA CMR through earthaccess. It does not download granules.
The assessment covers the matching July 28-August 26 window in 2021-2025 for
Terra and Aqua 1 km, 8-day Collection 6.1 land-surface-temperature products.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import warnings

import earthaccess


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "data/exp/modis-heat-history"
INVENTORY_PATH = OUTPUT_DIR / "granule_inventory.csv"
SUMMARY_PATH = OUTPUT_DIR / "assessment_summary.json"

PRODUCTS = {
    "MOD11A2": "Terra MODIS 8-Day Land Surface Temperature",
    "MYD11A2": "Aqua MODIS 8-Day Land Surface Temperature",
}
VERSION = "061"
YEARS = range(2021, 2026)
BOUNDING_BOX = (129.85, 31.95, 131.40, 33.35)


def hdf_link(granule: earthaccess.results.DataGranule) -> str:
    links = [link for link in granule.data_links() if link.lower().endswith(".hdf")]
    if len(links) != 1:
        raise ValueError(f"Expected one HDF link, found {len(links)}")
    return links[0]


def main() -> int:
    rows: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()

    warnings.filterwarnings("ignore", category=FutureWarning, module="earthaccess")
    for short_name, long_name in PRODUCTS.items():
        for year in YEARS:
            start = f"{year}-07-28"
            end = f"{year}-08-26"
            results = earthaccess.search_data(
                short_name=short_name,
                version=VERSION,
                bounding_box=BOUNDING_BOX,
                temporal=(start, end),
            )
            for granule in results:
                granule_id = str(granule.get("umm", {}).get("GranuleUR", ""))
                key = (short_name, granule_id)
                if not granule_id or key in seen:
                    continue
                seen.add(key)
                rows.append(
                    {
                        "short_name": short_name,
                        "product_name": long_name,
                        "version": VERSION,
                        "historical_year": year,
                        "window_start": start,
                        "window_end": end,
                        "granule_id": granule_id,
                        "cmr_concept_id": granule.get("meta", {}).get("concept-id", ""),
                        "size_mb": float(granule.get("size") or 0.0),
                        "hdf_url": hdf_link(granule),
                    }
                )

    rows.sort(key=lambda row: (str(row["short_name"]), str(row["granule_id"])))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with INVENTORY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    product_summary: dict[str, dict[str, object]] = {}
    for short_name, long_name in PRODUCTS.items():
        product_rows = [row for row in rows if row["short_name"] == short_name]
        product_summary[short_name] = {
            "product_name": long_name,
            "granules": len(product_rows),
            "estimated_download_mb": round(
                sum(float(row["size_mb"]) for row in product_rows), 3
            ),
            "years": sorted({int(row["historical_year"]) for row in product_rows}),
        }

    summary = {
        "query_only": True,
        "download_started": False,
        "version": VERSION,
        "bounding_box_wgs84": list(BOUNDING_BOX),
        "annual_window": "July 28-August 26",
        "historical_years": list(YEARS),
        "products": product_summary,
        "total_granules": len(rows),
        "estimated_total_download_mb": round(
            sum(float(row["size_mb"]) for row in rows), 3
        ),
        "recommended_layers": [
            "LST_Day_1km",
            "LST_Night_1km",
            "QC_Day",
            "QC_Night",
            "Day_view_time",
            "Night_view_time",
        ],
        "interpretation_limit": (
            "MODIS land-surface temperature is a spatial covariate and is not "
            "near-surface air temperature, indoor temperature, or a forecast."
        ),
    }
    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Saved: {INVENTORY_PATH.relative_to(ROOT)}")
    print(f"Saved: {SUMMARY_PATH.relative_to(ROOT)}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
