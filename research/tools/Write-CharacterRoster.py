#!/usr/bin/env python3
"""权威人物名册（S204）。以人物卡为主源，合并重复卡、拆分共卡、补无卡说话人，
输出 research/character-roster.json 与 design/04_人物/人物权威名册.md。
同时给出 172 / 165 / 217-218 三个旧口径的现场重算与差异解释。只读其他登记。"""
import json, re, glob, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
rd = lambda p: open(p, encoding='utf-8').read()

# 主卡 id → 统一 id（与城市人物目录里的 NPC-* 卡为同一人）
MAIN_ALIAS = {'NPC05': 'NPC-REY', 'NPC06': 'NPC-MAYA', 'NPC08': 'NPC-SENA', 'NPC10': 'NPC-HERS', 'NPC12': 'NPC-MORREN'}
VANILLA = {'NPC01', 'NPC02', 'NPC03', 'NPC-REY', 'NPC-MORREN'}  # 原作人物：维伦、葛文涅尔、工匠Darrel、雷奥、莫伦
# 共卡拆分与无卡说话人（出处：人物_玛拉与伊沃 卡、说话人与人物卡闭合核对）
SPLIT = {'CHAR-N1': [('NPC-N-MARA', '玛拉'), ('NPC-N-IVO', '伊沃')]}
NOCARD = [('NPC-N-RHEA', '蕾雅', '玛拉与伊沃', '台本_N1_无钟之夜'),
          ('NPC-N-TOR', '托雷', '玛拉与伊沃', '台本_N1_无钟之夜;台本_N3_听审前的灯'),
          ('NPC-N-AREN', '艾伦', '', '台本_N11_关隘外的交换;台本_SQ08_逃兵的家书')]
# 同名不同人：说话人闭合登记把 N11/SQ08 的逃兵艾伦归到了布林装帧修复者艾伦的卡上
NOT_THIS = {'BRY-NPC-ELEN': {'台本_N11_关隘外的交换', '台本_SQ08_逃兵的家书'}}

def city_names():
    m = {}
    for p in glob.glob('design/02_世界与地图/**/聚落_*.md', recursive=True):
        stem = os.path.basename(p)[3:-3]
        code, _, nm = stem.partition('_')
        if code and '-' not in code:
            m[code] = stem
    return m

def scripts():
    return {os.path.basename(p)[:-3]: p for p in glob.glob('design/**/台本_*.md', recursive=True)}

