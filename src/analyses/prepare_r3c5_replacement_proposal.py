"""Prepare, but never apply, the linked R3/C5 manuscript replacement proposal."""
from pathlib import Path
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
import pandas as pd
from openpyxl import load_workbook
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'Rev/revision/KE01.rev.clean.docx'
MARKUP = ROOT / 'Rev/revision/KE01.rev.markup.docx'
OUT = ROOT / 'Rev/docs/proposal-r3-c5.md'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def text(e):
    return ''.join(t.text or '' for t in e.findall('.//w:t', NS))
with zipfile.ZipFile(DOC) as z:
    body = ET.fromstring(z.read('word/document.xml')).find('w:body', NS)
    pars = body.findall('w:p', NS)
    rels = {e.get('Id'): e.get('Target') for e in ET.fromstring(z.read('word/_rels/document.xml.rels'))}
with zipfile.ZipFile(MARKUP) as z:
    mp = ET.fromstring(z.read('word/document.xml')).find('w:body', NS).findall('w:p', NS)
parts = []
def add(p, before, after, label):
    assert text(pars[p]).count(before) == 1, (p, before)
    start = text(pars[p]).index(before)
    assert all(x['paragraph'] != p or start + len(before) <= x['start'] or start >= x['end'] for x in parts)
    # Match the exact span against earlier tracked insertions, not just paragraph identity.
    insertion_overlap = []
    for ins in mp[p].findall('.//w:ins', NS):
        value = text(ins)
        if value and (value in before or before in value):
            insertion_overlap.append(value)
    assert not insertion_overlap, (p, insertion_overlap)
    parts.append(dict(id=f'P{len(parts)+1:02}', paragraph=p, label=label,
                      before=before, after=after, start=start, end=start+len(before),
                      shared_paragraph_with_prior_insert=bool(mp[p].findall('.//w:ins', NS))))

add(25, 'We construct disclosure-group allocation weights from an exposure proxy and exponential distance decay from the official epicenter.',
    'We construct disclosure-group allocation weights from an exposure proxy and exponential distance decay from the official epicenter. This is a study-defined total-constrained screening allocation, not a fitted damage-prediction model. Groups without general households receive zero allocation; the remaining weights are renormalized to conserve the scenario total.', '2.4: provenance and eligibility')
add(27, 'Housing-loss scenarios cross three exposure proxies, three distance-decay scales, and three half-collapse weights, producing 27 allocations.',
    'Housing-loss scenarios cross general households, mapped-building count and mapped footprint area with three distance-decay scales and half-collapse weights of 0, 0.5 and 1, producing 27 allocations. Building proxies are weighting variables, not counts of residences.', '2.4: structural ensemble')
add(29, 'The central surface is the normalized pointwise median of the allocation scenarios constrained to the approved central functional-loss total.',
    'The central surface is one coherent scenario using general households, a 20-km decay scale and a half-collapse weight of 0.5, giving 303.5 functional-loss units. Household counts align the allocation denominator with the target population; 20 km and 0.5 are transparent planning assumptions, not empirically optimized parameters or a calibrated loss fraction. The normalized pointwise-median surface, rebuilt after the zero-household correction, is retained only as a separate sensitivity.', '2.4: replace hybrid primary')
add(30, "We associate structural housing loss with older residents by scaling each group's population aged 65 or older by its modeled share of general households lost.",
    "We associate structural housing loss with older residents by scaling each group's estimated general-household population aged 65 or older by its modeled share of general households lost. For each group, the lower bound is the number of households containing an older member; the upper bound is the all-resident older population where that lower bound is positive, and zero otherwise. Starting from the lower bound, we distribute the municipal remainder in proportion to older-household counts, subject to the upper bounds, to match official municipal general-household older-population controls. Groups are assigned to municipalities by representative points. Residual-capacity weighting is a separate demographic sensitivity. These allocations reproduce municipal controls but do not validate within-municipality residence patterns. Equation 3 assumes that housing loss is not systematically associated with age composition within a group; exposure is defined as zero where general households are zero.", '2.4: bounded demographic allocation and Eq. 3 assumption')
