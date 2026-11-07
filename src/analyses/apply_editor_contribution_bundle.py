"""Apply copy-tested approved parts sequentially through the skill adapter."""
import json
from test_editor_contribution_compat import OUT, SOURCE, ROOT, e, verify_pair

proof=json.loads((OUT/'copy-test-receipts.json').read_text())
assert len(proof)==5
assert e.sha256_path(SOURCE)=='3a0c4be3de37c5fe815e1dd3301c9ba4d91393779dd8f9b80a6315e619ca53b1'
receipts=[]
for i in range(1,6):
    spec=OUT/f'part-{i:02}.json'
    log=ROOT/'Rev/docs/revisionchanges.md'
    e.apply_revision(SOURCE,log,spec,'Kila',True)
    receipt=e.apply_revision(SOURCE,log,spec,'Kila',False)
    receipt['independent_verification']=verify_pair(__import__('pathlib').Path(receipt['backup']),SOURCE,i)
    assert f"contribution-{i:02}" in log.read_text()
    receipts.append(receipt)
    (OUT/'formal-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print('Formal part',i,'verified and logged',flush=True)
