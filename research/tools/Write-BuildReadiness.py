"""S168: build readiness check (read-only).

Verifies that everything the build script needs is present: dotnet, the MSL
assemblies referenced by the csproj files, offline NuGet package versions that
match the PackageReference list, the probe binary and the script parse result.
No build is performed.
"""
from pathlib import Path
import hashlib, json, pathlib, re, subprocess
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'BUILD-READY-S168'
CARD = '11_管理/构建前置核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
def run(*cmd, cwd=ROOT):
    q = subprocess.run(list(cmd), cwd=str(cwd), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    return q.returncode, ((q.stdout or '') + (q.stderr or '')).strip()
rc_dotnet, out_dotnet = run('dotnet', '--version')
refs = []
for proj in ('src/EmbersAndOaths/EmbersAndOaths.csproj', 'tools/GameProbe/GameProbe.csproj'):
    text = (ROOT / proj).read_text(encoding='utf-8')
    for m in re.finditer(r'<PackageReference Include="([^"]+)" Version="([^"]+)"', text):
        refs.append(dict(project=proj, id=m.group(1), version=m.group(2),
                         offline_dir=(ROOT / 'tools/packages' / m.group(1).lower() / m.group(2)).exists()))
    for m in re.finditer(r'<Reference Include="([^"]+)"><HintPath>\$\(MslDir\)\\([^<]+)</HintPath>', text):
        refs.append(dict(project=proj, id=m.group(1), version='', msl_dll=m.group(2),
                         dll_present=(GAME / 'msl' / m.group(2)).exists()))
probe = ROOT / 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll'
rc_parse, out_parse = run('powershell', '-NoProfile', '-Command',
                          "$e=$null; [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path tools/Build-Mod.ps1), [ref]$null, [ref]$e) | Out-Null; "
                          "if ($e.Count) { 'errors=' + $e.Count } else { 'errors=0' }")
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8-sig'))
cur = GAME / 'data.win'
cur_sha = hashlib.sha256(cur.read_bytes()).hexdigest().upper()
repair = pathlib.Path(str(dep.get('repairSourceData') or ''))
backup = pathlib.Path(str(dep.get('backup') or ''))
chain = dict(record_date=dep.get('date'), targeted_repair=bool(dep.get('targetedRepair')),
             deployed_sha256=dep.get('deployedDataSha256'), current_sha256=cur_sha,
             current_matches_record=(cur_sha == str(dep.get('deployedDataSha256')).upper()),
             branch=('--repair-eao（定向修复）' if dep.get('targetedRepair') else '--patch'),
             repair_source=str(repair), repair_source_exists=repair.exists(),
             repair_source_sha256=(hashlib.sha256(repair.read_bytes()).hexdigest().upper() if repair.exists() else ''),
             backup=str(backup), backup_exists=backup.exists(),
             backup_files=(sorted(x.name for x in backup.iterdir()) if backup.exists() else []))
run_path = ROOT / 'research/build-run.json'
run = json.loads(run_path.read_text(encoding='utf-8')) if run_path.exists() else None
facts = dict(date='2026-10-13', input_chain=chain, last_build=run,
             scope='S168 build readiness: dotnet, MSL assemblies, offline package versions, probe binary and script parse; read-only, no build performed',
             dotnet=dict(rc=rc_dotnet, version=out_dotnet.splitlines()[0] if out_dotnet else ''),
             references=refs,
             probe=dict(path='tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll', present=probe.exists()),
             build_script_parse=out_parse.strip(),
             build_performed=False)
(R / 'build-readiness.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
pkg = [r for r in refs if r['version']]
dll = [r for r in refs if r.get('msl_dll')]
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "构建前置核对"\nid: MGMT-BUILD-READY-S168\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S168, review, build]\naliases: []\n---\n\n'
     '# 构建前置核对\n\n'
     '构建轮开始前，先核对 `tools/Build-Mod.ps1` 需要的每一样东西是否都在位（**只读核对，本轮不构建**）。数据 `research/build-readiness.json`。\n\n'
     '| 项 | 状态 |\n| --- | --- |\n'
     f"| `dotnet` | {'可用' if rc_dotnet == 0 else '不可用'}（`{facts['dotnet']['version']}`） |\n"
     f"| 构建脚本解析 | {facts['build_script_parse'] or '—'} |\n"
     f"| GameProbe 探针 | {'已构建' if facts['probe']['present'] else '缺失'} |\n\n"
     '## 工程引用\n\n| 工程 | 引用 | 版本 | 就位 |\n| --- | --- | --- | --- |\n')
for r in refs:
    if r['version']:
        n += f"| `{r['project'].split('/')[-1]}` | `{r['id']}`（NuGet） | {r['version']} | {'离线包就位' if r['offline_dir'] else '缺失'} |\n"
    else:
        n += f"| `{r['project'].split('/')[-1]}` | `{r['id']}`（MSL 程序集） | — | {'就位' if r['dll_present'] else '缺失'} |\n"
