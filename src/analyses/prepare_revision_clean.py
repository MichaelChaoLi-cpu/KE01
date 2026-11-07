"""Fresh clean copy only for a package verified to contain no tracked revisions.

Fail closed on revision markup; this is not a general revision acceptor.
"""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Rev/revision/KE01.rev.markup.docx'
DEST = ROOT / 'Rev/revision/KE01.rev.clean.docx'


def main():
    before = SOURCE.stat()
    sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    with ZipFile(SOURCE) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            if name.startswith('word/') and name.endswith('.xml'):
                for element in ET.fromstring(archive.read(name)).iter():
                    local = element.tag.split('}')[-1]
                    if local in {'ins', 'del', 'moveFrom', 'moveTo', 'cellIns', 'cellDel', 'cellMerge', 'numberingChange'} or local.endswith('Change') or local.startswith(('moveFromRange', 'moveToRange', 'customXmlInsRange', 'customXmlDelRange', 'customXmlMove')):
                        raise ValueError(f'Revision construct {local} in {name}; requires a revision acceptor.')
        comments = any('comments' in name.lower() for name in archive.namelist())
    fd, temporary = tempfile.mkstemp(suffix='.docx', dir=DEST.parent)
    os.close(fd)
    shutil.copyfile(SOURCE, temporary)
    os.replace(temporary, DEST)
    after = SOURCE.stat()
    assert before.st_size == after.st_size and before.st_mtime_ns == after.st_mtime_ns
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == sha
    assert hashlib.sha256(DEST.read_bytes()).hexdigest() == sha
    report = {'source': str(SOURCE), 'clean': str(DEST), 'source_sha256_before': sha,
              'source_sha256_after': sha, 'size': before.st_size, 'mtime_ns': before.st_mtime_ns,
              'generated_utc': datetime.now(timezone.utc).isoformat(),
              'method': 'Package-wide revision absence verified; acceptance is a no-op; fresh atomic copy.',
              'comments_preserved': comments, 'visual_review': 'not performed'}
    (ROOT / 'Rev/docs/clean-provenance.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
