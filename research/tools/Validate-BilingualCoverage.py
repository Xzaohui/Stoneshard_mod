"""Validate the S120 bilingual coverage report by recomputing pair counts."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
bc = read('research/bilingual-coverage.json')
rows = {r['registry']: r for r in bc['rows']}
check(len(bc['rows']) == 14, 'row-count-14')
check(bc['user_zh_only'] == 0, 'no-user-facing-zh-only')
check(bc['user_pairs'] == sum(r['pairs'] for r in bc['rows'] if r['kind'] == 'user'), 'user-pairs-sum')
# recompute the explicit registries
fx = read('research/field-npc-dialogue.json')
check(rows['field-npc-dialogue']['pairs'] == sum(len([1 for _ in (x.get('english') or {}).values() if _]) for x in fx['npcs']), 'recompute-field-npc')
fd = read('research/field-docs.json')
check(rows['field-docs']['pairs'] == sum(3 for d in fd['docs'] if d.get('title_en') and d.get('text_en') and d.get('read_en')), 'recompute-docs')
sg = read('research/field-signs.json')
check(rows['field-signs']['pairs'] == sum(4 for s in sg['signs'] if s.get('title_en') and s.get('obs_en') and s.get('judge_en') and s.get('danger_en')), 'recompute-signs')
for reg, path in [('ambient-gossip', 'research/ambient-gossip.json'), ('town-gossip', 'research/town-gossip.json'), ('band-gossip', 'research/band-gossip.json')]:
    d = read(path)
    check(rows[reg]['pairs'] == sum(1 for x in d['lines'] if x.get('cn') and x.get('en')), 'recompute-' + reg)
inv = read('research/special-location-inventory.json')
check(rows['special-location-inventory']['pairs'] == sum(1 for g in ('map_regions', 'rumor_sites', 'site_types') for r in inv[g] if r.get('name_zh') and r.get('name_en')), 'recompute-names')
svc = read('research/service-registry.json')
check(all(s.get('convenience_en') and s.get('refresh_en') for s in svc['services']), 'service-en-present')
items = read('research/item-registry.json')
check(all(('official_en' in x) == (read('research/official-term-probe.json')['entries'][i].get('verified_index') is not None)
          for i, x in enumerate(items['terminology_alignment'])), 'official-en-matches-probe')
card = (V / '11_管理/中英对照覆盖报告.md').read_text(encoding='utf-8')
check('# 中英对照覆盖报告' in card and '## 边界' in card and '**口径**' in card, 'card-structure')
check(f"用户可见文本共 {bc['user_pairs']} 组中英成对" in card and '中文单语 0 条' in card, 'card-numbers')
for r in bc['rows']:
    check(f"| {r['registry']} |" in card, 'card-row-' + r['registry'])
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('BILINGUAL-COVERAGE-S120:BEGIN' in plan and '[[中英对照覆盖报告]]' in plan, 'plan-block-and-link')
check('BILINGUAL-COVERAGE-S120:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/bilingual-coverage-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S120 bilingual coverage: recomputed pair counts, user-facing zh-only is zero, service and official-term pairs present, rendering and chain; not translation quality or runtime',
              user_pairs=bc['user_pairs'], rows=len(bc['rows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/bilingual-coverage-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
