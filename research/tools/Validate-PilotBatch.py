"""Validate the S153 pilot-batch plan against the live registries."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
batch = json.loads((R / 'pilot-batch-n2.json').read_text(encoding='utf-8'))
st = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
sk = json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']
cf = json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows']
n2st = [s for s in st if s['script'] == 'N2']
n2k = [k for k in sk if k['script'] == 'N2']
n2f = [f for f in cf if f['id'] == 'N2'][0]
script = (V / '05_主线/台本/台本_N2_灰堤没有墓碑.md').read_text(encoding='utf-8')
methods = sorted({m for m in re.findall(r'\b(N2-R-[A-Za-z0-9\-]+)', script) if not m.endswith(('-L01', '-L02'))})
edges = sorted({'X' + x for x in re.findall(r'\bX(\d\d)\b', script)})
check([s['event'] for s in batch['stubs']] == [s['event'] for s in n2st], 'stub-ids-live')
check([k['key'] for k in batch['keys']] == [k['key'] for k in n2k], 'key-names-live')
check(batch['flow_nodes'] == [n['id'] for n in n2f['nodes']], 'flow-nodes-live')
check(batch['methods'] == methods, 'methods-live')
check(batch['x_edges'] == edges, 'edges-live')
check(len(batch['gml_files']) == len(n2st), 'gml-count')
check(all(f.endswith('.gml') and f.startswith('n2_') for f in batch['gml_files']), 'gml-naming')
for s in batch['stubs']:
    check(s['trigger'].startswith('on_'), 'trigger-' + s['event'])
    check(s['cooldown'] in ('once', 'repeatable'), 'cooldown-' + s['event'])
card = (V / '11_管理/试点实现批次N2.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 输入（现场提取）', '## 建议的落地顺序', '## 建议新增文件（沿用既有命名）', '## 前置与边界'):
    check(sec in card, 'section-' + sec)
for s in n2st:
    check('`' + s['event'] + '`' in card, 'card-stub-' + s['event'])
for k in n2k:
    check('`' + k['key'] + '`' in card, 'card-key-' + k['key'])
for m in methods:
    check('`' + m + '`' in card, 'card-method-' + m)
for f in batch['gml_files']:
    check('`src/EmbersAndOaths/Codes/' + f + '`' in card, 'card-file-' + f)
check(re.search(r'不含\*{0,2}实现代码', card) and '不分配事件号' in card, 'card-scope-limits')
plan = (V / '11_管理/特殊地点与野外NPC对口扩展计划.md').read_text(encoding='utf-8') if (V / '11_管理/特殊地点与野外NPC对口扩展计划.md').exists() else (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PILOT-N2-S153:BEGIN' in plan and '[[试点实现批次N2]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PILOT-N2-S153:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'pilot-batch-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S153 pilot batch N2: stubs/keys/flow/methods/edges recomputed from registries, GML naming, page rows and chain; planning only, nothing implemented',
              stubs=len(n2st), keys=len(n2k), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'pilot-batch-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
