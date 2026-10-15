"""Validate the S141 R/X header backfill: presence, derivation and registry match."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
METHOD = re.compile(r'^###\s+([^\s：:]{1,24})[：:]\s*(.+?)\s*$', re.M)
KEY = re.compile(r'\b((?:resolve|paid)_[A-Za-z0-9_]+)')
LINK = re.compile(r'\[\[([^\]|#]+)')
MARK_B = '<!-- RX-HEADER-S141:BEGIN -->'; MARK_E = '<!-- RX-HEADER-S141:END -->'
reg = read('research/rx-headers.json')
by_id = {r['id']: r for r in reg['scripts']}
native = derived = 0
for p in sorted(list(V.rglob('台本_CS-*.md')) + list(V.rglob('台本_CM-*.md'))):
    text = p.read_text(encoding='utf-8')
    sid = p.stem.split('_')[1]
    has_native = bool(re.search(r'当前R/X|R：方法与提交', text))
    has_block = MARK_B in text and MARK_E in text
    check(has_native or has_block, 'header-' + sid)
    native += 1 if has_native else 0
    derived += 1 if has_block else 0
    r = by_id.get(sid)
    check(r is not None, 'registry-' + sid)
    if r:
        check(r['native'] == has_native, 'registry-native-' + sid)
        check(r['derived'] == has_block, 'registry-derived-' + sid)
    if has_block:
        block = text[text.index(MARK_B):text.index(MARK_E)]
        sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', text, re.S)
        body = sec.group(1) if sec else ''
        live_methods = [f'{m.group(1)}：{m.group(2)}' for m in METHOD.finditer(body)]
        listed = re.findall(r'`([^`]+)`\s+([^·`]+?)(?=\s·|$)', block.split('R（方法）：')[1].split('\n')[0]) if 'R（方法）：' in block else []
        listed_methods = [f'{a}：{b.strip()}' for a, b in listed]
        check(listed_methods == live_methods, 'methods-match-' + sid)
        live_keys = set(KEY.findall(text))
        block_keys = set(KEY.findall(block))
        check(block_keys <= live_keys, 'keys-derived-' + sid)
        live_names = set()
        for line in body.splitlines():
            if '：「' in line or '：“' in line:
                for lm in LINK.finditer(line):
                    live_names.add(lm.group(1).split('_')[-1])
        m = re.search(r'回访：(.+)$', block, re.M)
        if m:
            for nm in m.group(1).split('、'):
                check(nm.strip() in live_names, 'callback-derived-' + sid + '-' + nm.strip())
        for tok in re.findall(r'[A-Za-z_]{6,}', block):
            if tok.startswith(('resolve_', 'paid_')):
                check(tok in text, 'token-in-body-' + sid)
for p in V.rglob('台本_N*.md'):
    check(MARK_B not in p.read_text(encoding='utf-8'), 'no-block-in-N-' + p.stem)
check(reg['native'] == native, 'native-count-live')
check(reg['derived'] == derived, 'derived-count-live')
check(native + derived == len(reg['scripts']) == 79, 'partition-79')
card = (V / '11_管理/R-X头部补齐记录.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 派生规则', '## 逐篇登记', '## 边界'):
    check(sec in card, 'section-' + sec)
check(f"**{len(reg['scripts'])} 篇**中 {native} 篇原有 R/X 头" in card, 'card-native')
check(f"**{derived} 篇**带派生块" in card, 'card-derived')
for r in reg['scripts']:
    check(f"| {r['id']} | " in card, 'card-row-' + r['id'])
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('RX-HEADER-S141:BLOCK:BEGIN' in plan and '[[R-X头部补齐记录]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('RX-HEADERS-S141:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/rx-headers-note-hashes.json')
check(len(h) >= 65, 'own-manifest-65plus')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S141 R/X headers: presence in every city script, derived-block content matches live methods/keys/callbacks, registry and page match, links and chain; derivation-only, not runtime',
              scripts=len(reg['scripts']), native=native, derived=derived,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/rx-headers-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
