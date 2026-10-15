"""S141: backfill an explicit R/X header block into city scripts that lack one.

The block is derived only from text already inside the script (method headings,
resolve_/paid_ keys, callback names); nothing new is authored. Insertion is
idempotent and the original text is never modified.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'RX-HEADER-S141'
CARD = '11_管理/R-X头部补齐记录.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
METHOD = re.compile(r'^###\s+([^\s：:]{1,24})[：:]\s*(.+?)\s*$', re.M)
KEY = re.compile(r'\b((?:resolve|paid)_[A-Za-z0-9_]+)')
LINK = re.compile(r'\[\[([^\]|#]+)')
HAS_RX = re.compile(r'当前R/X|R：方法与提交|RX-HEADER-S141:BEGIN')
rows = []
changed_files = {}
for p in sorted(list(V.rglob('台本_CS-*.md')) + list(V.rglob('台本_CM-*.md'))):
    text = p.read_text(encoding='utf-8')
    rel = 'design/' + str(p.relative_to(V)).replace('\\', '/')
    already = bool(HAS_RX.search(text))
    had_block = f'<!-- {MARK}:BEGIN -->' in text
    sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', text, re.S)
    body = sec.group(1) if sec else ''
    methods = [(m.group(1), m.group(2)) for m in METHOD.finditer(body)]
    keys = sorted(set(KEY.findall(text)))
    names = []
    for line in body.splitlines():
        if '：「' not in line and '：“' not in line:
            continue
        for lm in LINK.finditer(line):
            nm = lm.group(1).split('_')[-1]
            if nm not in names:
                names.append(nm)
    native = bool(re.search(r'当前R/X|R：方法与提交', text))
    rows.append(dict(file=rel, id=p.stem.split('_')[1], native=native, derived=(had_block or not native), inserted=not already, regenerated=had_block,
                     methods=[f'{a}：{b}' for a, b in methods], keys=keys, callbacks=names))
    if already and not had_block:
        continue
    h1 = re.search(r'^# .+$', text, re.M)
    assert h1, rel
    rx_lines = ['> [!note] R／X（S141 头部补齐）']
    rx_lines.append('> R（方法）：' + (' · '.join(f'`{a}` {b}' for a, b in methods) if methods else '见「可执行方案与回访」'))
    tail = []
    if keys:
        tail.append('写入键：' + '、'.join(f'`{k}`' for k in keys))
    if names:
        tail.append('回访：' + '、'.join(names))
    rx_lines.append('> X（后续）：' + ('；'.join(tail) if tail else '见「中断、缺席与不同到达顺序」'))
    rx_lines.append('> 本块由脚本内既有小节与键名生成，不新增设定、不改动既有文字。')
    block = (f'<!-- {MARK}:BEGIN -->\n' + '\n'.join(rx_lines) + f'\n<!-- {MARK}:END -->')
    if had_block:
        new = re.sub(re.escape(f'<!-- {MARK}:BEGIN -->') + '.*?' + re.escape(f'<!-- {MARK}:END -->'),
                     lambda _: block, text, flags=re.S)
    else:
        new = text[:h1.end()] + '\n\n' + block + text[h1.end():]
    stripped = re.sub(re.escape(f'<!-- {MARK}:BEGIN -->') + '.*?' + re.escape(f'<!-- {MARK}:END -->') + '\n*', '', new, flags=re.S)
    baseline = re.sub(re.escape(f'<!-- {MARK}:BEGIN -->') + '.*?' + re.escape(f'<!-- {MARK}:END -->') + '\n*', '', text, flags=re.S)
    assert stripped == baseline, 'insertion must not alter existing text: ' + rel
    changed_files[rel] = new
for rel, new in changed_files.items():
    p = V / rel[len('design/'):]
    p.write_text(preserve_foreign(V, rel[len('design/'):], new), encoding='utf-8')
out = dict(date='2026-10-13',
           scope='S141 R/X headers: derived header blocks for city scripts that lacked an explicit R/X section; derivation-only, no new content',
           scripts=rows, native=sum(1 for r in rows if r['native']), derived=sum(1 for r in rows if r['derived']),
           inserted_this_run=sum(1 for r in rows if r['inserted']))
(ROOT / 'research/rx-headers.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(changed_files); generated = {rel: sha(ROOT / rel) for rel in changed}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "R-X头部补齐记录"\nid: MGMT-RX-HEADERS-S141\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S141, review, screenplay]\naliases: []\n---\n\n'
     '# R-X头部补齐记录\n\n'
     f"按 S62「各台本顶部 R/X 为准」的口径核对城市稿：**{len(rows)} 篇**中 {out['native']} 篇原有 R/X 头（`当前R/X` 或 `R：方法与提交`），"
     f"**{out['derived']} 篇**带派生块。派生块只由脚本内既有内容生成——方法小节标题、`resolve_`／`paid_` 键与回访人物——不新增设定、不改动既有文字；插入前后逐篇比对，除新块外文本逐字相同。"
     "登记 `research/rx-headers.json`，工具 `research/tools/Write-RXHeaders.py`。\n\n"
     '## 派生规则\n\n'
     '- R（方法）：取「可执行方案与回访」小节内 `### 标签：名称` 标题，按原顺序列出；\n'
     '- X（后续）：取全篇 `resolve_*`／`paid_*` 键（去重排序）与同节回访行的人物链接名；\n'
     '- 块尾注明来源，便于后续维护者区分"原作文字"与"派生索引"。\n\n'
     '## 逐篇登记\n\n| 脚本 | 本轮插入 | 方法 | 写入键 | 回访人物 |\n| --- | --- | --- | --- | --- |\n')
for r in rows:
    n += (f"| {r['id']} | {'原有' if r['native'] else '派生'} | " +
          (' · '.join(f'`{m}`' for m in r['methods']) or '—') + ' | ' +
          ('、'.join(f'`{k}`' for k in r['keys']) or '—') + ' | ' +
          ('、'.join(r['callbacks']) or '—') + ' |\n')
n += ('\n## 边界\n\n'
      '- 派生块是索引，不是新设定；方法、键与回访名一律以脚本正文为准。\n'
      '- 校验器逐篇重算：块内方法与正文小节一致、键来自正文、插入不改变既有文字。\n'
      '- 主线／支线／日常／副本（`N`／`SQ`／`DT`／`D`）另有「可执行解法＋本任务影响的后事」与 `-R-` 键名体系，不属本次补齐范围。\n\n'
      '[[质量守卫总表]] · [[逐角色稿完成度核对]] · [[任务台本总索引]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BLOCK:BEGIN -->'; z = f'<!-- {MARK}:BLOCK:END -->'
blk = (a + f"\n## S141 R/X头部补齐（当前登记）\n\n[[R-X头部补齐记录]]：城市稿 {len(rows)} 篇中 {out['native']} 篇原有 R/X 头、{out['derived']} 篇带派生块（仅用脚本内既有方法、键与回访名，不改既有文字）。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/rx-headers-note-hashes.json'
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
rule = ('\n<!-- RX-HEADERS-S141:BEGIN -->\n2026-10-13 S141：R/X头部补齐。'
        f"城市稿{len(rows)}篇中{out['native']}篇原有R/X头、{out['derived']}篇带派生块（仅用脚本内既有方法小节、resolve_/paid_键与回访名，不新增设定、不改既有文字，逐篇比对保证只增块）。"
        'N/SQ/DT/D另用「可执行解法＋本任务影响的后事」与-R-键名，不在本次范围。'
        '入口design/11_管理/R-X头部补齐记录.md；运行Validate-RXHeaders.py及既有检查；不部署游戏包。\n<!-- RX-HEADERS-S141:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- RX-HEADERS-S141:BEGIN -->.*?<!-- RX-HEADERS-S141:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- RX-HEADERS-S141:BEGIN -->.*?<!-- RX-HEADERS-S141:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(scripts=len(rows), native=out['native'], derived=out['derived'], inserted_this_run=out['inserted_this_run']), ensure_ascii=False))
