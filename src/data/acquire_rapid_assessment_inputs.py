#!/usr/bin/env python3
"""Acquire official inputs for the Kumamoto rapid heat-protection assessment.

The script is resumable: existing non-empty source files are kept. It downloads
the prefecture-wide GSI shelter layers, the mapped surface-displacement boundary,
and only the GSI vector-map tiles intersecting Kumamoto Prefecture at a selected zoom.
The vector tiles contain the pre-event building layer current on 2026-04-01.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import mapbox_vector_tile
import mercantile
from shapely.geometry import box


SNAPSHOT_DATE = "2026-08-02"
VECTOR_DATA_DATE = "2026-04-01"
DEFAULT_VECTOR_ZOOM = 15
USER_AGENT = "KE01-kumamoto-rapid-assessment/1.0"


@dataclass(frozen=True)
class Source:
    dataset_id: str
    url: str
    relative_path: str
    role: str
    limitation: str


STATIC_SOURCES = (
    Source(
        "gsi-shelter-publication-prefecture-list",
        "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/publicHistoryCSV/prefectureListData.csv",
        "data/raw/shelters/gsi_designated_2026-08-02/prefectureListData.csv",
        "Verify the GSI publication date for each prefecture.",
        "Publication date is not the date on which each facility was field-verified.",
    ),
    Source(
        "gsi-kumamoto-designated-shelters-geojson",
        "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/geoJSON/43000_1.geojson",
        "data/raw/shelters/gsi_designated_2026-08-02/43000_1_designated_shelters.geojson",
        "Prefecture-wide locations and basic attributes for designated shelters.",
        "No HVAC, generator, capacity, occupancy, or current-opening fields.",
    ),
    Source(
        "gsi-kumamoto-designated-shelters-csv",
        "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv/43000_1.csv",
        "data/raw/shelters/gsi_designated_2026-08-02/43000_1_designated_shelters.csv",
        "Tabular copy of the prefecture-wide designated-shelter layer.",
        "Municipalities must be contacted to confirm current operational status.",
    ),
    Source(
        "gsi-kumamoto-emergency-evacuation-sites-geojson",
        "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/geoJSON/43000_2.geojson",
        "data/raw/shelters/gsi_designated_2026-08-02/43000_2_emergency_evacuation_sites.geojson",
        "Prefecture-wide designated emergency evacuation sites by hazard type.",
        "An emergency evacuation site is not necessarily a shelter for overnight stay.",
    ),
    Source(
        "gsi-kumamoto-emergency-evacuation-sites-csv",
        "https://hinanmap.gsi.go.jp/hinanjocp/defaultFtpData/csv/43000_2.csv",
        "data/raw/shelters/gsi_designated_2026-08-02/43000_2_emergency_evacuation_sites.csv",
        "Tabular copy of designated emergency evacuation sites.",
        "Hazard designation does not establish current availability after this earthquake.",
    ),
    Source(
        "gsi-2026-kumamoto-surface-displacement-boundary",
        "https://www.gsi.go.jp/common/000279851.pdf",
        "data/raw/earthquake/2026-07-28_kumamoto/gsi/surface_displacement_boundary_2026-07-31.pdf",
        "Official interpreted boundary of earthquake-related surface displacement.",
        "PDF map, not a machine-readable fault or building-damage layer.",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path, retries: int = 4) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and destination.stat().st_size > 0:
        return "kept"

    part = destination.with_suffix(destination.suffix + ".part")
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
                str(retries),
                "--connect-timeout",
                "30",
                "--max-time",
                "180",
                "--user-agent",
                USER_AGENT,
                "--output",
                str(part),
                url,
            ],
            check=False,
        )
        if result.returncode == 0 and part.is_file() and part.stat().st_size > 0:
            part.replace(destination)
            return "downloaded"
        part.unlink(missing_ok=True)
        raise RuntimeError(f"curl failed with exit code {result.returncode}: {url}")

    for attempt in range(retries):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                with part.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
            if part.stat().st_size == 0:
                raise OSError("empty response")
            part.replace(destination)
            return "downloaded"
        except (OSError, TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
            part.unlink(missing_ok=True)
            if attempt + 1 == retries:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"download failed: {url}")


def kumamoto_tiles(
    boundary_path: Path, vector_zoom: int
) -> list[mercantile.Tile]:
    boundary = gpd.read_file(boundary_path).to_crs(4326).geometry.union_all()
    west, south, east, north = boundary.bounds
    candidates = mercantile.tiles(west, south, east, north, zooms=[vector_zoom])
    selected = []
    for tile in candidates:
        bounds = mercantile.bounds(tile)
        tile_polygon = box(bounds.west, bounds.south, bounds.east, bounds.north)
        if boundary.intersects(tile_polygon):
            selected.append(tile)
    return selected


def vector_tile_url(tile: mercantile.Tile) -> str:
    return (
        "https://cyberjapandata.gsi.go.jp/xyz/experimental_bvmap/"
        f"{tile.z}/{tile.x}/{tile.y}.pbf"
    )


def acquire_tile(root: Path, tile: mercantile.Tile) -> dict[str, str | int]:
    relative = Path(
        "data/raw/buildings/gsi_vector_2026-04-01"
    ) / f"z{tile.z}" / str(tile.x) / f"{tile.y}.pbf"
    path = root / relative
    status = download(vector_tile_url(tile), path)
    decoded = mapbox_vector_tile.decode(path.read_bytes())
    building_count = len(decoded.get("building", {}).get("features", []))
    return {
        "z": tile.z,
        "x": tile.x,
        "y": tile.y,
        "relative_path": str(relative),
        "status": status,
        "bytes": path.stat().st_size,
        "building_fragment_count": building_count,
        "sha256": sha256(path),
        "source_url": vector_tile_url(tile),
    }


def write_csv(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        raise ValueError(f"no records for {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--vector-zoom", type=int, default=DEFAULT_VECTOR_ZOOM)
    parser.add_argument("--skip-buildings", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    boundary_path = (
        root
        / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
    )
    if not boundary_path.is_file():
        raise FileNotFoundError(boundary_path)

    source_records: list[dict[str, object]] = []
    for source in STATIC_SOURCES:
        path = root / source.relative_path
        status = download(source.url, path)
        source_records.append(
            {
                "dataset_id": source.dataset_id,
                "snapshot_date": SNAPSHOT_DATE,
                "source_url": source.url,
                "relative_path": source.relative_path,
                "status": status,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "role": source.role,
                "limitation": source.limitation,
            }
        )

    tiles: list[mercantile.Tile] = []
    tile_records: list[dict[str, object]] = []
    if not args.skip_buildings:
        tiles = kumamoto_tiles(boundary_path, args.vector_zoom)
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            pending = {executor.submit(acquire_tile, root, tile): tile for tile in tiles}
            for completed, future in enumerate(as_completed(pending), start=1):
                tile_records.append(future.result())
                if completed % 100 == 0 or completed == len(pending):
                    print(f"building tiles: {completed}/{len(pending)}", flush=True)
        tile_records.sort(key=lambda row: (int(row["x"]), int(row["y"])))
        write_csv(
            root
            / (
                "data/raw/buildings/gsi_vector_2026-04-01/"
                f"tile_index_z{args.vector_zoom}.csv"
            ),
            tile_records,
        )
        source_records.append(
            {
                "dataset_id": (
                    "gsi-vector-kumamoto-building-tiles-"
                    f"z{args.vector_zoom}"
                ),
                "snapshot_date": SNAPSHOT_DATE,
                "source_url": "https://cyberjapandata.gsi.go.jp/xyz/experimental_bvmap/{z}/{x}/{y}.pbf",
                "relative_path": (
                    "data/raw/buildings/gsi_vector_2026-04-01/"
                    f"z{args.vector_zoom}"
                ),
                "status": "downloaded-or-kept",
                "bytes": sum(int(row["bytes"]) for row in tile_records),
                "sha256": f"see tile_index_z{args.vector_zoom}.csv",
                "role": "Pre-event building polygons for damage-probability and exposure aggregation.",
                "limitation": (
                    "Experimental vector map; geometries are clipped at tile boundaries, "
                    "so fragment counts are not building counts."
                ),
            }
        )

    write_csv(
        root / "data/raw/_manifests/kumamoto_2026_rapid_assessment.csv",
        source_records,
    )
    summary = {
        "snapshot_date": SNAPSHOT_DATE,
        "vector_data_date": VECTOR_DATA_DATE,
        "vector_zoom": args.vector_zoom,
        "static_sources": len(STATIC_SOURCES),
        "building_tiles": len(tile_records),
        "building_fragments_in_tiles": sum(
            int(row["building_fragment_count"]) for row in tile_records
        ),
        "building_tile_bytes": sum(int(row["bytes"]) for row in tile_records),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
