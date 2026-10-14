"""Validate the S87 foreshadow ledger: closure of all X edges, reference counts, open items and rendering."""
from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)

data = read('research/foreshadow-ledger.json')
network = read('research/story-network.json'); edges = {e['id']: e for e in network['edges']}
model = read('research/city-campaign.json')
cont = read('research/brynn-continuation.json')
rep = read('research/town-reputation.json')
story_ids = set(network['tasks']) | {f'D{i:02}' for i in range(1, 11)}
quest_ids = {q['id'] for q in model['quests']} | {q['id'] for q in cont['quests']}
city_ids = {c['id'] for c in model['cities']}
allowed = story_ids | quest_ids | city_ids
threads = data['threads']; tid = [t['id'] for t in threads]
check(len(tid) == len(set(tid)), 'unique-thread-ids')
check(set(data['buckets']) == {'must_payoff', 'reference', 'deliberate_open'}, 'three-buckets')
check(len(threads) >= 28, 'thread-count')
for t in threads:
    check(t['bucket'] in data['buckets'], t['id'] + '-bucket-valid')
    check(t['name_cn'] and t['name_en'], t['id'] + '-bilingual-name')
    for pid in t.get('plants', []):
        check(pid in allowed, t['id'] + f"-plant-exists-{pid}")
    if t['bucket'] == 'must_payoff':
        check(t.get('plants') and t.get('payoff') and t.get('backed_by'), t['id'] + '-mechanism-complete')
        check(t['guard_cn'] and t['guard_en'], t['id'] + '-bilingual-guard')
        for x in t['backed_by']:
            e = edges.get(x)
            check(e is not None, t['id'] + f"-edge-exists-{x}")
            if e:
                check(e['source'] in t['plants'], t['id'] + f"-edge-{x}-plant-matches-{e['source']}")
                check(e['target'] in t['payoff'], t['id'] + f"-edge-{x}-payoff-matches-{e['target']}")
        for pid in t['payoff']:
            check(pid in allowed, t['id'] + f"-payoff-exists-{pid}")
    if t['bucket'] == 'reference':
        check((ROOT / t['registry']).exists(), t['id'] + '-registry-exists')
        check(t['owner'] and t['count'] > 0 and t['guard_cn'] and t['guard_en'], t['id'] + '-reference-meta')
    if t['bucket'] == 'deliberate_open':
        check(t['rationale_cn'] and t['rationale_en'], t['id'] + '-bilingual-rationale')
        check('backed_by' not in t, t['id'] + '-open-has-no-mechanism')
covered = [x for t in threads if t['bucket'] == 'must_payoff' for x in t['backed_by']]
check(len(covered) == len(set(covered)), 'no-edge-covered-twice')
check(set(covered) == set(edges), 'all-X-edges-covered-74')
ref = {t['id']: t for t in threads if t['bucket'] == 'reference'}
check(ref['FS-25']['count'] == len(cont['effects']) == 15, 'brynn-bridges-15')
check(ref['FS-26']['count'] == len(rep['towns']) == 15, 'town-entitlements-15')
check(ref['FS-27']['count'] == sum('echo' in x for x in rep['towns']) == 15, 'town-hearsay-15')
check(ref['FS-28']['count'] == sum(e['id'].startswith('IN-') for e in model['effects']) == 15, 'in-receipts-15')
check(len([t for t in threads if t['bucket'] == 'deliberate_open']) >= 4, 'four-open-items')

doc = (V / '09_系统逻辑/伏笔与回收台账.md').read_text(encoding='utf-8')
check('# 伏笔与回收台账' in doc and '## 主线与并入丝线' in doc and '## 有意留白' in doc, 'doc-structure')
for t in threads:
    check(t['name_cn'] in doc, t['id'] + '-rendered')
    if t['bucket'] == 'must_payoff':
        check(t['guard_cn'] in doc and all(x in doc for x in t['backed_by']), t['id'] + '-mechanism-rendered')
    if t['bucket'] == 'deliberate_open':
        check(t['rationale_cn'] in doc, t['id'] + '-rationale-rendered')
check(f'{len(edges)}条，全部由丝线背书覆盖' in doc, 'doc-states-x-coverage')
for name in ['系统逻辑索引', '任务台本总索引', '布林续篇任务与伏笔回收总表']:
    p = next(V.rglob(name + '.md'))
    check('FORESHADOW-LEDGER-S87:BEGIN' in p.read_text(encoding='utf-8'), name + '-s87-block')
h = read('research/foreshadow-generated-note-hashes.json')
check(set(h) == {'design/09_系统逻辑/伏笔与回收台账.md'}, 'own-manifest-one-doc')
for rel, expected in h.items():
    check(sha(ROOT / rel) == expected, rel + '-generated-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = read('research/' + p.name)
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()):
        continue
    for rel, expected in m.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == expected, rel + '-all-manifests-reconciled')
check('FORESHADOW-LEDGER-S87:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block-present')

report = dict(date='2026-10-12', scope='S87 foreshadow ledger: all 74 X edges closed into threads, reference groups counted, four deliberate open items; not literary or runtime validation', threads=len(threads), must_payoff=sum(t['bucket'] == 'must_payoff' for t in threads), edges_covered=len(covered), references=len(ref), open_items=len([t for t in threads if t['bucket'] == 'deliberate_open']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/foreshadow-ledger-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
