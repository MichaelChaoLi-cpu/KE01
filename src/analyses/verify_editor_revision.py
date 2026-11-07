"""Preservation and exact rendered-locator checks for the editor bundle."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from docx import Document
import json,re,subprocess
root=Path(__file__).resolve().parents[2]; out=root/'data/exp/revision_editor'
before=root/'Rev/revision/.kila-backups/KE01.rev.markup.20261003T103034719255.editor-overall-comment.part-01.docx'
after=root/'Rev/revision/KE01.rev.markup.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','m':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
with ZipFile(before) as a,ZipFile(after) as b:
    assert all(a.read(k)==b.read(k) for k in a.namelist() if k!='word/document.xml')
    x=E.fromstring(a.read('word/document.xml'));y=E.fromstring(b.read('word/document.xml'))
old=x.xpath('.//w:ins|.//w:del',namespaces=ns)
new={n.get('{'+ns['w']+'}id'):E.tostring(n) for n in y.xpath('.//w:ins|.//w:del',namespaces=ns)}
assert all(new[n.get('{'+ns['w']+'}id')]==E.tostring(n) for n in old)
for q in ['.//m:oMath','.//w:hyperlink','.//w:instrText','.//w:fldChar','.//w:tbl','.//w:pPr']:
    assert [E.tostring(n) for n in x.xpath(q,namespaces=ns)]==[E.tostring(n) for n in y.xpath(q,namespaces=ns)]
text='\n'.join(p.text for p in Document(root/'Rev/revision/KE01.rev.clean.docx').paragraphs)
pages=subprocess.check_output(['pdftotext','-layout',str(out/'render-clean/KE01.rev.clean.pdf'),'-'],text=True).split('\f')
chars=[];loc=[]
for page,p in enumerate(pages,1):
    for line in p.splitlines():
        m=re.match(r'^\s*(\d+)\s+(.+)',line)
        if not m:continue
        for c in m[2]:
            if not c.isspace():chars.append(c);loc.append((page,int(m[1])))
hay=''.join(chars);quotes=[]
for p in sorted(out.glob('part-*.json')):
    s=json.loads(p.read_text());assert text.count(s['after'])==1
    quote=s['after'][len(s['before']):].strip();needle=re.sub(r'\s+','',quote)
    assert hay.count(needle)==1,p
    i=hay.index(needle);first=loc[i];last=loc[i+len(needle)-1]
    quotes.append(dict(quote=quote,page_start=first[0],page_end=last[0],line_start=first[1],line_end=last[1]))
report=dict(passed=True,old_revision_nodes_preserved=len(old),formulas_preserved=69,quotes=quotes)
(out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
