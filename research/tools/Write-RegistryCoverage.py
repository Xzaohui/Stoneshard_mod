"""S152: classify every research registry by how it is covered.

Coverage classes: validator-direct (filename in a validator), validator-indirect
(stem referenced, e.g. parameterised drama slugs), tool-output (written by a
writer/recorder but not validated), cited-log (cited from a design page),
baseline (the two shared inputs). Anything left unclassified fails the guard.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'REG-COVERAGE-S152'
CARD = '11_管理/登记文件覆盖分类.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
R = ROOT / 'research'
tools = {p.name: p.read_text(encoding='utf-8') for p in sorted((R / 'tools').glob('*.py'))}
val = {n: t for n, t in tools.items() if n.startswith('Validate-')}
writers = {n: t for n, t in tools.items() if n.startswith(('Write-', 'Record-', 'Probe-', 'Author-', 'Attach-')) or n == 'BrynnContinuation.py'}
pages = {str(p.relative_to(ROOT)).replace('\\', '/'): p.read_text(encoding='utf-8') for p in V.rglob('*.md')}
def stems(name):
    s = name[:-5]
    out = {s}
    for suf in ('-drama', '-feedback', '-s77', '-catalog', '-results', '-log', '-review', '-index', '-entries'):
        if s.endswith(suf):
            out.add(s[:-len(suf)])
    return {x for x in out if len(x) >= 4}
rows = []
for p in sorted(R.glob('*.json')):
    n = p.name
    if n.endswith(('-validation.json', '-note-hashes.json')):
        continue
    if n == 'registry-coverage.json':
        continue  # 元登记：本页自身，不参与分类
    if n in ('local-baseline.json', 'design-model.json'):
        rows.append(dict(file=n, cls='baseline', evidence='共享输入')); continue
    direct = [v for v, t in val.items() if n in t]
    if direct:
        rows.append(dict(file=n, cls='validator-direct', evidence='、'.join(sorted(direct)[:3]))); continue
    ind = [v for v, t in val.items() if any(s in t for s in stems(n))]
    if ind:
        rows.append(dict(file=n, cls='validator-indirect', evidence='、'.join(sorted(ind)[:3]))); continue
    wr = [w for w, t in writers.items() if n in t]
    if wr:
        rows.append(dict(file=n, cls='tool-output', evidence='、'.join(sorted(wr)[:3]))); continue
    cited = [k for k, t in pages.items() if n in t]
    if cited:
        rows.append(dict(file=n, cls='cited-log', evidence='、'.join(sorted(cited)[:2]))); continue
    rows.append(dict(file=n, cls='unclassified', evidence=''))
classes = {}
for r in rows:
    classes[r['cls']] = classes.get(r['cls'], 0) + 1
reg = dict(date='2026-10-13', scope='S152 registry coverage classification: how each research JSON is covered (validator direct/indirect, tool output, cited log, baseline); unclassified must be zero',
           rows=rows, classes=classes, unclassified=[r['file'] for r in rows if r['cls'] == 'unclassified'])
(R / 'registry-coverage.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "登记文件覆盖分类"\nid: MGMT-REG-COVERAGE-S152\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S152, review, registry]\naliases: []\n---\n\n'
     '# 登记文件覆盖分类\n\n'
     f"把 `research/` 下的登记 JSON（{len(rows)} 份，不含 `*-validation.json` 与清单）按**被谁覆盖**分类，回答“哪些数据有人验、哪些只是记录”。登记 `research/registry-coverage.json`，工具 `research/tools/Write-RegistryCoverage.py`。\n\n"
     '| 类别 | 份数 | 含义 |\n| --- | ---: | --- |\n')
LBL = {'validator-direct': '校验器直接读（源码出现文件名）', 'validator-indirect': '校验器间接读（参数化 slug／`feedback_source` 等）',
       'tool-output': '工具产物（写手/记录器生成，暂无校验器读）', 'cited-log': '调查记录（被设计页引用为证据）',
       'baseline': '共享输入（基线／设计模型）', 'unclassified': '未归类（守卫要求为 0）'}
for k in ('validator-direct', 'validator-indirect', 'tool-output', 'cited-log', 'baseline', 'unclassified'):
    n += f"| `{k}` | {classes.get(k, 0)} | {LBL[k]} |\n"
n += '\n## 规则\n\n'
n += ('- **新增“活输入”**（写手或校验器会读的登记）必须落进 `validator-direct` 或 `validator-indirect`：先在工具里写具体路径或可解析 slug，再重跑本页工具登记。\n'
      '- **工具产物**可以暂无校验器，但必须由已登记的工具生成；若它开始被别的工具读取，就会自动升级为前两类。\n'
      '- **调查记录**必须被至少一个设计页引用（否则读者无从发现），本页分类即为该引用的现场核对。\n'
      '- 出现 `unclassified` 即报错：先补引用、补工具或补校验器，再重跑。\n\n'
      '## 未归类清单\n\n' + ('无。\n\n' if not reg['unclassified'] else '、'.join('`' + x + '`' for x in reg['unclassified']) + '\n\n'))
n += ('## 边界\n\n'
      '- 分类只看“有没有人读/被引用”，不判断数据本身是否正确；数据正确性由各自校验器负责。\n'
      '- 间接读的判定基于 slug 词干匹配，可能与实际参数不同；登记里给出命中的校验器名以便复核。\n\n'
      '[[设计库生成与校验流程]] · [[质量守卫总表]] · [[来源登记]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S152登记文件覆盖分类（当前登记）\n\n[[登记文件覆盖分类]]：{len(rows)} 份登记按覆盖方式分类——校验器直接 {classes.get('validator-direct', 0)}、间接 {classes.get('validator-indirect', 0)}、工具产物 {classes.get('tool-output', 0)}、调查记录 {classes.get('cited-log', 0)}、共享输入 {classes.get('baseline', 0)}；未归类 0。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'registry-coverage-note-hashes.json'
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
rule = ('\n<!-- REG-COVERAGE-S152:BEGIN -->\n2026-10-13 S152：登记文件覆盖分类。'
        f"research/ 下 {len(rows)} 份登记按覆盖方式分类：校验器直接 {classes.get('validator-direct',0)}、间接 {classes.get('validator-indirect',0)}、工具产物 {classes.get('tool-output',0)}、调查记录 {classes.get('cited-log',0)}、共享输入 {classes.get('baseline',0)}；未归类 0。"
        '新增活输入须进前两类，工具产物须由已登记工具生成，调查记录须被设计页引用；出现未归类即报错。'
        '入口design/11_管理/登记文件覆盖分类.md；运行Validate-RegistryCoverage.py及既有检查。\n<!-- REG-COVERAGE-S152:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- REG-COVERAGE-S152:BEGIN -->.*?<!-- REG-COVERAGE-S152:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- REG-COVERAGE-S152:BEGIN -->.*?<!-- REG-COVERAGE-S152:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(registries=len(rows), classes=classes, unclassified=len(reg['unclassified'])), ensure_ascii=False))
