"""S145: record the fifth full-chain replay drill (main order run + minimal copy).

Facts are captured from the actual runs: the canonical-order writer run in the
main repository, and a minimal copy (design/research/tools/src only) run of the
same order and of every validator. No design content changes; the record only
documents reproducibility and the environment-dependency inventory.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'REPLAY-S145'
CARD = '11_管理/全链复跑演练S145.md'
FLOW = '11_管理/设计库生成与校验流程.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
writers = sorted(p.name for p in (ROOT / 'research/tools').glob('Write-*.py'))
probes = sorted(p.name for p in (ROOT / 'research/tools').glob('Probe-*.py'))
validators = sorted(p.name for p in (ROOT / 'research/tools').glob('Validate-*.py'))
drill = dict(
    date='2026-10-13',
    scope='S145 fifth full-chain replay drill: canonical-order writer run in the main tree, and a minimal copy (design/research/tools/src) re-running the same order plus all validators; documentation of reproducibility and environment dependencies, not runtime',
    main_run=dict(order='design/11_管理/设计库生成与校验流程.md 生成链表内顺序（去重后 61 项，跳过 Validate-* 与需外部素材者）',
                  writers_ok=54, env_skipped=6, failures=0,
                  env_skipped_list=['Record-CityTaskArt.py', 'Record-ShoreVineTaskArt.py', 'Record-BrynnTaskArt.py',
                                    'Prepare-CityArt.py', 'Finalize-CityArtMetadata.py', 'Write-CitySpaces.py'],
                  note='主库按此顺序重跑后，65 个校验器与 Test-DesignVault.ps1 全通过。'),
    copy_run=dict(copy='%TEMP%/eao-replay-s145（仅 design/research/tools/src＋两份部署记录与 .sml）',
                  writers_ok=46, env_skipped=6, aborted=8,
                  aborted_list=['Write-CityIndexes.py', 'BrynnContinuation.py', 'Write-TownReputation.py',
                                'Write-ForeshadowLedger.py', 'Write-TimelineRegistry.py', 'Write-FineDetails.py',
                                'Write-ServiceRegistry.py', 'Write-ImplState.py'],
                  abort_reason='缺 backups/ 差异源与 artifacts/ 记录；首个中止后下游“保留既有笔记”守卫按设计连锁触发（不是静默覆盖）。',
                  validators_ok=49, validators_failed=16,
                  failed_validators=['Validate-AdditionalCityDrama.py', 'Validate-BrynnContinuation.py',
                                     'Validate-CareAndHighlandDrama.py', 'Validate-CityArt.py', 'Validate-CityDrama.py',
                                     'Validate-CitySpaces.py', 'Validate-CityTaskArt.py', 'Validate-FineDetails.py',
                                     'Validate-ForestAndMineDrama.py', 'Validate-ForgeAndWoolDrama.py',
                                     'Validate-GrainAndMemoryDrama.py', 'Validate-ImplHandoff.py', 'Validate-MaenDrama.py',
                                     'Validate-NamesAndPassDrama.py', 'Validate-ShoreAndVineDrama.py',
                                     'Validate-ShoreVineTaskArt.py'],
                  failed_reason='全部为环境项或首轮中止的后果：戏剧/城市类校验器读 backups/ 快照，美术类读 stoneshard-assets-sample，ImplHandoff 读计数页（依赖已中止的写手）。',
                  vault='Test-DesignVault.ps1 在副本中通过'),
    inventory=dict(writers=len(writers), probes=len(probes), validators=len(validators)),
    s165=dict(
        copy='%TEMP%/eao-replay-s165（design/research/tools/src ＋ artifacts 四件：两份部署记录、.sml、顺序表）',
        writers_ok=54, env_skipped=6, aborted=0,
        note='本轮把 artifacts 四件一并复制，写手链在副本中 54/0 全通过（S145 时缺 artifacts 导致 8 个写手中止）。',
        validators_ok=66, validators_failed=16,
        failed_validators=['Validate-AdditionalCityDrama.py', 'Validate-CareAndHighlandDrama.py', 'Validate-CityArt.py',
                           'Validate-CityDrama.py', 'Validate-CitySpaces.py', 'Validate-CityTaskArt.py',
                           'Validate-ForestAndMineDrama.py', 'Validate-ForgeAndWoolDrama.py', 'Validate-GrainAndMemoryDrama.py',
                           'Validate-MaenDrama.py', 'Validate-NamesAndPassDrama.py', 'Validate-PreservationBaselines.py',
                           'Validate-PhaseClose.py', 'Validate-ShoreAndVineDrama.py', 'Validate-ShoreVineTaskArt.py',
                           'Validate-ToolchainChecks.py'],
        failed_reason='全部为环境项或其后果：11 个戏剧/城市/快照类读 backups/，2 个美术类读 stoneshard-assets-sample，'
                      'ToolchainChecks 需 artifacts 的候选 .win 输入，PhaseClose 的数字取自主库（副本内校验器失败会改变合计）。',
        vault='Test-DesignVault.ps1 在副本中通过'))
(ROOT / 'research/replay-drill-s145.json').write_text(json.dumps(drill, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "全链复跑演练S145"\nid: MGMT-REPLAY-S145\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S145, review, replay]\naliases: []\n---\n\n'
     '# 全链复跑演练S145\n\n'
     '第五轮全链复跑：**主库**按 [[设计库生成与校验流程]] 生成链顺序重跑写手；**最小副本**（`%TEMP%/eao-replay-s145`，仅 `design/research/tools/src` 加两份部署记录与 `.sml`）重跑同一顺序与全部校验器。目的：证明链路可复现，并把**环境依赖**清点成表。只读文档，未改设计内容、未构建、未部署。\n\n'
     '## 主库按序重跑\n\n'
     '| 项 | 结果 |\n| --- | --- |\n'
     f"| 写手（按流程表顺序，去重 {drill['inventory']['writers']} 个 `Write-*`＋探针） | 通过 **{drill['main_run']['writers_ok']}**、需外部素材跳过 **{drill['main_run']['env_skipped']}**、失败 **0** |\n"
     '| 校验器 | 65 个全通过；`Test-DesignVault.ps1` 通过 |\n\n'
     '跳过项（需美术素材或备份差异源）：' + '、'.join('`' + x + '`' for x in drill['main_run']['env_skipped_list']) + '。\n\n'
     '## 最小副本\n\n'
     '| 项 | 结果 |\n| --- | --- |\n'
     f"| 写手 | 通过 **{drill['copy_run']['writers_ok']}**、跳过 **{drill['copy_run']['env_skipped']}**、中止 **{drill['copy_run']['aborted']}** |\n"
     f"| 校验器 | 通过 **{drill['copy_run']['validators_ok']}**、失败 **{drill['copy_run']['validators_failed']}**（全为环境项或中止后果） |\n"
     f"| 库检查 | {drill['copy_run']['vault']} |\n\n"
     '中止的写手：' + '、'.join('`' + x + '`' for x in drill['copy_run']['aborted_list']) + '。\n\n'
     f"原因：{drill['copy_run']['abort_reason']}\n\n"
     '失败的校验器：' + '、'.join('`' + x + '`' for x in drill['copy_run']['failed_validators']) + '。\n\n'
     f"原因：{drill['copy_run']['failed_reason']}\n\n"
     '## S165 复跑（第六轮，2026-10-13）\n\n'
     f"副本：{drill['s165']['copy']}。写手 **{drill['s165']['writers_ok']}** 通过／跳过 {drill['s165']['env_skipped']}／中止 **{drill['s165']['aborted']}**"
     f"（{drill['s165']['note']}）；校验器 **{drill['s165']['validators_ok']}** 通过／{drill['s165']['validators_failed']} 失败（{drill['s165']['failed_reason']}）；{drill['s165']['vault']}。\n\n"
     '## 结论与后续动作\n\n'
     '- **主库链路自洽**：按流程表顺序重跑无失败，重跑后全量校验与库检查通过——本轮新增的 S132—S144 工具（含两个探针、五项守卫、R/X 派生块、实现侧与工具链核对）都能在既有链路上重跑。\n'
     '- **顺序敏感**：写手一旦中止，下游"保留既有笔记"守卫会按设计连锁触发而不是静默覆盖；复跑时先修输入，再按原顺序继续。\n'
     '- **环境依赖清点**：`backups/` 供城市/戏剧类校验器与部分写手读差异源，`stoneshard-assets-sample` 供美术类，`artifacts/` 供实现侧与计数页；最小副本因此只覆盖 `design/research/tools/src` 可独立重跑的部分。\n'
     '- **未验证项**：副本未比对逐文件字节一致性（首轮中止改变了后续输入），故本轮只声明"主库可复现＋副本子集可复现"，不声明整树字节一致。\n\n'
     '## 边界\n\n'
     '- 演练只跑设计库工具；不构建、不部署、不写游戏目录。\n'
     '- 记录 `research/replay-drill-s145.json`；工具 `research/tools/Write-ReplayDrill.py`。\n\n'
     '[[设计库生成与校验流程]] · [[质量守卫总表]] · [[实现侧现状核对]] · [[逻辑验收记录]]\n')
put(CARD, n)
flow = (V / FLOW).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n- 全链复跑演练（S145，第五轮）：主库按生成链顺序重跑写手——通过 {drill['main_run']['writers_ok']}、需素材跳过 {drill['main_run']['env_skipped']}、失败 0；重跑后 65 校验器与 `Test-DesignVault.ps1` 全通过。最小副本（仅 `design/research/tools/src`）重跑同序写手 46 通过／8 中止（缺 `backups/`、`artifacts/` 输入，首个中止后下游保留守卫按设计连锁），49 校验器通过、16 失败（戏剧/城市类读 `backups/`、美术类读素材、计数页读已中止写手的结果）。结论：主库链路自洽、顺序敏感、环境依赖已清点；未声明整树字节一致。详见 [[全链复跑演练S145]]。\n" + z)
flow2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, flow, flags=re.S) if a in flow else flow.rstrip() + '\n' + blk + '\n'
put(FLOW, flow2)
t = (V / PLAN).read_text(encoding='utf-8-sig')
blk2 = (a + f"\n## S145全链复跑（当前登记）\n\n[[全链复跑演练S145]]：主库按序重跑写手 {drill['main_run']['writers_ok']} 通过/0 失败，随后全量校验与库检查通过；最小副本 46 通过/8 中止（环境输入缺失）、49 校验器通过。环境依赖与顺序敏感性已记录。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk2 + '\n'
put(PLAN, t2)
own = ROOT / 'research/replay-drill-note-hashes.json'
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
rule = ('\n<!-- REPLAY-S145:BEGIN -->\n2026-10-13 S145：第五轮全链复跑演练。'
        f"主库按生成链顺序重跑写手：通过{drill['main_run']['writers_ok']}、需素材跳过{drill['main_run']['env_skipped']}、失败0；重跑后65校验器与Test-DesignVault全通过。"
        f"最小副本（design/research/tools/src）重跑同序：写手46通过/8中止（缺backups与artifacts输入，下游保留守卫按设计连锁）、校验器49通过/16失败（戏剧城市类读backups、美术类读素材、计数页读已中止写手结果）。"
        '结论：主库链路自洽、顺序敏感、环境依赖已清点；未声明整树字节一致。'
        '入口design/11_管理/全链复跑演练S145.md；不构建、不部署。\n<!-- REPLAY-S145:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- REPLAY-S145:BEGIN -->.*?<!-- REPLAY-S145:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- REPLAY-S145:BEGIN -->.*?<!-- REPLAY-S145:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(main_ok=drill['main_run']['writers_ok'], copy_ok=drill['copy_run']['writers_ok'],
                      inventory=drill['inventory']), ensure_ascii=False))
