"""Extract the five human-approved R3/C11 parts without changing wording."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = ROOT/'data/exp/revision_r3c11'
out.mkdir(parents=True, exist_ok=True)
text = (ROOT/'Rev/docs/proposal-r3-c11.md').read_text()
parts = re.split(r'\n## Part \d+[^\n]*\n', text)[1:]
assert len(parts) == 5
for i, part in enumerate(parts, 1):
    spec = dict(schema_version=1, comment_id='reviewer-3/comment-11',
                part_id=f'part-{i:02}', mode='replace',
                decision_ids=['KILA-D-20261003-016'],
                location=re.search(r'Location: (.*)', part)[1],
                reason=re.search(r'Reason: (.*)', part)[1],
                before=re.search(r'Target sentence: "(.*?)"', part)[1],
                after=re.search(r'Replace with: "(.*?)"', part)[1])
    (out/f'part-{i:02}.json').write_text(json.dumps(spec, indent=2)+'\n')
