"""Validate the S146 preservation-baseline registry against live snapshots and sources."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
FULL = re.compile(r"backups/[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-.]+)*\.(?:json|ini)")
reg = read('research/preservation-baselines.json')
registered = {e['snapshot'] for e in reg['entries']}
live_refs = {}
for p in sorted((ROOT / 'research/tools').glob('*.py')):
    for m in FULL.finditer(p.read_text(encoding='utf-8')):
        live_refs.setdefault(m.group(0), set()).add(p.name)
check(registered == set(live_refs), 'references-registered')
for rel, tools in live_refs.items():
    e = next((x for x in reg['entries'] if x['snapshot'] == rel), None)
    check(e is not None, 'entry-' + rel)
    if e:
        check(e['used_by'] == sorted(tools), 'users-' + rel)
        check(bool(e['purpose']), 'purpose-' + rel)
base = [e for e in reg['entries'] if e['role'] == 'preservation-baseline']
check(len(base) == 11, 'eleven-baselines')
for e in base:
    f = ROOT / e['snapshot']
    check(f.exists(), 'exists-' + e['snapshot'])
    if f.exists():
        check(e['sha256'] == sha(f), 'sha-' + e['snapshot'])
        check(e['bytes'] == f.stat().st_size, 'size-' + e['snapshot'])
special = [e for e in reg['entries'] if e['role'] != 'preservation-baseline']
check(len(special) == 1, 'one-non-dependency')
card = (V / '11_管理/验证快照依赖登记.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 规则', '## 边界'):
    check(sec in card, 'section-' + sec)
for e in base:
    check(f"`{e['snapshot']}`" in card and e['sha256'][:16] in card, 'card-row-' + e['snapshot'])
check(f"{len(base)} 份快照" in card, 'card-count')
flow = (V / '11_管理/设计库生成与校验流程.md').read_text(encoding='utf-8')
check('BASELINE-REG-S146:BEGIN' in flow and '[[验证快照依赖登记]]' in flow, 'flow-entry')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('BASELINE-REG-S146:BEGIN' in plan and '[[验证快照依赖登记]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('BASELINE-REG-S146:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/baseline-reg-note-hashes.json')
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S146 baseline registry: every tool-referenced backups path registered, snapshot hashes recomputed read-only, page and chain; no snapshot modified',
              entries=len(reg['entries']), baselines=len(base), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(ROOT / 'research/baseline-reg-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
