"""Attach S89 fine-detail blocks onto each person card, create the four missing
story-cast cards, and reconcile note-hash manifests. Design vault only."""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FINE-DETAILS-CARD-S91'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
npcs = read('research/npc-fine-details.json')['npcs']
by_id = {}
for p in sorted(V.rglob('*.md')):
    t = p.read_text(encoding='utf-8-sig')
    m = re.search(r'^id:\s*(\S+)', t, re.M)
    if m and m.group(1) not in by_id: by_id[m.group(1)] = p.relative_to(V).as_posix()
def block(a, z, t, b):
    n = a + '\n' + b.rstrip() + '\n' + z
    return re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + n + '\n'
def fields(x):
    return (f"**体貌**：{x['look_cn']}\n\n**衣着与磨损**：{x['wear_cn']}\n\n**随身物**：{x['carry_cn']}\n\n"
            f"**举止**：{x['manner_cn']}\n\n**风格守卫**：{x['avoid_cn']}")
# ---- four missing story-cast cards ----
NEW = {
 'NPC-N-ENA': dict(name='艾娜', tags='stoneshard, character, N-series', work='灰堤工人纳拉的妻子（N2—N4；与MAE-S03的艾娜分人）。',
   arc='想停止追索、拿到工伤和欠薪，眼前先得吃饭，因此可能接受没有尸体的死亡登记；借名领过补助的旧错要留着。看到丈夫活着先问能否吃住，不要求他替赔付公开住址。',
   links=['台本_N2_灰堤没有墓碑', '台本_N3_听审前的灯', '台本_N4_第一张空白债票', '台本_N18_誓约之后']),
 'NPC-N-NARA': dict(name='纳拉', tags='stoneshard, character, N-series', work='事故中伤腿的绞盘维修工（N2—N3）。',
   arc='活着不返营是怕被重新按在绞盘上。活着的选择与死后的记录分开，不写成超自然复活；他的行踪不由旁人代为公开。',
   links=['台本_N2_灰堤没有墓碑', '台本_N3_听审前的灯']),
 'NPC-N-NELL': dict(name='妮尔', tags='stoneshard, character, N-series', work='原创地方劳务书记（N3—N4；与原作尼尔不是同一人）。',
   arc='改过栏目，承认时要说清哪一天、哪一栏；保护她不等于免责，也不写成幕后主使。',
   links=['台本_N3_听审前的灯', '台本_N4_第一张空白债票']),
 'NPC-N-SEL': dict(name='塞尔', tags='stoneshard, character, N-series', work='工坊债票相关的地方经手人（N4）。',
   arc='卖炉与工人去向必须分开算；被问大炉时沉默一瞬，不写成冷血债主。',
   links=['台本_N4_第一张空白债票']),
}
DUAL = {'NPC-N-MARA': 'CHAR-N1', 'NPC-N-IVO': 'CHAR-N1'}
changed = set(); created = []
for x in npcs:
    if x['id'] in DUAL:
        rel = by_id.get('CHAR-N1'); assert rel, x['id'] + ' dual card'
        continue
    rel = by_id.get('CITY-NPC-' + x['id']) or by_id.get(x['id'])
    if rel: continue
    spec = NEW[x['id']]; rel = f"04_人物/人物_{spec['name']}.md"
    body = (f"---\ntitle: \"人物_{spec['name']}\"\nid: {x['id']}\ntype: character\nstatus: draft\ncanon: mod-original\n"
            f"baseline: \"0.9.4.25-modbranch\"\nupdated: 2026-10-13\ntags: [{spec['tags']}]\naliases: []\n---\n\n# 人物_{spec['name']}\n\n"
            f"**工作**：{spec['work']}\n\n**处境与转折**：{spec['arc']}\n\n关联台本：" + ' · '.join('[[' + l + ']]' for l in spec['links']) + "\n\n"
            "此卡概括弧线；实际台词、路线代价与去留见篇章台本。只有亲历、本人授权或有限回执可解锁回应，不能用同一城的传闻补齐；缺席仅用事前有效有限陈述。\n\n"
            "[[人物弧光与关系转折]] · [[任务台本总索引]] · [[台本新增人物与知识边界]]\n")
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(body, encoding='utf-8')
    by_id[x['id']] = rel; created.append(rel); changed.add('design/' + rel)
# ---- blocks ----
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
dual = [x for x in npcs if x['id'] in DUAL]
def attach(rel, text):
    p = V / rel; t = p.read_text(encoding='utf-8-sig'); n = block(a, z, t, text)
    if n != t: p.write_text(preserve_foreign(V, rel, n), encoding='utf-8'); changed.add('design/' + rel)
head = '## 形象细描（S89登记）\n\n'
tail = '\n\n登记口径见[[人物细描与随身物]]；体貌与衣着为设计口径，不替代美术终稿与角色存档。'
for x in npcs:
    if x['id'] in DUAL: continue
    rel = by_id.get('CITY-NPC-' + x['id']) or by_id.get(x['id']); assert rel, x['id']
    attach(rel, head + fields(x) + tail)
if dual:
    rel = by_id.get('CHAR-N1'); assert rel
    body = head
    for x in dual:
        body += f"**{x['name']}**（`{x['id']}`）\n\n" + fields(x) + '\n\n'
    attach(rel, body.rstrip() + tail)
# ---- manifests ----
own = ROOT / 'research/fine-details-card-note-hashes.json'
manifest = json.loads(own.read_text(encoding='utf-8')) if own.exists() else {}
for x in npcs:
    rel = by_id.get(DUAL.get(x['id'], '')) or by_id.get('CITY-NPC-' + x['id']) or by_id.get(x['id'])
    assert rel, x['id']
    manifest['design/' + rel] = sha(V / rel)
own.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in manifest and h[rel] != manifest[rel]: h[rel] = manifest[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- FINE-DETAILS-S91:BEGIN -->\n2026-10-13 S91：S89的172名人物细描已回灌各自人物卡（块标记FINE-DETAILS-CARD-S91，含体貌/衣着/随身/举止/风格守卫）；补建艾娜、纳拉、妮尔、塞尔四张主线配角卡，玛拉与伊沃共卡双块。十个整篇重写人物卡的生成器已接入NotePreserve保留外部登记块；Attach-FineDetails.py维护research/fine-details-card-note-hashes.json并回写各哈希清单。入口design/04_人物/人物细描与随身物.md；风格描述不替代美术终稿与运行验证。\n<!-- FINE-DETAILS-S91:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- FINE-DETAILS-S91:BEGIN -->.*?<!-- FINE-DETAILS-S91:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- FINE-DETAILS-S91:BEGIN -->.*?<!-- FINE-DETAILS-S91:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/04_人物/人物细描与随身物.md', '入口 [人物细描与随身物](design/04_人物/人物细描与随身物.md)'), encoding='utf-8')
print(json.dumps(dict(npcs=len(npcs), cards_touched=len(changed), created=created), ensure_ascii=False))
