"""Validate the S159 handoff/register/pilot cross-links."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
handoff = (V / '11_管理/实现交接总表.md').read_text(encoding='utf-8')
register = (V / '11_管理/待办与已知缺口登记.md').read_text(encoding='utf-8')
index = (V / '11_管理/试点批次总表.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
check('[[试点批次总表]]' in handoff, 'handoff-to-index')
check('P1 主链' in handoff and 'P3 野外层' in handoff, 'handoff-order-note')
check('[[实现交接总表]]' in index, 'index-to-handoff')
oi = json.loads((R / 'open-items.json').read_text(encoding='utf-8'))
oi01 = next((x for x in oi['items'] if x['id'] == 'OI-01'), None)
check(oi01 is not None, 'oi01-present')
check(oi01 and '[[试点批次总表]]' in oi01['what'], 'oi01-points-at-index')
check('[[试点批次总表]]' in register, 'register-to-index')
for doc, name in ((handoff, 'handoff'), (register, 'register'), (index, 'index')):
    for lm in re.finditer(r'\[\[([^\]]+)\]\]', doc):
        check(lm.group(1) in stems, name + '-link-' + lm.group(1))
report = dict(date='2026-10-13', scope='S159 cross-links: handoff -> pilot index, register OI-01 -> pilot index, index -> handoff, link resolution; documentation only',
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'handoff-links-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
