"""Validate the S142 quality-guard table numbers against live recomputation."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
CODE = re.compile(r'`[^`]*`'); LINK = re.compile(r'\[\[([^\]|#]+)')
CS_M = re.compile(r'^###\s+([^\s：:]{1,24})[：:]', re.M)
RID = re.compile(r'\b([A-Z]{1,3}(?:-[A-Z]{1,3})*-?\d*-R-[A-Za-z0-9\-]+)')
allow = read('research/placeholder-allowlist.json')
cov = read('research/dialogue-coverage.json'); spk = read('research/speaker-closure.json')
dup = read('research/dialogue-distinctiveness.json')
stems = {p.stem for p in V.rglob('*.md')}
links = 0; broken = []
for q in sorted(V.rglob('*.md')):
    text = CODE.sub('``', q.read_text(encoding='utf-8'))
    for m in LINK.finditer(text):
        links += 1
        if m.group(1).strip() not in stems: broken.append(m.group(1).strip())
ex = set(allow.get('exclude_files', [])); hits = 0
for q in sorted(V.rglob('*.md')):
    rel = 'design/' + str(q.relative_to(V)).replace('\\', '/')
    if rel in ex: continue
    text = CODE.sub('``', q.read_text(encoding='utf-8'))
    for term in allow['patterns']: hits += text.count(term)
low = []
for q in sorted(V.rglob('台本_*.md')):
    t = q.read_text(encoding='utf-8'); sid = q.stem.split('_')[1]
    fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
    if fam == 'FX': continue
    ms = set(RID.findall(t))
    if fam in ('CS', 'CM'):
        sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', t, re.S)
        if sec: ms |= {m.group(1) for m in CS_M.finditer(sec.group(1))}
    if len(ms) < 2: low.append(sid)
matrix = (V / '09_系统逻辑/叙事交叉影响矩阵.md').read_text(encoding='utf-8')
edges = set(re.findall(r'^## (X\d\d)\s', matrix, re.M)); refs = set()
for q in sorted(V.rglob('台本_*.md')):
    refs |= {'X' + x for x in re.findall(r'\bX(\d\d)\b', q.read_text(encoding='utf-8'))}
card = (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8')
expect = [
    f"{len(cov['rows'])} 篇、{sum(1 for r in cov['rows'] if r['tree'])} 篇有对话节、场次 {sum(r['scenes'] for r in cov['rows'])}",
    f"{len(spk['rows'])} 位、未闭合 {len(spk['unresolved'])} 位",
    f"{dup['total_lines']} 行、去重 {dup['distinct_lines']} 条、重复 {len(dup['duplicates'])} 组（全部主章—副本配对）",
    f"{links} 条双链、未解析 {len(broken)}",
    f"命中 {hits} 处、全部已登记",
    f"低于 2 条方法的脚本 {len(low)} 篇",
    f"矩阵 {len(edges)} 条、无脚本引用 {len(edges - refs)} 条、悬空引用 {len(refs - edges)} 条",
]
for e in expect:
    check(e in card, 'row-' + e[:26])
check(len(re.findall(r'^\| (?:结构覆盖|说话人闭合|对白去重|链接完整|占位扫描|方法数|X边闭合) ', card, re.M)) == 7, 'seven-guard-rows')
check(not broken, 'no-broken-links')
check(not low, 'no-low-method-scripts')
check(edges == refs and len(edges) == 74, 'edge-closure')
check(hits == len(allow['entries']), 'placeholder-allowlist-complete')
for sec in ('## 已登记的非占位命中', '## 既有守卫（不重复登记）', '## 边界'):
    check(sec in card, 'section-' + sec)
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
report = dict(date='2026-10-13', scope='S142 quality-guard table: seven guard rows recomputed live (coverage, speakers, duplicates, links, placeholders, methods, X edges); static, not runtime',
              guards=7, links=links, low_method_scripts=len(low), edges=len(edges),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/quality-guards-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
