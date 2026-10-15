"""Validate the S138 speaker-closure audit against the live notes."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“]')
reg = read('research/speaker-closure.json'); allow = read('research/speaker-allowlist.json')
cov = read('research/dialogue-coverage.json')
card_names = {p.stem.split('_')[-1] for p in V.rglob('人物_*.md')}
card_bodies = [(p, p.read_text(encoding='utf-8')) for p in V.rglob('人物_*.md')]
def classify(s):
    if s in allow['player']: return 'player'
    if s in card_names: return 'card-exact'
    for c in sorted(card_names):
        if c.startswith(s + '·') or c.startswith(s): return 'card-prefix'
    if s in allow['generic_roles']: return 'generic'
    if s in allow['labels']: return 'label'
    for p, body in card_bodies:
        if s in body: return 'card-mention'
    return 'unresolved'
live = {}
for p in sorted(V.rglob('台本_*.md')):
    for ln in p.read_text(encoding='utf-8').splitlines():
        m = LINE.match(ln.strip())
        if not m: continue
        raw = (m.group(1) or m.group(2) or m.group(3)).strip()
        s = raw.split('｜')[-1].strip().strip('[]').strip()
        if s.startswith('人物_'): s = s.split('_')[-1]
        d = live.setdefault(s, dict(lines=0, files=set()))
        d['lines'] += 1; d['files'].add(p.stem)
check(len(reg['rows']) == len(live), 'speaker-count-live')
check(sum(r['lines'] for r in reg['rows']) == sum(d['lines'] for d in live.values()), 'line-total-live')
check(sum(r['lines'] for r in reg['rows']) == sum(r['lines'] for r in cov['rows']), 'line-total-matches-coverage')
for r in reg['rows']:
    lv = live.get(r['speaker'])
    check(lv is not None, 'live-speaker-' + r['speaker'])
    if lv:
        check(r['lines'] == lv['lines'], 'lines-' + r['speaker'])
        check(set(r['files']) == lv['files'], 'files-' + r['speaker'])
    check(r['cls'] == classify(r['speaker']), 'class-' + r['speaker'])
    check(r['cls'] != 'unresolved', 'resolved-' + r['speaker'])
used = {r['speaker'] for r in reg['rows']}
for s in allow['generic_roles'] + allow['labels'] + allow['player']:
    check(s in used, 'allowlist-used-' + s)
check(reg['unresolved'] == [], 'no-unresolved')
for s in used:
    check(classify(s) != 'unresolved', 'classified-' + s)
card = (V / '11_管理/说话人与人物卡闭合核对.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 归类结果', '## 落到人物卡的说话人', '## 通用称谓与标记（不建人物卡）', '## 未闭合', '## 边界'):
    check(sec in card, 'section-' + sec)
for k, v in reg['classes'].items():
    check(f"| {k} | {v} |" in card, 'card-class-' + k)
check(f"| **合计** | **{len(reg['rows'])}** |" in card, 'card-total')
check('未发现未闭合说话人' in card, 'card-no-unresolved')
for r in reg['rows']:
    if r['cls'].startswith('card-'):
        check(f"| {r['speaker']} | {r['lines']} |" in card, 'card-row-' + r['speaker'])
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('SPEAKER-CLOSURE-S138:BEGIN' in plan and '[[说话人与人物卡闭合核对]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('SPEAKER-CLOSURE-S138:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/speaker-closure-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S138 speaker closure: live speaker extraction vs registry, classification of every speaker, allowlist usage, page rows, links and chain; structure only, not runtime',
              speakers=len(reg['rows']), classes=reg['classes'], checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(ROOT / 'research/speaker-closure-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
