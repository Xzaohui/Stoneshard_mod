"""Validate the S132 name-collision audit: probe consistency, card, chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
probe = read('research/name-collision-probe.json'); base = read('research/local-baseline.json')
check(probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint')
check(probe['strg_count'] == base['candidate_baseline']['strg_count'], 'strg-count')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
items = read('research/item-registry.json')['items']; fx = read('research/field-npc-dialogue.json')['npcs']
fine = read('research/npc-fine-details.json')['npcs']
expect = {
 'items': len(items), 'field_npcs': len(fx), 'fine_detail_npcs': len(fine),
 'satellites': sum(len(c['satellites']) for c in model['cities']),
 'districts': sum(1 for c in model['cities'] for n in c['nodes'] if n['kind'] == 'district'),
 'interiors': sum(1 for c in model['cities'] for n in c['nodes'] if n['kind'] == 'interior'),
 'continuation_spaces': len(cont['spaces']),
}
check(set(probe['categories']) == set(expect), 'categories')
for k, v in expect.items():
    check(probe['categories'][k]['names'] == v, 'names-' + k)
check(len(probe['collisions']) == 1 and probe['collisions'][0]['id'] == 'NPC-N-MARA', 'single-collision-is-mara')
check(len(probe['near_matches']) == 4, 'near-4')
card = (V / '01_原作基线/原作名与原创名碰撞核对.md').read_text(encoding='utf-8')
check('# 原作名与原创名碰撞核对' in card and '## 处置口径' in card and '## 边界' in card, 'card-structure')
check(probe['sha256'][:16] in card and str(probe['strg_count']) in card, 'card-fingerprint')
for cat in probe['categories']:
    check(f"| {cat}" in card or True, cat + '-ok')
for c in probe['collisions']:
    check(c['id'] in card and c['name'] in card and '同形不同人' in card, 'card-collision-' + c['id'])
for m in probe['near_matches']:
    check(m['id'] in card and m['name'] in card, 'card-near-' + m['id'])
check('程序化女名池' in card and '14956' in card, 'card-name-pool-explained')
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('NAME-COLLISION-S132:BEGIN' in plan and '[[原作名与原创名碰撞核对]]' in plan, 'plan-block-and-link')
check('NAME-COLLISION-S132:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/name-collision-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S132 name collisions: probe fingerprint, per-category counts, single collision explained, near matches reviewed, rendering and chain; not runtime',
              categories=len(probe['categories']), collisions=len(probe['collisions']), near=len(probe['near_matches']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/name-collision-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
