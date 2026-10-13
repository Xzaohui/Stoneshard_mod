"""Validate the S158 pilot index against the three batch registries."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
idx = json.loads((R / 'pilot-batches.json').read_text(encoding='utf-8'))
n2 = json.loads((R / 'pilot-batch-n2.json').read_text(encoding='utf-8'))
sc2 = json.loads((R / 'pilot-batch-scenarios-n2.json').read_text(encoding='utf-8'))
bry = json.loads((R / 'pilot-batch-cs-bry-01.json').read_text(encoding='utf-8'))
fx = json.loads((R / 'pilot-batch-fx.json').read_text(encoding='utf-8'))
expect = {
    'P1': dict(stubs=len(n2['stubs']), keys=len(n2['keys']), nodes=len(n2['flow_nodes']), methods=len(n2['methods']), scenarios=len(sc2['scenarios'])),
    'P2': dict(stubs=len(bry['stubs']), keys=len(bry['keys']), nodes=len(bry['flow_nodes']), methods=len(bry['methods']), scenarios=len(bry['scenarios'])),
    'P3': dict(stubs=0, keys=0, nodes=len(fx['flow']['nodes']), methods=0, scenarios=len(fx['scenarios'])),
}
for r in idx['batches']:
    e = expect[r['id']]
    for k, v in e.items():
        check(r[k] == v, f"{r['id']}-{k}")
for k in ('stubs', 'keys', 'nodes', 'methods', 'scenarios'):
    check(idx['totals'][k] == sum(r[k] for r in idx['batches']), 'total-' + k)
card = (V / '11_管理/试点批次总表.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 建议顺序', '## 共享规则（三批一致）', '## 边界'):
    check(sec in card, 'section-' + sec)
for r in idx['batches']:
    check(f"| {r['id']} | {r['layer']} |" in card, 'card-row-' + r['id'])
    check(r['entry'] in card, 'card-entry-' + r['id'])
for k, v in idx['totals'].items():
    check(f"**{v}**" in card, 'card-total-' + k)
for term in ('EAO_', 'OI-02', 'OI-03', '同一 SHA', '不回滚历史', '不含实现代码'):
    check(term in card, 'card-rule-' + term)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PILOT-INDEX-S158:BEGIN' in plan and '[[试点批次总表]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PILOT-INDEX-S158:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'pilot-index-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S158 pilot index: per-batch counts and totals recomputed from the three registries, shared rules present, page and chain; planning only',
              batches=len(idx['batches']), totals=idx['totals'], checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'pilot-index-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
