"""Validate the S154 pilot acceptance scenarios against the live key registry."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'pilot-batch-scenarios-n2.json').read_text(encoding='utf-8'))
batch = json.loads((R / 'pilot-batch-n2.json').read_text(encoding='utf-8'))
sk = {k['key']: k for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys'] if k['script'] == 'N2'}
check(len(reg['scenarios']) == 6, 'six-scenarios')
ids = [s['id'] for s in reg['scenarios']]
check(len(set(ids)) == 6 and all(i.startswith('N2-T') for i in ids), 'scenario-ids')
covered = set()
for s in reg['scenarios']:
    check(bool(s['steps']) and bool(s['invariants']), 'fields-' + s['id'])
    for k, v in s['writes']:
        spec = sk.get(k)
        check(spec is not None, 'key-registered-' + s['id'] + '-' + k)
        if spec:
            check(v in spec['values'], 'value-in-set-' + s['id'] + '-' + k)
        covered.add(k)
check(covered == set(sk), 'all-keys-covered')
check(len(reg['write_matrix']) == sum(len(s['writes']) for s in reg['scenarios']), 'matrix-size')
for r in reg['write_matrix']:
    check(sk.get(r['key'], {}).get('kind') == r['kind'], 'kind-' + r['scenario'] + '-' + r['key'])
card = (V / '11_管理/试点批次验收场景N2.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 场景与期望写入', '## 写入矩阵（对照取值集合）', '## 运行记录要求', '## 边界'):
    check(sec in card, 'section-' + sec)
for s in reg['scenarios']:
    check(f"| {s['id']} | {s['name']} |" in card, 'card-row-' + s['id'])
for k in sk:
    check('`' + k + '`' in card, 'card-key-' + k)
check('同一 SHA' in card or '同一 **SHA**' in card, 'card-sha-rule')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PILOT-N2-SCEN-S154:BEGIN' in plan and '[[试点批次验收场景N2]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PILOT-N2-SCEN-S154:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'pilot-scenarios-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S154 pilot scenarios: six scenarios, every expected write checked against live key value sets, all N2 keys covered, page and chain; planning only',
              scenarios=len(reg['scenarios']), keys=len(sk), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'pilot-scenarios-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
