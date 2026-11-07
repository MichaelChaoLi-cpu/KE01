"""Accept row deletions only on a staged clean copy, then bundled text revisions."""
from pathlib import Path
import sys, tempfile, subprocess, hashlib, json, os
from datetime import datetime, timezone
from apply_r3c12_compat import editor as e

def clean(source,dest,report):
    before=e.sha256_path(source);stat=source.stat()
    infos,files=e.read_package(source)
    root=e.etree.fromstring(files['word/document.xml'])
    rows=root.xpath('.//w:tr[w:trPr/w:del]',namespaces=e.NS)
    assert len(rows)==105
    for row in rows:row.getparent().remove(row)
    files['word/document.xml']=e.xml_bytes(root)
    with tempfile.TemporaryDirectory(dir=dest.parent) as td:
        stage=Path(td)/'row-accepted.docx';out=Path(td)/'accepted.docx'
        e.write_package(stage,infos,files)
        helper=Path('/Users/lichao/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents/scripts/accept_tracked_changes.py')
        subprocess.run([sys.executable,str(helper),str(stage),'--mode','accept','--out',str(out)],check=True)
        _,new=e.read_package(out)
        r=e.etree.fromstring(new['word/document.xml'])
        assert not r.xpath('.//w:ins|.//w:del',namespaces=e.NS)
        assert [len(t.findall('w:tr',e.NS)) for t in r.xpath('./w:body/w:tbl',namespaces=e.NS)]==[11]*3
        assert e.sha256_path(source)==before and source.stat().st_mtime_ns==stat.st_mtime_ns
        os.replace(out,dest)
    report.write_text(json.dumps(dict(source_sha256_before=before,source_sha256_after=e.sha256_path(source),clean_sha256=e.sha256_path(dest),generated_utc=datetime.now(timezone.utc).isoformat(),method='Staged copy accepts105 tracked row deletions, then bundled text revision acceptance',clean=str(dest)),indent=2))

if __name__=='__main__':clean(*map(Path,sys.argv[1:]))
