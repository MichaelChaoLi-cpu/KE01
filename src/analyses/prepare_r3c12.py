"""Prepare exact specs, preserve complete tables, and create copy-first fixture."""
from pathlib import Path
import copy, json, shutil, re
from docx import Document
from docx.shared import Inches
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.table import Table
from docx.oxml import OxmlElement

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/revision_r3c12'
OUT.mkdir(parents=True, exist_ok=True)
source=ROOT/'Rev/revision/KE01.rev.clean.docx'
doc=Document(source)
tables=[copy.deepcopy(t._tbl) for t in doc.tables]
values=[[[c.text for c in r.cells] for r in t.rows] for t in doc.tables]
assert [len(t) for t in values]==[46]*3
proposal=(ROOT/'Rev/docs/proposal-r3-c12.md').read_text()
for i in range(3):
    s=dict(schema_version=1,comment_id='reviewer-3/comment-12',part_id=f'part-0{i+2}',mode='replace',decision_ids=['KILA-D-20261003-013','KILA-D-20261003-014'],location=f'Table {i+1}, data rows11–45',reason='Retain ten-row main excerpt and preserve full table in supplement',table_index=i,cells_before=values[i],before=json.dumps(values[i],ensure_ascii=False),after=json.dumps(values[i][:11],ensure_ascii=False))
    (OUT/f'part-0{i+2}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
for i in range(5,8):
    block=proposal.split(f'Part 0{i} target: ',1)[1]
    s=dict(schema_version=1,comment_id='reviewer-3/comment-12',part_id=f'part-0{i}',mode='replace',decision_ids=['KILA-D-20261003-014'],location=f'Table {i-4} caption',reason='Explain excerpt and point to complete supplement',before=re.search(r'^"(.*?)"',block)[1],after=re.search(r'Replace with: "(.*?)"',block)[1])
    (OUT/f'part-0{i}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
shutil.copy2(ROOT/'Rev/revision/KE01.rev.markup.docx',OUT/'test.markup.docx')
shutil.copy2(ROOT/'Rev/docs/revisionchanges.md',OUT/'test-changes.md')
(OUT/'source-cells.json').write_text(json.dumps(values,ensure_ascii=False,indent=2))
# Reuse manuscript style definitions, not its body or section breaks.
body=doc._element.body
for child in list(body):
    if child.tag.endswith('}sectPr'):continue
    body.remove(child)
sec=doc.sections[0]
sec.page_width=Inches(11.7);sec.page_height=Inches(8.3)
sec.left_margin=sec.right_margin=Inches(.65)
sec.top_margin=sec.bottom_margin=Inches(.65)
for node in list(sec._sectPr):
    if node.tag.endswith('}lnNumType'):sec._sectPr.remove(node)
doc.add_paragraph('Complete municipality planning tables',style='Title')
title=doc.paragraphs[-1]
title.style.font.color.rgb=RGBColor(0,0,0)
title.style.font.name='Times New Roman'
title.style.font.size=Pt(18)
for props in [title._p.get_or_add_pPr(),title.style.element.get_or_add_pPr()]:
    for node in list(props):
        if node.tag.endswith('}pBdr'):props.remove(node)
doc.add_paragraph('Tables S2–S4 provide all 45 municipalities corresponding to the main-text excerpts. Values, columns and order are unchanged; these scenario quantities are not observed losses, verified capacity gaps or deaths.')
titles=['Complete Municipality Housing Loss and Cooling Need','Complete Municipality Cooling Electricity Planning Summary','Complete Municipality Cooling-Loss Health-Risk Summary']
for i,table in enumerate(tables):
    if i:doc.add_page_break()
    p=doc.add_paragraph(f'Table S{i+2}. {titles[i]}');p.paragraph_format.keep_with_next=True
    body.insert(len(body)-1,table)
    for row in Table(table,doc._body).rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                fmt=para.paragraph_format
                fmt.left_indent=fmt.right_indent=fmt.first_line_indent=Pt(0)
                fmt.space_before=fmt.space_after=Pt(3)
                fmt.line_spacing=1
                fmt.keep_with_next=False
                para.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for run in para.runs:run.font.size=Pt(10)
    pr=table.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr').find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}trPr')
    if pr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tblHeader') is None:pr.append(OxmlElement('w:tblHeader'))
    doc.add_paragraph('')
dest=OUT/'KE01.supplementary-tables-S2-S4.docx'
doc.save(dest)
check=Document(dest)
assert [[[c.text for c in r.cells] for r in t.rows] for t in check.tables]==values
print(dest)
