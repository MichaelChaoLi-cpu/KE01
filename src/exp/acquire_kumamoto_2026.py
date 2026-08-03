#!/usr/bin/env python3
"""Acquire an immutable first-pass dataset bundle for the 2026 Kumamoto earthquake.

Only public, official endpoints that do not require credentials are used here. Existing
non-empty files are preserved. A SHA-256 manifest is written after acquisition.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path


EVENT_DATE = date(2026, 7, 28)
SNAPSHOT_END = date(2026, 8, 3)
USER_AGENT = "KE01-research-data-acquisition/1.0"


def download(url: str, destination: Path, *, optional: bool = False) -> str:
    """Download to a temporary file and atomically move it into place."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_size > 0:
        return "kept"

    temporary = destination.with_suffix(destination.suffix + ".part")
    curl = shutil.which("curl")
    if curl:
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
        if result.returncode == 0 and temporary.is_file() and temporary.stat().st_size > 0:
            temporary.replace(destination)
            return "downloaded"
        temporary.unlink(missing_ok=True)
        if optional:
            return "unavailable"
        raise RuntimeError(f"curl failed with exit code {result.returncode}: {url}")

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            with temporary.open("wb") as stream:
                shutil.copyfileobj(response, stream)
        temporary.replace(destination)
        return "downloaded"
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        temporary.unlink(missing_ok=True)
        if optional:
            return "unavailable"
        raise


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_archive(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if member.is_dir():
                continue
            target = destination / Path(member.filename).name
            if target.is_file() and target.stat().st_size > 0:
                continue
            with bundle.open(member) as source, target.open("wb") as output:
                shutil.copyfileobj(source, output)


def date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    raw = root / "data" / "raw"
    records: list[dict[str, str]] = []

    static_sources = [
        {
            "dataset_id": "fdma-earthquake-report-15",
            "url": "https://www.fdma.go.jp/disaster/info/items/20260728kumamotojishin15.pdf",
            "path": raw / "earthquake" / "2026-07-28_kumamoto" / "fdma" / "fdma_report_15_2026-07-29.pdf",
            "note": "Preliminary national fire and disaster management damage report; values may be revised.",
        },
        {
            "dataset_id": "gsi-event-page",
            "url": "https://www.gsi.go.jp/BOUSAI/20260728_kumamoto_earthquake.html",
            "path": raw / "earthquake" / "2026-07-28_kumamoto" / "gsi" / "gsi_event_page_2026-08-02.html",
            "note": "Snapshot of the GSI catalogue for aerial imagery and geospatial disaster products.",
        },
        {
            "dataset_id": "estat-population-mesh-T001231-43",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?statsId=T001231&code=43&downloadType=2",
            "path": raw / "population" / "estat_2020_T001231_kumamoto" / "estat_T001231_43.zip",
            "note": "2020 Census mesh statistics for Kumamoto Prefecture, including population aged 65+.",
        },
        {
            "dataset_id": "estat-population-mesh-T001231-definition",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?datatype=1&statsId=T001231&downloadType=1",
            "path": raw / "population" / "estat_2020_T001231_kumamoto" / "T001231_definition.pdf",
            "note": "Official e-Stat field and disclosure-rule definition for the T001231 reference table.",
        },
        {
            "dataset_id": "estat-mesh-boundary-E-4829",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=E&code=4829&coordSys=1&format=shape&downloadType=5",
            "path": raw / "boundaries" / "estat_mesh_E_kumamoto" / "EDDSWE4829.zip",
            "note": "Official latitude-longitude Shapefile boundary package for first-order mesh M4829.",
        },
        {
            "dataset_id": "estat-mesh-boundary-E-4830",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=E&code=4830&coordSys=1&format=shape&downloadType=5",
            "path": raw / "boundaries" / "estat_mesh_E_kumamoto" / "EDDSWE4830.zip",
            "note": "Official latitude-longitude Shapefile boundary package for first-order mesh M4830.",
        },
        {
            "dataset_id": "estat-mesh-boundary-E-4831",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=E&code=4831&coordSys=1&format=shape&downloadType=5",
            "path": raw / "boundaries" / "estat_mesh_E_kumamoto" / "EDDSWE4831.zip",
            "note": "Official latitude-longitude Shapefile boundary package for first-order mesh M4831.",
        },
        {
            "dataset_id": "estat-mesh-boundary-E-4930",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=E&code=4930&coordSys=1&format=shape&downloadType=5",
            "path": raw / "boundaries" / "estat_mesh_E_kumamoto" / "EDDSWE4930.zip",
            "note": "Official latitude-longitude Shapefile boundary package for first-order mesh M4930.",
        },
        {
            "dataset_id": "estat-mesh-boundary-E-4931",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=E&code=4931&coordSys=1&format=shape&downloadType=5",
            "path": raw / "boundaries" / "estat_mesh_E_kumamoto" / "EDDSWE4931.zip",
            "note": "Official latitude-longitude Shapefile boundary package for first-order mesh M4931.",
        },
        {
            "dataset_id": "estat-2020-small-area-boundary-kumamoto",
            "url": "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A002005212020&code=43&coordSys=1&format=shape&downloadType=5&datum=2011",
            "path": raw / "boundaries" / "estat_2020_small_area_kumamoto" / "A002005212020DDSWC43-JGD2011.zip",
            "note": "Official 2020 Census small-area Shapefile package for all of Kumamoto Prefecture.",
        },
        {
            "dataset_id": "jma-amedas-station-table",
            "url": "https://www.jma.go.jp/bosai/amedas/const/amedastable.json",
            "path": raw / "weather" / "jma_amedas" / "stations" / "amedastable_2026-08-02.json",
            "note": "JMA AMeDAS station metadata snapshot.",
        },
        {
            "dataset_id": "fdma-heatstroke-pre-event-week",
            "url": "https://www.fdma.go.jp/disaster/heatstroke/items/r8/heatstroke_sokuhouti_20260720.pdf",
            "path": raw / "health" / "fdma_heatstroke" / "heatstroke_2026-07-20_to_2026-07-26_preliminary.pdf",
            "note": "Pre-event weekly heatstroke ambulance transport report with prefecture and age breakdowns.",
        },
    ]

    for source in static_sources:
        status = download(source["url"], source["path"])
        records.append(
            {
                "dataset_id": source["dataset_id"],
                "source_url": source["url"],
                "relative_path": str(source["path"].relative_to(root)),
                "status": status,
                "note": source["note"],
            }
        )

    population_archive = static_sources[2]["path"]
    extract_archive(population_archive, population_archive.parent / "extracted")

    for source in static_sources:
        if source["dataset_id"].startswith("estat-mesh-boundary-E-"):
            extract_archive(
                source["path"],
                source["path"].parent / "extracted" / source["path"].stem,
            )
        elif source["dataset_id"] == "estat-2020-small-area-boundary-kumamoto":
            extract_archive(source["path"], source["path"].parent / "extracted")

    stations = {
        "86141": "kumamoto",
        "86216": "misumi",
        "86236": "kosa",
        "86271": "matsushima",
        "86336": "yatsushiro",
    }
    for station_id, station_name in stations.items():
        for observation_date in date_range(EVENT_DATE, SNAPSHOT_END):
            day = observation_date.strftime("%Y%m%d")
            for block_hour in range(0, 24, 3):
                block = f"{block_hour:02d}"
                url = (
                    "https://www.jma.go.jp/bosai/amedas/data/point/"
                    f"{station_id}/{day}_{block}.json"
                )
                path = (
                    raw
                    / "weather"
                    / "jma_amedas"
                    / "event_window"
                    / station_name
                    / f"{day}_{block}.json"
                )
                status = download(url, path, optional=True)
                records.append(
                    {
                        "dataset_id": f"jma-amedas-{station_name}-{day}-{block}",
                        "source_url": url,
                        "relative_path": str(path.relative_to(root)),
                        "status": status,
                        "note": (
                            "JMA event-window three-hour block; values are arrays of value "
                            "and quality flag. Eight blocks form one complete day."
                        ),
                    }
                )

    historical_pages = {
        "kumamoto": (
            "daily_s1.php",
            "47819",
        ),
        "yatsushiro": (
            "daily_a1.php",
            "0846",
        ),
    }
    for station_name, (page, block_no) in historical_pages.items():
        for year in range(2021, 2027):
            for month in (7, 8):
                url = (
                    f"https://www.data.jma.go.jp/stats/etrn/view/{page}"
                    f"?prec_no=86&block_no={block_no}&year={year}&month={month}"
                    "&day=&view=p1"
                )
                path = (
                    raw
                    / "weather"
                    / "jma_daily_html"
                    / station_name
                    / f"{year}_{month:02d}.html"
                )
                status = download(url, path)
                records.append(
                    {
                        "dataset_id": f"jma-daily-{station_name}-{year}-{month:02d}",
                        "source_url": url,
                        "relative_path": str(path.relative_to(root)),
                        "status": status,
                        "note": "JMA monthly daily-observation table for same-season baseline construction.",
                    }
                )

    retrieved_at = datetime.now().astimezone().isoformat(timespec="seconds")
    manifest_path = raw / "_manifests" / "kumamoto_2026_initial.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "dataset_id",
                "source_url",
                "relative_path",
                "status",
                "retrieved_at",
                "bytes",
                "sha256",
                "note",
            ],
        )
        writer.writeheader()
        for record in records:
            path = root / record["relative_path"]
            available = path.is_file()
            writer.writerow(
                {
                    **record,
                    "retrieved_at": retrieved_at,
                    "bytes": path.stat().st_size if available else "",
                    "sha256": sha256(path) if available else "",
                }
            )

    summary = {
        "manifest": str(manifest_path),
        "downloaded_or_kept": sum(record["status"] != "unavailable" for record in records),
        "unavailable": sum(record["status"] == "unavailable" for record in records),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
