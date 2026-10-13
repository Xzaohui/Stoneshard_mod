"""Validate that no undocumented placeholder markers remain in the design corpus."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
allow = json.loads((ROOT / 'research/placeholder-allowlist.json').read_text(encoding='utf-8'))
CODE = re.compile(r'`[^`]*`')
pats = [(t, re.compile(re.escape(t))) for t in allow['patterns']]
allowed = {(e['file'], e['term']) for e in allow['entries']}
exclude = set(allow.get('exclude_files', []))
hits = []
for p in sorted(V.rglob('*.md')):
    rel = 'design/' + str(p.relative_to(V)).replace('\\', '/')
    if rel in exclude:
        continue
    text = CODE.sub('``', p.read_text(encoding='utf-8'))
    for term, rx in pats:
        for m in rx.finditer(text):
            hits.append((rel, term))
for rel, term in hits:
    check((rel, term) in allowed, 'allowlisted-' + rel + ':' + term)
for e in allow['entries']:
    check((e['file'], e['term']) in hits, 'allowlist-entry-used-' + e['file'] + ':' + e['term'])
    check(bool(e.get('reason')), 'allowlist-reason-' + e['file'])
card = (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8')
check('占位扫描' in card and str(len(hits)) in card, 'card-placeholder-numbers')
report = dict(date='2026-10-13', scope='S140 placeholder scan: every TODO/FIXME/占位-family hit is documented in the allowlist; static, not runtime',
              hits=len(hits), allowlisted=len(allowed), checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(ROOT / 'research/placeholder-scan-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
