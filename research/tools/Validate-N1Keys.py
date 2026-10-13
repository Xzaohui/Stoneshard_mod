"""Validate the S161 N1 key evidence page against a live GML scan."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
facts = json.loads((R / 'n1-stage-evidence.json').read_text(encoding='utf-8'))
live = []
for p in sorted((ROOT / 'src/EmbersAndOaths/Codes').glob('*.gml')):
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        for m in re.finditer(r'"(EAO_N1_[A-Za-z0-9_]+)"', line):
            kind = 'write' if 'ds_map_set' in line else ('read' if ('ds_map_find_value' in line or 'ds_map_exists' in line) else 'reference')
            live.append(dict(key=m.group(1), file=p.name, line=i, kind=kind, code=line.strip()[:120]))
check(len(facts['usages']) == len(live), 'usage-count-live')
for a, b in zip(facts['usages'], live):
    check(a == b, 'usage-' + a['key'] + '-' + str(a['line']))
check(facts['stage_has_writer'] is False, 'stage-unwritten')
check('EAO_N1_stage' not in facts['written_keys'], 'stage-not-in-writes')
check('EAO_N1_stage' in facts['read_keys'], 'stage-in-reads')
check(set(facts['written_keys']) == {r['key'] for r in live if r['kind'] == 'write'}, 'writes-live')
check(set(facts['read_keys']) == {r['key'] for r in live if r['kind'] == 'read'}, 'reads-live')
sk = {k['key'] for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys'] if k['script'] == 'N1'}
check({'encountered_N1', 'resolve_N1'} <= sk, 'registry-n1-keys')
card = (V / '11_管理/N1小样键语义与迁移建议.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 用法清单（现场扫描）', '## 关键观察（静态）', '## 迁移建议（供 OI-03 决策）', '## 边界'):
    check(sec in card, 'section-' + sec)
for r in facts['usages']:
    check('`' + r['file'] + '`' in card and f"| {r['line']} |" in card, 'card-usage-' + r['file'] + str(r['line']))
check('没有任何写入点' in card, 'card-no-writer')
check('encountered_N1' in card and 'resolve_N1' in card and '读取垫片' in card, 'card-proposal')
check('静态' in card and '未运行游戏' in card, 'card-static-limit')
eng = (V / '11_管理/引擎键名前缀与遗留键登记.md').read_text(encoding='utf-8')
check('[[N1小样键语义与迁移建议]]' in eng, 'engine-page-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('N1-KEYS-S161:BEGIN' in plan and '[[N1小样键语义与迁移建议]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('N1-KEYS-S161:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'n1-keys-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S161 N1 keys: live GML scan vs evidence registry, stage-unwritten claim, proposal wording, links and chain; read-only static analysis',
              usages=len(live), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'n1-keys-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
