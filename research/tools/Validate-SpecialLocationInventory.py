"""Validate the S92 special-location inventory, its card and the source chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
inv = read('research/special-location-inventory.json'); base = read('research/local-baseline.json')
KANA = re.compile(r'[\u3040-\u30ff]'); HANGUL = re.compile(r'[\uac00-\ud7af]'); CJK = re.compile(r'[\u4e00-\u9fff]')

check(inv['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint-matches-baseline')
check(inv['bytes'] == base['candidate_baseline']['bytes'] and inv['strg_count'] == base['candidate_baseline']['strg_count'], 'size-and-strg-match')
check(len(inv['map_regions']) == 8, 'map-region-count-8')
check(len(inv['rumor_sites']) == 44, 'rumor-site-count-44')
check(len(inv['site_types']) == 13, 'site-type-count-13')
check(inv['site_types_without_zh'] == [], 'all-site-types-have-zh')
check(set(inv['site_type_identifier_only']) <= {'Cave11', 'Cave12'}, 'identifier-only-subset-cave11-12')
fam = inv['dialogue_families']
check(fam == {'scene': 326, 'greeting': 446, 'chat': 125, 'npc': 227, 'follower': 8}, 'dialogue-family-counts')
seen = set()
for group in ['map_regions', 'rumor_sites', 'site_types']:
    for r in inv[group]:
        check(r['key'] not in seen, r['key'] + '-unique')
        seen.add(r['key'])
        check(bool(CJK.search(r['name_zh'])) and not KANA.search(r['name_zh']) and not HANGUL.search(r['name_zh']), r['key'] + '-zh-pure')
        check(2 <= len(r['name_zh']) <= 24, r['key'] + '-name-length')
        check(isinstance(r['index'], int) and r['index'] > 0, r['key'] + '-index')
        check(bool(r.get('name_en')) and not CJK.search(r['name_en']) and len(r['name_en']) <= 48, r['key'] + '-en-name')
for r in inv['rumor_sites']:
    check(r['dialogue_entries'] >= 1, r['key'] + '-has-dialogue-entry')
    check(all(re.fullmatch(r'[A-Za-z ]{3,}', t) for t in r['towns']), r['key'] + '-towns-latin')

# no long text stored anywhere except method/limits/source
long_ok = {'method', 'limits', 'source', 'sha256'}
def walk(node, path=''):
    if isinstance(node, dict):
        for k, v in node.items(): walk(v, path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node): walk(v, path + '/[]')
    elif isinstance(node, str):
        if len(node) > 60: check(path.rsplit('/', 1)[-1] in long_ok, 'no-long-text' + path)
walk(inv)
card = (V / '01_原作基线/特殊地点与野外NPC清点.md').read_text(encoding='utf-8')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('# 特殊地点与野外NPC清点' in card and '## 世界地图区域' in card and '## 特殊地点候选' in card and '## 地形与类型名' in card, 'card-structure')
check('## 未核与边界' in card and '不保存对白全文' in card, 'card-limits')
check(inv['sha256'][:16] in card and str(inv['strg_count']) in card, 'card-fingerprint')
for group in ['map_regions', 'rumor_sites', 'site_types']:
    for r in inv[group]:
        check(f"`{r['key']}`" in card and r['name_zh'] in card, r['key'] + '-card-row')
        check(r.get('name_en', '') in card, r['key'] + '-en-name-rendered')
check('SPECIAL-LOC-S92:BEGIN' in plan and '[[特殊地点与野外NPC清点]]' in plan, 'plan-block-and-link')
check('## 每项设计交付' in plan and 'SPECIAL-LOC-S92:END' in plan, 'plan-content-preserved')
check('SPECIAL-LOC-S92:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/special-location-note-hashes.json')
check(set(h) == {'design/01_原作基线/特殊地点与野外NPC清点.md', 'design/11_管理/特殊地点与野外NPC对白扩展计划.md'}, 'own-manifest-two-notes')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S92 special-location inventory: source fingerprint, family counts, zh purity, card rendering and manifest chain; not runtime reachability, dialogue reading or design cards',
              regions=len(inv['map_regions']), rumor_sites=len(inv['rumor_sites']), site_types=len(inv['site_types']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/special-location-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
