"""Validate the S177 narrative-depth audit against the live registries."""
from pathlib import Path
import json, hashlib, collections, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'narrative-depth-audit.json').read_text(encoding='utf-8'))
flows = json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows']
matrix = (V / '09_系统逻辑/叙事交叉影响矩阵.md').read_text(encoding='utf-8')
edges = re.findall(r'^## (X\d\d)\s+([A-Za-z0-9\-]+) → ([A-Za-z0-9\-]+)$', matrix, re.M)
out_deg = collections.Counter(a for _, a, _ in edges)
in_deg = collections.Counter(b for _, _, b in edges)
live = {}
for f in flows:
    when = collections.Counter(n.get('when') for n in f['nodes'])
    live[f['id']] = dict(nodes=len(f['nodes']),
                         conditioned=sum(1 for n in f['nodes'] if n.get('when') != 'any'),
                         early=when.get('order_early', 0), late=when.get('order_late', 0),
                         absent=when.get('npc_absent', 0), x_in=in_deg.get(f['id'], 0), x_out=out_deg.get(f['id'], 0))
check(len(reg['metrics']) == len(live), 'rows-live')
for r in reg['metrics']:
    lv = live[r['id']]
    for k in ('nodes', 'conditioned', 'early', 'late', 'absent', 'x_in', 'x_out'):
        check(r[k] == lv[k], f"{r['id']}-{k}")
check(sum(1 for r in reg['metrics'] if r['conditioned'] < 3) == 0, 'min-conditioned')
gaps = reg['gaps']
check(gaps['no_timing'] == [r['id'] for r in reg['metrics'] if not r['early'] and not r['late']], 'gap-timing-live')
check(gaps['no_absence'] == [r['id'] for r in reg['metrics'] if not r['absent']], 'gap-absence-live')
check(gaps['no_inbound'] == [r['id'] for r in reg['metrics'] if r['x_in'] == 0], 'gap-inbound-live')
check(gaps['no_outbound'] == [r['id'] for r in reg['metrics'] if r['x_out'] == 0], 'gap-outbound-live')
check(gaps['thin_nodes'] == [r['id'] for r in reg['metrics'] if r['nodes'] <= 4], 'gap-thin-live')
for name, s in reg['families'].items():
    rs = [r for r in reg['metrics'] if r['family'] == name]
    check(s['scripts'] == len(rs), 'fam-count-' + name)
    check(s['with_early'] == sum(1 for r in rs if r['early']), 'fam-early-' + name)
    check(s['with_absent'] == sum(1 for r in rs if r['absent']), 'fam-absent-' + name)
check(len(reg['proposal']) == 3, 'three-proposals')
card = (V / '11_管理/网状叙事深度审计.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 家族分布（中位数／计数）', '## 缺口清单（现场重算）', '## 对照经验（BG3／DOS）', '## 优化提案（下一步执行）', '## 边界'):
    check(sec in card, 'section-' + sec)
for name, s in reg['families'].items():
    check(f"| {name} | {s['scripts']} |" in card, 'card-fam-' + name)
check(f"{len(gaps['no_timing'])} 篇" in card and f"{len(gaps['no_inbound'])} 篇" in card, 'card-gap-counts')
check('不评判文学质量' in card, 'card-limit')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('NARRATIVE-DEPTH-S177:BEGIN' in plan and '[[网状叙事深度审计]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('NARRATIVE-DEPTH-S177:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'narrative-depth-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S177 narrative-depth audit: per-script metrics and gaps recomputed, family aggregates, page and chain; read-only',
              flows=len(reg['metrics']), gaps={k: len(v) for k, v in gaps.items()},
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'narrative-depth-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
