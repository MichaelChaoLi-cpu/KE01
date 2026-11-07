"""Audit household/age counts without changing demographic allocations."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/revision_age_allocation'

def main():
    path=ROOT/'data/processed/kumamoto_spatial_foundation_disclosure_groups_preprocessed.parquet'
    cols=['General Households','Population Age 65+','Population Age 75+','Population Age 85+','Households with Member Age 65+','Older Single-Person Households','Older Couple Households']
    f=pd.read_parquet(path,columns=cols)
    h,n,a,s,c=(f[x] for x in [cols[0],cols[1],cols[4],cols[5],cols[6]])
    report={'groups':len(f),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'columns':{x:{'missing':int(f[x].isna().sum()),'negative':int(f[x].lt(0).sum()),'noninteger':int(f[x].mod(1).ne(0).sum()),'sum':int(f[x].sum())} for x in cols},
            'violations':{'older_households_above_general':int((a>h).sum()),'single_plus_couple_above_older_households':int((s+c>a).sum()),'older_households_above_older_people':int((a>n).sum()),'age75_above65':int((f[cols[2]]>n).sum()),'age85_above75':int((f[cols[3]]>f[cols[2]]).sum())},
            'zero_general_household_groups':int((h==0).sum()),
            'older_people_in_zero_general_household_groups':int(n[h==0].sum()),
            'groups_with_older_people_but_no_older_general_households':int(((n>0)&(a==0)).sum()),
            'older_people_in_groups_without_older_general_households':int(n[a==0].sum()),
            'caution':'All-resident age counts and general-household counts have different universes. No institutional status is inferred for individual residents.'}
    assert all(v['missing']==v['negative']==v['noninteger']==0 for v in report['columns'].values())
    assert not any(report['violations'].values())
    OUT.mkdir(exist_ok=True,parents=True)
    (OUT/'input_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
