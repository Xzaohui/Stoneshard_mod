"""S143: implementation-side state snapshot (read-only).

Hashes the built package, the deployed MSL copy, the combined data.win and the
vanilla backup, cross-checks them against the recorded deployment values, and
renders the snapshot page. No build, no deployment, no game writes.
"""
from pathlib import Path
import hashlib, json, datetime, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'IMPL-STATE-S143'
CARD = '11_管理/实现侧现状核对.md'
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
def info(p):
    st = p.stat()
    return dict(path=str(p).replace('\\', '/'), bytes=st.st_size, sha256=sha(p),
                mtime=datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M'))
art = ROOT / 'artifacts/EmbersAndOaths.sml'
msl = GAME / 'msl/Mods/EmbersAndOaths.sml'
data = GAME / 'data.win'; vanilla = GAME / 'vanilla.win'
rec_night = json.loads((ROOT / 'artifacts/night-runtime-acceptance.json').read_text(encoding='utf-8'))
rec_direct = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8'))
dev_path = sorted((ROOT / 'artifacts').glob('dev-runtime-*.json'))[-1]
dev_evidence = dev_path.relative_to(ROOT).as_posix()
dev_run = json.loads(dev_path.read_text(encoding='utf-8')) if dev_path.exists() else {}
version = re.search(r'<Version>([^<]+)</Version>', (ROOT / 'src/EmbersAndOaths/EmbersAndOaths.csproj').read_text(encoding='utf-8')).group(1)
scene_paths = list((ROOT / 'artifacts').glob('scene-runtime-*.json'))
scene_path = max(scene_paths, key=lambda p: p.stat().st_mtime) if scene_paths else None
scene_run = json.loads(scene_path.read_text(encoding='utf-8')) if scene_path else {}
scene_evidence = scene_path.relative_to(ROOT).as_posix() if scene_path else ''
story = json.loads((ROOT / 'artifacts/story-validation.json').read_text(encoding='utf-8-sig'))
validation = json.loads((ROOT / 'artifacts/direct-validation.json').read_text(encoding='utf-8-sig'))
pilot_checks = story.get('checks', []) if story.get('inputSha256') == validation.get('outputSha256') else []
pilots_present = all(any(c.startswith(prefix) for c in pilot_checks) for prefix in ('cs-stub-registry-', 'fx-stub-registry-'))
pilot_summary = ('P2（CS-BRY-01）与 P3（FX-QRY）已进入当前候选，离线检查通过；逐项剧情和存读档实测仍待完成，其余 S62+ 设计稿仍分批实现。' if pilots_present else 'P2/P3 与其余 S62+ 设计稿尚未获得当前候选的离线验收证据。')

deployed_version = rec_direct.get('modVersion') or (version if sha(art) == rec_direct['packageSha256'] else '未登记')
base = json.loads((ROOT / 'research/local-baseline.json').read_text(encoding='utf-8'))
codes = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('src/**/Codes/*.gml'))
tools = sorted(p.name for p in (ROOT / 'tools').glob('*.ps1'))
state = dict(date=datetime.date.today().isoformat(),
             scope='S143 implementation-side snapshot: built package, deployed copy, combined data.win and vanilla backup hashed read-only; no build or deployment performed',
             artifact=info(art), msl_copy=info(msl), data_win=info(data), vanilla_win=info(vanilla),
             recorded=dict(package_sha256=rec_direct['packageSha256'], deployed_data_sha256=rec_direct['deployedDataSha256'],
                           version=deployed_version, deployment_date=rec_direct['date'],
                           runtime_verified=rec_direct['runtimeVerified']),
             runtime_observation=dev_run, runtime_evidence_path=dev_evidence,
             scene_runtime_observation=scene_run, scene_runtime_evidence_path=scene_evidence, pilots_present=pilots_present,
             baseline=dict(vanilla_sha256=base['candidate_baseline']['sha256'], strg_count=base['candidate_baseline']['strg_count']),
             sources=dict(gml_codes=len(codes), codes=codes, tools=tools))
