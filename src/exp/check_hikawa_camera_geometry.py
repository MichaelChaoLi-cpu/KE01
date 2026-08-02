#!/usr/bin/env python3
"""Create a geometry-informed orientation check for HIK-V-0034.

This is a visual geolocation diagnostic.  It uses the photograph EXIF altitude and
35 mm-equivalent focal length to approximate its ground footprint, centres that
footprint on the recorded GPS position, and renders four cardinal rotations over
the available 2020 GSI annual orthophoto.  It does not classify damage.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import ExifTags, Image


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PHOTO_ID = "HIK-V-0034"
INDEX_CSV = PROJECT_ROOT / "data/exp/gsi-imagery/triage/focal_imagery_review_index.csv"
PRE_DIR = PROJECT_ROOT / "data/raw/imagery/gsi_historical/hikawa_prepost_pilot/HIK-V-0034"
PRE_PATH = PRE_DIR / "nendophoto2020_z16_mosaic.jpg"
META_PATH = PRE_DIR / "mosaic_metadata.json"
OUTPUT_DIR = PROJECT_ROOT / "data/exp/gsi-imagery/hikawa_prepost_manual_check"
SENSOR_WIDTH_MM = 35.9
SENSOR_HEIGHT_MM = 23.9


def web_mercator_world_pixel(lon: float, lat: float, zoom: int) -> tuple[float, float]:
    scale = 256 * 2**zoom
    x = (lon + 180.0) / 360.0 * scale
    lat_rad = math.radians(lat)
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * scale
    return x, y


def read_camera(photo_path: Path) -> tuple[float, float]:
    with Image.open(photo_path) as image:
        exif = image.getexif()
        exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
        gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
        focal_35 = float(exif_ifd[41989])
        altitude = float(gps_ifd[6])
    return focal_35, altitude


def rotate_bound(image: np.ndarray, angle: float) -> tuple[np.ndarray, np.ndarray]:
    height, width = image.shape[:2]
    centre = (width / 2.0, height / 2.0)
    matrix = cv2.getRotationMatrix2D(centre, angle, 1.0)
    cosine, sine = abs(matrix[0, 0]), abs(matrix[0, 1])
    new_width = int(round(height * sine + width * cosine))
    new_height = int(round(height * cosine + width * sine))
    matrix[0, 2] += new_width / 2.0 - centre[0]
    matrix[1, 2] += new_height / 2.0 - centre[1]
    rotated = cv2.warpAffine(
        image, matrix, (new_width, new_height), flags=cv2.INTER_AREA,
        borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255),
    )
    mask = cv2.warpAffine(
        np.full((height, width), 255, np.uint8), matrix, (new_width, new_height),
        flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0,
    )
    return rotated, mask


def place_at_centre(
    foreground: np.ndarray, mask: np.ndarray, canvas_shape: tuple[int, int], centre: tuple[float, float]
) -> tuple[np.ndarray, np.ndarray]:
    canvas_height, canvas_width = canvas_shape
    output = np.full((canvas_height, canvas_width, 3), 255, np.uint8)
    output_mask = np.zeros((canvas_height, canvas_width), np.uint8)
    height, width = foreground.shape[:2]
    x0, y0 = int(round(centre[0] - width / 2)), int(round(centre[1] - height / 2))
    source_x0, source_y0 = max(0, -x0), max(0, -y0)
    target_x0, target_y0 = max(0, x0), max(0, y0)
    copy_width = min(width - source_x0, canvas_width - target_x0)
    copy_height = min(height - source_y0, canvas_height - target_y0)
    if copy_width <= 0 or copy_height <= 0:
        return output, output_mask
    source = np.s_[source_y0 : source_y0 + copy_height, source_x0 : source_x0 + copy_width]
    target = np.s_[target_y0 : target_y0 + copy_height, target_x0 : target_x0 + copy_width]
    output[target] = foreground[source]
    output_mask[target] = mask[source]
    return output, output_mask


def main() -> None:
    Image.MAX_IMAGE_PIXELS = None
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with INDEX_CSV.open(newline="", encoding="utf-8") as handle:
        indexed = {row["review_id"]: row for row in csv.DictReader(handle)}
    source = indexed[PHOTO_ID]
    lon, lat = float(source["longitude"]), float(source["latitude"])
    photo_path = PROJECT_ROOT / source["full_photo_path"]
    focal_35, altitude_m = read_camera(photo_path)

    with Image.open(photo_path) as opened:
        post = np.asarray(opened.convert("RGB"))
    with Image.open(PRE_PATH) as opened:
        pre = np.asarray(opened.convert("RGB"))
    metadata = json.loads(META_PATH.read_text(encoding="utf-8"))
    zoom = int(metadata["zoom"])

    # Use 35 mm frame dimensions with the EXIF 35 mm-equivalent focal length.
    footprint_width_m = altitude_m * SENSOR_WIDTH_MM / focal_35
    footprint_height_m = altitude_m * SENSOR_HEIGHT_MM / focal_35
    map_resolution = 156543.03392804097 * math.cos(math.radians(lat)) / 2**zoom
    target_width = int(round(footprint_width_m / map_resolution))
    target_height = int(round(footprint_height_m / map_resolution))
    post_scaled = cv2.resize(post, (target_width, target_height), interpolation=cv2.INTER_AREA)

    centre_tile_x = int((lon + 180.0) / 360.0 * 2**zoom)
    lat_rad = math.radians(lat)
    centre_tile_y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * 2**zoom)
    mosaic_origin = ((centre_tile_x - 4) * 256, (centre_tile_y - 4) * 256)
    world_x, world_y = web_mercator_world_pixel(lon, lat, zoom)
    centre_pixel = (world_x - mosaic_origin[0], world_y - mosaic_origin[1])

    figure, axes = plt.subplots(2, 2, figsize=(14, 14), constrained_layout=True)
    for axis, angle in zip(axes.flat, (0, 90, 180, 270), strict=True):
        rotated, mask = rotate_bound(post_scaled, angle)
        placed, placed_mask = place_at_centre(rotated, mask, pre.shape[:2], centre_pixel)
        overlap = placed_mask > 0
        overlay = pre.copy()
        overlay[overlap] = (0.50 * pre[overlap] + 0.50 * placed[overlap]).astype(np.uint8)
        axis.imshow(overlay)
        axis.scatter([centre_pixel[0]], [centre_pixel[1]], marker="+", s=90, c="red", linewidths=2)
        axis.set_title(f"Candidate rotation: {angle}°")
        axis.axis("off")
    figure.suptitle(
        f"{PHOTO_ID} geometry-informed check: altitude={altitude_m:.0f} m, "
        f"footprint≈{footprint_width_m/1000:.2f}×{footprint_height_m/1000:.2f} km",
        fontsize=14,
    )
    output_path = OUTPUT_DIR / f"{PHOTO_ID}_cardinal_orientation_check.png"
    figure.savefig(output_path, dpi=180, facecolor="white")
    plt.close(figure)

    diagnostics = {
        "photo_id": PHOTO_ID,
        "historical_year": 2020,
        "camera_longitude": lon,
        "camera_latitude": lat,
        "exif_altitude_m": altitude_m,
        "exif_focal_length_35mm_equivalent_mm": focal_35,
        "assumed_sensor_width_mm": SENSOR_WIDTH_MM,
        "assumed_sensor_height_mm": SENSOR_HEIGHT_MM,
        "estimated_footprint_width_m": footprint_width_m,
        "estimated_footprint_height_m": footprint_height_m,
        "map_resolution_m_per_px": map_resolution,
        "estimated_post_gsd_m_per_px": footprint_width_m / post.shape[1],
        "mosaic_centre_pixel_x": centre_pixel[0],
        "mosaic_centre_pixel_y": centre_pixel[1],
        "note": "Altitude is GPS altitude, not verified above-ground height; footprint is approximate.",
    }
    (OUTPUT_DIR / f"{PHOTO_ID}_geometry.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(diagnostics, ensure_ascii=False, indent=2))
    print(output_path.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()
