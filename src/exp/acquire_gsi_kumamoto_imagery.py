#!/usr/bin/env python3
"""Inventory and sample official GSI imagery for the 2026 Kumamoto earthquake.

The script first downloads the official layer definition and every event GeoJSON
catalogue. It extracts direct full-resolution photo URLs, downloads a small
representative sample from each photo layer, samples the continuous orthophoto,
and estimates full-photo download size from a bounded number of HEAD requests.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
import shutil
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "data/raw/imagery/gsi_2026_kumamoto"
CATALOG_DIR = OUTPUT_ROOT / "catalog"
SAMPLE_DIR = OUTPUT_ROOT / "samples"
THUMBNAIL_DIR = OUTPUT_ROOT / "thumbnails"
PHOTO_DIR = OUTPUT_ROOT / "photos"
LAYER_CONFIG_URL = (
    "https://maps.gsi.go.jp/layers_txt/layers_20260729kumamoto.txt"
)
USER_AGENT = "KE01-research/1.0 (official public data acquisition)"
PHOTO_BASE_URL = "https://saigai.gsi.go.jp/1/"


def request(url: str, method: str = "GET") -> urllib.request.Request:
    return urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})


def download(url: str, destination: Path) -> tuple[int, str]:
    """Download one source atomically and return byte count and SHA-256."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        digest = hashlib.sha256()
        with destination.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        return destination.stat().st_size, digest.hexdigest()
    temporary = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(request(url), timeout=90) as response, temporary.open(
        "wb"
    ) as stream:
        while chunk := response.read(1024 * 1024):
            stream.write(chunk)
            digest.update(chunk)
            size += len(chunk)
    temporary.replace(destination)
    return size, digest.hexdigest()


def load_json(url: str, destination: Path) -> dict[str, Any]:
    download(url, destination)
    with destination.open(encoding="utf-8") as stream:
        return json.load(stream)


def iter_layers(
    entries: Iterable[dict[str, Any]], group_path: tuple[str, ...] = ()
) -> Iterable[dict[str, Any]]:
    """Yield leaf layers while retaining their hierarchy."""
    for entry in entries:
        title = str(entry.get("title", "")).strip()
        if entry.get("type") == "LayerGroup":
            yield from iter_layers(entry.get("entries", []), (*group_path, title))
        elif entry.get("type") == "Layer" and entry.get("url"):
            layer = dict(entry)
            layer["group_path"] = list(group_path)
            yield layer


def tile_xy(longitude: float, latitude: float, zoom: int) -> tuple[int, int]:
    scale = 2**zoom
    x = int((longitude + 180.0) / 360.0 * scale)
    y = int(
        (
            1.0
            - math.asinh(math.tan(math.radians(latitude))) / math.pi
        )
        / 2.0
        * scale
    )
    return x, y


def catalogue_url(template: str, longitude: float, latitude: float) -> str:
    """Resolve the native GeoJSON tile containing the Kumamoto event."""
    zoom = 2
    x, y = tile_xy(longitude, latitude, zoom)
    return template.format(z=zoom, x=x, y=y)


def direct_photo_url(image_html: str) -> str | None:
    """Extract the full-resolution photo path from a GSI viewer link."""
    decoded = html.unescape(image_html)
    match = re.search(r'href="([^"]+)"', decoded)
    if not match:
        return None
    viewer_url = match.group(1)
    parsed = urllib.parse.urlparse(viewer_url)
    relative_path = urllib.parse.unquote(parsed.query).split("&", 1)[0]
    if not relative_path:
        return None
    return urllib.parse.urljoin(PHOTO_BASE_URL, relative_path)


def thumbnail_photo_url(image_html: str) -> str | None:
    """Extract the catalogue thumbnail URL."""
    decoded = html.unescape(image_html)
    match = re.search(r'<img[^>]+src="([^"]+)"', decoded)
    return match.group(1) if match else None


