"""Apply the copy-tested, human-approved R3/C12 bundle through the editor."""
from pathlib import Path
import json, shutil
from docx import Document
from test_r3c12 import run, verify, OUT, ROOT
from clean_r3c12 import clean
from apply_r3c12_compat import editor as e

if __name__ == '__main__':
    source = ROOT/'Rev/revision/KE01.rev.markup.docx'
    log = ROOT/'Rev/docs/revisionchanges.md'
    assert e.sha256_path(source) == '0e22d02b590126bd1257a06dfcd9b0897d253752baffb76fb5a74bff73a4343b'
    assert json.loads((OUT/'test-verification.json').read_text())['passed']
    supplement = ROOT/'Rev/revision/KE01.supplementary-tables-S2-S4.docx'
    assert not supplement.exists()
    expected = json.loads((OUT/'source-cells.json').read_text())
    draft = OUT/supplement.name
    assert [[[c.text for c in r.cells] for r in t.rows] for t in Document(draft).tables] == expected
    shutil.copy2(draft, supplement)
    before = OUT/'formal-before.markup.docx'
    assert not before.exists()
    shutil.copy2(source, before)
    with log.open('a') as f:
        f.write('\n\n## reviewer-3/comment-12 — supplementary artifact\n\n### part-01\n\n'
                '- Decision: KILA-D-20261003-014\n'
                '- Action: Create complete supplementary Tables S2–S4; existing S1 unchanged.\n'
                '- Before: No S2–S4 document.\n'
                '- After: Rev/revision/KE01.supplementary-tables-S2-S4.docx; three continuous tables, each with 45 municipalities and one header.\n'
                '- Source: Fresh pre-bundle clean 07e84e9ec1e017ac6f47587bb1e91d079cb4f6d1a0cff632a240bb399f435064. All cell values and row order match source-cells.json exactly.\n'
                f'- Artifact SHA256: {e.sha256_path(supplement)}\n'
                '- Visual review: All nine rendered supplementary pages verified before copy; copied artifact identical.\n')
    receipts = run(source, log)
    count = verify(before, source)
    dest = ROOT/'Rev/revision/KE01.rev.clean.docx'
    clean(source, dest, OUT/'formal-clean-provenance.json')
    assert [[[c.text for c in r.cells] for r in t.rows] for t in Document(dest).tables] == [v[:11] for v in expected]
    _, formal = e.read_package(dest)
    _, test = e.read_package(OUT/'test.clean.docx')
    assert formal['word/document.xml'] == test['word/document.xml']
    (OUT/'formal-verification.json').write_text(json.dumps(dict(passed=True,old_revisions_preserved=count,exact_rejection_recovery=True,clean_matches_test_xml=True,supplement_sha256=e.sha256_path(supplement),receipts=receipts),indent=2))
    print('PASS: formal clean matches tested clean; old revisions preserved; exact rejection recovery')
