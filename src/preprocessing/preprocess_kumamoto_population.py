#!/usr/bin/env python3
"""Preprocess the 2020 e-Stat Kumamoto 125 m population mesh.

Outputs
-------
1. A populated-mesh layer containing exact, unsuppressed population and household
   totals for each 125 m cell.
2. A disclosure-group layer for age and vulnerable-household variables. Cells
   suppressed by e-Stat are dissolved into their official aggregation destination.

An asterisk in the source table is disclosure suppression, not zero. This script
never imputes suppressed values.
"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
POPULATION_SOURCE = (
    ROOT
    / "data/raw/population/estat_2020_T001231_kumamoto/extracted/tblT001231E43.txt"
)
MESH_ROOT = ROOT / "data/raw/boundaries/estat_mesh_E_kumamoto/extracted"
MESH_OUTPUT = ROOT / "data/processed/kumamoto_population_mesh_125m_preprocessed.parquet"
GROUP_OUTPUT = (
    ROOT / "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet"
)

RENAME_MAP = {
    "KEY_CODE": "Mesh Code",
    "HTKSYORI": "Disclosure Status",
    "HTKSAKI": "Aggregation Destination Mesh Code",
    "GASSAN": "Aggregated Source Mesh Codes",
    "T001231001": "Total Population",
    "T001231019": "Population Age 65+",
    "T001231022": "Population Age 75+",
    "T001231025": "Population Age 85+",
    "T001231034": "Total Households",
    "T001231035": "General Households",
    "T001231036": "One-Person Households",
    "T001231047": "Households with Member Age 65+",
    "T001231049": "Older Single-Person Households",
    "T001231050": "Older Couple Households",
}

EXACT_TOTAL_COLUMNS = [
    "Total Population",
    "Total Households",
    "General Households",
]

DISCLOSURE_GROUP_COUNT_COLUMNS = [
    "Population Age 65+",
    "Population Age 75+",
    "Population Age 85+",
    "One-Person Households",
    "Households with Member Age 65+",
    "Older Single-Person Households",
    "Older Couple Households",
]


def require(condition: bool, message: str) -> None:
    """Raise a validation error with an actionable message."""
    if not condition:
        raise ValueError(message)


def read_population() -> pd.DataFrame:
    """Read the CP932 table, discard its label row, and apply confirmed names."""
    population = pd.read_csv(
        POPULATION_SOURCE,
        encoding="cp932",
        skiprows=[1],
        dtype="string",
        low_memory=False,
    )
    missing = sorted(set(RENAME_MAP) - set(population.columns))
    require(not missing, f"Population source is missing columns: {missing}")

    population = population[list(RENAME_MAP)].rename(columns=RENAME_MAP)
    for column in [
        "Mesh Code",
        "Aggregation Destination Mesh Code",
        "Aggregated Source Mesh Codes",
    ]:
        population[column] = population[column].str.strip()

    numeric_columns = [
        "Disclosure Status",
        *EXACT_TOTAL_COLUMNS,
        *DISCLOSURE_GROUP_COUNT_COLUMNS,
    ]
    for column in numeric_columns:
        population[column] = pd.to_numeric(population[column], errors="coerce")

    require(population["Mesh Code"].notna().all(), "Mesh Code contains missing values")
    require(population["Mesh Code"].is_unique, "Mesh Code is not unique")
    require(
        set(population["Disclosure Status"].dropna().astype(int).unique()) == {0, 1, 2},
        "Unexpected disclosure status values",
    )
    require(
        population[EXACT_TOTAL_COLUMNS].notna().all().all(),
        "An exact population or household total is missing",
    )
    return population


def read_mesh_geometries(population_codes: pd.Series) -> gpd.GeoDataFrame:
    """Read the five prefecture-covering mesh files and retain populated cells."""
    paths = sorted(MESH_ROOT.glob("**/MESH0*.shp"))
    require(len(paths) == 5, f"Expected 5 mesh shapefiles, found {len(paths)}")

    target_codes = set(population_codes.astype(str))
    frames: list[gpd.GeoDataFrame] = []
    expected_crs = None
    for path in paths:
        frame = gpd.read_file(path, columns=["KEY_CODE", "geometry"])
        if expected_crs is None:
            expected_crs = frame.crs
        require(frame.crs == expected_crs, f"CRS mismatch in {path.name}")
        frame["KEY_CODE"] = frame["KEY_CODE"].astype("string")
        frame = frame.loc[frame["KEY_CODE"].isin(target_codes)]
        frames.append(frame)

    mesh = gpd.GeoDataFrame(
        pd.concat(frames, ignore_index=True), geometry="geometry", crs=expected_crs
    ).rename(columns={"KEY_CODE": "Mesh Code"})
    require(mesh["Mesh Code"].is_unique, "Boundary Mesh Code is not unique")

    missing_geometry = target_codes - set(mesh["Mesh Code"])
    require(
        not missing_geometry,
        f"Population meshes without geometry: {len(missing_geometry):,}",
    )
    return mesh


def validate_disclosure_links(population: pd.DataFrame) -> pd.Series:
    """Validate the official destination/source links and return group codes."""
    status = population["Disclosure Status"].astype("int8")
    source_rows = population.loc[status == 2]
    destination_rows = population.loc[status == 1]
    destination_codes = set(destination_rows["Mesh Code"])

    require(
        source_rows["Aggregation Destination Mesh Code"].notna().all(),
        "A suppressed source mesh lacks an aggregation destination",
    )
    unknown_destinations = (
        set(source_rows["Aggregation Destination Mesh Code"]) - destination_codes
    )
    require(
        not unknown_destinations,
        f"Suppressed meshes reference {len(unknown_destinations):,} unknown destinations",
    )

    linked_lists = source_rows.groupby("Aggregation Destination Mesh Code")[
        "Mesh Code"
    ].agg(list)
    linked = {destination: set(codes) for destination, codes in linked_lists.items()}
    mismatched_destinations: list[str] = []
    for destination_code, declared_text in zip(
        destination_rows["Mesh Code"],
        destination_rows["Aggregated Source Mesh Codes"],
        strict=True,
    ):
        declared = set(str(declared_text).split(";")) if pd.notna(declared_text) else set()
        if declared != linked.get(destination_code, set()):
            mismatched_destinations.append(destination_code)
    require(
        not mismatched_destinations,
        "Official disclosure links disagree for "
        f"{len(mismatched_destinations):,} destination meshes",
    )

    group_code = population["Mesh Code"].copy()
    group_code.loc[status == 2] = source_rows["Aggregation Destination Mesh Code"]
    return group_code.rename("Disclosure Group Code")


def build_mesh_layer(
    population: pd.DataFrame, mesh: gpd.GeoDataFrame, group_code: pd.Series
) -> gpd.GeoDataFrame:
    """Build exact totals at the original 125 m resolution."""
    columns = [
        "Mesh Code",
        "Disclosure Status",
        "Aggregation Destination Mesh Code",
        "Aggregated Source Mesh Codes",
        *EXACT_TOTAL_COLUMNS,
    ]
    exact = population[columns].copy()
    exact.insert(1, "Disclosure Group Code", group_code)
    group_sizes = exact.groupby("Disclosure Group Code")["Mesh Code"].transform("size")
    exact.insert(2, "Disclosure Group Size", group_sizes.astype("int32"))

    output = mesh.merge(exact, on="Mesh Code", how="inner", validate="one_to_one")
    require(len(output) == len(population), "Mesh/population merge changed the row count")
    require(output.geometry.notna().all(), "The mesh output contains missing geometry")
    return gpd.GeoDataFrame(output, geometry="geometry", crs=mesh.crs)


def build_disclosure_group_layer(
    population: pd.DataFrame, mesh_layer: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Dissolve source cells into the finest official disclosure geography."""
    working = mesh_layer[
        [
            "Mesh Code",
            "Disclosure Group Code",
            "Disclosure Status",
            *EXACT_TOTAL_COLUMNS,
            "geometry",
        ]
    ].merge(
        population[
            ["Mesh Code", *DISCLOSURE_GROUP_COUNT_COLUMNS]
        ],
        on="Mesh Code",
        how="left",
        validate="one_to_one",
    )

    status = working["Disclosure Status"].astype("int8")
    # Status 2 rows contain suppressed asterisks. Status 0 rows are exact; status 1
    # rows contain the official total for the whole disclosure group.
    detailed = working.loc[status != 2].set_index("Disclosure Group Code")
    require(detailed.index.is_unique, "A disclosure group has multiple detail records")
    require(
        detailed[DISCLOSURE_GROUP_COUNT_COLUMNS].notna().all().all(),
        "A disclosure-group detail value is missing after suppression handling",
    )

    exact_sums = working.groupby("Disclosure Group Code")[EXACT_TOTAL_COLUMNS].sum()
    member_stats = working.groupby("Disclosure Group Code").agg(
        **{
            "Disclosure Group Size": ("Mesh Code", "size"),
            "Suppressed Source Mesh Count": (
                "Disclosure Status",
                lambda values: int((values == 2).sum()),
            ),
        }
    )
    group_geometry = working[["Disclosure Group Code", "geometry"]].dissolve(
        by="Disclosure Group Code", as_index=True
    )

    groups = group_geometry.join(member_stats).join(exact_sums).join(
        detailed[DISCLOSURE_GROUP_COUNT_COLUMNS]
    )
    groups["Disclosure Group Size"] = groups["Disclosure Group Size"].astype("int32")
    groups["Suppressed Source Mesh Count"] = groups[
        "Suppressed Source Mesh Count"
    ].astype("int32")

    population_checks = {
        "Population Age 65+": "Total Population",
        "Population Age 75+": "Total Population",
        "Population Age 85+": "Total Population",
        "One-Person Households": "General Households",
        "Households with Member Age 65+": "General Households",
        "Older Single-Person Households": "General Households",
        "Older Couple Households": "General Households",
    }
    for numerator, denominator in population_checks.items():
        require(
            (groups[numerator] <= groups[denominator]).all(),
            f"{numerator} exceeds {denominator} in at least one disclosure group",
        )

    groups["Population Age 65+ Share"] = (
        groups["Population Age 65+"] / groups["Total Population"]
    )
    groups["Population Age 75+ Share"] = (
        groups["Population Age 75+"] / groups["Total Population"]
    )
    groups["Population Age 85+ Share"] = (
        groups["Population Age 85+"] / groups["Total Population"]
    )
    groups["Older Single-Person Household Share"] = (
        groups["Older Single-Person Households"] / groups["General Households"]
    )
    groups["Older Couple Household Share"] = (
        groups["Older Couple Households"] / groups["General Households"]
    )

    groups = groups.reset_index()
    require(groups.geometry.notna().all(), "The disclosure-group output lacks geometry")
    return gpd.GeoDataFrame(groups, geometry="geometry", crs=mesh_layer.crs)


def write_geoparquet(frame: gpd.GeoDataFrame, destination: Path) -> None:
    """Write through a temporary file so a failed run cannot leave partial output."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp.parquet")
    frame.to_parquet(temporary, index=False)
    temporary.replace(destination)


def main() -> int:
    population = read_population()
    group_code = validate_disclosure_links(population)
    mesh = read_mesh_geometries(population["Mesh Code"])
    mesh_layer = build_mesh_layer(population, mesh, group_code)
    group_layer = build_disclosure_group_layer(population, mesh_layer)

    write_geoparquet(mesh_layer, MESH_OUTPUT)
    write_geoparquet(group_layer, GROUP_OUTPUT)

    print(
        f"Saved {len(mesh_layer):,} rows x {len(mesh_layer.columns)} columns -> "
        f"{MESH_OUTPUT.relative_to(ROOT)}"
    )
    print(
        f"Saved {len(group_layer):,} rows x {len(group_layer.columns)} columns -> "
        f"{GROUP_OUTPUT.relative_to(ROOT)}"
    )
    print(
        "Validation: all population meshes matched geometry; disclosure links matched; "
        "no suppressed value was imputed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
