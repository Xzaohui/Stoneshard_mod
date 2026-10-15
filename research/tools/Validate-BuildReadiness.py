"""Validate the S168 build-readiness page against live prerequisites."""
from pathlib import Path
import json, hashlib, pathlib, re, subprocess
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
facts = json.loads((R / 'build-readiness.json').read_text(encoding='utf-8'))
q = subprocess.run(['dotnet', '--version'], capture_output=True, text=True, timeout=300)
check(q.returncode == 0, 'dotnet-available')
check(facts['dotnet']['version'] == (q.stdout or '').strip().splitlines()[0], 'dotnet-version-live')
refs = []
for proj in ('src/EmbersAndOaths/EmbersAndOaths.csproj', 'tools/GameProbe/GameProbe.csproj'):
    text = (ROOT / proj).read_text(encoding='utf-8')
    for m in re.finditer(r'<PackageReference Include="([^"]+)" Version="([^"]+)"', text):
        refs.append((m.group(1), m.group(2)))
    for m in re.finditer(r'<Reference Include="([^"]+)"><HintPath>\$\(MslDir\)\\([^<]+)</HintPath>', text):
        refs.append((m.group(1), m.group(2)))
check(len(facts['references']) == len(refs), 'refs-count-live')
for r in facts['references']:
    if r['version']:
        live = (ROOT / 'tools/packages' / r['id'].lower() / r['version']).exists()
        check(r['offline_dir'] == live, 'pkg-live-' + r['id'])
        check(live, 'pkg-present-' + r['id'])
    else:
        live = (GAME / 'msl' / r['msl_dll']).exists()
        check(r['dll_present'] == live, 'dll-live-' + r['id'])
        check(live, 'dll-present-' + r['id'])
check(facts['build_script_parse'].strip() == 'errors=0', 'script-parses')
check(facts['probe']['present'] == (ROOT / facts['probe']['path']).exists(), 'probe-live')
check(facts['build_performed'] is False, 'no-build-this-round')
chain = facts['input_chain']
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8-sig'))
cur_sha = sha(GAME / 'data.win').upper()
check(chain['current_sha256'] == cur_sha, 'chain-current-sha-live')
check(chain['current_matches_record'] == (cur_sha == str(dep.get('deployedDataSha256')).upper()), 'chain-match-live')
check(chain['targeted_repair'] == bool(dep.get('targetedRepair')), 'chain-branch-live')
rs = pathlib.Path(chain['repair_source'])
check(chain['repair_source_exists'] == rs.exists(), 'chain-repair-live')
if rs.exists(): check(chain['repair_source_sha256'].upper() == sha(rs).upper(), 'chain-repair-sha-live')
bk = pathlib.Path(chain['backup'])
check(chain['backup_exists'] == bk.exists(), 'chain-backup-live')
if bk.exists():
    check(set(chain['backup_files']) == {x.name for x in bk.iterdir()}, 'chain-backup-files-live')
check('## 构建输入链（来自部署记录）' in (V / '11_管理/构建前置核对.md').read_text(encoding='utf-8'), 'card-chain-section')
card = (V / '11_管理/构建前置核对.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 工程引用', '## 边界'):
    check(sec in card, 'section-' + sec)
check(facts['dotnet']['version'] in card, 'card-dotnet')
check('本轮不构建' in card, 'card-no-build')
for r in facts['references']:
    check(r['id'] in card, 'card-ref-' + r['id'])
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('BUILD-READY-S168:BEGIN' in plan and '[[构建前置核对]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('BUILD-READY-S168:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'build-ready-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S168 build readiness: live dotnet, offline package versions vs csproj, MSL assemblies, probe, script parse, page and chain; no build performed',
              references=len(refs), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'build-readiness-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
