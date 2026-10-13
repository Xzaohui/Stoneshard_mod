"""Validate the S89 fine-detail registries: items, NPC details, coverage and rendering."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
items = read('research/item-registry.json'); npcs = read('research/npc-fine-details.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json'); network = read('research/story-network.json')
CJK = re.compile(r'[\u4e00-\u9fff]')
BACKSTAGE = re.compile(r'\b(?:resolve|paid)\b|\b(?:SQ|DT|CM|CS)\b|(?<![A-Za-z])N\d{1,2}(?![A-Za-z0-9])')

# ---- items ----
kinds = {}
for x in items['items']:
    kinds[x['kind']] = kinds.get(x['kind'], 0) + 1
check(kinds == {'document': 26, 'keepsake': 30, 'tool': 7}, 'item-kind-counts')
check(len({x['id'] for x in items['items']}) == len(items['items']), 'item-ids-unique')
check(len(items['style_rules']) >= 6, 'item-style-rules')
term = items.get('terminology_alignment', [])
check(len(term) >= 12, 'terminology-entries')
for x in term:
    check(bool(x.get('concept')) and bool(x.get('mod_usage')) and bool(x.get('note_cn')), 'terminology-fields')
    check(x.get('verdict') in {'match', 'related', 'new', 'deliberate-divergence'}, 'terminology-verdict-' + str(x.get('concept')))
    if x.get('official_cn'):
        check(isinstance(x.get('official_index'), int), 'terminology-index-' + str(x.get('concept')))
    else:
        check(x.get('official_index') is None, 'terminology-no-index-' + str(x.get('concept')))
probe = read('research/official-term-probe.json')
base2 = read('research/local-baseline.json')
check(probe['sha256'] == base2['candidate_baseline']['sha256'], 'official-term-probe-fingerprint')
probe_by = {r['concept']: r for r in probe['entries']}
check(set(probe_by) == {x['concept'] for x in items['terminology_alignment']}, 'official-term-probe-coverage')
for x in items['terminology_alignment']:
    pr = probe_by[x['concept']]
    if pr.get('verified_index') is not None:
        check(x.get('official_index') == pr['verified_index'], 'terminology-verified-index-' + x['concept'])
        check(x.get('official_en') == pr.get('official_en') and not CJK.search(x.get('official_en', '')), 'terminology-official-en-' + x['concept'])
        check(len(x.get('official_en', '')) <= 48, 'terminology-official-en-length-' + x['concept'])
    else:
        check('official_en' not in x, 'terminology-no-en-without-verify-' + x['concept'])
valid = {q['id'] for q in model['quests']} | set(network['tasks']) | {q['id'] for q in cont['quests']}
for x in items['items']:
    for f in ['name_cn', 'name_en', 'desc_cn', 'desc_en', 'rules_cn', 'rules_en']:
        check(bool(x.get(f)), x['id'] + '-field-' + f)
    check(CJK.search(x['desc_cn']) and not CJK.search(x['desc_en']), x['id'] + '-desc-script-purity')
    check(CJK.search(x['rules_cn']) and not CJK.search(x['rules_en']), x['id'] + '-rules-script-purity')
    check(10 <= len(x['desc_cn']) <= 120, x['id'] + '-desc-length')
    check(not BACKSTAGE.search(x['desc_cn']) and not BACKSTAGE.search(x['desc_en']), x['id'] + '-desc-no-backstage')
    check(bool(x.get('origin')), x['id'] + '-origin')
    for o in x.get('origin', []):
        check(o in valid, x['id'] + '-origin-resolves-' + o)

# ---- npcs ----
expected = set()
for cast in model['dramatic_casts'].values():
    for a in cast.values():
        if not a['existing']: expected.add(a['id'])
for a in cont['actors']: expected.add(a['id'])
for c in model['cities']:
    for s in c['satellites']: expected.add(s['resident']['id'])
expected |= {'NPC-N-ENA', 'NPC-N-NARA', 'NPC-N-NELL', 'NPC-N-SEL'}
expected |= {'BRY-NPC-RENA', 'BRY-NPC-OSIN', 'BRY-NPC-MIRO', 'BRY-NPC-VIT',
             'ALD-NPC-HEL', 'ALD-NPC-EMO', 'ALD-NPC-SIN',
             'NPC-SENA', 'NPC-LYD', 'NPC-MAYA', 'MAE-NPC-FIL',
             'SKO-NPC-NIS', 'SKO-NPC-BOH', 'YOS-NPC-TAY', 'YOS-NPC-TIN',
             'DEN-NPC-SEF', 'DEN-NPC-KAR', 'MNS-NPC-ROS', 'MNS-NPC-TIO',
             'EED-NPC-OLA', 'EED-NPC-LIN', 'FOR-NPC-MAN', 'FOR-NPC-APE',
             'OSB-NPC-FUD', 'OSB-NPC-VAS', 'RAT-NPC-ALI', 'RAT-NPC-IME',
             'KOR-NPC-NOD', 'KOR-NPC-EV', 'NPC-MIA', 'ASH-NPC-LINT',
             'HIG-NPC-ARO', 'NPC-HERS',
             'NPC-N-MARA', 'NPC-N-IVO', 'NPC09', 'NPC07', 'NPC04', 'NPC11'}
got = {x['id'] for x in npcs['npcs']}
check(got == expected, 'npc-coverage-exact')
check('NPC-REY' not in got and 'NPC-MORREN' not in got, 'original-game-characters-excluded')
check(len(got) == len(npcs['npcs']), 'npc-ids-unique')
src_names = {}
for cast in model['dramatic_casts'].values():
    for a in cast.values(): src_names[a['id']] = a['name']
for c in model['cities']:
    for s in c['satellites']: src_names[s['resident']['id']] = s['resident']['name']
for a in cont['actors']: src_names[a['id']] = a['name']
src_names.update({'NPC-N-ENA': '艾娜', 'NPC-N-NARA': '纳拉', 'NPC-N-NELL': '妮尔', 'NPC-N-SEL': '塞尔',
                  'NPC-N-MARA': '玛拉', 'NPC-N-IVO': '伊沃', 'NPC09': '欧达·苇', 'NPC07': '托曼·索', 'NPC04': '伊莲·沃斯', 'NPC11': '罗温·雾'})
for x in npcs['npcs']:
    for f in ['look_cn', 'wear_cn', 'carry_cn', 'manner_cn', 'avoid_cn']:
        check(bool(x.get(f)) and CJK.search(x.get(f, '')), x['id'] + '-field-' + f)
        check(not BACKSTAGE.search(x.get(f, '')), x['id'] + '-no-backstage-' + f)
    check(src_names.get(x['id']) == x['name'], x['id'] + '-name-matches-source')
check(any('分人' in r for r in npcs['style_rules']), 'npc-style-rules-same-name-split')
check(any('原作人物' in r for r in npcs['style_rules']), 'npc-style-rules-original-characters')

# ---- docs ----
it = (V / '05_主线/原创物品与装备总表.md').read_text(encoding='utf-8')
np_doc = (V / '04_人物/人物细描与随身物.md').read_text(encoding='utf-8')
check('# 原创物品与装备总表' in it and '## 文书与可读物' in it and '## 工具与有限装备' in it, 'items-doc-structure')
check('## 与原作术语对照' in it and all(x['concept'] in it for x in term), 'items-doc-terminology')
check('# 人物细描与随身物' in np_doc and '同名分人' in np_doc, 'npc-doc-structure')
check('原作人物（维伦、葛文涅尔、雷奥、莫伦、工匠Darrel等）不在此表' in np_doc, 'npc-doc-exclusion-note')
for x in items['items']:
    check(x['id'] in it and x['name_cn'] in it, x['id'] + '-item-rendered')
for x in npcs['npcs']:
    check(x['id'] in np_doc and x['name'] in np_doc, x['id'] + '-npc-rendered')
check(f"本批覆盖 {len(npcs['npcs'])} 名Mod原创人物" in np_doc, 'npc-doc-count')
for name in ['文书与现场文本台本', '人物弧光与关系转折', '经济与奖励', '任务台本总索引']:
    p = next(V.rglob(name + '.md'))
    check('FINE-DETAILS-S89:BEGIN' in p.read_text(encoding='utf-8'), name + '-s89-block')
h = read('research/fine-details-generated-note-hashes.json')
check(set(h) == {'design/05_主线/原创物品与装备总表.md', 'design/04_人物/人物细描与随身物.md'}, 'own-manifest-two-docs')
for rel, exp in h.items():
    check(sha(ROOT / rel) == exp, rel + '-generated-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = read('research/' + p.name)
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()):
        continue
    for rel, exp in m.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-all-manifests-reconciled')
check('FINE-DETAILS-S89:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block-present')

# ---- S91 card attachment ----
by_id = {}
for p in sorted(V.rglob('*.md')):
    t = p.read_text(encoding='utf-8-sig')
    m = re.search(r'^id:\s*(\S+)', t, re.M)
    if m and m.group(1) not in by_id: by_id[m.group(1)] = p.relative_to(V).as_posix()
DUAL = {'NPC-N-MARA': 'CHAR-N1', 'NPC-N-IVO': 'CHAR-N1'}
cards = {}
for x in npcs['npcs']:
    if x['id'] in DUAL: rel = by_id.get('CHAR-N1')
    else: rel = by_id.get('CITY-NPC-' + x['id']) or by_id.get(x['id'])
    check(bool(rel), x['id'] + '-card-resolves')
    if rel: cards.setdefault(rel, []).append(x)
check(len(cards) == 171, 'card-count-171')
for rel, people in cards.items():
    t = (V / rel).read_text(encoding='utf-8')
    check(t.count(f'<!-- FINE-DETAILS-CARD-S91:BEGIN -->') == 1 and f'<!-- FINE-DETAILS-CARD-S91:END -->' in t, rel + '-s91-block')
    for x in people:
        for f in ['look_cn', 'wear_cn', 'carry_cn', 'manner_cn', 'avoid_cn']:
            check(x[f] in t, x['id'] + '-card-field-' + f)
        check(x['name'] in t, x['id'] + '-card-name')
for rel in ['04_人物/人物_艾娜.md', '04_人物/人物_纳拉.md', '04_人物/人物_妮尔.md', '04_人物/人物_塞尔.md']:
    check((V / rel).exists() and 'updated: 2026-10-13' in (V / rel).read_text(encoding='utf-8'), rel + '-created')
for w in ['Write-CitySpaces', 'Write-CityDrama', 'Write-AdditionalCityDrama', 'Write-MaenDrama', 'Write-ForgeAndWoolDrama',
          'Write-ShoreAndVineDrama', 'Write-ForestAndMineDrama', 'Write-GrainAndMemoryDrama', 'Write-NamesAndPassDrama', 'Write-CareAndHighlandDrama',
          'BrynnContinuation']:
    src = (ROOT / 'research/tools' / (w + '.py')).read_text(encoding='utf-8')
    check('NotePreserve import' in src and ('preserve_foreign(' in src or 'keep_foreign(' in src), w + '-preserves-foreign-blocks')
check('FINE-DETAILS-S91:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-s91-block')
h91 = read('research/fine-details-card-note-hashes.json')
check(len(h91) == 171 and all(rel.startswith('design/') for rel in h91), 's91-own-manifest')
for rel, exp in h91.items():
    check(sha(ROOT / rel) == exp, rel + '-s91-hash')

report = dict(date='2026-10-13', scope='S89/S91 fine details: item registry, NPC detail coverage, field completeness, script purity, origin resolution, rendering, and per-card attachment blocks; not numeric economy, art or runtime validation',
              items=len(items['items']), documents=kinds.get('document', 0), keepsakes=kinds.get('keepsake', 0), tools=kinds.get('tool', 0),
              npcs=len(npcs['npcs']), cards=len(cards), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/fine-details-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
