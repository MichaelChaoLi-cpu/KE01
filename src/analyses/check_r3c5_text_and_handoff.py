"""Verify the approved text subset and prepare the human-owned object handoff."""
from pathlib import Path
import json
import hashlib
import zipfile
from lxml import etree as E

ROOT=Path(__file__).resolve().parents[2]
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
proposal=json.loads((ROOT/'Rev/docs/proposal-r3-c5.json').read_text())
markup=ROOT/'Rev/revision/KE01.rev.markup.docx'
clean=ROOT/'Rev/revision/KE01.rev.clean.docx'
original=ROOT/'Rev/revision/.kila-backups/KE01.rev.markup.20261002T155234522943.reviewer-3-comment-5.part-01.docx'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def txt(p):return ''.join(p.xpath('.//w:t/text()',namespaces=ns))
assert sha(original)==proposal['markup_sha256']
with zipfile.ZipFile(clean) as z:
    root=E.fromstring(z.read('word/document.xml'));pars=root.find('w:body',ns).findall('w:p',ns)
    for p in proposal['parts']:
        # Subsequent P05 updates the same paragraph but does not intersect P04.
        assert p['after'] in txt(pars[p['paragraph']]),p['id']
with zipfile.ZipFile(original) as a,zipfile.ZipFile(markup) as b:
    ar=E.fromstring(a.read('word/document.xml'));br=E.fromstring(b.read('word/document.xml'))
    for tag in ['w:tbl','m:oMath','w:instrText','w:hyperlink']:
        assert [E.tostring(x) for x in ar.xpath('//'+tag,namespaces=ns)]==[E.tostring(x) for x in br.xpath('//'+tag,namespaces=ns)],tag
    for name in a.namelist():
        if name.startswith('word/media/') or name.endswith('.rels') or name in ['word/endnotes.xml','word/footnotes.xml']:
            assert a.read(name)==b.read(name),name
    oldids={x.get('{'+ns['w']+'}id'):E.tostring(x) for x in ar.xpath('//w:ins|//w:del',namespaces=ns)}
    newids={x.get('{'+ns['w']+'}id'):E.tostring(x) for x in br.xpath('//w:ins|//w:del',namespaces=ns)}
    assert all(newids[k]==v for k,v in oldids.items())
log=(ROOT/'Rev/docs/revisionchanges.md').read_text().split('## reviewer-3/comment-5',1)[1]
assert log.count('### part-')==23
lines=['# R3/C5 图表人工替换清单','',
       '状态：23处文字已按批准方案写入修订稿；以下13项尚未执行。文件暂时含新版文字与旧图表，不能提交。', '',
       '在 `Rev/revision/KE01.rev.markup.docx` 中保持“修订”开启，不要接受已有修订，不要用 clean 文件覆盖。完成下列全部操作后保存同一路径，告知 agent 已保存，再统一核查。','',
       '## 四张图','',
       '使用 Word 的更改图片功能，保留现有位置、宽度和纵横比，避免裁掉图框。图注已经更新，无需再次粘贴。','']
for o in proposal['objects'][:4]:
    assert sha(ROOT/o['replacement'])==o['sha256']
    lines += [f'- {o["id"]}：[{Path(o["replacement"]).name}]({ROOT/o["replacement"]})']
lines += ['', '## 九个原生表格分块','',
          '按下列已核准的显示值逐单元格更新，保留表格样式、六列及16/16/13行的现有分块和顺序。不要把整表换成图片。数字格式已与新版工作簿一致；较小非零值保留必要精度。无需改动表题。','']
for o in proposal['objects'][4:]:
    assert sha(ROOT/o['replacement'])==o['sha256']
    lines += [f'### {o["id"]}', '', f'来源：`{o["replacement"]}`，工作表 `{o["sheet"]}`。','']
    def row(v):return '| '+' | '.join(str(c).replace('|','\\|') for c in v)+' |'
    lines += [row(o['after'][0]),'| '+' | '.join(['---']*6)+' |']
    lines += [row(r) for r in o['after'][1:]]
    lines += ['']
lines += ['## 保存后核查','',
          'Agent 将重新生成 clean，检查13项对象及全部文字，渲染所有受影响页面，刷新已受分页影响的回复定位；核查完成之前不更新 R3/C5 完成状态。正式 data/results 尚未晋升，生产管线迁移不属于本次人工 Word 操作。','']
(ROOT/'Rev/docs/r3-c5-human-object-handoff.md').write_text('\n'.join(lines))
receipt=dict(text_parts_verified=23,prior_revision_nodes_unchanged=True,omml_fields_hyperlinks_unchanged=True,
             tables_media_relationships_unchanged=True,markup_sha256=sha(markup),clean_sha256=sha(clean),
             pending_human_objects=13,visual_review='pending',response='untouched')
(ROOT/'Rev/docs/r3-c5-text-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
