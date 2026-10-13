"""Validate the S109 rule-consistency audit by recomputing every row."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
au = read('research/rule-audit.json')
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json')
sg = read('research/field-signs.json'); fl = read('research/field-scene-flows.json')
inv = read('research/special-location-inventory.json')
check(len(au['rows']) == 14, 'row-count-14')
check(au['failed'] == [], 'no-failed-rows')
BANNED = ('reward', 'rewards', 'requires', 'repeatable', 'cooldown', 'deadline', 'paid', 'price', 'gold', 'coin_amount')
for name, data in [('field-npc-dialogue', fx), ('field-docs', fd), ('field-signs', sg), ('field-scene-flows', fl)]:
    keys = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items(): keys.add(k); walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    check(not [k for k in keys if k in BANNED], name + '-no-banned-keys')
check(all(n['site_lines'][2][1] for n in fx['npcs']), 'refusals-present')
check(all(n['visits']['proxy'] for n in fx['npcs']), 'proxies-present')
check(all(len(n['knows']) >= 2 and len(n['not_knows']) >= 2 for n in fx['npcs']), 'knowledge-limits')
check(all(len(n.get('english') or {}) == 14 for n in fx['npcs']), 'bilingual-parity')
check(all(d.get('text_en') for d in fd['docs']), 'docs-english')
check(all(s.get('danger_en') for s in sg['signs']), 'signs-english')
check(all({'refused', 'npc_absent', 'task_open', 'task_done'} <= {nd['when'] for nd in f['nodes']} for f in fl['flows']), 'flows-required-states')
cards = sorted((V / '02_世界与地图/特殊地点与野外NPC').glob('地点设计卡_*.md'))
check(len(cards) == 6, 'site-cards-6')
for p in cards:
    t = p.read_text(encoding='utf-8')
    m = re.search(r'\*\*服务\*\*：([^\n]+)', t)
    check(bool(m) and ('无固定服务' in m.group(1) or '不新增柜台与服务' in m.group(1)), p.stem + '-service-clause')
have = {n['site'] for n in fx['npcs']} | {s['site'] for s in sg['signs']}
check(have == {r['key'] for r in inv['rumor_sites']}, 'all-44-sites-covered')
check(len(list((V / '04_人物/野外人物').glob('*.md'))) == len(fx['npcs']), 'card-count-matches')
card = (V / '11_管理/野外内容规则一致性审计.md').read_text(encoding='utf-8')
check('# 野外内容规则一致性审计' in card and '## 边界' in card and '不合口径：无' in card, 'card-structure')
for r in au['rows']:
    check(f"| {r['rule']} | {r['scope']} |" in card, 'row-rendered-' + r['rule'][:10])
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('RULE-AUDIT-S109:BEGIN' in plan and '[[野外内容规则一致性审计]]' in plan, 'plan-block-and-link')
check('RULE-AUDIT-S109:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/rule-audit-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S109 rule audit: recomputed rule rows from the field registries and site cards; structure and rules only, not runtime or literary quality',
              rows=len(au['rows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/rule-audit-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
