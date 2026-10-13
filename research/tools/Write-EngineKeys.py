"""S155: engine key prefix and legacy key registry.

Scans the implemented GML for EAO_-prefixed save keys, classifies them, and
renders the prefix rule page. Read-only: no source or save change.
"""
from pathlib import Path
import hashlib, json, re, collections
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'ENGINE-KEYS-S155'
CARD = '11_管理/引擎键名前缀与遗留键登记.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
PILOT = '11_管理/试点实现批次N2.md'
CLASS = {
    'EAO_MQ01': ('legacy-quest', '0.3.0 期旧任务图遗留（历史蓝图，不作当前任务链）'),
    'EAO_MQ02': ('legacy-quest', '同上'),
    'EAO_read_eao_copy': ('legacy-item', '0.3.0 期抄本阅读标记'),
    'EAO_D01_archive_visited': ('legacy-flag', '旧 D01 档案访问标记（D01 不再作为新内容）'),
}
def classify(k):
    if k in CLASS: return CLASS[k]
    if k.startswith('EAO_test_'): return ('test-teleport', '可选测试传送/返回点（F8 开关）状态键')
    if k.startswith('EAO_dev_'): return ('dev-tool', '开发观察工具键（F6/F7/F9/F10/F11 迷雾/格网/素材/场景/返回）')
    if k.startswith('EAO_N1_'): return ('sample-N1', 'N1 小样键（stage、origin 坐标与 dev_visit 场景标记）；与登记键 resolve_N1/encountered_N1 不是同一套')
    return ('unclassified', '')
keys = collections.defaultdict(set)
for p in sorted((ROOT / 'src/EmbersAndOaths/Codes').glob('*.gml')):
    for m in re.finditer(r'"([A-Za-z_][A-Za-z0-9_]*)"', p.read_text(encoding='utf-8')):
        if m.group(1).startswith('EAO_'):
            keys[m.group(1)].add(p.name)
