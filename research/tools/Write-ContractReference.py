"""S134: render the vanilla contract/reputation structure reference card.

Renders research/contract-structure-probe.json (read-only, bounded snippets)
into design/01_原作基线/原作契据任务与声誉结构参照.md with a Mod-side
comparison section, and registers the card in the baseline index and plan.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'CONTRACT-REF-S134'
CARD = '01_原作基线/原作契据任务与声誉结构参照.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
probe = read('research/contract-structure-probe.json'); base = read('research/local-baseline.json')
assert probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint drift'
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "原作契据任务与声誉结构参照"\nid: BASE-016\ntype: research\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, baseline, contract, reputation]\naliases: []\n---\n\n'
     '# 原作契据任务与声誉结构参照\n\n'
     '按“扒原作任务/对白系统作初始参照”的要求，对本地 `vanilla.win` 的字符串表做**只读**契据（contract）结构探针：只存键名、定位索引与不超过约46字的片段，不存完整对白；工具 `research/tools/Probe-ContractStructure.py`，记录 `research/contract-structure-probe.json`。静态表结构，不是运行时行为验证。\n\n'
     '## 读取指纹\n\n| 项 | 值 |\n| --- | --- |\n'
     f"| 来源 | 本地 `vanilla.win`（用户确认为原始 data.WIN 备份） |\n"
     f"| SHA256 | `{probe['sha256']}`（与 `research/local-baseline.json` 一致） |\n"
     f"| 字符串总数 | {probe['strg_count']} |\n"
     f"| 契据相关键（本地化） | {probe['contract_key_count']} |\n"
     f"| 具名契据对白行（巨魔） | {len(probe['troll_rows'])} |\n"
     f"| 标识符侧契据名 | {len(probe['identifier_contract_names'])} |\n\n"
     '## 自定义开局设置项\n\n'
     '`Contract_*` 与相邻行位于**自定义/难度设置**块（同块含 `ReputationGainGlobal`、`Ambush_Chance`、`Area_Wilderness`、`Gem_SP_Mod` 等），说明契据时限、可领数量与声誉收益是开局可调项：\n\n'
     '| 键 | 简中 | 英文 |\n| --- | --- | --- |\n')
for s in probe['settings']:
    n += f"| `{s['key']}` | {s['zh']} | {s['en']} |\n"
n += ('\n## 信息流与计数\n\n'
      '| 键 | 简中 | 英文 |\n| --- | --- | --- |\n')
for f in probe['feeds']:
    n += f"| `{f['key']}` | {f['zh']} | {f['en'] or '—'} |\n"
n += ('\n完成/失败模板带 `%town_name%`、`%contract_name%`、`%rep_amount%` 三个占位符：契据声誉按**聚落**结算。\n\n'
      '## 契据对话族\n\n'
      '本地化侧共有 @NK@ 个 `*contract*` 键，含受理界面与操作句（示例）：@KS@。\n\n'
      '## 声誉与契据的联动（原版）\n\n'
      '- 声誉收益按**地牢类型**分档：地下经堂（Catacombs）、墓穴（Crypt）、棱堡（Bastion）与通用档。\n'
      '- 「当地人信任→预支赏金」：`advances`「你获得了当地人的信任，现在领取契据任务可以预先拿到赏金。」\n'
      '- 「跨区外溢」：`underworldConnections1/2`「完成城联其他地区契据任务获得多少声誉，布林的声誉也会相应提升一部分。」二档另解锁特殊商贩。\n'
      '- 「竞争」：`competition`「传闻这个地方的契据赏金丰厚，奥尔多各地的雇佣兵因此蜂拥而来，竞争便也激烈了起来。」伴随可领契据难度变大与其他雇佣兵出现。\n\n'
      '## 具名契据与条件对白\n\n'
      '巨魔契据（`trollcontract*`，@NT@ 行）按状态出句：未接（`status_unaccepted`）、进行（`status_wip`）、去过（`beenthere`）、已击杀（`status_dead*`），另有语气变体（`status_boast`/`status_modest`）与 PC/对方成对行。标识符侧另有剧情链名（示例）：@IS@。\n\n'
      '## 对照与本Mod口径\n\n'
      '- **命名**：本Mod新增任务不使用「契据」名（模组用「工约/短单/运单」，见 [[原创物品与装备总表]] 的「契据」行），不冒充原版契据。\n'
      '- **声誉分层**：原版声誉按聚落结算且可由契据跨区外溢；本Mod新增层是自有的「地方信任 −2..+2」，与原版声望分开，且不外溢到原版声誉（见 [[势力关系总览]]、[[经济与奖励]]）。\n'
      '- **重复性**：原版契据可反复领取并有竞争修正；本Mod的普通运输、维修、清运不做玩家重复任务（S62 口径）。\n'
      '- **条件对白**：巨魔契据的状态化出句与本Mod [[网状叙事与条件对话规范]] 的状态＋有限回执同构；本Mod额外限定知情范围，死亡/缺席/拒绝不播新句。\n'
      '- **不照搬项**：预支赏金、跨区声誉外溢、竞争修正三项结构不引入；信任档只解锁服务与信息，奖励去重不变。\n\n'
      '## 边界\n\n'
      '- 只读静态表；未在游戏内验证契据流程、时限或声誉数值。\n'
      '- 片段截断至约46字；完整对白不落盘。\n'
      '- 设置项数值不在字符串表内，未读取；如需引用数值须另行读取标识符/常量表并标注。\n\n'
      '[[原作剧情与对话系统参照]] · [[原作基线索引]] · [[网状叙事与条件对话规范]] · [[势力关系总览]] · [[原创物品与装备总表]] · [[城镇声望与信任系统]] · [[城镇声望系统中英对照]]\n'
      ).replace('@NK@', str(probe['contract_key_count'])).replace(
          '@KS@', '、'.join(f"`{k}`" for k in probe['contract_keys_sample'][:10])).replace(
          '@NT@', str(len(probe['troll_rows']))).replace(
          '@IS@', '、'.join(f"`{k}`" for k in probe['identifier_contract_names'][:6]))
put(CARD, n)
# register in the baseline index (block preserved)
idx = (V / '01_原作基线/原作基线索引.md').read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = a + '\n[[原作契据任务与声誉结构参照]]：契据设置项、聚落声誉结算模板、地牢类型分档、预支/外溢/竞争三项联动、巨魔契据状态化对白；只读探针，片段≤46字。\n' + z
idx2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, idx, flags=re.S) if a in idx else idx.rstrip() + '\n\n' + blk + '\n'
put('01_原作基线/原作基线索引.md', idx2)
plan = (V / PLAN).read_text(encoding='utf-8-sig')
blk2 = a + '\n## S134原作契据与声誉结构（当前登记）\n\n[[原作契据任务与声誉结构参照]]：6 设置项、5 信息流、144 契据键、60 行巨魔契据对白、667 标识符名；对照口径见卡内。\n' + z
plan2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, plan, flags=re.S) if a in plan else plan.rstrip() + '\n\n' + blk2 + '\n'
put(PLAN, plan2)
own = ROOT / 'research/contract-ref-note-hashes.json'
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
rule = ('\n<!-- CONTRACT-REF-S134:BEGIN -->\n2026-10-13 S134：原作契据任务与声誉结构参照（只读探针）。'
        '6设置项（时限/可领数/按地牢类型声誉收益）、5信息流（%town_name%/%contract_name%/%rep_amount%）、144契据键、60行巨魔契据状态化对白、667标识符名；'
        '对照口径：不用「契据」名、地方信任与原版声望分开、不做重复任务、不引入预支/外溢/竞争。'
        '入口design/01_原作基线/原作契据任务与声誉结构参照.md；片段≤46字。运行Validate-ContractReference.py及既有检查；不部署游戏包。\n<!-- CONTRACT-REF-S134:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- CONTRACT-REF-S134:BEGIN -->.*?<!-- CONTRACT-REF-S134:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- CONTRACT-REF-S134:BEGIN -->.*?<!-- CONTRACT-REF-S134:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(notes=len(generated), keys=probe['contract_key_count'], troll=len(probe['troll_rows'])), ensure_ascii=False))
