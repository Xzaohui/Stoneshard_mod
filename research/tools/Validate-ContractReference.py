"""Validate the S134 vanilla contract/reputation reference card."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
probe = read('research/contract-structure-probe.json'); base = read('research/local-baseline.json')
check(probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint')
check(probe['strg_count'] == base['candidate_baseline']['strg_count'], 'strg-count')
check(len(probe['settings']) == 6, 'settings-6')
check(len(probe['feeds']) == 5, 'feeds-5')
check(probe['contract_key_count'] >= 100, 'contract-keys')
check(len(probe['troll_rows']) >= 20, 'troll-rows')
check(len(probe['identifier_contract_names']) >= 100, 'ident-names')
for s in probe['settings']:
    check(bool(s['zh']) and bool(s['en']), 'setting-bilingual-' + s['key'])
for f in probe['feeds']:
    check(bool(f['zh']), 'feed-zh-' + f['key'])
for row in probe['settings'] + probe['feeds'] + probe['troll_rows']:
    check(len(row['zh']) <= 47, 'clip-' + str(row['locator']))
for h in probe['zh_mentions']:
    check(len(h['zh']) <= 47, 'clip-mention-' + str(h['locator']))
card = (V / '01_原作基线/原作契据任务与声誉结构参照.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 读取指纹', '## 自定义开局设置项', '## 信息流与计数', '## 契据对话族', '## 声誉与契据的联动（原版）', '## 具名契据与条件对白', '## 对照与本Mod口径', '## 边界'):
    check(sec in card, 'section-' + sec)
check(probe['sha256'] in card and str(probe['strg_count']) in card, 'card-fingerprint')
for s in probe['settings']:
    check(s['key'] in card and s['zh'] in card and s['en'] in card, 'card-setting-' + s['key'])
for f in probe['feeds']:
    check(f['key'] in card and f['zh'] in card, 'card-feed-' + f['key'])
check('%town_name%' in card and '%contract_name%' in card and '%rep_amount%' in card, 'card-placeholders')
for term in ('advances', 'underworldConnections1', 'competition', 'trollcontract', 'Catacombs', 'Crypt', 'Bastion'):
    check(term in card, 'card-term-' + term)
for term in ('地方信任', '原版声望', '不做玩家重复任务', '不引入', '有限回执'):
    check(term in card, 'card-comparison-' + term)
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
idx = (V / '01_原作基线/原作基线索引.md').read_text(encoding='utf-8')
check('CONTRACT-REF-S134:BEGIN' in idx and '[[原作契据任务与声誉结构参照]]' in idx, 'baseline-index-block')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('CONTRACT-REF-S134:BEGIN' in plan and '[[原作契据任务与声誉结构参照]]' in plan, 'plan-block')
check('CONTRACT-REF-S134:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/contract-ref-note-hashes.json')
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S134 contract reference: probe fingerprint and sections, bilingual labels, clipped snippets, comparison wording, registration and chain; static table read, not runtime',
              settings=len(probe['settings']), feeds=len(probe['feeds']), contract_keys=probe['contract_key_count'],
              troll_rows=len(probe['troll_rows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/contract-ref-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
