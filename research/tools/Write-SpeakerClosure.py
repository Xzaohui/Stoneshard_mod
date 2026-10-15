"""S138: speaker-to-card closure audit over every story script.

Classifies every line speaker as player, card-exact, card-prefix,
card-mention, allowlisted generic role/label, or unresolved; writes the
registry, renders the audit page and registers it in the plan and AGENTS.
"""
from pathlib import Path
import json, hashlib, re, collections
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'SPEAKER-CLOSURE-S138'
CARD = '11_管理/说话人与人物卡闭合核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
LINE = re.compile(r'^(?:\[\[([^\]]+)\]\]|\*\*([^*]+)\*\*|([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z·\- ]{1,11}))[：:]\s*[「“]')
allow = json.loads((ROOT / 'research/speaker-allowlist.json').read_text(encoding='utf-8'))
card_names = set()
for p in V.rglob('人物_*.md'):
    card_names.add(p.stem.split('_')[-1])
card_bodies = []
for p in V.rglob('人物_*.md'):
    card_bodies.append((p, p.read_text(encoding='utf-8')))
speakers = {}
for p in sorted(V.rglob('台本_*.md')):
    for ln in p.read_text(encoding='utf-8').splitlines():
        m = LINE.match(ln.strip())
        if not m:
            continue
        raw = (m.group(1) or m.group(2) or m.group(3)).strip()
        form = 'link' if m.group(1) else ('bold' if m.group(2) else 'plain')
        s = raw.split('｜')[-1].strip().strip('[]').strip()
        if s.startswith('人物_'):
            s = s.split('_')[-1]
        d = speakers.setdefault(s, dict(lines=0, forms=set(), files=set()))
        d['lines'] += 1; d['forms'].add(form); d['files'].add(p.stem)
def classify(s):
    if s in allow['player']:
        return 'player', ''
    if s in card_names:
        return 'card-exact', s
    for c in sorted(card_names):
        if c.startswith(s + '·') or c.startswith(s):
            return 'card-prefix', c
    if s in allow['generic_roles']:
        return 'generic', ''
    if s in allow['labels']:
        return 'label', ''
    for p, body in card_bodies:
        if s in body:
            return 'card-mention', p.stem.split('_')[-1]
    return 'unresolved', ''
rows = []
for s, d in sorted(speakers.items()):
    cls, target = classify(s)
    rows.append(dict(speaker=s, lines=d['lines'], forms=sorted(d['forms']), files=sorted(d['files']),
                     cls=cls, target=target))
classes = collections.Counter(r['cls'] for r in rows)
unresolved = [r['speaker'] for r in rows if r['cls'] == 'unresolved']
used_generic = {r['speaker'] for r in rows if r['cls'] == 'generic'}
used_label = {r['speaker'] for r in rows if r['cls'] == 'label'}
out = dict(date='2026-10-13',
           scope='S138 speaker closure: every line speaker classified as player, card (exact/prefix/mention) or allowlisted generic/label; structure only',
           rows=rows, classes=dict(classes), unresolved=unresolved,
           unused_generic=sorted(set(allow['generic_roles']) - used_generic),
           unused_labels=sorted(set(allow['labels']) - used_label))
(ROOT / 'research/speaker-closure.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "说话人与人物卡闭合核对"\nid: MGMT-SPEAKER-CLOSURE-S138\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S138, review, dialogue]\naliases: []\n---\n\n'
     '# 说话人与人物卡闭合核对\n\n'
     f"对全部台本逐行取说话人（{len(rows)} 位、{sum(r['lines'] for r in rows)} 行），逐个归类：**玩家**、**人物卡**（精确／前缀如「塞娜」→「塞娜·里德」／人物注中的指名提及）、**通用称谓**、**标记与旁注**。"
     '凡不能归入前四类的即未闭合。登记 `research/speaker-closure.json`，白名单 `research/speaker-allowlist.json`，工具 `research/tools/Write-SpeakerClosure.py`。\n\n'
     '## 归类结果\n\n| 类别 | 位数 |\n| --- | --- |\n')
for k in ('player', 'card-exact', 'card-prefix', 'card-mention', 'generic', 'label', 'unresolved'):
    n += f"| {k} | {classes.get(k, 0)} |\n"
n += f"| **合计** | **{len(rows)}** |\n\n"
n += ('## 落到人物卡的说话人\n\n| 说话人 | 行 | 形式 | 落点 |\n| --- | --- | --- | --- |\n')
for r in rows:
    if r['cls'].startswith('card-'):
        n += f"| {r['speaker']} | {r['lines']} | {'/'.join(r['forms'])} | {r['cls']}:{r['target']} |\n"
n += '\n## 通用称谓与标记（不建人物卡）\n\n| 类别 | 称谓 |\n| --- | --- |\n'
n += '| 通用称谓 | ' + '、'.join(sorted(used_generic)) + ' |\n'
n += '| 标记与旁注 | ' + '、'.join(sorted(used_label)) + ' |\n'
n += ('\n这些称谓在不同脚本可由不同个体说出（如看守、护理者、记录员），或本就是时点标记、旁注与物件文本（如早到／晚到、检修铭牌）；'
      '它们不承担人物弧光，故只登记不建卡。\n\n'
      f"## 未闭合\n\n{'未发现未闭合说话人。' if not unresolved else '未闭合：' + '、'.join(unresolved)}\n\n"
      '## 边界\n\n'
      '- 只按行首说话人标记归类；`**早到**：「…」` 这类时点标记借说话人位承载说明，按标记处理。\n'
      '- 前缀与提及命中只证明名字在人物注中出现，不证明该人物已有完整卡或弧光。\n'
      '- 新增脚本出现未列入白名单的说话人时，闭合校验会报错，须先归类再合入。\n\n'
      '[[逐角色稿完成度核对]] · [[叙事内容清单]] · [[任务台本总索引]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f'\n## S138说话人闭合（当前登记）\n\n[[说话人与人物卡闭合核对]]：{len(rows)} 位说话人全部归类——玩家、人物卡（精确/前缀/提及）、通用称谓与标记；'
       f"未闭合 {len(unresolved)} 位。白名单见 `research/speaker-allowlist.json`，新增说话人须先归类。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = ROOT / 'research/speaker-closure-note-hashes.json'
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
rule = ('\n<!-- SPEAKER-CLOSURE-S138:BEGIN -->\n2026-10-13 S138：说话人与人物卡闭合核对。'
        f"逐行取说话人 {len(rows)} 位全部归类（玩家/人物卡精确/前缀/提及/通用称谓/标记），未闭合 {len(unresolved)} 位；"
        '白名单research/speaker-allowlist.json（通用称谓与标记不建卡）；新增说话人未列入白名单时校验报错。'
        '入口design/11_管理/说话人与人物卡闭合核对.md；运行Validate-SpeakerClosure.py及既有检查；不部署游戏包。\n<!-- SPEAKER-CLOSURE-S138:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- SPEAKER-CLOSURE-S138:BEGIN -->.*?<!-- SPEAKER-CLOSURE-S138:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- SPEAKER-CLOSURE-S138:BEGIN -->.*?<!-- SPEAKER-CLOSURE-S138:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(speakers=len(rows), classes=dict(classes), unresolved=unresolved[:5],
                      unused_generic=out['unused_generic'][:5], unused_labels=out['unused_labels'][:5]), ensure_ascii=False))
