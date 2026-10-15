"""Validate the S148 navigation status lines against live totals."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
reg = read('research/nav-status.json')
fams = {}
for p in sorted(V.rglob('台本_*.md')):
    m = re.match(r'台本_([A-Za-z0-9]+)', p.name)
    sid = m.group(1) if m else p.stem
    fam = re.sub(r'[-]?\d+$', '', sid).split('-')[0]
    fams[fam] = fams.get(fam, 0) + 1
total = sum(fams.values()); city = fams.get('CS', 0) + fams.get('CM', 0)
guards = len(re.findall(r'^\| (?:结构覆盖|说话人闭合|对白去重|链接完整|占位扫描|方法数|X边闭合) ',
                        (V / '11_管理/质量守卫总表.md').read_text(encoding='utf-8'), re.M))
satellites = len(list(V.rglob('聚落_*-S*.md')))
check(reg['families'] == fams, 'families-live')
check(reg['total'] == total, 'total-live')
check(reg['city'] == city, 'city-live')
check(reg['guards'] == guards, 'guards-live')
check(reg['satellites'] == satellites, 'satellites-live')
status = (f'**导航现状（S148 机检）：台本 {total} 篇（晶石 {fams.get("N",0)+fams.get("SQ",0)+fams.get("DT",0)+fams.get("D",0)}＋'
          f'城市 {city}＋野外人物 {fams.get("FX",0)}）、卫星聚落 {satellites} 篇、质量守卫 {guards} 项。**')
check(status == reg['status'], 'status-string-stable')
for rel in ('00_导航/设计总览.md', '00_导航/任务台本总索引.md', '00_导航/城市与聚落设计总索引.md'):
    t = (V / rel).read_text(encoding='utf-8')
    check('NAV-STATUS-S148:BEGIN' in t, 'block-' + rel)
    check(status in t, 'status-' + rel)
    check('[[叙事内容清单]]' in t and '[[逐角色稿完成度核对]]' in t, 'pointers-' + rel)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('NAV-STATUS-S148:BEGIN' in plan, 'plan-block')
check('NAV-STATUS-S148:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/nav-status-note-hashes.json')
check(len(h) == 4, 'own-manifest-4')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S148 navigation status: totals recomputed (families, satellites, guards), identical status line on three pages, chain; documentation only',
              total=total, city=city, satellites=satellites, guards=guards,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/nav-status-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
