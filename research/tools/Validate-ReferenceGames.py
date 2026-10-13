"""Validate the reference-game comparison page (S172).

Checks that the page still covers every game the user named, that each game has
mechanism rows plus a lesson, that the takeaway table maps to our pages, that
citations are URLs and that the page keeps its external-research boundaries.
"""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
page = V / '11_管理/参考游戏叙事与声望机制对照.md'
text = page.read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
GAMES = {'博德之门3': 'BG3', '神界原罪1': 'DOS1', '神界原罪2': 'DOS2', 'Drova': 'Drova'}
for game in GAMES:
    check(game in text, 'game-named-' + game)
# mechanism rows per game
rows = [l for l in text.splitlines() if l.startswith('|') and l.count('|') >= 6]
for game in GAMES:
    check(any(l.startswith(f'| {game}') for l in rows), 'mechanism-row-' + game)
# lesson paragraph per game
for game in GAMES:
    m = re.search(r'\*\*' + re.escape(game) + r'[^*]*\*\*', text)
    check(m is not None, 'lesson-head-' + game)
    if m:
        seg = text[m.start(): m.start() + 1200]
        check('教训：' in seg, 'lesson-takeaway-' + game)
check('教训：' in text and text.count('教训：') >= 4, 'four-takeaways')
# takeaway mapping table with links to our pages
mapseg = text.split('## 本Mod的取舍映射', 1)
check(len(mapseg) == 2, 'mapping-section')
if len(mapseg) == 2:
    mapping = mapseg[1]
    mrows = [l for l in mapping.splitlines() if l.startswith('|') and '---' not in l]
    check(len(mrows) >= 6, 'mapping-rows')
    for ref in ('BG3', 'DOS1', 'DOS2', 'Drova'):
        check(ref in mapping, 'mapping-covers-' + ref)
    for lm in re.finditer(r'\[\[([^\]]+)\]\]', mapping):
        check(lm.group(1) in stems, 'mapping-link-' + lm.group(1))
# citations are URLs
urls = re.findall(r'\((https?://[^)]+)\)', text)
check(len(urls) >= 8, 'citation-count')
check(all(u.startswith('http') for u in urls), 'citations-are-urls')
# boundaries
check('机制层面' in text and '外部研究' in text, 'external-scope-stated')
check('复制品目录中没有游戏文本' in text, 'no-text-copied-stated')
check('均未验证' in text or '未验证' in text, 'unverified-stated')
check('[[城镇声望与信任系统]]' in text, 'links-design-page')
report = dict(date='2026-10-13',
              scope='S172 reference-game page: four named games covered with mechanism rows and lessons, takeaway mapping linked, citations are URLs, external boundaries kept; documentation guard only',
              games=len(GAMES), mapping_rows=len([l for l in text.split('## 本Mod的取舍映射', 1)[1].splitlines() if l.startswith('|') and '---' not in l]) if '## 本Mod的取舍映射' in text else 0,
              citations=len(urls), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'reference-games-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