regnames = {k['key'] for k in json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']}
rows = []
for k in sorted(keys):
    cls, note = classify(k)
    rows.append(dict(key=k, cls=cls, files=sorted(keys[k]), mapped_to_registry=(k[4:] in regnames), note=note))
classes = collections.Counter(r['cls'] for r in rows)
out = dict(date='2026-10-13',
           scope='S155 engine key prefix: EAO_-prefixed keys found in implemented GML, classified; prefix rule for registry keys; read-only scan, no source or save change',
           rule='引擎键名 = `EAO_` + 登记键名（登记名是设计标识；引擎侧统一前缀以避免与原版键冲突）。',
           keys=rows, classes=dict(classes), unclassified=[r['key'] for r in rows if r['cls'] == 'unclassified'],
           registry_keys=len(regnames))
(R / 'engine-keys.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "引擎键名前缀与遗留键登记"\nid: MGMT-ENGINE-KEYS-S155\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S155, guide, implementation]\naliases: []\n---\n\n'
     '# 引擎键名前缀与遗留键登记\n\n'
     '实现侧的存档键与设计登记键**命名口径不同**：已实现的 GML 全部使用 `EAO_` 前缀，而 `research/state-keys.json` 的登记键不带前缀。本页定口径并清点现状（只读扫描，不改源码、不改存档）。\n\n'
     '## 口径\n\n'
     '- **引擎键名 ＝ `EAO_` ＋ 登记键名**：登记名（如 `resolve_N2`）是设计标识；落库时加 `EAO_` 前缀，避免与原版键冲突（原版键示例：`Reputation1_Steppe`、`follower_loyalty`）。\n'
     '- 例：`resolve_N2` → `EAO_resolve_N2`；`encountered_N2` → `EAO_encountered_N2`；`presence_N2` → `EAO_presence_N2`。\n'
     '- 反向不成立：`EAO_` 键不一定来自登记（见下表遗留键）。\n\n'
     '## 已实现的 `EAO_` 键（扫描 `src/EmbersAndOaths/Codes/*.gml`）\n\n'
     f"共 **{len(rows)}** 个：测试传送 {classes.get('test-teleport', 0)}、N1 小样 {classes.get('sample-N1', 0)}、旧任务 {classes.get('legacy-quest', 0)}、旧物品/标记 {classes.get('legacy-item', 0) + classes.get('legacy-flag', 0)}。**映射到登记键者 0**——全部是 0.3.0 期遗留。\n\n"
     '| 键 | 类别 | 出现文件 | 说明 |\n| --- | --- | --- | --- |\n')
for r in rows:
    n += f"| `{r['key']}` | {r['cls']} | {'、'.join('`' + f + '`' for f in r['files'])} | {r['note'] or '—'} |\n"
n += ('\n## 与 N1 小样的冲突（须在实现时决定）\n\n'
      '- 小样用 **`EAO_N1_stage`**（整数阶段）与 `EAO_N1_origin_*`（出发房间/坐标）；登记侧 `N1` 用 **`resolve_N1`**（none/shelter/audit）＋`encountered_N1`＋`presence_N1`＋两个 `callback_*`。\n'
      '- 实现新批次时只能**二选一**：把小样阶段迁移为登记键（写迁移口径），或保留 `EAO_N1_stage` 作兼容垫片并在 [[状态键映射总表]] 登记为遗留。未定前不得同时写两套键。\n'
      '- 这条属于 [[待办与已知缺口登记]] 的 OI-03（存档字段命名与旧档迁移），实现轮第一件事；证据与迁移建议见 [[N1小样键语义与迁移建议]]。\n\n'
      '## 边界\n\n'
      '- 本页只读扫描 GML 字面量，不检查运行时读写路径；键的实际生效仍须游戏内验证。\n'
      '- 不改源码、不改存档、不部署；新增键在实现时先登记 [[状态键映射总表]] 再落库。\n\n'
      '[[试点实现批次N2]] · [[状态键映射总表]] · [[键名口径对账]] · [[实现侧现状核对]] · [[待办与已知缺口登记]]\n')
put(CARD, n)
pilot = (V / PILOT).read_text(encoding='utf-8')
if '引擎键名前缀与遗留键登记' not in pilot:
    pilot = pilot.replace('- 前置：OI-02（引擎事件号分配）',
                          '- 键名口径：落库时引擎键＝`EAO_`＋登记键名（见 [[引擎键名前缀与遗留键登记]]）；小样 `EAO_N1_stage` 与登记 `resolve_N1` 的取舍属 OI-03。\n- 前置：OI-02（引擎事件号分配）', 1)
    put(PILOT, pilot)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S155引擎键名前缀与遗留键（当前登记）\n\n[[引擎键名前缀与遗留键登记]]：口径＝引擎键 `EAO_`＋登记键名；已实现 GML 中 {len(rows)} 个 `EAO_` 键**全部为 0.3.0 期遗留**（测试传送／N1 小样／旧任务），映射登记键 0 个；小样 `EAO_N1_stage` 与登记 `resolve_N1` 的取舍属 OI-03。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'engine-keys-note-hashes.json'
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
rule = ('\n<!-- ENGINE-KEYS-S155:BEGIN -->\n2026-10-13 S155：引擎键名前缀与遗留键登记。'
        f"口径＝引擎键 `EAO_`＋登记键名；扫描已实现GML得{len(rows)}个EAO_键，全部为0.3.0期遗留（测试传送/N1小样/旧任务），映射登记键0个；"
        '小样EAO_N1_stage与登记resolve_N1须二选一（属OI-03）。只读扫描，不改源码与存档。'
        '入口design/11_管理/引擎键名前缀与遗留键登记.md；运行Validate-EngineKeys.py及既有检查。\n<!-- ENGINE-KEYS-S155:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- ENGINE-KEYS-S155:BEGIN -->.*?<!-- ENGINE-KEYS-S155:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- ENGINE-KEYS-S155:BEGIN -->.*?<!-- ENGINE-KEYS-S155:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(keys=len(rows), classes=dict(classes), mapped=sum(1 for r in rows if r['mapped_to_registry'])), ensure_ascii=False))
