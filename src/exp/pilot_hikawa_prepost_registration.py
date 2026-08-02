#!/usr/bin/env python3
"""Test low-cost pre/post registration for five Hikawa vertical photographs.

The script finds the latest available pre-2026 GSI annual orthophoto at each camera
centre, downloads a broad z16 mosaic, and estimates a coarse projective registration
with SIFT feature matches.  It is a feasibility test, not damage classification.
"""

from __future__ import annotations

import csv
import json
import math
import urllib.error
import urllib.request
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INDEX_CSV = PROJECT_ROOT / "data/exp/gsi-imagery/triage/focal_imagery_review_index.csv"
RAW_DIR = PROJECT_ROOT / "data/raw/imagery/gsi_historical/hikawa_prepost_pilot"
OUTPUT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_prepost_pilot"

PHOTO_IDS = ["HIK-V-0013", "HIK-V-0014", "HIK-V-0018", "HIK-V-0022", "HIK-V-0034"]
YEARS = list(range(2025, 2017, -1))
# A 9 x 9 mosaic at z16 spans roughly 4.6 km at Hikawa latitude.  That is close to
# the footprint visible in the oblique 2026 photographs and is therefore better for
# coarse registration than the earlier z18 (roughly 1.1 km) trial.
ZOOM = 16
RADIUS_TILES = 4
TILE_SIZE = 256
USER_AGENT = "KE01-research-prepost-pilot/1.0"


def lonlat_to_tile(lon: float, lat: float, zoom: int) -> tuple[int, int]:
    scale = 2**zoom
    x = int((lon + 180.0) / 360.0 * scale)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * scale)
    return x, y


def tile_to_lonlat(x: float, y: float, zoom: int) -> tuple[float, float]:
    scale = 2**zoom
    lon = x / scale * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / scale))))
    return lon, lat


def tile_url(year: int, x: int, y: int) -> str:
    return f"https://cyberjapandata.gsi.go.jp/xyz/nendophoto{year}/{ZOOM}/{x}/{y}.png"


def fetch(url: str) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return None
    if len(data) < 100:
        return None
    return data


def decode_tile(data: bytes | None) -> np.ndarray | None:
    if data is None:
        return None
    image = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_UNCHANGED)
    if image is None:
        return None
    if image.ndim == 3 and image.shape[2] == 4:
        alpha = image[:, :, 3]
        if int(alpha.max()) == 0:
            return None
        rgb = cv2.cvtColor(image[:, :, :3], cv2.COLOR_BGR2RGB)
        rgb[alpha == 0] = 255
        return rgb
    if image.ndim == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)


def latest_available_year(x: int, y: int) -> tuple[int | None, list[dict[str, str]]]:
    checks: list[dict[str, str]] = []
    selected = None
    for year in YEARS:
        data = fetch(tile_url(year, x, y))
        available = decode_tile(data) is not None
        checks.append({"year": str(year), "centre_tile_available": "yes" if available else "no"})
        if available and selected is None:
            selected = year
    return selected, checks


