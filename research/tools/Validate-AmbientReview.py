"""Validate the S130 ambient-layer review: live counts, layers, freeze record."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ar = read('research/ambient-review.json')
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json'); sg = read('research/field-signs.json')
ag = read('research/ambient-gossip.json'); tg = read('research/town-gossip.json'); bg = read('research/band-gossip.json')
ia = read('research/interior-ambient.json'); da = read('research/district-ambient.json'); rep = read('research/town-reputation.json')
layers = {x['id']: x for x in ar['layers']}
check(len(ar['layers']) == 9, 'layers-9')
expect = {
 'field_npc': sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][k]) for k in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs']),
 'docs': len(fd['docs']) * 3, 'signs': len(sg['signs']) * 4, 'region_gossip': len(ag['lines']), 'town_gossip': len(tg['lines']),
 'band_reactions': len(bg['lines']), 'district_gossip': len(da['lines']), 'interior_ambient': len(ia['lines']),
 'counter_lines': sum(len(t['bands']) for t in rep['towns']),
}
for k, v in expect.items():
    check(layers[k]['lines'] == v, 'lines-' + k)
check(ar['total_lines'] == sum(expect.values()), 'total-lines')
check(len(ar['freeze']) >= 5, 'freeze-items')
check(len(ar['risks']) >= 3, 'risks')
stems = {p.stem for p in V.rglob('*.md')}
card = (V / '11_管理/氛围层总览与冻结建议.md').read_text(encoding='utf-8')
check('# 氛围层总览与冻结建议' in card and '## 冻结建议' in card and '## 边界' in card, 'card-structure')
check(f"共 **{ar['total_lines']}** 个可播单元" in card, 'card-total')
for x in ar['layers']:
    check(f"| {x['id']} | {x['scale']} | {x['count']} {x['unit']} | {x['lines']} |" in card, 'card-row-' + x['id'])
    check(f"[[{x['entry']}]]" in card, 'card-entry-' + x['id'])
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('AMBIENT-REVIEW-S130:BEGIN' in plan and '[[氛围层总览与冻结建议]]' in plan, 'plan-block-and-link')
check('AMBIENT-REVIEW-S130:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/ambient-review-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S130 ambient review: nine layers with live counts, freeze record, rendering and chain; review only, not runtime',
              layers=len(ar['layers']), total_lines=ar['total_lines'], checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/ambient-review-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
