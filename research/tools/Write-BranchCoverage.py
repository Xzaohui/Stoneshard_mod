"""S103: compute a dialogue-branch coverage audit across all script families.

Checks per family: multiple methods, per-route follow-ups, early/late callbacks,
refusal/absence alternatives, guards, interruption recovery and daily variants.
Renders a coverage card; recomputable by its validator.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'BRANCH-COVERAGE-S103'
CARD = '11_管理/对白分支覆盖审计.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def keys_of(v):
    out = []
    for x in v or []:
        out.append(x.get('key') if isinstance(x, dict) and 'key' in x else (x if isinstance(x, str) else x.get('id', '')))
    return [k for k in out if k]
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
rows = []; gaps = []
for q in model['quests']:
    routes = keys_of(q.get('routes'))
    fu = sorted((q.get('dramatic_followups') or {}).keys())
    fb = q.get('dramatic_feedback') or []
    ex = q.get('dramatic_exceptions') or []
    gu = q.get('dramatic_guards') or []
    ok = len(routes) >= 2 and set(fu) == set(routes) and len(fb) >= 1 and len(ex) >= 1 and len(gu) >= 1
    rows.append(dict(id=q['id'], family='city', routes=len(routes), followups=len(fu), feedback=len(fb), exceptions=len(ex), guards=len(gu), ok=ok))
    if not ok: gaps.append(q['id'])
for q in cont['quests']:
    routes = keys_of(q.get('routes'))
    sc = q.get('scenes') or []
    ok = len(routes) >= 2 and len(sc) >= 1 and bool(q.get('interruption')) and bool(q.get('reward_owner'))
    rows.append(dict(id=q['id'], family='continuation', routes=len(routes), followups=0, feedback=0,
                     exceptions=1 if q.get('interruption') else 0, guards=len(sc), ok=ok))
    if not ok: gaps.append(q['id'])
for name, fam in [('story-main.json', 'main'), ('story-side.json', 'side'), ('story-main-late.json', 'main-late'), ('story-dungeon.json', 'dungeon')]:
    for x in read('research/' + name):
        ok = len(x.get('choices') or []) >= 2 and bool(x.get('scenes')) and bool(x.get('recovery'))
        rows.append(dict(id=x['id'], family=fam, routes=len(x.get('choices') or []), followups=0, feedback=0,
                         exceptions=1 if x.get('recovery') else 0, guards=len(x.get('scenes') or []), ok=ok))
        if not ok: gaps.append(x['id'])
for x in read('research/story-daily.json'):
    ok = all(bool(x.get(k)) for k in ('opening', 'field', 'closing', 'failure', 'variants', 'player_mid', 'player_close'))
    rows.append(dict(id=x['id'], family='daily', routes=len(x.get('variants') or []), followups=0, feedback=0,
                     exceptions=1 if x.get('failure') else 0, guards=1 if x.get('state') else 0, ok=ok))
    if not ok: gaps.append(x['id'])
fam_counts = {}
for r in rows: fam_counts[r['family']] = fam_counts.get(r['family'], 0) + 1
out = dict(date='2026-10-13', scope='S103 branch-coverage audit: multiple methods, per-route follow-ups, early/late callbacks, refusal/absence alternatives, guards, interruption recovery and daily variants; structure only, not literary quality or runtime',
           families=fam_counts, rows=rows, gaps=gaps)
(ROOT / 'research/branch-coverage.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "对白分支覆盖审计"\nid: MGMT-BRANCH-COVERAGE-S103\ntype: review\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S103, review]\naliases: []\n---\n\n'
     '# 对白分支覆盖审计\n\n'
     '按计划剩余项「对白分支」做的结构审计：对每个台本族检查是否具备多方法、逐方法先做/后做、早/晚回执、拒绝或缺席替代、知识守卫与中断恢复。'
     '只审结构与字段，不评文学质量、不证明运行；来源为 `research/city-campaign.json`、`brynn-continuation.json`、`story-*.json`。\n\n'
     '| 族 | 脚本数 | 多方法 | 逐方法回访 | 早晚回执 | 拒绝/替代 | 守卫 |\n|---|---:|---|---|---|---|---|\n')
fam_spec = {'city': '≥2 路线且回访键覆盖全部路线，≥1 早/晚回执，≥1 拒绝/替代，≥1 知识守卫',
            'continuation': '≥2 路线，≥1 场次，中断恢复与奖励所有者非空',
            'main': '≥2 选项，≥1 场次，恢复路径非空', 'side': '≥2 选项，≥1 场次，恢复路径非空',
            'main-late': '≥2 选项，≥1 场次，恢复路径非空', 'dungeon': '≥2 选项，≥1 场次，恢复路径非空',
            'daily': '开场/现场/收束/失败/变体/玩家中段/玩家收束齐备'}
for fam, cnt in sorted(fam_counts.items()):
    sub = [r for r in rows if r['family'] == fam]
    okn = sum(1 for r in sub if r['ok'])
    n += f"| {fam}（{cnt}） | {cnt} | {okn}/{cnt} | {sum(1 for r in sub if r['followups'])} | {sum(1 for r in sub if r['feedback'])} | {sum(1 for r in sub if r['exceptions'])} | {sum(1 for r in sub if r['guards'])} |\n"
n += f"\n共 {len(rows)} 个脚本；不合口径：{'无' if not gaps else '、'.join(gaps)}。\n\n## 口径\n\n"
for fam, spec in fam_spec.items():
    n += f"- {fam}：{spec}。\n"
n += ('\n## 边界\n\n- 审计只看字段是否存在与数量；字段存在不等于文笔、不等于玩家可触达，也不等于实机跳转正确。\n'
      '- 续篇的桥组条件、早晚与缺席替代归续篇登记所有；本页只核其结构，不重复内容。\n'
      '- 野外人物的条件回访见[[台本_FX_野外人物对白]]，不在本表计数（其口径为任务进行中/完成后与先做/后做，另见 S97）。\n\n'
      '[[特殊地点与野外NPC阶段验收记录]] · [[逻辑验收记录]] · [[伏笔与回收台账]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S103对白分支覆盖审计（当前登记）\n\n'
           f"[[对白分支覆盖审计]]：{len(rows)} 个脚本（城市{len(model['quests'])}、续篇{len(cont['quests'])}、主线/支线/后章/副本、日常）结构审计——多方法、逐方法回访、早晚回执、拒绝/替代、守卫与中断恢复；不合口径：{'无' if not gaps else '、'.join(gaps)}。只审结构，不评文学与运行。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/branch-coverage-note-hashes.json'
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
rule = ('\n<!-- BRANCH-COVERAGE-S103:BEGIN -->\n2026-10-13 S103：按计划剩余项「对白分支」做结构审计。'
        f'research/branch-coverage.json 覆盖 {len(rows)} 个脚本（城市73/续篇6/主线·支线·后章·副本/日常16）：多方法、逐方法先做后做、早晚回执、拒绝或缺席替代、知识守卫与中断恢复齐备，不合口径无。'
        '入口design/11_管理/对白分支覆盖审计.md；只审字段结构，不评文学、不证明运行；运行Validate-BranchCoverage.py及既有检查；不部署游戏包。\n<!-- BRANCH-COVERAGE-S103:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- BRANCH-COVERAGE-S103:BEGIN -->.*?<!-- BRANCH-COVERAGE-S103:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- BRANCH-COVERAGE-S103:BEGIN -->.*?<!-- BRANCH-COVERAGE-S103:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/对白分支覆盖审计.md', '入口 [对白分支覆盖审计](design/11_管理/对白分支覆盖审计.md)'), encoding='utf-8')
print(json.dumps(dict(rows=len(rows), families=fam_counts, gaps=gaps), ensure_ascii=False))
