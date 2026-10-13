"""Validate the S135 vanilla reputation reference card."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
probe = read('research/reputation-structure-probe.json'); base = read('research/local-baseline.json')
check(probe['sha256'] == base['candidate_baseline']['sha256'], 'fingerprint')
check(probe['strg_count'] == base['candidate_baseline']['strg_count'], 'strg-count')
check(len(probe['feeds']) == 10, 'feeds-10')
check(len(probe['sources']) == 20, 'sources-20')
check(len(probe['ui']) == 4, 'ui-4')
check(sum(1 for p in probe['perks'] if p['row'] == 'name') == 20, 'perk-names-20')
check(sum(1 for p in probe['states'] if p['row'] == 'name') == 15, 'state-names-15')
check(all('[声誉' in s['zh'] for s in probe['sources']), 'sources-bracket')
check(sum(1 for s in probe['sources'] if 'rep_amount' in s['zh']) >= 18, 'sources-placeholder')
for row in probe['feeds'] + probe['sources'] + probe['perks'] + probe['states'] + probe['crime']:
    check(len(row['zh']) <= 47, 'clip-' + str(row['locator']))
card = (V / '01_原作基线/原作声誉档位与地方状态参照.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 读取指纹', '## 声誉信息流与界面', '## 声誉来源清单（均带 `[声誉%rep_amount%]`）', '## 档位加成（正负两向）', '## 犯罪与通缉', '## 地方状态（15 项）', '## 对照与本Mod口径', '## 边界'):
    check(sec in card, 'section-' + sec)
check(probe['sha256'] in card and str(probe['strg_count']) in card, 'card-fingerprint')
for f in probe['feeds']:
    check(f['key'] in card and f['zh'] in card, 'card-feed-' + f['key'])
for s in probe['sources']:
    check(s['key'] in card and s['zh'] in card, 'card-source-' + s['key'])
for name in ('特殊任务', '特色商品', '赏金预付', '同心同德', '应有尽有·一', '价格公道·一', '宰你没商量·一', '粗布烂铁·一', '本地公敌'):
    check(name in card, 'card-perk-' + name)
for name in ('物资短缺', '竞争', '集会', '梦魇', '瘟病'):
    check(name in card, 'card-state-' + name)
for term in ('格杀勿论', '罚金或拘役', '犯罪次数'):
    check(term in card, 'card-crime-' + term)
for term in ('地方信任', '原版声望', '城市服务班与有限库存', '不超过 15%', '不引入', '不改原版通缉'):
    check(term in card, 'card-comparison-' + term)
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
idx = (V / '01_原作基线/原作基线索引.md').read_text(encoding='utf-8')
check('REP-REF-S135:BEGIN' in idx and '[[原作声誉档位与地方状态参照]]' in idx, 'baseline-index-block')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('REP-REF-S135:BEGIN' in plan and '[[原作声誉档位与地方状态参照]]' in plan, 'plan-block')
check('REP-REF-S135:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/rep-ref-note-hashes.json')
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S135 reputation reference: probe fingerprint and sections, source/perk/state coverage, comparison wording, registration and chain; static table read, not runtime',
              feeds=len(probe['feeds']), sources=len(probe['sources']), perk_rows=len(probe['perks']),
              state_rows=len(probe['states']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/rep-ref-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
