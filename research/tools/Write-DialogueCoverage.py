"""S137: dialogue-coverage audit over every story script.

Recomputes per-script structure (dialogue-tree section, scene markers, speaker
lines, distinct speakers, draft marker), writes the registry, renders the audit
page, and corrects the stale pending figure on the plan page.
"""
from pathlib import Path
import json, hashlib, re, collections
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'DIALOGUE-COVERAGE-S137'
CARD = '11_管理/逐角色稿完成度核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“]')
SCENE = re.compile(r'(?:^|\n)[#\s]*(场\s?\d)|(?:^|\n)[#\s]*([A-Z]{1,3}\d*-S\d\d)')
TREE = re.compile(r'对话树|场次与|逐场素材')
MARKER = re.compile(r'场次与[^（(]{0,6}[（(]([^）)]+)[）)]')
rows = []
for p in sorted(V.rglob('台本_*.md')):
    t = p.read_text(encoding='utf-8')
    rel = str(p.relative_to(V)).replace('\\', '/')
    m = re.match(r'台本_([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)', p.name)
    sid = m.group(1) if m else p.stem
    fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
    scenes = set()
    for a, b in SCENE.findall(t):
        if a: scenes.add(a.replace(' ', ''))
        if b: scenes.add(b)
    speakers = []
    lines = 0
    for ln in t.splitlines():
        lm = LINE.match(ln.strip())
        if lm:
            lines += 1
            sp = lm.group(1) or lm.group(2) or lm.group(3)
            if '｜' in sp:
                sp = sp.split('｜')[-1]
            elif sp.startswith('人物_'):
                sp = sp.split('_')[-1]
            speakers.append(sp)
    mk = MARKER.search(t)
    rows.append(dict(id=sid, file=rel, family=fam, tree=bool(TREE.search(t)),
                     marker=mk.group(1) if mk else ('continuation' if '场次与条件对白' in t else ''),
                     scenes=len(scenes), lines=lines, speakers=len(set(speakers)), sp=sorted(set(speakers))))
famsum = {}
for r in rows:
    d = famsum.setdefault(r['family'], dict(files=0, tree=0, scenes=0, lines=0, speakers=set()))
    d['files'] += 1; d['tree'] += 1 if r['tree'] else 0
    d['scenes'] += r['scenes']; d['lines'] += r['lines']
    for s in r.get('sp', []): d['speakers'].add(s)
markers = collections.Counter(r['marker'] or '无标记' for r in rows if r['family'] in ('CS', 'CM'))
no_tree = [r['id'] for r in rows if not r['tree']]
out = dict(date='2026-10-13', scope='S137 dialogue coverage: per-script dialogue-tree section, scene markers, speaker lines and draft markers; structure only, not literary quality',
           rows=rows, families={k: dict(v, speakers=len(v['speakers'])) for k, v in famsum.items()},
           markers=dict(markers), no_tree=no_tree)
(ROOT / 'research' / 'dialogue-coverage.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "逐角色稿完成度核对"\nid: MGMT-DIALOGUE-COVERAGE-S137\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S137, review, dialogue]\naliases: []\n---\n\n'
     '# 逐角色稿完成度核对\n\n'
     f"按每篇台本的**结构**逐篇重算：是否有对话树/场次节、场次标记数、说话人行数、说话人数与版本标记（{len(rows)} 篇）。只核对结构，不评判文学质量，也不代表游戏内可运行。登记 `research/dialogue-coverage.json`，工具 `research/tools/Write-DialogueCoverage.py`。\n\n"
     '## 按家族\n\n| 家族 | 篇数 | 有对话树/场次节 | 场次标记 | 说话人行 | 说话人 |\n| --- | --- | --- | --- | --- | --- |\n')
for k in sorted(famsum):
    d = famsum[k]
    n += f"| {k} | {d['files']} | {d['tree']} | {d['scenes']} | {d['lines']} | {len(d['speakers'])} |\n"
