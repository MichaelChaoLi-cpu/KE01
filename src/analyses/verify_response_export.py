"""Verify namespace-only repair and prepare full-page QA contact sheets."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / 'data/exp/revision_response_export'
with ZipFile(ROOT / 'Rev/revision/response-draft.docx') as before, ZipFile(EXP / 'response-repaired.docx') as after:
    assert before.namelist() == after.namelist()
    for name in before.namelist():
        a, b = before.read(name), after.read(name)
        if a != b:
            x, y = etree.fromstring(a), etree.fromstring(b)
            assert [(e.tag, dict(e.attrib), e.text, e.tail) for e in x.iter()] == [(e.tag, dict(e.attrib), e.text, e.tail) for e in y.iter()], name
    assert before.read('word/document.xml') == after.read('word/document.xml')
print('All package entries semantically unchanged; body XML byte-identical.')
paths = sorted((EXP / 'repaired-render-v2').glob('page-*.png'), key=lambda p: int(p.stem.split('-')[1]))
for start in range(0, len(paths), 6):
    sheet = Image.new('RGB', (1800, 2400), 'white')
    for j, path in enumerate(paths[start:start+6]):
        im = Image.open(path).convert('RGB'); im.thumbnail((600, 765))
        x, y = j % 3 * 600, j // 3 * 1200
        sheet.paste(im, (x, y+30))
        ImageDraw.Draw(sheet).text((x+15,y+8),path.stem,fill='black')
    sheet.crop((0,0,1800,2000)).save(EXP / f'contact-{start//6+1}.png')
print(len(paths), 'pages rendered')
