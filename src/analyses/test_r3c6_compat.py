"""Copy-first regression test of the explicitly approved R3/C6 adapter."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_r3c6'
SOURCE = ROOT / 'Rev/revision/KE01.rev.markup.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}


def validate(before, after):
    with ZipFile(before) as z: a = {n: z.read(n) for n in z.namelist()}
    with ZipFile(after) as z: b = {n: z.read(n) for n in z.namelist()}
    assert a.keys() == b.keys()
    assert all(a[n] == b[n] for n in a if n != 'word/document.xml')
    ra, rb = (etree.fromstring(x['word/document.xml']) for x in (a, b))
    def serial(nodes): return [etree.tostring(x, method='c14n') for x in nodes]
    old = {(x.tag, x.get('{'+NS['w']+'}id')): etree.tostring(x, method='c14n')
           for x in ra.xpath('//w:ins | //w:del', namespaces=NS)}
    new = {(x.tag, x.get('{'+NS['w']+'}id')): etree.tostring(x, method='c14n')
           for x in rb.xpath('//w:ins | //w:del', namespaces=NS)}
    assert all(new.get(k) == v for k,v in old.items())
    for query in ['//m:oMath', '//w:hyperlink', '//w:fldChar', '//w:instrText', '//w:tbl', '//w:drawing', '//w:pPr']:
        assert serial(ra.xpath(query, namespaces=NS)) == serial(rb.xpath(query, namespaces=NS)), query
    pa,pb = [r.xpath('//w:body/w:p', namespaces=NS) for r in (ra,rb)]
    assert len(pa)==len(pb)
    assert all(etree.tostring(x)==etree.tostring(y) for i,(x,y) in enumerate(zip(pa,pb)) if i not in [19,27,46])
    for i in range(1,4):
        s=json.loads((OUT/f'part-0{i}.json').read_text())
        text=[''.join(p.xpath('.//w:t[not(ancestor::w:del)]/text()',namespaces=NS)) for p in pb]
        assert sum(s['after'] in t for t in text)==1
    return {'old_revisions_preserved':len(old), 'new_revisions':len(new)-len(old),
            'all_other_zip_parts_identical':True, 'equations_fields_links_tables_drawings_styles_preserved':True,
            'non_target_paragraphs_identical':True, 'three_approved_after_spans_unique':True}


if __name__ == '__main__':
    digest=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    test=OUT/'test.markup.docx'
    log=OUT/'test-revisionchanges.md'
    for i in range(1,4):
        args=[sys.executable,str(ROOT/'src/analyses/apply_r3c6_compat.py'),'apply',
              '--docx',str(test),'--log',str(log),'--spec',str(OUT/f'part-0{i}.json')]
        for phase in ['dry-run','apply']:
            run=subprocess.run(args+(['--dry-run'] if phase=='dry-run' else []),capture_output=True,text=True)
            (OUT/f'test-p{i}-{phase}.json').write_text(run.stdout+run.stderr)
            if run.returncode: raise RuntimeError(run.stdout+run.stderr)
        subprocess.run([sys.executable,str(ROOT/'src/analyses/apply_r3c6_compat.py'),'verify','--docx',str(test)],check=True,capture_output=True)
    result=validate(SOURCE,test)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==digest
    result['formal_source_unchanged']=digest
    (OUT/'copy-test-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
