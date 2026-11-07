"""Extract the approved R3/C9 proposal verbatim into tracked-edit specs."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
proposal = (ROOT / 'Rev/docs/proposal-r3-c9.md').read_text()
out = ROOT / 'data/exp/revision_r3c9'
out.mkdir(parents=True, exist_ok=True)
for i in range(1, 4):
    block = proposal.split(f'## Part 0{i} — ', 1)[1].split('\n## ', 1)[0]
    spec = dict(schema_version=1, comment_id='reviewer-3/comment-9',
                part_id=f'part-0{i}', mode='replace',
                decision_ids=['KILA-D-20261002-011', 'KILA-D-20261002-035'],
                location=re.search(r'Location: (.*)', block)[1],
                reason=re.search(r'Reason: (.*)', block)[1],
                before=re.search(r'Target sentence: "(.*?)"', block)[1],
                after=re.search(r'Replace with: "(.*?)"', block)[1])
    (out / f'part-0{i}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n')
print(out)
