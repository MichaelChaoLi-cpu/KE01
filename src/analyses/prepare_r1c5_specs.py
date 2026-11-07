"""Extract the approved R1/C5 proposal into exact tracked-edit specs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
proposal = (ROOT / 'Rev/docs/proposal-r1-c5.md').read_text()
out = ROOT / 'data/exp/revision_protected_multiplier'
out.mkdir(parents=True, exist_ok=True)
for i in range(1, 4):
    block = proposal.split(f'## Part 0{i} — ', 1)[1].split('\n## ', 1)[0]
    spec = dict(schema_version=1, comment_id='reviewer-1/comment-5',
                part_id=f'part-0{i}', mode='replace',
                decision_ids=['KILA-D-20261003-006'],
                location=re.search(r'Location: (.*)', block)[1],
                reason=re.search(r'Reason: (.*)', block)[1],
                before=re.search(r'Target sentence: "(.*?)"', block)[1],
                after=re.search(r'Replace with: "(.*?)"', block)[1])
    (out / f'part-0{i}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
