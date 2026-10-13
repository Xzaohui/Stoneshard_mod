"""S157: pilot implementation batch for the field layer (FX-QRY example).

Extracts one field NPC (with its four-state presence, visits, flow nodes), one
field document and one field sign, plus the ambient pool counts, and renders the
field-layer batch page. Planning only: nothing implemented.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PILOT-FX-S157'
CARD = '11_管理/试点实现批次FX野外层.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
fx = json.loads((R / 'field-npc-dialogue.json').read_text(encoding='utf-8'))['npcs']
npc = next(n for n in fx if n['id'] == 'FX-QRY')
flows = json.loads((R / 'field-scene-flows.json').read_text(encoding='utf-8'))['flows']
flow = next((f for f in flows if f.get('id') == 'FX-QRY' or f.get('npc') == 'FX-QRY'), flows[0])
docs = json.loads((R / 'field-docs.json').read_text(encoding='utf-8'))['docs']
signs = json.loads((R / 'field-signs.json').read_text(encoding='utf-8'))['signs']
doc = docs[0]
sign = signs[0]
pools = {}
for name in ('ambient-gossip', 'town-gossip', 'band-gossip'):
    d = json.loads((R / f'{name}.json').read_text(encoding='utf-8'))
    pools[name] = len(d.get('lines', []))
SCEN = [
    dict(id='FX-T01', name='存在性四态', steps=['以 present 接近该人物', '分别模拟 absent／dead／refused 后重访'],
         writes=[], invariants=['absent 只播代理句', 'dead/refused 停本人新句但保事前有限陈述', '不伪造新同意']),
    dict(id='FX-T02', name='条件回访', steps=['先做任务再回访', '或先回访再做任务'],
         writes=[], invariants=['已结案只追加新句', '顺序颠倒只重评未来', '不回滚旧结']),
    dict(id='FX-T03', name='文书只给信息', steps=['拾取并阅读该文书'],
         writes=[], invariants=['不推进任务、不发物品、不改结算', '原件/副件/残件分记']),
    dict(id='FX-T04', name='迹象判定', steps=['观察该迹象并按提示判断'],
         writes=[], invariants=['提示不含数值与掉落', '观察不改变实际生成与判定']),
    dict(id='FX-T05', name='闲谈三池', steps=['在地区／城镇／声望档三种语境下听闲谈'],
         writes=[], invariants=['三池互不克隆', '中间档不播档位池', '闲谈不改任何结算']),
]
batch = dict(date='2026-10-13',
             scope='S157 pilot batch field layer: one field NPC with four-state presence and visits, one document, one sign, ambient pool counts; planning only',
             npc=dict(id=npc['id'], role=npc.get('role'), site=npc.get('site'),
                      greetings=len(npc['greetings']), chats=len(npc['chats']), site_lines=len(npc['site_lines']),
                      visits={k: (len(v) if isinstance(v, list) else 'note') for k, v in npc['visits'].items()}),
             flow=dict(id=flow.get('id') or flow.get('npc'), nodes=[n.get('id') for n in flow.get('nodes', [])]),
             doc=dict(id=doc.get('id'), kind=doc.get('kind')),
             sign=dict(id=sign.get('id'), kind=sign.get('kind')),
             pools=pools,
             scenarios=[dict(id=s['id'], name=s['name'], steps=s['steps'], invariants=s['invariants']) for s in SCEN])
(R / 'pilot-batch-fx.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "试点实现批次FX野外层"\nid: MGMT-PILOT-FX-S157\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S157, guide, implementation]\naliases: []\n---\n\n'
     '# 试点实现批次FX野外层\n\n'
     '两批试点覆盖主章（N2）与城市系统（CS-BRY-01）；本页补**野外层**：以 `FX-QRY` 为例——存在性四态、条件回访、文书只给信息、迹象判定与三池闲谈。仅排程与输入提取，不含实现代码、不部署；数据 `research/pilot-batch-fx.json`。\n\n'
     '## 输入（现场提取）\n\n'
     f"- **野外人物** `{npc['id']}`（{npc.get('role') or '角色见登记'}，地点 `{npc.get('site')}`）：问候 {len(npc['greetings'])}、闲谈 {len(npc['chats'])}、地点句 {len(npc['site_lines'])}；"
     f"回访槽 {'、'.join(f'{k}={v}' for k, v in batch['npc']['visits'].items())}（`task` 为说明文本，其余为回访句数）。\n"
     f"- **条件流**：节点 {'、'.join('`' + x + '`' for x in batch['flow']['nodes']) or '见登记'}。\n"
     f"- **文书** `{doc.get('id')}`（{doc.get('kind')}）：阅读只给信息。\n"
     f"- **迹象** `{sign.get('id')}`（{sign.get('kind')}）：判定提示只写“看得出什么”。\n"
     f"- **闲谈三池**：地区 {pools['ambient-gossip']} 条／城镇 {pools['town-gossip']} 条／声望档 {pools['band-gossip']} 条。\n\n"
     '## 落地顺序\n\n'
     '1. **存在性**：四态（present／absent／dead／refused）先落地，缺席只播代理句；死亡/拒绝停本人新句。\n'
     '2. **台词接线**：问候／闲谈／地点句与回访槽按登记逐字接入；回访槽分 before／after／early／late／proxy。\n'
     '3. **文书与迹象**：文书阅读只给信息、不推进任务；迹象提示不含数值与掉落，观察不改生成与判定。\n'
     '4. **闲谈池**：三池分池播放，中间档不播档位池；闲谈不改任何结算。\n'
     '5. **验收**：见下节场景；运行记录按 [[试玩路线与检查单]]。\n\n'
     '## 验收场景\n\n| 场景 | 名称 | 不得发生 |\n| --- | --- | --- |\n')
for s in SCEN:
    n += f"| {s['id']} | {s['name']} | {'；'.join(s['invariants'])} |\n"
n += ('\n## 与另外两批的分工\n\n'
      '- N2：主章单案（键/桩/台词/回访）。\n'
      '- CS-BRY-01：城市系统（服务班／信任档／闲谈池）。\n'
      '- 本批：野外层（存在性四态／文书／迹象／三池）。三批合起来覆盖实现交接六步的全部接线类型。\n\n'
      '## 边界\n\n'
      '- 只选 `FX-QRY` 作样本；其余 35 名野外人物、11 份文书与 15 处迹象按同一模式铺开（数量见 [[特殊地点与野外NPC清点]]）。\n'
      '- 键名口径同 S155；前置同前两批（OI-02／OI-03）；经济、比例与触发距离仍待实机。\n'
      '- 本页**不含实现代码、不分配事件号、不写数值、不部署**。\n\n'
      '[[试点实现批次N2]] · [[试点实现批次CS-BRY-01]] · [[台本_FX_野外人物对白]] · [[文书_FX_野外地点短稿]] · [[野外迹象与观察]] · [[实现交接总表]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S157试点实现批次FX野外层（当前登记）\n\n[[试点实现批次FX野外层]]：以 `FX-QRY` 为例覆盖野外层——存在性四态、条件回访、文书只给信息、迹象判定与三池闲谈（{pools['ambient-gossip']}／{pools['town-gossip']}／{pools['band-gossip']} 条）；5 条验收场景。仅排程。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'pilot-fx-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted(R.glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- PILOT-FX-S157:BEGIN -->\n2026-10-13 S157：试点实现批次FX野外层。'
        f"以 FX-QRY 为例覆盖野外层（存在性四态/条件回访/文书只给信息/迹象判定/三池闲谈 {pools['ambient-gossip']}／{pools['town-gossip']}／{pools['band-gossip']} 条），5条验收场景；"
        '与 N2（主章）、CS-BRY-01（城市系统）合起来覆盖实现交接六步的全部接线类型；仅排程，不含实现代码、不部署。'
        '入口design/11_管理/试点实现批次FX野外层.md；运行Validate-PilotFx.py及既有检查。\n<!-- PILOT-FX-S157:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PILOT-FX-S157:BEGIN -->.*?<!-- PILOT-FX-S157:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PILOT-FX-S157:BEGIN -->.*?<!-- PILOT-FX-S157:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(npc=npc['id'], visits=batch['npc']['visits'], pools=pools, scenarios=len(SCEN)), ensure_ascii=False))
