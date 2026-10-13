"""S163: event-number allocation scheme for the 1,807 event stubs.

Deterministic allocation: family base ranges, per-script blocks rounded to the
next 64, one number per stub in registry order. Planning only; no engine change.
"""
from pathlib import Path
import hashlib, json, re, collections
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'EVT-NUM-S163'
CARD = '11_管理/事件号分配方案.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
STUBS_PAGE = '09_系统逻辑/事件桩映射总表.md'
def family(script):
    if script.startswith('DT'): return 'DT'
    if script.startswith('D') and not script.startswith('DT'): return 'D'
    if script.startswith('N'): return 'N'
    if script.startswith('SQ'): return 'SQ'
    if script.startswith('CM'): return 'CM'
    if script.startswith('CS'): return 'CS'
    if script.startswith('FX'): return 'FX'
    return 'other'
BASE = {'N': 10000, 'SQ': 20000, 'DT': 30000, 'D': 40000, 'CS': 50000, 'CM': 60000, 'FX': 70000, 'other': 90000}
stubs = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
by_script = collections.OrderedDict()
for s in stubs:
    by_script.setdefault(s['script'], []).append(s['event'])
alloc = []
used = set()
for fam, base in BASE.items():
    scripts = sorted(k for k in by_script if family(k) == fam)
    offset = 0
    for sc in scripts:
        n = len(by_script[sc])
        block = ((n + 63) // 64) * 64
        start = base + offset
        end = start + block - 1
        for i, ev in enumerate(by_script[sc]):
            num = start + i
            assert num not in used, 'overlap at ' + str(num)
            used.add(num)
            alloc.append(dict(event=ev, script=sc, number=num))
        offset += block
    if scripts:
        pass
reg = dict(date='2026-10-13',
           scope='S163 event-number allocation scheme: deterministic per-script blocks within family ranges, one number per stub; planning only, engine numbers are assigned at implementation time',
           bases=BASE, allocations=alloc, total=len(alloc),
           per_family={f: dict(scripts=len([k for k in by_script if family(k) == f]),
                               stubs=sum(len(v) for k, v in by_script.items() if family(k) == f)) for f in BASE if any(family(k) == f for k in by_script)})
(R / 'event-number-scheme.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
rng = {}
for a in alloc:
    f = family(a['script'])
    lo, hi = rng.get(f, (a['number'], a['number']))
    rng[f] = (min(lo, a['number']), max(hi, a['number']))
n = ('---\ntitle: "事件号分配方案"\nid: MGMT-EVT-NUM-S163\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S163, guide, implementation]\naliases: []\n---\n\n'
     '# 事件号分配方案\n\n'
     f"把 [[事件桩映射总表]] 的 **{len(alloc)}** 个桩按**确定性规则**预分配引擎事件号：家族基址 + 脚本块（按 64 对齐）+ 登记顺序逐桩递增。本页只给方案与分配表，**引擎号在实现时分配并回写** [[事件桩映射总表]]；不构建、不部署。数据 `research/event-number-scheme.json`。\n\n"
     '## 家族基址与范围\n\n| 家族 | 基址 | 脚本数 | 桩数 | 实际占用范围 |\n| --- | ---: | ---: | ---: | --- |\n')
for f, base in BASE.items():
    if f not in reg['per_family']: continue
    d = reg['per_family'][f]; lo, hi = rng[f]
    n += f"| {f} | {base} | {d['scripts']} | {d['stubs']} | {lo}–{hi} |\n"
n += ('\n规则：\n\n'
      '- 家族基址之间留出万位间隔，互不侵占；同一家族内按脚本名排序分配 64 对齐块。\n'
      '- **一桩一号、不复用**：脚本退役时该号标记退役，不转给新桩（避免旧档误触）。\n'
      '- 桩名可重排，号与桩的绑定以回写后的 [[事件桩映射总表]] 为准；键名不随号变。\n'
      '- hub 类不写键、入口写 `encountered_*`、route 类读 `resolve_*`——号的语义只标识事件，不改变读写规则。\n\n'
      '## 分配样例（每家族前三）\n\n| 家族 | 脚本 | 桩 | 号 |\n| --- | --- | --- | ---: |\n')
seen = collections.Counter()
for a in alloc:
    f = family(a['script'])
    if seen[f] < 3:
        seen[f] += 1
        n += f"| {f} | {a['script']} | `{a['event']}` | {a['number']} |\n"
n += ('\n完整分配见登记文件；实现时逐桩回写并保留本页作为对照。\n\n'
      '## 边界\n\n'
      '- 号段是**纸面方案**：引擎是否接受、是否与原生事件号冲突，须在实现轮实测（原生事件号空间未读取）。\n'
      '- 本页不改源码、不分配真实号、不部署；未跑过的运行项不得标"已验证"。\n\n'
      '[[事件桩映射总表]] · [[实现交接总表]] · [[试点批次总表]] · [[待办与已知缺口登记]] · [[实现侧现状核对]]\n')
put(CARD, n)
sp = (V / STUBS_PAGE).read_text(encoding='utf-8')
if '事件号分配方案' not in sp:
    sp = sp.rstrip() + '\n\n<!-- EVT-NUM-S163:BEGIN -->\n[[事件号分配方案]]：1,807 桩的家族基址＋64 对齐块预分配（一桩一号、不复用）；实现时回写本表。\n<!-- EVT-NUM-S163:END -->\n'
    put(STUBS_PAGE, sp)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S163事件号分配方案（当前登记）\n\n[[事件号分配方案]]：{len(alloc)} 桩按家族基址（N/SQ/DT/D/CS/CM/FX）＋64 对齐块确定性预分配，一桩一号不复用；引擎号实现时回写。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'evt-num-note-hashes.json'
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
rule = ('\n<!-- EVT-NUM-S163:BEGIN -->\n2026-10-13 S163：事件号分配方案。'
        '1,807桩按家族基址（N10000/SQ20000/DT30000/D40000/CS50000/CM60000/FX70000）＋脚本64对齐块确定性预分配，一桩一号不复用，退役不转号；'
        '引擎号实现时分配并回写事件桩映射总表；纸面方案，原生事件号空间未读取。'
        '入口design/11_管理/事件号分配方案.md；运行Validate-EventNumbers.py及既有检查。\n<!-- EVT-NUM-S163:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- EVT-NUM-S163:BEGIN -->.*?<!-- EVT-NUM-S163:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- EVT-NUM-S163:BEGIN -->.*?<!-- EVT-NUM-S163:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(total=len(alloc), families=len(reg['per_family']), ranges={k: v for k, v in rng.items()}), ensure_ascii=False))
