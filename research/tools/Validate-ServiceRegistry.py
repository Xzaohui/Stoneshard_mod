"""Validate the S90 service registry: one service per city, resolvable operators, finite stock, band gates and rendering."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
data = read('research/service-registry.json'); model = read('research/city-campaign.json')
CJK = re.compile(r'[\u4e00-\u9fff]')
BACKSTAGE = re.compile(r'\b(?:resolve|paid)\b|\b(?:SQ|DT|CM|CS)\b|(?<![A-Za-z])N\d{1,2}(?![A-Za-z0-9])')
city_ids = [c['id'] for c in model['cities']]
svc = data['services']
check([s['city'] for s in svc] == city_ids, 'one-service-per-city-in-order')
check(len({s['id'] for s in svc}) == len(svc) == 15, 'fifteen-services-unique')
check(len(data['shared_rules']) >= 6 and any('不刷新' in r for r in data['shared_rules']), 'shared-rules')
anchors = {}
for cid, cast in model['dramatic_casts'].items():
    anchors[cid] = {a['name'] for a in cast.values()}
    anchors[cid] |= {s['resident']['name'] for s in next(c for c in model['cities'] if c['id'] == cid)['satellites']}
    anchors[cid] |= {p[0] for p in next(c for c in model['cities'] if c['id'] == cid)['people']}
for s in svc:
    for f in ['name_cn', 'name_en', 'function_cn', 'function_en', 'bounds_cn', 'bounds_en', 'convenience_cn', 'convenience_en', 'refresh_cn', 'refresh_en']:
        check(bool(s.get(f)), s['id'] + '-field-' + f)
    check(CJK.search(s['function_cn']) and not CJK.search(s['function_en']), s['id'] + '-function-script-purity')
    check(CJK.search(s['bounds_cn']) and not CJK.search(s['bounds_en']), s['id'] + '-bounds-script-purity')
    check(s['operator'] in anchors.get(s['city'], set()), s['id'] + '-operator-resolves')
    check(len(s['stock']) >= 2 and all(x.strip() for x in s['stock']), s['id'] + '-finite-stock')
    check('+1' in s['convenience_cn'] and '+2' in s['convenience_cn'], s['id'] + '-band-convenience')
    check('+1' in s['convenience_en'] and '+2' in s['convenience_en'], s['id'] + '-band-convenience-en')
    check(not re.search(r'[\u4e00-\u9fff]', s['convenience_en'] + s['refresh_en']), s['id'] + '-en-purity')
    check(len(s['convenience_en']) <= 200 and len(s['refresh_en']) <= 200, s['id'] + '-en-length')
    check(any(k in s['refresh_cn'] for k in ['不刷新', '按批', '按案', '占满']), s['id'] + '-refresh-rule')
    check('负声望' in s['bounds_cn'] or '低信任' in s['bounds_cn'], s['id'] + '-low-band-safety')
    for f in ['function_cn', 'function_en', 'bounds_cn', 'bounds_en', 'convenience_cn', 'refresh_cn']:
        check(not BACKSTAGE.search(s.get(f, '')), s['id'] + '-no-backstage-' + f)
doc = (V / '09_系统逻辑/城市服务班与有限库存.md').read_text(encoding='utf-8')
check('# 城市服务班与有限库存' in doc and '## 共享规则' in doc and '## 一览' in doc, 'doc-structure')
for s in svc:
    check(s['name_cn'] in doc and s['name_en'] in doc and s['operator'] in doc, s['id'] + '-rendered')
    check(f"## {s['city']}：{s['name_cn']}" in doc, s['id'] + '-section')
for name in ['经济与奖励', '城市与聚落设计总索引', '系统逻辑索引', '城市篇章与跨区域任务网']:
    p = next(V.rglob(name + '.md'))
    check('SERVICE-REGISTRY-S90:BEGIN' in p.read_text(encoding='utf-8'), name + '-s90-block')
for s in svc:
    c = next(x for x in model['cities'] if x['id'] == s['city'])
    ct = (V / c['file']).read_text(encoding='utf-8')
    check('SERVICE-REGISTRY-S90:BEGIN' in ct and s['name_cn'] in ct and s['operator'] in ct, s['id'] + '-city-page-block')
h = read('research/service-generated-note-hashes.json')
check(set(h) == {'design/09_系统逻辑/城市服务班与有限库存.md'}, 'own-manifest-one-doc')
for rel, exp in h.items():
    check(sha(ROOT / rel) == exp, rel + '-generated-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = read('research/' + p.name)
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()):
        continue
    for rel, exp in m.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-all-manifests-reconciled')
check('SERVICE-REGISTRY-S90:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block-present')
report = dict(date='2026-10-12', scope='S90 fifteen city services: one per city, resolvable operators, finite stock, band conveniences, refresh rules and low-band safety; not price calibration, art or runtime validation',
              services=len(svc), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/service-registry-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
