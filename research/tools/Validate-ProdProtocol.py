"""Validate the S108 production protocol: sections, prohibitions and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
pp = read('research/production-protocol.json')
stems = {p.stem for p in V.rglob('*.md')}
check(len(pp['sections']) == 4, 'section-count-4')
check([s['id'] for s in pp['sections']] == ['economy', 'maps', 'runtime', 'triggers'], 'section-ids')
card = (V / '11_管理/特殊地点阶段制作与校准规程.md').read_text(encoding='utf-8')
check('# 特殊地点阶段制作与校准规程' in card and '## 通用要求' in card and '## 边界' in card, 'card-structure')
for s in pp['sections']:
    check(len(s['fields']) >= 4, s['id'] + '-fields')
    for k in ('target', 'sample', 'pass_cond', 'forbid'):
        check(bool(s[k].strip()), s['id'] + '-' + k)
    check(f"## {s['title']}" in card, s['id'] + '-rendered')
    check(s['pass_cond'] in card and s['forbid'] in card, s['id'] + '-conds-rendered')
    for f in s['fields']:
        check(f in card, s['id'] + '-field-rendered-' + f[:12])
check('未测量的内容不得在库内补成具体值' in card and '不含任何实测数字' in card, 'no-unmeasured-values-clause')
check('未在游戏内跑过不得标记“已验证”' in card, 'runtime-clause')
check('不得用自制传送替代原生转场' in card, 'no-teleport-clause')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PROD-PROTOCOL-S108:BEGIN' in plan and '[[特殊地点阶段制作与校准规程]]' in plan, 'plan-block-and-link')
check('PROD-PROTOCOL-S108:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/prod-protocol-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S108 production protocol: four sections with targets, evidence fields, sampling, pass conditions and prohibitions; no measured values; rendering and chain',
              sections=len(pp['sections']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/prod-protocol-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
