"""Validate the S87 town trust system: sources grounded in the model, bands complete, docs rendered."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)

data = read('research/town-reputation.json')
model = read('research/city-campaign.json')
network = read('research/story-network.json')
towns = data['towns']; town_ids = {t['id'] for t in towns}
model_ids = {c['id'] for c in model['cities']}
check(town_ids == model_ids and len(towns) == 15, 'fifteen-town-records-match-model')
check(len(town_ids) == len(towns), 'no-duplicate-town-ids')
check([b['value'] for b in data['scale']] == [-2, -1, 0, 1, 2], 'scale-five-bands')
check(len(data['rules']) >= 10 and all(r['cn'] and r['en'] for r in data['rules']), 'ten-rules-bilingual')
check(all(data['ui'][k + '_cn'] and data['ui'][k + '_en'] for k in ['label', 'standing', 'changed', 'record_title', 'legend', 'gate', 'freeze']), 'ui-complete-bilingual')
CJK = re.compile(r'[\u4e00-\u9fff]')
for b in data['scale']:
    check(CJK.search(b['behavior_cn']) and not CJK.search(b['behavior_en']), f"scale-{b['value']}-script-purity")
for r in data['rules']:
    check(CJK.search(r['cn']) and not CJK.search(r['en']), r['id'] + '-script-purity')
for k in ['label', 'standing', 'changed', 'record_title', 'legend', 'gate', 'freeze']:
    check(CJK.search(data['ui'][k + '_cn']) and not CJK.search(data['ui'][k + '_en']), 'ui-' + k + '-script-purity')
for t in data['towns']:
    for b in t['bands']:
        check(CJK.search(b['name_cn']) and not CJK.search(b['name_en']), t['id'] + f"-band-b{b['value']}-name-script-purity")
        check(CJK.search(b['line_cn']) and not CJK.search(b['line_en']), t['id'] + f"-band-b{b['value']}-line-script-purity")
    for f2 in ['unlock', 'echo', 'limits']:
        check(CJK.search(t[f2]['cn']) and not CJK.search(t[f2]['en']), t['id'] + f"-{f2}-script-purity")

route_keys = {q['id']: {r['key'] for r in q['routes']} for q in model['quests']}
story_keys = {k: {r.get('key') or r.get('id') for r in v['routes']} for k, v in network['tasks'].items()}
valid_sources = set(route_keys) | set(story_keys)
cast_names = {cid: {a['name'] for a in cast.values()} for cid, cast in model['dramatic_casts'].items()}
in_edges = {e['id'][3:]: e['source'] for e in model['effects'] if e['id'].startswith('IN-')}
BACKSTAGE = re.compile(r'\b(?:N\d{1,2}|SQ\d{2}|DT\d{2}|resolve|paid)\b|(?<![A-Za-z])(?:BRY|DEN|OSB|MNS|ALD|SKO|YOS|KOR|EED|FOR|RAT|PAS|ASH|HIG|MAE)(?![A-Za-z])')

seen_cn = set(); seen_en = set()
edited_units = 0
for t in towns:
    tid = t['id']
    values = [b['value'] for b in t['bands']]
    check(values == [-2, -1, 0, 1, 2], tid + '-five-ordered-bands')
    for b in t['bands']:
        check(b['name_cn'] and b['name_en'] and b['line_cn'] and b['line_en'], tid + f"-band-b{b['value']}-bilingual")
        check(b['name_cn'] not in seen_cn, tid + f"-band-b{b['value']}-cn-name-unique")
        check(b['name_en'] not in seen_en, tid + f"-band-b{b['value']}-en-name-unique")
        seen_cn.add(b['name_cn']); seen_en.add(b['name_en'])
        for field in ['line_cn', 'line_en']:
            check(not BACKSTAGE.search(b[field]), tid + f"-band-b{b['value']}-no-backstage-token-{field}")
    check(t['bands'][0]['name_cn'] != '', tid + '-hostile-band-present')
    for w in t['writes']:
        check(w['source'] in valid_sources, tid + f"-write-source-{w['source']}")
        tokens = set(w['match'])
        pool = route_keys.get(w['source']) or story_keys.get(w['source']) or set()
        check(tokens <= pool, tid + f"-write-tokens-in-source-{w['source']}")
        check(w['delta'] in (-2, -1, 1, 2), tid + f"-write-delta-range-{w['source']}")
        check(w['cn'] and w['en'], tid + f"-write-bilingual-{w['source']}")
        if w['delta'] < 0:
            check(w['source'] in {'N4', 'N11'}, tid + f"-negative-write-only-listed-harm-{w['source']}")
        if w['source'].startswith('DT'):
            check(False, tid + f"-daily-must-not-write-band-{w['source']}")
    check(t['receipt']['source'] == in_edges.get(tid), tid + '-receipt-anchored-to-IN-edge')
    check(t['receipt']['cn'] and t['receipt']['en'], tid + '-receipt-bilingual')
    check(t['unlock']['anchor'] in cast_names.get(tid, set()), tid + '-unlock-anchor-is-local-cast')
    check(t['unlock']['cn'] and t['unlock']['en'], tid + '-unlock-bilingual')
    check(t['echo']['from'] in model_ids and t['echo']['from'] != tid, tid + '-echo-from-another-town')
    check(t['echo']['anchor'] in cast_names.get(tid, set()), tid + '-echo-anchor-is-local-cast')
    check(t['echo']['cn'] and t['echo']['en'], tid + '-echo-bilingual')
    check(t['limits']['cn'] and t['limits']['en'], tid + '-limits-bilingual')
    for field in ['unlock', 'echo', 'limits']:
        for sub in ['cn', 'en']:
            check(not BACKSTAGE.search(t[field][sub]), tid + f"-{field}-no-backstage-{sub}")
    edited_units += len(t['bands']) + len(t['writes'])

pairs = [(x['from'], x['to']) for x in data['transfers']]
check(len(pairs) == len(set(pairs)) == len(data['transfers']) and len(data['transfers']) <= 8, 'transfers-bounded-and-unique')
for x in data['transfers']:
    check(x['from'] in model_ids and x['to'] in model_ids and x['from'] != x['to'], 'transfer-towns-exist-' + x['when'])
    check(x['when'] in route_keys, 'transfer-source-is-regional-chapter-' + x['when'])
    check(x['delta'] == 1 and x.get('once') is True, 'transfer-one-positive-once-' + x['when'])
    check(x['cn'] and x['en'], 'transfer-bilingual-' + x['when'])
group = {cid: g for g, ids in data['groups'].items() for cid in ids}
check(set(group) <= model_ids and len(group) == 12 and len(data['groups']) == 3, 'three-political-blocs-cover-twelve')

sysdoc = (V / '09_系统逻辑/城镇声望与信任系统.md').read_text(encoding='utf-8')
bil = (V / '09_系统逻辑/城镇声望系统中英对照.md').read_text(encoding='utf-8')
check('## 逐地域记录' in sysdoc and '# 城镇声望与信任系统' in sysdoc, 'system-doc-structure')
check('# 城镇声望系统中英对照' in bil and 'TT-UI-LABEL' in bil, 'bilingual-doc-structure')
for t in towns:
    check(f"### {t['name_cn']}（{t['name_en']}）" in sysdoc, t['id'] + '-system-section')
    for b in t['bands']:
        check(b['name_cn'] in sysdoc and b['name_en'] in sysdoc, t['id'] + f"-band-b{b['value']}-rendered")
        check(b['line_cn'] in sysdoc and b['line_cn'] in bil and b['line_en'] in bil, t['id'] + f"-band-b{b['value']}-bilingual-rendered")
    for w in t['writes']:
        check(f"`{w['source']}`" in sysdoc, t['id'] + f"-write-{w['source']}-rendered")
    for field in ['unlock', 'echo', 'limits']:
        check(t[field]['cn'] in sysdoc and t[field]['cn'] in bil and t[field]['en'] in bil, t['id'] + f"-{field}-rendered")
for r in data['rules']:
    check(f"TT-RULE-{r['id']}" in bil, 'rule-' + r['id'] + '-bilingual-key')
for x in data['transfers']:
    check(x['cn'] in sysdoc, 'transfer-' + x['when'] + '-rendered')
for name in ['系统逻辑索引', '经济与奖励', '势力关系总览', '城市与聚落设计总索引', '来源登记']:
    p = next(V.rglob(name + '.md'))
    check('TOWN-REPUTATION-S87:BEGIN' in p.read_text(encoding='utf-8'), name + '-s87-block')
h = read('research/reputation-generated-note-hashes.json')
check(set(h) == {'design/09_系统逻辑/城镇声望与信任系统.md', 'design/09_系统逻辑/城镇声望系统中英对照.md'}, 'own-manifest-two-docs')
for rel, expected in h.items():
    check(sha(ROOT / rel) == expected, rel + '-generated-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = read('research/' + p.name)
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()):
        continue
    for rel, expected in m.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == expected, rel + '-all-manifests-reconciled')
check('未映射引擎' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-s87-block-present')

report = dict(date='2026-10-12', scope='S87 fifteen-town trust design: layered against original reputation and faction commitments, bands/writes/receipts/anchors grounded in the authored model; not runtime, economy or literary validation', towns=len(towns), bands=sum(len(t['bands']) for t in towns), writes=sum(len(t['writes']) for t in towns), transfers=len(data['transfers']), rules=len(data['rules']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/town-reputation-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
