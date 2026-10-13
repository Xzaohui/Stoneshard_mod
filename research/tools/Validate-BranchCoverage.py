"""Validate the S103 branch-coverage audit by recomputing from the sources."""
from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
def keys_of(v):
    out = []
    for x in v or []:
        out.append(x.get('key') if isinstance(x, dict) and 'key' in x else (x if isinstance(x, str) else x.get('id', '')))
    return [k for k in out if k]
bc = read('research/branch-coverage.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
expect = {}
for q in model['quests']:
    routes = keys_of(q.get('routes'))
    ok = (len(routes) >= 2 and set((q.get('dramatic_followups') or {}).keys()) == set(routes)
          and len(q.get('dramatic_feedback') or []) >= 1 and len(q.get('dramatic_exceptions') or []) >= 1
          and len(q.get('dramatic_guards') or []) >= 1)
    expect[q['id']] = ('city', ok)
for q in cont['quests']:
    ok = len(keys_of(q.get('routes'))) >= 2 and bool(q.get('scenes')) and bool(q.get('interruption')) and bool(q.get('reward_owner'))
    expect[q['id']] = ('continuation', ok)
for name, fam in [('story-main.json', 'main'), ('story-side.json', 'side'), ('story-main-late.json', 'main-late'), ('story-dungeon.json', 'dungeon')]:
    for x in read('research/' + name):
        ok = len(x.get('choices') or []) >= 2 and bool(x.get('scenes')) and bool(x.get('recovery'))
        expect[x['id']] = (fam, ok)
for x in read('research/story-daily.json'):
    ok = all(bool(x.get(k)) for k in ('opening', 'field', 'closing', 'failure', 'variants', 'player_mid', 'player_close'))
    expect[x['id']] = ('daily', ok)
rows = {r['id']: r for r in bc['rows']}
check(set(rows) == set(expect), 'row-ids-match-sources')
check(len(bc['rows']) == 130, 'row-count-130')
check(bc['families'] == {'city': 73, 'continuation': 6, 'main': 9, 'side': 8, 'main-late': 9, 'dungeon': 9, 'daily': 16}, 'family-counts')
check(bc['gaps'] == [], 'no-gaps')
for rid, (fam, ok) in expect.items():
    r = rows.get(rid)
    check(r is not None and r['family'] == fam, rid + '-family')
    check(r is not None and r['ok'] == ok, rid + '-flag')
    if r and fam == 'city':
        q = next(q for q in model['quests'] if q['id'] == rid)
        check(r['routes'] == len(keys_of(q.get('routes'))), rid + '-routes')
        check(r['followups'] == len(q.get('dramatic_followups') or {}), rid + '-followups')
        check(r['feedback'] == len(q.get('dramatic_feedback') or []), rid + '-feedback')
card = (V / '11_管理/对白分支覆盖审计.md').read_text(encoding='utf-8')
check('# 对白分支覆盖审计' in card and '## 边界' in card and '## 口径' in card, 'card-structure')
check('共 130 个脚本' in card and '不合口径：无' in card, 'card-summary')
for fam, cnt in bc['families'].items():
    check(f"| {fam}（{cnt}） |" in card, 'card-row-' + fam)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('BRANCH-COVERAGE-S103:BEGIN' in plan and '[[对白分支覆盖审计]]' in plan, 'plan-block-and-link')
check('BRANCH-COVERAGE-S103:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/branch-coverage-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S103 branch coverage: recomputed per-script flags, family counts, rendering and chain; structure only, not literary quality or runtime',
              rows=len(bc['rows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/branch-coverage-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
