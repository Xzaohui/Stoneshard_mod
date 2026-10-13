"""Render the authored town trust system into two vault notes.

- design/09_系统逻辑/城镇声望与信任系统.md (system + per-town design)
- design/09_系统逻辑/城镇声望系统中英对照.md (flat CN/EN string table)
Also attaches S87 registry blocks to known index notes and reconciles all
prior *note-hashes manifests the way earlier generators do.
"""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]
V = ROOT / 'design'
SRC = ROOT / 'research/town-reputation.json'
MARK = 'TOWN-REPUTATION-S87'
HP = ROOT / 'research/reputation-generated-note-hashes.json'
SYS_DOC = '09_系统逻辑/城镇声望与信任系统.md'
BIL_DOC = '09_系统逻辑/城镇声望系统中英对照.md'

def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def front(t, i, k): return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, S87, reputation]\naliases: []\n---\n\n# {t}\n\n'
def block(t, b):
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + b.rstrip() + '\n' + z
    return re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + n + '\n'

data = read('research/town-reputation.json')
model = read('research/city-campaign.json')
cast_names = {cid: {a['name'] for a in cast.values()} for cid, cast in model['dramatic_casts'].items()}
towns = data['towns']; by_id = {t['id']: t for t in towns}
scale = {b['value']: b for b in data['scale']}

# Verify manifests before writing (same protection as earlier generators).
manifests = {}
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    try:
        h = read('research/' + p.name)
    except Exception:
        continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()):
        continue
    for rel, expected in h.items():
        if sha(ROOT / rel) != expected:
            raise SystemExit('Preserve/reconcile prior note: ' + rel)
    manifests[p] = h

changed = set(); generated = {}
def put(rel, text, own=False):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8'); changed.add('design/' + rel)
    if own: generated['design/' + rel] = sha(p)

# ---------- system doc ----------
t = front('城镇声望与信任系统', 'SYS-TOWN-REPUTATION-S87', 'system')
t += '本页按用户2026-10-12要求设计：十五个地域各有独立城镇信任记录，中英对照；参照原作声誉分层与优秀RPG的分支/后果结构，但全部为Mod原创语义。设计字段尚未映射引擎；不改游戏包。使用的原作结构见[[原作剧情与对话系统参照]]，机制对照见[[参考游戏叙事与声望机制对照]]（后者为外部分析，不复制其情节）。\n\n'
t += '## 分层：三本账各记各的\n\n'
t += '| 层 | 内容 |\n| --- | --- |\n'
for layer in data['source_layers']:
    t += f"| {layer['name_cn']}（{layer['name_en']}） | {layer['note_cn']} |\n"
t += '\n原作声誉的聚落/阵营档位、来源明细与跨地传播均保持原作处理；本页新增层只做语气、有限服务与回访伏笔，不作结局资格，也不重复计同一行为。\n\n'
t += '## 五档刻度（全地域共用语义）\n\n| 档 | 类 | 名称 | Name | 行为 |\n| --- | --- | --- | --- | --- |\n'
for b in data['scale']:
    t += f"| {b['value']:+d} | {b['class']} | {b['name_cn']} | {b['name_en']} | {b['behavior_cn']}<br>{b['behavior_en']} |\n"
t += '\n## 写入与冻结规则\n\n'
for r in data['rules']:
    t += f"- **{r['id']}** {r['cn']}\n  <br>{r['en']}\n"
t += '\n## 界面与记录文案\n\n| 键 | 中文 | English |\n| --- | --- | --- |\n'
for k, label in [('label', '标签'), ('standing', '当前档'), ('changed', '变动提示'), ('record_title', '记录页标题'), ('legend', '记录页说明'), ('gate', '门槛提示'), ('freeze', '冻结提示')]:
    t += f"| TT-UI-{k.upper()} | {data['ui'][k + '_cn']} | {data['ui'][k + '_en']} |\n"
t += '\n## 跨城传递（一次性、明列）\n\n| 触发 | 起点 | 终点 | ± | 条件 |\n| --- | --- | --- | --- | --- |\n'
for x in data['transfers']:
    t += f"| {x['when']} | {x['from']} | {x['to']} | {x['delta']:+d} | {x['cn']}<br>{x['en']} |\n"
t += '\n同组（城联/王廷/灰军）的其他地区按原有‘听闻’进入对话，不自动换算成数字；传递条目需收到实际核验的账目或货物才写。\n\n'
t += '## 逐地域记录\n\n'
for town in towns:
    t += f"### {town['name_cn']}（{town['name_en']}）\n\n"
    t += '| 档 | 名称 | Name | 现场语气 |\n| --- | --- | --- | --- |\n'
    for b in town['bands']:
        t += f"| {b['value']:+d} | {b['name_cn']} | {b['name_en']} | {b['line_cn']}<br>{b['line_en']} |\n"
    t += '\n**写入**（实际执行且最小核验；每来源一次）：\n\n'
    for w in town['writes']:
        match = '、'.join(w['match'])
        t += f"- `{w['source']}`（{match}）：{w['delta']:+d}；{w['cn']} <br>{w['en']}\n"
    t += f"\n**接入回执**（`{town['receipt']['source']}`）：{town['receipt']['cn']} <br>{town['receipt']['en']}\n\n"
    t += f"**受托解锁**（{town['unlock']['anchor']}）：{town['unlock']['cn']} <br>{town['unlock']['en']}\n\n"
    t += f"**听闻**（来自{town['echo']['from']}；{town['echo']['anchor']}）：{town['echo']['cn']} <br>{town['echo']['en']}\n\n"
    t += f"**边界**：{town['limits']['cn']} <br>{town['limits']['en']}\n\n"
