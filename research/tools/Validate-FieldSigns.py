"""Validate the S101 field signs, coverage of remaining sites, rendering and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
sg = read('research/field-signs.json')
inv = read('research/special-location-inventory.json')
SITES = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
fx = read('research/field-npc-dialogue.json')
have = {n['site'] for n in fx['npcs']}
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
check(len(sg['signs']) == 16, 'sign-count-16')
check(len(sg['rules']) >= 4, 'rules-present')
sign_sites = {s['site'] for s in sg['signs']}
check(sign_sites | have == set(SITES), 'sites-covered-by-people-or-signs')
check(len(sign_sites) == 16, 'sign-sites-unique')
obs = set(); en_texts = {}
for s in sg['signs']:
    for k in ('title', 'obs', 'judge', 'danger'):
        check(bool(s[k].strip()) and bool(CJK.search(s[k])), s['id'] + '-' + k)
        check(not re.search(r'[A-Za-z]', s[k]), s['id'] + '-purity-' + k)
    check(s['obs'] not in obs, s['id'] + '-obs-unique')
    for k in ('title_en', 'obs_en', 'judge_en', 'danger_en'):
        e = s.get(k, '')
        check(bool(e.strip()) and not re.search(r'[\u4e00-\u9fff]', e), s['id'] + '-en-purity-' + k)
        check(len(e) <= 220, s['id'] + '-en-length-' + k)
        check(e not in en_texts, s['id'] + '-en-unique-' + k)
        en_texts[e] = s['id']
    obs.add(s['obs'])
    if s['link']:
        check(s['link'] in stems, s['id'] + '-link-resolves')
card = (V / '02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md').read_text(encoding='utf-8')
check('# 野外迹象与观察' in card and '## 边界' in card and '人物与迹象合计覆盖 44 处传闻地点' in card, 'card-structure')
for s in sg['signs']:
    check(s['title'] in card and f"`{s['id']}`" in card and f"`{s['site']}`" in card, s['id'] + '-row')
    check(s['obs'] in card and s['judge'] in card and s['danger'] in card, s['id'] + '-fields-rendered')
    check(s['title_en'] in card and s['obs_en'] in card and s['judge_en'] in card and s['danger_en'] in card, s['id'] + '-en-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('FIELD-SIGNS-S101:BEGIN' in plan and '[[野外迹象与观察]]' in plan, 'plan-block-and-link')
check('FIELD-SIGNS-S101:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/field-signs-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S101/S107 field signs: coverage of the 16 remaining sites, bilingual observation/judgement/danger purity, links and chain; not spawn points, proportions or runtime',
              signs=len(sg['signs']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/field-signs-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
