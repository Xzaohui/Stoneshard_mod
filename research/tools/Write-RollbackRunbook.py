"""S174: deployment and rollback runbook (plan only, nothing executed).

Reads the deployment record and its backup set, verifies the hashes the runbook
will rely on, and renders the runbook page. Read-only: no deployment, no
rollback, no game writes.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'ROLLBACK-S174'
CARD = '11_管理/部署与回滚运行手册.md'
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
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8-sig'))
bk = Path(str(dep['backup']))
before = json.loads((bk / 'before.json').read_text(encoding='utf-8-sig')) if (bk / 'before.json').exists() else {}
bk_data = bk / 'data.win'
bk_sml = bk / 'EmbersAndOaths.sml'
game_data = GAME / 'data.win'
game_sml = GAME / 'msl/Mods/EmbersAndOaths.sml'
settings_path = GAME / 'msl/Settings.json'
user_dir = Path('C:/Users/83912/AppData/Local/StoneShard')
settings = json.loads(settings_path.read_text(encoding='utf-8-sig')) if settings_path.exists() else {}
user_files = [x for x in user_dir.rglob('*') if x.is_file()] if user_dir.exists() else []
user_side = dict(settings_path=str(settings_path).replace('\\', '/'), settings_exists=settings_path.exists(),
                 settings_sha256=sha(settings_path) if settings_path.exists() else '',
                 enable_mods=settings.get('EnableMods', []), mod_enabled=('EmbersAndOaths' in settings.get('EnableMods', [])),
                 user_dir=str(user_dir).replace('\\', '/'), user_files_now=len(user_files),
                 user_files_recorded=dep.get('userFilesChecked'))
facts = dict(
    date='2026-10-13', user_side=user_side,
    scope='S174 deployment and rollback runbook: steps derived from Build-Mod.ps1/Deploy-Mod.ps1 and the recorded backup set; nothing executed',
    record=dict(path='artifacts/direct-deployment.json', mode=dep['mode'], game=dep['game'], package=dep['package'],
                backup=str(bk), targeted_repair=bool(dep['targetedRepair']),
                deployed_data_sha256=dep['deployedDataSha256'], user_files_checked=dep.get('userFilesChecked')),
    backup=dict(dir=str(bk), exists=bk.exists(),
                files=sorted(x.name for x in bk.iterdir()) if bk.exists() else [],
                data_sha256=sha(bk_data) if bk_data.exists() else '',
                data_expected=before.get('beforeDataSha256', ''),
                sml_sha256=sha(bk_sml) if bk_sml.exists() else ''),
    live=dict(data_sha256=sha(game_data), deployed_sml_sha256=sha(game_sml) if game_sml.exists() else '',
              data_matches_record=(sha(game_data) == str(dep['deployedDataSha256']).upper())),
)
(R / 'rollback-runbook.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "部署与回滚运行手册"\nid: MGMT-ROLLBACK-S174\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S174, guide, deployment]\naliases: []\n---\n\n'
     '# 部署与回滚运行手册\n\n'
     '按 `tools/Build-Mod.ps1` 与 `tools/Deploy-Mod.ps1` 的实际行为，把**部署**与**回滚**写成可照做的步骤，并用当前部署记录与备份集核对每一步依赖的哈希。**本轮未执行任何部署或回滚**；数据 `research/rollback-runbook.json`。\n\n'
     '## 部署步骤（放行后执行）\n\n'
     '1. **退出游戏与 MSL**：脚本在文件被占用时暂停，不强制结束用户进程。\n'
     '2. **构建并离线验收**：`tools/Build-Mod.ps1 -Deploy`——构建两工程 → 打包 `.sml` → 生成候选补丁 → 跑四套离线检查（compiledCallbackScenarios／rooms／teleport／story）；任一失败即中止，不部署。\n'
     '3. **备份与部署**（`Deploy-Mod.ps1` 内部顺序）：快照用户文件（记录 `userFilesChecked`）→ 备份 `data.win`、`Settings.json`、旧 `.sml` 到 `backups/direct-<时间戳>/` → 复制新 `.sml` 到 `msl/Mods/` → 以 `data.win.eao-pending` 原子替换 `data.win` → 复核包/输出/vanilla/用户文件哈希。\n'
     '4. **记录**：写 `artifacts/direct-deployment.json`（本次部署）与 `artifacts/package-deployment.json`（包模式）；`runtimeVerified` 保持 `false`，待实机。\n'
     '5. **部署后核对**：`vanilla.win` 哈希未变、用户文件数与哈希未变、[[实现侧现状核对]] 重跑（候选与副本应变为一致）。\n\n'
     '## 回滚步骤（必要时执行）\n\n'
     f"1. **定位备份集**：读 `artifacts/direct-deployment.json` 的 `backup` 字段——本次为 `{facts['record']['backup']}`（含 {'、'.join(facts['backup']['files']) or '—'}）。\n"
     f"2. **校验备份完整**：备份 `data.win` 的 SHA256 应等于 `before.json` 的 `beforeDataSha256`（记录值 `{facts['backup']['data_expected'][:16]}…`）。\n"
     '3. **退出游戏与 MSL**，然后把备份 `data.win` 复制回游戏目录（覆盖当前文件）。\n'
     '4. **还原 MSL 设置与旧包**：把备份 `Settings.json` 复制回 MSL 设置路径；把备份的旧 `EmbersAndOaths.sml` 复制回 `msl/Mods/`（或按用户意愿移除本 Mod 条目）。\n'
     '5. **复核**：游戏 `data.win` 哈希应回到 `beforeDataSha256`；`vanilla.win` 应等于 `before.json` 的 `vanillaSha256`；**用户数据一律不动**（不删除角色、不覆盖存档）。\n'
     '6. **留痕**：按部署记录同格式写一份回滚记录到 `artifacts/`（时间、还原来源、还原后哈希、结果），并把 [[实现侧现状核对]] 重跑为回滚后的状态。\n\n'
     '## 现状核对（只读）\n\n'
     '| 项 | 值 |\n| --- | --- |\n'
     f"| 部署记录 | `{facts['record']['mode']}`；`targetedRepair={str(facts['record']['targeted_repair']).lower()}`；用户文件核对 {facts['record']['user_files_checked']} 个 |\n"
     f"| 记录中的游戏 `data.win` | `{facts['record']['deployed_data_sha256'][:16]}…` |\n"
     f"| 当前游戏 `data.win` | `{facts['live']['data_sha256'][:16]}…`（{'与记录一致' if facts['live']['data_matches_record'] else '与记录不一致'}） |\n"
     f"| 备份集 `data.win` | `{facts['backup']['data_sha256'][:16]}…`（{'与 before.json 一致' if facts['backup']['data_sha256'] == str(facts['backup']['data_expected']).upper() else '与 before.json 不一致'}） |\n"
     f"| 备份集旧包 | `{facts['backup']['sml_sha256'][:16]}…` |\n"
     f"| 已部署副本 | `{facts['live']['deployed_sml_sha256'][:16]}…`（本地候选见 [[构建前置核对]] 的“最近一次构建”节） |\n\n"
     '## 用户侧前置状态（只读）\n\n'
     '| 项 | 值 |\n| --- | --- |\n'
     f"| MSL 设置 | `{facts['user_side']['settings_path']}`（{'存在' if facts['user_side']['settings_exists'] else '缺失'}，`{facts['user_side']['settings_sha256'][:16]}…`） |\n"
     f"| 本 Mod 是否启用 | {'已启用' if facts['user_side']['mod_enabled'] else '未启用'}（EnableMods 共 {len(facts['user_side']['enable_mods'])} 项，其余为玩家自装 Mod，部署时不动） |\n"
     f"| 用户数据文件 | 当前 {facts['user_side']['user_files_now']} 个／记录 {facts['user_side']['user_files_recorded']} 个（{'与部署记录一致' if facts['user_side']['user_files_now'] == facts['user_side']['user_files_recorded'] else '与记录不同：部署时会重新快照'}） |\n\n"
     '说明：部署脚本按包文件名识别 MSL 设置项；它只**追加**本 Mod 条目，不删除玩家自装 Mod。\n\n'
     '## 风险与边界\n\n'
     '- **不保证无损卸载**：带 Mod 状态的存档在回滚后可能无法正常读取（见 `README.md` 旧任务与存档节）；回滚只还原游戏资源与设置，不动用户数据。\n'
     '- 回滚**不会**清理 `msl/Mods` 下的其他 Mod，也不改 Steam 设置。\n'
     '- 本页是**计划**：本轮未部署、未回滚、未改游戏目录；执行后须按第 6 步留痕并重跑相关页。\n\n'
     '[[实现侧现状核对]] · [[构建前置核对]] · [[工具链离线自检记录]] · [[实现交接总表]] · [[待办与已知缺口登记]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S174部署与回滚手册（当前登记）\n\n[[部署与回滚运行手册]]：按两个脚本的实际行为写部署五步与回滚六步，并用当前备份集（`{Path(facts['record']['backup']).name}`）核对哈希；未执行部署或回滚。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'rollback-note-hashes.json'
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
rule = ('\n<!-- ROLLBACK-S174:BEGIN -->\n2026-10-13 S174：部署与回滚运行手册。'
        f"部署五步（退出→构建验收→备份与替换→记录→部署后核对）与回滚六步（定位备份集→校验→还原data.win→还原设置与旧包→复核→留痕）按脚本实际行为写成；当前备份集 {Path(facts['record']['backup']).name} 哈希已核对；不保证无损卸载、用户数据不动。"
        '本轮未执行部署或回滚。入口design/11_管理/部署与回滚运行手册.md；运行Validate-RollbackRunbook.py及既有检查。\n<!-- ROLLBACK-S174:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- ROLLBACK-S174:BEGIN -->.*?<!-- ROLLBACK-S174:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- ROLLBACK-S174:BEGIN -->.*?<!-- ROLLBACK-S174:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(backup=facts['record']['backup'].split('\\')[-1], files=len(facts['backup']['files']),
                      backup_data_matches=facts['backup']['data_sha256'] == str(facts['backup']['data_expected']).upper(),
                      live_matches=facts['live']['data_matches_record']), ensure_ascii=False))
