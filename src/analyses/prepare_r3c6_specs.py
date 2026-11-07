"""Extract unchanged approved prose into Kila tracked-edit specs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
proposal = (ROOT / 'Rev/docs/proposal-r3-c6.md').read_text()
out = ROOT / 'data/exp/revision_r3c6'
out.mkdir(parents=True, exist_ok=True)
for i in range(1, 4):
    block = proposal.split(f'## P{i} — ', 1)[1].split('\n## ', 1)[0]
    spec = dict(schema_version=1, comment_id='reviewer-3/comment-6',
                part_id=f'part-0{i}',
                location=re.search(r'Location: (.*)', block)[1],
                reason=re.search(r'Reason: (.*)', block)[1],
                decision_ids=['KILA-D-20261002-029', 'KILA-D-20261002-030'],
                mode='replace',
                before=re.search(r'Target sentences?: "(.*?)"', block)[1],
                after=re.search(r'Replace with: "(.*?)"', block)[1])
    if i == 2:
        spec.update(reedit_confirmed=True, revises=['reviewer-3/comment-5#part-02'])
    (out / f'part-0{i}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
print(out)
