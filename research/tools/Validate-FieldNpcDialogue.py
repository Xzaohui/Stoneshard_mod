"""Validate the S94 field-NPC roster, authored dialogue, cards and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
fd = read('research/field-npc-dialogue.json')
inv = read('research/special-location-inventory.json')
SITES = {r['key'] for r in inv['rumor_sites']} | {r['key'] for r in inv['site_types']}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACKSTAGE = re.compile(r'[A-Za-z]')
check(len(fd['npcs']) == 36, 'roster-36')
stems = {p.stem for p in V.rglob('*.md')}
check(len(fd['rules']) >= 5, 'rules-present')
ids = set(); lines = {}; en_lines = {}
for n in fd['npcs']:
    check(n['id'] not in ids, n['id'] + '-unique'); ids.add(n['id'])
    check(n['site'] in SITES, n['id'] + '-site-known')
    check(n['region'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, n['id'] + '-region')
    for k in ('name', 'role', 'look', 'voice'): check(bool(n[k].strip()), n['id'] + '-' + k)
    check(len(n['knows']) >= 2 and len(n['not_knows']) >= 2, n['id'] + '-knowledge-limits')
    check([k for k, _ in n['greetings']] == ['first', 'revisit', 'night'], n['id'] + '-greeting-keys')
    check(len(n['chats']) >= 3, n['id'] + '-chats')
    check([k for k, _ in n['site_lines']] == ['arrival', 'warning', 'refusal'], n['id'] + '-site-keys')
    check(bool(n['links']), n['id'] + '-links')
    v = n['visits']
    check(v['task'] in stems, n['id'] + '-visit-task-resolves')
    for key in ('before', 'after', 'early', 'late', 'proxy'):
        check(bool(v[key]) and all(CJK.search(t) and len(t) <= 48 and not BACKSTAGE.search(t) for t in v[key]), n['id'] + '-visit-' + key)
    SLOTS = ['greet.first', 'greet.revisit', 'greet.night', 'chat.1', 'chat.2', 'chat.3',
             'site.arrival', 'site.warning', 'site.refusal',
             'visit.before', 'visit.after', 'visit.early', 'visit.late', 'visit.proxy']
    en = n.get('english') or {}
    check(sorted(en) == sorted(SLOTS), n['id'] + '-english-slots')
    for slot in SLOTS:
        s2 = en.get(slot, '')
        check(bool(s2.strip()) and not re.search(r'[\u4e00-\u9fff]', s2), n['id'] + '-english-purity-' + slot)
        check(len(s2) <= 160, n['id'] + '-english-length-' + slot)
        check(s2 not in en_lines, n['id'] + '-english-unique-' + slot)
        en_lines[s2] = n['id']
    for k, t in n['greetings'] + n['site_lines'] + [(f'chat{i}', c) for i, c in enumerate(n['chats'], 1)] + \
            [(key, t) for key in ('before', 'after', 'early', 'late', 'proxy') for t in v[key]]:
        check(bool(CJK.search(t)) and len(t) <= 48, n['id'] + '-line-len-' + str(k))
        check(not BACKSTAGE.search(t), n['id'] + '-line-no-latin-' + str(k))
        check(t not in lines, n['id'] + '-line-unique-' + str(k))
        lines[t] = n['id']
for n in fd['npcs']:
    for l in n['links']: check(l in stems, n['id'] + '-link-resolves-' + l)
agg_rel = '02_世界与地图/特殊地点与野外NPC/台本_FX_野外人物对白.md'
agg = (V / agg_rel).read_text(encoding='utf-8')
check('# 台本_FX_野外人物对白' in agg and '## 边界' in agg, 'aggregate-structure')
for n in fd['npcs']:
    rel = f"04_人物/野外人物/人物_{n['id']}_{n['name']}.md"
    check((V / rel).exists(), n['id'] + '-card-exists')
    card = (V / rel).read_text(encoding='utf-8')
    check(n['role'] in card and n['look'] in card and n['voice'] in card, n['id'] + '-card-fields')
    check(f"`{n['site']}`" in card and '[[台本_FX_野外人物对白]]' in card, n['id'] + '-card-links')
    check(f"## {n['name']}·{n['role']}" in agg and f"[[人物_{n['id']}_{n['name']}]]" in agg, n['id'] + '-aggregate-row')
    check(f"关联台本：[[{n['visits']['task']}]]" in agg, n['id'] + '-visit-task-rendered')
    for k, t in n['greetings'] + n['site_lines'] + [(f'chat{i}', c) for i, c in enumerate(n['chats'], 1)] + \
            [(key, t) for key in ('before', 'after', 'early', 'late', 'proxy') for t in n['visits'][key]]:
        check(f"「{t}」" in agg, n['id'] + '-line-rendered-' + str(k))
    for slot in SLOTS:
        check(en[slot] in agg, n['id'] + '-english-rendered-' + slot)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('FIELD-NPC-S94:BEGIN' in plan and '[[台本_FX_野外人物对白]]' in plan, 'plan-block-and-link')
check('FIELD-NPC-S94:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/field-npc-note-hashes.json')
check(len(h) == 38 and agg_rel in {rel.replace('design/', '') for rel in h}, 'own-manifest-38')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S94/S97/S99/S106 field NPCs: roster, site/region mapping, knowledge limits, bilingual dialogue length/uniqueness/rendering, links and manifest chain; not proportional placement or runtime rooms',
              npcs=len(fd['npcs']), lines=len(lines), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/field-npc-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
