"""Validate the S160 design-phase closure page against live evidence."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest().upper()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
facts = json.loads((R / 'phase-close.json').read_text(encoding='utf-8'))
notes = len(list(V.rglob('*.md')))
validators = len(list((R / 'tools').glob('Validate-*.py')))
checksum = 0
for p in R.glob('*-validation.json'):
    d = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(d, dict) and 'checks_passed' in d:
        checksum += d['checks_passed']
gml = len(list((ROOT / 'src').rglob('Codes/*.gml')))
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8'))
dep['version'] = re.search(r'<Version>([^<]+)</Version>', (ROOT / 'src/EmbersAndOaths/EmbersAndOaths.csproj').read_text(encoding='utf-8')).group(1)
pilots = json.loads((R / 'pilot-batches.json').read_text(encoding='utf-8'))
oi = json.loads((R / 'open-items.json').read_text(encoding='utf-8'))
check(facts['notes'] == notes, 'notes-live')
check(facts['validators'] == validators, 'validators-live')
check(facts['checks'] == checksum, 'checks-live')
check(facts['gml_codes'] == gml, 'gml-live')
check(facts['sml_sha256'] == sha(ROOT / 'artifacts/EmbersAndOaths.sml'), 'sml-hash-live')
check(facts['deployed_version'] == dep['version'] and facts['deployed_runtime_verified'] is False, 'deploy-record-live')
check(facts['pilots']['batches'] == len(pilots['batches']), 'pilots-live')
check(facts['open_items'] == len(oi['items']), 'open-items-live')
check(facts['vault_passed'] is True, 'vault-passed')
card = (V / '11_管理/设计阶段收束核对.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 设计阶段交付物（现场证据）', '## 后续范围（登记在案）', '## 结论与边界'):
    check(sec in card, 'section-' + sec)
check(f"**{notes}** 篇笔记" in card, 'card-notes')
check(f"**{validators}** 个校验器" in card and f"**{checksum:,}** 项检查" in card, 'card-checks')
check(f"**{gml}** 个 GML" in card, 'card-gml')
check(facts['sml_sha256'][:16] in card, 'card-sml')
check('runtimeVerified=false' in card, 'card-runtime-flag')
check('完整扩展事件、全部场景美术' in card and '仍待实现或验收' in card, 'card-limits')
check('完整扩张事件、全部美术和剧情回归仍待实现或验收' in card, 'card-remaining-scope')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('PHASE-CLOSE-S160:BEGIN' in plan and '[[设计阶段收束核对]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('PHASE-CLOSE-S160:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'phase-close-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S160 closure audit: every design-phase figure recomputed live, deploy record and limits stated, chain; does not claim implementation or runtime',
              notes=notes, validators=validators, checks=checksum, checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'phase-close-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
