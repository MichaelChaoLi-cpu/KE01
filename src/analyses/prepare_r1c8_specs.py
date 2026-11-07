"""Extract approved R1/C8 exact wording for the bundled tracked editor."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / 'Rev/docs/proposal-r1-c8.md').read_text()
out = ROOT / 'data/exp/revision_r1c8'
out.mkdir(parents=True, exist_ok=True)
spec = dict(schema_version=1, comment_id='reviewer-1/comment-8',
            part_id='part-01', mode='replace', decision_ids=['KILA-D-20261003-011'],
            location=re.search(r'Location: (.*)', text)[1],
            reason=re.search(r'Reason: (.*)', text)[1],
            before=re.search(r'Target sentence: "(.*?)"', text)[1],
            after=re.search(r'Replace with: "(.*?)"', text)[1])
(out / 'part-01.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
