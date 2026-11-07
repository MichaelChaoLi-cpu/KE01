"""Approved R3/C10 exception: preserve a leading rendered-page marker.

All actual tracked edits, backups, field guards and logging remain owned by
the bundled patcher. Only its in-memory simple-run adapter is extended.
"""
from pathlib import Path
import importlib.util
import copy

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / '.codex/skills/edit-markup-docx/scripts/apply_tracked_revision.py'
spec = importlib.util.spec_from_file_location('tracked_editor', path)
editor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editor)
original = editor.simple_run_for_node


def compatible_run(node, paragraph):
    run = node.getparent()
    if run is not None and run.getparent() is paragraph:
        children = [c for c in run if c.tag != editor.qn(editor.W_NS, 'rPr')]
        if (len(children) == 2
                and children[0].tag == editor.qn(editor.W_NS, 'lastRenderedPageBreak')
                and children[1] is node
                and node.tag == editor.qn(editor.W_NS, 't')
                and not editor.has_ancestor(run, {'ins', 'del', 'moveFrom', 'moveTo'})):
            # A zero-width cached pagination marker precedes the unchanged text.
            # Preserve the marker exactly in a separate run at the same position.
            marker_run = editor.etree.Element(editor.qn(editor.W_NS, 'r'), attrib=dict(run.attrib))
            props = run.find('w:rPr', namespaces=editor.NS)
            if props is not None:
                marker_run.append(copy.deepcopy(props))
            marker_run.append(children[0])
            paragraph.insert(paragraph.index(run), marker_run)
    return original(node, paragraph)


editor.simple_run_for_node = compatible_run
if __name__ == '__main__':
    editor.main()