def build_mosaic(photo_id: str, year: int, centre_x: int, centre_y: int) -> tuple[np.ndarray, np.ndarray, dict]:
    width_tiles = RADIUS_TILES * 2 + 1
    mosaic = np.full((width_tiles * TILE_SIZE, width_tiles * TILE_SIZE, 3), 255, np.uint8)
    valid = np.zeros((width_tiles * TILE_SIZE, width_tiles * TILE_SIZE), np.uint8)
    available_tiles = 0
    for row, y in enumerate(range(centre_y - RADIUS_TILES, centre_y + RADIUS_TILES + 1)):
        for col, x in enumerate(range(centre_x - RADIUS_TILES, centre_x + RADIUS_TILES + 1)):
            tile = decode_tile(fetch(tile_url(year, x, y)))
            if tile is None:
                continue
            if tile.shape[:2] != (TILE_SIZE, TILE_SIZE):
                tile = cv2.resize(tile, (TILE_SIZE, TILE_SIZE), interpolation=cv2.INTER_AREA)
            y0, x0 = row * TILE_SIZE, col * TILE_SIZE
            mosaic[y0 : y0 + TILE_SIZE, x0 : x0 + TILE_SIZE] = tile
            valid[y0 : y0 + TILE_SIZE, x0 : x0 + TILE_SIZE] = 255
            available_tiles += 1

    west, north = tile_to_lonlat(centre_x - RADIUS_TILES, centre_y - RADIUS_TILES, ZOOM)
    east, south = tile_to_lonlat(
        centre_x + RADIUS_TILES + 1, centre_y + RADIUS_TILES + 1, ZOOM
    )
    metadata = {
        "photo_id": photo_id,
        "year": year,
        "zoom": ZOOM,
        "tile_radius": RADIUS_TILES,
        "available_tiles": available_tiles,
        "total_tiles": width_tiles**2,
        "west": west,
        "south": south,
        "east": east,
        "north": north,
    }
    photo_raw_dir = RAW_DIR / photo_id
    photo_raw_dir.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mosaic).save(photo_raw_dir / f"nendophoto{year}_z{ZOOM}_mosaic.jpg", quality=94)
    (photo_raw_dir / "mosaic_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return mosaic, valid, metadata


def resize_for_matching(image: np.ndarray, max_dimension: int = 2304) -> tuple[np.ndarray, float]:
    height, width = image.shape[:2]
    scale = min(1.0, max_dimension / max(height, width))
    if scale == 1.0:
        return image, scale
    resized = cv2.resize(
        image,
        (int(round(width * scale)), int(round(height * scale))),
        interpolation=cv2.INTER_AREA,
    )
    return resized, scale


def register(post_rgb: np.ndarray, pre_rgb: np.ndarray, valid_mask: np.ndarray) -> dict:
    post_small, scale = resize_for_matching(post_rgb)
    post_gray = cv2.cvtColor(post_small, cv2.COLOR_RGB2GRAY)
    pre_gray = cv2.cvtColor(pre_rgb, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    post_gray = clahe.apply(post_gray)
    pre_gray = clahe.apply(pre_gray)

    sift = cv2.SIFT_create(nfeatures=20000, contrastThreshold=0.01, edgeThreshold=20)
    key_post, desc_post = sift.detectAndCompute(post_gray, None)
    key_pre, desc_pre = sift.detectAndCompute(pre_gray, valid_mask)
    if desc_post is None or desc_pre is None:
        return {"status": "failed_no_descriptors", "post_scale": scale}

    matcher = cv2.BFMatcher(cv2.NORM_L2)
    forward = matcher.knnMatch(desc_post, desc_pre, k=2)
    # The two sources differ strongly in viewing angle, season, and ground sampling
    # distance.  A one-way 0.85 Lowe ratio retains enough candidates for RANSAC to
    # find the common footprint; the previous mutual 0.75 filter was too restrictive.
    candidates = [m for m, n in forward if m.distance < 0.85 * n.distance]
    if len(candidates) < 8:
        return {
            "status": "failed_too_few_matches",
            "post_scale": scale,
            "keypoints_post": len(key_post),
            "keypoints_pre": len(key_pre),
            "ratio_matches": len(candidates),
        }

    source_points = np.float32([key_post[m.queryIdx].pt for m in candidates]).reshape(-1, 1, 2)
    target_points = np.float32([key_pre[m.trainIdx].pt for m in candidates]).reshape(-1, 1, 2)
    homography, inlier_mask = cv2.findHomography(
        source_points, target_points, cv2.RANSAC, 5.0, maxIters=10000, confidence=0.999
    )
    if homography is None or inlier_mask is None:
        return {
            "status": "failed_homography",
            "post_scale": scale,
            "keypoints_post": len(key_post),
            "keypoints_pre": len(key_pre),
            "ratio_matches": len(candidates),
        }
    inliers = inlier_mask.ravel().astype(bool)
    projected = cv2.perspectiveTransform(source_points[inliers], homography)
    residuals = np.linalg.norm(projected[:, 0] - target_points[inliers, 0], axis=1)
    rmse_px = float(np.sqrt(np.mean(residuals**2)))
    inlier_count = int(inliers.sum())
    inlier_ratio = inlier_count / len(candidates)

    post_height, post_width = post_small.shape[:2]
    pre_height, pre_width = pre_rgb.shape[:2]
    post_corners = np.float32(
        [[[0, 0]], [[post_width - 1, 0]], [[post_width - 1, post_height - 1]], [[0, post_height - 1]]]
    )
    projected_corners = cv2.perspectiveTransform(post_corners, homography)[:, 0]
    projected_area_ratio = abs(cv2.contourArea(projected_corners)) / (pre_width * pre_height)

    # A few repeated road or roof textures can yield a tiny residual while collapsing
    # the whole photograph into one point.  Reject such geometrically degenerate
    # solutions before considering the feature-count thresholds.
    if projected_area_ratio < 0.01 or projected_area_ratio > 8.0:
        status = "failed_degenerate_homography"
    elif inlier_count >= 100 and rmse_px <= 3.0:
        status = "good_global_match"
    elif inlier_count >= 30 and rmse_px <= 6.0:
        status = "usable_global_match"
    elif inlier_count >= 15 and rmse_px <= 10.0:
        status = "tentative_global_match"
    else:
        status = "failed_quality_threshold"
    return {
        "status": status,
        "post_scale": scale,
        "keypoints_post": len(key_post),
        "keypoints_pre": len(key_pre),
        "ratio_matches": len(candidates),
        "inliers": inlier_count,
        "inlier_ratio": inlier_ratio,
        "rmse_px": rmse_px,
        "projected_area_ratio": projected_area_ratio,
        "homography": homography,
        "post_small": post_small,
    }


def ground_resolution_m(lat: float, zoom: int) -> float:
    return 156543.03392804097 * math.cos(math.radians(lat)) / 2**zoom


def save_preview(photo_id: str, year: int, post_rgb: np.ndarray, pre_rgb: np.ndarray, result: dict) -> str:
    homography = result["homography"]
    post_small = result["post_small"]
    height, width = pre_rgb.shape[:2]
    warped = cv2.warpPerspective(post_small, homography, (width, height))
    warped_mask = cv2.warpPerspective(
        np.full(post_small.shape[:2], 255, np.uint8), homography, (width, height)
    )
    overlay = pre_rgb.copy()
    overlap = warped_mask > 0
    overlay[overlap] = (0.5 * pre_rgb[overlap] + 0.5 * warped[overlap]).astype(np.uint8)
    pre_gray = cv2.cvtColor(pre_rgb, cv2.COLOR_RGB2GRAY)
    post_gray = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)
    difference = cv2.absdiff(pre_gray, post_gray)
    difference[~overlap] = 0

    figure, axes = plt.subplots(1, 4, figsize=(18, 5.2), constrained_layout=True)
    axes[0].imshow(pre_rgb)
    axes[0].set_title(f"Pre-event GSI orthophoto ({year})")
    axes[1].imshow(warped)
    axes[1].set_title("2026 post-event photo, warped")
    axes[2].imshow(overlay)
    axes[2].set_title("50% alignment overlay")
    axes[3].imshow(difference, cmap="magma", vmin=0, vmax=100)
    axes[3].set_title("Raw grayscale difference")
    for axis in axes:
        axis.axis("off")
    figure.suptitle(
        f"{photo_id}: {result['status']}; inliers={result['inliers']}; "
        f"RMSE={result['rmse_px']:.2f} px",
        fontsize=13,
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{photo_id}_registration_preview.png"
    figure.savefig(path, dpi=170, facecolor="white")
    plt.close(figure)
    return str(path.relative_to(PROJECT_ROOT))


def write_csv(path: Path, rows: list[dict]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        indexed = {row["review_id"]: row for row in csv.DictReader(handle)}

    availability_rows: list[dict] = []
    metric_rows: list[dict] = []
    for photo_id in PHOTO_IDS:
        source = indexed[photo_id]
        lon, lat = float(source["longitude"]), float(source["latitude"])
        centre_x, centre_y = lonlat_to_tile(lon, lat, ZOOM)
        year, checks = latest_available_year(centre_x, centre_y)
        for check in checks:
            availability_rows.append(
                {
                    "review_id": photo_id,
                    "longitude": lon,
                    "latitude": lat,
                    **check,
                }
            )
        if year is None:
            metric_rows.append(
                {
                    "review_id": photo_id,
                    "status": "no_pre_event_annual_tile_2018_2025",
                    "selected_year": "",
                }
            )
            print(f"{photo_id}: no annual orthophoto at centre for 2018-2025", flush=True)
            continue

        pre_rgb, valid_mask, metadata = build_mosaic(photo_id, year, centre_x, centre_y)
        with Image.open(PROJECT_ROOT / source["full_photo_path"]) as opened:
            post_rgb = np.asarray(opened.convert("RGB"))
        result = register(post_rgb, pre_rgb, valid_mask)
        resolution = ground_resolution_m(lat, ZOOM)
        row = {
            "review_id": photo_id,
            "selected_year": year,
            "year_gap": 2026 - year,
            "status": result["status"],
            "camera_longitude": lon,
            "camera_latitude": lat,
            "source_post_path": source["full_photo_path"],
            "available_mosaic_tiles": metadata["available_tiles"],
            "total_mosaic_tiles": metadata["total_tiles"],
            "ground_resolution_m_per_px": f"{resolution:.4f}",
            "keypoints_post": result.get("keypoints_post", ""),
            "keypoints_pre": result.get("keypoints_pre", ""),
            "ratio_matches": result.get("ratio_matches", ""),
            "inliers": result.get("inliers", ""),
            "inlier_ratio": f"{result['inlier_ratio']:.4f}" if "inlier_ratio" in result else "",
            "rmse_px": f"{result['rmse_px']:.4f}" if "rmse_px" in result else "",
            "projected_area_ratio": (
                f"{result['projected_area_ratio']:.8g}"
                if "projected_area_ratio" in result
                else ""
            ),
            "estimated_rmse_m": (
                f"{result['rmse_px'] * resolution:.4f}" if "rmse_px" in result else ""
            ),
            "preview_path": "",
        }
        # Also render rejected homographies for visual diagnosis.  The filename and
        # figure title retain the failed status so these cannot be mistaken for
        # accepted registrations.
        if "homography" in result:
            row["preview_path"] = save_preview(photo_id, year, post_rgb, pre_rgb, result)
        metric_rows.append(row)
        print(
            f"{photo_id}: pre={year}, tiles={metadata['available_tiles']}/81, "
            f"status={result['status']}, inliers={result.get('inliers', 0)}, "
            f"rmse_px={result.get('rmse_px', float('nan')):.2f}",
            flush=True,
        )

    write_csv(OUTPUT_DIR / "annual_tile_availability.csv", availability_rows)
    write_csv(OUTPUT_DIR / "registration_metrics.csv", metric_rows)
    usable = sum(row["status"] in {"good_global_match", "usable_global_match"} for row in metric_rows)
    tentative = sum(row["status"] == "tentative_global_match" for row in metric_rows)
    centre_lat = float(indexed[PHOTO_IDS[0]]["latitude"])
    mosaic_width_km = (
        ground_resolution_m(centre_lat, ZOOM) * TILE_SIZE * (RADIUS_TILES * 2 + 1) / 1000
    )
    summary = f"""# Hikawa pre/post registration pilot

Five residential-context vertical photographs were tested against the latest available pre-2026 GSI annual orthophoto tile at each camera centre. The annual layers checked were 2018-2025 at zoom level {ZOOM}; each downloaded mosaic covers 9 by 9 tiles (approximately {mosaic_width_km:.1f} km by {mosaic_width_km:.1f} km at Hikawa latitude).

- Good or usable global registrations: {usable} of 5
- Tentative registrations: {tentative} of 5
- Failed or unavailable: {5 - usable - tentative} of 5

The SIFT/RANSAC residual measures consistency among matched visual features, not exact building-corner accuracy. Relief displacement, different camera geometry, shadows, vegetation, and construction between dates can cause local misalignment even when the global metric is good. Raw grayscale difference images are diagnostic only and must not be interpreted as earthquake damage without local building-level review.

Visual inspection of the diagnostic previews is required for rejected solutions. In this run, the apparent low residuals for HIK-V-0013 and HIK-V-0034 were produced by degenerate homographies that collapsed the post-event image footprint to nearly one point; they are false registrations and cannot support change detection.

See `registration_metrics.csv` for the selected historical year and quantitative results, and the generated `*_registration_preview.png` files for visual inspection.
"""
    (OUTPUT_DIR / "README.md").write_text(summary, encoding="utf-8")
    print(f"Wrote outputs to {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
