"""Validate the S145 replay-drill record against the live tool inventory."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
drill = read('research/replay-drill-s145.json')
tools = {p.name for p in (ROOT / 'research/tools').glob('*.py')}
writers = {p.name for p in (ROOT / 'research/tools').glob('Write-*.py')}
validators = {p.name for p in (ROOT / 'research/tools').glob('Validate-*.py')}
probes = {p.name for p in (ROOT / 'research/tools').glob('Probe-*.py')}
check(drill['inventory']['writers'] == len(writers), 'writer-count-live')
check(drill['inventory']['validators'] == len(validators), 'validator-count-live')
check(drill['inventory']['probes'] == len(probes), 'probe-count-live')
for lst in ('env_skipped_list', 'aborted_list', 'failed_validators'):
    for name in drill['copy_run'][lst] if lst != 'env_skipped_list' else drill['main_run'][lst]:
        check(name in tools, lst + '-' + name)
check(len(drill['main_run']['env_skipped_list']) == drill['main_run']['env_skipped'], 'env-skip-count')
check(len(drill['copy_run']['aborted_list']) == drill['copy_run']['aborted'], 'abort-count')
check(len(drill['copy_run']['failed_validators']) == drill['copy_run']['validators_failed'], 'failed-count')
check(drill['main_run']['failures'] == 0, 'main-zero-failures')
check(drill['main_run']['writers_ok'] + drill['main_run']['env_skipped'] <= len(writers) + len(probes), 'main-run-sane')
check('Write-ImplState.py' in drill['copy_run']['aborted_list'], 'impl-state-listed')
card = (V / '11_管理/全链复跑演练S145.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 主库按序重跑', '## 最小副本', '## 结论与后续动作', '## 边界'):
    check(sec in card, 'section-' + sec)
check(f"通过 **{drill['main_run']['writers_ok']}**、需外部素材跳过 **{drill['main_run']['env_skipped']}**、失败 **0**" in card, 'card-main-numbers')
check(f"通过 **{drill['copy_run']['writers_ok']}**、跳过 **{drill['copy_run']['env_skipped']}**、中止 **{drill['copy_run']['aborted']}**" in card, 'card-copy-numbers')
check(f"通过 **{drill['copy_run']['validators_ok']}**、失败 **{drill['copy_run']['validators_failed']}**" in card, 'card-validator-numbers')
check('不声明整树字节一致' in card, 'card-scope-limit')
flow = (V / '11_管理/设计库生成与校验流程.md').read_text(encoding='utf-8')
check('REPLAY-S145:BEGIN' in flow and '[[全链复跑演练S145]]' in flow and '第五轮' in flow, 'flow-entry')
check('## S165 复跑（第六轮，2026-10-13）' in card, 's165-section')
s165 = drill['s165']
check(s165['writers_ok'] == 54 and s165['aborted'] == 0, 's165-writers')
check(s165['validators_ok'] == 66 and s165['validators_failed'] == 16, 's165-validators')
check(len(s165['failed_validators']) == s165['validators_failed'], 's165-list-size')
for name in s165['failed_validators']:
    check(name in tools, 's165-tool-' + name)
check('REPLAY-S165:BEGIN' in flow and '第六轮' in flow and 'S165' in flow, 'flow-s165')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('REPLAY-S145:BEGIN' in plan and '[[全链复跑演练S145]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('REPLAY-S145:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/replay-drill-note-hashes.json')
check(len(h) == 3, 'own-manifest-3')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S145 replay drill record: tool inventory match, run numbers, environment lists, flow entry and chain; record of an executed drill, not runtime',
              writers=len(writers), validators=len(validators), probes=len(probes),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/replay-drill-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
