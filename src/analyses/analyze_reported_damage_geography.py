"""Compare reported damage shares with fixed model geography, not ground truth."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/exp/revision_spatial_validation"
FIELDS = ["full", "large_half", "half", "partial", "unclassified"]
EXPECTED = {"20260731": [182,20,225,1032,67], "20260929": [2301,811,6594,52601,10036]}

def extract(date):
    path = OUT / "sources" / f"prefecture_{date}.pdf"
    text = subprocess.check_output(["pdftotext","-f","3","-l","3","-layout",str(path),"-"], text=True)
    records = []
    printed_total = None
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        name = parts[0]
        if not (re.fullmatch(r"[一-龥ぁ-んァ-ヶ]+[市町村]", name) or name == "合計"):
            continue
        if not all(re.fullmatch(r"[0-9,]+", v) for v in parts[1:]):
            continue
        values = [int(v.replace(",","")) for v in parts[1:]]
        assert len(values) == (13 if date=="20260731" else 14), (name,values)
        counts = values[8:13]
        if name == "合計":
            printed_total = counts
            continue
        if len(values) == 14:
            assert sum(counts) == values[13], (name,counts,values[13])
        records.append({"Municipality Japanese":name, **dict(zip(FIELDS,counts))})
    table = pd.DataFrame(records)
    assert len(table)==45 and table["Municipality Japanese"].is_unique
    assert table[FIELDS].sum().tolist() == printed_total == EXPECTED[date]
    table["snapshot"] = date
    table["zero_interpretation"] = "reported_zero_not_verified_absence"
    table["inspection_completeness"] = "unknown"
    return table, hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    geography = pd.read_parquet(ROOT/"data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet")
    lookup = geography[["Municipality Code","Municipality Japanese","Municipality"]].copy()
    lookup.loc[lookup["Municipality Code"].eq("43100"),"Municipality Japanese"] = "熊本市"
    model = pd.read_csv(ROOT/"data/exp/revision_snapshot_sensitivity/municipality_comparison.csv", dtype={"Municipality Code":str})
    model_col = "Expected Functionally Lost Residences_early"
    diagnostics, sources, extracts = [], {}, []
    for date in EXPECTED:
        table, digest = extract(date)
        sources[date] = digest
        table = table.merge(lookup, on="Municipality Japanese",validate="one_to_one")
        assert len(table)==45 and table.notna().all().all()
        table = table.merge(model[["Municipality Code",model_col]],on="Municipality Code",validate="one_to_one")
        table["model_share"] = table[model_col]/table[model_col].sum()
        # Broad half-collapse is explicit aggregation, not a silently harmonized source count.
        table["broad_half"] = table["large_half"] + table["half"]
        table["full_or_half"] = table["full"] + table["broad_half"]
        for field in ["full","broad_half","full_or_half"]:
            share = table[field]/table[field].sum()
            table[field+"_share"] = share
            top_report = set(table.nlargest(5,field)["Municipality Code"])
            top_model = set(table.nlargest(5,"model_share")["Municipality Code"])
            diagnostics.append({"snapshot":date,"reported_category":field,
                                "reported_total":int(table[field].sum()),
                                "municipalities_with_positive_reports":int(table[field].gt(0).sum()),
                                "rank_correlation_all_reported_rows":float(table[field].rank().corr(table["model_share"].rank())),
                                "share_total_variation_distance":float(abs(share-table["model_share"]).sum()/2),
                                "top5_overlap":len(top_report & top_model) if table[field].gt(0).sum() >= 5 else None})
        table.to_csv(OUT/f"municipality_damage_{date}.csv",index=False)
        extracts.append(table)
    pd.DataFrame(diagnostics).to_csv(OUT/"geographic_diagnostics.csv",index=False)
    report = {"source_pdf_sha256":sources,"rows_each":45,"category_totals_reconcile":True,
              "scope":"descriptive reported-share comparison; not building accuracy or fully independent validation",
              "caveats":["reporting zeros are not inspected negatives","unclassified counts retained",
                         "different report dates and categories","functional-loss model is not a classifier for each damage category",
                         "no model fitting or production replacement"],"diagnostics":diagnostics}
    (OUT/"validation.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    print(extracts[-1].sort_values("full_or_half",ascending=False)[["Municipality Japanese","full","broad_half","model_share","full_or_half_share"]].head(5).to_string(index=False))

if __name__=="__main__":
    main()
