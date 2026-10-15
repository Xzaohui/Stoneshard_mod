"""S154: acceptance scenarios for the pilot batch N2.

Derives the scenario list from the pilot registry and the state-key value sets,
then renders the acceptance-scenario page. Planning only: no implementation.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PILOT-N2-SCEN-S154'
CARD = '11_管理/试点批次验收场景N2.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
batch = json.loads((R / 'pilot-batch-n2.json').read_text(encoding='utf-8'))
sk = {k['key']: k for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys'] if k['script'] == 'N2'}
SCEN = [
    dict(id='N2-T01', name='接取与首见', steps=['在灰堤找到当事人并首次交谈', '听完入口三句后仍可离开'],
         writes=[('encountered_N2', 'true')], invariants=['resolve_N2 仍为 none', '不因只交谈而写入任何 callback_*']),
    dict(id='N2-T02', name='保护路线结算', steps=['完成现场实际观察', '选择保护路线并二次确认', '实际处置发生后才提交'],
         writes=[('resolve_N2', 'protected'), ('callback_N2_protected', 'true')],
         invariants=['callback_N2_public 不写', '缺实际观察或未二次确认时保持 pending']),
    dict(id='N2-T03', name='公开路线结算', steps=['完成现场实际观察', '选择公开路线并二次确认'],
         writes=[('resolve_N2', 'public'), ('callback_N2_public', 'true')],
         invariants=['callback_N2_protected 不写', '两条路线互斥，先结算者生效']),
    dict(id='N2-T04', name='拒绝与缺席', steps=['明确拒绝本案', '再次接近同一当事人'],
         writes=[('presence_N2', 'refused')],
         invariants=['resolve_N2 保持 none', '拒绝后不播结算台词，只播拒绝回应']),
    dict(id='N2-T05', name='已结案回访', steps=['任一结算后再次回访', '查阅相关物件'],
         writes=[], invariants=['不回滚 resolve_N2', '不重复结算或发奖', '只追加新回应']),
    dict(id='N2-T06', name='存读档与顺序', steps=['结算后保存并重载', '先做后续章再回访本案'],
         writes=[], invariants=['键值跨读档保持', '顺序颠倒只重评未来，不回滚历史']),
]
rows = []
for s in SCEN:
    for key, val in s['writes']:
        spec = sk.get(key)
        assert spec is not None, key
        assert val in spec['values'], (key, val, spec['values'])
        rows.append(dict(scenario=s['id'], key=key, value=val, kind=spec['kind']))
reg = dict(date='2026-10-13', scope='S154 pilot batch N2 acceptance scenarios: expected writes checked against the state-key value sets; planning only, nothing implemented',
           scenarios=[dict(id=s['id'], name=s['name'], steps=s['steps'], writes=s['writes'], invariants=s['invariants']) for s in SCEN],
           write_matrix=rows)
(R / 'pilot-batch-scenarios-n2.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "试点批次验收场景N2"\nid: MGMT-PILOT-N2-SCEN-S154\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S154, guide, acceptance]\naliases: []\n---\n\n'
     '# 试点批次验收场景N2\n\n'
     '[[试点实现批次N2]] 的**验收场景**：每条给出步骤、**期望写入**与**不得发生的事**。期望写入逐条对照 [[状态键映射总表]] 的取值集合校验（登记 `research/pilot-batch-scenarios-n2.json`）；本页只列场景，不含实现代码、不部署。\n\n'
     '## 场景与期望写入\n\n| 场景 | 名称 | 步骤 | 期望写入 | 不得发生 |\n| --- | --- | --- | --- | --- |\n')
for s in SCEN:
    writes = '；'.join(f"`{k}`＝`{v}`" for k, v in s['writes']) or '无写入'
    n += f"| {s['id']} | {s['name']} | {' → '.join(s['steps'])} | {writes} | {'；'.join(s['invariants'])} |\n"
n += ('\n## 写入矩阵（对照取值集合）\n\n| 场景 | 键 | 取值 | 类型 |\n| --- | --- | --- | --- |\n')
for r in rows:
    n += f"| {r['scenario']} | `{r['key']}` | `{r['value']}` | {r['kind']} |\n"
n += (f"\n覆盖：{len(SCEN)} 条场景覆盖 N2 的全部 **{len(sk)}** 个键（`encountered_N2`、`resolve_N2`、`callback_N2_protected`、`callback_N2_public`、`presence_N2`）；每个写入值都取自登记取值集合，未新增取值。\n\n"
      '## 运行记录要求\n\n'
      '- 每条场景按 [[特殊地点阶段制作与校准规程]] 记录：版本指纹、步骤、观察、截图或日志、差异与结论；未跑过不得标"已验证"。\n'
      '- 编译侧沿用既有链：新增场景须与候选包 **同一 SHA** 匹配；静态检查不替代游戏内结果。\n'
      '- 顺序场景（N2-T05/T06）验证"已结案只追加回应、不回滚历史"这一条全局规则。\n\n'
      '## 边界\n\n'
      '- 期望写入是**设计口径**，实现时若引擎需要额外字段，先在 [[状态键映射总表]] 登记再改本页。\n'
      '- 本页不覆盖经济数值、比例碰撞与触发距离（见 [[待办与已知缺口登记]]）。\n\n'
      '[[试点实现批次N2]] · [[状态键映射总表]] · [[实现交接总表]] · [[试玩路线与检查单]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S154试点批次验收场景（当前登记）\n\n[[试点批次验收场景N2]]：{len(SCEN)} 条场景覆盖 N2 全部 {len(sk)} 键，期望写入逐条对照取值集合；含顺序与存读档场景；仅场景清单，不含实现。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'pilot-scenarios-note-hashes.json'
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
rule = ('\n<!-- PILOT-N2-SCEN-S154:BEGIN -->\n2026-10-13 S154：试点批次验收场景N2。'
        f"6条场景覆盖N2全部5键（encountered/resolve/callback×2/presence），期望写入逐条对照取值集合校验，含拒绝、已结案回访与存读档顺序场景；"
        '仅场景清单与口径，不含实现代码、不部署。入口design/11_管理/试点批次验收场景N2.md；运行Validate-PilotScenarios.py及既有检查。\n<!-- PILOT-N2-SCEN-S154:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PILOT-N2-SCEN-S154:BEGIN -->.*?<!-- PILOT-N2-SCEN-S154:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PILOT-N2-SCEN-S154:BEGIN -->.*?<!-- PILOT-N2-SCEN-S154:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(scenarios=len(SCEN), writes=len(rows), keys=len(sk)), ensure_ascii=False))
