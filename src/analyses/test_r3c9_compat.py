"""Copy-first regression checks for the approved pagination-marker exception."""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_r3c9'
SOURCE = ROOT / 'Rev/revision/KE01.rev.markup.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}

def validate(before, after):
    with ZipFile(before) as z: a = {n: z.read(n) for n in z.namelist()}
    with ZipFile(after) as z: b = {n: z.read(n) for n in z.namelist()}
    assert a.keys() == b.keys()
    assert all(a[n] == b[n] for n in a if n != 'word/document.xml')
    x, y = [E.fromstring(z['word/document.xml']) for z in (a, b)]
    c = lambda n: E.tostring(n, method='c14n')
    old = {(n.tag, n.get('{'+NS['w']+'}id')): c(n) for n in x.xpath('//w:ins|//w:del', namespaces=NS)}
    new = {(n.tag, n.get('{'+NS['w']+'}id')): c(n) for n in y.xpath('//w:ins|//w:del', namespaces=NS)}
    assert all(new.get(k) == v for k, v in old.items())
    for tag in ['m:oMath', 'w:hyperlink', 'w:fldChar', 'w:instrText', 'w:tbl', 'w:drawing', 'w:pPr', 'w:lastRenderedPageBreak']:
        assert [c(n) for n in x.xpath('//'+tag, namespaces=NS)] == [c(n) for n in y.xpath('//'+tag, namespaces=NS)], tag
    p, q = [r.xpath('//w:body/w:p', namespaces=NS) for r in (x, y)]
    assert len(p) == len(q)
    assert [i for i, (u, v) in enumerate(zip(p, q)) if c(u) != c(v)] == [99]
    spec = json.loads((OUT/'part-03.json').read_text())
    texts = [''.join(n.xpath('.//w:t[not(ancestor::w:del)]/text()', namespaces=NS)) for n in q]
    assert sum(spec['after'] in t for t in texts) == 1
    # Rejected-view paragraph must recover exactly the same text and marker positions.
    def rejected_events(par):
        events = []
        for n in par.iter():
            if n.xpath('ancestor::w:ins', namespaces=NS): continue
            if n.tag in ['{'+NS['w']+'}t', '{'+NS['w']+'}delText']:
                events.extend(n.text or '')
            elif n.tag == '{'+NS['w']+'}lastRenderedPageBreak': events.append('<PAGE_MARKER>')
        return events
    assert rejected_events(p[99]) == rejected_events(q[99])
    return {'old_revisions_preserved': len(old), 'new_revisions': len(new)-len(old),
            'other_package_parts_unchanged': True, 'formula_field_link_style_asset_checks': True,
            'pagination_markers_and_rejected_view_preserved': True, 'only_paragraph_99_changed': True}

if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(json.dumps(validate(Path(sys.argv[1]), Path(sys.argv[2])), indent=2))
    else:
        test = OUT/'test.markup.docx'
        assert not test.exists(), 'Do not overwrite a prior copy test'
        digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        shutil.copy2(SOURCE, test)
        args = [sys.executable, str(ROOT/'src/analyses/apply_r3c9_compat.py'), 'apply', '--docx', str(test),
                '--log', str(OUT/'test-revisionchanges.md'), '--spec', str(OUT/'part-03.json')]
        for phase in ['dry-run', 'apply']:
            run = subprocess.run(args+(['--dry-run'] if phase == 'dry-run' else []), capture_output=True, text=True)
            (OUT/f'test-{phase}.json').write_text(run.stdout+run.stderr)
            assert run.returncode == 0, run.stdout+run.stderr
        subprocess.run([sys.executable, str(ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py'),
                        'verify', '--docx', str(test)], check=True)
        result = validate(SOURCE, test)
        assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == digest
        result['formal_source_unchanged'] = digest
        (OUT/'copy-test-verification.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))
