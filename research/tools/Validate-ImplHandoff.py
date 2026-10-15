"""Validate the S122 implementation hand-off index and its live counts."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ih = read('research/impl-handoff.json')
check(len(ih['artifacts']) == 18, 'artifact-count-18')
check(len(ih['steps']) == 6, 'step-count-6')
check(len(ih['gates']) >= 5, 'gates')
check(len(ih['open_items']) >= 6, 'open-items')
for a in ih['artifacts']:
    check((ROOT / a['path']).exists(), 'artifact-exists-' + a['path'])
    check(bool(a['what']) and bool(a['entry']), 'artifact-meta-' + a['path'])
for s in ih['steps']:
    check(bool(s['name']) and bool(s['how']) and bool(s['accept']), 'step-fields-' + s['name'])
check(not re.search(r'\d+\s*(?:金币|银币|克朗)', json.dumps(ih, ensure_ascii=False)), 'no-currency-numbers')
# live counts must match validation reports
for k, v in ih['validation'].items():
    live = read(f'research/{k}-validation.json')['checks_passed']
    check(v == live, f'live-count-{k}')
card = (V / '11_管理/实现交接总表.md').read_text(encoding='utf-8')
check('# 实现交接总表' in card and '## 输入清单' in card and '## 实现顺序与验收' in card and '## 尚未确定' in card and '## 边界' in card, 'card-structure')
for a in ih['artifacts']:
    check(f"`{a['path']}`" in card and a['entry'] in card, 'card-artifact-' + a['path'])
for s in ih['steps']:
    check(f"| {s['name']} |" in card, 'card-step-' + s['name'])
for k, v in ih['validation'].items():
    check(f"| `{k}` | {v} |" in card, 'card-count-' + k)
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('IMPL-HANDOFF-S122:BEGIN' in plan and '[[实现交接总表]]' in plan, 'plan-block-and-link')
check('IMPL-HANDOFF-S122:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/impl-handoff-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S122 hand-off index: artifact existence, step fields, live counts match validation reports, rendering and chain; not implementation or runtime',
              artifacts=len(ih['artifacts']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/impl-handoff-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
