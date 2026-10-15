"""Validate the S152 registry-coverage classification against live sources."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'registry-coverage.json').read_text(encoding='utf-8'))
tools = {p.name: p.read_text(encoding='utf-8') for p in sorted((R / 'tools').glob('*.py'))}
val = {n: t for n, t in tools.items() if n.startswith('Validate-')}
writers = {n: t for n, t in tools.items() if n.startswith(('Write-', 'Record-', 'Probe-', 'Author-', 'Attach-')) or n == 'BrynnContinuation.py'}
pages = {str(p.relative_to(ROOT)).replace('\\', '/'): p.read_text(encoding='utf-8') for p in V.rglob('*.md')}
def stems(name):
    s = name[:-5]
    out = {s}
    for suf in ('-drama', '-feedback', '-s77', '-catalog', '-results', '-log', '-review', '-index', '-entries'):
        if s.endswith(suf):
            out.add(s[:-len(suf)])
    return {x for x in out if len(x) >= 4}
live = {}
for p in sorted(R.glob('*.json')):
    n = p.name
    if n.endswith(('-validation.json', '-note-hashes.json')):
        continue
    if n == 'registry-coverage.json':
        continue  # 元登记：本页自身，不参与分类
    if n in ('local-baseline.json', 'design-model.json'):
        live[n] = 'baseline'; continue
    if any(n in t for t in val.values()):
        live[n] = 'validator-direct'; continue
    if any(any(s in t for s in stems(n)) for t in val.values()):
        live[n] = 'validator-indirect'; continue
    if any(n in t for t in writers.values()):
        live[n] = 'tool-output'; continue
    if any(n in t for t in pages.values()):
        live[n] = 'cited-log'; continue
    live[n] = 'unclassified'
check(len(reg['rows']) == len(live), 'row-count-live')
for r in reg['rows']:
    check(live.get(r['file']) == r['cls'], 'class-' + r['file'])
    check(bool(r['evidence']) or r['cls'] == 'unclassified', 'evidence-' + r['file'])
check(reg['unclassified'] == [], 'no-unclassified')
check(sum(reg['classes'].values()) == len(reg['rows']), 'classes-sum')
check(reg['classes'].get('validator-direct', 0) >= 70, 'direct-majority')
card = (V / '11_管理/登记文件覆盖分类.md').read_text(encoding='utf-8')
stems_pages = {p.stem for p in V.rglob('*.md')}
for sec in ('## 规则', '## 未归类清单', '## 边界'):
    check(sec in card, 'section-' + sec)
check(f"（{len(reg['rows'])} 份" in card, 'card-count')
for k, v in reg['classes'].items():
    check(f"| `{k}` | {v} |" in card, 'card-class-' + k)
check('无。' in card, 'card-no-unclassified')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('REG-COVERAGE-S152:BEGIN' in plan and '[[登记文件覆盖分类]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems_pages, 'link-' + lm.group(1))
check('REG-COVERAGE-S152:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'registry-coverage-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S152 registry coverage: live reclassification of every research JSON, class and evidence per row, page counts, chain; classification only',
              registries=len(reg['rows']), classes=reg['classes'], checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'registry-coverage-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
