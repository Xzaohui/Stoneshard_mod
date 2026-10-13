"""Validate the S137 dialogue-coverage audit against the live notes."""
from pathlib import Path
import json, hashlib, re, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“]')
SCENE = re.compile(r'(?:^|\n)[#\s]*(场\s?\d)|(?:^|\n)[#\s]*([A-Z]{1,3}\d*-S\d\d)')
TREE = re.compile(r'对话树|场次与|逐场素材')
MARKER = re.compile(r'场次与[^（(]{0,6}[（(]([^）)]+)[）)]')
reg = read('research/dialogue-coverage.json')
# live recomputation
live = {}
for p in sorted(V.rglob('台本_*.md')):
    t = p.read_text(encoding='utf-8')
    m = re.match(r'台本_([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)', p.name)
    sid = m.group(1) if m else p.stem
    fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
    scenes = set()
    for a, b in SCENE.findall(t):
        if a: scenes.add(a.replace(' ', ''))
        if b: scenes.add(b)
    lines = 0; speakers = set()
    for ln in t.splitlines():
        lm = LINE.match(ln.strip())
        if lm:
            lines += 1
            sp = lm.group(1) or lm.group(2) or lm.group(3)
            if '｜' in sp: sp = sp.split('｜')[-1]
            elif sp.startswith('人物_'): sp = sp.split('_')[-1]
            speakers.add(sp)
    mk = MARKER.search(t)
    live[sid] = dict(family=fam, tree=bool(TREE.search(t)), scenes=len(scenes), lines=lines,
                     speakers=len(speakers), marker=mk.group(1) if mk else ('continuation' if '场次与条件对白' in t else ''))
check(len(reg['rows']) == len(live) == 131, 'file-count-131')
for r in reg['rows']:
    lv = live.get(r['id'])
    check(lv is not None, 'id-present-' + r['id'])
    if lv is None: continue
    check(r['family'] == lv['family'], 'family-' + r['id'])
    check(r['tree'] == lv['tree'], 'tree-' + r['id'])
    check(r['scenes'] == lv['scenes'], 'scenes-' + r['id'])
    check(r['lines'] == lv['lines'], 'lines-' + r['id'])
    check(r['speakers'] == lv['speakers'], 'speakers-' + r['id'])
    check(r['marker'] == lv['marker'], 'marker-' + r['id'])
check(reg['no_tree'] == ['FX'], 'fx-only-without-tree')
fam = collections.Counter(r['family'] for r in reg['rows'])
for k, v in fam.items():
    check(reg['families'][k]['files'] == v, 'fam-files-' + k)
    check(reg['families'][k]['tree'] == sum(1 for r in reg['rows'] if r['family'] == k and r['tree']), 'fam-tree-' + k)
check(reg['markers'].get('continuation') == 6, 'continuation-six')
card = (V / '11_管理/逐角色稿完成度核对.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 按家族', '## 城市稿版本标记', '## 待深化口径修正', '## 边界'):
    check(sec in card, 'section-' + sec)
for k, d in reg['families'].items():
    check(f"| {k} | {d['files']} | {d['tree']} | {d['scenes']} | {d['lines']} | {d['speakers']} |" in card, 'card-row-' + k)
check('待深化 0 篇' in card or '**待深化 0 篇**' in card, 'card-zero-pending')
check('ASH 与 HIG 各有 **3** 篇' in card, 'card-ash-hig-three')
check('`CS-BRY-11`—`16`' in card or 'CS-BRY-11' in card, 'card-continuation-six')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('DIALOGUE-COVERAGE-S137:BEGIN' in plan and '[[逐角色稿完成度核对]]' in plan, 'plan-block')
check('S84当前65篇逐角色初稿' not in plan, 'old-live-line-gone')
check('各3篇已于S86深化' in plan, 'plan-corrected-line')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('DIALOGUE-COVERAGE-S137:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/dialogue-coverage-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S137 dialogue coverage: per-script live recomputation vs registry, page rows, plan correction, links and chain; structure only, not runtime',
              files=len(reg['rows']), tree=sum(1 for r in reg['rows'] if r['tree']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/dialogue-coverage-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
