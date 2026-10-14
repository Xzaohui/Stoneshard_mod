"""Validate the S155 engine-key registry against a live GML scan."""
from pathlib import Path
import json, hashlib, re, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'engine-keys.json').read_text(encoding='utf-8'))
live = collections.defaultdict(set)
for p in sorted((ROOT / 'src/EmbersAndOaths/Codes').glob('*.gml')):
    for m in re.finditer(r'"([A-Za-z_][A-Za-z0-9_]*)"', p.read_text(encoding='utf-8')):
        if m.group(1).startswith('EAO_'):
            live[m.group(1)].add(p.name)
check(len(reg['keys']) == len(live), 'key-count-live')
for r in reg['keys']:
    check(r['key'] in live, 'key-live-' + r['key'])
    if r['key'] in live:
        check(r['files'] == sorted(live[r['key']]), 'files-' + r['key'])
    check(r['cls'] != 'unclassified', 'classified-' + r['key'])
check(reg['unclassified'] == [], 'no-unclassified')
mapped={r['key'] for r in reg['keys'] if r['mapped_to_registry']}
check(mapped == {r['key'] for r in reg['keys'] if r['cls'].startswith('pilot-N2')}, 'mapped-exactly-pilot-keys')
check(reg['classes'].get('test-teleport', 0) >= 15 and reg['classes'].get('sample-N1', 0) >= 5 and reg['classes'].get('pilot-N2', 0) >= 4, 'class-shape')
card = (V / '11_管理/引擎键名前缀与遗留键登记.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 口径', '## 已实现的 `EAO_` 键（扫描 `src/EmbersAndOaths/Codes/*.gml`）', '## 与 N1 小样的冲突（须在实现时决定）', '## 边界'):
    check(sec in card, 'section-' + sec)
check('引擎键名 ＝ `EAO_` ＋ 登记键名' in card, 'card-rule')
check(f"共 **{len(live)}** 个" in card, 'card-count')
for r in reg['keys']:
    check('`' + r['key'] + '`' in card, 'card-key-' + r['key'])
check('EAO_N1_stage' in card and 'resolve_N1' in card and '二选一' in card, 'card-n1-conflict')
pilot = (V / '11_管理/试点实现批次N2.md').read_text(encoding='utf-8')
check('[[引擎键名前缀与遗留键登记]]' in pilot and 'EAO_' in pilot, 'pilot-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('ENGINE-KEYS-S155:BEGIN' in plan and '[[引擎键名前缀与遗留键登记]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('ENGINE-KEYS-S155:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'engine-keys-note-hashes.json').read_text(encoding='utf-8'))
check(set(h) >= {'design/11_管理/引擎键名前缀与遗留键登记.md', 'design/11_管理/特殊地点与野外NPC对白扩展计划.md'}, 'own-manifest-entries')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S155 engine keys: live GML scan vs registry, classification, prefix rule and N1 conflict on the page, pilot link, chain; read-only',
              keys=len(live), classes=reg['classes'], checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'engine-keys-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
