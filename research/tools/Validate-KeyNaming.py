"""Validate the S123 key-naming reconciliation and its pointer blocks."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
kn = read('research/key-naming-reconciliation.json')
sk = read('research/state-keys.json'); keys = {x['key'] for x in sk['keys']}
stems = {p.stem for p in V.rglob('*.md')}
check(len(kn['mapping']) == 7, 'mapping-7')
PAT = re.compile(r'[a-z_]*resolve[A-Za-z_]*|[a-z_]*encountered[A-Za-z_]*|[a-z_]*receipt[A-Za-z_]*|[a-z_]*callback[A-Za-z_]*|[a-z_]*consent[A-Za-z_]*|[a-z_]*paid[A-Za-z_]*')
STRIP = re.compile(r'<!--\s*[A-Z0-9-]+:BEGIN\s*-->.*?<!--\s*[A-Z0-9-]+:END\s*-->', re.S)
BARE_WORDS = {'resolve', 'resolved'}
for rel, names in kn['legacy_found'].items():
    t = STRIP.sub('', (V / rel).read_text(encoding='utf-8'))
    live = sorted({m.group(0) for m in PAT.finditer(t)} - BARE_WORDS)
    check(names == live, 'legacy-list-' + Path(rel).stem)
    for x in names:
        check(any(m['legacy'] == x for m in kn['mapping']), 'legacy-mapped-' + x)
SAMPLES = {'resolve_<脚本ID>': 'resolve_CS_BRY_01', 'encountered_<脚本ID>': 'encountered_CS_BRY_01',
           'callback_<脚本ID>_<路线>': 'callback_CS_BRY_01_continuity', 'consent_<脚本ID>_<路线>': 'consent_CS_BRY_01_continuity',
           'paid_<脚本ID>_<路线>': 'paid_CS_BRY_01_continuity', 'receipt_<回执ID>': 'receipt_CX01', 'resolve_<CM-XXX>': 'resolve_CM_BRY'}
for m in kn['mapping']:
    s = SAMPLES[m['current']]
    check(s in keys, 'current-sample-' + s)
    check(m['status'] in ('refined', 'renamed', 'same'), 'status-' + m['legacy'])
card = (V / '09_系统逻辑/键名口径对账.md').read_text(encoding='utf-8')
check('# 键名口径对账' in card and '## 规则' in card and '## 边界' in card, 'card-structure')
for m in kn['mapping']:
    check(f"`{m['legacy']}` | `{m['current']}`" in card, 'card-row-' + m['legacy'])
for rel in kn['legacy_found']:
    check(f"[[{Path(rel).stem}]]" in card, 'card-legacy-note-' + Path(rel).stem)
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
for rel in ['09_系统逻辑/当前任务依赖与状态字典.md', '09_系统逻辑/网状叙事与条件对话规范.md']:
    t = (V / rel).read_text(encoding='utf-8')
    check('KEY-NAMES-S123:BEGIN' in t and '[[键名口径对账]]' in t, 'pointer-' + Path(rel).stem)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('KEY-NAMES-S123:BEGIN' in plan and '[[键名口径对账]]' in plan, 'plan-block-and-link')
check('KEY-NAMES-S123:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/key-naming-note-hashes.json')
check(len(h) == 4, 'own-manifest-4')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S123 key naming: legacy names recomputed from notes, mapping rows, current samples exist, pointer blocks, rendering and chain; not engine fields or save migration',
              mapping=len(kn['mapping']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/key-naming-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
