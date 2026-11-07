"""Copy-first six-part test and structural preservation proof."""
from pathlib import Path
import json, copy
from docx import Document
from apply_r3c12_compat import editor as e
from clean_r3c12 import clean

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/revision_r3c12'

def run(source,log):
    receipts=[]
    for i in range(2,8):
        spec=OUT/f'part-0{i}.json'
        dry=e.apply_revision(source,log,spec,'Kila',True)
        if i<5:assert len(dry['revision_ids'])==35 and dry['minimal_fragments'][0]['operation']=='delete-rows'
        else:assert all(f['operation']=='insert' for f in dry['minimal_fragments'])
        receipt=e.apply_revision(source,log,spec,'Kila',False)
        e.validate_docx(source)
        assert f'### part-0{i}' in log.read_text()
        receipts.append(receipt)
        print(i,receipt['status'],receipt['sha256_after'])
    return receipts

def verify(before,after):
    _,a=e.read_package(before);_,b=e.read_package(after)
    for k in a:
        if k!='word/document.xml':assert a[k]==b[k],k
    x=e.etree.fromstring(a['word/document.xml']);y=e.etree.fromstring(b['word/document.xml'])
    old=x.xpath('.//w:ins|.//w:del',namespaces=e.NS)
    d={n.get(e.qn(e.W_NS,'id')):e.etree.tostring(n) for n in y.xpath('.//w:ins|.//w:del',namespaces=e.NS)}
    for n in old:assert d[n.get(e.qn(e.W_NS,'id'))]==e.etree.tostring(n)
    for q in ['.//m:oMath','.//w:hyperlink','.//w:instrText','.//w:fldChar','.//w:pPr','.//w:tc']:
        assert [e.etree.tostring(n) for n in x.xpath(q,namespaces=e.NS)]==[e.etree.tostring(n) for n in y.xpath(q,namespaces=e.NS)],q
    # Remove only new revision markers/insertions: input document must be exact.
    oldids={n.get(e.qn(e.W_NS,'id')) for n in old}
    for n in y.xpath('.//w:ins|.//w:del',namespaces=e.NS):
        if n.get(e.qn(e.W_NS,'id')) not in oldids:n.getparent().remove(n)
    assert e.etree.tostring(x)==e.etree.tostring(y)
    return len(old)

if __name__=='__main__':
    source=OUT/'test.markup.docx'
    receipts=run(source,OUT/'test-changes.md')
    count=verify(ROOT/'Rev/revision/KE01.rev.markup.docx',source)
    clean(source,OUT/'test.clean.docx',OUT/'test-clean-provenance.json')
    expected=json.loads((OUT/'source-cells.json').read_text())
    doc=Document(OUT/'test.clean.docx')
    assert [[[c.text for c in r.cells] for r in t.rows] for t in doc.tables]==[v[:11] for v in expected]
    (OUT/'test-verification.json').write_text(json.dumps(dict(passed=True,old_revisions_preserved=count,cell_values_preserved=True,rejection_recovers_original_xml=True,receipts=receipts),indent=2))
    print('PASS: old revisions, cells, math and fields unchanged; reject restores exact source; clean tables11 rows each')
