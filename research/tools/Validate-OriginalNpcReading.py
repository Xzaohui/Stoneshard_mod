"""Validate the S93 field-NPC reading: slot coverage, examples, card and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
inv = read('research/original-dialogue-inventory.json')
rd = read('research/original-npc-reading.json')
CJK = re.compile(r'[\u4e00-\u9fff]')
rows = {}
for fam in ('greeting', 'chat'):
    for e in inv['families'][fam]['entries']:
        spk = e.get('speaker')
        if spk: rows.setdefault(spk, {'greeting': [], 'chat': []})[fam].append(e['index'])
slots = set(rows)
assigned = {}
for g in rd['groups']:
    for s in g['slots']:
        check(s not in assigned, s + '-assigned-once')
        assigned[s] = g['id']
check(set(assigned) == slots, 'all-slots-assigned')
check(rd['unassigned'] == [], 'no-unassigned')
check(rd['slots'] == len(slots) == 72, 'slot-count-72')
check(len(rd['groups']) == 17, 'group-count-17')
fam_index = {e['index'] for fam in ('greeting', 'chat') for e in inv['families'][fam]['entries']}
for g in rd['groups']:
    check(bool(g['summary']) and len(g['summary']) <= 400 and CJK.search(g['summary']), g['id'] + '-summary')
    check(len(g['patterns']) >= 3, g['id'] + '-patterns')
    for p in g['patterns']:
        check(len(p) <= 70 and CJK.search(p), g['id'] + '-pattern-length')
    check(len(g['examples']) >= 2, g['id'] + '-examples')
    own_idx = {i for s in g['slots'] for fam in ('greeting', 'chat') for i in rows.get(s, {}).get(fam, [])}
    for ex in g['examples']:
        check(ex['index'] in fam_index, g['id'] + '-example-index-exists')
        check(len(ex['zh']) <= 48 and CJK.search(ex['zh']), g['id'] + '-example-short-zh')
        if own_idx: check(ex['index'] in own_idx, g['id'] + '-example-belongs-to-group')
card = (V / '01_原作基线/野外NPC口吻与闲谈参照.md').read_text(encoding='utf-8')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('# 野外NPC口吻与闲谈参照' in card and '## 未核与边界' in card, 'card-structure')
check('greeting 446' in card and 'chat 125' in card, 'card-counts')
for g in rd['groups']:
    check(g['title'] in card, g['id'] + '-title-rendered')
    check(g['patterns'][0] in card, g['id'] + '-pattern-rendered')
    for ex in g['examples']:
        check(ex['zh'] in card and f"`{ex['index']}`" in card, g['id'] + '-example-rendered')
check('NPC-READING-S93:BEGIN' in plan and '[[野外NPC口吻与闲谈参照]]' in plan, 'plan-block-and-link')
check('## 每项设计交付' in plan, 'plan-content-preserved')
check('NPC-READING-S93:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
# S98 additions
check(len(rd['npc_tags']) == 6, 'npc-tag-groups-6')
inv_npc = inv['families']['npc']['entries']
unique_keys = {e['key'] for e in inv_npc}
tag_keys = [k for g in rd['npc_tags'] for k in g['keys']]
check(len(tag_keys) == len(set(tag_keys)), 'tag-keys-unique')
check(set(tag_keys) == unique_keys, 'tag-keys-cover-unique-npc-keys')
check(sum(g['count'] for g in rd['npc_tags']) == len(unique_keys), 'tag-count-matches-unique')
bands = next(g for g in rd['npc_tags'] if g['id'] == 'bands')
check(bands['count'] == 14, 'bands-14-keys')
crime = next(g for g in rd['npc_tags'] if g['id'] == 'crime')
check(crime['count'] >= 7, 'crime-keys')
util = next(g for g in rd['npc_tags'] if g['id'] == 'utility')
check(util['count'] >= 4, 'utility-keys')
state = next(g for g in rd['npc_tags'] if g['id'] == 'state')
check(state['count'] >= 5, 'state-keys')
for g in rd['npc_tags']:
    check(g['title'] in card and g['note'] in card, g['id'] + '-tag-rendered')
    check(f"| {g['title']} | {g['count']} |" in card, g['id'] + '-tag-count-rendered')
check('## 场景族的结构结论' in card and rd['scene_finding'] in card, 'scene-finding-rendered')
h = read('research/npc-reading-note-hashes.json')
check(set(h) == {'design/01_原作基线/野外NPC口吻与闲谈参照.md', 'design/11_管理/特殊地点与野外NPC对白扩展计划.md'}, 'own-manifest-two-notes')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S93/S98 field-NPC reading: slot coverage, group summaries, example length/locators, npc behavior tag grouping, scene-structure finding, card rendering and manifest chain; scene/npc tag text lives engine-side and is not read',
              slots=len(slots), groups=len(rd['groups']), npc_tags=len(rd['npc_tags']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/npc-reading-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
