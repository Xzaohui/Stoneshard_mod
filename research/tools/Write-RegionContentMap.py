"""S104: map the eight original world-map regions to Mod content and avoidance.

One mapping page: per region, its original localization locator, terrain and
life, which Mod content touches it, entry and return anchors, observables,
dangers, services (none added) and original-content avoidance.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'REGION-MAP-S104'
CARD = '02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inv = json.loads((ROOT / 'research/special-location-inventory.json').read_text(encoding='utf-8'))
REGIONS = {r['key']: r for r in inv['map_regions']}
REGNAME = {'R01': '布林外港与旧渠', 'R02': '布林东侧河口与渡口', 'R03': '曼恩边地', 'R04': '王廷关隘与边城', 'R05': '灰烬湿地与疫村', 'R06': '无名修院山地'}
REG_EN = {k: v.get('name_en', '') for k, v in REGIONS.items()}
ROWS = [
 dict(key='map_brynn', name='布林城郊', mod='R01', cards=['地点设计卡_R01_布林外港与旧渠'], people=['人物_FX-BUR_库奇', '人物_FX-SGE_瓦顿', '人物_FX-MAN_岱珥'],
      terrain='港城外围的旧渠、营地和废庄园；盐锈味重，夜里风大。',
      use='拾荒、卸货、围城遗民落脚；不登记的人走渠不走门。',
      entry='渠口石阶；安全回程认港灯，逆灯回城。', obs='旧水位线、锯断的闸栅、焦土里的锅底。',
      danger='涨潮、碎石、埋在地里的钉子。', avoid='不改原作港区商店与守卫；围城叙述不重写。'),
 dict(key='map_mannshire', name='曼郡村郊', mod='R03', cards=['地点设计卡_R03_曼恩边地'], people=['人物_FX-HNT_珥兰', '人物_FX-HNY_忒曼', '人物_FX-LOT_绥珥'],
      terrain='缓坡草场与田界石；今年有一半田没种。', use='放牧、设陷、养蜂与拾穗。',
      entry='沿田界石走，第二块界石后分岔；安全回程认看羊棚旗杆。', obs='翻起的草皮、烟熏的蜂箱、被啃的界桩。',
      danger='未撤的兽夹与陷坑、蜂群、入冬前的狼。', avoid='不替原作牧场主与猎人NPC改身份；不动官方狩猎点。'),
 dict(key='map_osbrook', name='奥斯布鲁克村郊', mod='R03', cards=['地点设计卡_R03_曼恩边地'], people=['人物_FX-HNT_珥兰'],
      terrain='麦地与三户人家的田界；收草季人多。', use='收草、拾穗、临时雇工。',
      entry='沿麦田小路；安全回程认村口水槽。', obs='晾草架、茬口、断绳。', danger='收草时械斗与误伤。',
      avoid='不改原作村长与农事任务；不新增重复委托。'),
 dict(key='map_plaguevillage', name='阿尔内姆村郊', mod='R05', cards=['地点设计卡_R05_灰烬湿地与疫村'], people=['人物_FX-PLG_蔻珥'],
      terrain='封门未拆的旧村与湿地边沿；雾天能见度低。', use='封存看管、送药、避居。',
      entry='村口上风处；安全回程认旧风车基座。', obs='门上的封条、晒过的药草捆。', danger='疫源未清、游荡者。',
      avoid='不把疫病写成可治愈奖励线；不动原作病村叙事与医护身份。'),
 dict(key='map_oldhomestead', name='老宅子', mod='R02', cards=['地点设计卡_R02_布林东侧河口与渡口'], people=['人物_FX-HOM_苇珥', '人物_FX-FRM_蓟珥'],
      terrain='河岸路旁的旧农宅与荒宅；春天路面翻浆。', use='住人、拾荒、过路歇脚。',
      entry='沿官道里程碑；安全回程认渡口摆渡棚灯。', obs='灶台旧灰、塌陷地板、烟道里的窝。', danger='地板塌陷、夜路劫道。',
      avoid='不认领原主房屋；不改官方商路走向。'),
 dict(key='map_abbey', name='修院', mod='R06', cards=['地点设计卡_R06_无名修院山地'], people=['人物_FX-ABY_缇菈', '人物_FX-HUT_珂琳', '人物_FX-CRP_瑟珥'],
      terrain='山道与修院废墟；雾从谷底上来得快。', use='避难、守墓、采药。',
      entry='沿山道石堆标记；安全回程认山道口药棚箭号。', obs='钟楼空阶、后墙豁口、晾草分层。', danger='地窖不可擅入、山雨石阶湿滑。',
      avoid='不揭原作修院与地窖内容；不动官方山道任务点。'),
 dict(key='map_rottenwillow', name='烂柳', mod='R05', cards=['地点设计卡_R05_灰烬湿地与疫村'], people=['人物_FX-WIL_摩珥'],
      terrain='据点式酒馆与周边湿地；人来人往、帮派换人。', use='喝酒、听传闻、临时交易。',
      entry='沿湿地木栈道；安全回程认旧风车基座。', obs='拴马桩、后院旧账板。', danger='赌债与帮派纠纷。',
      avoid='不替帮派收账、不改原作酒馆身份与在场人物。'),
 dict(key='map_freevalley', name='自由谷', mod='R02', cards=['地点设计卡_R02_布林东侧河口与渡口'], people=['人物_FX-RLY_珥薇'],
      terrain='谷地田庄与桥路；桥板坏一次绕半天。', use='过路、中继、歇脚。',
      entry='沿谷地土路；安全回程认中继营地旧锅。', obs='压平的草、旧灰坑、桥板茬口。', danger='旧灰坑未熄透、路面湿滑。',
      avoid='不新增第二个摆渡点；不改原作渡口与旅店人物。'),
]
assert set(r['key'] for r in ROWS) == set(REGIONS), (set(REGIONS) - set(r['key'] for r in ROWS))
stems = {p.stem for p in V.rglob('*.md')}
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
out = dict(date='2026-10-13', scope='S104 original world-map regions mapped to Mod content and avoidance; design intent only, no proportional maps or spawn points',
           regions=[dict(key=r['key'], name=r['name'], locator=REGIONS[r['key']]['index'], mod=r['mod'],
                         cards=r['cards'], people=r['people']) for r in ROWS])
(ROOT / 'research' / 'region-content-map.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
n = ('---\ntitle: "原作地图区域与Mod内容映射"\nid: SRC-REGION-MAP-S104\ntype: source\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S104, map, source]\naliases: []\n---\n\n'
     '# 原作地图区域与Mod内容映射\n\n'
     f"把[[特殊地点与野外NPC清点]]登记的 {len(ROWS)} 个世界地图区域逐一映射到 Mod 内容：地域卡、地点卡、野外人物与既有台本。"
     '本页只做映射与避让口径：不改原作村落、任务与在场人物，不新增服务；比例地图与生成点未做。\n\n'
     '| 原作区域 | STRG | English | Mod 地域 | 地点卡 | 野外人物 |\n|---|---|---|---|---|---|\n')
for r in ROWS:
    n += f"| {r['name']}（`{r['key']}`） | {REGIONS[r['key']]['index']} | {REG_EN[r['key']]} | [[区域_{r['mod']}_{REGNAME[r['mod']]}]] | [[" + ']], [['.join(r['cards']) + "]] | " + ('、'.join('[[' + p + ']]' for p in r['people']) if r['people'] else '—') + " |\n"
for r in ROWS:
    n += (f"\n## {r['name']}（`{r['key']}`）\n\n"
          f"**地貌与生活**：{r['terrain']}{r['use']}\n\n**入口与安全回程**：{r['entry']}\n\n**固定可观察物**：{r['obs']}\n\n"
          f"**特殊危险**：{r['danger']}\n\n**服务**：无固定服务；不新增柜台或奖励。\n\n**原作避让**：{r['avoid']}\n\n"
          f"**Mod 落点**：地域 [[区域_{r['mod']}_{REGNAME[r['mod']]}]]；地点卡 {'、'.join('[[' + c + ']]' for c in r['cards'])}；人物 " + ('、'.join('[[' + p + ']]' for p in r['people']) if r['people'] else '—') + "。\n")
n += ('\n## 边界\n\n- 原作区域名与 STRG 定位只读登记；Mod 不占区域、不改原作地图与任务。\n'
      '- 映射用于放置与避让：同一区域内的 Mod 内容以地点卡与人物卡为准，本页不重复其正文。\n'
      '- 未做：比例地图、生成点、区域边界实测与英文稿。\n\n'
      '[[特殊地点与野外NPC清点]] · [[特殊地点设计卡总表]] · [[台本_FX_野外人物对白]] · [[地图扩张总图]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S104原作区域映射（当前登记）\n\n'
           f"[[原作地图区域与Mod内容映射]]：8 个世界地图区域（布林城郊/曼郡村郊/奥斯布鲁克村郊/阿尔内姆村郊/老宅子/修院/烂柳/自由谷）逐一映射到 Mod 地域、地点卡与野外人物，含入口/观察/危险/服务（不新增）与原作避让；只做映射，不改原作地图与任务。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/region-map-note-hashes.json'
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
rule = ('\n<!-- REGION-MAP-S104:BEGIN -->\n2026-10-13 S104：用户要求扩充各特殊地点。'
        'research/region-content-map.json 把8个原作世界地图区域映射到Mod地域/地点卡/野外人物，入口design/02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md；'
        '只做映射与避让口径：不占区域、不改原作地图与任务、不新增服务；比例与生成点仍待做。运行Validate-RegionContentMap.py及既有检查；不部署游戏包。\n<!-- REGION-MAP-S104:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- REGION-MAP-S104:BEGIN -->.*?<!-- REGION-MAP-S104:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- REGION-MAP-S104:BEGIN -->.*?<!-- REGION-MAP-S104:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md', '入口 [原作地图区域与Mod内容映射](design/02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md)'), encoding='utf-8')
print(json.dumps(dict(regions=len(ROWS), notes=len(generated)), ensure_ascii=False))
