"""S113: project every script family into an implementation-ready condition graph.

Deterministic projection of city quests, Brynn continuation, story main/side/
late/dungeon and daily scripts into nodes with a fixed condition vocabulary;
refs point back to the exact source strings, notes carry guard prose.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'CORPUS-FLOWS-S113'
CARD = '11_管理/全库条件流投影.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
flows = []
# ---- city quests ----
for q in model['quests']:
    nodes = []
    scenes = q.get('dramatic_scenes') or []
    if scenes:
        first = scenes[0]
        refs = [[f'scene.1.line.{i}', t] for i, (_, t) in enumerate(first.get('lines') or [], 1)]
        for c in first.get('choices') or []:
            refs.append([f'scene.1.choice.{c[0]}.ans', c[4]])
        nodes.append(dict(id='entry', when='first_meet', refs=refs, notes=[]))
    hub_refs = []
    for si, sc in enumerate(scenes[1:], 2):
        hub_refs += [[f'scene.{si}.line.{i}', t] for i, (_, t) in enumerate(sc.get('lines') or [], 1)]
    nodes.append(dict(id='hub', when='any', refs=hub_refs, notes=[]))
    for r in q.get('routes') or []:
        key = r['key']
        refs = [[f'route.{key}.line', r.get('line', '')]]
        for i, (_, t) in enumerate((q.get('dramatic_followups') or {}).get(key, []), 1):
            refs.append([f'followup.{key}.{i}', t])
        nodes.append(dict(id=f'route.{key}', when=f'route({key})', refs=refs,
                          notes=[[f'route.{key}.action', r.get('action', '')], [f'route.{key}.cost', r.get('cost', '')],
                                 [f'route.{key}.result', r.get('result', '')]]))
    for i, fb in enumerate(q.get('dramatic_feedback') or [], 1):
        nodes.append(dict(id=f'feedback.{i}.early', when='task_done', refs=[[f'feedback.{i}.early', fb['early_line']]], notes=[[f'feedback.{i}.fact', fb['known_fact']]]))
        nodes.append(dict(id=f'feedback.{i}.late', when='order_late', refs=[[f'feedback.{i}.late', fb['late_line']]], notes=[[f'feedback.{i}.scope', fb.get('late_scope', '')]]))
    ex = q.get('dramatic_exceptions') or {}
    if ex.get('refusal'):
        nodes.append(dict(id='refusal', when='refused', refs=[], notes=[['exception.refusal', ex['refusal']]]))
    if ex.get('dead'):
        nodes.append(dict(id='absent', when='npc_absent', refs=[], notes=[['exception.dead', ex['dead']]]))
    if ex.get('before_city'):
        nodes.append(dict(id='before_city', when='order_early', refs=[], notes=[['exception.before_city', ex['before_city']]]))
    if ex.get('after_city'):
        nodes.append(dict(id='after_city', when='order_late', refs=[], notes=[['exception.after_city', ex['after_city']]]))
    guards = [v for v in (q.get('dramatic_guards') or {}).values()]
    flows.append(dict(id=q['id'], family='city', source='research/city-campaign.json', nodes=nodes, guards=guards))
# ---- continuation ----
effects_by_source = {}
for e in cont['effects']:
    effects_by_source.setdefault(e['source'], []).append(e)
for q in cont['quests']:
    nodes = []
    scenes = q.get('scenes') or []
    if scenes:
        refs = [[f'scene.1.line.{i}', ln['text']] for i, ln in enumerate(scenes[0].get('lines') or [], 1)]
        for ci, c in enumerate(scenes[0].get('choices') or [], 1):
            if isinstance(c, str):
                m = re.search(r'‘([^’]+)’|“([^”]+)”', c)
                if m: refs.append([f'scene.1.choice.{ci}.ans', m.group(1) or m.group(2)])
            else:
                refs.append([f'scene.1.choice.{c[0]}.ans', c[4]])
        nodes.append(dict(id='entry', when='first_meet', refs=refs, notes=[]))
    hub_refs = []
    for si, sc in enumerate(scenes[1:], 2):
        hub_refs += [[f'scene.{si}.line.{i}', ln['text']] for i, ln in enumerate(sc.get('lines') or [], 1)]
    nodes.append(dict(id='hub', when='any', refs=hub_refs, notes=[]))
    for r in q.get('routes') or []:
        key = r['key']
        nodes.append(dict(id=f'route.{key}', when=f'route({key})',
                          refs=[[f'route.{key}.line', r.get('line', '')]],
                          notes=[[f'route.{key}.action', r.get('action', '')], [f'route.{key}.cost', r.get('cost', '')], [f'route.{key}.result', r.get('result', '')]]))
    for e in effects_by_source.get(q['id'], []):
        refs = []
        for key, d in (e.get('route_dialogue') or {}).items():
            if d.get('early'): refs.append([f'effect.{e["id"]}.{key}.early', d['early']])
            if d.get('late'): refs.append([f'effect.{e["id"]}.{key}.late', d['late']])
        if e.get('missing'): refs.append([f'effect.{e["id"]}.missing', e['missing']])
        nodes.append(dict(id=f'effect.{e["id"]}', when='task_done', refs=refs,
                          notes=[[f'effect.{e["id"]}.routes', '；'.join(f'{k}：{v}' for k, v in (e.get('routes') or {}).items())]]))
    if q.get('interruption'):
        nodes.append(dict(id='refusal', when='refused', refs=[], notes=[['interruption', q['interruption']]]))
    flows.append(dict(id=q['id'], family='continuation', source='research/brynn-continuation.json', nodes=nodes,
                      guards=[q.get('hook', ''), f"奖励所有者：{q.get('reward_owner', '')}"]))
# ---- story families ----
for name, fam in [('story-main.json', 'main'), ('story-side.json', 'side'), ('story-main-late.json', 'main-late'), ('story-dungeon.json', 'dungeon')]:
    for x in read('research/' + name):
        nodes = []
        scenes = x.get('scenes') or []
        if scenes:
            first = scenes[0]
            refs = [[f'scene.1.line.{i}', t] for i, (_, t) in enumerate(first.get('lines') or [], 1)]
            nodes.append(dict(id='entry', when='first_meet', refs=refs, notes=[]))
        hub_refs = []
        for si, sc in enumerate(scenes[1:], 2):
            hub_refs += [[f'scene.{si}.line.{i}', t] for i, (_, t) in enumerate(sc.get('lines') or [], 1)]
        nodes.append(dict(id='hub', when='any', refs=hub_refs, notes=[]))
        for c in x.get('choices') or []:
            nodes.append(dict(id=f'choice.{c[0]}', when=f'route({c[0]})', refs=[],
                              notes=[[f'choice.{c[0]}.label', c[1]], [f'choice.{c[0]}.outcome', c[2]]]))
        if x.get('recovery'):
            nodes.append(dict(id='refusal', when='refused', refs=[], notes=[['recovery', x['recovery']]]))
        notes = [[k, x[k]] for k in ('outcome', 'evidence') if x.get(k)]
        flows.append(dict(id=x['id'], family=fam, source='research/' + name, nodes=nodes,
                          guards=[x.get('premise', '')] + [n[1] for n in notes]))
# ---- daily ----
for x in read('research/story-daily.json'):
    nodes = []
    for fld, when, nid in [('opening', 'first_meet', 'entry'), ('field', 'any', 'hub'), ('closing', 'task_done', 'close')]:
        v = x.get(fld) or ''
        refs = [[f'{fld}.{i}', m.group(1)] for i, m in enumerate(re.finditer(r'‘([^’]{6,})’', v), 1)]
        nodes.append(dict(id=nid, when=when, refs=refs, notes=[]))
    if x.get('failure'):
        nodes.append(dict(id='refusal', when='refused', refs=[], notes=[['failure', x['failure']]]))
    notes = [[k, x[k]] for k in ('variants', 'player_mid', 'player_close', 'state') if x.get(k)]
    flows.append(dict(id=x['id'], family='daily', source='research/story-daily.json', nodes=nodes,
                      guards=[n[1] for n in notes]))
fam_counts = {}
for f in flows: fam_counts[f['family']] = fam_counts.get(f['family'], 0) + 1
out = dict(date='2026-10-13', scope='S113 corpus flow projection: fixed condition vocabulary, per-script node graphs, refs to source strings and guard notes; projection only, no new lines or rewards',
           vocabulary=['first_meet', 'any', 'task_done', 'order_early', 'order_late', 'refused', 'npc_absent', 'route(<key>)'],
           families=fam_counts, flows=flows)
(ROOT / 'research' / 'corpus-flows.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "全库条件流投影"\nid: SYS-CORPUS-FLOWS-S113\ntype: system\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S113, system]\naliases: []\n---\n\n'
     '# 全库条件流投影\n\n'
     '把全库台本投影成实现可用的条件图：城市支线、布林续篇、主线/支线/后章/副本与日常，共 '
     f"{len(flows)} 个脚本。节点只用固定条件词表；`refs` 逐条回指源文件里的原句（投影不新写台词），`notes` 载守卫、例外与代价等设计散文。"
     '机器可读数据在 `research/corpus-flows.json`。\n\n'
     '**条件词表**：' + '、'.join('`' + w + '`' for w in out['vocabulary']) + '。\n\n'
     '| 族 | 脚本数 | 节点数 | 引用数 | 守卫/注记数 |\n|---|---:|---:|---:|---:|\n')
for fam in ['city', 'continuation', 'main', 'side', 'main-late', 'dungeon', 'daily']:
    sub = [f for f in flows if f['family'] == fam]
    n += (f"| {fam} | {len(sub)} | {sum(len(f['nodes']) for f in sub)} | "
          f"{sum(len(r) for f in sub for nd in f['nodes'] for r in nd['refs'])} | "
          f"{sum(len(nd['notes']) for f in sub for nd in f['nodes']) + sum(len(f['guards']) for f in sub)} |\n")
n += '\n## 节点模板\n\n'
n += ('- **city**：`entry`（首场台词与选项答案）→ `hub`（其余场次台词）→ 每路线 `route.<key>`（路线台词与逐路线回访）'
      '→ `feedback.N.early/late`（早/晚回执）→ `refusal`/`absent`/`before_city`/`after_city`（例外与先后）。\n'
      '- **continuation**：`entry`/`hub` → `route.<key>` → `effect.<BC85-NN>`（续篇桥的早/晚/缺席台词）。\n'
      '- **main/side/main-late/dungeon**：`entry`/`hub` → `choice.<key>`（选项标签与结果）→ `refusal`（恢复路径）。\n'
      '- **daily**：`entry`（开场引句）/`hub`（现场引句）/`close`（收束引句）→ `refusal`（失败口径）。\n\n')
n += '## 代表脚本\n\n'
for sid in ['CS-BRY-01', 'N1', 'CS-BRY-11', 'DT01']:
    f = next((x for x in flows if x['id'] == sid), None)
    if not f: continue
    n += f"### {sid}（{f['family']}）\n\n| 节点 | 条件 | 引用/注记 |\n|---|---|---|\n"
    for nd in f['nodes']:
        items = '、'.join('`' + r[0] + '`' for r in nd['refs']) or '、'.join('`' + k[0] + '`' for k in nd['notes'])
        n += f"| `{nd['id']}` | `{nd['when']}` | {items} |\n"
    n += '\n'
n += ('## 口径\n\n- 投影只读源文件：refs 的文本必须与源逐字一致，任何不一致由校验器拦下。\n'
      '- 节点不含奖励、库存或结算字段；结算仍归各台本唯一所有者。\n'
      '- 缺席/拒绝/先后节点按源提供的内容生成；源没有就不生成，不虚构出口。\n\n'
      '## 边界\n\n- 本页是实现用的条件图，不是引擎事件；触发距离、作息与生成点见[[特殊地点阶段制作与校准规程]]。\n'
      '- 投影不评文学质量、不改变任何台本内容；源改则重跑本工具。\n\n'
      '[[特殊地点与野外NPC阶段验收记录]] · [[对白分支覆盖审计]] · [[野外对白条件流]] · [[任务台本总索引]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S113全库条件流投影（当前登记）\n\n'
           f"[[全库条件流投影]]：把 {len(flows)} 个脚本（城市{len(model['quests'])}、续篇{len(cont['quests'])}、主线/支线/后章/副本、日常）投影成实现用条件图（固定词表、refs 回指原句、notes 载守卫与例外）；"
           '机器可读数据 research/corpus-flows.json。不新写台词、不含奖励字段。')
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/corpus-flows-note-hashes.json'
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
rule = ('\n<!-- CORPUS-FLOWS-S113:BEGIN -->\n2026-10-13 S113：全库条件流投影（实现桥）。'
        f'research/corpus-flows.json 把 {len(flows)} 个脚本（城市73/续篇6/主线·支线·后章·副本/日常16）投影成固定词表条件图，refs 逐条回指源原句、notes 载守卫与例外；入口design/11_管理/全库条件流投影.md。'
        '投影不新写台词、不含奖励/结算字段、不改台本；运行Validate-CorpusFlows.py及既有检查；引擎触发与部署仍待实现阶段。\n<!-- CORPUS-FLOWS-S113:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- CORPUS-FLOWS-S113:BEGIN -->.*?<!-- CORPUS-FLOWS-S113:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- CORPUS-FLOWS-S113:BEGIN -->.*?<!-- CORPUS-FLOWS-S113:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/全库条件流投影.md', '入口 [全库条件流投影](design/11_管理/全库条件流投影.md)'), encoding='utf-8')
print(json.dumps(dict(flows=len(flows), families=fam_counts), ensure_ascii=False))
