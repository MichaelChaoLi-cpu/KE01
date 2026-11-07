"""User-approved scoped object-edit exception; prepare, validate, then promote."""
from pathlib import Path
from zipfile import ZipFile
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, re, shutil, sys, os
from lxml import etree as E
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/exp/revision_object_replacement'
SRC = ROOT / 'Rev/revision/KE01.rev.markup.docx'
DST = OUT / 'KE01.objects.markup.docx'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def w(n): return '{'+NS['w']+'}'+n
def text(e): return ''.join(e.xpath('.//w:t/text()', namespaces=NS))

if '--promote' in sys.argv:
    receipt = json.loads((OUT/'validation.json').read_text())
    assert sha(SRC) == receipt['before_sha256']
    assert sha(DST) == receipt['candidate_sha256']
    tmp = SRC.with_suffix('.staged.docx')
    shutil.copy2(DST, tmp); os.replace(tmp, SRC)
    print('Promoted', sha(SRC)); sys.exit()

proposal_path = ROOT/'Rev/docs/proposal-r3-c5.json'
assert sha(proposal_path) == '2c15da1628e1adeada43c42dbbb4f21905e831de10a1b9ad6b4af29737fd3219'
proposal = json.loads(proposal_path.read_text())
assert sha(SRC) == 'f1e3c1af7f82876885bdc28045b293e7579326058b559654f97dc8b0a5d9abfd'
for obj in proposal['objects']:
    assert sha(ROOT/obj['replacement']) == obj['sha256'], obj['id']
OUT.mkdir(exist_ok=True)
backup = OUT/'before_objects.markup.docx'
assert not backup.exists(), 'Never overwrite original backup'
shutil.copy2(SRC, backup)
stamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
changes = []; images = []; replacements = {}
with ZipFile(SRC) as z:
    root = E.fromstring(z.read('word/document.xml'))
    original = deepcopy(root)
    body = root.find('w:body', NS)
    old_revs = {e.get(w('id')): E.tostring(e) for e in root.xpath('//w:ins|//w:del', namespaces=NS)}
    next_id = max(int(v) for v in root.xpath('//@w:id', namespaces=NS) if v.isdigit()) + 1
    tabs = body.findall('w:tbl', NS); assert len(tabs) == 3
    for ti, tab in enumerate(tabs):
        blocks = proposal['objects'][4+ti*3:7+ti*3]
        before = [blocks[0]['before'][0]] + [r for b in blocks for r in b['before'][1:]]
        after = [blocks[0]['after'][0]] + [r for b in blocks for r in b['after'][1:]]
        rows = tab.findall('w:tr', NS); assert len(rows) == len(after) == 46
        for ri, row in enumerate(rows):
            cells = row.findall('w:tc', NS); assert len(cells) == 6
            for ci, cell in enumerate(cells):
                old, new = before[ri][ci], after[ri][ci]
                assert text(cell) == old, (ti, ri, ci, text(cell), old)
                if old == new: continue
                pars = cell.findall('w:p', NS); assert len(pars) == 1
                p = pars[0]; runs = p.findall('w:r', NS)
                assert runs and all(c.tag in {w('pPr'), w('r')} for c in p)
                assert all(c.tag in {w('rPr'), w('t')} for run in runs for c in run)
                props = runs[0].find('w:rPr', NS)
                assert all(E.tostring(r.find('w:rPr',NS)) == E.tostring(props) for r in runs)
                deletion = E.Element(w('del'), {w('id'): str(next_id), w('author'): 'Codex', w('date'): stamp})
                insertion = E.Element(w('ins'), {w('id'): str(next_id+1), w('author'): 'Codex', w('date'): stamp})
                for run in runs:
                    p.remove(run)
                    for t in run.findall('w:t',NS): t.tag = w('delText')
                    deletion.append(run)
                run = E.SubElement(insertion, w('r'))
                if props is not None: run.append(deepcopy(props))
                E.SubElement(run,w('t')).text = new
                p.extend([deletion,insertion])
                assert text(cell) == new
                changes.append(dict(table=ti+1,row=ri,column=ci+1,before=old,after=new,revision_ids=[next_id,next_id+1]))
                next_id += 2
    rels = E.fromstring(z.read('word/_rels/document.xml.rels'))
    for obj in proposal['objects'][:4]:
        rid = re.search(r'rId\d+',obj['target']).group()
        target = next(e.get('Target') for e in rels if e.get('Id') == rid)
        assert target == 'media/image'+obj['id'][1:]+'.png'
        blips = root.xpath('//a:blip[@r:embed="'+rid+'"]',namespaces=NS); assert len(blips) == 1
        drawing = blips[0]
        while drawing.tag != w('drawing'): drawing = drawing.getparent()
        assert drawing.find('wp:inline',NS) is not None
        assert not drawing.xpath('.//a:srcRect',namespaces=NS)
        asset = ROOT/obj['replacement']
        with Image.open(asset) as im:
            width,height = im.size
            assert min(im.info['dpi']) > 300
        extents = drawing.xpath('.//wp:extent|.//a:xfrm/a:ext',namespaces=NS)
        assert len(extents) == 2
        cx = int(extents[0].get('cx')); cy = round(cx*height/width)
        for extent in extents:
            assert int(extent.get('cx')) == cx
            extent.set('cy',str(cy))
        replacements['word/'+target] = asset.read_bytes()
        images.append(dict(id=obj['id'],target='word/'+target,asset=obj['replacement'],sha256=obj['sha256'],width_emu=cx,height_emu=cy))
    assert {e.get(w('id')): E.tostring(e) for e in root.xpath('//w:ins|//w:del',namespaces=NS) if e.get(w('id')) in old_revs} == old_revs
    # Outside tables, only four figure extent values may differ.
    a=deepcopy(original); b=deepcopy(root)
    for tree in [a,b]:
        for t in tree.findall('w:body/w:tbl',NS): t.getparent().remove(t)
        for e in tree.xpath('//wp:extent|//a:xfrm/a:ext',namespaces=NS): e.set('cy','NORMALIZED')
    assert E.tostring(a) == E.tostring(b)
    assert E.fromstring(z.read('word/settings.xml')).find('w:trackRevisions',NS) is not None
    replacements['word/document.xml'] = E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(DST,'w') as out:
        for entry in z.infolist(): out.writestr(entry,replacements.get(entry.filename,z.read(entry.filename)))
with ZipFile(SRC) as a, ZipFile(DST) as b:
    assert b.testzip() is None
    for name in a.namelist():
        if name not in replacements: assert a.read(name) == b.read(name),name
    for name in b.namelist():
        if name.endswith('.xml'): E.fromstring(b.read(name))
receipt = dict(before_sha256=sha(SRC),candidate_sha256=sha(DST),backup=str(backup),
               changed_cells=len(changes),insertions=103+len(changes),deletions=81+len(changes),
               images=images,changes=changes,prior_revisions_preserved=True,
               endnotes_relationships_and_other_parts_unchanged=True,
               note='Scoped explicit workflow exception. Cells are tracked; media swaps are backed up, not tracked image revisions.')
(OUT/'validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print({k:v for k,v in receipt.items() if k not in ['changes','images']})
