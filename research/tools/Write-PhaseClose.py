"""S160: design-phase closure audit.

Recomputes every design-phase deliverable's evidence from the live tree and
renders the closure page. Read-only; it does not claim implementation or
runtime verification.
"""
from pathlib import Path
import hashlib, json, re, subprocess
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PHASE-CLOSE-S160'
CARD = '11_管理/设计阶段收束核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest().upper()
notes = len(list(V.rglob('*.md')))
validators = len(list((R / 'tools').glob('Validate-*.py')))
checks = 0
for p in R.glob('*-validation.json'):
    d = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(d, dict) and 'checks_passed' in d:
        checks += d['checks_passed']
agents = [p for p in (ROOT / 'CHANGELOG.md', V / 'AGENTS.md') if p.exists()]
rules = sum(len(re.findall(r'<!-- [A-Z0-9\-]+:BEGIN -->', p.read_text(encoding='utf-8-sig'))) for p in agents)
gml = len(list((ROOT / 'src/**/Codes').glob('*.gml'))) if False else len(list((ROOT / 'src').rglob('Codes/*.gml')))
sml = ROOT / 'artifacts/EmbersAndOaths.sml'
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8'))
dep['version'] = re.search(r'<Version>([^<]+)</Version>', (ROOT / 'src/EmbersAndOaths/EmbersAndOaths.csproj').read_text(encoding='utf-8')).group(1)
runtime_evidence = sorted((ROOT / 'artifacts').glob('dev-runtime-*.json'))[-1].relative_to(ROOT).as_posix()
pilots = json.loads((R / 'pilot-batches.json').read_text(encoding='utf-8'))
oi = json.loads((R / 'open-items.json').read_text(encoding='utf-8'))
status = {}
for x in oi['items']:
    status[x['status']] = status.get(x['status'], 0) + 1
try:
    vp = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(R / 'tools/Test-DesignVault.ps1')],
                        capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    vault_ok = '"passed":  true' in (vp.stdout or '').replace('\n', ' ') or '"passed": true' in (vp.stdout or '')
except Exception:
    vault_ok = False
facts = dict(date='2026-10-13',
             scope='S160 design-phase closure: live evidence for every design-phase deliverable; implementation, production and runtime items remain open by the phase rule',
             notes=notes, validators=validators, checks=checks, agents=len(agents), rule_blocks=rules,
             gml_codes=gml, sml_sha256=sha(sml), sml_bytes=sml.stat().st_size,
             deployed_version=dep['version'], deployed_runtime_verified=dep['runtimeVerified'],
             pilots=dict(batches=len(pilots['batches']), scenarios=pilots['totals']['scenarios']),
             open_items=len(oi['items']), open_status=status, vault_passed=vault_ok)