add(30, 'is the resident older population', 'is the estimated general-household older population', '2.4: Eq. 3 symbol definition; preserve OMML')
add(64, 'Additive disclosure-group outcomes are summed within municipality boundaries after the central scenario is selected at its defined analytical scale.',
    'Additive disclosure-group outcomes are summed using representative-point municipality assignments after the central scenario is selected at its defined analytical scale.', '2.8: consistent municipality geography')
anchor = 'Keeping them separate makes each planning range traceable to its assumption.'
add(66, anchor, anchor + ' We additionally compare the selected primary with the corrected hybrid, bounded demographic alternative and 54 hypothetical shaking allocations. For the latter, nearest-station JMA intensity categories are assigned in projected coordinates, including neighbouring-prefecture stations and excluding the withdrawn Tomiai observation. Three full-collapse vulnerability shapes from Suto et al. (2019, Equation 2 and Table 4; https://doi.org/10.5610/jaee.19.4_13) are crossed with two category-endpoint evaluations, three exposure proxies and three half-collapse weights. The wooden, steel and light-steel normal-CDF shapes use location/scale pairs (6.87, 0.73), (7.25, 0.63) and (7.24, 0.60), respectively. The open upper endpoint of intensity 7 uses the limiting value of one, not an observed intensity. Relative weights are normalized with household-capacity constraints; no caps bind. These are hypothetical weighting shapes, not local material shares or validated functional-loss probabilities. We assess municipality rank correlations, rank shifts and top-five overlap. Separate comparisons with July 31 and September 29 prefectural reports use full collapse, large-scale-half plus half collapse, and their combined counts. Share total-variation distance is half the sum of absolute municipal share differences. Report dates and categories are kept distinct from the planning snapshot. These comparisons are descriptive rather than independent validation: outcomes and assessment completeness differ, report zeros are not verified negatives, and report geography was examined before developing the alternatives.', '2.8: shaking and report-comparison design')

folder = ROOT / 'data/exp/revision_integrated_calculation'
def primary(name):
    d = pd.read_parquet(folder / (name+'.parquet'))
    return d.loc[d.demographic_scenario.eq('older_households')]
n = primary('municipal_need').set_index('Municipality Code')
p = primary('municipal_power'); pc = p.loc[p.engineering_scenario.eq('Central')].set_index('Municipality Code')
h = primary('municipal_health'); h = h.loc[h.health_scenario.eq('main_lower_missing')].set_index('Municipality Code')
total = n.older_exposure.sum()
add(77, 'The central exposure totals 245.794 residents aged 65 or older across Kumamoto.', f'The central exposure totals {total:.3f} residents aged 65 or older across Kumamoto.', '3.3: prefecture exposure')
add(77, 'Table 1 reports 134.030 central functionally lost residences and 90.383 affected older residents in Kumamoto City, followed by 54.839 residences and 48.287 older residents in Yatsushiro City. Across all municipalities, the central totals are 303.5 residences, 245.794 older residents, and 7,373.815 no-placement older-person-days.',
    f'Table 1 reports {n.loc["43100","functional_loss"]:.3f} central functionally lost residences and {n.loc["43100","older_exposure"]:.3f} affected older residents in Kumamoto City, followed by {n.loc["43202","functional_loss"]:.3f} residences and {n.loc["43202","older_exposure"]:.3f} older residents in Yatsushiro City. Across all municipalities, the central totals are 303.5 residences, {total:.3f} older residents, and {n.no_placement_person_days.sum():,.3f} no-placement older-person-days.', '3.3: municipality and person-day totals')
