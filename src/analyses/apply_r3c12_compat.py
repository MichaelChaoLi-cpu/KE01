"""Approved 014 narrow adapter; transactions and audit logs use bundled editor."""
import copy
from apply_revision_pagination_compat import editor

original = editor.patch_normal

def patch(root, spec, change_id, author, when):
    if 'table_index' not in spec:
        assert spec['comment_id']=='reviewer-3/comment-12'
        assert 'KILA-D-20261003-014' in spec['decision_ids']
        p,idx,start,_=editor.locate_unique_part(root,spec['before'],None)
        assert editor.paragraph_text(p)==spec['before']
        assert spec['after'].startswith(spec['before'])
        suffix=spec['after'][len(spec['before']):]
        run=p.findall('w:r',editor.NS)[-1]
        insertion=editor.make_change_wrapper('ins',change_id,author,when)
        insertion.append(editor.make_text_run(suffix,editor.clone_rpr(run)))
        p.append(insertion)
        assert editor.paragraph_text(p)==spec['after']
        return change_id+1,[{'operation':'insert','before':'','after':suffix}],[change_id],editor.rpr_fingerprint(run),[{'paragraph_index':idx,'character_offset':len(spec['before'])}]
    assert spec['comment_id'] == 'reviewer-3/comment-12'
    assert 'KILA-D-20261003-014' in spec['decision_ids']
    i = spec['table_index']
    assert i in [0, 1, 2] and spec['part_id'] == f'part-0{i+2}'
    pristine = editor.etree.tostring(root)
    table = root.xpath('./w:body/w:tbl', namespaces=editor.NS)[i]
    rows = table.findall('w:tr', editor.NS)
    assert len(rows) == 46
    assert not table.xpath('./w:tr/w:trPr/w:del|./w:tr/w:trPr/w:ins', namespaces=editor.NS)
    values = [[editor.paragraph_text(p) for p in row.xpath('./w:tc/w:p', namespaces=editor.NS)] for row in rows]
    assert values == spec['cells_before']
    ids = []
    for row in rows[11:]:
        pr = row.find('w:trPr', editor.NS)
        assert pr is not None
        pr.append(editor.make_change_wrapper('del', change_id, author, when))
        ids.append(change_id)
        change_id += 1
    # Rejecting ONLY these new row deletions exactly recovers the input XML.
    restored = copy.deepcopy(root)
    for node in restored.xpath('.//w:trPr/w:del', namespaces=editor.NS):
        if int(node.get(editor.qn(editor.W_NS, 'id'))) in ids:
            node.getparent().remove(node)
    assert editor.etree.tostring(restored) == pristine
    return change_id, [{'operation':'delete-rows','before':spec['before'],'after':spec['after']}], ids, 'all original row/cell formatting preserved', [{'table_index':i,'data_rows_deleted':'11–45'}]

editor.patch_normal = patch
if __name__ == '__main__':
    editor.main()
