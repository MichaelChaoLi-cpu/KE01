#!/usr/bin/env python3
"""Municipality Cooling-Loss Health-Risk Summary.

Plan: report the literature-anchored cooled-versus-uncooled 30-day contrast.
Framework: AnaSOP cumulative daily survival risk under common outdoor weather.
"""

from municipality_table_common import ROOT, build_master_summary, write_result_workbook


OUTPUT = ROOT / "data/results/tables/Table_municipality_cooling_loss_health_risk_summary.xlsx"


def main() -> int:
    master = build_master_summary().rename(
        columns={
            "Expected High-Heat Scenario Days": "Expected High-Heat Days",
            "Incremental Cooling-Loss-Related Excess Deaths": "Incremental Excess Deaths (30 Days)",
            "Cooling-Loss Relative 30-Day Mortality Burden Increase %": "Relative Mortality Burden Increase %",
            "Cooling-Loss Relative 30-Day Mortality Burden Increase % Lower 95% CI": "Relative Mortality Burden Increase % Lower 95% CI",
            "Cooling-Loss Relative 30-Day Mortality Burden Increase % Upper 95% CI": "Relative Mortality Burden Increase % Upper 95% CI",
        }
    )
    table = master[
        [
            "Municipality",
            "Expected High-Heat Days",
            "Incremental Excess Deaths (30 Days)",
            "Relative Mortality Burden Increase %",
            "Relative Mortality Burden Increase % Lower 95% CI",
            "Relative Mortality Burden Increase % Upper 95% CI",
        ]
    ].sort_values("Relative Mortality Burden Increase %", ascending=False)
    definitions = [
        ("Municipality", "name", "Kumamoto Prefecture municipality; Kumamoto City's five wards are consolidated.", "45-unit mortality geography."),
        ("Expected High-Heat Days", "days", "Five-year matching-period mean hot-day or hot-night count in the 30-day window.", "Historical scenario, not a 2026 forecast."),
        ("Incremental Excess Deaths (30 Days)", "expected deaths", "Central expected deaths without effective cooling minus with effective cooling.", "Planning scenario, not observed or earthquake-attributable mortality."),
        ("Relative Mortality Burden Increase %", "%", "Central relative increase in modeled 30-day mortality burden without effective cooling.", "Outdoor heat is held fixed; Katz et al. (2025) effect is transferred."),
        ("Relative Mortality Burden Increase % Lower 95% CI", "%", "Lower risk scenario from the published cooling-effect interval.", "Only cooling-effect parameter uncertainty is varied."),
        ("Relative Mortality Burden Increase % Upper 95% CI", "%", "Upper risk scenario from the published cooling-effect interval.", "Only cooling-effect parameter uncertainty is varied."),
    ]
    write_result_workbook(
        table, OUTPUT, "Municipality Cooling-Loss Health-Risk Summary",
        definitions, {2: "0.0", 3: "0.00000", 4: "0.00", 5: "0.00", 6: "0.00"},
        (3, 4), "Literature-anchored planning scenario — not observed mortality",
    )
    print(f"Saved: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
