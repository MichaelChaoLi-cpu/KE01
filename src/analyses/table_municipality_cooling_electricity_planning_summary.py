#!/usr/bin/env python3
"""Municipality Cooling Electricity Planning Summary.

Plan: report the Central demand scenario for protective cooling by municipality.
Framework: AnaSOP demand-side equations for peak power and daily electricity.
"""

from municipality_table_common import ROOT, build_master_summary, write_result_workbook


OUTPUT = ROOT / "data/results/tables/Table_municipality_cooling_electricity_planning_summary.xlsx"


def main() -> int:
    master = build_master_summary().rename(
        columns={
            "Estimated Affected Population Age 65+": "Affected Population Age 65+ (Central)",
            "No-Placement Unprotected Older-Person-Days": "No-Placement Older-Person-Days",
            "Expected High-Heat Scenario Days": "Expected High-Heat Days",
            "Required Peak Cooling Electric Power kW (Central)": "Peak Cooling Power kW (Central)",
            "Required Daily Cooling Electricity kWh (Central)": "Daily Cooling Electricity kWh (Central)",
        }
    )
    table = master[
        [
            "Municipality",
            "Affected Population Age 65+ (Central)",
            "No-Placement Older-Person-Days",
            "Expected High-Heat Days",
            "Peak Cooling Power kW (Central)",
            "Daily Cooling Electricity kWh (Central)",
        ]
    ].sort_values("Affected Population Age 65+ (Central)", ascending=False)
    definitions = [
        ("Municipality", "name", "Kumamoto Prefecture municipality; Kumamoto City's five wards are consolidated.", "45-unit analysis geography."),
        ("Affected Population Age 65+ (Central)", "persons", "Central older-person cooling-assessment population.", "Modeled exposure, not observed displacement."),
        ("No-Placement Older-Person-Days", "person-days", "Thirty-day demand-side bound without verified effective cooled placement.", "Does not claim placement capacity is zero."),
        ("Expected High-Heat Days", "days", "Five-year matching-period mean hot-day or hot-night count in the 30-day window.", "Historical scenario, not a 2026 forecast."),
        ("Peak Cooling Power kW (Central)", "kW", "Central-scenario peak electricity demand for protective cooling.", "Demand only; verified supply and power gap are excluded."),
        ("Daily Cooling Electricity kWh (Central)", "kWh/day", "Central-scenario daily electricity demand for protective cooling.", "Based on approved area, load, COP, diversity, and operating-hour assumptions."),
    ]
    write_result_workbook(
        table, OUTPUT, "Municipality Cooling Electricity Planning Summary",
        definitions, {2: "#,##0.0", 3: "#,##0.0", 4: "0.0", 5: "0.00", 6: "#,##0.0"},
        (2, 5, 6), "Central demand scenario — verified available supply is not estimated",
    )
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
