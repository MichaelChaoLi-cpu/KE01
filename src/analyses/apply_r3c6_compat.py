"""User-approved 030 adapter: add a sibling insertion without editing old w:ins.

Delegates tracking, backups, package checks, and logging to the skill patcher.
Only the exact approved P2 zero-width insertion has an extra safe route.
"""
import copy
from apply_revision_pagination_compat import editor

original_replace = editor.replace_range
original_normal = editor.patch_normal
NEW = ('The proxies are the census general-household count, mapped-building '
       'polygon count and summed mapped-building footprint area within each '
       'disclosure group. ')
OLD = ' Building proxies are weighting variables, not counts of residences.'


def compatible_replace(paragraph, start, end, replacement, change_id, author,
                       when, replacement_xml=None):
    if start == end and replacement == NEW and replacement_xml is None:
        matches = [s for s in editor.text_segments(paragraph)
                   if s['start'] + 1 == start and s['node'].text == OLD]
        if len(matches) != 1:
            raise editor.RevisionError('Approved P2 insertion anchor differs')
        run, insertion = editor.inserted_run_for_node(matches[0]['node'], paragraph)
        if len(insertion) != 1:
            raise editor.RevisionError('P2 requires a single intact prior insertion run')
        old_xml = editor.etree.tostring(insertion)
        before = editor.paragraph_text(paragraph)
        # Move the new sentence's trailing space to its front. This lets the
        # entire prior insertion (including its leading space) remain unchanged.
        sibling = editor.make_change_wrapper('ins', change_id, author, when)
        sibling.append(editor.make_text_run(' ' + replacement[:-1], editor.clone_rpr(run)))
        paragraph.insert(paragraph.index(insertion), sibling)
        assert editor.etree.tostring(insertion) == old_xml
        assert editor.paragraph_text(paragraph) == before[:start] + replacement + before[start:]
        return change_id + 1, [change_id], editor.rpr_fingerprint(run)
    return original_replace(paragraph, start, end, replacement, change_id,
                            author, when, replacement_xml)


def guarded_normal(root, spec, change_id, author, when):
    if spec['comment_id'] != 'reviewer-3/comment-6':
        raise editor.RevisionError('Adapter is restricted to R3/C6')
    if 'KILA-D-20261002-030' not in spec.get('decision_ids', []):
        raise editor.RevisionError('Explicit compatibility exception required')
    if spec['part_id'] not in {'part-01', 'part-02', 'part-03'}:
        raise editor.RevisionError('Unapproved part')
    prior = {(x.tag, x.get(editor.qn(editor.W_NS, 'id'))):
             editor.etree.tostring(x, method='c14n')
             for x in root.xpath('.//w:ins | .//w:del', namespaces=editor.NS)}
    protected = [editor.etree.tostring(x, method='c14n') for x in root.xpath(
        './/m:oMath | .//w:hyperlink | .//w:fldChar | .//w:instrText', namespaces=editor.NS)]
    result = original_normal(root, spec, change_id, author, when)
    current = {(x.tag, x.get(editor.qn(editor.W_NS, 'id'))):
               editor.etree.tostring(x, method='c14n')
               for x in root.xpath('.//w:ins | .//w:del', namespaces=editor.NS)}
    assert all(current.get(k) == v for k, v in prior.items()), 'Prior revision changed'
    assert protected == [editor.etree.tostring(x, method='c14n') for x in root.xpath(
        './/m:oMath | .//w:hyperlink | .//w:fldChar | .//w:instrText', namespaces=editor.NS)]
    return result


editor.replace_range = compatible_replace
editor.patch_normal = guarded_normal
if __name__ == '__main__':
    editor.main()
