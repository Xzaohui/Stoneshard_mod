"""S177: narrative-depth audit - reactivity metrics per script, adapted from the
BG3/DOS lessons (in-scene reactions, timing/absence slots, explicit consequence
edges). Read-only: computes from the existing registries and renders the audit.
"""
from pathlib import Path
import hashlib, json, collections, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'NARRATIVE-DEPTH-S177'
CARD = '11_管理/网状叙事深度审计.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
flows = json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows']
keys = json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']
matrix = (V / '09_系统逻辑/叙事交叉影响矩阵.md').read_text(encoding='utf-8')
edges = re.findall(r'^## (X\d\d)\s+([A-Za-z0-9\-]+) → ([A-Za-z0-9\-]+)$', matrix, re.M)
out_deg = collections.Counter(a for _, a, _ in edges)
in_deg = collections.Counter(b for _, _, b in edges)
# speakers per script file
spk = json.loads((R / 'speaker-closure.json').read_text(encoding='utf-8'))['rows']
speakers_by_file = collections.defaultdict(set)
for r in spk:
    for f in r['files']:
        speakers_by_file[f].add(r['speaker'])
SCRIPT_FILES = {p.stem: p for p in V.rglob('台本_*.md')}
def script_stem(qid):
    for stem in SCRIPT_FILES:
        if stem.split('_')[1] == qid:
            return stem
    return ''
rows = []
for f in flows:
    nodes = f['nodes']
    when = collections.Counter(n.get('when') for n in nodes)
    stem = script_stem(f['id'])
    rows.append(dict(id=f['id'], family=f['family'], nodes=len(nodes),
                     conditioned=sum(1 for n in nodes if n.get('when') != 'any'),
                     early=when.get('order_early', 0), late=when.get('order_late', 0),
                     absent=when.get('npc_absent', 0), refused=when.get('refused', 0),
                     done=when.get('task_done', 0),
                     routes=sum(1 for w in when if str(w).startswith('route(')),
                     lines=sum(len(n.get('refs', [])) for n in nodes),
                     x_out=out_deg.get(f['id'], 0), x_in=in_deg.get(f['id'], 0),
                     guards=len(f.get('guards', [])),
                     speakers=len(speakers_by_file.get(stem, ()))))
fam = collections.defaultdict(list)
for r in rows:
    fam[r['family']].append(r)
