"""Refresh descriptive reported-damage comparisons against locked allocations.

No fitting, source reclassification, production writes or independent-validation
claim. Dates and damage categories remain separate.
"""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd
from analyze_reported_damage_geography import extract, EXPECTED

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'data/exp/revision_damage_comparison'
STRUCTURAL = ROOT/'data/exp/revision_integrated_calculation/structural_municipalities.parquet'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protected = {str(p.relative_to(ROOT)):sha(p) for folder in ['data/results','Rev/revision']
                 for p in (ROOT/folder).rglob('*') if p.is_file()}
    s = pd.read_parquet(STRUCTURAL)
    # Later-total proportional rescaling is not independent geographic evidence.
    s = s.loc[~s.scenario.eq('later_snapshot_primary')]
    assert s.scenario.nunique()==56 and not s.duplicated(['scenario','Municipality Code']).any()
    lookup = pd.read_parquet(ROOT/'data/processed/kumamoto_cooling_loss_mortality_scenario_preprocessed.parquet')
    lookup = lookup[['Municipality Code','Municipality Japanese','Municipality']].copy()
    lookup.loc[lookup['Municipality Code'].eq('43100'),'Municipality Japanese']='熊本市'
    diagnostics, details, sources = [], [], {str(STRUCTURAL.relative_to(ROOT)):sha(STRUCTURAL)}
    for date in EXPECTED:
        report,pdfsha = extract(date)
        sources[f'data/exp/revision_spatial_validation/sources/prefecture_{date}.pdf']=pdfsha
        report = report.merge(lookup,on='Municipality Japanese',validate='one_to_one').set_index('Municipality Code')
        assert len(report)==45
        report['broad_half']=report.large_half+report.half
        report['full_or_half']=report.full+report.broad_half
        for label, frame in s.groupby('scenario'):
            frame=frame.set_index('Municipality Code').loc[report.index]
            assert frame.functional_loss.notna().all()
            model=frame.functional_loss/frame.functional_loss.sum()
            for category in ['full','broad_half','full_or_half']:
                observed=report[category]/report[category].sum()
                diagnostics.append({'snapshot':date,'scenario':label,'category':category,
                    'reported_total':int(report[category].sum()),
                    'positive_report_municipalities':int(report[category].gt(0).sum()),
                    'spearman':float(report[category].rank().corr(model.rank())),
                    'share_total_variation':float((observed-model).abs().sum()/2),
                    'top5_overlap':(len(set(report[category].nlargest(5).index)&set(model.nlargest(5).index))
                                    if report[category].gt(0).sum()>=5 else None)})
                if label in ['primary','corrected_hybrid']:
                    d=report[['Municipality']].copy()
                    d['snapshot']=date;d['scenario']=label;d['category']=category
                    d['reported_share']=observed;d['modeled_share']=model
                    details.append(d.reset_index())
    results=pd.DataFrame(diagnostics)
    assert len(results)==336 and np.isfinite(results[['spearman','share_total_variation']]).all().all()
    assert results.share_total_variation.between(0,1).all()
    assert all(sha(ROOT/p)==value for p,value in protected.items())
    OUT.mkdir(parents=True,exist_ok=True)
    results.to_parquet(OUT/'diagnostics.parquet',index=False)
    pd.concat(details).to_parquet(OUT/'municipal_shares.parquet',index=False)
    (OUT/'validation.json').write_text(json.dumps({'source_sha256':sources,'script_sha256':sha(Path(__file__)),
        'comparisons':len(results),'scenarios':56,'dates':list(EXPECTED),
        'official_category_totals_reconciled':True,'formal_and_revision_files_unchanged':True,
        'interpretation':'Descriptive report-share comparison; not independent validation. Reported zeros are not inspected negatives. Categories and dates differ from functional-loss estimand; no fitting or model selection.'},indent=2)+'\n')
    print(results.loc[results.scenario.isin(['primary','corrected_hybrid'])].to_string(index=False))
    print('September shaking full-or-half range:')
    print(results.loc[results.snapshot.eq('20260929')&results.category.eq('full_or_half')&~results.scenario.isin(['primary','corrected_hybrid']),['spearman','share_total_variation','top5_overlap']].agg(['min','max']).to_string())


if __name__=='__main__':main()
