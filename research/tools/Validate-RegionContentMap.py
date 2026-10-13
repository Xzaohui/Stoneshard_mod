"""Validate the S104 original-region to Mod-content mapping and its page."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
rm = read('research/region-content-map.json')
inv = read('research/special-location-inventory.json')
regions = {r['key']: r for r in inv['map_regions']}
stems = {p.stem for p in V.rglob('*.md')}
check(len(rm['regions']) == 8, 'region-count-8')
check({r['key'] for r in rm['regions']} == set(regions), 'regions-match-inventory')
for r in rm['regions']:
    check(r['locator'] == regions[r['key']]['index'], r['key'] + '-locator')
    check(regions[r['key']]['name_zh'].startswith(r['name']), r['key'] + '-name-prefix')
    check(bool(regions[r['key']].get('name_en')), r['key'] + '-en-name')
    check(r['mod'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, r['key'] + '-mod-region')
    check(bool(r['cards']) and all(c in stems for c in r['cards']), r['key'] + '-cards-resolve')
    check(all(p in stems for p in r['people']), r['key'] + '-people-resolve')
card = (V / '02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md').read_text(encoding='utf-8')
check('# 原作地图区域与Mod内容映射' in card and '## 边界' in card, 'card-structure')
check('| 原作区域 | STRG | English | Mod 地域 | 地点卡 | 野外人物 |' in card, 'card-table-header')
for r in rm['regions']:
    name = r['name']
    check(f"{name}（`{r['key']}`）" in card, r['key'] + '-row')
    check(f"| {name}（`{r['key']}`） | {r['locator']} | {regions[r['key']]['name_en']} |" in card, r['key'] + '-locator-rendered')
    for c in r['cards']:
        check(f"[[{c}]]" in card, r['key'] + '-card-linked-' + c)
    for p in r['people']:
        check(f"[[{p}]]" in card, r['key'] + '-person-linked-' + p)
    for f in ['**地貌与生活**', '**入口与安全回程**', '**固定可观察物**', '**特殊危险**', '**服务**', '**原作避让**', '**Mod 落点**']:
        pass
check(card.count('**原作避让**') == 8 and card.count('**入口与安全回程**') == 8, 'per-region-fields-8')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('REGION-MAP-S104:BEGIN' in plan and '[[原作地图区域与Mod内容映射]]' in plan, 'plan-block-and-link')
check('REGION-MAP-S104:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/region-map-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S104 region mapping: eight original regions mapped to Mod regions/cards/people with locators, rendering and chain; not proportions, spawn points or runtime',
              regions=len(rm['regions']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/region-map-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
