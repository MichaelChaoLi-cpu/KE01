"""Accept the observed human revision constructs on a staged copy only."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import hashlib, json, shutil, subprocess, sys, tempfile, os
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/human_revision_refresh_20261005'
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = {'w': W[1:-1]}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    source = ROOT/'Rev/revision/KE01.rev.markup.docx'
    dest = ROOT/'Rev/revision/KE01.rev.clean.docx'
    before, stat = sha(source), source.stat()
    for name in ['KE01.rev.clean.docx', 'response-draft.md', 'response-draft.docx']:
        old = ROOT/'Rev/revision'/name
        backup = OUT/('before-'+name)
        if old.exists() and not backup.exists(): shutil.copy2(old, backup)
    with ZipFile(source) as z:
        entries = [(i, z.read(i.filename)) for i in z.infolist()]
    parts = dict((i.filename,b) for i,b in entries)
    r = E.fromstring(parts['word/document.xml'])
    rows = r.xpath('.//w:tr[w:trPr/w:del]', namespaces=NS)
    for row in rows: row.getparent().remove(row)
    deleted_empty = r.xpath('.//w:p[w:pPr/w:rPr/w:del]', namespaces=NS)
    merged_nonempty = 0
    for p in deleted_empty:
        assert p.getnext() is not None and p.getnext().tag == W+'p'
        if any(c.tag != W+'pPr' for c in p):
            # Accept a deleted paragraph mark by joining content to the following
            # paragraph, whose surviving paragraph mark supplies its properties.
            assert not p.xpath('./w:pPr/w:sectPr', namespaces=NS)
            following = p.getnext()
            before_text = p.xpath('.//w:t/text()', namespaces=NS) + following.xpath('.//w:t/text()', namespaces=NS)
            children = [c for c in p if c.tag != W+'pPr']
            offset = 1 if following.find(W+'pPr') is not None else 0
            for i, child in enumerate(children): following.insert(offset+i, child)
            assert following.xpath('.//w:t/text()', namespaces=NS) == before_text
            merged_nonempty += 1
        p.getparent().remove(p)
    # Property revisions store superseded properties; retain current properties.
    props = {'pPrChange','rPrChange','tcPrChange','trPrChange','tblPrChange','tblPrExChange','tblGridChange','sectPrChange'}
    removed = []
    for x in list(r.iter()):
        if E.QName(x).localname in props:
            removed.append(E.QName(x).localname); x.getparent().remove(x)
    for x in list(r.iter()):
        if E.QName(x).localname.startswith(('moveFromRange','moveToRange')): x.getparent().remove(x)
    parts['word/document.xml'] = E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
    with tempfile.TemporaryDirectory(dir=OUT) as td:
        stage=Path(td)/'stage.docx'; accepted=Path(td)/'accepted.docx'
        with ZipFile(stage,'w') as z:
            for i,b in entries:z.writestr(i,parts[i.filename])
        helper='/Users/lichao/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents/scripts/accept_tracked_changes.py'
        subprocess.run([sys.executable,helper,str(stage),'--mode','accept','--out',str(accepted)],check=True)
        with ZipFile(accepted) as z:
            for n in z.namelist():
                if n.startswith('word/') and n.endswith('.xml'):
                    for x in E.fromstring(z.read(n)).iter():
                        local=E.QName(x).localname
                        assert local not in {'ins','del','moveFrom','moveTo','cellIns','cellDel','cellMerge','numberingChange'} and not local.endswith('Change') and not local.startswith(('moveFromRange','moveToRange')), (n,local)
        assert sha(source)==before and source.stat().st_mtime_ns==stat.st_mtime_ns and source.stat().st_size==stat.st_size
        os.replace(accepted,dest)
    report=dict(source=str(source),clean=str(dest),source_sha256_before=before,source_sha256_after=sha(source),source_size=stat.st_size,source_mtime_ns=stat.st_mtime_ns,clean_sha256=sha(dest),generated_utc=datetime.now(timezone.utc).isoformat(),method='Staged OOXML acceptance: deleted rows and empty deleted paragraph marks; retain current properties; remove move ranges; bundled text/move acceptance; package-wide revision absence verification',deleted_rows=len(rows),deleted_empty_paragraphs=len(deleted_empty),property_revisions=len(removed),comments_preserved=any('comments' in n.lower() for n in parts))
    report['merged_nonempty_paragraphs'] = merged_nonempty
    report['deleted_empty_paragraphs'] -= merged_nonempty
    report['method'] += '; deleted paragraph marks join content using surviving paragraph properties'
    (OUT/'clean-provenance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
