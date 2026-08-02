#!/usr/bin/env python3
"""Profile the CP932, two-header-row e-Stat T001231 population table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd


def variable_group(code: str) -> str:
    if not code.startswith("T001231"):
        return "linkage_and_disclosure_metadata"
    number = int(code[-3:])
    if number <= 3:
        return "total_population_by_sex"
    if number <= 6:
        return "population_age_0_14_by_sex"
    if number <= 9:
        return "population_age_15_plus_by_sex"
    if number <= 12:
        return "population_age_15_64_by_sex"
    if number <= 15:
        return "population_age_18_plus_by_sex"
    if number <= 18:
        return "population_age_20_plus_by_sex"
    if number <= 21:
        return "population_age_65_plus_by_sex"
    if number <= 24:
        return "population_age_75_plus_by_sex"
    if number <= 27:
        return "population_age_85_plus_by_sex"
    if number <= 30:
        return "population_age_95_plus_by_sex"
    if number <= 33:
        return "foreign_population_by_sex"
    if number <= 35:
        return "household_totals"
    if number <= 42:
        return "households_by_size"
    return "household_structure_and_vulnerability"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    source = (
        root
        / "data/raw/population/estat_2020_T001231_kumamoto/extracted/tblT001231E43.txt"
    )
    output_dir = root / "data/exp/data-preprocessing"
    output_dir.mkdir(parents=True, exist_ok=True)

    codes = list(pd.read_csv(source, encoding="cp932", nrows=0).columns)
    labels = list(
        pd.read_csv(source, encoding="cp932", skiprows=1, nrows=1, header=None).iloc[0]
    )
    data = pd.read_csv(
        source,
        encoding="cp932",
        skiprows=[1],
        dtype="string",
        low_memory=False,
    )

    rows: list[dict[str, object]] = []
    for code, label in zip(codes, labels, strict=True):
        series = data[code]
        non_missing = series.dropna()
        rows.append(
            {
                "source_dataset": str(source.relative_to(root)),
                "variable_group": variable_group(code),
                "original_name": code,
                "japanese_label": "" if pd.isna(label) else str(label).strip(),
                "inferred_dtype": "string_identifier"
                if code in {"KEY_CODE", "HTKSAKI", "GASSAN"}
                else "integer_candidate",
                "rows": len(series),
                "blank_pct": round(float(series.isna().mean() * 100), 1),
                "suppressed_star_pct": round(float((series == "*").mean() * 100), 1),
                "sample_values": "; ".join(
                    str(value)[:80] for value in non_missing.drop_duplicates().head(3)
                ),
                "feasibility_status": "partly-testable"
                if code
                in {
                    "KEY_CODE",
                    "HTKSYORI",
                    "HTKSAKI",
                    "GASSAN",
                    "T001231001",
                    "T001231019",
                    "T001231022",
                    "T001231025",
                    "T001231034",
                    "T001231035",
                    "T001231047",
                    "T001231049",
                    "T001231050",
                }
                else "unknown",
            }
        )

    csv_path = output_dir / "estat_population_variable_inventory.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    markdown = [
        "# e-Stat T001231 Population Variable Inventory",
        "",
        f"- Rows: {len(data):,}",
        f"- Variables: {len(rows)}",
        "- Source encoding: CP932",
        "- Header rows: 2",
        "- Spatial unit: 125 m sixth-level mesh",
        "- An asterisk is an official disclosure-suppression marker, not zero.",
        "",
    ]
    grouped = pd.DataFrame(rows).groupby("variable_group", sort=False)
    for group, table in grouped:
        markdown.extend(
            [
                f"## {group}",
                "",
                "| original_name | Japanese label | dtype | blank % | suppressed `*` % | feasibility | sample values |",
                "|---|---|---|---:|---:|---|---|",
            ]
        )
        for row in table.to_dict(orient="records"):
            markdown.append(
                f"| {row['original_name']} | {row['japanese_label']} | {row['inferred_dtype']} "
                f"| {row['blank_pct']} | {row['suppressed_star_pct']} | {row['feasibility_status']} "
                f"| {row['sample_values']} |"
            )
        markdown.append("")

    readme_path = output_dir / "README.estat-population.md"
    readme_path.write_text("\n".join(markdown), encoding="utf-8")
    print(f"wrote {csv_path.relative_to(root)} ({len(rows)} variables)")
    print(f"wrote {readme_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
