"""Validate the S173 ask-traceability page against live deliverables."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'ask-traceability.json').read_text(encoding='utf-8'))
stems = {p.stem for p in V.rglob('*.md')}
tools = {p.name for p in (R / 'tools').glob('*.py')}
check(len(reg['rows']) == 12, 'twelve-rows')
for r in reg['rows']:
    check(bool(r['ask']) and bool(r['guard']) and bool(r['note']), 'fields-' + r['ask'])
    check(r['status'] in ('done', 'deferred'), 'status-' + r['ask'])
    check(len(r['deliver']) >= 1, 'deliverables-' + r['ask'])
    for d in r['deliver']:
        m = re.fullmatch(r'\[\[([^\]]+)\]\]', d)
        check(m is not None, 'deliver-link-form-' + r['ask'])
        if m:
            check(m.group(1) in stems, 'deliver-exists-' + m.group(1))
    for t in re.findall(r'[A-Z][A-Za-z\-]+\.py', r['guard']):
        check(t in tools, 'guard-tool-' + t)
    if '质量守卫' in r['guard'] or 'Test-DesignVault' in r['guard']:
        pass
card = (V / '11_管理/用户要求与交付对照.md').read_text(encoding='utf-8')
for sec in ('## 口径', '## 边界'):
    check(sec in card, 'section-' + sec)
for r in reg['rows']:
    check(r['ask'] in card and r['guard'] in card, 'card-row-' + r['ask'])
check('不表示游戏内已实现或已运行' in card, 'card-scope-limit')
check('[[待办与已知缺口登记]]' in card, 'card-points-at-open-items')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('ASK-TRACE-S173:BEGIN' in plan and '[[用户要求与交付对照]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('ASK-TRACE-S173:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'ask-trace-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S173 ask traceability: twelve clauses with existing deliverable pages, guard tools that exist, scope limits, links and chain; documentation only',
              rows=len(reg['rows']), deliverable_pages=sum(len(r['deliver']) for r in reg['rows']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'ask-trace-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
