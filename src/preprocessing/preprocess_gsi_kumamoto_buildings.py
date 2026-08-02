#!/usr/bin/env python3
"""Decode Kumamoto GSI vector tiles into a unique polygon GeoParquet layer.

The GSI building layer contains both polygons and outline lines, and tiles have a
small buffer.  This script keeps polygonal geometry only and assigns ownership to
the nominal tile containing each polygon's representative point.  The result is a
mapped-building polygon layer, not a dwelling inventory or damage classification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import geopandas as gpd
import mapbox_vector_tile
import mercantile
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from pyproj import CRS, Transformer
from shapely import make_valid, normalize, to_wkb
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, shape
from shapely.prepared import prep


ROOT = Path(__file__).resolve().parents[2]
TILE_ROOT = ROOT / "data/raw/buildings/gsi_vector_2026-04-01/z15"
OUTPUT = ROOT / "data/processed/kumamoto_gsi_buildings_z15_preprocessed.parquet"
SUMMARY = ROOT / "data/exp/spatial-foundation/building_preprocessing_summary.json"
BOUNDARY = ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
ZOOM = 15
EXTENT = 4096.0


def polygonal_part(geometry):
    """Return only polygonal components after validity repair."""
    if geometry.is_empty:
        return None
    if not geometry.is_valid:
        geometry = make_valid(geometry)
    if isinstance(geometry, (Polygon, MultiPolygon)):
        return geometry
    if isinstance(geometry, GeometryCollection):
        polygons = [part for part in geometry.geoms if isinstance(part, Polygon)]
        if not polygons:
            return None
        return polygons[0] if len(polygons) == 1 else MultiPolygon(polygons)
    return None


def tile_transformer(tile: mercantile.Tile):
    """Create a vector-tile-coordinate to longitude/latitude callback."""
    bounds = mercantile.xy_bounds(tile)
    to_lonlat = Transformer.from_crs(3857, 4326, always_xy=True)
    width = bounds.right - bounds.left
    height = bounds.top - bounds.bottom

    def transform(x: float, y: float) -> tuple[float, float]:
        web_x = bounds.left + (x / EXTENT) * width
        web_y = bounds.top - (y / EXTENT) * height
        return to_lonlat.transform(web_x, web_y)

    return transform


def owned_by_tile(point, tile: mercantile.Tile) -> bool:
    """Apply a half-open ownership rule to remove buffered-tile duplicates."""
    bounds = mercantile.bounds(tile)
    return (
        bounds.west <= point.x < bounds.east
        and bounds.south < point.y <= bounds.north
    )


def crosses_nominal_bounds(geometry, tile: mercantile.Tile) -> bool:
    bounds = mercantile.bounds(tile)
    min_x, min_y, max_x, max_y = geometry.bounds
    return (
        min_x < bounds.west
        or min_y < bounds.south
        or max_x > bounds.east
        or max_y > bounds.north
    )


def schema() -> pa.Schema:
    geo = {
        "version": "1.0.0",
        "primary_column": "geometry",
        "columns": {
            "geometry": {
                "encoding": "WKB",
                "geometry_types": ["Polygon", "MultiPolygon"],
                "crs": CRS.from_epsg(6668).to_json_dict(),
            }
        },
    }
    return pa.schema(
        [
            ("Building ID", pa.string()),
            ("Source Zoom", pa.int16()),
            ("Source Tile X", pa.int32()),
            ("Source Tile Y", pa.int32()),
            ("Feature Code", pa.int32()),
            ("Source Map Scale Level", pa.string()),
            ("Building Area m2", pa.float64()),
            ("Crosses Nominal Tile Boundary", pa.bool_()),
            ("geometry", pa.binary()),
        ],
        metadata={b"geo": json.dumps(geo).encode("utf-8")},
    )


def write_chunk(
    records: list[dict], writer: pq.ParquetWriter, seen_ids: set[str]
) -> tuple[int, int]:
    if not records:
        return 0, 0
    frame = gpd.GeoDataFrame(records, geometry="geometry", crs=6668)
    frame["Building Area m2"] = frame.to_crs(6670).area.to_numpy()
    geometry_wkb = to_wkb(frame.geometry.array, hex=False)
    building_ids = [
        "gsi-" + hashlib.blake2b(to_wkb(normalize(geom)), digest_size=12).hexdigest()
        for geom in frame.geometry
    ]
    new_ids: set[str] = set()
    keep_values = []
    for building_id in building_ids:
        retained = building_id not in seen_ids and building_id not in new_ids
        keep_values.append(retained)
        if retained:
            new_ids.add(building_id)
    keep = np.asarray(keep_values, dtype=bool)
    duplicate_count = int((~keep).sum())
    frame = frame.loc[keep].copy()
    geometry_wkb = geometry_wkb[keep]
    kept_ids = [building_id for building_id, retained in zip(building_ids, keep, strict=True) if retained]
    seen_ids.update(kept_ids)
    frame["Building ID"] = kept_ids
    arrays = {
        "Building ID": frame["Building ID"].tolist(),
        "Source Zoom": frame["Source Zoom"].tolist(),
        "Source Tile X": frame["Source Tile X"].tolist(),
        "Source Tile Y": frame["Source Tile Y"].tolist(),
        "Feature Code": frame["Feature Code"].tolist(),
        "Source Map Scale Level": frame["Source Map Scale Level"].tolist(),
        "Building Area m2": frame["Building Area m2"].tolist(),
        "Crosses Nominal Tile Boundary": frame[
            "Crosses Nominal Tile Boundary"
        ].tolist(),
        "geometry": geometry_wkb.tolist(),
    }
    writer.write_table(pa.Table.from_pydict(arrays, schema=writer.schema))
    return len(frame), duplicate_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tile-root", type=Path, default=TILE_ROOT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--summary", type=Path, default=SUMMARY)
    parser.add_argument("--boundary", type=Path, default=BOUNDARY)
    parser.add_argument("--chunk-tiles", type=int, default=40)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    tile_paths = sorted(args.tile_root.glob("*/*.pbf"))
    tile_paths = tile_paths[args.start :]
    if args.limit is not None:
        tile_paths = tile_paths[: args.limit]
    if not tile_paths:
        raise FileNotFoundError(f"No PBF tiles found under {args.tile_root}")
    prefecture = gpd.read_file(args.boundary)[["geometry"]].to_crs(6668)
    prefecture_boundary = prep(prefecture.geometry.union_all())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    part = args.output.with_suffix(args.output.suffix + ".part")
    part.unlink(missing_ok=True)

    metrics = {
        "source_tiles": len(tile_paths),
        "raw_building_features": 0,
        "non_polygon_features_excluded": 0,
        "polygon_features_outside_owner_tile_excluded": 0,
        "polygon_features_outside_kumamoto_excluded": 0,
        "invalid_or_empty_polygon_features_excluded": 0,
        "exact_geometry_duplicates_excluded": 0,
        "mapped_building_polygons": 0,
        "polygons_crossing_nominal_tile_boundary": 0,
    }
    records: list[dict] = []
    seen_ids: set[str] = set()
    with pq.ParquetWriter(part, schema(), compression="zstd") as writer:
        for number, path in enumerate(tile_paths, start=1):
            x = int(path.parent.name)
            y = int(path.stem)
            tile = mercantile.Tile(x=x, y=y, z=ZOOM)
            decoded = mapbox_vector_tile.decode(
                path.read_bytes(),
                per_layer_options={
                    "building": {"transformer": tile_transformer(tile)}
                },
            )
            features = decoded.get("building", {}).get("features", [])
            metrics["raw_building_features"] += len(features)
            for feature in features:
                geometry_type = feature.get("geometry", {}).get("type")
                if geometry_type not in {"Polygon", "MultiPolygon"}:
                    metrics["non_polygon_features_excluded"] += 1
                    continue
                geometry = polygonal_part(shape(feature["geometry"]))
                if geometry is None:
                    metrics["invalid_or_empty_polygon_features_excluded"] += 1
                    continue
                point = geometry.representative_point()
                if not owned_by_tile(point, tile):
                    metrics["polygon_features_outside_owner_tile_excluded"] += 1
                    continue
                if not prefecture_boundary.covers(point):
                    metrics["polygon_features_outside_kumamoto_excluded"] += 1
                    continue
                crosses = crosses_nominal_bounds(geometry, tile)
                properties = feature.get("properties", {})
                records.append(
                    {
                        "Building ID": None,
                        "Source Zoom": ZOOM,
                        "Source Tile X": x,
                        "Source Tile Y": y,
                        "Feature Code": properties.get("ftCode"),
                        "Source Map Scale Level": properties.get("orgGILvl"),
                        "Building Area m2": None,
                        "Crosses Nominal Tile Boundary": crosses,
                        "geometry": geometry,
                    }
                )
                metrics["polygons_crossing_nominal_tile_boundary"] += int(crosses)

            if number % args.chunk_tiles == 0 or number == len(tile_paths):
                written, duplicates = write_chunk(records, writer, seen_ids)
                metrics["mapped_building_polygons"] += written
                metrics["exact_geometry_duplicates_excluded"] += duplicates
                records.clear()
            if number % 250 == 0 or number == len(tile_paths):
                print(
                    f"tiles {number:,}/{len(tile_paths):,}; "
                    f"buildings {metrics['mapped_building_polygons']:,}",
                    flush=True,
                )

    part.replace(args.output)
    with args.summary.open("w", encoding="utf-8") as stream:
        json.dump(metrics, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"Saved {metrics['mapped_building_polygons']:,} buildings -> {args.output}")
    print(f"Summary -> {args.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
