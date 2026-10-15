"""Validate the S88 timeline-and-reward registry against its sources and rendering."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cell(t, n=88):
    if not t: return ''
    t = re.sub(r'\s+', ' ', str(t)).strip()
    return t if len(t) <= n else t[:n] + '…'
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)

reg = read('research/timeline-registry.json')
main = read('research/story-main.json') + read('research/story-main-late.json')
side = read('research/story-side.json'); daily = read('research/story-daily.json'); dungeons = read('research/story-dungeon.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')

check([q['id'] for q in reg['main']] == [q['id'] for q in main] == [f'N{i}' for i in range(1, 19)], 'main-18-in-order')
check([q['id'] for q in reg['side']] == [q['id'] for q in side] == [f'SQ{i:02}' for i in range(1, 9)], 'side-8-in-order')
check([q['id'] for q in reg['daily']] == [q['id'] for q in daily] and len(reg['daily']) == 16, 'daily-16')
check([q['id'] for q in reg['dungeon']] == [q['id'] for q in dungeons] and len(reg['dungeon']) == 9, 'dungeon-9')
check([q['id'] for q in reg['city']] == [q['id'] for q in model['quests']] and len(reg['city']) == 73, 'city-73')
check([q['id'] for q in reg['continuation']] == [q['id'] for q in cont['quests']] and len(reg['continuation']) == 6, 'continuation-6')
# Freshness: the registry must equal a fresh extraction (no stale or hand-edited numbers).
fresh = {
 'main': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], at_least=q.get('at_least'), reward=cell(q.get('reward'))) for q in main],
 'side': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], reward=cell(q.get('reward'))) for q in side],
 'daily': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], cooldown=q.get('cooldown'), deadline=cell(q.get('deadline')), state=cell(q.get('state')), reward=cell(q.get('reward'))) for q in daily],
 'dungeon': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], main=cell(q.get('main')), side=cell(q.get('side')), reward=cell(q.get('reward'))) for q in dungeons],
 'city': [dict(id=q['id'], city=q['city'], kind=q['kind'], requires=q.get('requires') or [], turn=cell(q.get('turn')), need=cell(q.get('need'))) for q in model['quests']],
 'continuation': [dict(id=q['id'], title=q['title'], requires=q.get('requires') or [], repeatable=q.get('repeatable'), reward_owner=q.get('reward_owner')) for q in cont['quests']]}
for k in fresh:
    check(reg[k] == fresh[k], 'registry-fresh-' + k)
ids = {q['id'] for g in [main, side, daily, dungeons] for q in g} | {q['id'] for q in model['quests']} | {q['id'] for q in cont['quests']}
for group in ['main', 'side', 'daily', 'dungeon', 'city', 'continuation']:
    for q in reg[group]:
        for req in q['requires']:
            check(req in ids, f"{q['id']}-requires-{req}")
for q in reg['daily']:
    check(q['cooldown'] and q['cooldown'] > 0, q['id'] + '-explicit-cooldown')
    check(q['deadline'] and '倒计时' in q['deadline'], q['id'] + '-explicit-deadline-semantics')
    check('episode_state' in q['state'], q['id'] + '-episode-state')
for q in reg['main']:
    check(q['reward'], q['id'] + '-reward-statement')
for q in reg['side']:
    check(q['reward'], q['id'] + '-reward-statement')
for q in reg['dungeon']:
    check(q['main'], q['id'] + '-entry-position')
for q in reg['city']:
    check(q['turn'], q['id'] + '-turn')
    check(q['kind'] in {'regional-main', 'city-side'}, q['id'] + '-kind')
for q in reg['continuation']:
    check(q['repeatable'] is False, q['id'] + '-one-time')
    check(q['reward_owner'], q['id'] + '-reward-owner')
check('N17' in reg['main'][-1]['requires'], 'N18-requires-N17')
# Reward bands follow 经济与奖励: N 0–0.7B, side stages 0.2–0.3B, dailies 0.15–0.3B;
# values explicitly marked 停用 are historical and excluded. Audit full source text,
# not the trimmed registry cells, so trailing qualifiers stay visible.
RANGE = {'main': (0.0, 0.7), 'side': (0.2, 0.3), 'daily': (0.15, 0.3)}
SRC = {'main': main, 'side': side, 'daily': daily}
out = []
for group, (lo, hi) in RANGE.items():
    for q in SRC[group]:
        for m2 in re.finditer(r'(\d+(?:\.\d+)?)B(.{0,8})', q.get('reward') or ''):
            if '停用' in m2.group(2):
                continue
            val = float(m2.group(1))
            if not (lo <= val <= hi):
                out.append((q['id'], val, (q.get('reward') or '')[:60]))
check(not out, 'reward-within-documented-band')
for qid, val, frag in out[:5]:
    check(False, f'reward-out-of-band: {qid} {val}B :: {frag}')
# Unbounded-promise scan: economy text may only mention "无限/永久免费" inside a negation.
UNBOUND = re.compile(r'无限|不限量|永久免费|任意取用|想拿多少')
NEG = re.compile(r'[不无非没禁勿拒免]')
promise_hits = []
def scan_promises(t, src):
    if not isinstance(t, str):
        return
    for m in UNBOUND.finditer(t):
        before = t[max(0, m.start() - 24):m.start()]
        if not NEG.search(before):
            promise_hits.append((src, t[max(0, m.start() - 16):m.end() + 16]))
for q in main + side + daily + dungeons:
    for k in ['premise', 'reward', 'deadline', 'state', 'failure', 'variants']:
        scan_promises(q.get(k), f"{q['id']}:{k}")
for q in model['quests']:
    for k in ['need', 'turn']:
        scan_promises(q.get(k), f"{q['id']}:{k}")
check(not promise_hits, 'no-unbounded-promises')
for src, frag in promise_hits[:5]:
    check(False, 'unbounded: ' + src + ' :: ' + frag)

doc = (V / '09_系统逻辑/时序与奖励总表.md').read_text(encoding='utf-8')
check('# 时序与奖励总表' in doc and '## 全局口径' in doc and '## 日常期限' in doc, 'doc-structure')
check('无隐藏全局倒计时' in doc and 'episode_state' in doc, 'doc-global-rules')
for group in ['main', 'side', 'daily', 'dungeon', 'city', 'continuation']:
    for q in reg[group]:
        check(q['id'] in doc, q['id'] + '-rendered')
check('覆盖：主线18、支线8、日常16、副本9、城市73、续篇6' in doc, 'doc-counts')
for name in ['系统逻辑索引', '经济与奖励', '任务台本总索引']:
    p = next(V.rglob(name + '.md'))
    check('TIMELINE-REGISTRY-S88:BEGIN' in p.read_text(encoding='utf-8'), name + '-s88-block')
h = read('research/timeline-generated-note-hashes.json')
check(set(h) == {'design/09_系统逻辑/时序与奖励总表.md'}, 'own-manifest-one-doc')
for rel, expected in h.items():
    check(sha(ROOT / rel) == expected, rel + '-generated-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = read('research/' + p.name)
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()):
        continue
    for rel, expected in m.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == expected, rel + '-all-manifests-reconciled')
check('TIMELINE-REGISTRY-S88:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block-present')
report = dict(date='2026-10-12', scope='S88 timeline and reward registry: coverage, freshness vs sources, explicit daily windows, entry prerequisites, one-time continuation and rendering; not economy calibration or runtime validation',
              main=len(reg['main']), side=len(reg['side']), daily=len(reg['daily']), dungeon=len(reg['dungeon']), city=len(reg['city']), continuation=len(reg['continuation']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/timeline-registry-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
