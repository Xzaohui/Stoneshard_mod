"""Validate the S113 corpus flow projection by recomputing every ref from sources."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
cf = read('research/corpus-flows.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
check(len(cf['flows']) == 130, 'flow-count-130')
check(cf['families'] == {'city': 73, 'continuation': 6, 'main': 9, 'side': 8, 'main-late': 9, 'dungeon': 9, 'daily': 16}, 'family-counts')
# --- city ---
city = {q['id']: q for q in model['quests']}
for f in [x for x in cf['flows'] if x['family'] == 'city']:
    q = city[f['id']]
    routes = [r['key'] for r in q.get('routes') or []]
    node_ids = [nd['id'] for nd in f['nodes']]
    for key in routes: check(f'route.{key}' in node_ids, f['id'] + '-route-node-' + key)
    if (q.get('dramatic_exceptions') or {}).get('refusal'): check('refusal' in node_ids, f['id'] + '-refusal-node')
    if (q.get('dramatic_exceptions') or {}).get('dead'): check('absent' in node_ids, f['id'] + '-absent-node')
    for nd in f['nodes']:
        for rid, text in nd['refs']:
            m = re.fullmatch(r'scene\.(\d+)\.line\.(\d+)', rid)
            if m:
                t = q['dramatic_scenes'][int(m.group(1)) - 1]['lines'][int(m.group(2)) - 1][1]
                check(t == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'scene\.(\d+)\.choice\.(\w+)\.ans', rid)
            if m:
                sc = q['dramatic_scenes'][int(m.group(1)) - 1]
                c = next(x for x in sc['choices'] if x[0] == m.group(2))
                check(c[4] == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'route\.(\w+)\.line', rid)
            if m:
                r = next(x for x in q['routes'] if x['key'] == m.group(1))
                check(r.get('line', '') == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'followup\.(\w+)\.(\d+)', rid)
            if m:
                t = q['dramatic_followups'][m.group(1)][int(m.group(2)) - 1][1]
                check(t == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'feedback\.(\d+)\.(early|late)', rid)
            if m:
                fb = q['dramatic_feedback'][int(m.group(1)) - 1]
                check(fb[m.group(2) + '_line'] == text, f['id'] + '-ref-' + rid); continue
            check(False, f['id'] + '-ref-unknown-' + rid)
# --- continuation ---
cby = {q['id']: q for q in cont['quests']}
eff = {}
for e in cont['effects']: eff[e['id']] = e
for f in [x for x in cf['flows'] if x['family'] == 'continuation']:
    q = cby[f['id']]
    node_ids = [nd['id'] for nd in f['nodes']]
    for key in [r['key'] for r in q.get('routes') or []]:
        check(f'route.{key}' in node_ids, f['id'] + '-route-node-' + key)
    if q.get('interruption'): check('refusal' in node_ids, f['id'] + '-refusal-node')
    for nd in f['nodes']:
        for rid, text in nd['refs']:
            m = re.fullmatch(r'scene\.(\d+)\.line\.(\d+)', rid)
            if m:
                t = q['scenes'][int(m.group(1)) - 1]['lines'][int(m.group(2)) - 1]['text']
                check(t == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'scene\.(\d+)\.choice\.(\w+)\.ans', rid)
            if m:
                sc = q['scenes'][int(m.group(1)) - 1]
                spans = []
                for c in sc.get('choices') or []:
                    if isinstance(c, str):
                        mm = re.search(r'‘([^’]+)’|“([^”]+)”', c)
                        if mm: spans.append(mm.group(1) or mm.group(2))
                check(text in spans, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'route\.(\w+)\.line', rid)
            if m:
                r = next(x for x in q['routes'] if x['key'] == m.group(1))
                check(r.get('line', '') == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'effect\.(BC85-\d+)\.(\w+)\.(early|late)', rid)
            if m:
                check(eff[m.group(1)]['route_dialogue'][m.group(2)][m.group(3)] == text, f['id'] + '-ref-' + rid); continue
            m = re.fullmatch(r'effect\.(BC85-\d+)\.missing', rid)
            if m:
                check(eff[m.group(1)]['missing'] == text, f['id'] + '-ref-' + rid); continue
            check(False, f['id'] + '-ref-unknown-' + rid)
# --- story ---
for name, fam in [('story-main.json', 'main'), ('story-side.json', 'side'), ('story-main-late.json', 'main-late'), ('story-dungeon.json', 'dungeon')]:
    src = {x['id']: x for x in read('research/' + name)}
    for f in [x for x in cf['flows'] if x['family'] == fam]:
        x = src[f['id']]
        node_ids = [nd['id'] for nd in f['nodes']]
        for c in x.get('choices') or []:
            check(f'choice.{c[0]}' in node_ids, f['id'] + '-choice-node-' + c[0])
        if x.get('recovery'): check('refusal' in node_ids, f['id'] + '-refusal-node')
        for nd in f['nodes']:
            for rid, text in nd['refs']:
                m = re.fullmatch(r'scene\.(\d+)\.line\.(\d+)', rid)
                check(bool(m), f['id'] + '-ref-unknown-' + rid)
                if m:
                    t = x['scenes'][int(m.group(1)) - 1]['lines'][int(m.group(2)) - 1][1]
                    check(t == text, f['id'] + '-ref-' + rid)
# --- daily ---
dail = {x['id']: x for x in read('research/story-daily.json')}
for f in [x for x in cf['flows'] if x['family'] == 'daily']:
    x = dail[f['id']]
    node_ids = [nd['id'] for nd in f['nodes']]
    check({'entry', 'hub', 'close'} <= set(node_ids), f['id'] + '-daily-nodes')
    if x.get('failure'): check('refusal' in node_ids, f['id'] + '-refusal-node')
    for nd in f['nodes']:
        for rid, text in nd['refs']:
            m = re.fullmatch(r'(opening|field|closing)\.(\d+)', rid)
            check(bool(m), f['id'] + '-ref-unknown-' + rid)
            if m:
                spans = re.findall(r'‘([^’]{6,})’', x[m.group(1)])
                check(text in spans, f['id'] + '-ref-' + rid)
# --- global ---
keys = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items(): keys.add(k); walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(cf)
check(not [k for k in keys if k in ('reward', 'rewards', 'requires', 'paid', 'price', 'gold')], 'no-reward-keys')
card = (V / '11_管理/全库条件流投影.md').read_text(encoding='utf-8')
check('# 全库条件流投影' in card and '## 边界' in card and '共 130 个脚本' in card, 'card-structure')
for fam, cnt in cf['families'].items():
    check(f"| {fam} | {cnt} |" in card, 'card-row-' + fam)
for sid in ['CS-BRY-01', 'N1', 'CS-BRY-11', 'DT01']:
    check(f"### {sid}（" in card, 'card-sample-' + sid)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('CORPUS-FLOWS-S113:BEGIN' in plan and '[[全库条件流投影]]' in plan, 'plan-block-and-link')
check('CORPUS-FLOWS-S113:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/corpus-flows-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S113 corpus flows: recomputed refs against sources, route/choice/refusal/absence node coverage, no reward keys, rendering and chain; projection only, not engine events',
              flows=len(cf['flows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/corpus-flows-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
