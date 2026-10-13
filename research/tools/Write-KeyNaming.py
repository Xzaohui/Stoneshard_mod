"""S123: reconcile legacy state-field names with the S114 key map.

Reads the legacy names from the S62-era notes, maps them to the current
per-script/per-route keys, records the table, and attaches a pointer block to
the two legacy notes. No key is renamed in data here.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'KEY-NAMES-S123'
CARD = '09_系统逻辑/键名口径对账.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
LEGACY_NOTES = ['09_系统逻辑/当前任务依赖与状态字典.md', '09_系统逻辑/网状叙事与条件对话规范.md']
PAT = re.compile(r'[a-z_]*resolve[A-Za-z_]*|[a-z_]*encountered[A-Za-z_]*|[a-z_]*receipt[A-Za-z_]*|[a-z_]*callback[A-Za-z_]*|[a-z_]*consent[A-Za-z_]*|[a-z_]*paid[A-Za-z_]*')
STRIP = re.compile(r'<!--\s*[A-Z0-9-]+:BEGIN\s*-->.*?<!--\s*[A-Z0-9-]+:END\s*-->', re.S)
BARE_WORDS = {'resolve', 'resolved'}
legacy = {}
for rel in LEGACY_NOTES:
    t = STRIP.sub('', (V / rel).read_text(encoding='utf-8'))
    legacy[rel] = sorted({m.group(0) for m in PAT.finditer(t)} - BARE_WORDS)
MAPPING = [
 ('resolve_ID', 'resolve_<脚本ID>', 'refined', 'S114 把结算键具体到脚本：ID 中的 `-` 换 `_`（CS-BRY-01 → CS_BRY_01）；取值＝路线/选项键，结算前 none。'),
 ('resolve_CM', 'resolve_<CM-XXX>', 'refined', 'S63 的 resolve_CM/CS 是族级命名；现按脚本逐个建键，不再用族级键。'),
 ('encountered', 'encountered_<脚本ID>', 'refined', '首次接触按脚本记；bool。'),
 ('callback_seen', 'callback_<脚本ID>_<路线>', 'refined', '回执按路线/选项逐条记；只表示已播，不重复给奖。'),
 ('consent', 'consent_<脚本ID>_<路线>', 'refined', '授权按路线逐条记；未授权不写。'),
 ('paid', 'paid_<脚本ID>_<路线>', 'refined', '费用按路线逐条记一次；仅路线含费用时建键。'),
 ('target_receipt', 'receipt_<回执ID>', 'refined', '跨任务回执按 CX##/BC85-## 建键；接收者与时机记在条目里，不写进键名。'),
]
CURRENT_SAMPLES = {
 'resolve_<脚本ID>': ['resolve_CS_BRY_01', 'resolve_N1'],
 'encountered_<脚本ID>': ['encountered_CS_BRY_01', 'encountered_N1'],
 'callback_<脚本ID>_<路线>': ['callback_CS_BRY_01_continuity'],
 'consent_<脚本ID>_<路线>': ['consent_CS_BRY_01_continuity'],
 'paid_<脚本ID>_<路线>': ['paid_CS_BRY_01_continuity'],
 'receipt_<回执ID>': ['receipt_CX01', 'receipt_BC85_01'],
 'resolve_<CM-XXX>': ['resolve_CM_BRY'],
}
sk = read('research/state-keys.json'); keys = {x['key'] for x in sk['keys']}
for _t, cur, _s, _n in MAPPING:
    for sample in CURRENT_SAMPLES.get(cur, []):
        assert sample in keys, (cur, sample)
out = dict(date='2026-10-13', scope='S123 key naming reconciliation: legacy S62-era field names mapped to the S114 per-script keys; current map is authoritative, legacy names stay as reading aliases only',
           legacy_found={k: v for k, v in legacy.items()}, mapping=[dict(legacy=l, current=c, status=s, note=n) for l, c, s, n in MAPPING],
           rules=['[[状态键映射总表]] 为唯一权威：键名、取值与语义以该表为准',
                  '旧文档中的 resolve_ID/encountered/target_receipt/consent/callback_seen/paid 只作阅读别名，不双写',
                  '实现时不得同时写族级键与脚本级键；族级命名仅保留在历史文档',
                  '回执接收者与时机写在条目里，不进入键名'])
(ROOT / 'research' / 'key-naming-reconciliation.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "键名口径对账"\nid: SYS-KEY-NAMES-S123\ntype: system\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S123, system, state]\naliases: []\n---\n\n'
     '# 键名口径对账\n\n'
     'S62 期文档用的是族级字段名（`resolve_ID`、`encountered`、`target_receipt`、`consent`、`callback_seen`、`paid`），S114 把键具体到脚本与路线。本页给出对账：**[[状态键映射总表]] 为唯一权威**，旧名只作阅读别名，不双写。\n\n'
     '| 旧名 | 现名 | 状态 | 说明 |\n|---|---|---|---|\n')
for l, c, s, note in MAPPING:
    n += f"| `{l}` | `{c}` | {s} | {note} |\n"
n += '\n## 规则\n\n' + '\n'.join('- ' + r for r in out['rules']) + '\n\n'
n += '## 旧文档中的出现位置\n\n| 文档 | 出现的旧名 |\n|---|---|\n'
for rel, names in legacy.items():
    n += f"| [[{Path(rel).stem}]] | " + '、'.join('`' + x + '`' for x in names) + ' |\n'
n += ('\n## 边界\n\n- 本页不改任何数据：键集合与取值仍以 [[状态键映射总表]] 与 `research/state-keys.json` 为准。\n'
      '- 旧文档不逐字改写；两篇旧文已加指向本页的提示块。\n'
      '- 未做：引擎侧字段名映射与旧档迁移策略。\n\n'
      '[[状态键映射总表]] · [[实现交接总表]] · [[当前任务依赖与状态字典]] · [[网状叙事与条件对话规范]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
# pointer blocks on the two legacy notes
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
ptr = ('## 键名口径（S123）\n\n本文出现的 `resolve_ID`/`encountered`/`target_receipt`/`consent`/`callback_seen`/`paid` 为族级旧名；'
       '当前权威键名为按脚本/按路线的具体键，见 [[键名口径对账]] 与 [[状态键映射总表]]。旧名只作阅读别名，实现不双写。')
for rel in LEGACY_NOTES:
    p2 = V / rel
    t2 = p2.read_text(encoding='utf-8-sig')
    nb = a + '\n' + ptr + '\n' + z
    t3 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t2, flags=re.S) if a in t2 else t2.rstrip() + '\n\n' + nb + '\n'
    put(rel, t3)
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb2 = a + '\n## S123键名口径对账（当前登记）\n\n[[键名口径对账]]：旧族级字段名（resolve_ID/encountered/target_receipt/consent/callback_seen/paid）映射到 S114 的按脚本/按路线键；[[状态键映射总表]] 为唯一权威，旧名只作阅读别名、不双写。\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb2 + '\n'
put(PLAN, t2)
own = ROOT / 'research/key-naming-note-hashes.json'
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
rule = ('\n<!-- KEY-NAMES-S123:BEGIN -->\n2026-10-13 S123：键名口径对账。'
        'research/key-naming-reconciliation.json 把S62旧族级字段名映射到S114按脚本/按路线键；[[状态键映射总表]]为唯一权威，旧名只作阅读别名、不双写；两篇旧文加提示块。'
        '入口design/09_系统逻辑/键名口径对账.md；运行Validate-KeyNaming.py及既有检查；引擎字段与旧档迁移仍待实现。\n<!-- KEY-NAMES-S123:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- KEY-NAMES-S123:BEGIN -->.*?<!-- KEY-NAMES-S123:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- KEY-NAMES-S123:BEGIN -->.*?<!-- KEY-NAMES-S123:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/09_系统逻辑/键名口径对账.md', '入口 [键名口径对账](design/09_系统逻辑/键名口径对账.md)'), encoding='utf-8')
print(json.dumps(dict(mapping=len(MAPPING), legacy_notes=len(LEGACY_NOTES), notes=len(generated)), ensure_ascii=False))
