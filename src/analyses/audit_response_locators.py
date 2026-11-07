"""Audit all quoted response passages; emit locator-only patch, never alter prose."""
from pathlib import Path
from docx import Document
import subprocess,re,json,os
root=Path(__file__).resolve().parents[2];out=Path(os.environ.get('KE01_LOCATOR_DIR',str(root/'data/exp/revision_editor')))
path=root/'Rev/revision/response-draft.md';s=path.read_text()
d=Document(root/'Rev/revision/KE01.rev.clean.docx')
paras=[p.text for p in d.paragraphs]
text='\n'.join(paras)+ '\n'+'\n'.join(c.text for t in d.tables for r in t.rows for c in r.cells)
pdf=subprocess.check_output(['pdftotext','-layout',str(out/'render-clean/KE01.rev.clean.pdf'),'-'],text=True)
chars=[];loc=[]
for page,p in enumerate(pdf.split('\f'),1):
    for line in p.splitlines():
        m=re.match(r'^\s*(\d+)\s+(.+)',line)
        if not m:continue
        for c in m[2]:
            if not c.isspace():chars.append(c);loc.append((page,int(m[1])))
hay=''.join(chars);records=[];hunks=[]
for m in re.finditer(r'^"(.*)"\n(\([^\n]+\))',s,re.M):
    quote,old=m.groups();record=dict(quote=quote,old=old,line=s[:m.start()].count('\n')+1)
    if quote not in text:
        record['status']='quote_not_exact'
    elif 'Table ' in old and ('final municipality row' in old or 'table note' in old):
        ti=int(re.search(r'Table (\d+)',old)[1])
        rows=d.tables[ti-1].rows
        if 'table note' in old:
            assert rows[-1].cells[0].text.strip()==quote
            label='table note'
        else:
            data_rows=[row for row in rows if not row.cells[0].text.startswith('Note:')]
            assert data_rows[-1].cells[0].text==quote
            label='final municipality row'
        pages=[i+1 for i,p in enumerate(pdf.split('\f')) if f'Table {ti}.' in p]
        assert len(pages)==1
        page_text=pdf.split('\f')[pages[0]-1]
        if label=='table note':
            assert re.sub(r'\s+','',quote) in re.sub(r'\s+','',page_text)
        else:
            assert all(word in page_text for word in quote.split())
        record.update(status='verified',new=f'(Page {pages[0]}, Table {ti}, {label})')
    else:
        needle=re.sub(r'\s+','',quote)
        if hay.count(needle)!=1:record['status']='render_match_required'
        else:
            i=hay.index(needle);a,b=loc[i],loc[i+len(needle)-1]
            page=f'Page {a[0]}' if a[0]==b[0] else f'Pages {a[0]}–{b[0]}'
            record.update(status='verified',new=f'({page}, Lines {a[1]}–{b[1]})')
    if record.get('new') and record['new']!=old:
        hunks.append(f'@@\n "{quote}"\n-{old}\n+{record["new"]}')
    records.append(record)
(out/'locator-audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(out/'locator-only.patch').write_text('*** Begin Patch\n*** Update File: '+str(path)+'\n'+'\n'.join(hunks)+'\n*** End Patch\n')
print(json.dumps(dict(total=len(records),verified=sum(r['status']=='verified' for r in records),updates=len(hunks),issues=[r for r in records if r['status']!='verified']),ensure_ascii=False,indent=2))
