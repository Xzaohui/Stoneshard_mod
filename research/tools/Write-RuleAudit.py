"""S109: consolidated rule-consistency audit over the new field-content registries.

Recomputes, from the sources, that the stage's content obeys the standing rules:
no rewards, no full-walk prerequisites, no repeatable daily tasks, refusal and
absence exits present, knowledge limits stated, bilingual parity, no services added.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'RULE-AUDIT-S109'
CARD = '11_管理/野外内容规则一致性审计.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json')
sg = read('research/field-signs.json'); fl = read('research/field-scene-flows.json')
inv = read('research/special-location-inventory.json')
rows = []
def add(rule, scope, ok, detail=''):
    rows.append(dict(rule=rule, scope=scope, ok=ok, detail=detail))
# 1 no rewards / no prerequisites / no repeatable tasks anywhere in the registries
BANNED = ('reward', 'rewards', 'requires', 'repeatable', 'cooldown', 'deadline', 'paid', 'price', 'gold', 'coin_amount')
for name, data in [('field-npc-dialogue', fx), ('field-docs', fd), ('field-signs', sg), ('field-scene-flows', fl)]:
    keys = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items(): keys.add(k); walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(data)
    bad = sorted(k for k in keys if k in BANNED)
    add('无奖励/无前置/无重复任务字段', name, not bad, ','.join(bad))
# 2 refusal + absence exits and knowledge limits per NPC
no_refusal = [n['id'] for n in fx['npcs'] if not n['site_lines'][2][1]]
no_proxy = [n['id'] for n in fx['npcs'] if not n['visits']['proxy']]
thin_knowledge = [n['id'] for n in fx['npcs'] if len(n['knows']) < 2 or len(n['not_knows']) < 2]
add('拒绝出口齐备', 'field-npc-dialogue', not no_refusal, ','.join(no_refusal))
add('缺席替代齐备', 'field-npc-dialogue', not no_proxy, ','.join(no_proxy))
add('知情边界至少各两条', 'field-npc-dialogue', not thin_knowledge, ','.join(thin_knowledge))
# 3 bilingual parity
miss_en = []
for n in fx['npcs']:
    en = n.get('english') or {}
    if len(en) != 14 or any(not v.strip() for v in en.values()): miss_en.append(n['id'])
add('中英逐槽对齐（14/人）', 'field-npc-dialogue', not miss_en, ','.join(miss_en))
doc_miss = [d['id'] for d in fd['docs'] if not (d.get('title_en') and d.get('text_en') and d.get('read_en'))]
sign_miss = [s['id'] for s in sg['signs'] if not (s.get('title_en') and s.get('obs_en') and s.get('judge_en') and s.get('danger_en'))]
add('文书中英齐备', 'field-docs', not doc_miss, ','.join(doc_miss))
add('迹象中英齐备', 'field-signs', not sign_miss, ','.join(sign_miss))
# 4 flows: required states, proxy speaker, no reward keys
flow_bad = []
for f in fl['flows']:
    whens = {nd['when'] for nd in f['nodes']}
    if not {'refused', 'npc_absent', 'task_open', 'task_done'} <= whens: flow_bad.append(f['npc'])
    if not any(nd.get('speaker') == 'proxy' for nd in f['nodes']): flow_bad.append(f['npc'] + ':proxy')
add('条件流必备状态与缺席说话人', 'field-scene-flows', not flow_bad, ','.join(flow_bad))
# 5 services not added: region cards' service fields must deny a counter
cards = sorted((V / '02_世界与地图/特殊地点与野外NPC').glob('地点设计卡_*.md'))
svc_bad = []
for p in cards:
    t = p.read_text(encoding='utf-8')
    m = re.search(r'\*\*服务\*\*：([^\n]+)', t)
    if not m or not ('无固定服务' in m.group(1) or '不设' in m.group(1) or '不新增' in m.group(1)): svc_bad.append(p.stem)
add('六张地点卡均声明不新增服务', 'site-cards', not svc_bad, ','.join(svc_bad))
# 6 site coverage: every site has a person or a sign
have = {n['site'] for n in fx['npcs']} | {s['site'] for s in sg['signs']}
missing = sorted({r['key'] for r in inv['rumor_sites']} - have)
add('44 地点全部有落点', 'inventory+registries', not missing, ','.join(missing))
# 7 every NPC's card and aggregate exist (spot: count)
add('人物卡数量与登记一致', 'field-npc-dialogue', len(list((V / '04_人物/野外人物').glob('*.md'))) == len(fx['npcs']))
out = dict(date='2026-10-13', scope='S109 rule-consistency audit: recomputed from the field registries and site cards; structure and rule compliance only, not runtime or literary quality',
           rows=rows, failed=[r for r in rows if not r['ok']])
(ROOT / 'research' / 'rule-audit.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "野外内容规则一致性审计"\nid: MGMT-RULE-AUDIT-S109\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S109, review]\naliases: []\n---\n\n'
     '# 野外内容规则一致性审计\n\n'
     '按 S62 与各台本顶部规则，对新阶段四个登记文件与六张地点卡做一致性重算：无奖励/无前置/无重复任务字段、拒绝与缺席出口、知情边界、中英对齐、服务不新增、44 地点落点。'
     '本页只验规则与结构，不评文学质量、不证明运行。\n\n| 规则 | 范围 | 结果 | 说明 |\n|---|---|---|---|\n')
for r in rows:
    n += f"| {r['rule']} | {r['scope']} | {'通过' if r['ok'] else '不合'} | {r['detail'] or '—'} |\n"
n += f"\n共 {len(rows)} 项，不合口径：{'无' if not out['failed'] else '、'.join(r['rule'] for r in out['failed'])}。\n\n"
n += ('## 口径\n\n- “无奖励字段”指四个登记文件里没有 reward/requires/repeatable/cooldown/price 等键；野外内容只给信息与口信。\n'
      '- “缺席替代”要求每人有 proxy 节点与 proxy 台词；“拒绝出口”要求每人有拒绝句且条件流含 refused 状态。\n'
      '- “服务不新增”逐卡核对服务栏必须声明无固定服务或等义措辞。\n\n'
      '## 边界\n\n- 重算只覆盖登记文件与地点卡；运行表现、数值与生成点不在本审计范围（见[[特殊地点阶段制作与校准规程]]）。\n'
      '- 审计通过不等于内容可用；文学、节奏与实机表现仍需人工与运行验证。\n\n'
      '[[特殊地点与野外NPC阶段验收记录]] · [[台本_FX_野外人物对白]] · [[文书_FX_野外地点短稿]] · [[野外迹象与观察]] · [[野外对白条件流]] · [[逻辑验收记录]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S109规则一致性审计（当前登记）\n\n'
           f"[[野外内容规则一致性审计]]：对四个登记文件与六张地点卡重算 {len(rows)} 项规则（无奖励/无前置/无重复任务、拒绝与缺席出口、知情边界、中英对齐、服务不新增、44地点落点），不合口径：{'无' if not out['failed'] else '、'.join(r['rule'] for r in out['failed'])}。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/rule-audit-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- RULE-AUDIT-S109:BEGIN -->\n2026-10-13 S109：野外内容规则一致性审计。'
        f'research/rule-audit.json 重算 {len(rows)} 项（无奖励/前置/重复任务字段、拒绝与缺席出口、知情边界、中英对齐、服务不新增、44地点落点），入口design/11_管理/野外内容规则一致性审计.md。'
        '只验规则与结构；运行、数值与生成点见制作规程。运行Validate-RuleAudit.py及既有检查；不部署游戏包。\n<!-- RULE-AUDIT-S109:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- RULE-AUDIT-S109:BEGIN -->.*?<!-- RULE-AUDIT-S109:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- RULE-AUDIT-S109:BEGIN -->.*?<!-- RULE-AUDIT-S109:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/野外内容规则一致性审计.md', '入口 [野外内容规则一致性审计](design/11_管理/野外内容规则一致性审计.md)'), encoding='utf-8')
print(json.dumps(dict(rows=len(rows), failed=[r['rule'] for r in out['failed']]), ensure_ascii=False))
