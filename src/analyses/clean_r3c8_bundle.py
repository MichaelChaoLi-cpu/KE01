"""Fresh accepted clean for an explicitly counted insertion-only revision set."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[2]
expected_insertions = int(sys.argv[1]) if len(sys.argv) > 1 else 3
expected_deletions = int(sys.argv[2]) if len(sys.argv) > 2 else 0
source=ROOT/'Rev/revision/KE01.rev.markup.docx'
dest=ROOT/'Rev/revision/KE01.rev.clean.docx'
helper=Path('/Users/lichao/.codex/plugins/cache/openai-primary-runtime/documents/26.909.12148/skills/documents/scripts/accept_tracked_changes.py')
stat=source.stat(); sha=hashlib.sha256(source.read_bytes()).hexdigest()
with ZipFile(source) as z:
    for name in z.namelist():
        if name.startswith('word/') and name.endswith('.xml'):
            tags=[e.tag.split('}')[-1] for e in ET.fromstring(z.read(name)).iter()]
            revisions=[t for t in tags if t in {'ins','del','moveTo','moveFrom'} or t.endswith('Change')]
            assert not revisions or (name=='word/document.xml' and set(revisions) <= {'ins','del'} and revisions.count('ins') == expected_insertions and revisions.count('del') == expected_deletions)
fd, temp=tempfile.mkstemp(suffix='.docx',dir=dest.parent);os.close(fd)
subprocess.run([sys.executable,str(helper),str(source),'--mode','accept','--out',temp],check=True)
with ZipFile(temp) as z:
    for name in z.namelist():
        if name.startswith('word/') and name.endswith('.xml'):
            assert not any(e.tag.split('}')[-1] in {'ins','del','moveTo','moveFrom'} for e in ET.fromstring(z.read(name)).iter())
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
assert source.stat().st_mtime_ns==stat.st_mtime_ns and source.stat().st_size==stat.st_size
os.replace(temp,dest)
report={'source_sha256_before':sha,'source_sha256_after':sha,'clean_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'generated_utc':datetime.now(timezone.utc).isoformat(),'method':f'Bundled accept_tracked_changes.py on staged output; {expected_insertions} insertions and {expected_deletions} deletions accepted; all XML revision absence checked.','source_size':stat.st_size,'source_mtime_ns':stat.st_mtime_ns,'comments':'No comments in source','clean':str(dest)}
(ROOT/'Rev/docs/clean-provenance.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
