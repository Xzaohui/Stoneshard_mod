"""Validate the S95 special-site design cards, coverage, links and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
inv = read('research/special-location-inventory.json')
SITE_NAME = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
SITE_EN = {r['key']: r.get('name_en', '') for r in inv['rumor_sites']}
REGIONS = [('R01', '布林外港与旧渠'), ('R02', '布林东侧河口与渡口'), ('R03', '曼恩边地'),
           ('R04', '王廷关隘与边城'), ('R05', '灰烬湿地与疫村'), ('R06', '无名修院山地')]
stems = {p.stem for p in V.rglob('*.md')}
covered = {}
for rid, name in REGIONS:
    rel = f"02_世界与地图/特殊地点与野外NPC/地点设计卡_{rid}_{name}.md"
    check((V / rel).exists(), rid + '-card-exists')
    t = (V / rel).read_text(encoding='utf-8')
    for f in ['**地貌与生活用途**', '**入口与安全回程**', '**固定可观察物**', '**特殊危险**', '**服务**', '**原作避让**', '**关联任务与人物**']:
        check(f in t, rid + '-field-' + f)
    check('## 逐地点' in t and '## 边界' in t and '[[特殊地点设计卡总表]]' in t, rid + '-structure')
    for m in re.finditer(r'^\| `(rumor_[A-Za-z0-9_]+)` ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$', t, re.M):
        key, sname, use, obs, danger, link = [x.strip() for x in m.groups()]
        check(key in SITE_NAME, rid + '-site-known-' + key)
        check(key not in covered, rid + '-site-once-' + key)
        covered[key] = rid
        check(sname.startswith(SITE_NAME.get(key, '')), rid + '-site-name-' + key)
        check(SITE_EN.get(key, '') and SITE_EN[key] in sname, rid + '-site-en-name-' + key)
        check(len(use) >= 6 and len(obs) >= 6 and len(danger) >= 6, rid + '-site-fields-' + key)
        if link != '—':
            lm = re.match(r'\[\[(.+?)\]\]', link)
            check(bool(lm) and lm.group(1) in stems, rid + '-site-link-' + key)
    for lm in re.finditer(r'\[\[([^\]]+)\]\]', t):
        check(lm.group(1) in stems, rid + '-link-resolves-' + lm.group(1))
check(set(covered) == set(SITE_NAME), 'all-44-sites-covered')
check(len(covered) == 44, 'site-count-44')
idx = (V / '02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md').read_text(encoding='utf-8')
check('# 特殊地点设计卡总表' in idx and '## 口径' in idx, 'index-structure')
for rid, name in REGIONS:
    check(f"[[地点设计卡_{rid}_{name}]]" in idx, rid + '-index-link')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('SITE-CARDS-S95:BEGIN' in plan and '[[特殊地点设计卡总表]]' in plan, 'plan-block-and-link')
check('SITE-CARDS-S95:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/site-cards-note-hashes.json')
check(len(h) == 8, 'own-manifest-8')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S95 special-site cards: 44-site coverage, per-site fields, region fields, links and manifest chain; not proportional maps, collision or runtime rooms',
              regions=len(REGIONS), sites=len(covered), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/site-cards-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
