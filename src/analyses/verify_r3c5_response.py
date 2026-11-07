"""Verify exact DOCX quotations and printed page/line ranges for one response."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import subprocess, re, json, hashlib

ROOT=Path(__file__).resolve().parents[2]
response=(ROOT/'Rev/revision/response-draft.md').read_text()
section=response.split('# Reviewer 3\n',1)[1].split('## Comment 5\n',1)[1].split('## Comment 6\n',1)[0]
structured=(ROOT/'Rev/docs/structuredcomments.md').read_text().split('# Reviewer 3\n',1)[1].split('## Comment 5\n',1)[1].split('## Comment 6\n',1)[0]
assert section.split('**Response:**')[0].strip()==structured.strip()
clean=ROOT/'Rev/revision/KE01.rev.clean.docx'
with ZipFile(clean) as z, ZipFile(ROOT/'data/exp/revision_object_replacement/KE01.objects.clean.docx') as old:
    assert z.namelist()==old.namelist() and all(z.read(n)==old.read(n) for n in z.namelist())
    tree=E.fromstring(z.read('word/document.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paragraphs=[''.join(p.xpath('.//w:t/text()',namespaces=ns)) for p in tree.findall('w:body/w:p',ns)]
pdf=ROOT/'data/exp/revision_object_replacement/render/KE01.objects.clean.pdf'
pages=subprocess.check_output(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),'-'],text=True).split('\f')
def norm(s): return ''.join(c.lower() for c in s if c.isalnum())
quoted=re.findall(r'^"(.+)"\n\(Pages? (\d+)(?:–(\d+))?, Lines (\d+)–(\d+)\)$',section,re.M)
assert len(quoted)==15
results=[]
for quote,first,last,start,end in quoted:
    assert sum(quote in p for p in paragraphs)==1,quote
    lo,hi=int(start),int(end); first=int(first);last=int(last or first)
    numbered=[]
    for page in range(first,last+1):
        for line in pages[page-1].splitlines():
            m=re.match(r'^\s*(\d+)\s{2,}(.*)$',line)
            if m and lo<=int(m[1])<=hi:numbered.append((page,int(m[1]),m[2]))
    joined=''.join(norm(t) for _,_,t in numbered);target=norm(quote)
    assert target in joined,(first,lo,hi,quote)
    # Require both endpoints to be used, not merely a broad enclosing range.
    assert target not in ''.join(norm(t) for _,_,t in numbered[1:])
    assert target not in ''.join(norm(t) for _,_,t in numbered[:-1])
    results.append(dict(quote=quote,pages=[first,last],lines=[lo,hi],exact_docx_match=True,printed_locator_match=True))
body=section.split('**Response:**',1)[1]
for banned in ['XX','quotation tier','representative passages','required sample','approved bundle','part IDs','fresh clean','revisionchanges.md','KILA-D-','human verification required']:
    assert banned.lower() not in body.lower(),banned
report=dict(comment='reviewer-3/comment-5',quotations=results,quote_count=15,
            distinct_text_paragraphs=15,figure_objects=4,table_objects=3,
            counting_note='23 text parts occupy 15 distinct paragraphs; seven result objects give at least 22 distinct locations. 21+ tier requires 15 quotations.',
            clean_sha256=hashlib.sha256(clean.read_bytes()).hexdigest(),
            render_equivalence='All clean ZIP entries byte-identical to the rendered candidate.',
            status='pending human review')
(ROOT/'Rev/docs/r3-c5-response-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 15 exact quotations, every printed locator including its endpoints, reviewer text, external cleanliness.')