anchor = "The table's scenario ranges remain structural sensitivity summaries rather than inspection intervals."
add(77, anchor, anchor + ' The corrected hybrid yields 216.546 exposed older residents, 7.18% above the selected primary; municipal exposure rank correlation is 0.9818, with a maximum rank shift of six and the same top-five set. Residual-capacity demographic weighting yields 202.185 exposed older residents, with a maximum rank shift of one. Across the 54 shaking scenarios, exposure ranges from 133.49 to 363.43 and rank correlations from 0.8163 to 0.8978; maximum rank shifts are 16–24. All retain the exposure top-five set, but incremental-death top-five overlap is four of five. These ranges combine hazard, proxy and half-collapse assumptions and are not confidence intervals. Against September 29 full-or-half reports, the primary has rank correlation 0.7252, share total-variation distance 0.5845 and top-five overlap 3/5; the corresponding shaking ranges are 0.7732–0.8127, 0.2374–0.3855 and 4/5. The July 31 combined report has only five municipalities with positive counts; primary correlation is 0.3108 and share distance 0.9674. Thus stable high-exposure membership does not establish accurate reported-damage geography.', '3.3: validated sensitivity and limited agreement')
q = p.groupby('engineering_scenario')[['electric_kW','daily_kWh']].sum()
add(80, 'Peak power rises from 21.85 kW in the Low bundle to 34.583 kW in the Central bundle and 48.52 kW in the High bundle; corresponding daily electricity rises from 262.21 to 622.497 and 1,164.47 kWh.',
    f'Peak power rises from {q.loc["Low","electric_kW"]:.2f} kW in the Low bundle to {q.loc["Central","electric_kW"]:.3f} kW in the Central bundle and {q.loc["High","electric_kW"]:.2f} kW in the High bundle; corresponding daily electricity rises from {q.loc["Low","daily_kWh"]:.2f} to {q.loc["Central","daily_kWh"]:.3f} and {q.loc["High","daily_kWh"]:,.2f} kWh.', '3.4: engineering totals')
add(80, 'Table 2 gives Kumamoto City a Central requirement of 12.717 kW and 228.903 kWh per day, followed by Yatsushiro City at 6.794 kW and 122.292 kWh per day.',
    f'Table 2 gives Kumamoto City a Central requirement of {pc.loc["43100","electric_kW"]:.3f} kW and {pc.loc["43100","daily_kWh"]:.3f} kWh per day, followed by Yatsushiro City at {pc.loc["43202","electric_kW"]:.3f} kW and {pc.loc["43202","daily_kWh"]:.3f} kWh per day.', '3.4: municipality engineering values')
add(83, 'The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.34%, with a transferred-effect interval from 0.67% to 10.01%.',
    'The prefecture-weighted central 30-day mortality-burden increase without effective cooling is 5.31%, with source-effect endpoint scenarios of 0.66% and 9.96%; these endpoints are not whole-model confidence limits.', '3.5: aggregate effect and uncertainty label')
add(83, '0.01797', f'{h.loc["43100","expected_excess_deaths"]:.5f}', '3.5: Kumamoto incremental expected deaths')
add(83, '0.04380', f'{h.expected_excess_deaths.sum():.5f}', '3.5: prefecture incremental expected deaths')
add(99, 'In this study, epicentral distance remains an incomplete hazard representation, and the functional contribution of half-collapse varies across scenarios.',
    'In this study, epicentral distance remains an incomplete hazard representation, and the functional contribution of half-collapse varies across scenarios. The selected allocation is retained as transparent early demand screening, not validated municipal or building-level damage prediction. Report-share disagreement remains substantial; the closer descriptive agreement of shaking alternatives does not establish independent validity or justify post hoc selection. Nearest-station categories omit local site effects, source vulnerability curves are transferred beyond their original setting, and full-collapse shapes are used only as hypothetical functional-loss weights. Municipal calibration and demographic rank stability cannot verify within-group residence patterns or the assumed absence of systematic age-related loss differences.', '4.5: explicit residual validity limits')
add(3, 'approximately 246', 'approximately 202', 'Abstract: exposure')
add(3, '34.583 kW of peak cooling power and 622.497 kWh', '28.427 kW of peak cooling power and 511.691 kWh', 'Abstract: engineering')
add(3, '5.34%', '5.31%', 'Abstract: health')
add(123, text(pars[123]), text(pars[123]) + ' Panels b and c use the household/20-km/0.5 primary and bounded general-household older-population allocation; panel a is contextual evidence, not independent validation.', 'Figure 5 note')
add(127, 'whose values are not additive', 'derived from pointwise maxima across the 27 distance/proxy/half-collapse scenarios and not representing a jointly realized aggregate scenario', 'Figure 6 note: envelope')
add(131, text(pars[131]), text(pars[131]) + ' All bundles use the same selected primary population; daily energy assumes constant scenario power over the specified operating hours, not measured consumption or a verified supply shortfall.', 'Figure 7 note')
add(135, 'transferred effect interval', 'source-effect endpoint range, which excludes structural, engineering, baseline and transfer uncertainty', 'Figure 8 note')

