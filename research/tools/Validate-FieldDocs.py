"""Validate the S100 field-site documents, rendering and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
fd = read('research/field-docs.json')
inv = read('research/special-location-inventory.json')
SITES = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
fxn = read('research/field-npc-dialogue.json')
npc_ids = {n['id'] for n in fxn['npcs']}
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
check(len(fd['docs']) == 12, 'doc-count-12')
check(len(fd['rules']) >= 4, 'rules-present')
texts = set(); en_texts = {}
for d in fd['docs']:
    check(d['site'] in SITES, d['id'] + '-site-known')
    check(d['holder'] in npc_ids, d['id'] + '-holder-is-field-npc')
    check(20 <= len(d['text']) <= 120, d['id'] + '-text-length')
    check(bool(CJK.search(d['text'])) and not re.search(r'[A-Za-z]', d['text']), d['id'] + '-text-purity')
    check(d['text'] not in texts, d['id'] + '-text-unique')
    texts.add(d['text'])
    for k in ('title', 'state', 'where', 'read'): check(bool(d[k].strip()), d['id'] + '-' + k)
    for k in ('title_en', 'text_en', 'read_en'):
        e = d.get(k, '')
        check(bool(e.strip()) and not re.search(r'[\u4e00-\u9fff]', e), d['id'] + '-en-purity-' + k)
        check(len(e) <= 260, d['id'] + '-en-length-' + k)
        check(e not in en_texts, d['id'] + '-en-unique-' + k)
        en_texts[e] = d['id']
    check(any(w in d['state'] for w in ['原件', '副件', '残件']), d['id'] + '-state-marked')
card = (V / '02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md').read_text(encoding='utf-8')
check('# 文书_FX_野外地点短稿' in card and '## 边界' in card, 'card-structure')
for d in fd['docs']:
    check(d['title'] in card and f"`{d['id']}`" in card, d['id'] + '-row')
    check(f"> {d['text']}" in card, d['id'] + '-text-rendered')
    check(d['title_en'] in card and d['text_en'] in card and d['read_en'] in card, d['id'] + '-en-rendered')
    check(d['read'] in card, d['id'] + '-read-rendered')
    holder_card = next((p.stem for p in (V / '04_人物/野外人物').glob(f"人物_{d['holder']}_*.md")), None)
    check(holder_card is not None and f"[[{holder_card}]]" in card, d['id'] + '-holder-link')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('FIELD-DOCS-S100:BEGIN' in plan and '[[文书_FX_野外地点短稿]]' in plan, 'plan-block-and-link')
check('FIELD-DOCS-S100:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/field-docs-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S100/S107 field documents: site/holder binding, copy-state marking, bilingual text length and purity, rendering, links and chain; not placement or interaction scripts',
              docs=len(fd['docs']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/field-docs-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
