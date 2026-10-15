"""Validate the S163 event-number allocation against the stub registry."""
from pathlib import Path
import json, hashlib, re, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
def family(script):
    if script.startswith('DT'): return 'DT'
    if script.startswith('D'): return 'D'
    if script.startswith('N'): return 'N'
    if script.startswith('SQ'): return 'SQ'
    if script.startswith('CM'): return 'CM'
    if script.startswith('CS'): return 'CS'
    if script.startswith('FX'): return 'FX'
    return 'other'
reg = json.loads((R / 'event-number-scheme.json').read_text(encoding='utf-8'))
stubs = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
by_script = collections.OrderedDict()
for s in stubs:
    by_script.setdefault(s['script'], []).append(s['event'])
alloc = []
for fam, base in reg['bases'].items():
    offset = 0
    for sc in sorted(k for k in by_script if family(k) == fam):
        n = len(by_script[sc]); block = ((n + 63) // 64) * 64
        for i, ev in enumerate(by_script[sc]):
            alloc.append(dict(event=ev, script=sc, number=base + offset + i))
        offset += block
check(len(reg['allocations']) == len(alloc) == len(stubs), 'allocation-count')
check(reg['allocations'] == alloc, 'allocation-deterministic')
nums = [a['number'] for a in reg['allocations']]
check(len(set(nums)) == len(nums), 'numbers-unique')
byfam = collections.defaultdict(list)
for a in reg['allocations']:
    byfam[family(a['script'])].append(a['number'])
for fam, ns in byfam.items():
    base = reg['bases'][fam]
    check(min(ns) >= base and max(ns) < base + 10000, 'range-' + fam)
card = (V / '11_管理/事件号分配方案.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 家族基址与范围', '## 分配样例（每家族前三）', '## 边界'):
    check(sec in card, 'section-' + sec)
for fam in byfam:
    lo, hi = min(byfam[fam]), max(byfam[fam])
    check(f"| {lo}–{hi} |" in card, 'card-range-' + fam)
check('一桩一号、不复用' in card, 'card-no-reuse')
check(f"**{len(reg['allocations'])}** 个桩" in card, 'card-total')
check('原生事件号空间未读取' in card, 'card-limit')
stubs_page = (V / '09_系统逻辑/事件桩映射总表.md').read_text(encoding='utf-8')
check('EVT-NUM-S163:BEGIN' in stubs_page and '[[事件号分配方案]]' in stubs_page, 'stubs-page-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('EVT-NUM-S163:BEGIN' in plan and '[[事件号分配方案]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('EVT-NUM-S163:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'evt-num-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S163 event numbers: deterministic allocation recomputed, uniqueness and family ranges, page rows, links and chain; planning only',
              total=len(reg['allocations']), families=len(byfam), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'evt-num-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
