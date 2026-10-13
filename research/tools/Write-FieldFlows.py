"""S105: render machine-readable condition flows for the 28 field NPCs.

Deterministic projection of research/field-npc-dialogue.json into an
implementation-ready node graph: entry states, task gates, order branches,
refusal and absence paths, with line references resolved back to the registry.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FIELD-FLOWS-S105'
CARD = '02_世界与地图/特殊地点与野外NPC/野外对白条件流.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
fx = json.loads((ROOT / 'research/field-npc-dialogue.json').read_text(encoding='utf-8'))
flows = []
for n in fx['npcs']:
    v = n['visits']
    ref = {
     'greeting.first': n['greetings'][0][1], 'greeting.revisit': n['greetings'][1][1], 'greeting.night': n['greetings'][2][1],
     'site.arrival': n['site_lines'][0][1], 'site.warning': n['site_lines'][1][1], 'site.refusal': n['site_lines'][2][1],
     'visit.before': v['before'][0], 'visit.after': v['after'][0], 'visit.early': v['early'][0],
     'visit.late': v['late'][0], 'visit.proxy': v['proxy'][0],
    }
    for i, c in enumerate(n['chats'], 1): ref[f'chat.{i}'] = c
    nodes = [
     dict(id='intro', when='first_meet', lines=['greeting.first'], next='hub'),
     dict(id='night', when='night', lines=['greeting.night'], next='hub'),
     dict(id='hub', when='any', lines=['greeting.revisit'], next='hub'),
     dict(id='before', when='task_open', lines=['visit.before'], next='hub'),
     dict(id='after', when='task_done', lines=['visit.after'], next='hub'),
     dict(id='early', when='order_early', lines=['visit.early'], next='hub'),
     dict(id='late', when='order_late', lines=['visit.late'], next='hub'),
     dict(id='refusal', when='refused', lines=['site.refusal'], next='hub'),
     dict(id='proxy', when='npc_absent', lines=['visit.proxy'], next='end', speaker='proxy'),
    ]
    flows.append(dict(npc=n['id'], name=n['name'], task=v['task'], site=n['site'], region=n['region'],
                      nodes=nodes, chats=[f'chat.{i}' for i in range(1, len(n['chats']) + 1)],
                      arrival=['site.arrival'], warning=['site.warning'], refs=ref,
                      guards=['说话者本人存活、在场且愿谈时才播新句', '本人缺席时只有 proxy 节点可播，旁人不得代述新决定',
                              '任务已结只追加 after，不回滚旧结、不改结算', 'refusal 有替代出口，不取消基本安全']))
out = dict(date='2026-10-13', scope='S105 machine-readable condition flows for field NPCs: entry states, task gates, order branches, refusal and absence paths; projection of the registry, no new lines',
           vocabulary=['first_meet', 'night', 'any', 'task_open', 'task_done', 'order_early', 'order_late', 'refused', 'npc_absent'],
           flows=flows)
(ROOT / 'research/field-scene-flows.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "野外对白条件流"\nid: FX-FIELD-FLOWS\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S105, field-npc, flow]\naliases: []\n---\n\n'
     '# 野外对白条件流\n\n'
     f"把[[台本_FX_野外人物对白]]的 {len(flows)} 名人物投影成实现可用的条件流：入口状态（初遇/夜里）、常驻循环（复访）、任务闸（进行中/完成后）、顺序分支（先做/后做）、拒绝出口与缺席替代。"
     '节点只引用登记台词（不新写），条件词表固定；本页是机器可读形式的说明，不新增奖励、不改任何结算。\n\n'
     '**条件词表**：' + '、'.join('`' + w + '`' for w in out['vocabulary']) + '。\n\n'
     '| 人物 | 关联台本 | 节点 | 闲谈 | 拒绝出口 | 缺席替代 |\n|---|---|---:|---:|---|---|\n')
for f in flows:
    n += f"| [[人物_{f['npc']}_{f['name']}]] | [[{f['task']}]] | {len(f['nodes'])} | {len(f['chats'])} | 有（refusal） | 有（proxy） |\n"
for f in flows:
    n += f"\n## {f['name']}（`{f['npc']}`）\n\n关联台本：[[{f['task']}]]；地点：`{f['site']}`。\n\n"
    n += '| 节点 | 条件 | 台词引用 | 去向 |\n|---|---|---|---|\n'
    for nd in f['nodes']:
        n += f"| `{nd['id']}` | `{nd['when']}` | " + '、'.join('`' + r + '`' for r in nd['lines']) + f" | `{nd['next']}` |\n"
    n += f"\n**到场/警告**：" + '、'.join('`' + r + '`' for r in f['arrival'] + f['warning']) + '。**闲谈**：' + '、'.join('`' + r + '`' for r in f['chats']) + '。\n\n'
n += ('\n## 口径\n\n- 节点只引用登记台词：`refs` 中的键对应 [[台本_FX_野外人物对白]] 的原文，投影不生成新句。\n'
      '- `refusal` 与 `proxy` 是必备出口：拒绝不取消基本安全；本人缺席只播 proxy，旁人不得代述新决定。\n'
      '- 任务闸只读台本状态：进行中播 before、完成后播 after；顺序分支按先做/后做给 early/late，不改旧结。\n'
      '- 未做：引擎侧触发距离、作息与生成点；本页只给条件与去向。\n\n'
      '[[台本_FX_野外人物对白]] · [[特殊地点与野外NPC阶段验收记录]] · [[特殊地点与野外NPC对白扩展计划]] · [[文书_FX_野外地点短稿]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S105野外对白条件流（当前登记）\n\n'
           f"[[野外对白条件流]]：28 名野外人物的条件流（初遇/夜里/复访、任务进行中/完成后、先做/后做、拒绝出口、缺席替代），节点只引用登记台词，条件词表固定；实现可用的机器可读形式（research/field-scene-flows.json）。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/field-flows-note-hashes.json'
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
rule = ('\n<!-- FIELD-FLOWS-S105:BEGIN -->\n2026-10-13 S105：把28名野外人物的对白投影成实现可用的条件流。'
        'research/field-scene-flows.json 含固定条件词表与逐人节点图（初遇/夜里/复访、任务进行中/完成后、先做/后做、拒绝出口、缺席替代），节点只引用登记台词；入口design/02_世界与地图/特殊地点与野外NPC/野外对白条件流.md。'
        '不新增奖励与结算、不改台本状态；引擎侧触发距离与生成点仍待做。运行Validate-FieldFlows.py及既有检查；不部署游戏包。\n<!-- FIELD-FLOWS-S105:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- FIELD-FLOWS-S105:BEGIN -->.*?<!-- FIELD-FLOWS-S105:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- FIELD-FLOWS-S105:BEGIN -->.*?<!-- FIELD-FLOWS-S105:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/野外对白条件流.md', '入口 [野外对白条件流](design/02_世界与地图/特殊地点与野外NPC/野外对白条件流.md)'), encoding='utf-8')
print(json.dumps(dict(flows=len(flows), notes=len(generated)), ensure_ascii=False))
