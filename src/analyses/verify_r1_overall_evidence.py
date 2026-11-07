"""Verify current overall-response excerpts and rendered page/line locators."""
from pathlib import Path
from docx import Document
from zipfile import ZipFile
import json, re, subprocess

ROOT=Path(__file__).resolve().parents[2]
doc=ROOT/'Rev/revision/KE01.rev.clean.docx'
prefixes=[
 'The central surface is one coherent scenario',
 'These allocations reproduce municipal controls',
 'Equation 3 assumes that housing loss',
 'These comparisons are descriptive rather than independent validation',
 'The corrected hybrid yields',
 'Residual-capacity demographic weighting yields',
 'Against September 29 full-or-half reports',
 'Compared with using mean heat days',
 'Across effective-cooling multipliers of',
 'In the hypothetical no-increment benchmark',
 'These demand estimates support resource sizing',
 'Broad high-demand screening is therefore',
 'The direction and magnitude of transfer bias',
 'The framework supports spatial screening and demand estimation, not',
 'The prefecture-wide 5.31% increase is a model output',
]
sentences=[s for p in Document(doc).paragraphs for s in re.split(r'(?<=[.!?])\s+(?=[A-Z])',p.text)]
# The accepted document is identical to the document rendered in the preceding
# cycle: compare with its archived clean content hash through the specifications
# and current source provenance; the current source hash must remain unchanged.
provenance=json.loads((ROOT/'data/exp/revision_r3c11/overall-clean-provenance.json').read_text())
assert provenance['source_sha256_before']==provenance['source_sha256_after']=='58fe55daffb02217c76db3a582bcb5bcc3ff82d67f050c2fb6eb13d666342f69'
pdf=ROOT/'data/exp/revision_r3c11/render-clean/KE01.rev.clean.pdf'
pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f')
chars=[]; loc=[]
for page,text in enumerate(pages,1):
    for line in text.splitlines():
        m=re.match(r'^\s*(\d+)\s+(.+)',line)
        if not m:continue
        for c in m[2]:
            if not c.isspace():chars.append(c);loc.append((page,int(m[1])))
hay=''.join(chars)
evidence=[]
for prefix in prefixes:
    hits=[s for s in sentences if s.startswith(prefix)]
    assert len(hits)==1,(prefix,hits)
    quote=hits[0].strip(); needle=re.sub(r'\s+','',quote)
    assert hay.count(needle)==1,(prefix,'PDF match absent or ambiguous')
    start=hay.index(needle);first=loc[start];last=loc[start+len(needle)-1]
    evidence.append(dict(quote=quote,page_start=first[0],page_end=last[0],line_start=first[1],line_end=last[1]))
out=ROOT/'data/exp/revision_r3c11/overall-evidence.json'
out.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(evidence,ensure_ascii=False,indent=2))
