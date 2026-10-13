"""S146: register the preservation-baseline snapshots that validators depend on.

Scans tool sources for concrete `backups/<...>.json|ini` references, hashes the
snapshots, writes the registry and renders the dependency page. No snapshot is
copied or modified.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'BASELINE-REG-S146'
CARD = '11_管理/验证快照依赖登记.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
FLOW = '11_管理/设计库生成与校验流程.md'
FULL = re.compile(r"backups/[A-Za-z0-9_\-]+(?:/[A-Za-z0-9_\-.]+)*\.(?:json|ini)")
PURPOSE = {
    'backups/city-drama-20261012-s76/research/city-campaign.json': 'S76 布林批之前的城市模型：证明该批未改写其他城市的字段与戏剧源。',
    'backups/city-drama-20261012-s78/city-campaign.json': 'S78 奥尔德文批之前的模型：证明布林演员表与全局字段保持不变。',
    'backups/city-drama-20261012-s79/city-campaign.json': 'S79 曼恩批之前的模型：证明既有城市与演员不被并入。',
    'backups/city-drama-20261012-s80-art-followup/city-campaign.json': 'S80 冶炼／羊毛批之前的模型：证明既有回执与路线字段保留。',
    'backups/city-drama-20261012-s81/city-campaign.json': 'S81 丹布里／曼郡批之前的模型：证明两城独立、他城不被改写。',
    'backups/city-drama-20261012-s82/city-campaign.json': 'S82 伊德斯／佛尔霍特批之前的模型：同上保留性检查。',
    'backups/city-drama-20261012-s83/city-campaign.json': 'S83 奥斯布鲁克／拉滕批之前的模型：同上。',
    'backups/city-drama-20261012-s84/city-campaign.json': 'S84 考德／柏石关批之前的模型：同上。',
    'backups/city-drama-20261012-s84/story-network.json': 'S84 之前的网状叙事登记：证明该批未改写主线边与依赖。',
    'backups/city-drama-20261012-s86/research/city-campaign.json': 'S86 寒凉盆地／无名修院批之前的模型：证明 ASH／HIG 深化未改他城。',
    'backups/city-spaces-20261012-s75/research/city-campaign.json': 'S75 空间替换之前的模型：城市空间写手与校验器用它做差异源。',
}
SPECIAL = {'backups/20261011-134931/formal-userdata/account.ini':
           '仅出现在工具链记录的“已停用检查”说明文本中，不是读取依赖。'}
refs = {}
for p in sorted((ROOT / 'research/tools').glob('*.py')):
    for m in FULL.finditer(p.read_text(encoding='utf-8')):
        refs.setdefault(m.group(0), set()).add(p.name)
entries = []
for rel, tools in sorted(refs.items()):
    f = ROOT / rel
    entries.append(dict(snapshot=rel, used_by=sorted(tools),
                        bytes=f.stat().st_size if f.exists() else 0,
                        sha256=hashlib.sha256(f.read_bytes()).hexdigest().upper() if f.exists() else '',
                        role='not-a-dependency' if rel in SPECIAL else 'preservation-baseline',
                        purpose=SPECIAL.get(rel) or PURPOSE.get(rel, '保留性检查的“变更前”快照。')))
reg = dict(date='2026-10-13',
           scope='S146 preservation-baseline registry: every concrete backups/ path referenced by tools, hashed read-only; deleting a snapshot breaks the preservation checks',
           entries=entries)
(ROOT / 'research/preservation-baselines.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
base = [e for e in entries if e['role'] == 'preservation-baseline']
n = ('---\ntitle: "验证快照依赖登记"\nid: MGMT-BASELINE-REG-S146\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S146, review, verification]\naliases: []\n---\n\n'
     '# 验证快照依赖登记\n\n'
     f"校验器里的**保留性检查**要拿“变更前”的快照做对照：本页登记工具源码中出现的全部 `backups/…` 具体路径（{len(base)} 份快照＋1 条非依赖说明），逐份给出大小、哈希与用途。**快照是验证输入，不是可随手清理的旧文件**；删除会让对应校验器无法运行。登记 `research/preservation-baselines.json`，工具 `research/tools/Write-BaselineRegistry.py`。\n\n"
     '| 快照 | 大小 | SHA256（前16） | 使用者 | 用途 |\n| --- | ---: | --- | --- | --- |\n')
for e in base:
    n += f"| `{e['snapshot']}` | {e['bytes']:,} | `{e['sha256'][:16]}…` | {'、'.join('`' + u + '`' for u in e['used_by'])} | {e['purpose']} |\n"
n += ('\n## 规则\n\n'
      '- 校验器与两个城市空间工具直接读这些快照；缺任一份即无法完成对应保留性检查（S145 演练已在最小副本中实测）。\n'
      '- 快照本身受哈希登记保护：被改动或替换会由 `Validate-PreservationBaselines.py` 报错，提示重新指认基线。\n'
      '- 新增保留性检查时，先在工具里写入具体路径，再重跑本页工具登记；不要用目录通配代替具体路径。\n\n'
      '## 边界\n\n'
      '- 只读哈希与登记，不复制、不修改、不删除任何备份。\n'
      '- 快照是当时的模型文本，不含游戏资源；本页不改变部署门槛。\n\n'
      '[[设计库生成与校验流程]] · [[全链复跑演练S145]] · [[质量守卫总表]] · [[逻辑验收记录]]\n')
put(CARD, n)
flow = (V / FLOW).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n- 验证快照依赖（S146）：{len(base)} 份 `backups/…` 快照是城市/戏剧类保留性检查的“变更前”基线，逐份登记哈希与用途（[[验证快照依赖登记]]）；缺任一份则对应校验器无法运行，改动或替换由 `Validate-PreservationBaselines.py` 报错。\n" + z)
flow2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, flow, flags=re.S) if a in flow else flow.rstrip() + '\n' + blk + '\n'
put(FLOW, flow2)
t = (V / PLAN).read_text(encoding='utf-8-sig')
blk2 = (a + f"\n## S146验证快照依赖（当前登记）\n\n[[验证快照依赖登记]]：{len(base)} 份 `backups/…` 快照为保留性检查基线，已逐份登记哈希/用途；缺任一份对应校验器不可运行。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk2 + '\n'
put(PLAN, t2)
own = ROOT / 'research/baseline-reg-note-hashes.json'
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
rule = ('\n<!-- BASELINE-REG-S146:BEGIN -->\n2026-10-13 S146：验证快照依赖登记。'
        f"工具源码中 {len(base)} 份 backups/… 快照（城市/戏剧类保留性检查的“变更前”基线）逐份登记大小/哈希/用途，另 1 条为非依赖说明；"
        '缺任一份对应校验器无法运行，改动或替换由 Validate-PreservationBaselines.py 报错。入口design/11_管理/验证快照依赖登记.md；不复制、不修改、不删除备份。\n<!-- BASELINE-REG-S146:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- BASELINE-REG-S146:BEGIN -->.*?<!-- BASELINE-REG-S146:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- BASELINE-REG-S146:BEGIN -->.*?<!-- BASELINE-REG-S146:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(entries=len(entries), baselines=len(base), missing=[e['snapshot'] for e in base if not e['bytes']]), ensure_ascii=False))
