"""Validate the S115 regional ambient gossip: parity, conditions, links and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ag = read('research/ambient-gossip.json')
fx = read('research/field-npc-dialogue.json')
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
check(len(ag['lines']) == 30, 'line-count-30')
check(len(ag['rules']) >= 4, 'rules-present')
check(ag['vocabulary'] == ['any', 'night', 'band:+1', 'band:-1', 'after:<task>'], 'vocabulary-fixed')
per = {}
seen_cn, seen_en = {}, {}
field_lines = {t for n in fx['npcs'] for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]
               + [(None, v) for kk in ('before', 'after', 'early', 'late', 'proxy') for v in n['visits'][kk]]}
for x in ag['lines']:
    per[x['region']] = per.get(x['region'], 0) + 1
    check(x['region'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, x['id'] + '-region')
    check(re.fullmatch(r'any|night|band:[+-]1|after:.+', x['when']) is not None, x['id'] + '-when')
    check(bool(CJK.search(x['cn'])) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + '-cn-purity')
    check(not CJK.search(x['en']) and len(x['en']) <= 150, x['id'] + '-en-purity')
    check(not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + '-no-backstage')
    check(x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + '-unique')
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
    check(x['cn'] not in field_lines, x['id'] + '-no-field-clone')
    if x['when'].startswith('after:'): check(x['when'][6:] in stems, x['id'] + '-after-resolves')
    check(x['link'] in stems, x['id'] + '-link-resolves')
    check(bool(x['speaker'].strip()), x['id'] + '-speaker')
check(per == {'R01': 5, 'R02': 5, 'R03': 5, 'R04': 5, 'R05': 5, 'R06': 5}, 'per-region-5')
card = (V / '02_世界与地图/特殊地点与野外NPC/地区闲谈池.md').read_text(encoding='utf-8')
check('# 地区闲谈池' in card and '## 边界' in card, 'card-structure')
check('**条件词表**' in card and '`after:<台本>` 只改未来台词' in card, 'card-vocabulary')
for x in ag['lines']:
    check(f"「{x['cn']}」" in card and x['en'] in card and f"[[{x['link']}]]" in card, x['id'] + '-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('AMBIENT-GOSSIP-S115:BEGIN' in plan and '[[地区闲谈池]]' in plan, 'plan-block-and-link')
check('AMBIENT-GOSSIP-S115:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/ambient-gossip-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S115 ambient gossip: region coverage, condition vocabulary, CN/EN parity and purity, uniqueness, links and chain; not triggers, voice work or runtime',
              lines=len(ag['lines']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/ambient-gossip-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
