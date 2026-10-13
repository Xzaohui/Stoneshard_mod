"""S148: machine-checkable status line on the three navigation pages.

Computes current totals from the live tree, writes the registry, and puts a
preserved block with the status line on each navigation page.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'NAV-STATUS-S148'
PAGES = ['00_导航/设计总览.md', '00_导航/任务台本总索引.md', '00_导航/城市与聚落设计总索引.md']
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
fams = {}
for p in sorted(V.rglob('台本_*.md')):
    m = re.match(r'台本_([A-Za-z0-9]+)', p.name)
    sid = m.group(1) if m else p.stem
    fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
    fams[fam] = fams.get(fam, 0) + 1
total = sum(fams.values())
city = fams.get('CS', 0) + fams.get('CM', 0)
guards = len(re.findall(r'^\| (?:结构覆盖|说话人闭合|对白去重|链接完整|占位扫描|方法数|X边闭合) ',
                        (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8'), re.M))
satellites = len(list(V.rglob('聚落_*-S*.md')))
status = (f'**导航现状（S148 机检）：台本 {total} 篇（晶石 {fams.get("N", 0) + fams.get("SQ", 0) + fams.get("DT", 0) + fams.get("D", 0)}＋'
          f'城市 {city}＋野外人物 {fams.get("FX", 0)}）、卫星聚落 {satellites} 篇、质量守卫 {guards} 项。**')
reg = dict(date='2026-10-13', scope='S148 navigation status lines: live totals recomputed and asserted on the three navigation pages',
           families=fams, total=total, city=city, satellites=satellites, guards=guards, status=status)
(ROOT / 'research/nav-status.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + '\n' + status + '\n' +
       '口径：台本按家族计（`N`/`SQ`/`DT`/`D` 为晶石线，`CS`/`CM` 为城市稿，`FX` 为野外人物对白卡）；卫星聚落按 `聚落_*-S*` 笔记数；'
       '守卫行数取 [[质量守卫总表]]。计数由 `Validate-NavStatus.py` 现场重算核对；叙事清单与逐角色稿核对见 [[叙事内容清单]]、[[逐角色稿完成度核对]]。\n' + z)
for rel in PAGES:
    t = (V / rel).read_text(encoding='utf-8-sig')
    t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
    put(rel, t2)
t = (V / PLAN).read_text(encoding='utf-8-sig')
blk2 = (a + f"\n## S148导航现状机检（当前登记）\n\n三张导航页加入机检状态行：台本 {total} 篇（晶石 {fams.get('N',0)+fams.get('SQ',0)+fams.get('DT',0)+fams.get('D',0)}＋城市 {city}＋野外 {fams.get('FX',0)}）、卫星聚落 {satellites} 篇、守卫 {guards} 项。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk2 + '\n'
put(PLAN, t2)
own = ROOT / 'research/nav-status-note-hashes.json'
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
rule = ('\n<!-- NAV-STATUS-S148:BEGIN -->\n2026-10-13 S148：三张导航页加入机检状态行。'
        f"台本{total}篇（晶石{fams.get('N',0)+fams.get('SQ',0)+fams.get('DT',0)+fams.get('D',0)}＋城市{city}＋野外{fams.get('FX',0)}）、卫星聚落{satellites}篇、质量守卫{guards}项；"
        '由 Validate-NavStatus.py 现场重算核对（家族计数、卫星笔记数、守卫行数），计数变化须重跑写手刷新。\n<!-- NAV-STATUS-S148:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- NAV-STATUS-S148:BEGIN -->.*?<!-- NAV-STATUS-S148:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- NAV-STATUS-S148:BEGIN -->.*?<!-- NAV-STATUS-S148:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(total=total, city=city, satellites=satellites, guards=guards, families=fams), ensure_ascii=False))