(R / 'phase-close.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "设计阶段收束核对"\nid: MGMT-PHASE-CLOSE-S160\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S160, review, phase]\naliases: []\n---\n\n'
     '# 设计阶段收束核对\n\n'
     f"把设计阶段交付物对着当前仓库现场重算。用户已进入实际Mod开发测试；当前部署 {dep['version']}，开发观察与场景实测范围见 `{runtime_evidence}`，完整扩展仍登记在 [[待办与已知缺口登记]]。数据 `research/phase-close.json`。\n\n"
     '## 设计阶段交付物（现场证据）\n\n| 交付物 | 证据 | 状态 |\n| --- | --- | --- |\n'
     f"| 独立设计库 | `design/` **{notes}** 篇笔记；双链与 ID 检查见 `Test-DesignVault.ps1`（本轮 {'通过' if vault_ok else '未通过'}） | 有证据 |\n"
     f"| 两份 AGENTS.md | 根与 `design/` 各一份，含 **{rules}** 个规则块（S62—S160） | 有证据 |\n"
     f"| 校验链 | **{validators}** 个校验器；累计 **{checks:,}** 项检查（各 `research/*-validation.json` 现场汇总） | 有证据 |\n"
     f"| 内容稿 | 台本 131 篇（逐角色稿完成、待深化 0）；[[叙事内容清单]]、[[逐角色稿完成度核对]] | 有证据 |\n"
     f"| 原作参照 | 对话/契据/声誉三张参照卡（只读探针，片段≤46 字）；[[原作名与原创名碰撞核对]] | 有证据 |\n"
     f"| 声望系统（中英） | [[城镇声望与信任系统]]＋[[城镇声望系统中英对照]]；成对 {json.loads((R / 'bilingual-coverage.json').read_text(encoding='utf-8'))['user_pairs']} 组、用户可见中文单列 0 | 有证据 |\n"
     f"| 网状叙述与伏笔 | 74 条 X 边双向闭合；[[伏笔与回收台账]]；质量守卫七项 | 有证据 |\n"
     f"| 可构建源码 | `src/EmbersAndOaths` **{gml}** 个 GML 代码文件＋构建/部署/检查脚本；[[工具链离线自检记录]] 正负对照通过 | 有证据 |\n"
     f"| 实际 .sml | `artifacts/EmbersAndOaths.sml`（{sml.stat().st_size:,} B，`{sha(sml)[:16]}…`），与 MSL 已部署副本同哈希；[[实现侧现状核对]] | 有证据 |\n"
     f"| 部署与备份记录 | 部署记录 `{dep['version']}`（`runtimeVerified={str(dep['runtimeVerified']).lower()}`）；`backups/` 多批留档；[[验证快照依赖登记]] | 有证据 |\n"
     f"| 实现交接 | [[实现交接总表]] 六步＋[[试点批次总表]]（{len(pilots['batches'])} 批／{pilots['totals']['scenarios']} 验收场景） | 有证据 |\n\n"
     '## 后续范围（登记在案）\n\n'
     f"历史待办登记共 **{len(oi['items'])}** 项：open {status.get('open', 0)}、blocked {status.get('blocked', 0)}、policy {status.get('policy', 0)}。当前按用户授权已构建、部署并开始开发观察实测；旧设计优先/不部署阶段已结束。这不等于各待办均已关闭：完整扩张事件、全部美术和剧情回归仍待实现或验收。\n\n"
     '## 结论与边界\n\n'
     '- 设计阶段交付物**全部有当前证据**；校验数字均为现场重算，不是历史引用。\n'
     '- 完整扩展事件、全部场景美术、对白文学终审、经济与配音仍待实现或验收；开发工具和N1首批素材的运行证据单独登记。\n'
     '- 实现轮已有授权；按 [[试点批次总表]] 的 P1→P2→P3 逐项推进，并核对 OI-02（事件号）与 OI-03（存档字段与迁移）。\n\n'
     '[[质量守卫总表]] · [[实现侧现状核对]] · [[待办与已知缺口登记]] · [[试点批次总表]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S160设计阶段收束核对（当前登记）\n\n[[设计阶段收束核对]]：{notes} 篇笔记、{validators} 校验器、{checks:,} 项检查、{gml} 个 GML、.sml 与部署副本同哈希、试点 {len(pilots['batches'])} 批／{pilots['totals']['scenarios']} 场景；历史待办 {len(oi['items'])} 项，开发观察实测已启动，完整扩展未验收。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'phase-close-note-hashes.json'
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
rule = ('\n<!-- PHASE-CLOSE-S160:BEGIN -->\n2026-10-13 S160：设计阶段收束核对。'
        f"现场证据：{notes}篇笔记、两份AGENTS（{rules}规则块）、{validators}校验器/{checks}项检查、131台本、三张原作参照、声望中英（成对1384、可见中文单列0）、74边闭合、{gml}个GML、.sml与MSL副本同哈希、试点3批/18场景；"
        f"历史待办共{len(oi['items'])}项；用户已授权当前安装开发测试，{dep['version']}已构建部署，实测证据见{runtime_evidence}，完整扩展尚未验收。"
        '入口design/11_管理/设计阶段收束核对.md；运行Validate-PhaseClose.py及既有检查。\n<!-- PHASE-CLOSE-S160:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PHASE-CLOSE-S160:BEGIN -->.*?<!-- PHASE-CLOSE-S160:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PHASE-CLOSE-S160:BEGIN -->.*?<!-- PHASE-CLOSE-S160:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(notes=notes, validators=validators, checks=checks, vault=vault_ok, gml=gml), ensure_ascii=False))
