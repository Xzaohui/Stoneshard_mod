"""Validate the S171 hook mapping against the stub registry and the sample code."""
from pathlib import Path
import json, hashlib, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = json.loads((R / 'hook-mapping.json').read_text(encoding='utf-8'))
stubs = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
counts = collections.Counter(s['trigger'] for s in stubs)
cooldowns = collections.Counter(s['cooldown'] for s in stubs)
check(reg['trigger_counts'] == dict(counts), 'trigger-counts-live')
check(reg['cooldown_counts'] == dict(cooldowns), 'cooldown-counts-live')
check(set(reg['hooks']) == set(counts), 'all-triggers-mapped')
for k, h in reg['hooks'].items():
    check(bool(h['pattern']) and bool(h['rule']), 'fields-' + k)
    check(len(h['evidence']) >= 1, 'evidence-' + k)
    for e in h['evidence']:
        p = ROOT / 'src/EmbersAndOaths/Codes' / e['file']
        check(p.exists(), 'evidence-file-' + k)
        if p.exists():
            lines = p.read_text(encoding='utf-8').splitlines()
            check(e['line'] <= len(lines), 'evidence-line-range-' + k)
            if e['line'] <= len(lines):
                check(e['code'][:24] in lines[e['line'] - 1], 'evidence-line-content-' + k)
card = (V / '11_管理/触发器接线点映射.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 触发 → 钩子', '## 原生钩子清单（小样证据）', '## 边界'):
    check(sec in card, 'section-' + sec)
for k, c in counts.items():
    check(f"| `{k}` | {c} |" in card, 'card-row-' + k)
check(f"**{len(stubs)}** 个桩" in card, 'card-stub-total')
check('不代表新内容已接线' in card, 'card-limit')
sp = (V / '09_系统逻辑/事件桩映射总表.md').read_text(encoding='utf-8')
check('HOOK-MAP-S171:BEGIN' in sp and '[[触发器接线点映射]]' in sp, 'stubs-page-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('HOOK-MAP-S171:BEGIN' in plan and '[[触发器接线点映射]]' in plan, 'plan-block')
for lm in __import__('re').finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('HOOK-MAP-S171:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'hook-map-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S171 hook mapping: trigger counts recomputed, every trigger mapped with live evidence lines, page and chain; read-only',
              triggers=len(counts), stubs=len(stubs), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'hook-map-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
