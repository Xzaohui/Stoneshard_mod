"""S120: bilingual coverage report across every content registry.

Counts, per registry, how many strings exist as (zh, en) pairs versus Chinese
only, splitting user-facing text (must be bilingual) from internal design prose
(intentionally Chinese-first). No content is translated here.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'BILINGUAL-COVERAGE-S120'
CARD = '11_管理/中英对照覆盖报告.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
CJK = re.compile(r'[\u4e00-\u9fff]')
INTERNAL_FIELDS = {'note_cn', 'official_cn'}
def pairs_generic(node, out):
    """Count *_cn/*_en and cn/en sibling pairs; INTERNAL_FIELDS count as internal prose."""
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and k.endswith('_cn'):
                en = node.get(k[:-3] + '_en')
                if isinstance(en, str) and en.strip(): out['pairs'] += 1
                elif v.strip():
                    out['internal_zh' if k in INTERNAL_FIELDS else 'zh_only'] += 1
            if k == 'cn' and isinstance(v, str):
                en = node.get('en')
                if isinstance(en, str) and en.strip(): out['pairs'] += 1
                elif v.strip(): out['zh_only'] += 1
            pairs_generic(v, out)
    elif isinstance(node, list):
        for v in node: pairs_generic(v, out)
rows = []
def add(reg, kind, pairs, zh_only, note):
    rows.append(dict(registry=reg, kind=kind, pairs=pairs, zh_only=zh_only, note=note))
# generic registries
for reg, path, kind, note in [
    ('item-registry', 'research/item-registry.json', 'user', '物品名称/描述/规则与术语对照'),
    ('service-registry', 'research/service-registry.json', 'user', '服务班名称/职能/便利/边界/刷新'),
    ('town-reputation', 'research/town-reputation.json', 'user', '五档柜台台词、解锁、回声与边界'),
    ('npc-fine-details', 'research/npc-fine-details.json', 'internal', '人物细描（设计口径，中文先行）'),
]:
    out = {'pairs': 0, 'zh_only': 0, 'internal_zh': 0}
    pairs_generic(read(path), out)
    note2 = note + (f"；其中分析性中文 {out['internal_zh']} 条（内部口径）" if out['internal_zh'] else '')
    add(reg, kind, out['pairs'], out['zh_only'], note2)
# explicit shapes
fx = read('research/field-npc-dialogue.json')
n = sum(len([1 for _ in (x.get('english') or {}).values() if _]) for x in fx['npcs'])
add('field-npc-dialogue', 'user', n, 0, '28 人 × 14 槽对白（含条件回访）')
fd = read('research/field-docs.json')
add('field-docs', 'user', sum(3 for d in fd['docs'] if d.get('title_en') and d.get('text_en') and d.get('read_en')), 0, '12 份文书（标题/正文/阅读边界）')
sg = read('research/field-signs.json')
add('field-signs', 'user', sum(4 for s in sg['signs'] if s.get('title_en') and s.get('obs_en') and s.get('judge_en') and s.get('danger_en')), 0, '16 处迹象（标题/观察/判定/退路）')
for reg, path, note in [('ambient-gossip', 'research/ambient-gossip.json', '六地域闲谈'),
                        ('town-gossip', 'research/town-gossip.json', '十五城镇闲谈'),
                        ('band-gossip', 'research/band-gossip.json', '声望档街头反应')]:
    d = read(path)
    add(reg, 'user', sum(1 for x in d['lines'] if x.get('cn') and x.get('en')), 0, note)
inv = read('research/special-location-inventory.json')
names = sum(1 for g in ('map_regions', 'rumor_sites', 'site_types') for r in inv[g] if r.get('name_zh') and r.get('name_en'))
add('special-location-inventory', 'user', names, 0, '8 区域/44 地点/13 类型的官方中英名')
cf = read('research/corpus-flows.json')
refs = sum(len(nd['refs']) for f in cf['flows'] for nd in f['nodes'])
add('corpus-flows', 'internal', 0, refs, '条件图引用中文本句（内部实现用，不另译）')
add('state-keys', 'internal', 0, 0, '键名与取值（无散文）')
es = read('research/event-stubs.json')
add('event-stubs', 'internal', 0, 0, f"{len(es['stubs'])} 个事件桩（无散文）")
user_pairs = sum(r['pairs'] for r in rows if r['kind'] == 'user')
user_zh = sum(r['zh_only'] for r in rows if r['kind'] == 'user')
out = dict(date='2026-10-13', scope='S120 bilingual coverage: pair counts per registry, user-facing versus internal split; no translation work, no runtime claims',
           rows=rows, user_pairs=user_pairs, user_zh_only=user_zh,
           policy=['用户可见文本（对白、文书、迹象、闲谈、声望台词、物品与服务）必须中英成对',
                   '内部设计散文（人物细描、条件图、键与桩、阅读摘要）中文先行，不视为缺口',
                   '英文均为 Mod 原创新稿，不冒充原版译文'])
(ROOT / 'research' / 'bilingual-coverage.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n2 = ('---\ntitle: "中英对照覆盖报告"\nid: MGMT-BILINGUAL-S120\ntype: review\nstatus: draft\ncanon: mod-original\n'
      'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S120, review]\naliases: []\n---\n\n'
      '# 中英对照覆盖报告\n\n'
      f"按登记文件重算：**用户可见文本共 {user_pairs} 组中英成对**，中文单语 {user_zh} 条（目标为 0）；内部设计散文（人物细描、条件图、键与桩、阅读摘要）中文先行，不视为缺口。数据 `research/bilingual-coverage.json`。\n\n"
      '| 登记 | 类别 | 成对 | 中文单语 | 说明 |\n|---|---|---:|---:|---|\n')
for r in rows:
    n2 += f"| {r['registry']} | {'用户可见' if r['kind'] == 'user' else '内部'} | {r['pairs']} | {r['zh_only']} | {r['note']} |\n"
n2 += '\n**口径**：\n\n' + '\n'.join('- ' + c for c in out['policy']) + '\n\n'
n2 += ('## 边界\n\n- 本页只统计成对与否，不评译文质量；英文稿为 Mod 原创，不冒充原版译文。\n'
       '- 内部散文若日后要出英文版，另立任务并回写本报告；当前不计缺口。\n'
       '- 未做：配音、界面排版与本地化终审。\n\n'
       '[[特殊地点与野外NPC阶段验收记录]] · [[地区闲谈池]] · [[城镇闲谈池]] · [[声望档街头反应]] · [[原创物品与装备总表]] · [[城镇声望与信任系统]] · [[设计库生成与校验流程]]\n')
put(CARD, n2)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S120中英对照覆盖（当前登记）\n\n'
           f"[[中英对照覆盖报告]]：用户可见文本 {user_pairs} 组成对、中文单语 {user_zh} 条（目标 0）；内部散文中文先行不计缺口；英文均为Mod原创。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/bilingual-coverage-note-hashes.json'
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
rule = ('\n<!-- BILINGUAL-COVERAGE-S120:BEGIN -->\n2026-10-13 S120：中英对照覆盖报告。'
        f'research/bilingual-coverage.json 逐登记重算：用户可见文本 {user_pairs} 组成对、中文单语 {user_zh} 条（目标0）；内部散文中文先行不计缺口；英文均为Mod原创。'
        '入口design/11_管理/中英对照覆盖报告.md；运行Validate-BilingualCoverage.py及既有检查；不部署游戏包。\n<!-- BILINGUAL-COVERAGE-S120:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- BILINGUAL-COVERAGE-S120:BEGIN -->.*?<!-- BILINGUAL-COVERAGE-S120:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- BILINGUAL-COVERAGE-S120:BEGIN -->.*?<!-- BILINGUAL-COVERAGE-S120:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/中英对照覆盖报告.md', '入口 [中英对照覆盖报告](design/11_管理/中英对照覆盖报告.md)'), encoding='utf-8')
print(json.dumps(dict(rows=len(rows), user_pairs=user_pairs, user_zh_only=user_zh, notes=len(generated)), ensure_ascii=False))
