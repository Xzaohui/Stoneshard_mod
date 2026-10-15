"""Render the S92 original special-location / field-NPC inventory card.

Reads research/special-location-inventory.json (metadata only) and writes the
baseline card plus index blocks; owns special-location-note-hashes.json.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'SPECIAL-LOC-S92'
CARD = '01_原作基线/特殊地点与野外NPC清点.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
inv = read('research/special-location-inventory.json')
base = read('research/local-baseline.json')
assert inv['sha256'] == base['candidate_baseline']['sha256'], 'source fingerprint drift'
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
def block(a, z, t, b):
    n = a + '\n' + b.rstrip() + '\n' + z
    return re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + n + '\n'
n = ('---\ntitle: "特殊地点与野外NPC清点"\nid: SRC-SPECIAL-LOC-S92\ntype: source\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S92, source, special-locations]\naliases: []\n---\n\n'
     '# 特殊地点与野外NPC清点\n\n'
     '本页是[[特殊地点与野外NPC对白扩展计划]]第一步的只读清点结果：从本地原版包枚举世界地图区域、特殊地点候选与地形类型名，并登记对白族规模。'
     '数据源为只读扫描，**只保存键名、STRG序号、中文可用性与短地点名**，不保存对白全文、反编译源码或图集；逐NPC中英对读、野外遭遇映射与地点设计卡是后续步骤。\n\n'
     '> [!info] 来源与指纹\n'
     f'> 文件 `{inv["source"]}`；SHA-256 `{inv["sha256"][:16]}…`；{inv["bytes"]} 字节；STRG {inv["strg_count"]} 条；清点日期 {inv["checked_at"]}。\n'
     '> 与 `research/local-baseline.json` 的候选基线指纹一致；当前 `data.win` 组合包不用于本清点。\n\n'
     '方法：读取 STRG 字符串表；简体槽取首个含汉字且不含假名/谚文的字段。键存在不证明场景在游戏中可达；名字与游戏内显示不一致时以游戏为准。\n\n')
n += f"## 世界地图区域（{len(inv['map_regions'])}）\n\n|键|STRG|中文名|English|\n|---|---|---|---|\n"
for r in inv['map_regions']:
    n += f"|`{r['key']}`|{r['index']}|{r['name_zh']}|{r.get('name_en', '')}|\n"
n += f"\n## 特殊地点候选（{len(inv['rumor_sites'])}）\n\n地点名取自传闻条目的地点槽（中文与官方英文名并列）；`对白入口`为已配到的传闻对白条目数（本条只计数量，不存文本）。\n\n|键|STRG|中文名|English|对白入口|已知所属城镇|\n|---|---|---|---|---:|---|\n"
for r in inv['rumor_sites']:
    towns = '、'.join(r['towns']) if r['towns'] else '待核'
    n += f"|`{r['key']}`|{r['index']}|{r['name_zh']}|{r.get('name_en', '')}|{r['dialogue_entries']}|{towns}|\n"
n += f"\n## 地形与类型名（{len(inv['site_types'])}）\n\n|键|STRG|中文名|English|\n|---|---|---|---|\n"
for r in inv['site_types']:
    n += f"|`{r['key']}`|{r['index']}|{r['name_zh']}|{r.get('name_en', '')}|\n"
if inv['site_type_identifier_only']:
    n += '\n仅有标识符、未见本地化名（待核）：' + '、'.join('`' + k + '`' for k in inv['site_type_identifier_only']) + '。\n'
fam = inv['dialogue_families']
n += (f"\n## 对白族规模\n\n场景 {fam['scene']}、问候 {fam['greeting']}、闲谈 {fam['chat']}、NPC {fam['npc']}、随从 {fam['follower']}；"
      '逐条键/序号/说话人槽见 `research/original-dialogue-inventory.json`，本页不重复。\n\n'
      '## 未核与边界\n\n- 键存在、有中文名都不证明玩家能到达、能触发对白或地点仍在当前版本使用；需按计划逐项做场景核对。\n'
      '- 传闻地点名为通用名（如「洞穴」「矿洞」），同名地点可能多处；具体位置与原文语境需逐条读取对白后才能定。\n'
      '- 只读扫描，未改游戏包、未触玩家存档；逐NPC中英对读、Mod原创特殊地点清点与地点设计卡见后续步骤。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[原作剧情与对话系统参照]] · [[来源登记]] · [[任务台本总索引]]\n')
put(CARD, n)
# incoming link + plan block
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S92特殊地点与野外NPC清点（当前登记）\n\n'
           f"[[特殊地点与野外NPC清点]]：只读枚举世界地图区域 {len(inv['map_regions'])}、特殊地点候选 {len(inv['rumor_sites'])}、地形类型 {len(inv['site_types'])}，"
           '并登记对白族规模（场景326/问候446/闲谈125/NPC227/随从8）。仅键名、序号、中文可用性与短地点名；逐NPC中英对读与地点设计卡为后续步骤。')
put(PLAN, block(a, z, (V / PLAN).read_text(encoding='utf-8-sig'), summary))
own = ROOT / 'research/special-location-note-hashes.json'
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
rule = ('\n<!-- SPECIAL-LOC-S92:BEGIN -->\n2026-10-13 S92：用户要求扩充特殊地点与野外NPC对白。'
        'research/special-location-inventory.json 只读清点原版特殊地点候选：8个世界地图区域、44个传闻地点、13个地形类型名与对白族规模（场景326/问候446/闲谈125/NPC227/随从8）；'
        '只存键名/STRG序号/中文可用性/短地点名，不存对白全文。入口design/01_原作基线/特殊地点与野外NPC清点.md；逐NPC中英对读、野外遭遇映射、Mod原创地点清点与地点设计卡仍待做。'
        'Probe-SpecialLocations.py与Write-SpecialLocationCard.py为作者工具，运行Validate-SpecialLocationInventory.py及既有设计检查；不部署游戏包。\n<!-- SPECIAL-LOC-S92:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- SPECIAL-LOC-S92:BEGIN -->.*?<!-- SPECIAL-LOC-S92:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- SPECIAL-LOC-S92:BEGIN -->.*?<!-- SPECIAL-LOC-S92:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/01_原作基线/特殊地点与野外NPC清点.md', '入口 [特殊地点与野外NPC清点](design/01_原作基线/特殊地点与野外NPC清点.md)'), encoding='utf-8')
print(json.dumps(dict(regions=len(inv['map_regions']), sites=len(inv['rumor_sites']), types=len(inv['site_types']), notes=len(generated)), ensure_ascii=False))
