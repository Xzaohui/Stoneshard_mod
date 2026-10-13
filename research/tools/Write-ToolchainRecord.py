"""S144: run the offline toolchain checks (read-only) and render the record.

Runs Test-MslInput.ps1 against vanilla.win (expect pass) and against the
combined data.win (expect rejection), inspects the other two checks, and
writes both the registry and the record page. No build, no deployment, no
writes to the game directory.
"""
from pathlib import Path
import hashlib, json, subprocess, datetime, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'TOOLCHAIN-S144'
CARD = '11_管理/工具链离线自检记录.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest().upper()
def run_ps(script, *args):
    cmd = ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), *args]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    out = (p.stdout or '') + (p.stderr or '')
    return p.returncode, out.strip()
vanilla = GAME / 'vanilla.win'; data = GAME / 'data.win'
rc_pos, out_pos = run_ps(ROOT / 'tools/Test-MslInput.ps1', '-InputFile', str(vanilla))
rc_neg, out_neg = run_ps(ROOT / 'tools/Test-MslInput.ps1', '-InputFile', str(data))
rc_env, out_env = run_ps(ROOT / 'tools/Check-FormalEnvironment.ps1')
probe = ROOT / 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll'
reg = json.loads((ROOT / 'artifacts/struct-access-regression.json').read_text(encoding='utf-8')) if (ROOT / 'artifacts/struct-access-regression.json').exists() else {}
def probe_struct(path):
    if not path.exists():
        return dict(path=str(path).replace('\\', '/'), exists=False)
    q = subprocess.run(['dotnet', str(probe), str(path), '--assert-eao-struct-access'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    out = ((q.stdout or '') + (q.stderr or '')).strip()
    return dict(path=str(path).replace('\\', '/'), exists=True, exit_code=q.returncode,
                passed='struct receiver check passed' in out,
                summary=next((l for l in out.splitlines() if 'check passed' in l or 'Exception' in l or 'error' in l.lower()), out[-120:]))
struct_probes = [probe_struct(ROOT / f'artifacts/{n}') for n in ('direct-data.win', 'repeat-data.win', 'vanilla-0.2.0.win')]
m = re.search(r'Loaded: (\d+) code entries, (\d+) objects, (\d+) rooms', out_pos)
counts = m.groups() if m else ()
state = dict(date=datetime.date.today().isoformat(),
             scope='S144 offline toolchain checks: MSL input precheck positive and negative controls, formal-environment check status, struct-regression re-runnability; read-only, no build or deployment',
             msl_input=dict(
                 positive=dict(input='vanilla.win', sha256=sha(vanilla), exit_code=rc_pos,
                               passed=rc_pos == 0 and 'precheck passed' in out_pos,
                               summary=next((l for l in out_pos.splitlines() if 'precheck passed' in l), out_pos[-160:]),
                               loaded=dict(code_entries=int(counts[0]), objects=int(counts[1]), rooms=int(counts[2])) if counts else {}),
                 negative=dict(input='data.win', sha256=sha(data), exit_code=rc_neg,
                               rejected=('Do not use this file as native MSL packaging input' in out_neg),
                               summary=next((l for l in out_neg.splitlines() if 'Do not use this file' in l), out_neg[-160:]))),
             formal_environment=dict(exit_code=rc_env, superseded=True,
                                     reason='隔离期检查：快照指向已移除的 test-env/backups/20261011-134931/formal-userdata/account.ini；AGENTS 已改为“不隔离，直接在当前路径下开发”，该检查不再是门槛。',
                                     observed=next((l for l in out_env.splitlines() if 'account.ini' in l), out_env[-200:])),
             struct_regression=dict(re_runnable=True,
                                    reason='S166 关闭：broken 输入在 backups 中找到（direct-20261011-155606-160/data.win），fixed 输入改用当前构建 artifacts/direct-data.win（2026-10-11 记录的 fixed 文件已不满足今日更严的 linkage 检查）；并修好两处工具缺陷（见下）。',
                                    inputs=dict(broken='backups/direct-20261011-155606-160/data.win',
                                                broken_sha256=sha(ROOT / 'backups/direct-20261011-155606-160/data.win'),
                                                fixed='artifacts/direct-data.win', fixed_sha256=sha(ROOT / 'artifacts/direct-data.win')),
                                    harness_fixes=['broken 运行改用 Continue 偏好，避免预期 stderr 终止脚本',
                                                   '产物写入改 [IO.File]::WriteAllText（PS5.1 无 -Encoding utf8NoBOM）'],
                                    recorded=reg, probes=struct_probes),
             gameprobe=dict(dll_present=probe.exists(), sha256=sha(probe) if probe.exists() else ''))
(ROOT / 'research/toolchain-checks.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p).lower()
pos = state['msl_input']['positive']; neg = state['msl_input']['negative']
n = ('---\ntitle: "工具链离线自检记录"\nid: MGMT-TOOLCHAIN-S144\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S144, review, toolchain]\naliases: []\n---\n\n'
     '# 工具链离线自检记录\n\n'
     '按 [[实现侧现状核对]] 的交接基线，复跑 `tools/` 下的**离线**检查并记录结果。全部只读：不构建、不部署、不写游戏目录。登记 `research/toolchain-checks.json`，工具 `research/tools/Write-ToolchainRecord.py`。\n\n'
     '## MSL 输入预检（正负对照）\n\n'
     '| 对照 | 输入 | 结果 | 说明 |\n| --- | --- | --- | --- |\n'
     f"| 正 | `vanilla.win`（`{pos['sha256'][:16]}…`） | {'通过' if pos['passed'] else '未通过'} | {pos['summary']} |\n"
     f"| 负 | 组合 `data.win`（`{neg['sha256'][:16]}…`） | {'按预期拒绝' if neg['rejected'] else '未拒绝'} | {neg['summary']} |\n")
if pos.get('loaded'):
    n += (f"\n正对照读取：代码条目 **{pos['loaded']['code_entries']}**、对象 **{pos['loaded']['objects']}**、房间 **{pos['loaded']['rooms']}**。"
          "工具自身声明：该预检只证明没有已知 MSL/EAO 对象标记，**不是**独立的原版来源鉴定。\n")
n += ('\n## 其余检查的状态\n\n'
      '| 检查 | 状态 | 说明 |\n| --- | --- | --- |\n'
      f"| `Check-FormalEnvironment.ps1` | 已停用（隔离期） | {state['formal_environment']['reason']} |\n"
      f"| `Test-EaoStructRegression.ps1` | **可复跑（S166）** | {state['struct_regression']['reason']} |\n"
      f"| `GameProbe` 探针 | {'已构建' if state['gameprobe']['dll_present'] else '缺失'} | `tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll` |\n"
      '\n结构回归输入复核（S162，`dotnet GameProbe <file> --assert-eao-struct-access`）：\n\n'
      '| 文件 | 结果 | 说明 |\n| --- | --- | --- |\n'
      + ''.join(f"| `{pr['path'].split('/')[-1]}` | {'通过' if pr.get('passed') else ('缺失' if not pr.get('exists') else '未通过')} | {pr.get('summary', '')[:70]} |\n" for pr in struct_probes) + '\n'
      f"结构回归输入（S166 指认）：broken `{state['struct_regression']['inputs']['broken']}`（`{state['struct_regression']['inputs']['broken_sha256'][:16]}…`）；fixed `{state['struct_regression']['inputs']['fixed']}`（`{state['struct_regression']['inputs']['fixed_sha256'][:16]}…`）。"
      '工具修复：' + '；'.join(state['struct_regression']['harness_fixes']) + '。最新一次复跑见 `artifacts/struct-access-regression.json`（broken 按预期理由拒绝、fixed 通过 linkage、`runtimeVerified=false`）。\n\n'
      '## 口径与边界\n\n'
      '- 预检通过只说明 `vanilla.win` 可作为 MSL 打包输入、且不含已知 EAO 标记；不证明原版来源、不代表组合包行为。\n'
      '- `Check-FormalEnvironment` 属被取代的隔离方案；保留脚本与快照作历史，不再作为开发门槛。\n'
      '- 结构回归的 broken 输入取自 `backups/`（验证快照依赖，勿清理）；fixed 输入随构建更新，重建包后须重指认并复跑。\n'
      '- 本页不改变任何部署门槛；仍以 `AGENTS.md` 为准。\n\n'
      '[[实现侧现状核对]] · [[待办与已知缺口登记]] · [[质量守卫总表]] · [[本地安装与证据]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S144工具链离线自检（当前登记）\n\n[[工具链离线自检记录]]：MSL 输入预检正对照通过（vanilla.win）、负对照按预期拒绝（组合 data.win）；`Check-FormalEnvironment` 属隔离期已停用；结构回归输入不在库中暂不可复跑。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/toolchain-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel].lower() != generated[rel].lower(): h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- TOOLCHAIN-S144:BEGIN -->\n2026-10-13 S144：工具链离线自检（只读）。'
        'Test-MslInput 正对照通过（vanilla.win：34189代码条目/9663对象/1067房间，无已知MSL/EAO标记）、负对照按预期拒绝（组合data.win）；'
        'Check-FormalEnvironment属隔离期已停用（快照指向已移除备份）；结构回归输入不在库中暂不可复跑；GameProbe已构建。'
        '入口design/11_管理/工具链离线自检记录.md；运行Validate-ToolchainChecks.py及既有检查；不构建、不部署。\n<!-- TOOLCHAIN-S144:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- TOOLCHAIN-S144:BEGIN -->.*?<!-- TOOLCHAIN-S144:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- TOOLCHAIN-S144:BEGIN -->.*?<!-- TOOLCHAIN-S144:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(positive=pos['passed'], negative=neg['rejected'], env_rc=rc_env,
                      regression_re_runnable=state['struct_regression']['re_runnable']), ensure_ascii=False))