t += '[[系统逻辑索引]] · [[经济与奖励]] · [[势力关系总览]] · [[城市与聚落设计总索引]] · [[原作剧情与对话系统参照]]\n'
put(SYS_DOC, t, own=True)

# ---------- bilingual doc ----------
b = front('城镇声望系统中英对照', 'SYS-TOWN-REPUTATION-BILINGUAL-S87', 'system')
b += '本页为城镇信任系统的全部玩家可见文案中英对照，键为稳定ID（TT-*），中文为设计口径，English为对照译法。修改文案时先改`research/town-reputation.json`再重生成的系统页与本页；不在对白里暴露`N#/SQ#/DT#/resolve/paid`等后台标识。\n\n'
b += '## 通用界面\n\n| 键 | 中文 | English |\n| --- | --- | --- |\n'
for k in ['label', 'standing', 'changed', 'record_title', 'legend', 'gate', 'freeze']:
    b += f"| TT-UI-{k.upper()} | {data['ui'][k + '_cn']} | {data['ui'][k + '_en']} |\n"
b += '\n> 占位符：`{town}`＝城镇名，`{band}`＝档名。\n\n## 通用规则短句\n\n| 键 | 中文 | English |\n| --- | --- | --- |\n'
for r in data['rules']:
    b += f"| TT-RULE-{r['id']} | {r['cn']} | {r['en']} |\n"
b += '\n## 逐城镇档名与语气\n\n'
for town in towns:
    b += f"### {town['name_cn']} / {town['name_en']}\n\n| 键 | 中文 | English |\n| --- | --- | --- |\n"
    for bd in town['bands']:
        tag = f"TT-{town['id']}-B{abs(bd['value'])}{'M' if bd['value'] < 0 else 'P' if bd['value'] > 0 else '0'}"
        b += f"| {tag}-NAME | {bd['name_cn']} | {bd['name_en']} |\n"
        b += f"| {tag}-LINE | {bd['line_cn']} | {bd['line_en']} |\n"
    tag = f"TT-{town['id']}"
    b += f"| {tag}-UNLOCK | {town['unlock']['cn']} | {town['unlock']['en']} |\n"
    b += f"| {tag}-ECHO | {town['echo']['cn']} | {town['echo']['en']} |\n"
    b += f"| {tag}-LIMITS | {town['limits']['cn']} | {town['limits']['en']} |\n\n"
b += '[[城镇声望与信任系统]] · [[系统逻辑索引]]\n'
put(BIL_DOC, b, own=True)

# ---------- index blocks ----------
summary = '## S87城镇信任系统（当前登记）\n\n[[城镇声望与信任系统]] · [[城镇声望系统中英对照]]。十五个地域各一条五档记录（−2..+2），只写实际执行且最小核验的成果，每来源一次；与原作声誉、阵营承诺分账，罪行照原，低信任不锁主线与回程，N17后冻结。中英对照见专用页；数值未映射、游戏未验证。'
for name in ['系统逻辑索引', '经济与奖励', '势力关系总览', '城市与聚落设计总索引', '来源登记']:
    p = next(V.rglob(name + '.md'))
    rel = p.relative_to(V).as_posix()
    put(rel, block(p.read_text(encoding='utf-8-sig'), summary))

# ---------- manifest reconciliation ----------
for p, h in manifests.items():
    touched = False
    for rel in changed & set(h):
        h[rel] = sha(ROOT / rel); touched = True
    if touched:
        p.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
HP.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

rule = f'<!-- {MARK}:BEGIN -->\n2026-10-12 S87：用户要求设计各城镇声望系统并中英对照。research/town-reputation.json定义三层分账（原作声誉/阵营承诺/城镇信任），十五地域各五档（−2..+2）、逐条写入来源、接收入口、受托解锁、听闻与边界。入口design/09_系统逻辑/城镇声望与信任系统.md与[[城镇声望系统中英对照]]；只能实际执行且最小核验写入，每来源一次，±1（重大伤害−1），上限±2；不洗罪、不解锁无限物资、不锁主线与回程，N17后冻结；跨城仅明列传递。运行Validate-TownReputation.py及原三项设计检查；未映射引擎、未部署。\n<!-- {MARK}:END -->'
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md', ROOT / 'README.md']:
    body = p.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + rule.split('\n', 1)[1].rsplit('\n', 1)[0] + '\n' + z
    p.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + n + '\n')
print(json.dumps({'towns': len(towns), 'bands': sum(len(t['bands']) for t in towns), 'writes': sum(len(t['writes']) for t in towns), 'transfers': len(data['transfers']), 'generated': len(generated), 'changed_notes': len(changed)}, ensure_ascii=False))
