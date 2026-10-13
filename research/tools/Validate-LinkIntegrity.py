"""Validate corpus link integrity: every wikilink outside code spans resolves."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
CODE = re.compile(r'`[^`]*`')
LINK = re.compile(r'\[\[([^\]|#]+)')
stems = {p.stem for p in V.rglob('*.md')}
files = sorted(V.rglob('*.md'))
total = 0; targets = set(); broken = {}
for p in files:
    text = CODE.sub('``', p.read_text(encoding='utf-8'))
    for m in LINK.finditer(text):
        t = m.group(1).strip()
        total += 1; targets.add(t)
        if t not in stems:
            broken.setdefault(t, []).append(str(p.relative_to(V)).replace('\\', '/'))
check(len(files) >= 600, 'file-count')
check(total >= 12000, 'link-count')
check(not broken, 'all-links-resolve')
for t, where in broken.items():
    check(False, 'broken-' + t + '@' + where[0])
card = (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8')
check('链接完整' in card and str(total) in card, 'card-link-numbers')
check('未解析 0' in card or '未解析：0' in card, 'card-link-zero')
report = dict(date='2026-10-13', scope='S140 link integrity: every wikilink outside code spans resolves to a note stem; static, not runtime',
              files=len(files), links=total, distinct_targets=len(targets), broken=broken,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/link-integrity-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
