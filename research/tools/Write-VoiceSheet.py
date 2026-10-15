#!/usr/bin/env python3
"""S204 人物口吻表：收集 OPT-S200..S209 块与 DT 开场白中的说话人，
挂接人物卡的「口吻」字段与 research/character-voice-notes.json 中的要点，
渲染 design/04_人物/人物口吻表.md 与 research/character-voice.json。"""
import json, re, glob, os, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
BLOCK = re.compile(r'<!-- OPT-S20[0-9]:BEGIN -->(.*?)<!-- OPT-S20[0-9]:END -->', re.S)
LINE = re.compile(r'\*\*[A-Za-z0-9\-]+｜([^*\n]{1,16})\*\*')
NOT_PERSON = {'玩家'}

def cards():
    out = {}
    for p in sorted(glob.glob('design/04_人物/**/人物_*.md', recursive=True)):
        stem = os.path.basename(p)[3:-3]
        name = stem.split('_')[-1]
        t = open(p, encoding='utf-8').read()
        m = re.search(r'\*\*口吻\*\*[：:]\s*(.+)', t)
        rec = {'card': stem, 'voice_card': m.group(1).strip() if m else ''}
        for n in {name, stem, name.split('·')[0]} | set(name.split('与')):
            out.setdefault(n, rec)
    return out

def collect():
    use = collections.defaultdict(lambda: {'lines': 0, 'files': set()})
    for p in sorted(glob.glob('design/**/*.md', recursive=True)):
        t = open(p, encoding='utf-8').read()
        for b in BLOCK.findall(t):
            for s in LINE.findall(b):
                s = s.strip()
                use[s]['lines'] += 1
                use[s]['files'].add(os.path.basename(p)[:-3])
    for q in json.load(open('research/story-daily.json', encoding='utf-8')):
        s = q['speaker'].strip()
        use[s]['lines'] += 1
        use[s]['files'].add(f"台本_{q['id']}_{q['name']}")
    return use

def main():
    cd = cards()
    notes_p = 'research/character-voice-notes.json'
    notes = json.load(open(notes_p, encoding='utf-8')) if os.path.exists(notes_p) else {}
    rows = []
    for s, u in sorted(collect().items(), key=lambda kv: (-kv[1]['lines'], kv[0])):
        if s in NOT_PERSON:
            continue
        c = cd.get(s, {})
        n = notes.get(s, {})
        rows.append({'speaker': s, 'card': c.get('card', ''), 'lines': u['lines'],
                     'files': sorted(u['files']), 'voice_card': c.get('voice_card', ''),
                     'traits': n.get('traits', []), 'avoid': n.get('avoid', '')})
    data = {'date': '2026-10-15', 'stage': 'S204',
            'scope': 'OPT-S200..S209 块与 DT01—DT16 开场白中的说话人；口吻要点供通读与后续改写对照，不是文学验收',
            'speakers': len(rows), 'with_card': sum(1 for r in rows if r['card']),
            'with_traits': sum(1 for r in rows if r['traits']), 'rows': rows}
    with open('research/character-voice.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write('\n')
    L = ['---', 'title: "人物口吻表"', 'id: VOICE-S204', 'type: reference', 'status: draft',
         'canon: mod-original', 'baseline: "0.9.4.25-modbranch"', 'updated: 2026-10-15', 'tags: [stoneshard, dialogue, voice, S204]', 'aliases: []', '---', '',
         '# 人物口吻表', '',
         f"S204 建立。覆盖 S200—S203 新增块（OPT 块）和 DT01—DT16 开场白里的全部具名或类型说话人，共 {data['speakers']} 个；其中 {data['with_card']} 个有人物卡，{data['with_traits']} 个写了口吻要点。",
         '后续改写对白时按本表核对：同一人前后口吻一致，不同人之间要能听出区别。要点不替代人物卡；有冲突时以人物卡为准，并回来修正本表。数据源：`research/character-voice-notes.json`（要点）、人物卡「口吻」字段；生成器 `research/tools/Write-VoiceSheet.py`。', '',
         '| 说话人 | 人物卡 | 句数 | 口吻要点 | 避免 | 卡上口吻 |', '|---|---|---|---|---|---|']
    esc = lambda x: x.replace('|', '／').replace('\n', ' ')
    for r in rows:
        card = f"[[人物_{r['card']}]]" if r['card'] else '—'
        L.append(f"| {esc(r['speaker'])} | {card} | {r['lines']} | {esc('；'.join(r['traits'])) or '—'} | {esc(r['avoid']) or '—'} | {esc(r['voice_card']) or '—'} |")
    L += ['', '出处：[[人物与动机]] · [[人物弧光与关系转折]] · [[对白去重与独特性核对]]', '']
    with open('design/04_人物/人物口吻表.md', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(L))
    print(json.dumps({k: data[k] for k in ('speakers', 'with_card', 'with_traits')}, ensure_ascii=False))
main()
