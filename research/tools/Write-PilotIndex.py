"""S158: consolidated pilot-batch index (three batches, shared rules, totals)."""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PILOT-INDEX-S158'
CARD = '11_管理/试点批次总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
n2 = json.loads((R / 'pilot-batch-n2.json').read_text(encoding='utf-8'))
sc2 = json.loads((R / 'pilot-batch-scenarios-n2.json').read_text(encoding='utf-8'))
bry = json.loads((R / 'pilot-batch-cs-bry-01.json').read_text(encoding='utf-8'))
fx = json.loads((R / 'pilot-batch-fx.json').read_text(encoding='utf-8'))
rows = [
    dict(id='P1', entry='[[试点实现批次N2]]', layer='主章单案', quest=n2['script'],
         stubs=len(n2['stubs']), keys=len(n2['keys']), nodes=len(n2['flow_nodes']), methods=len(n2['methods']),
         scenarios=len(sc2['scenarios']), covers='键→桩→台词→回访；拒绝/缺席与顺序规则'),
    dict(id='P2', entry='[[试点实现批次CS-BRY-01]]', layer='城市系统', quest=bry['quest'],
         stubs=len(bry['stubs']), keys=len(bry['keys']), nodes=len(bry['flow_nodes']), methods=len(bry['methods']),
         scenarios=len(bry['scenarios']), covers='服务班／信任档／闲谈池；早到与晚到回执'),
    dict(id='P3', entry='[[试点实现批次FX野外层]]', layer='野外层', quest=fx['npc']['id'],
         stubs=0, keys=0, nodes=len(fx['flow']['nodes']), methods=0,
         scenarios=len(fx['scenarios']), covers='存在性四态／文书只给信息／迹象判定／三池闲谈'),
]
tot = dict(stubs=sum(r['stubs'] for r in rows), keys=sum(r['keys'] for r in rows),
           nodes=sum(r['nodes'] for r in rows), methods=sum(r['methods'] for r in rows),
           scenarios=sum(r['scenarios'] for r in rows))
reg = dict(date='2026-10-13',
           scope='S158 pilot index: three batches consolidated with counts and shared rules; planning only',
           batches=rows, totals=tot)
(R / 'pilot-batches.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "试点批次总表"\nid: MGMT-PILOT-INDEX-S158\ntype: index\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S158, index, implementation]\naliases: []\n---\n\n'
     '# 试点批次总表\n\n'
     '实现轮的**单一入口**：三批试点合起来覆盖 [[实现交接总表]] 六步的全部接线类型。本页只汇总与给规则，具体输入、落地顺序与场景在各批页面；数据 `research/pilot-batches.json`（由三份批次登记现场汇总）。\n\n'
     '| 批次 | 层 | 样本 | 桩 | 键 | 流节点 | 解法 | 验收场景 | 覆盖 |\n| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |\n')
for r in rows:
    n += (f"| {r['id']} | {r['layer']} | `{r['quest']}` | {r['stubs']} | {r['keys']} | {r['nodes']} | {r['methods']} | {r['scenarios']} | {r['covers']} |\n")
n += (f"| **合计** | — | — | **{tot['stubs']}** | **{tot['keys']}** | **{tot['nodes']}** | **{tot['methods']}** | **{tot['scenarios']}** | — |\n\n"
      '## 建议顺序\n\n'
      '1. **P1（N2）**先做：键与桩最少，跑通"键→桩→台词→回访"这条主链；\n'
      '2. **P2（CS-BRY-01）**再做：加系统层（服务班／信任档／闲谈池）与早到/晚到回执；\n'
      '3. **P3（FX-QRY）**收尾：野外层的存在性四态、文书与迹象、三池分池。\n\n'
      '## 共享规则（三批一致）\n\n'
      '- **键名口径**：引擎键＝`EAO_`＋登记键名（[[引擎键名前缀与遗留键登记]]）；小样 `EAO_N1_stage` 与登记 `resolve_N1` 的取舍属 OI-03。\n'
      '- **前置**：OI-02（引擎事件号分配）、OI-03（存档字段命名与旧档迁移）；未定则事件号与键名只作占位。\n'
      '- **验收方式**：编译场景须与候选包**同一 SHA** 匹配；运行按 [[试玩路线与检查单]] 与 [[特殊地点阶段制作与校准规程]] 记录；未跑过不得标"已验证"。\n'
      '- **全局不变式**：已结案只追加回应、不回滚历史；拒绝/缺席/死亡优先于新台词；不重复结算、不二发奖励；闲谈与文书不推进任务。\n'
      '- **不越界**：三批都**不含实现代码、不分配事件号、不写数值**；经济、比例与触发距离待实机。\n\n'
      '## 边界\n\n'
      '- 三批各取一个样本（主章一案、城市一案、野外一人）；全量铺开按各登记（1,807 桩／1,393 键／130 条件流）分批推进，模式相同。\n'
      '- 本页计数由 `Validate-PilotIndex.py` 现场重算核对；批次登记变化须重跑写手刷新。\n\n'
      '[[实现交接总表]] · [[试点实现批次N2]] · [[试点批次验收场景N2]] · [[试点实现批次CS-BRY-01]] · [[试点实现批次FX野外层]] · [[待办与已知缺口登记]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S158试点批次总表（当前登记）\n\n[[试点批次总表]]：三批试点合计 {tot['stubs']} 桩／{tot['keys']} 键／{tot['nodes']} 流节点／{tot['methods']} 解法／{tot['scenarios']} 验收场景，覆盖实现六步的全部接线类型；共享键名口径、前置与验收方式。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'pilot-index-note-hashes.json'
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
rule = ('\n<!-- PILOT-INDEX-S158:BEGIN -->\n2026-10-13 S158：试点批次总表（实现轮单一入口）。'
        f"三批合计 {tot['stubs']}桩／{tot['keys']}键／{tot['nodes']}流节点／{tot['methods']}解法／{tot['scenarios']}验收场景，覆盖实现六步全部接线类型；"
        '共享键名口径（EAO_＋登记键名）、前置（OI-02/OI-03）与验收方式（同候选SHA＋按规程记录）；建议顺序 P1→P2→P3。'
        '入口design/11_管理/试点批次总表.md；运行Validate-PilotIndex.py及既有检查。\n<!-- PILOT-INDEX-S158:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PILOT-INDEX-S158:BEGIN -->.*?<!-- PILOT-INDEX-S158:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PILOT-INDEX-S158:BEGIN -->.*?<!-- PILOT-INDEX-S158:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(batches=len(rows), totals=tot), ensure_ascii=False))
