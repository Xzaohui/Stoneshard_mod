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
dev_path = ROOT / 'artifacts/dev-runtime-20261013.json'
dev_run = json.loads(dev_path.read_text(encoding='utf-8')) if dev_path.exists() else {}
version = re.search(r'<Version>([^<]+)</Version>', (ROOT / 'src/EmbersAndOaths/EmbersAndOaths.csproj').read_text(encoding='utf-8')).group(1)
base = json.loads((ROOT / 'research/local-baseline.json').read_text(encoding='utf-8'))
codes = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('src/**/Codes/*.gml'))
tools = sorted(p.name for p in (ROOT / 'tools').glob('*.ps1'))
state = dict(date='2026-10-13',
             scope='S143 implementation-side snapshot: built package, deployed copy, combined data.win and vanilla backup hashed read-only; no build or deployment performed',
             artifact=info(art), msl_copy=info(msl), data_win=info(data), vanilla_win=info(vanilla),
             recorded=dict(package_sha256=rec_direct['packageSha256'], deployed_data_sha256=rec_direct['deployedDataSha256'],
                           version=version, deployment_date=rec_direct['date'],
                           runtime_verified=rec_direct['runtimeVerified']),
             runtime_observation=dev_run,
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
      "（完整剧情与存读档验收未完成；本次开发工具实测逐项见 `artifacts/dev-runtime-20261013.json`，旧0.3.0记录保留）。\n\n"
      '## 源码与工具\n\n'
      f"- MSL 工程：`src/EmbersAndOaths`，GML 代码 **{state['sources']['gml_codes']}** 个（含入口绘制、点击、夜间控制器、房间/对象生成与保存桥）；\n"
      f"- 构建/部署/检查脚本：{'、'.join('`' + t + '`' for t in state['sources']['tools'])}；\n"
      '- 备份：`backups/` 下按日期留档（城市稿、美术、戏剧稿等多批）。\n\n'
      '## 与本轮设计的关系\n\n'
      f"- 当前工程 **{version}**：无钟之夜小样、可选世界格传送及开发观察工具、N1 HD2D首批素材；**不含** S62+ 的城市/对白/声望设计稿；\n"
      '- 因此 [[实现交接总表]] 的六步与 [[待办与已知缺口登记]] 的 OI-01 需要在现有工程上**新建事件**，而不是修改旧包；\n'
      '- 若重建包，本页四项指纹会变，须重跑本页与校验器（守卫会报"不一致"，提示刷新）。\n\n'
      '## 边界\n\n'
      '- 本页生成器只读哈希；实际安装与备份以本页引用的部署记录为准。\n'
      '- 完整任务/存读档回归尚未验收；`runtimeVerified` 仍为 false，开发观察实测与剧情全验收分开记录。\n'
      '- 本页不含任何新内容，也不改变部署门槛（见 `AGENTS.md`）。\n\n'
      '[[实现交接总表]] · [[待办与已知缺口登记]] · [[质量守卫总表]] · [[本地安装与证据]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S143实现侧现状（当前登记）\n\n[[实现侧现状核对]]：构建包与 MSL 副本同哈希（`{state['artifact']['sha256'][:16]}…`）、data.win 与部署记录一致、vanilla 与基线一致；{version} 完整验收 `runtimeVerified=false`，开发观察实测见本页证据指针；S62+ 设计稿尚未进包。\n" + z)
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
rule = ('\n<!-- IMPL-STATE-S143:BEGIN -->\n2026-10-13 S143：实现侧现状核对（只读哈希）。'
        f"构建包与MSL副本同哈希、data.win与部署记录一致、vanilla与基线一致；{version}完整验收runtimeVerified=false，开发观察实测独立登记；GML代码{state['sources']['gml_codes']}个、构建/部署/检查脚本{'/'.join(t[:-4] for t in state['sources']['tools'])}；"
        'S62—S143设计稿尚未进包，OI-01须在现有工程上新建事件。重建包后须重跑本页与校验器。'
        '入口design/11_管理/实现侧现状核对.md；运行Validate-ImplState.py及既有检查；不构建、不部署。\n<!-- IMPL-STATE-S143:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- IMPL-STATE-S143:BEGIN -->.*?<!-- IMPL-STATE-S143:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- IMPL-STATE-S143:BEGIN -->.*?<!-- IMPL-STATE-S143:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(checks=[c[0] for c in checks if c[1]], failed=[c[0] for c in checks if not c[1]],
                      gml=state['sources']['gml_codes']), ensure_ascii=False))
