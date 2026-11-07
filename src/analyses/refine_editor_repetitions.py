"""Four human-approved minimal re-edits through the bundled tracked editor."""
from pathlib import Path
import importlib.util,json,shutil,sys,copy,difflib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/exp/editor_repetition_refinement_v4'; OUT.mkdir(parents=True,exist_ok=True)
s=importlib.util.spec_from_file_location('editor',ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
parts=[
('4.1','The contribution is to make that link explicit in a common spatial accounting chain, not to establish a new causal effect of housing damage on mortality.','This contribution does not establish a new causal effect of housing damage on mortality.','part-01'),
('4.2','A policy implication is to assess effective cooled placement as a service to be maintained, rather than equating a listed shelter with delivered protection. ','','part-02'),
('4.2','Municipality totals support preliminary resource staging, while disclosure-group estimates identify areas for local assessment. ','','contribution-04'),
('4.3','Peak demand informs electrical-capacity checks, whereas daily energy informs sustained operation and fuel planning. ','','contribution-05')]
for loc,anchor,addition,prior in [
('Introduction','The integration question is how early housing-damage information can inform the thermal protection needs of older residents and the electricity required to meet those needs.','Modeling of concurrent heat waves and blackouts illustrates how disruption of cooling provision can amplify heat-related health risks.','contribution-01'),
('4.1','In this interpretation, the cascade concerns the interruption and replacement of protection, not a modeled increase in the meteorological hazard.','Research on cascading risks emphasizes how dependencies and vulnerabilities shape impacts beyond the initiating hazard.','contribution-02')]:
 parts.append((loc,anchor,addition+' '+anchor,prior))
original_reedit=e.patch_reedit
def compatible_reedit(root,spec):
 assert spec['decision_ids']==['KILA-D-20261005-004','KILA-D-20261005-005']
 assert spec==json.loads((OUT/f"part-{int(spec['part_id'].split('-')[-1]):02}.json").read_text())
 p,_,start,end=e.locate_unique_part(root,spec['before'],None)
 segments=[s for s in e.text_segments(p) if s['end']>start and s['start']<end]
 containers={s['node'].getparent().getparent() for s in segments}
 assert len(containers)==1
 ins=containers.pop();q=lambda n:e.qn(e.W_NS,n)
 assert ins.tag==q('ins') and ins.getparent() is p
 oldtext=''.join(ins.xpath('.//w:t/text()',namespaces=e.NS));saved=[];offset=0
 for run in list(ins):
  assert run.tag==q('r')
  markers=run.findall(q('lastRenderedPageBreak'))
  if markers:
   if not run.findall(q('t')):
    assert len(markers)==1 and all(c.tag in {q('rPr'),q('lastRenderedPageBreak')} for c in run)
    saved.append((offset,run));ins.remove(run);continue
   assert len(markers)==1 and len(run.findall(q('t')))==1
   assert all(c.tag in {q('rPr'),q('t'),q('lastRenderedPageBreak')} for c in run)
   marker=markers[0];assert run.index(marker)<run.index(run.find(q('t')))
   new=e.etree.Element(q('r'))
   if run.find(q('rPr')) is not None:new.append(copy.deepcopy(run.find(q('rPr'))))
   new.append(marker);saved.append((offset,new))
  offset+=len(''.join(run.xpath('./w:t/text()',namespaces=e.NS)))
 result=original_reedit(root,spec)
 newtext=''.join(ins.xpath('.//w:t/text()',namespaces=e.NS))
 opcodes=difflib.SequenceMatcher(None,oldtext,newtext,autojunk=False).get_opcodes()
 for oldoffset,marker in saved:
  mapped=len(newtext)
  for tag,a,b,c,d in opcodes:
   if a<=oldoffset<=b:
    mapped=c+oldoffset-a if tag=='equal' else c;break
  offset=0
  for run in list(ins):
   node=run.find(q('t'))
   if node is None:continue
   value=node.text or ''
   if offset<=mapped<=offset+len(value):
    at=mapped-offset;idx=ins.index(run)
    if at==0:ins.insert(idx,marker)
    elif at==len(value):ins.insert(idx+1,marker)
    else:
     tail=copy.deepcopy(run);tail.find(q('t')).text=value[at:];node.text=value[:at]
     ins.insert(idx+1,marker);ins.insert(idx+2,tail)
    break
   offset+=len(value)
  else:ins.append(marker)
 return result
e.patch_reedit=compatible_reedit

def verify(before,after,ids):
 _,a=e.read_package(before);_,b=e.read_package(after)
 ar=e.etree.fromstring(a['word/document.xml']);br=e.etree.fromstring(b['word/document.xml'])
 canon=lambda n:e.etree.tostring(n,method='c14n')
 xp='.//m:oMath|.//w:hyperlink|.//w:fldChar|.//w:instrText|.//w:tbl|.//w:lastRenderedPageBreak'
 assert [canon(n) for n in ar.xpath(xp,namespaces=e.NS)]==[canon(n) for n in br.xpath(xp,namespaces=e.NS)]
 revisions=lambda r:{(n.tag,n.get(e.qn(e.W_NS,'id'))):canon(n) for n in r.xpath('.//w:ins|.//w:del|.//w:moveFrom|.//w:moveTo',namespaces=e.NS)}
 old,new=revisions(ar),revisions(br)
 for key,value in old.items():
  if key[0]==e.qn(e.W_NS,'ins') and key[1] in set(map(str,ids)):continue
  assert new.get(key)==value,key
 for name in a:
  if name not in {'word/document.xml','word/settings.xml'}:assert a[name]==b[name],name
 return e.validate_docx(after)
for i,(loc,before,after,prior) in enumerate(parts,1):
 spec=dict(schema_version=1,comment_id='editor/overall-comment',part_id=f'deduplicate-{i:02}',mode='reedit',decision_ids=['KILA-D-20261005-004','KILA-D-20261005-005'],location=f'Section {loc}',reason='Approved deduplication or literature bridge; citations remain human-owned.',before=before,after=after,reedit_confirmed=True,revises=[f'editor/overall-comment#{prior}'])
 (OUT/f'part-{i:02}.json').write_text(json.dumps(spec,indent=2)+'\n')
source=ROOT/'Rev/revision/KE01.rev.markup.docx'
formal='--formal' in sys.argv
if formal:
 assert len(json.loads((OUT/'copy-receipts.json').read_text()))==6
 assert e.sha256_path(source)==(OUT/'source-sha.txt').read_text()
 doc=source;log=ROOT/'Rev/docs/revisionchanges.md'
else:
 doc=OUT/'test.docx';log=OUT/'test-log.md'
 assert not doc.exists();shutil.copy2(source,doc)
 (OUT/'source-sha.txt').write_text(e.sha256_path(source))
receipts=[]
for i in range(1,7):
 spec=OUT/f'part-{i:02}.json'
 e.apply_revision(doc,log,spec,'Kila',True)
 r=e.apply_revision(doc,log,spec,'Kila',False)
 r['independent_verification']=verify(Path(r['backup']),doc,r['revision_ids'])
 receipts.append(r)
 (OUT/('formal-receipts.json' if formal else 'copy-receipts.json')).write_text(json.dumps(receipts,indent=2)+'\n')
 print(i,'applied and verified',flush=True)
