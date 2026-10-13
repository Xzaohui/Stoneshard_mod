"""S135: render the vanilla reputation-tier/local-state reference card."""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'REP-REF-S135'
CARD = '01_原作基线/原作声誉档位与地方状态参照.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
probe = read('research/reputation-structure-probe.json'); base = read('research/local-baseline.json')
assert probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint drift'
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
GROUPS = [
    ('任务类', ('contract', 'contractFail', 'comission', 'quest', 'questFail')),
    ('贸易与文书', ('trade', 'haggling', 'heraldicNote', 'trophy')),
    ('行为与其他', ('dialogue', 'clearingArea', 'gravedigging')),
    ('犯罪类', ('thievery', 'lockpick', 'assault', 'murder', 'murderCattle', 'violation', 'escape', 'jail')),
]
by_key = {}
for s in probe['sources']:
    by_key.setdefault(s['key'], s)
perks = {}
for p in probe['perks']:
    perks.setdefault(p['key'], {})[p['row']] = p
states = {}
for s in probe['states']:
    states.setdefault(s['key'], {})[s['row']] = s
n = ('---\ntitle: "原作声誉档位与地方状态参照"\nid: BASE-017\ntype: research\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, baseline, reputation, settlement]\naliases: []\n---\n\n'
     '# 原作声誉档位与地方状态参照\n\n'
     '对本地 `vanilla.win` 字符串表做**只读**声誉结构探针：信息流、来源清单、档位加成、犯罪与通缉、地方状态；只存键名、定位与不超过约46字的片段，不存完整文本。工具 `research/tools/Probe-ReputationStructure.py`，记录 `research/reputation-structure-probe.json`。静态表结构，不是运行时行为验证。\n\n'
     '## 读取指纹\n\n| 项 | 值 |\n| --- | --- |\n'
     f"| 来源 | 本地 `vanilla.win`（原始 data.WIN 备份） |\n| SHA256 | `{probe['sha256']}` |\n| 字符串总数 | {probe['strg_count']} |\n"
     f"| 信息流 | {len(probe['feeds'])} |\n| 来源行 | {len(probe['sources'])} |\n| 档位行 | {len(probe['perks'])}（名/效果/描述） |\n| 地方状态行 | {len(probe['states'])}（名/效果/描述） |\n\n"
     '## 声誉信息流与界面\n\n| 键 | 简中 | 英文 |\n| --- | --- | --- |\n')
for f in probe['feeds']:
    n += f"| `{f['key']}` | {f['zh']} | {f['en'] or '—'} |\n"
n += '\n界面标签：' + '、'.join(f"{u['zh']}（{u['en'] or '—'}）" for u in probe['ui']) + '。声誉按村落/阵营/全域三层出信息流。\n\n'
n += '## 声誉来源清单（均带 `[声誉%rep_amount%]`）\n\n| 组 | 键 | 简中 | 英文 |\n| --- | --- | --- | --- |\n'
for gname, keys in GROUPS:
    for k in keys:
        s = by_key.get(k)
        if s:
            n += f"| {gname} | `{k}` | {s['zh']} | {s['en'] or '—'} |\n"
n += ('\n来源覆盖契据、委托、剧情任务、贸易、文书、对话选项，以及盗窃/撬锁/袭击/杀人/屠畜/扰乱治安/逃刑/坐牢等犯罪类；另有清理周边危险与毁坏坟墓。\n\n'
      '## 档位加成（正负两向）\n\n| 档位 | 英文 | 效果 |\n| --- | --- | --- |\n')
for k, rows in perks.items():
    nm = rows.get('name', {}); ef = rows.get('effect', {})
    n += f"| {nm.get('zh', k)} | {nm.get('en') or '—'} | {ef.get('zh', '—')} |\n"
n += ('\n正向含特殊任务、特色商品、赏金预付、同心同德（跨区外溢）、应有尽有（库存 +10/15/20%）、价格公道（+5/10/15%）；'
      '负向含宰你没商量（−15/−30%）、粗布烂铁（库存 −25/−50% 并降品级）、本地公敌（不交易）。\n\n'
      '## 犯罪与通缉\n\n| 键 | 简中 | 英文 |\n| --- | --- | --- |\n')
for c in probe['crime']:
    if c['row'] == 'label':
        n += f"| `{c['key']}` | {c['zh']} | {c['en'] or '—'} |\n"