def main():
    cities = city_names(); sc = scripts()
    fd = {n['id']: n for n in json.load(open('research/npc-fine-details.json', encoding='utf-8'))['npcs']}
    closure = json.load(open('research/speaker-closure.json', encoding='utf-8'))['rows']
    by_target = collections.defaultdict(set)
    for r in closure:
        if r.get('target'):
            by_target[r['target']].update(r['files'])
    # 反向：哪些台本链接到某张卡
    linked = collections.defaultdict(set)
    for s, p in sc.items():
        for l in set(re.findall(r'\[\[人物_([^\]|#]+)', rd(p))):
            linked[l].add(s)
    names = collections.Counter(os.path.basename(p)[3:-3].split('_')[-1] for p in glob.glob('design/04_人物/**/人物_*.md', recursive=True))
    notes = json.load(open('research/character-roster-notes.json', encoding='utf-8'))
    persons = collections.OrderedDict()
    for p in sorted(glob.glob('design/04_人物/**/人物_*.md', recursive=True)):
        t = rd(p); stem = os.path.basename(p)[3:-3]
        sid = re.search(r'\*\*稳定ID\*\*[：:]\s*(\S+)', t) or re.search(r'^id:\s*(\S+)', t, re.M)
        pid = sid.group(1).replace('CITY-NPC-', '')
        pid = MAIN_ALIAS.get(pid, pid)
        name = stem.split('_')[-1]
        sub = p.split('/')[2]
        if sub == '野外人物': typ = '野外'
        elif sub in ('城市人物', '聚落人物') and not pid.startswith('NPC-'): typ = '次要'
        else: typ = '主要'
        fac = ''
        m = re.search(r'组织关联[：:]\s*\[\[势力_([^\]|]+)', t) or re.search(r'\[\[势力_([^\]|]+)', t)
        if m: fac = m.group(1)
        loc = ''
        m = re.search(r'居住\s*\[\[(聚落_[^\]|]+)', t) or re.search(r'所属\s*\[\[(聚落_[^\]|]+)', t) or re.search(r'\[\[(区域_[^\]|]+)', t)
        if m: loc = m.group(1)
        elif re.match(r'[A-Z]{3}-', pid) and pid[:3] in cities: loc = cities[pid[:3]]
        apps = {x for x in re.findall(r'\[\[(台本_[^\]|#]+)', t) if x in sc}
        apps |= by_target.get(stem, set()) | linked.get(stem, set())
        if names[name] == 1:
            apps |= by_target.get(name, set())
        apps -= NOT_THIS.get(pid, set())
        canon = 'vanilla' if pid in VANILLA else 'mod-original'
        targets = SPLIT.get(pid, [(pid, name)])
        for tid, tname in targets:
            e = persons.get(tid)
            if e is None:
                e = persons[tid] = {'id': tid, 'name': tname, 'canon': canon, 'type': typ, 'faction': fac,
                                    'location': loc, 'appearances': set(), 'cards': [], 'fine_details': tid in fd,
                                    'note': ''}
            e['cards'].append(p)
            e['appearances'] |= apps
            if typ == '主要': e['type'] = '主要'
            e['faction'] = e['faction'] or fac
            e['location'] = e['location'] or loc
            if pid in SPLIT: e['note'] = '与另一人共用一张卡（人物_玛拉与伊沃）'
            nt = notes.get(tid, {})
            if nt.get('faction') and nt['faction'] != '无': e['faction'] = nt['faction']
            if nt.get('location') and not e['location']: e['location'] = nt['location']
    for tid, nm, card, apps in NOCARD:
        persons[tid] = {'id': tid, 'name': nm, 'canon': 'mod-original', 'type': '主要', 'faction': '',
                        'location': '', 'appearances': set(apps.split(';')), 'cards': [], 'fine_details': tid in fd,
                        'note': (f'无独立人物卡，只在 [[人物_{card}]] 中提及' if card else '无人物卡；与布林的艾伦（BRY-NPC-ELEN）同名不同人，说话人闭合登记误挂到后者'),
                        'faction': notes.get(tid, {}).get('faction', ''), 'location': notes.get(tid, {}).get('location', '')}
    notes_all = set(os.path.basename(x)[:-3] for x in glob.glob('design/**/*.md', recursive=True))
    for e in persons.values():
        if e['location'] and e['location'] not in notes_all:
            fix = '聚落_' + e['location']
            e['location'] = fix if fix in notes_all else ''
        e['appearances'] = sorted(e['appearances'])
        e['has_card'] = bool(e['cards'])
        if len(e['cards']) > 1 and not e['note']:
            e['note'] = '主卡与城市人物卡为同一人，两卡并存'
    rows = list(persons.values())
    order = {'主要': 0, '次要': 1, '野外': 2}
    rows.sort(key=lambda e: (order[e['type']], -len(e['appearances']), e['id']))
    for i, e in enumerate(rows, 1): e['no'] = i
    # 旧口径重算
    cards218 = len(glob.glob('design/04_人物/**/人物_*.md', recursive=True))
    md_all = len(glob.glob('design/04_人物/**/*.md', recursive=True))
    cast = json.load(open('research/cast-roster-validation.json', encoding='utf-8'))
    recon = {
        'fine_details_172': {'value': len(fd), 'source': 'research/npc-fine-details.json',
            'scope': 'S89 细描名单：只收 Mod 原创 NPC（城市新增演员、各城已有演员、布林续篇演员、卫星住户、6 名主线原创）；不含原作人物、不含 36 名野外人物，也不含 S200 新增的坎沃'},
        'cast_roster_165': {'value': cast['city_actors'] + cast['continuation_actors'], 'source': 'research/cast-roster-validation.json（city_actors + continuation_actors）',
            'scope': '城市演员名单：15 城城市稿里的演员 158 人 + 布林续篇演员 7 人；不含主线核心、聚落住户与野外人物'},
        'card_files_218': {'value': cards218, 'source': 'design/04_人物/**/人物_*.md',
            'scope': '人物卡文件数，不是人数：5 名主线人物各有主卡和城市人物卡两张，玛拉与伊沃共用一张卡；另有 5 篇非人物卡总表（本名册加入后）使目录 md 总数为 ' + str(md_all)},
        'roster': {'value': len(rows), 'formula': f'{cards218} 张卡 − 5 张重复卡 + 1（共卡拆成两人） + {len(NOCARD)} 名无卡说话人'},
    }
    data = {'date': '2026-10-15', 'stage': 'S204', 'scope': '权威人物名册：每个唯一身份一行；类型 主要/次要/野外；出场台本来自人物卡链接、台本对卡的链接与说话人闭合登记。不是美术或运行验收。',
            'count': len(rows), 'by_type': dict(collections.Counter(e['type'] for e in rows)),
            'by_canon': dict(collections.Counter(e['canon'] for e in rows)),
            'without_card': [e['id'] for e in rows if not e['has_card']], 'reconcile': recon, 'persons': rows}
    with open('research/character-roster.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
    esc = lambda x: str(x).replace('|', '／')
    L = ['---', 'title: "人物权威名册"', 'id: ROSTER-S204', 'type: reference', 'status: draft', 'canon: mixed',
         'baseline: "0.9.4.25-modbranch"', 'updated: 2026-10-15', 'tags: [stoneshard, character, roster, S204]', 'aliases: []', '---', '',
         '# 人物权威名册', '',
         f"截至 S204，共 **{len(rows)}** 人：" + '、'.join(f'{k} {v}' for k, v in data['by_type'].items()) + f"；原作人物 {data['by_canon'].get('vanilla', 0)}，Mod 原创 {data['by_canon'].get('mod-original', 0)}。数据：`research/character-roster.json`；生成器：`research/tools/Write-CharacterRoster.py`。绘图请以本表的编号和 ID 为准。", '',
         '## 三个旧数字的口径', '',
         '| 数字 | 来源 | 口径 |', '|---|---|---|']
    for k in ('fine_details_172', 'cast_roster_165', 'card_files_218'):
        r = recon[k]; L.append(f"| {r['value']} | {esc(r['source'])} | {esc(r['scope'])} |")
    L += [f"| {len(rows)} | 本名册 | {recon['roster']['formula']} |", '',
          '三者都不是“全部人物”：172 只算 Mod 原创细描对象，165 只算城市演员，218 是文件数。本名册按唯一身份去重。', '',
          '## 名册', '', '| 编号 | 名称 | ID | 类型 | 所属势力 | 地点 | 出场台本 | 人物卡 | 备注 |', '|---|---|---|---|---|---|---|---|---|']
    for e in rows:
        cards = ' '.join(f"[[{os.path.basename(c)[:-3]}]]" for c in e['cards']) or '无'
        apps = '、'.join(f'[[{a}]]' for a in e['appearances']) or '—'
        nm = e['name'] + ('（原作）' if e['canon'] == 'vanilla' else '')
        loc = f"[[{e['location']}]]" if e['location'] else '—'
        fac = (f"[[势力_{e['faction']}]]" if e['faction'] and e['faction'] != '无' else (e['faction'] or '—'))
        L.append(f"| {e['no']} | {esc(nm)} | {e['id']} | {e['type']} | {fac} | {loc} | {apps} | {cards} | {esc(e['note']) or ''} |")
    L += ['', '出处：[[人物细描与随身物]] · [[说话人与人物卡闭合核对]] · [[人物口吻表]]', '']
    with open('design/04_人物/人物权威名册.md', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(L))
    print(json.dumps({'count': len(rows), 'by_type': data['by_type'], 'by_canon': data['by_canon'], 'without_card': data['without_card'],
                      'no_app': sum(1 for e in rows if not e['appearances']), 'no_fac': sum(1 for e in rows if not e['faction']),
                      'no_loc': sum(1 for e in rows if not e['location'])}, ensure_ascii=False))
main()