assetroot = ROOT / 'data/exp/revision_asset_review'
objects = []
fig_names = ['functional_housing_loss_and_older_person_exposure','older_person_cooling_protection_need_and_placement_deficit','emergency_cooling_electricity_requirement_distribution','cooling_loss_related_incremental_mortality_risk_distribution']
for number, pi, name in zip(range(5,9), [121,125,129,133], fig_names):
    file = assetroot/'figures'/('Figure_'+name+'.png')
    rid = pars[pi].find('.//a:blip', NS).get('{'+NS['r']+'}embed')
    with Image.open(file) as im:
        assert min(im.info['dpi']) > 300
        size = im.size
    objects.append(dict(id=f'F{number}', target=f'Figure {number}; paragraph {pi}; {rid}; {rels[rid]}',
                        replacement=str(file.relative_to(ROOT)), sha256=sha(file), pixels=size,
                        operation='Human-owned inline image replacement; preserve anchor, aspect ratio, caption and approved page layout. Do not silently replace ZIP media.'))
tables = body.findall('w:tbl', NS)
assert len(tables) == 9
booknames = ['housing_loss_and_older_person_cooling_need_summary','cooling_electricity_planning_summary','cooling_loss_health_risk_summary']
for ti, name in enumerate(booknames,1):
    file = assetroot/'tables'/('Table_municipality_'+name+'.xlsx')
    wb = load_workbook(file, data_only=True)
    ws = wb.worksheets[0]
    assert ws.max_column == 6 and ws.max_row == 46
    for panel in range(3):
        table_index = (ti-1)*3+panel
        rows = tables[table_index].findall('w:tr', NS)
        # Preserve existing municipality row order, with cell-by-cell approved replacement values.
        old = [[text(c) for c in r.findall('w:tc', NS)] for r in rows]
        def display(cell):
            if not isinstance(cell.value, (float, int)):
                return str(cell.value)
            fmt = cell.number_format
            assert fmt.startswith(('0', '#,##0')), fmt
            decimals = len(fmt.split('.')[1]) if '.' in fmt else 0
            return format(cell.value, (',' if ',' in fmt else '') + f'.{decimals}f')
        byname = {r[0].value: [display(c) for c in r] for r in ws.iter_rows(min_row=2)}
        new = [list(next(ws.iter_rows(min_row=1,max_row=1,values_only=True)))]
        new += [byname[r[0]] for r in old[1:]]
        assert len(old) == len(new) == [17,17,14][panel] and all(len(r)==6 for r in old)
        assert [r[0] for r in old[1:]] == [r[0] for r in new[1:]], (ti,panel)
        objects.append(dict(id=f'T{ti}.{panel+1}', target=f'Table {ti}, panel {panel+1}/3; native Word table index {table_index}',
                            replacement=str(file.relative_to(ROOT)), sheet=ws.title,
                            rows='header row 1; municipality-name lookup from rows 2–46, preserving the existing 16/16/13 panel split', sha256=sha(file),
                            before=old, after=new,
                            operation='Human-owned native-table cell update; preserve six columns, row order, styles and captions. Use workbook displayed precision; do not paste workbook screenshots.'))

# Validate the recorded numerical-source and protected-production manifests. Clean is intentionally regenerated.
manifest = json.loads((assetroot/'validation.json').read_text())
for key in ['source_sha256', 'protected_sha256']:
    for name, expected in manifest[key].items():
        if name == 'Rev/revision/KE01.rev.clean.docx':
            continue
        assert sha(ROOT/name) == expected, name
for part in parts:
    part['after'] = part['after'].replace('https://doi.org/10.5610/jaee.19.4_13', 'https://www.jstage.jst.go.jp/article/jaee/19/4/19_4_13/_pdf')
payload = {'status':'proposal only; human exact-text and object-operation approval pending',
           'markup_sha256':sha(MARKUP), 'clean_sha256':sha(DOC), 'parts':parts, 'objects':objects,
           'asset_generator_current_sha256':sha(ROOT/'src/analyses/prepare_revision_asset_review.py'),
           'asset_generator_original_receipt_sha256':manifest['script_sha256'],
           'layout_note':'Current figure hashes freeze the subsequently accepted aligned frames and smaller emergency panel C; original validation receipt remains unchanged.'}
