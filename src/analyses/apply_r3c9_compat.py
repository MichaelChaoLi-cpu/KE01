"""R3/C9 part 03 only: approved marker-preserving bundled-editor adapter."""
import sys
from pathlib import Path
from apply_revision_pagination_compat import editor

if __name__ == '__main__':
    if 'apply' in sys.argv:
        spec = editor.load_spec(Path(sys.argv[sys.argv.index('--spec') + 1]))
        if (spec['comment_id'], spec['part_id']) != ('reviewer-3/comment-9', 'part-03'):
            raise SystemExit('Adapter restricted to approved R3/C9 part 03')
        if 'KILA-D-20261002-036' not in spec.get('decision_ids', []):
            raise SystemExit('Supplemental approval required')
    editor.main()
