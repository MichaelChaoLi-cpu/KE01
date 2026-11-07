"""Build approved Table S1 verbatim from the reviewed proposal."""
from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'Rev/docs/proposal-r3-c6.md').read_text()
part=source.split('## P4 —',1)[1].split('## Approval gate',1)[0]
doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.7)
sec.left_margin=sec.right_margin=Inches(.7)
style=doc.styles['Normal'];style.font.name='Times New Roman';style.font.size=Pt(11)
style.paragraph_format.space_after=Pt(6)
style.paragraph_format.line_spacing=1.05
for name in ['Title','Heading 1']:
    doc.styles[name].font.name='Times New Roman';doc.styles[name].font.color.rgb=RGBColor(0,0,0)
    doc.styles[name].font.size=Pt(16)
for st in doc.styles:
    for node in list(st.element.xpath('.//w:pBdr')):
        node.getparent().remove(node)
doc.add_paragraph('Emergency cooling demand parameters',style='Title')
caption=re.search(r'Title: (.*)',part)[1]
p=doc.add_paragraph(caption);p.runs[0].bold=True;p.paragraph_format.keep_with_next=True
rows=[[c.strip() for c in line.strip('|').split('|')] for line in part.splitlines() if line.startswith('|') and not line.startswith('|---')]
table=doc.add_table(rows=len(rows),cols=6);table.autofit=False
widths=[1.3,1.05,.48,.68,.48,3.11]
for j,w in enumerate(widths):table.columns[j].width=Inches(w)
for i,values in enumerate(rows):
    trpr=table.rows[i]._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
    if i==0:trpr.append(OxmlElement('w:tblHeader'))
    for j,value in enumerate(values):
        cell=table.cell(i,j);cell.width=Inches(widths[j]);cell.text=value
        cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        props=cell._tc.get_or_add_tcPr()
        margins=OxmlElement('w:tcMar')
        for edge in ['top','bottom','left','right']:
            e=OxmlElement('w:'+edge);e.set(qn('w:w'),'80');e.set(qn('w:type'),'dxa');margins.append(e)
        props.append(margins)
        borders=OxmlElement('w:tcBorders')
        for edge in ['top','bottom','left','right']:
            e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
        props.append(borders)
        if i==0:
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E8EEF3');props.append(shade)
        for p in cell.paragraphs:
            p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1
            if 1<=j<=4:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:r.font.size=Pt(10);r.bold=i==0
notes=re.search(r'Notes: (.*)',part)[1]
p=doc.add_paragraph('Notes: '+notes);p.paragraph_format.space_before=Pt(8)
for line in part.splitlines():
    if line.startswith('[S'):
        p=doc.add_paragraph(line)
        for run in p.runs:
            run.font.name='Hiragino Sans GB'
            run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Hiragino Sans GB')
out=ROOT/'Rev/revision/KE01.supplementary-table-S1.docx'
doc.save(out)
check=Document(out)
assert [[c.text for c in row.cells] for row in check.tables[0].rows]==rows
assert notes in '\n'.join(p.text for p in check.paragraphs)
print(out)
