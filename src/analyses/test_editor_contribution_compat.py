"""Copy-first integration and protected-object regression tests."""
from pathlib import Path
from zipfile import ZipFile
import json, shutil
from apply_editor_contribution_compat import editor as e, ROOT

OUT=ROOT/'data/exp/editor_contributions'
SOURCE=ROOT/'Rev/revision/KE01.rev.markup.docx'

def snapshot(path):
    _,files=e.read_package(path);r=e.etree.fromstring(files['word/document.xml'])
    canon=lambda x:e.etree.tostring(x,method='c14n')
    return files,r,dict(revisions={(x.tag,x.get(e.qn(e.W_NS,'id'))):canon(x) for x in r.xpath('.//w:ins|.//w:del|.//w:moveFrom|.//w:moveTo',namespaces=e.NS)},protected=[canon(x) for x in r.xpath('.//m:oMath|.//w:hyperlink|.//w:fldChar|.//w:instrText|.//w:tbl|.//w:lastRenderedPageBreak',namespaces=e.NS)])

def verify_pair(before,after,part):
    af,ar,a=snapshot(before);bf,br,b=snapshot(after)
    assert a['protected']==b['protected'],'Formula/citation/table/pagination object changed'
    for key,val in a['revisions'].items():
        if part==2 and key==(e.qn(e.W_NS,'ins'),'258'):continue
        assert b['revisions'].get(key)==val,('Prior revision changed',key)
    assert af.keys()==bf.keys()
    for n in af:
        if n not in {'word/document.xml','word/settings.xml'}:assert af[n]==bf[n],n
    return e.validate_docx(after)

def main():
    source_hash=e.sha256_path(SOURCE)
    copy=OUT/'copy-test-v2.docx';log=OUT/'copy-test-v2-log.md'
    assert not log.exists(),'Use a new test directory rather than overwrite test history'
    shutil.copy2(SOURCE,copy)
    receipts=[]
    for i in range(1,6):
        spec=OUT/f'part-{i:02}.json'
        dry=e.apply_revision(copy,log,spec,'Kila',True)
        prior=OUT/f'copy-before-{i:02}.docx';shutil.copy2(copy,prior)
        receipt=e.apply_revision(copy,log,spec,'Kila',False)
        receipt['independent_verification']=verify_pair(prior,copy,i)
        receipts.append(receipt)
        print('Copy part',i,'passed',flush=True)
    assert e.sha256_path(SOURCE)==source_hash
    # Check all approved added paragraphs and the re-edited span exactly.
    _,r,_=snapshot(copy);texts=[e.paragraph_text(p) for p in e.all_paragraphs(r)]
    for i in range(1,6):
        spec=json.loads((OUT/f'part-{i:02}.json').read_text())
        if i==2:assert sum(spec['after'] in t for t in texts)==1
        else:
            addition=next(t for t in spec['after'].split('\n\n') if t!=spec['before'])
            assert texts.count(addition)==1
    (OUT/'copy-test-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print('All copy tests passed; source unchanged.')

if __name__=='__main__':main()