jsonpath = OUT.with_suffix('.json')
jsonpath.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
lines = ['# R3/C5 — exact linked replacement proposal', '',
         '**Status: proposal only. No manuscript, formal result asset or response has been replaced.**', '',
         f'Source markup SHA-256: `{sha(MARKUP)}`. Fresh-clean SHA-256: `{sha(DOC)}`.', '',
         '## Scope and approval boundary', '',
         f'{len(parts)} minimal text parts and 13 object operations (four figures; nine native Word table panels). This coupled batch also reconciles R1/C1–C3 and downstream numerical claims, but does not close those comments or replace their remaining source/interpretation reviews.', '',
         'Decisions 005, 008, 011 and 021 lock the calculation and screening interpretation. No new model selection is proposed. The original equations are retained; the population-symbol definition and zero-denominator rule are corrected in adjacent text. All source numbers below are read from the validated integrated outputs.', '',
         'Existing R3/C1, C8 and C10 insertions remain untouched. Several target paragraphs are shared, but proposed literal spans do not replace those insertions. Before execution, the tracked-edit tool must still dry-run each part and stop on structural/field overlap. No protected citation deletion is requested.', '',
         'Object replacements are a single supplemental human-owned exception bundle under the revision procedure. Approval of text is not permission to bypass this boundary. Tables are nine native Word tables, not images; preserve their current three-panel structure. Table condensation remains a separate pending decision.', '',
         'The Suto PDF link in P07 is a plain-text source link for the verified coefficient source, not a claim that an EndNote record has been inserted. Formal reference-manager integration remains human-owned.', '',
         '## Exact text parts', '']
for x in parts:
    lines += [f'### {x["id"]} — {x["label"]}', '',f'Locator: direct-body paragraph {x["paragraph"]} (zero-based; not a submission page/line locator). Shared paragraph with previous insertion: {x["shared_paragraph_with_prior_insert"]}.', '', '**Before**', '', x['before'], '', '**After**', '', x['after'], '']
lines += ['## Exact object operations', '']
for x in objects:
    lines += [f'### {x["id"]} — {x["target"]}', '', f'Replacement: `{x["replacement"]}`; SHA-256 `{x["sha256"]}`.', '', x['operation'], '']
    if 'sheet' in x:
        lines += [f'Sheet `{x["sheet"]}`; {x["rows"]}. Exact old/new cell matrices are in `proposal-r3-c5.json` under this operation ID. No municipality row is added, removed or reordered.', '']
lines += ['## Execution sequence after approval', '',
          '1. Save a recoverable snapshot and verify all proposal hashes. Dry-run each literal edit; apply approved parts sequentially with true tracked changes and exact revision records, preserving equations and citation fields.',
          '2. Human performs the four figure and nine native-table operations as one approved batch. Retain the accepted map alignment and reduced Figure 7 panel C. Archive old formal assets before a separately verified synchronized promotion; never mix new results with stale production inputs.',
          '3. Regenerate fresh clean, check every literal and table value, render all changed pages once, and refresh all affected response locators. Only then draft R3/C5 response for human acceptance. No comment becomes done from this proposal.', '',
          '## Checks and remaining boundaries', '',
          'All before-spans match uniquely in their current clean paragraphs; no proposal spans overlap. All three tables contain 45 municipality rows and six columns; all nine existing table-panel row orders match the proposed sources. Four figure PNGs exceed 300 dpi (400 dpi metadata). Numerical source and protected formal-asset hashes match the earlier receipt; clean changed only by authorized regeneration. Latest layout-specific asset hashes are recorded here without overwriting the original receipt.', '',
          'This is not a production-pipeline migration or final submission freeze. Engineering-source, health-transfer/baseline and overall-framing comment responses remain separately pending; their approved numerical assumptions are unchanged. Exact object operations require the human-owned exception route. No Git/DVC action is included.', '']
OUT.write_text('\n'.join(lines))
print(json.dumps({'proposal':str(OUT),'text_parts':len(parts),'object_parts':len(objects),'checks':'passed'},indent=2))