def safe_extension(url: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png"} else ".jpg"


def photo_rows(layer: dict[str, Any], catalogue: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for feature_index, feature in enumerate(catalogue.get("features", []), start=1):
        properties = feature.get("properties") or {}
        coordinates = (feature.get("geometry") or {}).get("coordinates") or [None, None]
        image_html = str(properties.get("画像", ""))
        image_url = direct_photo_url(image_html)
        if not image_url or image_url in seen_urls:
            continue
        seen_urls.add(image_url)
        photo_number = str(properties.get("写真番号") or feature_index).strip()
        rows.append(
            {
                "layer_id": layer["id"],
                "category": " / ".join(layer.get("group_path", [])),
                "layer_title": layer.get("title", ""),
                "photo_number": photo_number,
                "captured_at": properties.get("撮影日")
                or properties.get("撮影日時")
                or "",
                "longitude": coordinates[0],
                "latitude": coordinates[1],
                "photo_url": image_url,
                "thumbnail_url": thumbnail_photo_url(image_html) or "",
            }
        )
    return rows


def representative_rows(
    rows: list[dict[str, Any]], layer: dict[str, Any], count: int
) -> list[dict[str, Any]]:
    """Choose photos nearest the official layer centre."""
    if not rows or count <= 0:
        return []
    area = layer.get("area") or {}
    centre_lon = float(area.get("lng", rows[0]["longitude"]))
    centre_lat = float(area.get("lat", rows[0]["latitude"]))
    ordered = sorted(
        rows,
        key=lambda row: (float(row["longitude"]) - centre_lon) ** 2
        + (float(row["latitude"]) - centre_lat) ** 2,
    )
    if count >= len(ordered):
        return ordered
    positions = [round(index * (len(ordered) - 1) / (count - 1)) for index in range(count)] if count > 1 else [0]
    return [ordered[position] for position in positions]


def content_length(url: str) -> int | None:
    try:
        with urllib.request.urlopen(request(url, method="HEAD"), timeout=45) as response:
            value = response.headers.get("Content-Length")
            return int(value) if value else None
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def estimate_layer_bytes(
    rows: list[dict[str, Any]], sample_size: int, workers: int
) -> dict[str, dict[str, Any]]:
    by_layer: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_layer.setdefault(str(row["layer_id"]), []).append(row)

    output: dict[str, dict[str, Any]] = {}
    for layer_id, layer_rows in by_layer.items():
        if len(layer_rows) <= sample_size:
            selected = layer_rows
        else:
            indices = sorted(
                {
                    round(index * (len(layer_rows) - 1) / (sample_size - 1))
                    for index in range(sample_size)
                }
            ) if sample_size > 1 else [len(layer_rows) // 2]
            selected = [layer_rows[index] for index in indices]

        sizes: list[int] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(content_length, str(row["photo_url"])): row
                for row in selected
            }
            for future in as_completed(futures):
                value = future.result()
                if value is not None:
                    sizes.append(value)
        median_size = int(statistics.median(sizes)) if sizes else None
        output[layer_id] = {
            "photo_count": len(layer_rows),
            "head_samples_requested": len(selected),
            "head_samples_succeeded": len(sizes),
            "median_photo_bytes": median_size,
            "estimated_total_bytes": median_size * len(layer_rows)
            if median_size is not None
            else None,
        }
    return output


def download_photo_samples(
    rows: list[dict[str, Any]],
    layers_by_id: dict[str, dict[str, Any]],
    per_layer: int,
) -> list[dict[str, Any]]:
    by_layer: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_layer.setdefault(str(row["layer_id"]), []).append(row)

    downloaded: list[dict[str, Any]] = []
    for layer_id, layer_rows in by_layer.items():
        for row in representative_rows(layer_rows, layers_by_id[layer_id], per_layer):
            suffix = safe_extension(str(row["photo_url"]))
            destination = SAMPLE_DIR / layer_id / f"{row['photo_number']}{suffix}"
            size, sha256 = download(str(row["photo_url"]), destination)
            item = dict(row)
            item.update(
                {
                    "relative_path": str(destination.relative_to(ROOT)),
                    "bytes": size,
                    "sha256": sha256,
                }
            )
            downloaded.append(item)
    return downloaded


def download_thumbnail_item(row: dict[str, Any]) -> dict[str, Any]:
    item = dict(row)
    url = str(row.get("thumbnail_url", ""))
    if not url:
        item.update({"status": "missing_url", "relative_path": "", "bytes": 0, "sha256": ""})
        return item
    suffix = safe_extension(url)
    destination = (
        THUMBNAIL_DIR
        / str(row["layer_id"])
        / f"{row['photo_number']}{suffix}"
    )
    try:
        size, sha256 = download(url, destination)
        item.update(
            {
                "status": "kept",
                "relative_path": str(destination.relative_to(ROOT)),
                "bytes": size,
                "sha256": sha256,
            }
        )
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        item.update(
            {
                "status": "error",
                "relative_path": "",
                "bytes": 0,
                "sha256": "",
                "error": str(error),
            }
        )
    return item


def download_all_thumbnails(
    rows: list[dict[str, Any]], workers: int
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(download_thumbnail_item, row) for row in rows]
        for future in as_completed(futures):
            results.append(future.result())
    return sorted(results, key=lambda row: (str(row["layer_id"]), str(row["photo_number"])))


def safe_filename(value: str) -> str:
    """Return a filesystem-safe, stable photo identifier."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned.strip("._") or "photo"


def download_full_photo_item(row: dict[str, Any], attempts: int = 3) -> dict[str, Any]:
    """Download one full-resolution photo with bounded retries."""
    item = dict(row)
    url = str(row["photo_url"])
    suffix = safe_extension(url)
    destination = PHOTO_DIR / str(row["layer_id"]) / f"{safe_filename(str(row['photo_number']))}{suffix}"
    for attempt in range(1, attempts + 1):
        try:
            size, sha256 = download(url, destination)
            item.update(
                {
                    "status": "kept",
                    "relative_path": str(destination.relative_to(ROOT)),
                    "bytes": size,
                    "sha256": sha256,
                    "error": "",
                }
            )
            return item
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            if attempt == attempts:
                item.update(
                    {
                        "status": "error",
                        "relative_path": str(destination.relative_to(ROOT)),
                        "bytes": 0,
                        "sha256": "",
                        "error": str(error),
                    }
                )
                return item
            time.sleep(2 ** (attempt - 1))
    raise AssertionError("unreachable")


FULL_PHOTO_MANIFEST_FIELDS = [
    "layer_id",
    "category",
    "layer_title",
    "photo_number",
    "captured_at",
    "longitude",
    "latitude",
    "photo_url",
    "status",
    "relative_path",
    "bytes",
    "sha256",
    "error",
]


def load_completed_full_photos(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """Load valid completed rows from a prior manifest for fast resume."""
    if not path.exists():
        return {}
    completed: dict[tuple[str, str], dict[str, Any]] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row.get("status") != "kept" or not row.get("relative_path"):
                continue
            destination = ROOT / str(row["relative_path"])
            try:
                expected_size = int(row.get("bytes") or 0)
            except ValueError:
                continue
            if destination.is_file() and destination.stat().st_size == expected_size:
                completed[(str(row["layer_id"]), str(row["photo_number"]))] = row
    return completed


def download_all_full_photos(
    rows: list[dict[str, Any]], workers: int, min_free_gib: float
) -> tuple[list[dict[str, Any]], bool]:
    """Download all photos in checkpointed batches; return rows and pause state."""
    manifest_path = CATALOG_DIR / "full_photo_manifest.csv"
    completed = load_completed_full_photos(manifest_path)
    results: dict[tuple[str, str], dict[str, Any]] = dict(completed)
    pending = [
        row
        for row in rows
        if (str(row["layer_id"]), str(row["photo_number"])) not in completed
    ]
    reserve_bytes = int(min_free_gib * 1024**3)
    batch_size = max(workers * 4, 1)
    paused = False

    def checkpoint() -> None:
        ordered = sorted(
            results.values(),
            key=lambda row: (str(row["layer_id"]), str(row["photo_number"])),
        )
        write_csv(manifest_path, ordered, FULL_PHOTO_MANIFEST_FIELDS)

    if completed:
        print(f"Resuming from manifest: {len(completed):,} already complete", flush=True)

    for start in range(0, len(pending), batch_size):
        free_bytes = shutil.disk_usage(OUTPUT_ROOT).free
        if free_bytes < reserve_bytes:
            paused = True
            print(
                f"PAUSED_LOW_DISK: {free_bytes / 1024**3:.2f} GiB free; "
                f"reserve is {min_free_gib:.2f} GiB",
                flush=True,
            )
            break
        batch = pending[start : start + batch_size]
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(download_full_photo_item, row) for row in batch]
            for future in as_completed(futures):
                item = future.result()
                key = (str(item["layer_id"]), str(item["photo_number"]))
                results[key] = item
        checkpoint()
        kept = sum(row.get("status") == "kept" for row in results.values())
        errors = sum(row.get("status") == "error" for row in results.values())
        kept_bytes = sum(
            int(row.get("bytes") or 0)
            for row in results.values()
            if row.get("status") == "kept"
        )
        free_gib = shutil.disk_usage(OUTPUT_ROOT).free / 1024**3
        print(
            f"Full photos: {kept:,}/{len(rows):,} kept, {errors:,} errors, "
            f"{kept_bytes / 1024**3:.2f} GiB stored, {free_gib:.2f} GiB free",
            flush=True,
        )

    checkpoint()
    return list(results.values()), paused


def download_orthophoto_sample(layer: dict[str, Any], zoom: int = 18) -> list[dict[str, Any]]:
    """Download a 3 x 3 orthophoto sample around the official layer centre."""
    area = layer.get("area") or {}
    centre_x, centre_y = tile_xy(float(area["lng"]), float(area["lat"]), zoom)
    downloaded: list[dict[str, Any]] = []
    for x in range(centre_x - 1, centre_x + 2):
        for y in range(centre_y - 1, centre_y + 2):
            url = str(layer["url"]).format(z=zoom, x=x, y=y)
            destination = SAMPLE_DIR / str(layer["id"]) / str(zoom) / str(x) / f"{y}.png"
            try:
                size, sha256 = download(url, destination)
            except urllib.error.HTTPError as error:
                if error.code == 404:
                    continue
                raise
            downloaded.append(
                {
                    "layer_id": layer["id"],
                    "category": " / ".join(layer.get("group_path", [])),
                    "layer_title": layer.get("title", ""),
                    "photo_number": f"z{zoom}-{x}-{y}",
                    "captured_at": "2026-07-29",
                    "longitude": "",
                    "latitude": "",
                    "photo_url": url,
                    "relative_path": str(destination.relative_to(ROOT)),
                    "bytes": size,
                    "sha256": sha256,
                }
            )
    return downloaded


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-per-photo-layer", type=int, default=1)
    parser.add_argument("--estimate-samples-per-layer", type=int, default=5)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--download-all-thumbnails", action="store_true")
    parser.add_argument("--download-all-photos", action="store_true")
    parser.add_argument("--min-free-gib", type=float, default=3.0)
    args = parser.parse_args()

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    layer_config_path = CATALOG_DIR / "layers_20260729kumamoto.json"
    configuration = load_json(LAYER_CONFIG_URL, layer_config_path)
    layers = list(iter_layers(configuration.get("layers", [])))
    layers_by_id = {str(layer["id"]): layer for layer in layers}

    all_photo_rows: list[dict[str, Any]] = []
    layer_inventory: list[dict[str, Any]] = []
    orthophoto_layers: list[dict[str, Any]] = []
    for layer in layers:
        template = str(layer["url"])
        group = " / ".join(layer.get("group_path", []))
        inventory_row = {
            "layer_id": layer["id"],
            "category": group,
            "layer_title": layer.get("title", ""),
            "url_template": template,
            "min_zoom": layer.get("minZoom", ""),
            "max_zoom": layer.get("maxZoom", ""),
            "feature_count": "",
            "photo_count": 0,
        }
        if template.endswith(".geojson"):
            area = layer.get("area") or {"lng": 130.7, "lat": 32.7}
            url = catalogue_url(template, float(area["lng"]), float(area["lat"]))
            destination = CATALOG_DIR / f"{layer['id']}.geojson"
            catalogue = load_json(url, destination)
            rows = photo_rows(layer, catalogue)
            inventory_row["feature_count"] = len(catalogue.get("features", []))
            inventory_row["photo_count"] = len(rows)
            all_photo_rows.extend(rows)
        elif template.endswith(".png") and "正射画像" in group:
            orthophoto_layers.append(layer)
        layer_inventory.append(inventory_row)

    write_csv(
        CATALOG_DIR / "layer_inventory.csv",
        layer_inventory,
        [
            "layer_id",
            "category",
            "layer_title",
            "url_template",
            "min_zoom",
            "max_zoom",
            "feature_count",
            "photo_count",
        ],
    )
    write_csv(
        CATALOG_DIR / "photo_catalog.csv",
        all_photo_rows,
        [
            "layer_id",
            "category",
            "layer_title",
            "photo_number",
            "captured_at",
            "longitude",
            "latitude",
            "photo_url",
            "thumbnail_url",
        ],
    )

    estimates = estimate_layer_bytes(
        all_photo_rows, args.estimate_samples_per_layer, args.workers
    )
    estimate_path = CATALOG_DIR / "photo_download_estimates.json"
    estimate_path.write_text(
        json.dumps(estimates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    samples = download_photo_samples(
        all_photo_rows, layers_by_id, args.sample_per_photo_layer
    )
    for layer in orthophoto_layers:
        samples.extend(download_orthophoto_sample(layer))
    write_csv(
        CATALOG_DIR / "sample_manifest.csv",
        samples,
        [
            "layer_id",
            "category",
            "layer_title",
            "photo_number",
            "captured_at",
            "longitude",
            "latitude",
            "photo_url",
            "relative_path",
            "bytes",
            "sha256",
        ],
    )

    thumbnails: list[dict[str, Any]] = []
    if args.download_all_thumbnails:
        thumbnails = download_all_thumbnails(all_photo_rows, args.workers)
        write_csv(
            CATALOG_DIR / "thumbnail_manifest.csv",
            thumbnails,
            [
                "layer_id",
                "category",
                "layer_title",
                "photo_number",
                "captured_at",
                "longitude",
                "latitude",
                "thumbnail_url",
                "status",
                "relative_path",
                "bytes",
                "sha256",
                "error",
            ],
        )

    full_photos: list[dict[str, Any]] = []
    paused_low_disk = False
    if args.download_all_photos:
        full_photos, paused_low_disk = download_all_full_photos(
            all_photo_rows, args.workers, args.min_free_gib
        )

    estimated_total = sum(
        value["estimated_total_bytes"] or 0 for value in estimates.values()
    )
    print(f"Official event layers: {len(layers)}")
    print(f"Photo layers: {len(estimates)}")
    print(f"Catalogued full-resolution photos: {len(all_photo_rows):,}")
    print(f"Sample files downloaded: {len(samples):,}")
    print(f"Sample bytes: {sum(int(row['bytes']) for row in samples):,}")
    print(f"Estimated all-photo bytes: {estimated_total:,}")
    if thumbnails:
        kept = [row for row in thumbnails if row.get("status") == "kept"]
        print(f"Thumbnails downloaded: {len(kept):,} / {len(thumbnails):,}")
        print(f"Thumbnail bytes: {sum(int(row['bytes']) for row in kept):,}")
    if full_photos:
        kept = [row for row in full_photos if row.get("status") == "kept"]
        errors = [row for row in full_photos if row.get("status") == "error"]
        print(f"Full photos downloaded: {len(kept):,} / {len(all_photo_rows):,}")
        print(f"Full photo errors: {len(errors):,}")
        print(f"Full photo bytes: {sum(int(row['bytes']) for row in kept):,}")
    print(f"Saved metadata -> {CATALOG_DIR.relative_to(ROOT)}")
    return 75 if paused_low_disk else 0


if __name__ == "__main__":
    raise SystemExit(main())
