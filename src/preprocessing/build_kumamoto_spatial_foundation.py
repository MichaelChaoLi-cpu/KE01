#!/usr/bin/env python3
"""Join mapped buildings and facility accessibility to Kumamoto population grids."""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from shapely import STRtree, from_wkb, point_on_surface


ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data/processed"
EXPERIMENT = ROOT / "data/exp/spatial-foundation"

MESH_SOURCE = PROCESSED / "kumamoto_population_mesh_125m_preprocessed.parquet"
GROUP_SOURCE = PROCESSED / "kumamoto_population_disclosure_groups_preprocessed.parquet"
BUILDING_SOURCE = PROCESSED / "kumamoto_gsi_buildings_z15_preprocessed.parquet"
SHELTER_SOURCE = PROCESSED / "kumamoto_designated_shelters_geospatial_preprocessed.parquet"
EMERGENCY_SOURCE = PROCESSED / "kumamoto_emergency_evacuation_sites_geospatial_preprocessed.parquet"
SUPPORT_SOURCE = PROCESSED / "kumamoto_support_facilities_preprocessed.parquet"

MESH_OUTPUT = PROCESSED / "kumamoto_spatial_foundation_125m_preprocessed.parquet"
GROUP_OUTPUT = PROCESSED / "kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet"
SUMMARY = EXPERIMENT / "spatial_foundation_summary.json"
PROJECTED_CRS = 6670


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def aggregate_buildings(mesh: gpd.GeoDataFrame) -> tuple[np.ndarray, np.ndarray, dict]:
    """Count building representative points and sum footprint area by populated cell."""
    tree = STRtree(mesh.geometry.array)
    counts = np.zeros(len(mesh), dtype=np.int32)
    areas = np.zeros(len(mesh), dtype=np.float64)
    matched = 0
    total = 0
    parquet = pq.ParquetFile(BUILDING_SOURCE)
    for number, batch in enumerate(
        parquet.iter_batches(columns=["Building Area m2", "geometry"], batch_size=100_000),
        start=1,
    ):
        geometry = from_wkb(batch.column("geometry").to_numpy(zero_copy_only=False))
        points = point_on_surface(geometry)
        pairs = tree.query(points, predicate="within")
        point_index, mesh_index = pairs
        batch_areas = batch.column("Building Area m2").to_numpy(zero_copy_only=False)
        np.add.at(counts, mesh_index, 1)
        np.add.at(areas, mesh_index, batch_areas[point_index])
        matched += len(point_index)
        total += len(geometry)
        print(f"building batches {number}; processed {total:,}; matched {matched:,}", flush=True)
    return counts, areas, {
        "mapped_buildings_total": total,
        "mapped_buildings_in_populated_125m_cells": matched,
        "mapped_buildings_outside_populated_125m_cells": total - matched,
    }


def nearest(
    origins_projected,
    destinations: gpd.GeoDataFrame,
    id_column: str,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the nearest destination ID and straight-line distance in metres."""
    require(len(destinations) > 0, "Nearest-neighbour destination layer is empty")
    projected = destinations.to_crs(PROJECTED_CRS)
    tree = STRtree(projected.geometry.array)
    indices, distances = tree.query_nearest(
        origins_projected, all_matches=False, return_distance=True
    )
    origin_index, destination_index = indices
    require(
        np.array_equal(origin_index, np.arange(len(origins_projected))),
        "Nearest-neighbour output does not cover every origin",
    )
    ids = projected[id_column].astype("string").to_numpy()[destination_index]
    return ids, distances


def add_nearest_fields(mesh: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    projected_centres = mesh.to_crs(PROJECTED_CRS).geometry.centroid.array
    shelters = gpd.read_parquet(SHELTER_SOURCE)
    emergency = gpd.read_parquet(EMERGENCY_SOURCE)
    support = gpd.read_parquet(SUPPORT_SOURCE)

    destination_sets = [
        (
            "Designated Shelter",
            shelters,
            "Common ID",
        ),
        (
            "Earthquake-Compatible Emergency Site",
            emergency.loc[emergency["Earthquake"].eq(1)],
            "Common ID",
        ),
        (
            "Medical Institution",
            support.loc[support["Support Facility Type"].eq("Medical Institution")],
            "Support Facility ID",
        ),
        (
            "Welfare Facility",
            support.loc[support["Support Facility Type"].eq("Welfare Facility")],
            "Support Facility ID",
        ),
        (
            "Public Office or Hall",
            support.loc[support["Support Facility Type"].eq("Public Office or Hall")],
            "Support Facility ID",
        ),
        (
            "School",
            support.loc[support["Support Facility Type"].eq("School")],
            "Support Facility ID",
        ),
    ]
    for label, destinations, id_column in destination_sets:
        ids, distances = nearest(projected_centres, destinations, id_column)
        mesh[f"Nearest {label} ID"] = pd.array(ids, dtype="string")
        mesh[f"Nearest {label} Distance m"] = distances
    return mesh


def group_nearest_fields(mesh: gpd.GeoDataFrame, groups: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    distance_columns = [column for column in mesh if column.endswith(" Distance m")]
    for distance_column in distance_columns:
        label = distance_column.removeprefix("Nearest ").removesuffix(" Distance m")
        id_column = f"Nearest {label} ID"
        indices = mesh.groupby("Disclosure Group Code")[distance_column].idxmin()
        lookup = mesh.loc[
            indices, ["Disclosure Group Code", id_column, distance_column]
        ]
        groups = groups.merge(
            lookup, on="Disclosure Group Code", how="left", validate="one_to_one"
        )
    return gpd.GeoDataFrame(groups, geometry="geometry", crs=groups.crs)


def main() -> int:
    EXPERIMENT.mkdir(parents=True, exist_ok=True)
    mesh = gpd.read_parquet(MESH_SOURCE)
    groups = gpd.read_parquet(GROUP_SOURCE)
    require(mesh["Mesh Code"].is_unique, "Mesh Code is not unique")
    require(groups["Disclosure Group Code"].is_unique, "Disclosure Group Code is not unique")

    building_count, building_area, summary = aggregate_buildings(mesh)
    mesh["Mapped Building Count"] = building_count
    mesh["Mapped Building Footprint Area m2"] = building_area
    mesh = add_nearest_fields(mesh)

    group_buildings = (
        mesh.groupby("Disclosure Group Code", as_index=False)
        .agg(
            **{
                "Mapped Building Count": ("Mapped Building Count", "sum"),
                "Mapped Building Footprint Area m2": (
                    "Mapped Building Footprint Area m2",
                    "sum",
                ),
            }
        )
    )
    groups = groups.merge(
        group_buildings,
        on="Disclosure Group Code",
        how="left",
        validate="one_to_one",
    )
    groups = group_nearest_fields(mesh, groups)

    mesh.to_parquet(MESH_OUTPUT, index=False)
    groups.to_parquet(GROUP_OUTPUT, index=False)
    summary.update(
        {
            "populated_125m_cells": len(mesh),
            "disclosure_groups": len(groups),
            "125m_cells_with_mapped_buildings": int((building_count > 0).sum()),
            "straight_line_distance_crs": f"EPSG:{PROJECTED_CRS}",
            "outputs": [
                str(MESH_OUTPUT.relative_to(ROOT)),
                str(GROUP_OUTPUT.relative_to(ROOT)),
            ],
        }
    )
    with SUMMARY.open("w", encoding="utf-8") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
