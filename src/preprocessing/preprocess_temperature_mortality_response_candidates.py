#!/usr/bin/env python3
"""Structure published temperature-mortality estimates as candidate scenarios.

The source reports cumulative DLNM contrasts at the 99th temperature percentile
relative to the minimum-mortality temperature. These values must not be treated
as linear relative risks per 1 C increase.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
ARTICLE = ROOT / (
    "data/raw/mortality/literature/nationwide_temperature_mortality_japan_2023/"
    "yuan_et_al_2023_temperature_mortality_japan.pdf"
)
SUPPLEMENT = ROOT / (
    "data/raw/mortality/literature/nationwide_temperature_mortality_japan_2023/"
    "extracted/ehp12854.s001.acco.pdf"
)
OUTPUT = ROOT / (
    "data/processed/kumamoto_temperature_mortality_response_candidates_preprocessed.parquet"
)
DOI_URL = "https://doi.org/10.1289/EHP12854"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> int:
    require(ARTICLE.is_file(), f"Missing article: {ARTICLE}")
    require(SUPPLEMENT.is_file(), f"Missing supplement: {SUPPLEMENT}")
    records = [
        {
            "Estimate ID": "YUAN2023-JAPAN-65PLUS-ALLCAUSE",
            "Study Region": "Japan",
            "Age Group": "65+",
            "Outcome": "All-Cause Mortality",
            "Exposure Metric": "Daily Mean Air Temperature C",
            "Reference Temperature Percentile": 82,
            "Reference Temperature C": 24.8,
            "Comparison Temperature Percentile": 99,
            "Comparison Temperature C": 30.6,
            "Cumulative Lag Minimum Days": 0,
            "Cumulative Lag Maximum Days": 21,
            "Heat Relative Risk": 1.04,
            "Heat Relative Risk Lower 95% Confidence Interval": 1.02,
            "Heat Relative Risk Upper 95% Confidence Interval": 1.06,
            "Heat Attributable Fraction %": 0.47,
            "Heat Attributable Fraction Lower 95% Confidence Interval %": 0.40,
            "Heat Attributable Fraction Upper 95% Confidence Interval %": 0.52,
            "Estimate Applicability Status": "candidate_age_specific_main_scenario",
            "Source Table": "Supplemental Table S7",
        },
        {
            "Estimate ID": "YUAN2023-SOUTH-ALLAGES-ALLCAUSE",
            "Study Region": "Southern Japan",
            "Age Group": "All Ages",
            "Outcome": "All-Cause Mortality",
            "Exposure Metric": "Daily Mean Air Temperature C",
            "Reference Temperature Percentile": 80,
            "Reference Temperature C": 25.2,
            "Comparison Temperature Percentile": 99,
            "Comparison Temperature C": pd.NA,
            "Cumulative Lag Minimum Days": 0,
            "Cumulative Lag Maximum Days": 21,
            "Heat Relative Risk": 1.03,
            "Heat Relative Risk Lower 95% Confidence Interval": 1.00,
            "Heat Relative Risk Upper 95% Confidence Interval": 1.06,
            "Heat Attributable Fraction %": 0.52,
            "Heat Attributable Fraction Lower 95% Confidence Interval %": 0.39,
            "Heat Attributable Fraction Upper 95% Confidence Interval %": 0.65,
            "Estimate Applicability Status": "candidate_regional_sensitivity_only",
            "Source Table": "Supplemental Table S7",
        },
        {
            "Estimate ID": "YUAN2023-KUMAMOTO-ALLAGES-ALLCAUSE",
            "Study Region": "Kumamoto Prefecture",
            "Age Group": "All Ages",
            "Outcome": "All-Cause Mortality",
            "Exposure Metric": "Daily Mean Air Temperature C",
            "Reference Temperature Percentile": 99,
            "Reference Temperature C": 31.2,
            "Comparison Temperature Percentile": 99,
            "Comparison Temperature C": 31.2,
            "Cumulative Lag Minimum Days": 0,
            "Cumulative Lag Maximum Days": 21,
            "Heat Relative Risk": 1.00,
            "Heat Relative Risk Lower 95% Confidence Interval": pd.NA,
            "Heat Relative Risk Upper 95% Confidence Interval": pd.NA,
            "Heat Attributable Fraction %": -0.03,
            "Heat Attributable Fraction Lower 95% Confidence Interval %": -0.05,
            "Heat Attributable Fraction Upper 95% Confidence Interval %": 0.00,
            "Estimate Applicability Status": "prefecture_specific_no_positive_heat_contrast",
            "Source Table": "Supplemental Table S4",
        },
        {
            "Estimate ID": "YUAN2023-KUMAMOTO-ALLAGES-CIRCULATORY",
            "Study Region": "Kumamoto Prefecture",
            "Age Group": "All Ages",
            "Outcome": "Circulatory Mortality",
            "Exposure Metric": "Daily Mean Air Temperature C",
            "Reference Temperature Percentile": 80,
            "Reference Temperature C": 25.5,
            "Comparison Temperature Percentile": 99,
            "Comparison Temperature C": pd.NA,
            "Cumulative Lag Minimum Days": 0,
            "Cumulative Lag Maximum Days": 21,
            "Heat Relative Risk": 1.13,
            "Heat Relative Risk Lower 95% Confidence Interval": 0.94,
            "Heat Relative Risk Upper 95% Confidence Interval": 1.35,
            "Heat Attributable Fraction %": 1.19,
            "Heat Attributable Fraction Lower 95% Confidence Interval %": 0.58,
            "Heat Attributable Fraction Upper 95% Confidence Interval %": 1.74,
            "Estimate Applicability Status": "reference_only_outcome_mismatch",
            "Source Table": "Supplemental Table S5",
        },
    ]
    frame = pd.DataFrame(records)
    frame["Estimate Scale"] = (
        "Cumulative relative risk at the 99th temperature percentile versus MMT"
    )
    frame["Linear per 1 C Estimate Available"] = False
    frame["Source Citation"] = (
        "Yuan et al. (2023), Environmental Health Perspectives 131(12):127008"
    )
    frame["Source URL"] = DOI_URL
    frame["Notes"] = (
        "Published two-stage DLNM/BLUP estimate; do not convert to a linear per-1-C coefficient."
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(OUTPUT, index=False)
    print(f"Saved {len(frame):,} rows x {len(frame.columns)} cols -> {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
