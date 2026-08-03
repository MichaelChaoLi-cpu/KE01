#!/usr/bin/env python3
"""Build municipality-level older-adult mortality reference tables.

The numerator pools official final all-cause deaths for 2020-2024. The
denominator is a fixed 2020 Census population multiplied by five years and is
therefore an explicit approximation, not an official e-Stat mortality rate.
"""

from __future__ import annotations

import re
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_PATTERN = "data/raw/mortality/estat_vital_statistics_*_kumamoto/nc10043.csv"
POPULATION_PATH = (
    ROOT / "data/processed/kumamoto_population_disclosure_groups_preprocessed.parquet"
)
BOUNDARY_PATH = (
    ROOT / "data/raw/boundaries/estat_2020_small_area_kumamoto/extracted/r2ka43.shp"
)
ANNUAL_OUTPUT = (
    ROOT / "data/processed/kumamoto_municipality_mortality_annual_preprocessed.parquet"
)
BASELINE_OUTPUT = (
    ROOT / "data/processed/kumamoto_municipality_mortality_baseline_preprocessed.parquet"
)

AGE_COLUMNS = {
    "65+": [
        "65～69歳",
        "70～74歳",
        "75～79歳",
        "80～84歳",
        "85～89歳",
        "90～94歳",
        "95～99歳",
        "100歳以上",
    ],
    "75+": [
        "75～79歳",
        "80～84歳",
        "85～89歳",
        "90～94歳",
        "95～99歳",
        "100歳以上",
    ],
    "85+": ["85～89歳", "90～94歳", "95～99歳", "100歳以上"],
}
POPULATION_COLUMNS = {
    "65+": "Population Age 65+",
    "75+": "Population Age 75+",
    "85+": "Population Age 85+",
}
KUMAMOTO_WARDS = {"43101", "43102", "43103", "43104", "43105"}
MUNICIPALITY_ENGLISH = {
    "43100": "Kumamoto City",
    "43202": "Yatsushiro City",
    "43203": "Hitoyoshi City",
    "43204": "Arao City",
    "43205": "Minamata City",
    "43206": "Tamana City",
    "43208": "Yamaga City",
    "43210": "Kikuchi City",
    "43211": "Uto City",
    "43212": "Kamiamakusa City",
    "43213": "Uki City",
    "43214": "Aso City",
    "43215": "Amakusa City",
    "43216": "Koshi City",
    "43348": "Misato Town",
    "43364": "Gyokuto Town",
    "43367": "Nankan Town",
    "43368": "Nagasu Town",
    "43369": "Nagomi Town",
    "43403": "Ozu Town",
    "43404": "Kikuyo Town",
    "43423": "Minamioguni Town",
    "43424": "Oguni Town",
    "43425": "Ubuyama Village",
    "43428": "Takamori Town",
    "43432": "Nishihara Village",
    "43433": "Minamiaso Village",
    "43441": "Mifune Town",
    "43442": "Kashima Town",
    "43443": "Mashiki Town",
    "43444": "Kosa Town",
    "43447": "Yamato Town",
    "43468": "Hikawa Town",
    "43482": "Ashikita Town",
    "43484": "Tsunagi Town",
    "43501": "Nishiki Town",
    "43505": "Taragi Town",
    "43506": "Yunomae Town",
    "43507": "Mizukami Village",
    "43510": "Sagara Village",
    "43511": "Itsuki Village",
    "43512": "Yamae Village",
    "43513": "Kuma Village",
    "43514": "Asagiri Town",
    "43531": "Reihoku Town",
}
SOURCE_URL = (
    "https://www.e-stat.go.jp/stat-search/files?cycle=7&layout=datalist&"
    "tclass1=000001053058&tclass2=000001053061&tclass3=000001053074&"
    "tclass4=000001053085&toukei=00450011&tstat=000001028897"
)
STAT_INF_IDS = (
    "000032119560,000032243689,000040098534,000040206370,000040316738"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def numeric(series: pd.Series) -> pd.Series:
    # MHLW notation: a dash means no count; ellipsis or a centered dot is unavailable.
    cleaned = series.astype("string").str.strip().replace({"-": "0", "…": pd.NA, "・": pd.NA})
    return pd.to_numeric(cleaned, errors="coerce").astype("Int64")


def age_sum(frame: pd.DataFrame, columns: list[str]) -> pd.Series:
    values = frame[columns].apply(numeric)
    return values.sum(axis=1, min_count=len(columns)).astype("Int64")


def source_year(path: Path) -> int:
    match = re.search(r"estat_vital_statistics_(\d{4})_kumamoto", str(path))
    require(match is not None, f"Cannot identify year from {path}")
    return int(match.group(1))


def parse_annual_deaths() -> pd.DataFrame:
    paths = sorted(ROOT.glob(RAW_PATTERN))
    require(len(paths) == 5, f"Expected five mortality files, found {len(paths)}")
    records: list[dict[str, object]] = []

    for path in paths:
        year = source_year(path)
        frame = pd.read_csv(path, encoding="cp932", header=2, dtype="string")
        place_column, sex_column = frame.columns[:2]
        for columns in AGE_COLUMNS.values():
            require(set(columns).issubset(frame.columns), f"Missing age columns in {path}")

        prefecture_total = frame.loc[
            frame[place_column].str.strip().eq("保健所別計")
            & frame[sex_column].str.strip().eq("総数")
        ]
        require(len(prefecture_total) == 1, f"Missing prefecture total in {path}")

        municipality = frame.loc[
            frame[place_column].str.strip().str.match(r"^43\d{3}", na=False)
            & frame[sex_column].str.strip().eq("総数")
        ].copy()
        require(len(municipality) == 49, f"Expected 49 city/ward rows in {path}")
        municipality["Source Municipality Code"] = (
            municipality[place_column].str.extract(r"^(\d{5})", expand=False)
        )
        municipality["Municipality Code"] = municipality["Source Municipality Code"].where(
            ~municipality["Source Municipality Code"].isin(KUMAMOTO_WARDS), "43100"
        )

        for age_group, columns in AGE_COLUMNS.items():
            municipality["Deaths"] = age_sum(municipality, columns)
            expected = int(age_sum(prefecture_total, columns).iloc[0])
            observed = int(municipality["Deaths"].sum())
            require(observed == expected, f"{year} {age_group}: {observed} != {expected}")
            grouped = municipality.groupby("Municipality Code", as_index=False)["Deaths"].sum()
            require(len(grouped) == 45, f"Expected 45 municipalities in {year}")
            for row in grouped.itertuples(index=False):
                records.append(
                    {
                        "Municipality Code": row[0],
                        "Municipality": MUNICIPALITY_ENGLISH[row[0]],
                        "Calendar Year": year,
                        "Age Group": age_group,
                        "All-Cause Deaths": int(row[1]),
                        "Mortality Data Status": "official_final",
                    }
                )

    annual = pd.DataFrame(records).sort_values(
        ["Municipality Code", "Calendar Year", "Age Group"]
    )
    require(len(annual) == 45 * 5 * 3, "Unexpected annual mortality row count")
    return annual.reset_index(drop=True)


def municipality_population() -> pd.DataFrame:
    population = gpd.read_parquet(POPULATION_PATH).to_crs(6670)
    boundaries = gpd.read_file(
        BOUNDARY_PATH, columns=["PREF", "CITY", "CITY_NAME", "geometry"]
    ).to_crs(6670)
    boundaries["Ward Code"] = (
        boundaries["PREF"].astype(str).str.zfill(2)
        + boundaries["CITY"].astype(str).str.zfill(3)
    )
    boundaries["Municipality Code"] = boundaries["Ward Code"].where(
        ~boundaries["Ward Code"].isin(KUMAMOTO_WARDS), "43100"
    )
    municipality = boundaries.dissolve("Municipality Code").reset_index()
    require(len(municipality) == 45, "Expected 45 municipality geometries")

    points = population[
        ["Disclosure Group Code", *POPULATION_COLUMNS.values(), "geometry"]
    ].copy()
    points["geometry"] = points.geometry.representative_point()
    assigned = gpd.sjoin(
        points,
        municipality[["Municipality Code", "geometry"]],
        how="left",
        predicate="within",
    ).drop(columns="index_right")

    unmatched = assigned[assigned["Municipality Code"].isna()].drop(
        columns="Municipality Code"
    )
    matched = assigned[assigned["Municipality Code"].notna()].copy()
    if len(unmatched):
        nearest = gpd.sjoin_nearest(
            unmatched,
            municipality[["Municipality Code", "geometry"]],
            how="left",
            distance_col="Assignment Distance m",
        ).drop(columns="index_right")
        require(
            nearest["Assignment Distance m"].max() <= 100,
            "A disclosure group is more than 100 m from the nearest municipality polygon",
        )
        assigned = pd.concat([matched, nearest], ignore_index=True)

    require(
        assigned["Disclosure Group Code"].is_unique,
        "Population disclosure groups were assigned more than once",
    )
    totals = assigned.groupby("Municipality Code", as_index=False)[
        list(POPULATION_COLUMNS.values())
    ].sum(min_count=1)
    require(len(totals) == 45, "Population assignment did not cover 45 municipalities")
    require(
        set(totals["Municipality Code"]) == set(MUNICIPALITY_ENGLISH),
        "Population and mortality municipality codes differ",
    )
    return totals


def main() -> int:
    annual = parse_annual_deaths()
    population = municipality_population()
    population_long = population.melt(
        id_vars="Municipality Code",
        value_vars=list(POPULATION_COLUMNS.values()),
        var_name="Population Variable",
        value_name="Population at Risk",
    )
    inverse_population = {value: key for key, value in POPULATION_COLUMNS.items()}
    population_long["Age Group"] = population_long["Population Variable"].map(
        inverse_population
    )
    population_long = population_long.drop(columns="Population Variable")

    annual = annual.merge(
        population_long, on=["Municipality Code", "Age Group"], how="left", validate="m:1"
    )
    annual["Population Reference Year"] = 2020
    annual["Source Organization"] = "Ministry of Health, Labour and Welfare via e-Stat"
    annual["Source URL"] = SOURCE_URL
    annual["Source Stat Inf IDs"] = STAT_INF_IDS

    baseline = (
        annual.groupby(
            ["Municipality Code", "Municipality", "Age Group"], as_index=False
        )
        .agg(
            **{
                "Population at Risk": ("Population at Risk", "first"),
                "All-Cause Deaths": ("All-Cause Deaths", "sum"),
                "Mean Annual All-Cause Deaths": ("All-Cause Deaths", "mean"),
            }
        )
        .sort_values(["Municipality Code", "Age Group"])
    )
    baseline["Baseline Period Start"] = pd.Timestamp("2020-01-01")
    baseline["Baseline Period End"] = pd.Timestamp("2024-12-31")
    baseline["Baseline Years"] = 5
    baseline["Population Reference Year"] = 2020
    baseline["Approximate Person-Years"] = (
        baseline["Population at Risk"] * baseline["Baseline Years"]
    )
    baseline["Baseline Mortality Rate per 100,000"] = np.where(
        baseline["Approximate Person-Years"] > 0,
        baseline["All-Cause Deaths"]
        / baseline["Approximate Person-Years"]
        * 100_000,
        np.nan,
    )
    baseline["Mortality Data Status"] = "official_final_deaths_pooled_2020_2024"
    baseline["Denominator Status"] = (
        "approximate_fixed_2020_total_population_times_5"
    )
    baseline["Source Organization"] = (
        "Ministry of Health, Labour and Welfare via e-Stat"
    )
    baseline["Source URL"] = SOURCE_URL
    baseline["Source Stat Inf IDs"] = STAT_INF_IDS
    baseline["Notes"] = (
        "Numerator is final Vital Statistics deaths among Japanese people in Japan; "
        "denominator is 2020 Census total resident population and is held fixed for five years."
    )

    ANNUAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    annual.to_parquet(ANNUAL_OUTPUT, index=False)
    baseline.to_parquet(BASELINE_OUTPUT, index=False)
    print(f"Saved {len(annual):,} rows x {len(annual.columns)} cols -> {ANNUAL_OUTPUT.relative_to(ROOT)}")
    print(f"Saved {len(baseline):,} rows x {len(baseline.columns)} cols -> {BASELINE_OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