n += '\n另有犯罪计数（`crimesCommited`）与悬赏提示行（含罚金/拘役占位符），完整文案未存。\n\n'
n += '## 地方状态（15 项）\n\n| 状态 | 英文 | 效果 |\n| --- | --- | --- |\n'
for k, rows in states.items():
    nm = rows.get('name', {}); ef = rows.get('effect', {})
    n += f"| {nm.get('zh', k)} | {nm.get('en') or '—'} | {ef.get('zh', '—')} |\n"
n += ('\n状态含物资短缺、货运中断/迟缓、梦魇、瘟病、路途险恶、黑道会面、跳蚤市场、参玄大会、增援、朝圣、竞争、动物繁殖、生机勃勃、集会；'
      '效果涉及价格、库存、睡眠收益、契据难度与区域声誉收益等。\n\n'
      '## 对照与本Mod口径\n\n'
      '- **分层**：原版声誉按村落/阵营/全域结算并可跨区外溢；本Mod新增层是自有的「地方信任 −2..+2」，与原版声望分开，不外溢（[[势力关系总览]]、[[任务状态与依赖]]、[[经济与奖励]]）。\n'
      '- **来源**：原版来源含契约/委托/剧情/贸易/犯罪等 20 类；本Mod地方信任只在具体支线与排他交易后有限写入，罪行另行处理。\n'
      '- **档位语义**：原版档位改价格、库存、预支、特殊任务/商品等数值与权限；本Mod信任档只改范围与便利（−2 关闭／−1 限范围／0 基础／+1 一处小便利／+2 预约与转介），不改授权、不无限供给（[[城市服务班与有限库存]]）。\n'
      '- **不照搬数值**：库存 ±10..50%、交易 ±5..30%、预付赏金、跨区外溢、特殊商贩等不引入；单渠道折扣初拟不超过 15%，不叠成负价格，且不因日常完成补满原作库存（[[经济与奖励]]）。\n'
      '- **地方状态**：原版状态带价格/库存/难度/收益修正；本Mod只写文本状态与回执，不写这些修正。\n'
      '- **犯罪**：原版有犯罪计数与两档通缉（格杀勿论／罚金或拘役）；本Mod不改原版通缉与罚金。\n\n'
      '## 边界\n\n'
      '- 只读静态表；档位阈值、具体数值与运行时行为未读取、未验证。\n'
      '- 片段截断至约46字；悬赏提示等长文案只留键名与标签。\n\n'
      '[[原作契据任务与声誉结构参照]] · [[原作剧情与对话系统参照]] · [[原作基线索引]] · [[城市服务班与有限库存]] · [[经济与奖励]] · [[城镇声望与信任系统]] · [[城镇声望系统中英对照]]\n')
put(CARD, n)
idx = (V / '01_原作基线/原作基线索引.md').read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = a + '\n[[原作声誉档位与地方状态参照]]：三层信息流、19+ 来源、正负档位（含库存/价格数值）、两档通缉与 15 项地方状态；只读探针，片段≤46字。\n' + z
idx2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, idx, flags=re.S) if a in idx else idx.rstrip() + '\n\n' + blk + '\n'
put('01_原作基线/原作基线索引.md', idx2)
plan = (V / PLAN).read_text(encoding='utf-8-sig')
blk2 = a + '\n## S135原作声誉档位与地方状态（当前登记）\n\n[[原作声誉档位与地方状态参照]]：10 信息流、20 来源、60 档位行、45 状态行、5 犯罪行；对照口径见卡内。\n' + z
plan2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, plan, flags=re.S) if a in plan else plan.rstrip() + '\n\n' + blk2 + '\n'
put(PLAN, plan2)
own = ROOT / 'research/rep-ref-note-hashes.json'
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
rule = ('\n<!-- REP-REF-S135:BEGIN -->\n2026-10-13 S135：原作声誉档位与地方状态参照（只读探针）。'
        '10信息流（村落/阵营/全域+界面）、20来源（任务/贸易/犯罪等，均带[声誉%rep_amount%]）、20档位（特殊任务/特色商品/赏金预付/库存±10..50%/交易±5..30%/本地公敌）、两档通缉、15地方状态；'
        '对照口径：地方信任与原版声望分开、信任档只改范围与便利、不照搬数值、不写地方状态修正、不改通缉。'
        '入口design/01_原作基线/原作声誉档位与地方状态参照.md；片段≤46字。运行Validate-ReputationReference.py及既有检查；不部署游戏包。\n<!-- REP-REF-S135:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- REP-REF-S135:BEGIN -->.*?<!-- REP-REF-S135:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- REP-REF-S135:BEGIN -->.*?<!-- REP-REF-S135:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(notes=len(generated), feeds=len(probe['feeds']), perks=len(perks), states=len(states)), ensure_ascii=False))
