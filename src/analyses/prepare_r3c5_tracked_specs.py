"""Materialize approved specs without editing Word; use skill patcher separately."""
from pathlib import Path
import json
import hashlib
import zipfile
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[2]
proposal = ROOT/'Rev/docs/proposal-r3-c5.json'
assert hashlib.sha256(proposal.read_bytes()).hexdigest() == '2c15da1628e1adeada43c42dbbb4f21905e831de10a1b9ad6b4af29737fd3219'
p = json.loads(proposal.read_text())
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(ROOT/'Rev/revision/KE01.rev.clean.docx') as z:
    pars = E.fromstring(z.read('word/document.xml')).find('w:body',ns).findall('w:p',ns)
out = ROOT/'Rev/docs/r3-c5-specs'
out.mkdir(exist_ok=True)
for part in p['parts']:
    anchor = ''.join(x.text or '' for x in pars[part['paragraph']].findall('.//w:t',ns))[:50]
    spec = dict(schema_version=1,comment_id='reviewer-3/comment-5',part_id='part-'+part['id'][1:],
                location=part['label']+f'; approved bundle {part["id"]}/23',
                reason='Execute the approved linked R3/C5 primary-allocation reconciliation: '+part['label'],
                decision_ids=['KILA-D-20261002-022'],mode='replace',before=part['before'],after=part['after'],paragraph_anchor=anchor)
    (out/(part['id']+'.json')).write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('Prepared 23 approved specs; no manuscript writes.')
