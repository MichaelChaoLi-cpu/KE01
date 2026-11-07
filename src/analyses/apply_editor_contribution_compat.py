"""Approved narrow adapter; bundled patcher retains transactions and audit logs.

Supports genuine tracked paragraph additions and preserves cached pagination
objects while re-editing the one approved existing insertion.
"""
from pathlib import Path
import copy, importlib.util, json

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('editor',ROOT/'.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py')
editor=importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)
W=editor.W_NS
q=lambda name: editor.qn(W,name)
original_reedit=editor.patch_reedit

def guard(spec):
    approved=json.loads((ROOT/'data/exp/editor_contributions'/f"part-{int(spec['part_id'].split('-')[-1]):02}.json").read_text())
    assert spec==approved and spec['comment_id']=='editor/overall-comment'
    assert 'KILA-D-20261005-003' in spec['decision_ids']

def props(p):
    node=p.find(q('pPr'))
    return copy.deepcopy(node) if node is not None else editor.etree.Element(q('pPr'))

def mark_boundary(p,change_id,author,when):
    pr=p.find(q('pPr'))
    if pr is None:pr=editor.etree.Element(q('pPr'));p.insert(0,pr)
    rp=pr.find(q('rPr'))
    if rp is None:rp=editor.etree.SubElement(pr,q('rPr'))
    assert not rp.findall(q('ins')) and not rp.findall(q('del'))
    rp.append(editor.make_change_wrapper('ins',change_id,author,when))

def new_paragraph(p,text,change_id,author,when,run):
    new=editor.etree.Element(q('p'));new.append(props(p))
    # New paragraphs inherit current formatting, not historical property changes.
    for node in list(new.iter()):
        if editor.etree.QName(node).localname.endswith('Change'):
            node.getparent().remove(node)
    mark_boundary(new,change_id,author,when)
    ins=editor.make_change_wrapper('ins',change_id+1,author,when)
    ins.append(editor.make_text_run(text,editor.clone_rpr(run)));new.append(ins)
    return new

def paragraph_addition(root,spec,change_id,author,when):
    guard(spec)
    p,index,start,end=editor.locate_unique_part(root,spec['before'],None)
    before=spec['before'];after=spec['after'];pid=spec['part_id']
    parent=p.getparent();assert parent.tag==q('body')
    old_text=editor.paragraph_text(p)
    old_props=editor.ppr_fingerprint(p)
    old_prop_values=[(x.tag,dict(x.attrib),x.text,x.tail) for x in props(p).iter()]
    segments=editor.text_segments(p)
    if pid in {'contribution-01','contribution-04'}:
        assert end==len(old_text) and after.startswith(before+'\n\n')
        addition=after[len(before)+2:]
        run=segments[-1]['node'].getparent()
        new=new_paragraph(p,addition,change_id,author,when,run)
        parent.insert(parent.index(p)+1,new)
        assert editor.ppr_fingerprint(p)==old_props
        assert editor.paragraph_text(p)==old_text
        ids=[change_id,change_id+1]
    else:
        assert pid in {'contribution-03','contribution-05'} and after.endswith('\n\n'+before)
        addition=after[:-len(before)-2]
        seg=next(s for s in segments if s['start']==start-1)
        assert seg['node'].text.startswith(' '+before)
        run=seg['node'].getparent();anchor=run.getparent()
        assert anchor.tag==q('ins') and anchor.getparent() is p
        cut=p.index(anchor)
        assert editor.paragraph_text(p)[:start].endswith(' ')
        # Split only between whole original children: no existing revision is split.
        suffix=editor.etree.Element(q('p'));suffix.append(props(p))
        for node in list(p)[cut:]:suffix.append(node)
        new=new_paragraph(p,addition,change_id,author,when,run)
        mark_boundary(p,change_id+2,author,when)
        pos=parent.index(p);parent.insert(pos+1,new);parent.insert(pos+2,suffix)
        assert editor.paragraph_text(p)+editor.paragraph_text(suffix)==old_text
        assert [(x.tag,dict(x.attrib),x.text,x.tail) for x in props(suffix).iter()]==old_prop_values
        ids=[change_id,change_id+1,change_id+2]
    assert editor.paragraph_text(new)==addition and not '\n' in addition
    return max(ids)+1,[dict(operation='insert-paragraph',before='',after=addition)],ids,editor.rpr_fingerprint(run),[dict(paragraph_index=index,character_offset=start,tracked_paragraph_boundaries=True)]

def reedit(root,spec):
    guard(spec);assert spec['part_id']=='contribution-02'
    p,_,start,end=editor.locate_unique_part(root,spec['before'],None)
    selected=[s for s in editor.text_segments(p) if s['end']>start and s['start']<end]
    containers={s['node'].getparent().getparent() for s in selected}
    assert len(containers)==1
    insertion=containers.pop();assert insertion.tag==q('ins') and insertion.getparent() is p
    # Isolate nonsemantic cached page-break markers without deleting any.
    for run in list(insertion):
        assert run.tag==q('r')
        breaks=run.findall(q('lastRenderedPageBreak'))
        if breaks:
            assert len(breaks)==1 and len(run.findall(q('t')))==1
            assert all(c.tag in {q('rPr'),q('t'),q('lastRenderedPageBreak')} for c in run)
            assert run.index(breaks[0])<run.index(run.find(q('t')))
            marker=editor.etree.Element(q('r'))
            if run.find(q('rPr')) is not None:marker.append(copy.deepcopy(run.find(q('rPr'))))
            marker.append(breaks[0]);insertion.insert(insertion.index(run),marker)
    return original_reedit(root,spec)

editor.patch_normal=paragraph_addition
editor.patch_reedit=reedit

if __name__=='__main__':editor.main()
