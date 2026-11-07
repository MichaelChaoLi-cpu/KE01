"""Restore missing namespace declarations in response template-derived parts."""
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

ROOT = Path(__file__).resolve().parents[2]


def repair(source, target):
    with ZipFile(ROOT / 'Rev/revision/KE01.rev.markup.docx') as z:
        known = etree.fromstring(z.read('word/document.xml')).nsmap
    changed = []
    with ZipFile(source) as zin, ZipFile(target, 'w') as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == '_rels/.rels':
                # LibreOffice's package detector expects the conventional default
                # namespace in this package entry (the template uses ns0).
                fixed = data.replace(b'ns0:', b'').replace(b'xmlns:ns0=', b'xmlns=')
                before, after = etree.fromstring(data), etree.fromstring(fixed)
                assert [(e.tag, dict(e.attrib), e.text, e.tail) for e in before.iter()] == [(e.tag, dict(e.attrib), e.text, e.tail) for e in after.iter()]
                data = fixed
                changed.append(item.filename)
            if item.filename.endswith('.xml'):
                root = etree.fromstring(data)
                missing = set()
                for el in root.iter():
                    for key, value in el.attrib.items():
                        if key == '{http://schemas.openxmlformats.org/markup-compatibility/2006}Ignorable':
                            missing.update(p for p in value.split() if p not in el.nsmap)
                if missing:
                    assert missing <= known.keys()
                    start = data.index(b'<', data.index(b'?>') + 2)
                    end = data.index(b'>', start)
                    declarations = ''.join(f' xmlns:{p}="{known[p]}"' for p in sorted(missing)).encode()
                    fixed = data[:end] + declarations + data[end:]
                    parsed = etree.fromstring(fixed)
                    assert [(e.tag, dict(e.attrib), e.text, e.tail) for e in root.iter()] == [(e.tag, dict(e.attrib), e.text, e.tail) for e in parsed.iter()]
                    data = fixed
                    changed.append(item.filename)
            zout.writestr(item, data)
    print('Namespace-only repair:', changed)


if __name__ == '__main__':
    repair(Path(sys.argv[1]), Path(sys.argv[2]))
