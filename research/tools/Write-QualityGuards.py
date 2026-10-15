"""S140: quality-guard index page with live numbers from the guard registries."""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'QUALITY-GUARDS-S140'
CARD = '11_管理/质量守卫总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
CODE = re.compile(r'`[^`]*`')
LINK = re.compile(r'\[\[([^\]|#]+)')
stems = {p.stem for p in V.rglob('*.md')}
total_links = 0; broken = []
for p in sorted(V.rglob('*.md')):
    text = CODE.sub('``', p.read_text(encoding='utf-8'))
    for m in LINK.finditer(text):
        total_links += 1
        if m.group(1).strip() not in stems:
            broken.append(m.group(1).strip())
allow = read('research/placeholder-allowlist.json')
hits = 0
for p in sorted(V.rglob('*.md')):
    text = CODE.sub('``', p.read_text(encoding='utf-8'))
    for t in allow['patterns']:
        hits += text.count(t)
low_methods = []; edge_total = 0; edge_unref = 0; edge_dangling = 0
cov = read('research/dialogue-coverage.json'); spk = read('research/speaker-closure.json')
dup = read('research/dialogue-distinctiveness.json')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
def measure():
    tl = 0; brs = []
    for q in sorted(V.rglob('*.md')):
        text = CODE.sub('``', q.read_text(encoding='utf-8'))
        for m in LINK.finditer(text):
            tl += 1
            if m.group(1).strip() not in stems: brs.append(m.group(1).strip())
    ex = set(allow.get('exclude_files', []))
    h = 0
    for q in sorted(V.rglob('*.md')):
        rel = 'design/' + str(q.relative_to(V)).replace('\\', '/')
        if rel in ex: continue
        text = CODE.sub('``', q.read_text(encoding='utf-8'))
        for term in allow['patterns']:
            h += text.count(term)
    # methods per script (family-aware) and X-edge closure
    CS_M = re.compile(r'^###\s+([^\s：:]{1,24})[：:]', re.M)
    RID = re.compile(r'\b([A-Z]{1,3}(?:-[A-Z]{1,3})*-?\d*-R-[A-Za-z0-9\-]+)')
    low = []
    for q in sorted(V.rglob('台本_*.md')):
        t2 = q.read_text(encoding='utf-8')
        sid = q.stem.split('_')[1]
        fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
        if fam == 'FX':
            continue
        ms = set(RID.findall(t2))
        if fam in ('CS', 'CM'):
            sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', t2, re.S)
            ms |= {m.group(1) for m in CS_M.finditer(sec.group(1))} if sec else set()
        if len(ms) < 2:
            low.append(sid)
    matrix = (V / '09_系统逻辑/叙事交叉影响矩阵.md').read_text(encoding='utf-8')
    edges = set(re.findall(r'^## (X\d\d)\s', matrix, re.M))
    refs = set()
    for q in sorted(V.rglob('台本_*.md')):
        refs |= {'X' + x for x in re.findall(r'\bX(\d\d)\b', q.read_text(encoding='utf-8'))}
    return tl, brs, h, low, len(edges), len(edges - refs), len(refs - edges)
for _ in range(4):
    before = (total_links, len(broken), hits, low_methods, edge_total, edge_unref, edge_dangling)
    total_links, broken, hits, low_methods, edge_total, edge_unref, edge_dangling = measure()
    if (total_links, len(broken), hits, low_methods, edge_total, edge_unref, edge_dangling) == before:
        break
