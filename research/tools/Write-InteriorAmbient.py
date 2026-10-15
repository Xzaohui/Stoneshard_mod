"""S124: author interior/daily ambient lines (9 dungeons x3, 16 dailies x2).

Dungeon lines are on-site observations tied to each dungeon premise; daily lines
are ambient remarks by the daily's own speaker role. CN/EN parity, no rewards,
no task progress; `after` lines only change future tone.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'INTERIOR-AMBIENT-S124'
CARD = '02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
dun = read('research/story-dungeon.json'); daily = read('research/story-daily.json')
DUN_LINES = {
 'D02': [('on_arrival', '水槽还在往下淌，桥面是后来搭的。', "The channel still runs; the walkway was added later."),
         ('inside', '墓龛围着干台子，活人住过的地方比死人那边整齐。', "Niche walls ring the dry platform; where the living stayed is tidier than where the dead rest."),
         ('on_exit', '检修梯通回泵房。别把唯一出口当备用。', "The service ladder leads back to the pump room. Never treat the only exit as a spare.")],
 'D03': [('on_arrival', '桥断了，税栈没断。箱子照样过秤。', "The bridge broke; the tax shed did not. Crates still get weighed."),
         ('inside', '箱号对不上脚印。混单就是这么来的。', "Crate numbers do not match the footprints. That is how one manifest swallows many."),
         ('on_exit', '桥墩下有小路。走的人多了，就不是小路。', "There is a path under the pier. Enough walkers and it stops being a path.")],
 'D04': [('on_arrival', '冷库先是保存点，后来才成了别的地方。', "The cold store began as a depot and only later became something else."),
         ('inside', '病历夹在粮袋和封柜之间。放的位置就是答案。', "Case notes sit between grain sacks and sealed cabinets. Where they sit is the answer."),
         ('on_exit', '门口的人只放你一次。下次得重新说。', "The man at the door lets you in once. Next time you explain again.")],
 'D05': [('on_arrival', '空庭不说话。器材会。', "The empty court says nothing. The equipment does."),
         ('inside', '墨迹要问时间和出处。问不清的，先别当真相。', "Ink marks must be asked when and from where. Unanswered, they are not yet truth."),
         ('on_exit', '废弃设备不是真相机。带走的只有你核过的。', "Abandoned gear is no truth machine. Carry out only what you checked.")],
 'D06': [('on_arrival', '编号完整，所以空名才像误差。', "The numbering is complete, which is why a blank name reads as a rounding error."),
         ('inside', '授权、病例、粮袋各有去处，别放在一张单上核。', "Warrants, case notes and grain sacks each go somewhere; do not check them on one sheet."),
         ('on_exit', '地窖的整齐是给人看的。看完就上来。', "The cellar is tidy for visitors. Look, then climb back up.")],
 'D07': [('on_arrival', '管线是后建的。护理和控制不是同一套设计。', "The piping was added later. Care and control were never one design."),
         ('inside', '出口开了不等于人都好了。照护才刚开始。', "An open door is not everyone healed. Care has only started."),
         ('on_exit', '别把离开当痊愈。名单还在。', "Do not take leaving for recovering. The list remains.")],
 'D08': [('on_arrival', '高处放资料，低处放人。顺序就是优先次序。', "Records up high, people down low. The order is the priority."),
         ('inside', '水下的架子不是图书馆，是留置点。', "The submerged racks are not a library; they are a holding point."),
         ('on_exit', '井口的风比井里冷。上来先晒一晒。', "The wind at the well mouth is colder than below. Dry off first.")],
 'D09': [('on_arrival', '回声大，回声有限。别把感觉当结论。', "The echo is loud and bounded. Feeling is not a conclusion."),
         ('inside', '机械台的读数错过一次。错的那次最像奇迹。', "The bench misread once. The wrong reading looked most like a miracle."),
         ('on_exit', '能安全做到的很少。承认这一点再走。', "What can be done safely is little. Admit it, then walk out.")],
 'D10': [('on_arrival', '外环能拆，内圈能退。退路先看。', "The outer ring can be dismantled and the inner one left. Check the way back first."),
         ('inside', '装置有限，人有限。别让门替你决定。', "The device is finite and so are people. Do not let a door decide for you."),
         ('on_exit', '先安全，再谈方案。顺序反了，什么都没了。', "Safety first, then terms. Reverse the order and nothing is left.")],
}
DAILY_LINES = {
 'DT01': [('any', '车队欠桥工的工钱，旅店要交货。两头都是真账。', "The caravan owes the bridge crew and the inn owes a delivery. Both ledgers are real."),
          ('after', '粮约履行过以后，桥工的钱还没算完。', "The grain delivery was honoured; the crew's wages are still open.")],
 'DT02': [('any', '上游的菜田和营地都要水。谁都不是污染源。', "The vegetable plots and the camp both need water. Neither is the source of the trouble."),
          ('after', '水的事说开以后，桶还是各用各的。', "With the water matter aired, each still uses their own bucket.")],
 'DT03': [('any', '两家认同一枚工牌。一家要人，一家要给付。', "Two households claim one work tag. One wants the body, the other the payment."),
          ('after', '墓标立起来以后，名单还是三个人。', "The marker stands; the list still holds three names.")],
 'DT04': [('any', '地是佃农的，作物是流离者种的。', "The land belongs to an injured tenant; the crop was sown by the displaced."),
          ('after', '空地收完以后，地契和庄稼分开算。', "Once the clearing is harvested, the deed and the crop are reckoned apart.")],
 'DT05': [('any', '一批退热药，军民两边都订了。', "One batch of fever medicine, ordered by both the garrison and the town."),
          ('after', '药分完以后，单子还在两边手里。', "The medicine is split; both sides still hold their slips.")],
 'DT06': [('any', '躲的是雇主，找的人付过旅费。', "He hides from an employer; the one looking covered his fare."),
          ('after', '路标立好以后，路费和去留分开谈。', "With the signpost up, fare and whereabouts are discussed separately.")],
 'DT07': [('any', '箱主说保密，搬运的说刺激物泄漏。', "The owner calls it confidential; the handlers call it an irritant leak."),
          ('after', '箱子的事处理完，伤害记录单独留。', "The crate is settled; the harm record is kept apart.")],
 'DT08': [('any', '桥工要欠薪，赶药车的要通路。', "The bridge crew wants unpaid wages; the medicine cart wants a road."),
          ('after', '第二块板修好以后，工钱还没付清。', "The second plank is fixed; the wages are not.")],
 'DT09': [('any', '助手把乡民用法当自己发现。', "The assistant takes a village remedy for his own discovery."),
          ('after', '草指认过以后，来源和效果分开说。', "The herb is identified; source and effect are stated apart.")],
 'DT10': [('any', '守夜的想杀狼，肉商不认弃血。', "The watch wants the wolves killed; the butcher denies the dumped blood."),
          ('after', '夜岗安生以后，狼还在坡上。', "The night watch is quiet; the wolves are still on the slope.")],
 'DT11': [('any', '两柜互验记录，一方要匿名对照表。', "Two cabinets cross-check records; one side wants the anonymous table too."),
          ('after', '抄本交接过以后，对照表仍留在原柜。', "The copies changed hands; the table stayed in its cabinet.")],
 'DT12': [('any', '螺栓不是核心件，雇主说封存已完成。', "The bolt is not a core part, and the employer says sealing is done."),
          ('after', '检修做完以后，面子的事归面子。', "The maintenance is finished; face is face's own business.")],
 'DT13': [('any', '掌勺的先祷告再领饭。有人不愿被看见立场。', "The cook prays before serving. Some would rather not be seen taking a side."),
          ('after', '汤分完以后，站着的人还是站着。', "The pot is empty; those who stood aside still stand aside.")],
 'DT14': [('any', '有人用假牌找药，有人混卖假牌牟利。', "One uses a forged tag to find medicine; another sells forgeries for profit."),
          ('after', '假牌的事处理完，找药的人还得看诊。', "The forgeries are dealt with; the one seeking medicine still needs care.")],
 'DT15': [('any', '非核心排水费，被转给了不参加托管的村户。', "Non-core drainage costs were shifted onto households outside the trust."),
          ('after', '巡查做完了，维护费还得重新分。', "The inspection is done; the upkeep still has to be re-split.")],
 'DT16': [('any', '患者想停一项有副作用的照护，家属怕被说放弃。', "The patient wants one side-effect treatment stopped; the family fears being called quitters."),
          ('after', '照护方案改过以后，副作用记录留着。', "The care plan changed; the side-effect record stays.")],
}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
rows = []
dun_by = {x['id']: x for x in dun}; daily_by = {x['id']: x for x in daily}
for did, lines in DUN_LINES.items():
    assert did in dun_by and len(lines) == 3
    for when, cn, en in lines:
        rows.append(dict(id=f'IA-{did}-{when}', kind='dungeon', owner=did, when=when, cn=cn, en=en,
                         link=Path(dun_by[did]['links'][0]).stem if dun_by[did].get('links') else '任务台本总索引'))
for tid, lines in DAILY_LINES.items():
    assert tid in daily_by and len(lines) == 2
    for when, cn, en in lines:
        rows.append(dict(id=f'IA-{tid}-{when}', kind='daily', owner=tid, when=when, cn=cn, en=en,
                         link=Path(daily_by[tid]['links'][0]).stem if daily_by[tid].get('links') else '任务台本总索引'))
seen_cn, seen_en = {}, {}
for x in rows:
    assert CJK.search(x['cn']) and not re.search(r'[A-Za-z]', x['cn']), x['id']
    assert not CJK.search(x['en']) and len(x['en']) <= 170, x['id']
    assert not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + ' backstage'
    assert x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + ' dup'
    assert x['link'] in {p.stem for p in V.rglob('*.md')}, x['id'] + ' link ' + x['link']
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
out = dict(date='2026-10-13', scope='S124 interior and daily ambient: dungeon on-site observations and daily ambient remarks, CN/EN parity; no rewards, no task progress, no knowledge leaks',
           vocabulary=['on_arrival', 'inside', 'on_exit', 'any', 'after'],
           rules=['副本句只写现场观察，不替任何当事人发言，不揭未核真相',
                  '日常句只写本事件周边口气，不推进任务、不发物品',
                  'after 只改未来口气，不回滚旧结',
                  '与迹象、闲谈池不重复：同地点同事实只留一处'],
           lines=rows)
(ROOT / 'research' / 'interior-ambient.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "副本与日常氛围句"\nid: FX-INTERIOR-AMBIENT\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S124, dialogue, ambient]\naliases: []\n---\n\n'
     '# 副本与日常氛围句\n\n'
     f"九个副本各 3 条现场观察（到场/内部/离场）＋十六个日常各 2 条周边口气（any/after），共 {len(rows)} 条（中英对照）。副本句只写现场，不替当事人发言；日常句不推进任务；`after` 只改未来口气。\n\n"
     '## 副本现场（9×3）\n\n| 副本 | 相位 | 中文 | English | 关联 |\n|---|---|---|---|---|\n')
for x in rows:
    if x['kind'] != 'dungeon': continue
    n += f"| {dun_by[x['owner']]['name']}（`{x['owner']}`） | `{x['when']}` | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] |\n"
n += '\n## 日常周边（16×2）\n\n| 日常 | 条件 | 中文 | English | 关联 |\n|---|---|---|---|---|\n'
for x in rows:
    if x['kind'] != 'daily': continue
    n += f"| {daily_by[x['owner']]['name']}（`{x['owner']}`） | `{x['when']}` | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] |\n"
n += ('\n## 边界\n\n- 全部为Mod原创；副本句不揭未核真相、不指认凶手；日常句不替当事人表态。\n'
      '- 不含奖励、不推进任务、不写状态键；播放条件只读时段与 `resolve_*`。\n'
      '- 未做：触发距离、作息与配音（见[[特殊地点阶段制作与校准规程]]）。\n\n'
      '[[任务台本总索引]] · [[野外迹象与观察]] · [[地区闲谈池]] · [[城镇闲谈池]] · [[特殊地点与野外NPC阶段验收记录]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S124副本与日常氛围句（当前登记）\n\n'
           f"[[副本与日常氛围句]]：9 副本×3（到场/内部/离场现场观察）＋16 日常×2（any/after周边口气），共 {len(rows)} 条中英对照；不推进任务、不写状态键、不揭未核真相。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/interior-ambient-note-hashes.json'
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
rule = ('\n<!-- INTERIOR-AMBIENT-S124:BEGIN -->\n2026-10-13 S124：副本与日常氛围句（原创，中英对照）。'
        f'research/interior-ambient.json 9副本×3现场观察＋16日常×2周边口气共 {len(rows)} 条；不推进任务、不写状态键、不揭未核真相，after 只改未来口气。'
        '入口design/02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md；运行Validate-InteriorAmbient.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。\n<!-- INTERIOR-AMBIENT-S124:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- INTERIOR-AMBIENT-S124:BEGIN -->.*?<!-- INTERIOR-AMBIENT-S124:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- INTERIOR-AMBIENT-S124:BEGIN -->.*?<!-- INTERIOR-AMBIENT-S124:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md', '入口 [副本与日常氛围句](design/02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md)'), encoding='utf-8')
print(json.dumps(dict(lines=len(rows), dungeons=len(DUN_LINES), dailies=len(DAILY_LINES), notes=len(generated)), ensure_ascii=False))
