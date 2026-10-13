"""Validate the S151 verification-record continuity (no gaps in S-number blocks)."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
t = (V / '11_管理/逻辑验收记录.md').read_text(encoding='utf-8')
nums = sorted({int(m) for m in re.findall(r'S(\d+)-VERIFICATION:BEGIN', t)})
ends = sorted({int(m) for m in re.findall(r'S(\d+)-VERIFICATION:END', t)})
check(len(nums) == len(ends), 'begin-end-balanced')
check(nums == ends, 'begin-end-same-set')
missing = [n for n in range(min(nums), max(nums) + 1) if n not in nums]
check(not missing, 'no-gaps')
check(min(nums) <= 100 and max(nums) >= 150, 'range-covered')
for n in (101, 120):
    check(n in nums, f'block-S{n}')
    body = t.split(f'<!-- S{n}-VERIFICATION:BEGIN -->', 1)[1].split(f'<!-- S{n}-VERIFICATION:END -->', 1)[0]
    check('补记' in body, f'S{n}-marked-supplement')
    check('[[野外迹象与观察]]' in body or '[[中英对照覆盖报告]]' in body, f'S{n}-entry-link')
    check('未改游戏包' in body or '不代表译文质量' in body, f'S{n}-scope-limit')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
for marker in ('FIELD-SIGNS-S101:BEGIN', 'BILINGUAL-COVERAGE-S120:BEGIN'):
    check(marker in plan, 'plan-block-' + marker)
report = dict(date='2026-10-13', scope='S151 verification-record continuity: S-number blocks balanced and gap-free, supplemented blocks marked with entry links and scope limits',
              blocks=len(nums), first=min(nums), last=max(nums),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/verification-record-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
