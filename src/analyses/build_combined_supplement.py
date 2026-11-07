"""Combine unchanged S1–S4 content with manuscript typography."""
from copy import deepcopy
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT=Path(__file__).resolve().parents[2]
REV=ROOT/'Rev/revision'
main=Document(REV/'KE01.rev.clean.docx')
s1=Document(REV/'KE01.supplementary-table-S1.docx')
s234=Document(REV/'KE01.supplementary-tables-S2-S4.docx')
out=Document()
body=out._element.body
for child in list(body):
    if child.tag!=qn('w:sectPr'): body.remove(child)
for name in ['Normal','Heading 1']:
    old=out.styles[name]._element
    old.getparent().replace(old,deepcopy(main.styles[name]._element))
out.styles['Title'].font.name='Times New Roman'
out.styles['Title'].font.size=Pt(16)
out.styles['Title'].font.bold=True
out.styles['Title'].font.color.rgb=RGBColor(0,0,0)
for border in out.styles['Title']._element.findall('.//'+qn('w:pBdr')):
    border.getparent().remove(border)
sec=out.sections[0]
sec.page_width=Inches(11);sec.page_height=Inches(8.5)
sec.left_margin=sec.right_margin=Inches(1.25)
sec.top_margin=sec.bottom_margin=Inches(1)
title=out.add_paragraph('Supplementary Materials',style='Title')
title.paragraph_format.first_line_indent=Pt(0)
for r in title.runs: r.font.name='Times New Roman';r.font.size=Pt(16);r.font.bold=True
out.add_paragraph('Tables',style='Heading 1')

def append_source(source, skip):
    for i,child in enumerate(source._element.body):
        if child.tag==qn('w:sectPr'): continue
        if child.tag==qn('w:p') and ''.join(t.text or '' for t in child.iter(qn('w:t'))) in skip: continue
        copied=deepcopy(child)
        for sect in copied.findall('.//'+qn('w:sectPr')): sect.getparent().remove(sect)
        body.insert(len(body)-1,copied)

append_source(s1,{s1.paragraphs[0].text})
append_source(s234,{s234.paragraphs[0].text})
for p in out.paragraphs[2:]:
    p.style=out.styles['Normal']
    p.paragraph_format.keep_with_next=p.text.startswith('Table S')
    p.paragraph_format.first_line_indent=Pt(0)
    p.paragraph_format.page_break_before=p.text.startswith(('Table S2.','Table S3.','Table S4.'))
    for r in p.runs:
        r.font.name='Times New Roman';r.font.size=Pt(12)
        r._r.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Hiragino Mincho ProN')
for table in out.tables:
    table.autofit=False
    widths=[c.width for c in table.columns]
    total=sum(widths)
    widths=[int(w/total*Inches(8.5)) for w in widths]
    for col,w in zip(table.columns,widths): col.width=w
    for ri,row in enumerate(table.rows):
        if ri==0 and row._tr.get_or_add_trPr().find(qn('w:tblHeader')) is None:
            row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
        for c,w in zip(row.cells,widths):
            c.width=w
            for p in c.paragraphs:
                p.style=out.styles['Normal'];p.paragraph_format.line_spacing=1
                p.paragraph_format.first_line_indent=Pt(0)
                p.paragraph_format.left_indent=Pt(0);p.paragraph_format.right_indent=Pt(0)
                p.alignment=WD_ALIGN_PARAGRAPH.CENTER
                if table is out.tables[0]: p.alignment=WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before=Pt(2);p.paragraph_format.space_after=Pt(2)
                p.paragraph_format.keep_with_next=False
                for r in p.runs: r.font.name='Times New Roman';r.font.size=Pt(10)
# Match the existing manuscript-style three-rule tables without changing cells.
first, reference = out.tables[:2]
for old in list(first._tbl.tblPr.findall(qn('w:tblBorders'))):
    first._tbl.tblPr.remove(old)
first._tbl.tblPr.append(deepcopy(reference._tbl.tblPr.find(qn('w:tblBorders'))))
for ri,row in enumerate(first.rows):
    for ci,cell in enumerate(row.cells):
        props=cell._tc.get_or_add_tcPr()
        for tag in ['w:tcBorders','w:shd']:
            for old in list(props.findall(qn(tag))): props.remove(old)
        if ri==0:
            borders=reference.rows[0].cells[ci]._tc.tcPr.find(qn('w:tcBorders'))
            if borders is not None: props.append(deepcopy(borders))
target=REV/'KE01.supplementary-materials.docx'
out.save(target)
check=Document(target)
assert len(check.tables)==4
for original,merged in zip(s1.tables+s234.tables,check.tables):
    assert [[c.text for c in r.cells] for r in original.rows]==[[c.text for c in r.cells] for r in merged.rows]
assert [p.text for p in check.paragraphs if p.style.name=='Heading 1']==['Tables']
print(target)
print('Cell-by-cell unchanged; table rows:',[len(t.rows) for t in check.tables])
