"""Validate the S128 playtest walkthrough: segments, entries, rendering, chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
pt = read('research/playtest-walkthrough.json')
stems = {p.stem for p in V.rglob('*.md')}
check(len(pt['segments']) == 11, 'segment-count-11')
ids = [s['id'] for s in pt['segments']]
check(len(set(ids)) == 11, 'segment-ids-unique')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json'); sg = read('research/field-signs.json')
known_scripts = {q['id'] for q in model['quests']} | {q['id'] for q in cont['quests']} | {x['id'] for n in ['story-main.json','story-side.json','story-main-late.json','story-daily.json','story-dungeon.json'] for x in read('research/' + n)}
known_people = {x['id'] for x in fx['npcs']}
for s in pt['segments']:
    check(len(s['steps']) >= 3 and len(s['observe']) >= 3 and len(s['record']) >= 3, s['id'] + '-sections')
    for e in s['entry']:
        check(e in stems, s['id'] + '-entry-' + e)
    blob = json.dumps(s, ensure_ascii=False)
    check(not re.search(r'\d+\s*(?:金币|银币|克朗)', blob), s['id'] + '-no-currency')
    for m in re.finditer(r'(?:CS|CM|DT|SQ)-[A-Z0-9-]+|D\d{2}|N\d{1,2}', blob):
        tid = m.group(0)
        check(tid in known_scripts, s['id'] + '-script-' + tid)
    for m in re.finditer(r'FX-[A-Z0-9]+', blob):
        check(m.group(0) in known_people, s['id'] + '-person-' + m.group(0))
    for m in re.finditer(r'DOC-[A-Z]+', blob):
        check(any(d['id'] == m.group(0) for d in fd['docs']), s['id'] + '-doc-' + m.group(0))
    for m in re.finditer(r'SGN-[A-Z0-9]+', blob):
        check(any(x['id'] == m.group(0) for x in sg['signs']), s['id'] + '-sign-' + m.group(0))
card = (V / '11_管理/试玩路线与检查单.md').read_text(encoding='utf-8')
check('# 试玩路线与检查单' in card and '## 使用口径' in card, 'card-structure')
for s in pt['segments']:
    check(f"## {s['id']} {s['name']}" in card, s['id'] + '-rendered')
    for x in s['steps'] + s['observe'] + s['record']:
        check(x in card, s['id'] + '-item-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PLAYTEST-S128:BEGIN' in plan and '[[试玩路线与检查单]]' in plan, 'plan-block-and-link')
check('PLAYTEST-S128:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/playtest-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S128 playtest walkthrough: segment structure, entry and id resolution, rendering and chain; guide only, not runtime results',
              segments=len(pt['segments']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/playtest-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
