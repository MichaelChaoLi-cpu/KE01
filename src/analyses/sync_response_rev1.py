"""Synchronize editor text and verified locators without replacing human edits."""
from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from lxml import etree as E
import re, json, hashlib, shutil, os

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('KE01_RESPONSE_SYNC_DIR', str(ROOT / 'data/exp/response_rev1_sync_20261005')))
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': W[1:-1]}

def text(p):
    return ''.join(p.xpath('.//w:t/text()', namespaces=NS))

def replacement(template, value):
    p = deepcopy(template)
    prop = p.find(W+'pPr')
    rp = p.find('.//'+W+'rPr')
    for c in list(p):
        if c is not prop: p.remove(c)
    if value:
        r = E.SubElement(p, W+'r')
        if rp is not None: r.append(deepcopy(rp))
        t = E.SubElement(r, W+'t'); t.text = value
        t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    return p

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    target=ROOT/'Rev/revision/response.rev1.docx'
    backup=OUT/'before-response.rev1.docx'
    assert not backup.exists(), 'Do not overwrite the pre-sync backup'
    md=(ROOT/'Rev/revision/response-draft.md').read_text()
    audit=json.loads(Path(os.environ.get('KE01_RESPONSE_AUDIT', str(ROOT/'data/exp/editor_response_refresh_20261005/locator-audit.json'))).read_text())
    assert len(audit)==110 and all(r['status']=='verified' and r['old']==r['new'] for r in audit)
    mapping={r['quote']:r['new'] for r in audit}
    with ZipFile(target) as z: entries=[(i,z.read(i.filename)) for i in z.infolist()]
    root=E.fromstring(dict((i.filename,b) for i,b in entries)['word/document.xml'])
    assert not root.xpath('.//w:ins|.//w:del',namespaces=NS), 'Preserve tracked edits for separate review'
    body=root.find(W+'body'); ps=list(body.findall(W+'p'))
    end=next(p for p in ps if text(p)=='Reviewer 1')
    start=next(p for p in ps if text(p).startswith('Thank you for the opportunity'))
    templates={k:deepcopy(ps[i]) for k,i in [('body',22),('label',26),('quote',27),('locator',28),('blank',23)]}
    original_reviewer=[E.tostring(p) for p in list(body)[body.index(end):]]
    old_reviewer_prose=[text(p) for p in list(body)[body.index(end):] if not text(p).startswith('(Page')]
    content=md.split('# Editor\n',1)[1].split('# Reviewer 1',1)[0].split('**Response:**\n',1)[1].strip()
    index=body.index(start)
    for p in list(body)[index:body.index(end)]:body.remove(p)
    for line in content.splitlines()+['']:
        kind='blank' if not line else 'locator' if line.startswith('(Page') else 'quote' if line.startswith('"') else 'label' if line.endswith(':') else 'body'
        body.insert(index,replacement(templates[kind],line)); index+=1
    summary=next(p for p in body if text(p).startswith('Align figures and tables'))
    newsummary=next(l[2:] for l in md.splitlines() if l.startswith('- Align figures and tables'))
    body.replace(summary,replacement(summary,newsummary))
    changed=0; checked=0
    ps=list(body.findall(W+'p'))
    for i,p in enumerate(ps):
        if text(p).startswith('(Page'):
            q=text(ps[i-1]).strip()
            assert q.startswith('"') and q.endswith('"'), q
            quote=q[1:-1]
            assert quote in mapping, 'Unmapped human quotation: '+quote
            value=mapping[quote];checked+=1
            if value!=text(p):body.replace(p,replacement(p,value));changed+=1
    assert old_reviewer_prose==[text(p) for p in list(body)[body.index(end):] if not text(p).startswith('(Page')]
    # Preserve every reviewer-region element byte-for-byte except locator paragraphs.
    before=[b for b in original_reviewer if not text(E.fromstring(b)).startswith('(Page')]
    after=[E.tostring(p) for p in list(body)[body.index(end):] if not text(p).startswith('(Page')]
    assert before==after
    shutil.copy2(target,backup)
    stage=OUT/'response.rev1.staged.docx'
    with ZipFile(stage,'w') as z:
        for info,b in entries:z.writestr(info,E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True) if info.filename=='word/document.xml' else b)
    with ZipFile(stage) as z:
        for i,b in entries:
            if i.filename!='word/document.xml':assert z.read(i.filename)==b
    stage.replace(target)
    report=dict(checked_locators=checked,updated_locators=changed,reviewer_prose_and_format_preserved=True,non_document_parts_byte_identical=True,backup=str(backup),sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    (OUT/'sync-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
