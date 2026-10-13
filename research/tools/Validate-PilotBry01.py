"""Validate the S156 city pilot batch against the live registries."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
QID = 'CS-BRY-01'
batch = json.loads((R / 'pilot-batch-cs-bry-01.json').read_text(encoding='utf-8'))
st = [s for s in json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs'] if s['script'] == QID]
sk = {k['key']: k for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys'] if k['script'] == QID}
cf = [f for f in json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows'] if f['id'] == QID][0]
script = next(V.rglob('台本_CS-BRY-01_*.md')).read_text(encoding='utf-8')
sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', script, re.S)
methods = [f"{m.group(1)}：{m.group(2).strip()}" for m in re.finditer(r'^###\s+([^\s：:]{1,24})[：:]\s*(.+?)\s*$', sec.group(1) if sec else '', re.M)]
check([s['event'] for s in batch['stubs']] == [s['event'] for s in st], 'stubs-live')
check([k['key'] for k in batch['keys']] == [k['key'] for k in sk.values()], 'keys-live')
check(batch['flow_nodes'] == [n['id'] for n in cf['nodes']], 'nodes-live')
check(batch['methods'] == methods, 'methods-live')
check(len(batch['gml_files']) == len(st), 'gml-count')
check(all(f.startswith('cs_bry_01_') and f.endswith('.gml') for f in batch['gml_files']), 'gml-naming')
check(len(batch['scenarios']) == 7, 'seven-scenarios')
covered = set()
for s in batch['scenarios']:
    check(bool(s['steps']) and bool(s['invariants']), 'fields-' + s['id'])
    for k, v in s['writes']:
        spec = sk.get(k)
        check(spec is not None, 'key-' + s['id'] + '-' + k)
        if spec: check(v in spec['values'], 'value-' + s['id'] + '-' + k)
        covered.add(k)
check({'resolve_CS_BRY_01', 'encountered_CS_BRY_01', 'presence_CS_BRY_01', 'order_CS_BRY_01'} <= covered, 'core-keys-covered')
check(len(batch['write_matrix']) == sum(len(s['writes']) for s in batch['scenarios']), 'matrix-size')
sysb = batch['systems']
check(sysb['service']['id'] == 'SVC-BRY' and sysb['service']['operator'], 'service-entry')
check(sysb['town_gossip_lines'] >= 1 and sysb['band_gossip_lines'] >= 1, 'gossip-counts')
card = (V / '11_管理/试点实现批次CS-BRY-01.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for s_ in ('## 输入（现场提取）', '## 系统层接线（与本案的关系）', '## 落地顺序', '## 验收场景', '## 建议新增文件（沿用既有命名）', '## 边界'):
    check(s_ in card, 'section-' + s_)
for s in batch['scenarios']:
    check(f"| {s['id']} | {s['name']} |" in card, 'card-scen-' + s['id'])
for m in methods:
    check(m in card, 'card-method-' + m[:12])
for f in batch['gml_files']:
    check('`src/EmbersAndOaths/Codes/' + f + '`' in card, 'card-file-' + f)
check('不含实现代码' in card or '不含**实现代码' in card, 'card-scope')
check('[[引擎键名前缀与遗留键登记]]' in card, 'card-key-rule-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PILOT-BRY01-S156:BEGIN' in plan and '[[试点实现批次CS-BRY-01]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PILOT-BRY01-S156:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'pilot-bry01-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S156 city pilot CS-BRY-01: stubs/keys/nodes/methods recomputed, scenario writes checked against value sets, systems wiring, page and chain; planning only',
              stubs=len(st), keys=len(sk), scenarios=len(batch['scenarios']), checks_passed=len(checks),
              errors=errors, passed=not errors, runtimeVerified=False)
(R / 'pilot-bry01-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
