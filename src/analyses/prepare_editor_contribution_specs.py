"""Extract the five human-approved parts without modifying manuscript files."""
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/editor_contributions'
OUT.mkdir(parents=True,exist_ok=True)
parts=re.split(r'\n## Part \d+[^\n]*\n',(ROOT/'Rev/docs/proposal-editor-contributions.md').read_text())[1:]
assert len(parts)==5
for i,p in enumerate(parts,1):
    spec=dict(schema_version=1,comment_id='editor/overall-comment',part_id=f'contribution-{i:02}',mode='reedit' if i==2 else 'replace',decision_ids=['KILA-D-20261005-002'],location=re.search(r'Location: (.*)',p)[1],reason=re.search(r'Reason: (.*)',p)[1],before=re.search(r'Target sentence: "(.*?)"',p)[1],after=re.search(r'Replace with:\n\n"(.*?)"\n\nReason:',p,re.S)[1])
    spec['decision_ids'].append('KILA-D-20261005-003')
    if i==2:spec.update(reedit_confirmed=True,revises=['editor/overall-comment#part-01'])
    (OUT/f'part-{i:02}.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Five approved specs extracted; four require actual paragraph-boundary insertion.')
