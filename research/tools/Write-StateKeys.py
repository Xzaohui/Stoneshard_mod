"""S114: derive the implementation state-key map for every script and receipt.

Keys are computed deterministically from the sources: encounter/settlement,
callbacks, cost, order, presence, consent and cross-impact receipts. IDs keep
their hyphens in data but keys use underscores (documented convention).
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'STATE-KEYS-S114'
CARD = '09_系统逻辑/状态键映射总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
fx = read('research/field-npc-dialogue.json')
def k(s): return s.replace('-', '_')
keys = []
def add(key, kind, script, source, values=None, note=''):
    keys.append(dict(key=key, kind=kind, script=script, source=source, values=values or [], note=note))
# city quests
for q in model['quests']:
    sid = q['id']
    routes = [r['key'] for r in q.get('routes') or []]
    add(f'encountered_{k(sid)}', 'encounter', sid, 'research/city-campaign.json', ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, 'research/city-campaign.json', ['none'] + routes)
    for r in q.get('routes') or []:
        add(f'callback_{k(sid)}_{k(r["key"])}', 'callback', sid, 'research/city-campaign.json', ['false', 'true'])
        add(f'consent_{k(sid)}_{k(r["key"])}', 'consent', sid, 'research/city-campaign.json', ['false', 'true'],
            note='本人或限权授权，未授权不写')
        if r.get('cost'): add(f'paid_{k(sid)}_{k(r["key"])}', 'paid', sid, 'research/city-campaign.json', ['false', 'true'],
                              note='本案费用只记一次')
    ex = q.get('dramatic_exceptions') or {}
    if ex.get('dead') or ex.get('refusal'):
        add(f'presence_{k(sid)}', 'presence', sid, 'research/city-campaign.json', ['present', 'absent', 'dead', 'refused'])
    if ex.get('before_city') or ex.get('after_city'):
        add(f'order_{k(sid)}', 'order', sid, 'research/city-campaign.json', ['early', 'late', 'unknown'])
# continuation quests
for q in cont['quests']:
    sid = q['id']
    routes = [r['key'] for r in q.get('routes') or []]
    add(f'encountered_{k(sid)}', 'encounter', sid, 'research/brynn-continuation.json', ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, 'research/brynn-continuation.json', ['none'] + routes)
    for r in q.get('routes') or []:
        add(f'callback_{k(sid)}_{k(r["key"])}', 'callback', sid, 'research/brynn-continuation.json', ['false', 'true'])
        add(f'consent_{k(sid)}_{k(r["key"])}', 'consent', sid, 'research/brynn-continuation.json', ['false', 'true'])
        if r.get('cost'): add(f'paid_{k(sid)}_{k(r["key"])}', 'paid', sid, 'research/brynn-continuation.json', ['false', 'true'])
    if q.get('interruption'):
        add(f'presence_{k(sid)}', 'presence', sid, 'research/brynn-continuation.json', ['present', 'absent', 'dead', 'refused'])
# story families
for name, fam in [('story-main.json', 'main'), ('story-side.json', 'side'), ('story-main-late.json', 'main-late'), ('story-dungeon.json', 'dungeon')]:
    for x in read('research/' + name):
        sid = x['id']
        choices = [c[0] for c in x.get('choices') or []]
        add(f'encountered_{k(sid)}', 'encounter', sid, 'research/' + name, ['false', 'true'])
        add(f'resolve_{k(sid)}', 'resolve', sid, 'research/' + name, ['none'] + choices)
        for c in choices:
            add(f'callback_{k(sid)}_{k(c)}', 'callback', sid, 'research/' + name, ['false', 'true'])
        if x.get('recovery'):
            add(f'presence_{k(sid)}', 'presence', sid, 'research/' + name, ['present', 'absent', 'dead', 'refused'])
for x in read('research/story-daily.json'):
    sid = x['id']
    add(f'encountered_{k(sid)}', 'encounter', sid, 'research/story-daily.json', ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, 'research/story-daily.json', ['none', 'done', 'failed'])
# field NPC presence
for n in fx['npcs']:
    add(f'presence_{k(n["id"])}', 'presence', n['id'], 'research/field-npc-dialogue.json', ['present', 'absent', 'dead', 'refused'])
# receipts: city effects + continuation effects
for e in model['effects']:
    add(f'receipt_{k(e["id"])}', 'receipt', e['id'], 'research/city-campaign.json', ['false', 'true'],
        note=f'{e["source"]}→{e["target"]}；接收者 {e["receiver"]}；{e["receipt"]}；{e["timing"]}')
for e in cont['effects']:
    add(f'receipt_{k(e["id"])}', 'receipt', e['id'], 'research/brynn-continuation.json', ['false', 'true'],
        note=f'{e["source"]}→{e["target"]}；{e["guard"]}')
# unify and check
seen = {}
for item in keys:
    assert item['key'] not in seen, item['key']
    seen[item['key']] = item
    assert re.fullmatch(r'[a-z]+_[A-Za-z0-9_]+', item['key']), item['key']
    assert not re.search(r'reward|gold|price|coin', item['key']), item['key']
fam_counts = {}
for item in keys: fam_counts[item['kind']] = fam_counts.get(item['kind'], 0) + 1
out = dict(date='2026-10-13', scope='S114 implementation state-key map: deterministic keys for encounter, settlement, callbacks, cost, order, presence, consent and cross-impact receipts',
           conventions=['键名把 ID 里的 `-` 换成 `_`（如 CS-BRY-01 → CS_BRY_01）',
                        '`resolve_*` 在结算前为 `none`，结算后取唯一路线/选项键；不回滚',
                        '`callback_*` 只表示该回执已播过；不重复给奖',
                        '`paid_*` 只记一次费用；`consent_*` 记本人或限权授权',
                        '`presence_*` 四态：present/absent/dead/refused；缺席不代播新句',
                        '`receipt_CX##` 为跨任务回执；接收者与时机见 note'],
           families=fam_counts, keys=keys)
(ROOT / 'research' / 'state-keys.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "状态键映射总表"\nid: SYS-STATE-KEYS-S114\ntype: system\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-14\ntags: [stoneshard, S114, system, state]\naliases: []\n---\n\n'
     '# 状态键映射总表\n\n'
     '把全库脚本与回执映射成实现用状态键（共 '
     f"{len(keys)} 个）。键名与取值由源文件确定性推导，见 `research/state-keys.json`；本页给出约定、族计数与逐项清单。\n\n"
     '**约定**：\n\n' + '\n'.join('- ' + c for c in out['conventions']) + '\n\n'
     '| 族 | 键数 | 说明 |\n|---|---:|---|\n')
fam_desc = {'encounter': '首次接触是否已发生', 'resolve': '唯一结算与路线/选项取值', 'callback': '逐路线/选项回执是否已播',
            'paid': '本案费用只记一次', 'order': '先做/后做次序', 'presence': '在场四态', 'consent': '本人或限权授权',
            'receipt': '跨任务回执（接收者与时机见条目）'}
for fam in ['encounter', 'resolve', 'callback', 'consent', 'paid', 'order', 'presence', 'receipt']:
    n += f"| {fam} | {fam_counts.get(fam, 0)} | {fam_desc[fam]} |\n"
n += '\n## 脚本键（按族取样）\n\n'
for fam in ['encounter', 'resolve', 'consent', 'paid', 'order', 'presence']:
    sub = [x for x in keys if x['kind'] == fam][:6]
    n += f"**{fam}**：" + '、'.join('`' + x['key'] + '`' for x in sub) + f"（共 {fam_counts.get(fam, 0)}）\n\n"
n += '## 跨任务回执（CX/BC85）\n\n| 键 | 源→目标 | 接收者/守卫 | 内容与时机 |\n|---|---|---|---|\n'
for x in keys:
    if x['kind'] != 'receipt': continue
    m = re.match(r'([^；]+)；接收者 ([^；]+)；([^；]+)；(.+)', x['note'])
    if m:
        n += f"| `{x['key']}` | {m.group(1)} | {m.group(2)} | {m.group(3)}；{m.group(4)} |\n"
    else:
        n += f"| `{x['key']}` | {x['note']} | — | — |\n"
n += ('\n## 旧档迁移与缺键口径（OI-03 定稿，2026-10-14）\n\n'
      '- **引擎键名＝`EAO_`＋登记键名**（[[引擎键名前缀与遗留键登记]]）：`encountered_N2` → `EAO_encountered_N2`。首批 [[试点批次总表]] P1（N2）五键已按此落地进 0.3.2 候选。\n'
      '- **取值存储**：枚举类（`resolve_*`、`presence_*`）存字符串；二值类（`encountered_*`/`callback_*`/`consent_*`/`paid_*`/`order_*` 的真假键）存整数 1＝真。\n'
      '- **缺键读取口径**：`resolve_*` 缺省 `none`（未结算，读档后仍为 none，见 [[试点批次验收场景N2]] T06）；二值类缺省假；`presence_*` 缺省 `present`。读取从不回写、不构成"已知"授权。\n'
      '- **旧字段不自动迁移**：N1 小样键（`EAO_N1_*`）、旧任务键（`EAO_MQ0*`）、测试传送与开发观察键原样保留，只读不重映射；N1 重制时按 [[N1小样键语义与迁移建议]] 改挂登记键，此前不动。\n'
      '- **同一脚本不得双写**：N1 小样完整保留样例键至重制；N2 起一律登记键（见 [[键名口径对账]]）。两套键并存于同一存档是允许的（不同脚本族），同一脚本内不允许。\n\n'
      '## 与条件流的对应\n\n'
      '- `first_meet` ⇔ `encountered_* = false`；`task_done` ⇔ `resolve_* != none`；`route(<key>)` ⇔ `resolve_* == <key>`。\n'
      '- `order_early/late` ⇔ `order_*`；`refused`/`npc_absent` ⇔ `presence_*`；回执播放 ⇔ `callback_*`。\n'
      '- 条件图（[[全库条件流投影]]）的 `when` 不直接写引擎键，由本页给出映射。\n\n'
      '## 边界\n\n- 本页只给键名、取值与语义；OI-03 口径已定稿并经 P1 五键离线落地，实机读档验证随 [[待办与已知缺口登记]] OI-10。\n'
      '- 旧字段与旧存档不自动迁移；投影不等于真实存档变化。\n'
      '- 键不含奖励、金币与库存语义；结算仍归各台本唯一所有者。\n\n'
      '[[当前任务依赖与状态字典]] · [[全库条件流投影]] · [[对白分支覆盖审计]] · [[任务台本总索引]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S114状态键映射（当前登记）\n\n'
           f"[[状态键映射总表]]：{len(keys)} 个实现用状态键（encounter/resolve/callback/consent/paid/order/presence 与 {fam_counts.get('receipt', 0)} 个跨任务回执 CX/BC85），"
           '键名与取值由源确定性推导，条件流 when 的映射见页内；不含奖励语义、不迁移旧存档。')
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/state-keys-note-hashes.json'
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
rule = ('\n<!-- STATE-KEYS-S114:BEGIN -->\n2026-10-13 S114：状态键映射（实现桥）。'
        f'research/state-keys.json 由源确定性推导 {len(keys)} 个实现用状态键（encounter/resolve/callback/consent/paid/order/presence＋{fam_counts.get("receipt", 0)} 个跨任务回执）；键名 ID 中 `-` 换 `_`，resolve 结算前 none、结算后唯一取值，回执只记已播。'
        '入口design/09_系统逻辑/状态键映射总表.md；条件流 when 的映射见页内。不迁移旧存档、不含奖励语义；运行Validate-StateKeys.py及既有检查；不部署游戏包。\n<!-- STATE-KEYS-S114:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- STATE-KEYS-S114:BEGIN -->.*?<!-- STATE-KEYS-S114:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- STATE-KEYS-S114:BEGIN -->.*?<!-- STATE-KEYS-S114:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/09_系统逻辑/状态键映射总表.md', '入口 [状态键映射总表](design/09_系统逻辑/状态键映射总表.md)'), encoding='utf-8')
print(json.dumps(dict(keys=len(keys), families=fam_counts), ensure_ascii=False))

# Rebuild the independent HX conditional extension after the base projection.
import runpy
runpy.run_path(str(ROOT / "research/tools/Write-HeavyEdges.py"))
