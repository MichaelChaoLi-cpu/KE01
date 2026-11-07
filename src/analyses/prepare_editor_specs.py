"""Extract exact approved editor Discussion additions."""
import re,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=root/'data/exp/revision_editor'
out.mkdir(parents=True,exist_ok=True)
parts=re.split(r'\n## Part \d+[^\n]*\n',(root/'Rev/docs/proposal-editor-discussion.md').read_text())[1:]
assert len(parts)==3
for i,p in enumerate(parts,1):
    spec=dict(schema_version=1,comment_id='editor/overall-comment',part_id=f'part-{i:02}',mode='replace',decision_ids=['KILA-D-20261003-019'],location=re.search(r'Location: (.*)',p)[1],reason=re.search(r'Reason: (.*)',p)[1],before=re.search(r'Target sentence: "(.*?)"',p)[1],after=re.search(r'Replace with: "(.*?)"',p)[1])
    (out/f'part-{i:02}.json').write_text(json.dumps(spec,indent=2)+'\n')
