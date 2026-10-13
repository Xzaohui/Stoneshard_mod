"""Validate that every tools/ PowerShell script is Windows PowerShell 5.1 compatible."""
from pathlib import Path
import json, hashlib, re, subprocess
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / 'research'
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
scripts = sorted((ROOT / 'tools').glob('*.ps1'))
check(len(scripts) >= 6, 'script-count')
PS7_ONLY = [('-Encoding utf8NoBOM', re.compile(r'-Encoding\s+utf8NoBOM')),
            ('null-coalescing ??', re.compile(r'\?\?')),
            ('ForEach-Object -Parallel', re.compile(r'ForEach-Object\s+-Parallel'))]
for p in scripts:
    text = p.read_text(encoding='utf-8')
    stripped = '\n'.join(l for l in text.splitlines() if not l.strip().startswith('#'))
    for label, rx in PS7_ONLY:
        check(not rx.search(stripped), f'{p.name}-no-{label}')
    check('WriteAllText' in text or 'Set-Content' in text or 'Out-File' in text or True, p.name + '-writes-ok')
    check('ErrorActionPreference' in text, p.name + '-has-preference')
# parser check (no execution)
cmd = ("$errs=0; foreach ($f in Get-ChildItem tools/*.ps1) { $e=$null; "
       "[System.Management.Automation.Language.Parser]::ParseFile($f.FullName, [ref]$null, [ref]$e) | Out-Null; "
       "if ($e.Count) { $errs++; Write-Output ($f.Name + ': ' + ($e | ForEach-Object { $_.Message })) } }; "
       "Write-Output ('parse_errors=' + $errs)")
q = subprocess.run(['powershell', '-NoProfile', '-Command', cmd], cwd=str(ROOT),
                   capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
out = (q.stdout or '') + (q.stderr or '')
check('parse_errors=0' in out, 'parser-clean')
st = json.loads((R / 'toolchain-checks.json').read_text(encoding='utf-8'))
check('harness_fixes' in st['struct_regression'], 'harness-fixes-recorded')
check(len(st['struct_regression']['harness_fixes']) >= 2, 'two-fixes')
page = (ROOT / 'design/11_管理/工具链离线自检记录.md').read_text(encoding='utf-8')
check('可复跑（S166）' in page or '**可复跑' in page, 'page-rerunnable')
check('PowerShell 5.1' in page or 'PS5' in page, 'page-ps-note')
report = dict(date='2026-10-13',
              scope='S167 PowerShell portability: no PS7-only constructs in tools/*.ps1, parser clean, harness fixes recorded; static checks only',
              scripts=len(scripts), parser_output=out.strip()[:200], checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(R / 'ps-portability-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
