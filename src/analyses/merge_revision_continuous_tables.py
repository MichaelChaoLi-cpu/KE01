"""Explicitly approved formatting exception: merge table panels, preserve data/revisions.

Prepare candidate only by default. --promote requires an inspected candidate.
Structural layout edits are recoverable through the byte-identical backup,
not represented as new Word text revisions. Existing revisions stay intact.
"""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib, json, shutil, sys, os

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/revision_continuous_tables'
SRC=ROOT/'Rev/revision/KE01.rev.markup.docx'
DST=OUT/'KE01.continuous.markup.docx'
BACK=OUT/'before_merge.markup.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tag(n):return '{'+NS['w']+'}'+n
def txt(e):return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
if '--promote' in sys.argv:
    receipt=json.loads((OUT/'validation.json').read_text())
    assert sha(SRC)==receipt['before_sha256'] and sha(DST)==receipt['candidate_sha256']
    temp=SRC.with_suffix('.staged.docx');shutil.copy2(DST,temp);os.replace(temp,SRC)
    print('Promoted validated layout candidate:',sha(SRC));sys.exit()
OUT.mkdir(exist_ok=True)
assert not BACK.exists(), 'Existing backup: do not overwrite'
shutil.copy2(SRC,BACK)
with ZipFile(SRC) as z:
    root=E.fromstring(z.read('word/document.xml'));body=root.find('w:body',NS)
    oldrevs=[E.tostring(e) for e in root.xpath('//w:ins|//w:del',namespaces=NS)]
    tabs=body.findall('w:tbl',NS);assert len(tabs)==9
    retained_pars=[E.tostring(p) for p in body.findall('w:p',NS) if '(continued, panel ' not in txt(p)]
    olddata=[];removed=[]
    for group in range(3):
        trio=tabs[group*3:group*3+3];first=trio[0]
        rows=[r for t in trio for r in t.findall('w:tr',NS)[1:]]
        values=[[txt(c) for c in r.findall('w:tc',NS)] for r in rows]
        assert len(values)==45 and len({r[0] for r in values})==45 and all(len(r)==6 for r in values)
        olddata.append(values)
        for t in trio[1:]:
            cap=t.getprevious()
            assert cap.tag==tag('p') and txt(cap).startswith(f'Table {group+1}.') and '(continued, panel ' in txt(cap)
            assert not cap.xpath('.//w:sectPr|.//w:ins|.//w:del|.//w:fldChar|.//w:hyperlink',namespaces=NS)
            removed.append(txt(cap));body.remove(cap)
            for r in t.findall('w:tr',NS)[1:]:first.append(r)
            body.remove(t)
        for i,r in enumerate(first.findall('w:tr',NS)):
            pr=r.find('w:trPr',NS)
            if pr is None:pr=E.Element(tag('trPr'));r.insert(0,pr)
            for h in pr.findall('w:trHeight',NS):pr.remove(h)
            if pr.find('w:cantSplit',NS)is None:E.SubElement(pr,tag('cantSplit'))
            for h in pr.findall('w:tblHeader',NS):pr.remove(h)
            if i==0:E.SubElement(pr,tag('tblHeader'))
    assert len(body.findall('w:tbl',NS))==3
    assert [E.tostring(e) for e in root.xpath('//w:ins|//w:del',namespaces=NS)]==oldrevs
    assert [E.tostring(p) for p in body.findall('w:p',NS)]==retained_pars
    for i,t in enumerate(body.findall('w:tbl',NS)):
        rows=t.findall('w:tr',NS);assert len(rows)==46
        assert [[txt(c) for c in r.findall('w:tc',NS)] for r in rows[1:]]==olddata[i]
        assert all(r.find('w:trPr/w:cantSplit',NS)is not None for r in rows)
    with ZipFile(DST,'w') as o:
        for entry in z.infolist():o.writestr(entry,E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True) if entry.filename=='word/document.xml' else z.read(entry.filename))
with ZipFile(SRC) as a,ZipFile(DST) as b:
    assert b.testzip()is None
    for name in a.namelist():
        if name!='word/document.xml':assert a.read(name)==b.read(name),name
report=dict(before_sha256=sha(SRC),candidate_sha256=sha(DST),backup=str(BACK),tables=3,rows_per_table=46,columns=6,
            data_values_and_order_unchanged=True,prior_revision_nodes_unchanged=True,other_package_parts_unchanged=True,
            removed_continuation_captions=removed,repeat_header=True,unsplit_rows=True,
            scope='Formatting only; no numerical refresh or figure replacement. Structural merge is backed up, not a new tracked textual change.')
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
