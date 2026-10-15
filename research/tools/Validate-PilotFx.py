"""Validate the S157 field-layer pilot batch against the live registries."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
batch = json.loads((R / 'pilot-batch-fx.json').read_text(encoding='utf-8'))
fx = json.loads((R / 'field-npc-dialogue.json').read_text(encoding='utf-8'))['npcs']
npc = next(n for n in fx if n['id'] == batch['npc']['id'])
docs = json.loads((R / 'field-docs.json').read_text(encoding='utf-8'))['docs']
signs = json.loads((R / 'field-signs.json').read_text(encoding='utf-8'))['signs']
pools = {n: len(json.loads((R / f'{n}.json').read_text(encoding='utf-8'))['lines'])
         for n in ('ambient-gossip', 'town-gossip', 'band-gossip')}
check(batch['npc']['greetings'] == len(npc['greetings']), 'greetings-live')
check(batch['npc']['chats'] == len(npc['chats']), 'chats-live')
check(batch['npc']['site_lines'] == len(npc['site_lines']), 'site-lines-live')
check(batch['npc']['visits']['proxy'] == len(npc['visits']['proxy']), 'proxy-live')
check(batch['npc']['visits']['before'] == len(npc['visits']['before']), 'before-live')
check(batch['pools'] == pools, 'pools-live')
check(batch['doc']['id'] == docs[0]['id'], 'doc-live')
check(batch['sign']['id'] == signs[0]['id'], 'sign-live')
check(len(batch['scenarios']) == 5, 'five-scenarios')
for s in batch['scenarios']:
    check(bool(s['invariants']), 'invariants-' + s['id'])
card = (V / '11_管理/试点实现批次FX野外层.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 输入（现场提取）', '## 落地顺序', '## 验收场景', '## 与另外两批的分工', '## 边界'):
    check(sec in card, 'section-' + sec)
check(batch['npc']['id'] in card and str(pools['ambient-gossip']) in card and str(pools['town-gossip']) in card, 'card-numbers')
for s in batch['scenarios']:
    check(f"| {s['id']} | {s['name']} |" in card, 'card-scen-' + s['id'])
check('不含实现代码' in card or '不含**实现代码' in card, 'card-scope')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PILOT-FX-S157:BEGIN' in plan and '[[试点实现批次FX野外层]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PILOT-FX-S157:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'pilot-fx-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S157 field pilot: NPC line counts, visit slots, pool counts, doc/sign ids recomputed, five scenarios, page and chain; planning only',
              npc=batch['npc']['id'], pools=pools, checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'pilot-fx-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
