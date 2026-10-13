"""S161: N1 sample key semantics and the OI-03 migration proposal.

Scans the implemented GML for every EAO_N1_* usage, classifies reads and
writes, and renders the evidence page plus a migration proposal. Read-only.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'N1-KEYS-S161'
CARD = '11_管理/N1小样键语义与迁移建议.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
ENGINE = '11_管理/引擎键名前缀与遗留键登记.md'
rows = []
for p in sorted((ROOT / 'src/EmbersAndOaths/Codes').glob('*.gml')):
    for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
        for m in re.finditer(r'"(EAO_N1_[A-Za-z0-9_]+)"', line):
            key = m.group(1)
            kind = 'write' if 'ds_map_set' in line else ('read' if 'ds_map_find_value' in line or 'ds_map_exists' in line else 'reference')
            rows.append(dict(key=key, file=p.name, line=i, kind=kind, code=line.strip()[:120]))
writes = sorted({r['key'] for r in rows if r['kind'] == 'write'})
reads = sorted({r['key'] for r in rows if r['kind'] == 'read'})
stage_written = 'EAO_N1_stage' in writes
regnames = {k['key'] for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']}
facts = dict(date='2026-10-13',
             scope='S161 N1 sample key evidence: every EAO_N1_* usage classified read/write; migration proposal for OI-03; static analysis only, runtime not verified',
             usages=rows, written_keys=writes, read_keys=reads,
             stage_has_writer=stage_written,
             n1_registry_keys=sorted(k for k in regnames if k.endswith('_N1') or k.endswith('N1')),
             proposal=dict(entry_spawn_key='encountered_N1', resolution_key='resolve_N1',
                           compat='EAO_N1_stage 仅作读取垫片：若旧档存在且 ≥1，视为 encountered_N1=true；不再写入'))
(R / 'n1-stage-evidence.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "N1小样键语义与迁移建议"\nid: MGMT-N1-KEYS-S161\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S161, review, implementation]\naliases: []\n---\n\n'
     '# N1小样键语义与迁移建议\n\n'
     '为 OI-03（存档字段命名与旧档迁移）提供**证据与建议**：逐行扫描已实现 GML 里的 `EAO_N1_*` 用法，区分读与写。**静态分析**——未运行游戏，不代表实际存档行为。数据 `research/n1-stage-evidence.json`。\n\n'
     '## 用法清单（现场扫描）\n\n| 键 | 文件 | 行 | 读/写 | 代码 |\n| --- | --- | ---: | --- | --- |\n')
for r in rows:
    n += f"| `{r['key']}` | `{r['file']}` | {r['line']} | {r['kind']} | `{r['code']}` |\n"
n += (f"\n**写过的键**：{'、'.join('`' + k + '`' for k in writes) or '无'}；**只读的键**：{'、'.join('`' + k + '`' for k in reads)}。\n\n"
      '## 关键观察（静态）\n\n'
      f"- `EAO_N1_stage` **没有任何写入点**（扫描范围内 0 处 `ds_map_set`），只在 `night_controller_step.gml` 被读一次：`stage < 1` 时不生成 N1 入口对象。\n"
      "- 也就是说：**仅凭小样自身代码，这个门槛不会自行打开**；若运行时入口曾出现，说明有本仓库之外（或历史版本）的写入路径。这一条是静态结论，需实现轮用实际存档核对。\n"
      "- `EAO_N1_origin_*` 五个键由 `night_entry_alarm.gml` 写入、由 `night_return_alarm.gml` 读取，用于**从哪来回哪去**；语义清楚、可保留。\n\n"
      '## 迁移建议（供 OI-03 决策）\n\n'
      f"- 入口生成门槛改用登记键 **`{facts['proposal']['entry_spawn_key']}`**（`false/true`）：接取即 true，重载后仍 true；不再依赖未写入的 stage。\n"
      f"- 解法结果用登记键 **`{facts['proposal']['resolution_key']}`**（`none/shelter/audit`）承载；原 `stage` 与它**不是同一套语义**，不做数值映射推断。\n"
      f"- `EAO_N1_stage` 保留为**读取垫片**：旧档存在且 ≥1 时视为 `encountered_N1=true`，此后不再写入；新档不产生该键。\n"
      "- `EAO_N1_origin_*` 保留原名（属该小样的出发/返回机制），但按 S155 口径可统一为 `EAO_`＋登记名——若登记表未收录 origin 族，先在 [[状态键映射总表]] 登记再迁移。\n\n"
      '## 边界\n\n'
      '- 只读扫描；未运行游戏，未验证旧档实际取值，也未验证入口在游戏内是否出现。\n'
      '- 本页是**建议**，不是已执行决定；OI-03 由实现轮确认后，把结论回写 [[状态键映射总表]] 与 [[引擎键名前缀与遗留键登记]]。\n'
      '- 不改源码、不改存档、不部署。\n\n'
      '[[引擎键名前缀与遗留键登记]] · [[状态键映射总表]] · [[试点实现批次N2]] · [[待办与已知缺口登记]] · [[实现侧现状核对]]\n')
put(CARD, n)
eng = (V / ENGINE).read_text(encoding='utf-8')
if 'N1小样键语义与迁移建议' not in eng:
    eng = eng.replace('- 这条属于 [[待办与已知缺口登记]] 的 OI-03（存档字段命名与旧档迁移），实现轮第一件事。',
                      '- 这条属于 [[待办与已知缺口登记]] 的 OI-03（存档字段命名与旧档迁移），实现轮第一件事；证据与迁移建议见 [[N1小样键语义与迁移建议]]。', 1)
    put(ENGINE, eng)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S161 N1小样键语义（当前登记）\n\n[[N1小样键语义与迁移建议]]：逐行扫描 `EAO_N1_*`（{len(rows)} 处用法）——**`EAO_N1_stage` 无任何写入点**（静态结论），入口门槛改挂登记键 `encountered_N1`、解法用 `resolve_N1`、`stage` 仅作旧档读取垫片；供 OI-03 决策。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'n1-keys-note-hashes.json'
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
rule = ('\n<!-- N1-KEYS-S161:BEGIN -->\n2026-10-13 S161：N1小样键语义与迁移建议（只读扫描）。'
        f"扫描EAO_N1_*共{len(rows)}处用法：EAO_N1_stage无任何写入点（静态结论，运行时未验证）；建议入口门槛改挂encountered_N1、解法用resolve_N1、stage仅作旧档读取垫片；origin族语义清楚可保留。"
        '供OI-03决策；不改源码、不改存档、不部署。入口design/11_管理/N1小样键语义与迁移建议.md；运行Validate-N1Keys.py及既有检查。\n<!-- N1-KEYS-S161:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- N1-KEYS-S161:BEGIN -->.*?<!-- N1-KEYS-S161:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- N1-KEYS-S161:BEGIN -->.*?<!-- N1-KEYS-S161:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(usages=len(rows), writes=writes, reads=reads, stage_written=stage_written), ensure_ascii=False))
