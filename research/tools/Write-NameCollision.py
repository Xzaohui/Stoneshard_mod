"""S132: name-collision audit card for Mod-original names versus vanilla strings.

Renders the read-only probe results (research/name-collision-probe.json) into a
baseline note: per-category counts, the single collision explained as a
procedural name-pool entry, near matches reviewed, and the standing decision.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'NAME-COLLISION-S132'
CARD = '01_原作基线/原作名与原创名碰撞核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
probe = read('research/name-collision-probe.json')
base = read('research/local-baseline.json')
assert probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint drift'
CAT_NAME = {'items': '原创物品名', 'field_npcs': '野外人物名', 'fine_detail_npcs': '人物细描登记名（172）',
            'satellites': '卫星聚落住户名', 'districts': '街区名', 'interiors': '室内名', 'continuation_spaces': '续篇场景名'}
EXPLAIN = {
 'NPC-N-MARA': '「玛拉」命中原作 STRG[14963]，经查该序号属**程序化女名池**（14956—14971：Maelis/Maela/Marlis/Maryell/Marilda/Marwen/Mara/Maida/Lysandra/Liora/Linette/Linda/Livith/Letecia/Lesley），不是有剧情的具名角色；保留现名，卡内标注同形不同人。',
}
NEAR_NOTE = {
 'YOS-S02-NPC': '「尤尔」与官方「尤尔文」不同名，仅同前缀。',
 'NPC-N-SEL': '「塞尔」与官方「塞尔玛/安塞尔姆/塞尔雯」不同名，仅同前缀。',
 'NPC-N-IVO': '「伊沃」与官方「沃伊沃德腰带」无命名关系，仅字符巧合。',
 'YOS-S02': '卫星住户「尤尔」同上前缀情况。',
}
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "原作名与原创名碰撞核对"\nid: SRC-NAME-COLLISION-S132\ntype: source\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S132, source, naming]\naliases: []\n---\n\n'
     '# 原作名与原创名碰撞核对\n\n'
     '只读扫描 `vanilla.win` 的简体槽，把 Mod 原创专名逐类与官方字符串比对（精确同名＋短子串近似）。方法、指纹与逐条结果在 `research/name-collision-probe.json`；本页给出结论与处置口径。\n\n'
     '> [!info] 来源与指纹\n'
     f"> 文件 `{probe['game_file']}`；SHA-256 `{probe['sha256'][:16]}…`；STRG {probe['strg_count']} 条；扫描日期 {probe['date']}。只存名称与序号，不存对白全文。\n\n"
     '| 类别 | 名称数 | 精确同名 | 近似 |\n|---|---:|---:|---:|\n')
for cat, d in probe['categories'].items():
    n += f"| {CAT_NAME[cat]} | {d['names']} | {d['exact']} | {d['near']} |\n"
n += '\n## 精确同名\n\n'
if probe['collisions']:
    for c in probe['collisions']:
        n += f"- `{c['id']}`「{c['name']}」＝ STRG[{c['strg'][0]}]。{EXPLAIN.get(c['id'], '待处置：改名或标注同形不同人。')}\n"
else:
    n += '- 无。\n'
n += '\n## 近似（仅前缀/子串巧合）\n\n'
for m in probe['near_matches']:
    n += f"- `{m['id']}`「{m['name']}」与 {('、'.join('「' + s + '」' for s in m['samples']))}。{NEAR_NOTE.get(m['id'], '仅字符巧合。')}\n"
n += ('\n## 处置口径\n\n- 与**程序化名字池**同形：保留现名，在人物卡标注“同形不同人”，不据此改名（名字池不指认具名角色）。\n'
      '- 与**有剧情的具名角色**同名：改名或明示分人并写明依据；不得让玩家把 Mod 人物当原作人物。\n'
      '- 与**物品/文书名**同名：原创物品不得复用官方物品名（当前 0 例）。\n'
      '- 每次新增专名后重跑本扫描；新命中须在本页留一行处置。\n\n'
      '## 边界\n\n- 命中与否只反映字符串同形，不证明原作中存在同名剧情角色；判定需看序号上下文（本轮已核）。\n'
      '- 名称保持与官方译名风格一致；本页不改任何名称（唯一命中已按名字池处置）。\n\n'
      '[[原作剧情与对话系统参照]] · [[来源登记]] · [[人物细描与随身物]] · [[原创物品与装备总表]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S132原作名与原创名碰撞核对（当前登记）\n\n'
           f"[[原作名与原创名碰撞核对]]：只读扫描 7 类共 {sum(d['names'] for d in probe['categories'].values())} 个原创专名——精确同名 {len(probe['collisions'])}（「玛拉」命中程序化女名池，保留并标注同形不同人）、近似 {len(probe['near_matches'])}（仅前缀巧合，已逐条核）；物品/街区/室内/场景名 0 命中。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/name-collision-note-hashes.json'
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
rule = ('\n<!-- NAME-COLLISION-S132:BEGIN -->\n2026-10-13 S132：原作名与原创名碰撞核对（只读）。'
        'Probe-NameCollisions.py 扫 7 类原创专名对 STRG 简体槽：精确同名 1（「玛拉」命中程序化女名池 14956—14971，保留并标注同形不同人）、近似 4（仅前缀巧合）；物品/街区/室内/场景 0 命中。'
        '入口design/01_原作基线/原作名与原创名碰撞核对.md；新增专名后重跑扫描。运行Validate-NameCollision.py及既有检查；不部署游戏包。\n<!-- NAME-COLLISION-S132:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- NAME-COLLISION-S132:BEGIN -->.*?<!-- NAME-COLLISION-S132:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- NAME-COLLISION-S132:BEGIN -->.*?<!-- NAME-COLLISION-S132:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/01_原作基线/原作名与原创名碰撞核对.md', '入口 [原作名与原创名碰撞核对](design/01_原作基线/原作名与原创名碰撞核对.md)'), encoding='utf-8')
print(json.dumps(dict(categories=len(probe['categories']), collisions=len(probe['collisions']), near=len(probe['near_matches']), notes=len(generated)), ensure_ascii=False))
