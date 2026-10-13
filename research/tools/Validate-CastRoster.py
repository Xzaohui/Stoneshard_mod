"""Validate the global cast roster: unique identities, real cards, and every actor used
in dialogue or conditionally referenced in guards/exceptions (no silent dead weight)."""
from pathlib import Path
import json, re, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
m = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')

def aliases(a):
    out = {a['id'], a['id'].removeprefix('BRY-NPC-')}
    if a.get('name'):
        out.add(a['name'])
        out.add(a['name'].split('·')[0])
    return {x for x in out if len(x) >= 2}

used = {}
for cid, cast in m['dramatic_casts'].items():
    for key in cast:
        used[(cid, key)] = False
    for q in m['quests']:
        if q['city'] != cid:
            continue
        for s in q.get('dramatic_scenes', []):
            for who, _ in s.get('lines', []):
                if who in cast: used[(cid, who)] = True
            for _, _, _, w, _ in s.get('choices', []):
                if w in cast: used[(cid, w)] = True
        for pairs in q.get('dramatic_followups', {}).values():
            for w, _ in pairs:
                if w in cast: used[(cid, w)] = True
        for fb in q.get('dramatic_feedback', []):
            if fb['speaker'] in cast: used[(cid, fb['speaker'])] = True

refs = collections.defaultdict(set)
for cid, cast in m['dramatic_casts'].items():
    texts = []
    for q in m['quests']:
        if q['city'] != cid:
            continue
        for s in q.get('dramatic_scenes', []):
            texts += [s.get('basis', ''), s.get('setup', '')]
        texts.append(q.get('dramatic_stage_note', ''))
        texts += list(q.get('dramatic_guards', {}).values())
        texts += list(q.get('dramatic_exceptions', {}).values())
    blob = ' '.join(texts)
    for key, a in cast.items():
        if any(x in blob for x in aliases(a)):
            refs[(cid, key)].add('referenced')

unused = [(cid, key) for (cid, key), u in used.items() if not u and (cid, key) not in refs]
check(not unused, 'every-actor-used-or-conditionally-referenced')
for cid, key in unused[:8]:
    check(False, f'unused-actor: {cid}:{key}')
referenced_only = sorted(f"{cid}:{key}" for (cid, key) in refs if not used[(cid, key)])

ids = collections.Counter(); total = 0; new_cards = 0
for cid, cast in m['dramatic_casts'].items():
    check(len({a['id'] for a in cast.values()}) == len(cast), cid + '-unique-local-identities')
    for key, a in cast.items():
        total += 1; ids[a['id']] += 1
        if not a.get('existing'): new_cards += 1
        p = V / a['file']
        check(p.exists() and a['name'] in p.read_text(encoding='utf-8'), a['id'] + '-card-name')
        check(a.get('role') and a.get('voice'), a['id'] + '-role-and-voice')
dups = [i for i, c in ids.items() if c > 1]
unresolved = []
for d in dups:
    inst = [(cid, a) for cid, cast in m['dramatic_casts'].items() for a in cast.values() if a['id'] == d]
    files = {a['file'] for _, a in inst}
    cities = {cid for cid, _ in inst}
    declared = any(set(a.get('shared_cities', [])) >= cities for _, a in inst)
    if len(files) == 1 and declared and len(inst) == len(cities):
        check(True, 'shared-identity-declared: ' + d)
    else:
        unresolved.append(d)
check(not unresolved, 'actor-ids-unique-or-declared-shared')
for d in unresolved[:5]:
    check(False, 'duplicate-id: ' + d)
cont_ok = 0
for a in cont['actors']:
    keys = aliases(a); ok = False
    for q in cont['quests']:
        for s in q.get('scenes', []):
            for l in s.get('lines', []):
                if l['speaker'] in keys: ok = True
        for r in q.get('routes', []):
            if r['speaker'] in keys: ok = True
    for e in cont['effects']:
        if any(x in e['receiver'] for x in keys): ok = True
    check(ok, a['id'] + '-continuation-used')
    p = V / a['file']
    check(p.exists() and a['name'] in p.read_text(encoding='utf-8'), a['id'] + '-card-name')
    cont_ok += 1
check(cont_ok == len(cont['actors']) == 7, 'seven-continuation-actors')

# Effect receivers must resolve to a named person, a declared generic, or a role noun
# present in the target's own corpus (its city drama/cast/quest text, or the story task).
name_set = set()
for cid, cast in m['dramatic_casts'].items():
    for a in cast.values():
        name_set.add(a['name']); name_set.add(a['name'].split('·')[0])
for c in m['cities']:
    for name, role, arc, pid in c['people']: name_set.add(name)
    for s in c['satellites']:
        name_set.add(s['resident']['name'])
story_blob = {}
for f in ['story-main.json', 'story-main-late.json', 'story-side.json', 'story-daily.json', 'story-dungeon.json']:
    d = read('research/' + f)
    for q in d:
        story_blob[q['id']] = json.dumps(q, ensure_ascii=False)
        for s in q.get('scenes', []):
            for item in s.get('lines', []):
                if isinstance(item, list) and len(item) == 2: name_set.add(item[0])
city_blob = {}
for c in m['cities']:
    cid = c['id']; parts = [json.dumps(c, ensure_ascii=False)]
    for a in m['dramatic_casts'].get(cid, {}).values(): parts.append(a.get('role', ''))
    for q in m['quests']:
        if q['city'] == cid: parts.append(json.dumps(q, ensure_ascii=False))
    city_blob[cid] = ' '.join(parts)
GENERIC = {'旧台本当事人'}
unresolved = []
for e in m['effects']:
    recv = e['receiver']; target = e['target']
    if recv in GENERIC:
        continue
    if any(n in recv or recv in n for n in name_set if len(n) >= 2):
        continue
    parts = target.split('-')
    tcity = parts[1] if len(parts) >= 2 and parts[0] in ('CM', 'CS') else None
    blob = city_blob.get(tcity, '') if tcity else story_blob.get(target, '')
    core = re.sub(r'^(?:地方|本案|本段|原)', '', recv)
    if recv and (recv in blob or core in blob):
        continue
    unresolved.append((e['id'], recv, target))
check(not unresolved, 'effect-receivers-resolve')
for eid, recv, target in unresolved[:8]:
    check(False, f'unresolved-receiver: {eid} {recv} -> {target}')
report = dict(date='2026-10-12', scope='global cast roster: unique identities, real cards, dialogue usage or conditional reference; not literary quality or runtime validation',
              city_actors=total, new_cards=new_cards, referenced_only=referenced_only, continuation_actors=cont_ok,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/cast-roster-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
