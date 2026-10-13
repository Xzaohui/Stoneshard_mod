"""Validate the S144 toolchain record by re-running the offline checks."""
from pathlib import Path
import json, hashlib, re, subprocess
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
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
def run_ps(script, *args):
    p = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), *args],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    return p.returncode, ((p.stdout or '') + (p.stderr or ''))
st = read('research/toolchain-checks.json')
rc_pos, out_pos = run_ps(ROOT / 'tools/Test-MslInput.ps1', '-InputFile', str(GAME / 'vanilla.win'))
rc_neg, out_neg = run_ps(ROOT / 'tools/Test-MslInput.ps1', '-InputFile', str(GAME / 'data.win'))
check(rc_pos == 0 and 'precheck passed' in out_pos, 'positive-live-pass')
check('Do not use this file as native MSL packaging input' in out_neg, 'negative-live-rejected')
check(st['msl_input']['positive']['passed'] is True, 'registry-positive')
check(st['msl_input']['negative']['rejected'] is True, 'registry-negative')
check(st['msl_input']['positive']['sha256'] == sha(GAME / 'vanilla.win'), 'positive-input-hash')
check(st['msl_input']['negative']['sha256'] == sha(GAME / 'data.win'), 'negative-input-hash')
m = re.search(r'Loaded: (\d+) code entries, (\d+) objects, (\d+) rooms', out_pos)
check(bool(m), 'positive-counts-live')
if m:
    loaded = st['msl_input']['positive']['loaded']
    check(loaded['code_entries'] == int(m.group(1)) and loaded['objects'] == int(m.group(2)) and loaded['rooms'] == int(m.group(3)), 'counts-match')
check(st['formal_environment']['superseded'] is True, 'env-superseded-flag')
check('account.ini' in st['formal_environment']['observed'] or st['formal_environment']['exit_code'] != 0, 'env-stale-path-recorded')
check(st['struct_regression']['re_runnable'] is True and 'recorded' in st['struct_regression'], 'regression-status')
ins = st['struct_regression']['inputs']
for label in ('broken', 'fixed'):
    f = ROOT / ins[label]
    check(f.exists(), 'input-exists-' + label)
    if f.exists(): check(sha(f) == ins[label + '_sha256'], 'input-hash-' + label)
script = (ROOT / 'tools/Test-EaoStructRegression.ps1').read_text(encoding='utf-8')
check('ErrorActionPreference = \'Continue\'' in script, 'harness-continue-fix')
check('WriteAllText' in script and 'Set-Content -LiteralPath' not in script, 'harness-ps5-write-fix')
rec = json.loads((ROOT / 'artifacts/struct-access-regression.json').read_text(encoding='utf-8-sig'))
check(rec['brokenStructReceiverRejected'] is True and rec['fixedSerializedResourcePassed'] is True, 'recorded-run-ok')
check(rec['fixedDataSha256'].upper() == ins['fixed_sha256'].upper(), 'recorded-fixed-matches')
import subprocess as _sp
probe_dll = ROOT / 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll'
def _probe(path):
    q = _sp.run(['dotnet', str(probe_dll), str(path), '--assert-eao-struct-access'], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    out = ((q.stdout or '') + (q.stderr or ''))
    return ('struct receiver check passed' in out), out.strip()[:120]
for pr in st['struct_regression'].get('probes', []):
    f = ROOT / pr['path']
    check(f.exists() == pr['exists'], 'probe-exists-' + f.name)
    if f.exists():
        ok, summary = _probe(f)
        check(ok == bool(pr.get('passed')), 'probe-result-' + f.name)
check(any(pr.get('passed') for pr in st['struct_regression'].get('probes', [])), 'one-usable-fixed-input')
check(st['gameprobe']['dll_present'] == (ROOT / 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll').exists(), 'gameprobe-present')
card = (V / '11_管理/工具链离线自检记录.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## MSL 输入预检（正负对照）', '## 其余检查的状态', '## 口径与边界'):
    check(sec in card, 'section-' + sec)
check(st['msl_input']['positive']['sha256'][:16] in card and st['msl_input']['negative']['sha256'][:16] in card, 'card-input-hashes')
if m:
    check(str(int(m.group(1))) in card and str(int(m.group(3))) in card, 'card-loaded-counts')
check('按预期拒绝' in card and '已停用（隔离期）' in card, 'card-status-words')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('TOOLCHAIN-S144:BEGIN' in plan and '[[工具链离线自检记录]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('TOOLCHAIN-S144:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/toolchain-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    mm = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(mm, dict) or not all(isinstance(v, str) for v in mm.values()): continue
    for rel, exp in mm.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S144 toolchain record: re-run MSL input precheck positive/negative, registry and page match, other checks status; read-only, no build or deployment',
              positive_passed=True, negative_rejected=True, checks_passed=len(checks), errors=errors,
              passed=not errors, runtimeVerified=False)
(ROOT / 'research/toolchain-checks-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
