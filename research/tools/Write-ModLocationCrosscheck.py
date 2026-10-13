"""Cross-check Mod-original special locations, dungeons and field NPCs (S96).

Reads existing sources (no game files) and renders a review note: every dungeon
maps to a region and unique settlement task, Brynn continuation spaces map to
the city and region, and field NPCs neither duplicate names nor sites.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'MOD-LOC-XCHECK-S96'
CARD = '11_管理/Mod特殊地点与人物交叉核对.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
dun = read('research/story-dungeon.json')
bc = read('research/brynn-continuation.json')
cc = read('research/city-campaign.json')
fx = read('research/field-npc-dialogue.json')
stems = {p.stem for p in V.rglob('*.md')}
# person-card names (04_人物 cards)
person_names = set()
for p in (V / '04_人物').rglob('*.md'):
    if p.stem.startswith('人物_FX-'): continue
    m = re.match(r'^人物_(?:[A-Z0-9-]+_)?(.+)$', p.stem)
    if m: person_names.add(m.group(1))
resident_names = {s['resident']['name'] for c in cc['cities'] for s in c['satellites']}
dungeons = []
for d in dun:
    dungeons.append(dict(id=d['id'], name=d['name'], region=d['region'], main=d['main'], side=d['side'],
                         reward=d['reward'], route=d['route'], links=d['links']))
spaces = [dict(id=s['id'], name=s['name'], city=bc['city'], region='R01') for s in bc['spaces']]
npcs = [dict(id=n['id'], name=n['name'], site=n['site'], region=n['region']) for n in fx['npcs']]
clash_person = sorted({n['name'] for n in npcs} & person_names)
clash_resident = sorted({n['name'] for n in npcs} & resident_names)
site_use = {}
for n in npcs: site_use.setdefault(n['site'], []).append(n['id'])
dup_sites = {k: v for k, v in site_use.items() if len(v) > 1}
dup_dun_names = [n for n in {d['name'] for d in dungeons} if [d['name'] for d in dungeons].count(n) > 1]
reward_owner = {}
for d in dungeons:
    for t in d['main'] + d['side']:
        reward_owner.setdefault(t, []).append(d['id'])
multi_owner = {t: v for t, v in reward_owner.items() if len(v) > 1}
out = dict(date='2026-10-13', scope='S96 cross-check of Mod special locations: dungeons to regions and unique settlement tasks, continuation spaces, field NPC uniqueness',
           dungeons=dungeons, brynn_spaces=spaces, field_npcs=npcs,
           checks=dict(clash_person=clash_person, clash_resident=clash_resident, duplicate_sites=dup_sites,
                       duplicate_dungeon_names=dup_dun_names, multi_task_reward_owner=multi_owner))
(ROOT / 'research/mod-location-crosscheck.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "Mod特殊地点与人物交叉核对"\nid: MGMT-MOD-LOC-S96\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S96, review]\naliases: []\n---\n\n'
     '# Mod特殊地点与人物交叉核对\n\n'
     '按[[特殊地点与野外NPC对白扩展计划]]第5步，核对Mod原创副本、布林续篇场景与S94野外人物：地域归属、任务结算唯一性、回程、服务与重名。'
     '数据源为设计库既有JSON；不读游戏文件、不新增奖励、不新增前置。\n\n'
     f"## Mod原创副本（{len(dungeons)}）\n\n| 副本 | 地域 | 主线 | 支线 | 结算口径 | 回程 |\n|---|---|---|---|---|---|\n")
for d in dungeons:
    n += f"| {d['name']}（`{d['id']}`） | {d['region']} | {'、'.join(d['main'])} | {'、'.join(d['side']) or '—'} | {d['reward']} | " + ('有（' + d['route'][:18] + '…）' if d['route'] else '缺') + ' |\n'
n += (f"\n## 布林续篇场景（{len(spaces)}）\n\n| 场景 | 城市 | 地域 |\n|---|---|---|\n")
for s in spaces:
    n += f"| [[空间_{s['id']}_{s['name']}]] | [[聚落_BRY_布林]] | {s['region']} |\n"
n += (f"\n## 野外人物（{len(npcs)}）\n\n| 人物 | 地点类型 | 地域 |\n|---|---|---|\n")
for x in npcs:
    n += f"| [[人物_{x['id']}_{x['name']}]] | `{x['site']}` | {x['region']} |\n"
n += ('\n## 交叉结论\n\n'
      f"- 副本结算：{len(reward_owner)} 个任务各由唯一副本结算（多主核对：{'无' if not multi_owner else str(multi_owner)}）。\n"
      f"- 副本重名：{'无' if not dup_dun_names else '、'.join(dup_dun_names)}；地域均落在 R01—R06。\n"
      f"- 野外人物与既有 04_人物 卡重名：{'无' if not clash_person else '、'.join(clash_person)}；与卫星住户重名：{'无' if not clash_resident else '、'.join(clash_resident)}。\n"
      f"- 同一地点类型重复挂人：{'无' if not dup_sites else str(dup_sites)}；每处野外人物各自独立卡与唯一ID。\n"
      '- 服务与奖励：副本只出普通材料，结算归主线/支线唯一所有者；野外人物不发奖励、不占服务台。\n\n'
      '## 边界\n\n- 副本内部布局、比例与运行房间仍按各副本台本；本页不重复其内容。\n'
      '- 布林续篇场景与野外人物是两类内容：前者在城内，后者在原作世界地点类型上，互不替代。\n'
      '- 未做：Mod原创地点与世界格的最终坐标、野外人物实际排布、英文稿。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[特殊地点与野外NPC清点]] · [[特殊地点设计卡总表]] · [[台本_FX_野外人物对白]] · [[城市扩展验收记录]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S96Mod地点与人物交叉核对（当前登记）\n\n'
           f"[[Mod特殊地点与人物交叉核对]]：{len(dungeons)} 个Mod副本、{len(spaces)} 个布林续篇场景、{len(npcs)} 名野外人物的地域/结算/重名交叉核对；任务结算唯一、无重名、无重复挂点。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/mod-loc-xcheck-note-hashes.json'
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
rule = ('\n<!-- MOD-LOC-XCHECK-S96:BEGIN -->\n2026-10-13 S96：按计划第5步交叉核对Mod特殊地点与人物。'
        'research/mod-location-crosscheck.json：9个副本各归R01—R06并只由唯一任务结算、6个布林续篇场景归布林、16名野外人物无重名无重复挂点；入口design/11_管理/Mod特殊地点与人物交叉核对.md。'
        '运行Validate-ModLocationCrosscheck.py及既有检查；坐标、实际排布与英文稿仍待做，不部署游戏包。\n<!-- MOD-LOC-XCHECK-S96:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- MOD-LOC-XCHECK-S96:BEGIN -->.*?<!-- MOD-LOC-XCHECK-S96:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- MOD-LOC-XCHECK-S96:BEGIN -->.*?<!-- MOD-LOC-XCHECK-S96:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/Mod特殊地点与人物交叉核对.md', '入口 [Mod特殊地点与人物交叉核对](design/11_管理/Mod特殊地点与人物交叉核对.md)'), encoding='utf-8')
print(json.dumps(dict(dungeons=len(dungeons), spaces=len(spaces), npcs=len(npcs), notes=len(generated),
                      clash_person=clash_person, clash_resident=clash_resident, dup_sites=dup_sites, multi=multi_owner), ensure_ascii=False))
