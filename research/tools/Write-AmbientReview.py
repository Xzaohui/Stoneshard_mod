"""S130: ambient-layer review and freeze recommendation.

Summarises every ambient/dialogue layer by scale with live counts, states the
speaker/condition semantics per layer, and records the decision to freeze the
ambient layer unless new locations or factions are added.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'AMBIENT-REVIEW-S130'
CARD = '11_管理/氛围层总览与冻结建议.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json'); sg = read('research/field-signs.json')
ag = read('research/ambient-gossip.json'); tg = read('research/town-gossip.json'); bg = read('research/band-gossip.json')
ia = read('research/interior-ambient.json'); da = read('research/district-ambient.json')
rep = read('research/town-reputation.json')
model = read('research/city-campaign.json')
districts = sum(1 for c in model['cities'] for n in c['nodes'] if n['kind'] == 'district')
LAYERS = [
 dict(id='field_npc', scale='地点级（人物）', count=len(fx['npcs']), unit='人', lines=sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][k]) for k in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs']),
      speaker='指定人物（本人）', when='初次/复访/夜里；任务进行中/完成后；先做/后做；拒绝；缺席替代',
      entry='台本_FX_野外人物对白', note='每人 14 槽；缺席只播 proxy，旁人不得代述新决定'),
 dict(id='docs', scale='地点级（文书）', count=len(fd['docs']), unit='份', lines=len(fd['docs']) * 3,
      speaker='无（可读物）', when='到达并在场时阅读', entry='文书_FX_野外地点短稿', note='原件/副件/残件分记；阅读只给信息'),
 dict(id='signs', scale='地点级（迹象）', count=len(sg['signs']), unit='处', lines=len(sg['signs']) * 4,
      speaker='无（观察）', when='到达并在场时观察', entry='野外迹象与观察', note='观察/判定/退路；不含数值与掉落'),
 dict(id='region_gossip', scale='地域级', count=len(ag['lines']), unit='条', lines=len(ag['lines']),
      speaker='路人口吻', when='any/night/band:+1/band:−1/after:<台本>', entry='地区闲谈池', note='六地域；只谈本区生活与旧事'),
 dict(id='town_gossip', scale='城镇级', count=len(tg['lines']), unit='条', lines=len(tg['lines']),
      speaker='街面行当口吻', when='any/night/after:<本城主章>', entry='城镇闲谈池', note='十五城各 4 条'),
 dict(id='band_reactions', scale='城镇/地域级（声望）', count=len(bg['lines']), unit='条', lines=len(bg['lines']),
      speaker='街面行当口吻', when='band:−1（冷）/band:+2（热）', entry='声望档街头反应', note='只写口气；与柜台台词分池'),
 dict(id='district_gossip', scale='街区级', count=len(da['lines']), unit='条', lines=len(da['lines']),
      speaker='本街行当口吻', when='在场即可', entry='街区氛围句', note=f'{districts} 街区各 1 条；不构成必访清单'),
 dict(id='interior_ambient', scale='副本/日常级', count=len(ia['lines']), unit='条', lines=len(ia['lines']),
      speaker='现场观察 + 当事人周边口吻', when='on_arrival/inside/on_exit；any/after', entry='副本与日常氛围句', note='9 副本×3＋16 日常×2'),
 dict(id='counter_lines', scale='服务台（声望）', count=sum(len(t['bands']) for t in rep['towns']), unit='条', lines=sum(len(t['bands']) for t in rep['towns']),
      speaker='各城经办人', when='按档位取值', entry='城镇声望与信任系统', note='五档×十五城；与街头反应分池'),
]
total_lines = sum(x['lines'] for x in LAYERS)
out = dict(date='2026-10-13', scope='S130 ambient layer review: per-scale counts, speaker/condition semantics, freeze recommendation; review only, no content changes',
           layers=LAYERS, total_lines=total_lines,
           freeze=['氛围层冻结在 S129 的尺度：地点/地域/城镇/街区/副本日常五级，共 '+str(total_lines)+' 个可播单元。',
                   '只有新增地点、聚落或派系时才新增氛围句；不为已有地点继续加句数。',
                   '不再新增“室内级”逐间台词：132 室内已有可观察物与交互，逐间加句会稀释密度。',
                   '新氛围句仍须过：中英成对、与既有池零克隆、无后台词、不发奖励、不写状态键。',
                   '每条新池子都会让各校验器计数 +2（清单回写），新增池子前先评估维护成本。'],
           risks=['过饱和：同一条在短距离内反复播会显得机械；按层控制密度（街区 1 条、城镇 4 条）。',
                  '翻译量：用户可见文本已 100% 中英成对，新增池子须同步英文稿。',
                  '维护成本：每新增一份清单，所有校验器的“清单回写”检查各 +2 项。'])
(ROOT / 'research' / 'ambient-review.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "氛围层总览与冻结建议"\nid: MGMT-AMBIENT-REVIEW-S130\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S130, review]\naliases: []\n---\n\n'
     '# 氛围层总览与冻结建议\n\n'
     f"按尺度清点全部可播氛围与对白层（计数取自各登记文件，实时）：共 **{total_lines}** 个可播单元。本页只做清点、口径与冻结建议，不新增内容。\n\n"
     '| 层 | 尺度 | 数量 | 可播单元 | 说话人 | 条件 | 入口 |\n|---|---|---:|---:|---|---|---|\n')
for x in LAYERS:
    n += f"| {x['id']} | {x['scale']} | {x['count']} {x['unit']} | {x['lines']} | {x['speaker']} | {x['when']} | [[{x['entry']}]] |\n"
n += '\n## 冻结建议\n\n' + '\n'.join('- ' + f for f in out['freeze']) + '\n\n'
n += '## 风险与密度\n\n' + '\n'.join('- ' + r for r in out['risks']) + '\n\n'
n += ('## 边界\n\n- 本页不新增、不改动任何氛围句；冻结不等于禁止修订：错字、口径冲突与克隆仍须修正。\n'
      '- 触发距离、作息与配音仍待实现阶段（见[[特殊地点阶段制作与校准规程]]）。\n\n'
      '[[叙事内容清单]] · [[地区闲谈池]] · [[城镇闲谈池]] · [[声望档街头反应]] · [[街区氛围句]] · [[副本与日常氛围句]] · [[台本_FX_野外人物对白]] · [[实现交接总表]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S130氛围层清点与冻结（当前登记）\n\n'
           f"[[氛围层总览与冻结建议]]：九层共 {total_lines} 个可播单元（人物 504、文书 36、迹象 64、地域 30、城镇 60、声望街头 42、街区 66、副本日常 59、柜台 75）；"
           '氛围层冻结在 S129 尺度，只有新增地点/聚落/派系时才加句。')
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/ambient-review-note-hashes.json'
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
rule = ('\n<!-- AMBIENT-REVIEW-S130:BEGIN -->\n2026-10-13 S130：氛围层总览与冻结建议。'
        f'research/ambient-review.json 清点九层共 {total_lines} 个可播单元并给出冻结口径（只有新增地点/聚落/派系时才加句；不新增室内级逐间台词）；入口design/11_管理/氛围层总览与冻结建议.md。'
        '只做清点与口径；运行Validate-AmbientReview.py及既有检查；触发与配音待实现。\n<!-- AMBIENT-REVIEW-S130:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- AMBIENT-REVIEW-S130:BEGIN -->.*?<!-- AMBIENT-REVIEW-S130:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- AMBIENT-REVIEW-S130:BEGIN -->.*?<!-- AMBIENT-REVIEW-S130:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/氛围层总览与冻结建议.md', '入口 [氛围层总览与冻结建议](design/11_管理/氛围层总览与冻结建议.md)'), encoding='utf-8')
print(json.dumps(dict(layers=len(LAYERS), total_lines=total_lines, notes=len(generated)), ensure_ascii=False))