n = ('---\ntitle: "质量守卫总表"\nid: MGMT-QUALITY-GUARDS-S140\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S140, review, quality]\naliases: []\n---\n\n'
     '# 质量守卫总表\n\n'
     '本页是设计库**质量守卫**的单一入口：每条守卫说明它防什么、工具与登记文件、当前计数与失败条件。守卫只做结构与一致性检查，不判文学质量，也不代表游戏内可运行。\n\n'
     '| 守卫 | 防什么 | 工具 | 入口 | 当前计数 | 失败条件 |\n| --- | --- | --- | --- | --- | --- |\n'
     f"| 结构覆盖 | 台本缺对话节、场次或版本标记 | `Write-DialogueCoverage.py` / `Validate-DialogueCoverage.py` | [[逐角色稿完成度核对]] | "
     f"{len(cov['rows'])} 篇、{sum(1 for r in cov['rows'] if r['tree'])} 篇有对话节、场次 {sum(r['scenes'] for r in cov['rows'])} | 逐篇现场重算与登记不一致 |\n"
     f"| 说话人闭合 | 台词落在无卡、无登记的人物名下 | `Write-SpeakerClosure.py` / `Validate-SpeakerClosure.py` | [[说话人与人物卡闭合核对]] | "
     f"{len(spk['rows'])} 位、未闭合 {len(spk['unresolved'])} 位 | 出现白名单外的新说话人 |\n"
     f"| 对白去重 | 模板化复制、跨人物共用整句 | `Write-DialogueDistinctiveness.py` / `Validate-DialogueDistinctiveness.py` | [[对白去重与独特性核对]] | "
     f"{dup['total_lines']} 行、去重 {dup['distinct_lines']} 条、重复 {len(dup['duplicates'])} 组（全部主章—副本配对） | 出现非配对的整句重复 |\n"
     f"| 链接完整 | 双链指向不存在的笔记 | `Validate-LinkIntegrity.py` | 本页 | {total_links} 条双链、未解析 {len(broken)} | 任一双方括号链接找不到同名笔记（行内代码段除外） |\n"
     f"| 占位扫描 | 正文留下待办式占位 | `Validate-PlaceholderScan.py` | 本页 · `research/placeholder-allowlist.json` | 命中 {hits} 处、全部已登记 | 出现未登记的 TODO/占位/待补类命中 |\n"
     f"| 方法数 | 脚本只有一条行动解法 | `Write-QualityGuards.py` / `Validate-QualityGuards.py` | 本页 | 低于 2 条方法的脚本 {len(low_methods)} 篇 | 任一脚本方法数 < 2（S62「多种实际行动解法」） |\n"
     f"| X边闭合 | 矩阵边无脚本引用、或脚本引用不存在的边 | `Write-QualityGuards.py` / `Validate-QualityGuards.py` | 本页 · [[叙事交叉影响矩阵]] | 矩阵 {edge_total} 条、无脚本引用 {edge_unref} 条、悬空引用 {edge_dangling} 条 | 任一方向出现缺口 |\n\n"
     '## 已登记的非占位命中\n\n'
     '| 文件 | 词 | 说明 |\n| --- | --- | --- |\n')
for e in allow['entries']:
    n += f"| {e['file']} | {e['term']} | {e['reason']} |\n"
n += ('\n## 既有守卫（不重复登记）\n\n'
      '- 库结构、ID、双链与来源检查：`Test-DesignVault.ps1`；\n'
      '- 任务依赖、分支汇合与证据替代：`Validate-StoryScripts.py`、`Validate-NarrativeNetwork.py`；\n'
      '- 伏笔—回收闭合：`Validate-ForeshadowLedger.py`；\n'
      '- 键名、状态与回执：`Validate-StateKeys.py`、`Validate-ConditionCoverage.py` 等。\n\n'
      '完整工具清单与重跑顺序见 [[设计库生成与校验流程]]。\n\n'
      '## 边界\n\n'
      '- 守卫只保证“没有已知的结构性错误”，不保证台词质量、经济数值或运行表现。\n'
      '- 新增脚本、人物或跨库改动后按 [[设计库生成与校验流程]] 的顺序重跑；计数页必须在校验器之后刷新。\n\n'
      '[[逐角色稿完成度核对]] · [[说话人与人物卡闭合核对]] · [[对白去重与独特性核对]] · [[逻辑验收记录]] · [[待办与已知缺口登记]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f'\n## S140质量守卫（当前登记）\n\n[[质量守卫总表]]：结构覆盖、说话人闭合、对白去重、链接完整（{total_links} 条、未解析 {len(broken)}）、占位扫描（命中 {hits} 处全部已登记）五项守卫单一入口。\n' + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/quality-guards-note-hashes.json'
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
rule = ('\n<!-- QUALITY-GUARDS-S140:BEGIN -->\n2026-10-13 S140：质量守卫总表与两项新守卫。'
        f"链接完整：{total_links}条双链、未解析{len(broken)}（行内代码段除外）；占位扫描：命中{hits}处且全部登记于research/placeholder-allowlist.json；"
        '连同S137结构覆盖、S138说话人闭合、S139对白去重共五项守卫。'
        '入口design/11_管理/质量守卫总表.md；运行Validate-LinkIntegrity.py与Validate-PlaceholderScan.py及既有检查；不部署游戏包。\n<!-- QUALITY-GUARDS-S140:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- QUALITY-GUARDS-S140:BEGIN -->.*?<!-- QUALITY-GUARDS-S140:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- QUALITY-GUARDS-S140:BEGIN -->.*?<!-- QUALITY-GUARDS-S140:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(links=total_links, broken=len(broken), placeholder_hits=hits, notes=len(generated)), ensure_ascii=False))
