#!/usr/bin/env python3
"""Municipality Housing Loss and Older-Person Cooling Need Summary.

Plan: compactly report structural housing loss, associated older residents, and
the no-verified-placement demand-side bound.
Framework: AnaSOP municipality aggregation of grid scenario values and bounds.
"""

from municipality_table_common import ROOT, build_master_summary, scenario_range, write_result_workbook


OUTPUT = ROOT / "data/results/tables/Table_municipality_housing_loss_and_older_person_cooling_need_summary.xlsx"


def main() -> int:
    master = build_master_summary()
    table = master.assign(
        **{
            "Functionally Lost Residences (Scenario Range)": scenario_range(
                master["Expected Functionally Lost Residences Lower Bound"],
                master["Expected Functionally Lost Residences Upper Bound"],
            ),
            "Affected Population Age 65+ (Scenario Range)": scenario_range(
                master["Estimated Affected Population Age 65+ Lower Bound"],
                master["Estimated Affected Population Age 65+ Upper Bound"],
            ),
        }
    ).rename(
        columns={
            "Expected Functionally Lost Residences": "Functionally Lost Residences (Central)",
            "Estimated Affected Population Age 65+": "Affected Population Age 65+ (Central)",
            "No-Placement Unprotected Older-Person-Days": "No-Placement Older-Person-Days",
        }
    )
    table = table[
        [
            "Municipality",
            "Functionally Lost Residences (Central)",
            "Functionally Lost Residences (Scenario Range)",
            "Affected Population Age 65+ (Central)",
            "Affected Population Age 65+ (Scenario Range)",
            "No-Placement Older-Person-Days",
        ]
    ].sort_values("Affected Population Age 65+ (Central)", ascending=False)
    definitions = [
        ("Municipality", "name", "Kumamoto Prefecture municipality; Kumamoto City's five wards are consolidated.", "45-unit geography aligned to the mortality baseline."),
        ("Functionally Lost Residences (Central)", "residences", "Central modeled structural residence-loss allocation.", "Scenario estimate, not an inspection count."),
        ("Functionally Lost Residences (Scenario Range)", "residences", "Pointwise lower-to-upper scenario range.", "Endpoints sum grid pointwise bounds and are not a joint confidence interval."),
        ("Affected Population Age 65+ (Central)", "persons", "Older residents associated with central modeled housing loss.", "Not observed displacement or shelter occupancy."),
        ("Affected Population Age 65+ (Scenario Range)", "persons", "Pointwise lower-to-upper affected-population range.", "Endpoints use lower and upper modeled housing-loss shares."),
        ("No-Placement Older-Person-Days", "person-days", "Thirty-day demand-side bound without verified effective cooled placement.", "Does not claim current placement capacity is zero."),
    ]
    write_result_workbook(
        table, OUTPUT, "Municipality Housing Loss and Older-Person Cooling Need Summary",
        definitions, {2: "#,##0.0", 4: "#,##0.0", 6: "#,##0.0"}, (2, 4, 6),
        "Modeled scenario — not observed damage, displacement, or placement",
    )
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