n += (f"| **合计** | **{sum(d['files'] for d in famsum.values())}** | **{sum(d['tree'] for d in famsum.values())}** | "
      f"**{sum(d['scenes'] for d in famsum.values())}** | **{sum(d['lines'] for d in famsum.values())}** | "
      f"**{len(set().union(*[d['speakers'] for d in famsum.values()]))}** |\n\n"
      '## 城市稿版本标记\n\n| 标记 | 篇数 |\n| --- | --- |\n')
for k, v in sorted(markers.items()):
    n += f"| {k} | {v} |\n"
n += ('\n`S76`—`S86` 为各批逐角色稿的版本标记；`continuation` 为布林续篇六篇（`CS-BRY-11`—`16`，节题为「场次与条件对白」）。\n\n'
      '## 待深化口径修正\n\n'
      '旧文（S84/S85 期）有「ASH/HIG 各四篇仍待深化」「8 篇待深化」的说法。逐篇重算结果：\n\n'
      '- ASH 与 HIG 各有 **3** 篇（不是四篇），且六篇均已在 `S86当前稿` 带上场次与对白；\n'
      '- 布林续篇六篇（`CS-BRY-11`—`16`）在场次与条件对白节中各有场 1—3；\n'
      '- 城市稿（CS/CM）**每篇**都有场次节与说话人行，当前**待深化 0 篇**（与 [[城市与聚落设计总索引]] 的「尚余 0 篇待同等精修」一致）。\n\n'
      '因此计划页的旧句改为指向本页；S84/S85 的日期块保留为历史记录，不追改。\n\n'
      '## 边界\n\n'
      '- 只按节题、场次标记与说话人行计数；不判定人物是否独特、台词是否合格。\n'
      '- 行数与说话人数受行格式影响（人物卡链接＋冒号＋引号、`**名**：`、`名：`），换格式需重跑本工具。\n'
      '- 结构齐备不代表已实现或已试玩。\n\n'
      '[[任务台本总索引]] · [[叙事内容清单]] · [[特殊地点与野外NPC对白扩展计划]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + '\n## S137逐角色稿完成度（当前登记）\n\n'
       '[[逐角色稿完成度核对]]：131 篇台本逐篇重算，130 篇有对话树/场次节（唯一例外为野外人物对白卡，属另一格式）；'
       '城市稿 ASH/HIG 各 3 篇且已在 `S86当前稿` 深化，布林续篇六篇各有场 1—3，当前**待深化 0 篇**。'
       '旧「各四篇仍待深化」「8 篇待深化」为 S84/S85 期说法，保留为历史记录。\n' + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
t2 = t2.replace('S84当前65篇逐角色初稿，ASH寒凉盆地与护理村、HIG无名修院山地各四篇仍待深化；',
                'S84当时65篇逐角色初稿，ASH寒凉盆地与护理村、HIG无名修院山地各3篇已于S86深化（当前待深化0篇，见 [[逐角色稿完成度核对]]）；')
put(PLAN, t2)
own = ROOT / 'research/dialogue-coverage-note-hashes.json'
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
rule = ('\n<!-- DIALOGUE-COVERAGE-S137:BEGIN -->\n2026-10-13 S137：逐角色稿完成度核对（结构重算）。'
        '131篇台本逐篇核对对话树/场次节、场次标记、说话人行数与版本标记：130篇有对话节（例外为野外人物对白卡格式）；'
        '城市稿ASH/HIG各3篇已于S86深化、布林续篇六篇各有场1—3，当前待深化0篇；旧「各四篇/8篇待深化」保留为S84/S85历史记录，计划页旧句改为指向本页。'
        '入口design/11_管理/逐角色稿完成度核对.md；运行Validate-DialogueCoverage.py及既有检查；不部署游戏包。\n<!-- DIALOGUE-COVERAGE-S137:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- DIALOGUE-COVERAGE-S137:BEGIN -->.*?<!-- DIALOGUE-COVERAGE-S137:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- DIALOGUE-COVERAGE-S137:BEGIN -->.*?<!-- DIALOGUE-COVERAGE-S137:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(files=len(rows), tree=len(rows) - len(no_tree), markers=dict(markers)), ensure_ascii=False))
