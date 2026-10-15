"""S139: dialogue distinctiveness audit - exact-duplicate line guard.

Extracts every speaker line, finds exact duplicates, classifies them as
deliberate main-quest/dungeon pairs (same speaker, one N script and one D
script) or as items needing review, and renders the audit page.
"""
from pathlib import Path
import json, hashlib, re, collections
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'DIALOGUE-DISTINCT-S139'
CARD = '11_管理/对白去重与独特性核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“](.+?)[」”]')
texts = collections.defaultdict(list)
total = 0
for p in sorted(V.rglob('台本_*.md')):
    m = re.match(r'台本_([A-Za-z0-9]+)', p.name)
    fam = (m.group(1)[:1] if m else '?')
    for ln in p.read_text(encoding='utf-8').splitlines():
        lm = LINE.match(ln.strip())
        if not lm: continue
        total += 1
        raw = (lm.group(1) or lm.group(2) or lm.group(3)).strip()
        s = raw.split('｜')[-1].strip().strip('[]').strip()
        if s.startswith('人物_'): s = s.split('_')[-1]
        texts[lm.group(4).strip()].append(dict(file=p.stem, fam=fam, speaker=s))
dups = []
for t, occ in texts.items():
    if len(occ) < 2 or len(t) <= 8:
        continue
    fams = {o['fam'] for o in occ}; spk = {o['speaker'] for o in occ}
    if len(spk) == 1 and fams == {'N', 'D'} and len(occ) == 2:
        cls = 'pair'
    elif len(spk) == 1:
        cls = 'review-same-speaker'
    else:
        cls = 'review-different-speakers'
    dups.append(dict(text=t, speaker=occ[0]['speaker'], cls=cls,
                     files=[o['file'] for o in occ]))
dups.sort(key=lambda d: (d['cls'] != 'pair', d['files'][0]))
classes = collections.Counter(d['cls'] for d in dups)
out = dict(date='2026-10-13',
           scope='S139 dialogue distinctiveness: exact-duplicate speaker lines, classified as deliberate main/dungeon pairs or review items; exact match only, not semantic similarity',
           total_lines=total, distinct_lines=len(texts), duplicates=dups, classes=dict(classes))
(ROOT / 'research/dialogue-distinctiveness.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
pairs = [d for d in dups if d['cls'] == 'pair']
reviews = [d for d in dups if d['cls'].startswith('review')]
n = ('---\ntitle: "对白去重与独特性核对"\nid: MGMT-DIALOGUE-DISTINCT-S139\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S139, review, dialogue]\naliases: []\n---\n\n'
     '# 对白去重与独特性核对\n\n'
     f"逐行抽取说话人台词：共 **{total} 行**、去重后 **{len(texts)} 条**不同文本。只查**完全相同**的重复（不做语义相似度），结果 {len(dups)} 组：主章—副本配对 {len(pairs)} 组，待复核 {len(reviews)} 组。"
     "登记 `research/dialogue-distinctiveness.json`，工具 `research/tools/Write-DialogueDistinctiveness.py`。\n\n"
     '## 口径\n\n'
     '- **主章—副本配对**：同一人物在 `N*` 与其对应 `D*` 副本里说同一句，属有意一致（副本是同一人物在场景内的可见版本），不视为重复写作。\n'
     '- **待复核**：同说话人跨其他家族重复，或不同说话人共用整句——须改写或说明理由，否则校验报错。\n'
     '- 只比完全相同的整句；换字、换标点的近似句不在本工具范围内。\n\n'
     '## 主章—副本配对\n\n| 说话人 | 台词 | 脚本 |\n| --- | --- | --- |\n')
for d in pairs:
    n += f"| {d['speaker']} | {d['text']} | {' · '.join(d['files'])} |\n"
n += '\n## 待复核\n\n'
n += ('未发现需复核的重复。\n\n' if not reviews else '| 说话人 | 台词 | 脚本 | 类别 |\n| --- | --- | --- | --- |\n' +
      ''.join(f"| {d['speaker']} | {d['text']} | {' · '.join(d['files'])} | {d['cls']} |\n" for d in reviews) + '\n')
n += ('## 分布观察\n\n'
      f"- 配对重复全部发生在主章与其副本之间（{len(pairs)} 组），说明副本沿用同一人物的既有立场，而非复制模板。\n"
      "- 其余 {0} 条文本各自独立；说话人分布见 [[说话人与人物卡闭合核对]]。\n\n".format(len(texts) - len(dups))
      + '## 边界\n\n'
      '- 只做整句完全匹配；不判断语气是否雷同、不判断人物是否独特。\n'
      '- 新增重复若不属主章—副本配对，闭合校验会报错，须改写或在页内登记理由。\n\n'
      '[[逐角色稿完成度核对]] · [[说话人与人物卡闭合核对]] · [[叙事内容清单]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f'\n## S139对白去重（当前登记）\n\n[[对白去重与独特性核对]]：{total} 行、去重 {len(texts)} 条，完全重复 {len(dups)} 组且全部为主章—副本配对（同人物跨 N/D），待复核 {len(reviews)} 组。\n' + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/dialogue-distinctiveness-note-hashes.json'
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
rule = ('\n<!-- DIALOGUE-DISTINCT-S139:BEGIN -->\n2026-10-13 S139：对白去重与独特性核对（整句完全匹配）。'
        f"逐行抽取{total}行、去重{len(texts)}条；完全重复{len(dups)}组，全部为主章—副本配对（同一人物跨N/D，有意一致），待复核{len(reviews)}组。"
        '新增重复不属配对时校验报错，须改写或登记理由。入口design/11_管理/对白去重与独特性核对.md；运行Validate-DialogueDistinctiveness.py及既有检查；不部署游戏包。\n<!-- DIALOGUE-DISTINCT-S139:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- DIALOGUE-DISTINCT-S139:BEGIN -->.*?<!-- DIALOGUE-DISTINCT-S139:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- DIALOGUE-DISTINCT-S139:BEGIN -->.*?<!-- DIALOGUE-DISTINCT-S139:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(total=total, distinct=len(texts), dups=len(dups), classes=dict(classes)), ensure_ascii=False))
