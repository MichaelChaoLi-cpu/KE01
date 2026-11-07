"""Project-local compatibility adapter for two human-approved table locators.

Keep the installed converter unchanged; retain all its validation and styling.
"""
import importlib.util
import re
from pathlib import Path
from repair_response_namespaces import repair
from zipfile import ZipFile
from lxml import etree


def separate_reviewer_numbering(path):
    """Give the original reviewer 1/2 headings their own Word list instance."""
    w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    with ZipFile(path) as z:
        entries = [(i, z.read(i.filename)) for i in z.infolist()]
    parts = {i.filename: b for i, b in entries}
    doc = etree.fromstring(parts['word/document.xml'])
    # Keep the closing thanks on the summary page without changing text/styles.
    body = doc.find(w+'body')
    for p in list(body):
        value = ''.join(p.xpath('.//w:t/text()', namespaces={'w': w[1:-1]}))
        if value in ('Thank you to the editor and reviewers for their careful review.', 'The main revisions are:', 'We thank the editor and reviewers again for their constructive comments and careful consideration of our revised manuscript.'):
            following = p.getnext()
            if following is not None and following.tag == w+'p' and not following.xpath('.//w:t|.//w:br', namespaces={'w': w[1:-1]}):
                body.remove(following)
    numbering = etree.fromstring(parts['word/numbering.xml'])
    new_id = str(max(int(n.get(w+'numId')) for n in numbering.findall(w+'num')) + 1)
    original = next(n for n in numbering.findall(w+'num') if n.get(w+'numId') == '2')
    num = etree.SubElement(numbering, w+'num', {w+'numId': new_id})
    etree.SubElement(num, w+'abstractNumId', {w+'val': original.find(w+'abstractNumId').get(w+'val')})
    override = etree.SubElement(num, w+'lvlOverride', {w+'ilvl': '0'})
    etree.SubElement(override, w+'startOverride', {w+'val': '1'})
    found = []
    for p in doc.iter(w+'p'):
        text = ''.join(p.itertext())
        if text in ('General Assessment', 'Comments'):
            node = p.find(w+'pPr/'+w+'numPr/'+w+'numId')
            assert node is not None and node.get(w+'val') == '2'
            node.set(w+'val', new_id)
            found.append(text)
    assert found == ['General Assessment', 'Comments'], found
    parts['word/document.xml'] = etree.tostring(doc, xml_declaration=True, encoding='utf-8')
    parts['word/numbering.xml'] = etree.tostring(numbering, xml_declaration=True, encoding='utf-8')
    staging = path.with_suffix('.numbering-fixed.docx')
    with ZipFile(staging, 'w') as z:
        for info, _ in entries:
            z.writestr(info, parts[info.filename])
    staging.replace(path)

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / '.codex/skills/convert-response-docx'
spec = importlib.util.spec_from_file_location('response_converter', SKILL / 'scripts/md_to_response_docx.py')
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)
approved = {
    '(Page 43, Table 1, final municipality row)': '"Kamiamakusa City"',
    '(Page 45, Table 3, final municipality row)': '"Nankan Town"',
    **{f'(Page {42+i}, Table {i}, table note)': f'"Note: Ten municipalities are shown in the existing table order; Table S{i+1} provides all 45 municipalities."' for i in range(1,4)},
}
converter.LOCATOR_RE = re.compile('(?:' + converter.LOCATOR_RE.pattern + '|' + '|'.join(re.escape(x) for x in approved) + ')')


def validate(text):
    lines = text.splitlines()
    for locator, quote in approved.items():
        assert lines.count(locator) == 1, locator
        assert lines[lines.index(locator) - 1] == quote, locator
    converter.validate_external_response(text)


if __name__ == '__main__':
    source = ROOT / 'Rev/revision/response-draft.md'
    text = source.read_text()
    validate(text)
    for bad in ['(Page XX, Lines XX–XX)', '(Page 42, Table 1, final municipality row)', '(Page 41, Table 2, final municipality row)', '']:
        try:
            validate(text.replace(next(iter(approved)), bad))
        except (AssertionError, RuntimeError):
            pass
        else:
            raise AssertionError('Invalid locator accepted: ' + bad)
    print('Positive and four negative locator tests passed')
    converter.main(['converter', str(source), str(SKILL / 'assets/response-template.docx'), str(ROOT / 'Rev/revision/response-draft.docx')])
    output = ROOT / 'Rev/revision/response-draft.docx'
    staging = output.with_suffix('.namespace-fixed.docx')
    repair(output, staging)
    staging.replace(output)
    separate_reviewer_numbering(output)