(ROOT / 'research/impl-state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
artifact_is_deployed = state['artifact']['sha256'] == state['msl_copy']['sha256']
artifact_is_recorded = state['artifact']['sha256'] == state['recorded']['package_sha256']
checks = [
    ('本地候选与已部署副本', artifact_is_deployed,
     '一致' if artifact_is_deployed else '**不一致**：本地候选较新，部署待放行（OI-11）'),
    ('本地候选与部署记录', artifact_is_recorded,
     '一致' if artifact_is_recorded else f"不一致（记录为已部署包 `{state['recorded']['package_sha256'][:16]}…`）"),
    ('data.win 与部署记录一致', state['data_win']['sha256'] == state['recorded']['deployed_data_sha256'], '一致'),
    ('vanilla 与基线一致', state['vanilla_win']['sha256'] == state['baseline']['vanilla_sha256'], '一致'),
]
state['relationships'] = dict(artifact_is_deployed=artifact_is_deployed, artifact_is_recorded=artifact_is_recorded)
(ROOT / 'research/impl-state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p).lower()
n = ('---\ntitle: "实现侧现状核对"\nid: MGMT-IMPL-STATE-S143\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S143, review, implementation]\naliases: []\n---\n\n'
     '# 实现侧现状核对\n\n'
     '只读核对**实现侧现状**：已构建包、MSL 已部署副本、当前组合 `data.win` 与原版备份的哈希/大小/时间，并与部署记录逐项比对。生成本页的脚本只读游戏文件；实际构建、部署和开发工具实测另有记录，不等于完整扩展已完成。登记 `research/impl-state.json`。\n\n'
     '## 文件指纹\n\n| 项 | 大小 | SHA256（前16） | 时间 |\n| --- | ---: | --- | --- |\n')
for label, k in (('构建包 `artifacts/EmbersAndOaths.sml`', 'artifact'), ('MSL 已部署副本', 'msl_copy'),
                 ('组合 `data.win`', 'data_win'), ('原版 `vanilla.win`', 'vanilla_win')):
    d = state[k]
    n += f"| {label} | {d['bytes']:,} | `{d['sha256'][:16]}…` | {d['mtime']} |\n"
n += ('\n## 与记录的比对\n\n| 核对 | 结果 |\n| --- | --- |\n')
for label, ok, text in checks:
    n += f"| {label} | {text} |\n"
n += (f"\n部署记录（`artifacts/direct-deployment.json`）：版本 **{state['recorded']['version']}**、"
      f"部署时间 {state['recorded']['deployment_date'][:19].replace('T', ' ')}、`runtimeVerified`＝**{state['recorded']['runtime_verified']}**"
      f"（完整剧情与存读档验收未完成；开发工具与场景实测逐项见 `{dev_evidence}`，旧记录保留）。\n\n"
      '## 源码与工具\n\n'
      f"- MSL 工程：`src/EmbersAndOaths`，GML 代码 **{state['sources']['gml_codes']}** 个（含入口绘制、点击、夜间控制器、房间/对象生成与保存桥）；\n"
      f"- 构建/部署/检查脚本：{'、'.join('`' + t + '`' for t in state['sources']['tools'])}；\n"
      '- 备份：`backups/` 下按日期留档（城市稿、美术、戏剧稿等多批）。\n\n'
      '## 与本轮设计的关系\n\n'
      f"- 已部署副本为 **{deployed_version}**；本地候选 **{version}**，{'**已部署，与安装副本同哈希**' if artifact_is_deployed else '**未部署**（候选较新，见 OI-11）'}。[[试点实现批次N2]] P1 的五桩五键、灰堤三景已经接线；0.3.3 增加六景巡览和 N2 HD2D 开发适配，验收范围以候选校验与上述实测记录为准；\n"
      f'- {pilot_summary} [[实现交接总表]] 六步与 OI-01 在既有工程上分批新建事件；\n'
      '- 若重建包，本页四项指纹会变，须重跑本页与校验器（守卫会报"不一致"，提示刷新）。\n\n'
      '## 边界\n\n'
      '- 本页生成器只读哈希；实际安装与备份以本页引用的部署记录为准。\n'
      '- 完整任务/存读档回归尚未验收；`runtimeVerified` 仍为 false，开发观察实测与剧情全验收分开记录。\n'
      '- 本页不含任何新内容，也不改变部署门槛（见 `AGENTS.md`）。\n\n'
      '[[实现交接总表]] · [[待办与已知缺口登记]] · [[质量守卫总表]] · [[本地安装与证据]] · [[逻辑验收记录]]\n')
if scene_evidence:
    n += f"\n## 场景搭建运行证据\n\n灰堤外院、三建筑出入口、室内陈设与正常模式显示的本批证据见 `{scene_evidence}`（版本 {scene_run.get('modVersion', '未登记')}）；是否与当前安装一致按该记录的 `deployedDataSha256` 核对。该记录仅证明明列观察，不替代 OI-10 完整回归。\n"
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S143实现侧现状（当前登记）\n\n[[实现侧现状核对]]：部署记录版本 {deployed_version}、本地候选 {version}（试点P1/N2），{'候选与部署副本一致' if artifact_is_deployed else '候选较新，未部署'}；完整验收 `runtimeVerified=false`，开发观察实测见 `{dev_evidence}`；{pilot_summary}\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/impl-state-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- IMPL-STATE-S143:BEGIN -->\n2026-10-14 S143：实现侧现状核对（只读哈希）。'
        f"部署记录版本{deployed_version}、本地候选{version}，{'候选与安装副本同哈希、已部署' if artifact_is_deployed else '候选较新、未部署'}；N2五桩五键三景已接线，0.3.3增加六景巡览与N2 HD2D开发适配，完整验收runtimeVerified=false；实测见{dev_evidence}；GML代码{state['sources']['gml_codes']}个、构建/部署/检查脚本{'/'.join(t[:-4] for t in state['sources']['tools'])}；"
        f'{pilot_summary}重建包后须重跑本页与校验器。'
        '入口design/11_管理/实现侧现状核对.md；运行Validate-ImplState.py及既有检查。\n<!-- IMPL-STATE-S143:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- IMPL-STATE-S143:BEGIN -->.*?<!-- IMPL-STATE-S143:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- IMPL-STATE-S143:BEGIN -->.*?<!-- IMPL-STATE-S143:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(checks=[c[0] for c in checks if c[1]], failed=[c[0] for c in checks if not c[1]],
                      gml=state['sources']['gml_codes']), ensure_ascii=False))
