"""Validate the README's live status claims against live registries."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
readme = (ROOT / 'README.md').read_text(encoding='utf-8') + (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')  # 迭代块已移至 CHANGELOG.md
cov = read('research/dialogue-coverage.json')
scripts = len(list(V.rglob('台本_*.md')))
city = len(list(V.rglob('台本_CS-*.md'))) + len(list(V.rglob('台本_CM-*.md')))
guards = len(re.findall(r'^\| (?:结构覆盖|说话人闭合|对白去重|链接完整|占位扫描|方法数|X边闭合) ', (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8'), re.M))
pending = sum(1 for r in cov['rows'] if not r['tree'] and r['family'] != 'FX')
status = f'**设计库现状（2026-10-13）：台本 {scripts} 篇、城市任务 {city} 篇、逐角色稿待深化 {pending} 篇、质量守卫 {guards} 项。**'
check(status in readme, 'status-line-matches-live')
check(scripts == len(cov['rows']), 'script-count-consistent')
check(city == 79, 'city-79')
check(pending == 0, 'pending-zero')
check(guards == 7, 'guards-seven')
for stale in ('S86作者工具尚未执行', '71篇有逐角色初稿', '八篇待完成。'):
    check(stale not in readme, 'no-stale-' + stale[:8])
for ptr in ('[[逐角色稿完成度核对]]', '[[实现侧现状核对]]', '[[待办与已知缺口登记]]'):
    check(ptr in readme, 'pointer-' + ptr)
check('第一版' in readme and '131 篇台本' in readme, 'history-reframed')
report = dict(date='2026-10-13', scope='S147 README live claims: recompute script/city/pending/guard counts and check the status line; stale-claim removal and pointers; documentation only',
              scripts=scripts, city=city, pending=pending, guards=guards,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/readme-claims-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
