"""Validate the S133 open-items register and the overview navigation block."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
oi = read('research/open-items.json')
stems = {p.stem for p in V.rglob('*.md')}
check(len(oi['items']) == 14, 'items-14')
ids = [x['id'] for x in oi['items']]
check(len(set(ids)) == 14, 'ids-unique')
for x in oi['items']:
    for k in ('area', 'what', 'owner', 'prereq', 'status', 'evidence'):
        check(bool(str(x[k]).strip()), x['id'] + '-' + k)
    check(x['status'] in ('open', 'blocked', 'policy'), x['id'] + '-status')
    for m in re.finditer(r'\[\[([^\]]+)\]\]', x['what'] + ' ' + x['evidence']):
        check(m.group(1) in stems, x['id'] + '-link-' + m.group(1))
card = (V / '11_管理/待办与已知缺口登记.md').read_text(encoding='utf-8')
check('# 待办与已知缺口登记' in card and '## 口径' in card and '## 边界' in card, 'card-structure')
for x in oi['items']:
    check(f"| {x['id']} | {x['area']} |" in card and x['status'] in card, 'card-row-' + x['id'])
ov = (V / '00_导航/设计总览.md').read_text(encoding='utf-8')
check('OPEN-ITEMS-S133:BEGIN' in ov and '[[待办与已知缺口登记]]' in ov and '[[叙事内容清单]]' in ov and '[[实现交接总表]]' in ov and '[[试玩路线与检查单]]' in ov, 'overview-nav-block')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('OPEN-ITEMS-S133:BEGIN' in plan and '[[待办与已知缺口登记]]' in plan, 'plan-block-and-link')
check('OPEN-ITEMS-S133:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/open-items-note-hashes.json')
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S133 open items: register fields, statuses, links, overview navigation, rendering and chain; register only, not runtime',
              items=len(oi['items']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/open-items-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
