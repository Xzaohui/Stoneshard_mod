"""Validate the S136 reputation base-link integration."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
sysdoc = (V / '09_系统逻辑/城镇声望与信任系统.md').read_text(encoding='utf-8')
bil = (V / '09_系统逻辑/城镇声望系统中英对照.md').read_text(encoding='utf-8')
contract = (V / '01_原作基线/原作契据任务与声誉结构参照.md').read_text(encoding='utf-8')
rep = (V / '01_原作基线/原作声誉档位与地方状态参照.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for name, doc in (('system', sysdoc), ('bilingual', bil)):
    check('REP-BASE-LINK-S136:BEGIN' in doc, name + '-block')
    for term in ('原作对照（S134/S135）', '[[原作契据任务与声誉结构参照]]', '[[原作声誉档位与地方状态参照]]',
                 '不写原版档位消息', '不作结局资格', '不重复计同一行为', '不引入', '≤15%', '不改原版通缉'):
        check(term in doc, name + '-term-' + term)
check('Base-game cross-reference (S134/S135)' in bil and 'never double-counts one deed' in bil, 'bilingual-en-block')
for doc, name in ((contract, 'contract-card'), (rep, 'rep-card')):
    check('[[城镇声望与信任系统]]' in doc and '[[城镇声望系统中英对照]]' in doc, name + '-backlinks')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', sysdoc):
    check(lm.group(1) in stems, 'sysdoc-link-' + lm.group(1))
h = read('research/rep-base-link-note-hashes.json')
check(set(h) == {'design/09_系统逻辑/城镇声望与信任系统.md', 'design/09_系统逻辑/城镇声望系统中英对照.md'}, 'own-manifest-two-docs')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
check('REP-BASE-LINK-S136:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S136 reputation base-link: cross-reference blocks in both design notes, EN block in the bilingual note, backlinks from both reference cards, links and chain; documentation only, not runtime',
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/rep-base-link-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
