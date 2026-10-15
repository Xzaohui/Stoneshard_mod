"""Validate the S139 dialogue distinctiveness audit against the live notes."""
from pathlib import Path
import json, hashlib, re, collections
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“](.+?)[」”]')
reg = read('research/dialogue-distinctiveness.json')
cov = read('research/dialogue-coverage.json')
live = collections.defaultdict(list); total = 0
for p in sorted(V.rglob('台本_*.md')):
    m = re.match(r'台本_([A-Za-z0-9]+)', p.name)
    fam = m.group(1)[:1] if m else '?'
    for ln in p.read_text(encoding='utf-8').splitlines():
        lm = LINE.match(ln.strip())
        if not lm: continue
        total += 1
        raw = (lm.group(1) or lm.group(2) or lm.group(3)).strip()
        s = raw.split('｜')[-1].strip().strip('[]').strip()
        if s.startswith('人物_'): s = s.split('_')[-1]
        live[lm.group(4).strip()].append(dict(file=p.stem, fam=fam, speaker=s))
check(reg['total_lines'] == total, 'total-lines-live')
check(total == sum(r['lines'] for r in cov['rows']), 'total-matches-coverage')
check(reg['distinct_lines'] == len(live), 'distinct-live')
live_dups = {t: occ for t, occ in live.items() if len(occ) > 1 and len(t) > 8}
check(len(reg['duplicates']) == len(live_dups), 'dup-count-live')
for d in reg['duplicates']:
    occ = live_dups.get(d['text'])
    check(occ is not None, 'dup-live-' + d['text'][:16])
    if occ is None: continue
    check(d['files'] == [o['file'] for o in occ], 'dup-files-' + d['text'][:16])
    check(d['speaker'] == occ[0]['speaker'] and len({o['speaker'] for o in occ}) == 1, 'dup-speaker-' + d['text'][:16])
    check(d['cls'] == 'pair', 'dup-class-' + d['text'][:16])
    check({o['fam'] for o in occ} == {'N', 'D'} and len(occ) == 2, 'dup-pair-shape-' + d['text'][:16])
check(reg['classes'].get('pair', 0) == len(reg['duplicates']), 'all-pairs')
card = (V / '11_管理/对白去重与独特性核对.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 口径', '## 主章—副本配对', '## 待复核', '## 分布观察', '## 边界'):
    check(sec in card, 'section-' + sec)
check(f"共 **{total} 行**、去重后 **{len(live)} 条**" in card, 'card-totals')
check('未发现需复核的重复' in card, 'card-no-review')
for d in reg['duplicates']:
    check(f"| {d['speaker']} | {d['text']} |" in card, 'card-dup-' + d['text'][:16])
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('DIALOGUE-DISTINCT-S139:BEGIN' in plan and '[[对白去重与独特性核对]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('DIALOGUE-DISTINCT-S139:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/dialogue-distinctiveness-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S139 dialogue distinctiveness: live duplicate extraction vs registry, pair-only duplicates, page rows, links and chain; exact match only, not runtime',
              total_lines=total, distinct_lines=len(live), duplicates=len(reg['duplicates']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/dialogue-distinctiveness-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