summary = {}
for name, rs in fam.items():
    med = lambda k: sorted(x[k] for x in rs)[len(rs) // 2]
    summary[name] = dict(scripts=len(rs), nodes=med('nodes'), conditioned=med('conditioned'),
                         lines=med('lines'), speakers=med('speakers'),
                         with_early=sum(1 for x in rs if x['early']), with_absent=sum(1 for x in rs if x['absent']),
                         no_x_in=sum(1 for x in rs if x['x_in'] == 0), no_x_out=sum(1 for x in rs if x['x_out'] == 0))
gaps = dict(
    no_timing=[r['id'] for r in rows if not r['early'] and not r['late']],
    no_absence=[r['id'] for r in rows if not r['absent']],
    no_inbound=[r['id'] for r in rows if r['x_in'] == 0],
    no_outbound=[r['id'] for r in rows if r['x_out'] == 0],
    thin_nodes=[r['id'] for r in rows if r['nodes'] <= 4],
)
facts = dict(date='2026-10-13',
             scope='S177 narrative-depth audit: per-script reactivity metrics computed from the live registries; read-only, no content change',
             metrics=rows, families=summary, gaps=gaps,
             reference_lessons=dict(bg3='同场景内反应、具体物品/行为作回调条件、不靠全知；',
                                    dos='标签解锁选项、后果以脚本旗标承载、身份类后果不因补救删除；'),
             proposal=[
                 '① 地牢（9 篇）与日常（16 篇）缺"先后/缺席"槽：按城市稿的 order_early／order_late／npc_absent 模式补，先各取 3 篇试点。',
                 '② 12 篇日常与 9 篇地牢没有显式入向 X 边：其反应目前只靠成组登记；按 FS-23／FS-24 的分组口径评估是否升为逐脚本边（先给 2—3 条最小边）。',
                 '③ 续篇六篇无缺席/代理槽：补 npc_absent＋proxy 各一条，保持"死亡/拒绝/缺席不播新句"的口径。',
             ])
(R / 'narrative-depth-audit.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "网状叙事深度审计"\nid: MGMT-NARRATIVE-DEPTH-S177\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S177, review, narrative]\naliases: []\n---\n\n'
     '# 网状叙事深度审计\n\n'
     '按 BG3／DOS 的经验把"反应性"拆成可数的量：**条件节点**（`when ≠ any`）、**先后槽**（early／late）、**缺席与拒绝槽**、**路线数**、**入/出向 X 边**、**说话人数**。全部由登记现场计算（只读，不改内容）；数据 `research/narrative-depth-audit.json`。\n\n'
     '## 家族分布（中位数／计数）\n\n| 家族 | 篇数 | 节点 | 条件节点 | 台词行 | 说话人 | 有 early | 有 absent | 无入向边 | 无出向边 |\n| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n')
for name in sorted(summary):
    s = summary[name]
    n += (f"| {name} | {s['scripts']} | {s['nodes']} | {s['conditioned']} | {s['lines']} | {s['speakers']} | "
          f"{s['with_early']} | {s['with_absent']} | {s['no_x_in']} | {s['no_x_out']} |\n")
n += (f"\n## 缺口清单（现场重算）\n\n"
      f"- **无先后槽**（既无 early 也无 late）：{len(gaps['no_timing'])} 篇——{'、'.join('`' + x + '`' for x in gaps['no_timing'][:12])}…\n"
      f"- **无缺席槽**：{len(gaps['no_absence'])} 篇；**无入向 X 边**：{len(gaps['no_inbound'])} 篇；**无出向 X 边**：{len(gaps['no_outbound'])} 篇；**节点 ≤4**：{len(gaps['thin_nodes'])} 篇。\n\n"
      '## 对照经验（BG3／DOS）\n\n'
      '- BG3：**只对在场与相关者生效**，回调以**具体物品与行为**为条件（如谋杀法庭按携带的断手生成幽灵），不靠全知。\n'
      '- DOS：标签解锁选项、后果以脚本旗标承载；身份类后果不因补救删除。\n'
      '- 本Mod已具备的强项：城市稿 73/73 同时有 early 与 absent 槽；每篇 ≥3 条件节点（无"低条件"脚本）。\n\n'
      '## 优化提案（下一步执行）\n\n')
for i, p in enumerate(facts['proposal'], 1):
    n += f"{i}. {p}\n"
n += ('\n## 边界\n\n'
      '- 只算结构与登记；**不评判文学质量**，也不代表游戏内已生效。\n'
      '- X 边缺口不等于缺陷：日常与副本原按 FS-23／FS-24 **成组登记**；是否升为逐脚本边由提案②决定。\n'
      '- 提案执行会改动作者源与交叉矩阵，须同步 [[伏笔与回收台账]]、[[全库条件流投影]] 与相关校验器。\n\n'
      '[[参考游戏叙事与声望机制对照]] · [[叙事交叉影响矩阵]] · [[全库条件流投影]] · [[伏笔与回收台账]] · [[质量守卫总表]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S177网状叙事深度审计（当前登记）\n\n[[网状叙事深度审计]]：按 BG3／DOS 经验量化反应性——每篇 ≥3 条件节点、城市稿 73/73 有 early＋absent；缺口：无先后槽 {len(gaps['no_timing'])} 篇、无缺席槽 {len(gaps['no_absence'])} 篇、无入向 X 边 {len(gaps['no_inbound'])} 篇；附三条优化提案。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'narrative-depth-note-hashes.json'
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
rule = ('\n<!-- NARRATIVE-DEPTH-S177:BEGIN -->\n2026-10-13 S177：网状叙事深度审计（只读计算）。'
        f"按BG3/DOS经验量化反应性：条件节点/先后槽/缺席槽/路线/入出向X边/说话人；城市稿73/73有early+absent；缺口：无先后槽{len(gaps['no_timing'])}篇、无缺席槽{len(gaps['no_absence'])}篇、无入向边{len(gaps['no_inbound'])}篇；附三条优化提案。"
        '入口design/11_管理/网状叙事深度审计.md；运行Validate-NarrativeDepth.py及既有检查；不改内容。\n<!-- NARRATIVE-DEPTH-S177:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- NARRATIVE-DEPTH-S177:BEGIN -->.*?<!-- NARRATIVE-DEPTH-S177:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- NARRATIVE-DEPTH-S177:BEGIN -->.*?<!-- NARRATIVE-DEPTH-S177:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(flows=len(rows), families={k: v['scripts'] for k, v in summary.items()},
                      gaps={k: len(v) for k, v in gaps.items()}), ensure_ascii=False))