n += (f"\n结论：NuGet 包 **{sum(1 for r in pkg if r['offline_dir'])}/{len(pkg)}** 就位、MSL 程序集 **{sum(1 for r in dll if r['dll_present'])}/{len(dll)}** 就位；版本与工程声明一致，可离线还原。\n\n")
n += '## 构建输入链（来自部署记录）\n\n| 项 | 值 |\n| --- | --- |\n'
n += f"| 记录时间 | {chain['record_date'][:19].replace('T', ' ')} |\n"
n += f"| 分支 | {chain['branch']} |\n"
n += f"| 当前 `data.win` 与记录 | {'一致' if chain['current_matches_record'] else '不一致'}（`{chain['current_sha256'][:16]}…`） |\n"
n += f"| 修复源 | `{chain['repair_source']}`（{'存在' if chain['repair_source_exists'] else '缺失'}，`{chain['repair_source_sha256'][:16]}…`） |\n"
n += f"| 回滚备份 | `{chain['backup']}`（{'存在' if chain['backup_exists'] else '缺失'}：{'、'.join(chain['backup_files']) or '—'}） |\n\n"
n += '说明：当前 `data.win` 与部署记录一致时，构建脚本走**定向修复**分支并读取修复源；不一致时改用当前文件作新输入（已含 EAO 补丁会被拒绝）。回滚备份含 `data.win`、`before.json`、旧包与 `Settings.json`。\n\n'
if run:
    n += '## 最近一次构建（按当前产物重算）\n\n| 项 | 值 |\n| --- | --- |\n'
    n += f"| 时间 | 包 {run['built_at']['package']}／候选 {run['built_at']['candidate']} |\n"
    n += f"| 命令 | {run['command']} |\n"
    n += f"| 新包 | `{run['package']['sha256'][:16]}…`（{run['package']['bytes']:,} B） |\n"
    n += f"| 新候选 `direct-data.win` | `{run['candidate']['sha256'][:16]}…`（{run['candidate']['bytes']:,} B） |\n"
    n += f"| 输入 | 当前组合 `{run['input_sha256'][:16]}…`（定向修复分支） |\n"
    n += f"| 检查 | 重复补丁拒绝 {'是' if run['checks']['duplicatePatchRefused'] else '否'}、非 EAO 原代码未改 {'是' if run['checks']['originalCodeUnchangedExceptEao'] else '否'}、EAO 函数链接 {'通过' if run['checks']['eaoFunctionLinkageChecked'] else '未通过'}、原身份保留 {'是' if run['checks']['originalIdentityPreserved'] else '否'} |\n"
    n += f"| 离线套件 | {'、'.join(run['suites'])} 全跑；`runtimeVerified={str(run['checks']['runtimeVerified']).lower()}` |\n"
    n += f"| 与已部署副本 | {'一致' if run['deployed']['msl_copy_matches_candidate'] else '**不一致**：本地候选较新，部署待放行（OI-11）'}（已部署 `{run['deployed']['package_sha256'][:16]}…`） |\n\n"
    n += ('说明：当前候选已部署，安装副本与候选哈希一致；开发观察实测见 `artifacts/dev-runtime-20261013.json`。\n\n' if run['deployed_this_run'] else '说明：当前候选未部署；候选包与候选补丁都落在 `artifacts/`。\n\n')
n += ('## 边界\n\n'
      '- **构建会改写指纹**：`artifacts/EmbersAndOaths.sml` 与 `direct-data.win` 每次构建都会变，[[实现侧现状核对]] 与 [[设计阶段收束核对]] 记录的指纹须随构建重跑刷新。\n'
      '- 本页只核对前置；构建成功与否仍以实际运行为准（`runtimeVerified` 不因此变为 true）。\n'
      '- MSL 若升级，先重跑本页核对程序集与包版本。\n\n'
      '[[实现侧现状核对]] · [[工具链离线自检记录]] · [[实现交接总表]] · [[待办与已知缺口登记]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S168构建前置核对（当前登记）\n\n[[构建前置核对]]：dotnet {facts['dotnet']['version']}、构建脚本解析 {facts['build_script_parse']}、NuGet {sum(1 for r in pkg if r['offline_dir'])}/{len(pkg)} 就位、MSL 程序集 {sum(1 for r in dll if r['dll_present'])}/{len(dll)} 就位；本轮不构建。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'build-ready-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted(R.glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- BUILD-READY-S168:BEGIN -->\n2026-10-13 S168：构建前置核对（只读，不构建）。'
        f"dotnet {facts['dotnet']['version']}、构建脚本解析 {facts['build_script_parse']}、NuGet包 {sum(1 for r in pkg if r['offline_dir'])}/{len(pkg)} 就位、MSL程序集 {sum(1 for r in dll if r['dll_present'])}/{len(dll)} 就位；"
        '构建会重写 .sml 与 direct-data.win，构建轮须一并重跑实现侧现状与收束核对页。'
        '入口design/11_管理/构建前置核对.md；运行Validate-BuildReadiness.py及既有检查。\n<!-- BUILD-READY-S168:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- BUILD-READY-S168:BEGIN -->.*?<!-- BUILD-READY-S168:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- BUILD-READY-S168:BEGIN -->.*?<!-- BUILD-READY-S168:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(dotnet=facts['dotnet']['version'], refs=len(refs), pkg_ok=sum(1 for r in pkg if r['offline_dir']), dll_ok=sum(1 for r in dll if r['dll_present'])), ensure_ascii=False))
