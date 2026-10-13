"""Read-only probe of the vanilla reputation structure.

Bounded: keys, locators and <=46-character snippets only; no full text.
Sections: reputation feeds and UI labels, reputation source rows (each carries
[%rep_amount%]), tier perk descriptions and effects, local settlement states,
crime/wanted rows.
"""
from pathlib import Path
import hashlib, json, re, struct

GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
SRC = GAME / 'vanilla.win'
OUT = Path(__file__).resolve().parents[1] / 'reputation-structure-probe.json'
CJK = re.compile(r'[\u4e00-\u9fff]')
KANA = re.compile(r'[\u3040-\u30ff]')

def read_strg(path):
    b = path.read_bytes()
    i = b.find(b'STRG')
    count = struct.unpack('<I', b[i+8:i+12])[0]
    offs = [struct.unpack('<I', b[i+12+4*k:i+16+4*k])[0] for k in range(count)]
    def text(o):
        n = struct.unpack('<I', b[o:o+4])[0]
        return b[o+4:o+4+n]
    return b, count, [text(o) for o in offs]

def zh_of(parts):
    best, best_n = '', 0
    for p in parts[1:]:
        n = len(CJK.findall(p))
        if n > best_n and not KANA.search(p):
            best, best_n = p, n
    return best

def en_of(parts):
    for p in parts[1:]:
        if (len(p) >= 3 and not p.isdigit()
                and re.fullmatch(r"[A-Za-z0-9 ,.'!?%$#\-_:;()\[\]…&/]+", p)):
            return p
    return ''

def clip(s, n=46):
    s = s.strip().replace('\n', ' ')
    return s if len(s) <= n else s[:n] + '…'

b, count, texts = read_strg(SRC)
rows = []
for k in range(count):
    raw = texts[k].decode('utf-8', 'replace')
    rows.append((k, raw.split(';') if ';' in raw else [raw]))

FEEDS = ('repVillageUp', 'repVillageDown', 'repVillageTier', 'repFactionUp', 'repFactionDown',
         'repFactionTier', 'repAllTownsUp', 'repAllTownsDown', 'ReputationGainGlobal')
UI_KEYS = ('当前关系', '声誉历史', '声誉的影响因素', '下一级')
feeds = []
seen_feeds = set()
sources = []
for k, parts in rows:
    if len(parts) < 2:
        continue
    key = parts[0]; z = zh_of(parts)
    if not z:
        continue
    if key in FEEDS and (key, z) not in seen_feeds:
        seen_feeds.add((key, z)); feeds.append(dict(locator=k, key=key, zh=clip(z), en=clip(en_of(parts))))
    if re.search(r'\[声誉%rep_amount%\]', z):
        sources.append(dict(locator=k, key=key, zh=clip(z), en=clip(en_of(parts))))

PERK_POS = ('specialQuest', 'specialtyGoods', 'advances', 'commonCause', 'betterStocks1',
            'betterStocks2', 'betterStocks3', 'favorablePrices1', 'favorablePrices2',
            'favorablePrices3', 'cityOfOpportunities', 'underworldConnections1',
            'underworldConnections2', 'magistrateCapital', 'magistrateForefront')
PERK_NEG = ('raisedPrices1', 'raisedPrices2', 'worseStocks1', 'worseStocks2', 'hostilePopulace')
def row_kind(locator, key, z):
    if 15494 <= locator <= 15513 or 15433 <= locator <= 15447:
        return 'name'
    if 15472 <= locator <= 15491 or 15416 <= locator <= 15430:
        return 'effect'
    return 'desc' if len(z) > 12 else 'name'

perks = []
for k, parts in rows:
    if len(parts) < 2:
        continue
    key = parts[0]; z = zh_of(parts)
    if key in PERK_POS or key in PERK_NEG:
        perks.append(dict(locator=k, key=key, kind='pos' if key in PERK_POS else 'neg', row=row_kind(k, key, z), zh=clip(z), en=clip(en_of(parts))))

STATES = ('shortage', 'disruptedLogistics', 'delayedSupplies', 'nightmares', 'pest',
          'dangerousRoads', 'gathering', 'fleaMarket', 'occultConsilium', 'reinforcements',
          'pilgrimage', 'competition', 'rut', 'bloom', 'fair')
states = []
for k, parts in rows:
    if len(parts) < 2:
        continue
    key = parts[0]; z = zh_of(parts)
    if key in STATES and z:
        states.append(dict(locator=k, key=key, row=row_kind(k, key, z), zh=clip(z), en=clip(en_of(parts))))

crime = []
for k, parts in rows:
    if len(parts) < 2:
        continue
    key = parts[0]; z = zh_of(parts)
    if key.startswith('o_db_crime') or key in ('crimesCommited',):
        crime.append(dict(locator=k, key=key, row='label' if len(z) <= 12 else 'text', zh=clip(z), en=clip(en_of(parts))))

ui = []
for k, parts in rows:
    if len(parts) < 2:
        continue
    z = zh_of(parts)
    if z in UI_KEYS:
        ui.append(dict(locator=k, key=parts[0], zh=z, en=clip(en_of(parts))))

notes = [
    '只读静态结构;片段不超过46字,不保存完整对白。',
    '声誉按村落/阵营/全域三层出信息流,另有声誉历史与影响因素界面。',
    '来源行统一带[声誉%rep_amount%],覆盖契据、委托、剧情任务与犯罪/贸易等。',
    '档位加成含正负两向:特殊任务、特殊货、预付赏金、库存/价格修正、外溢等。',
    '地方状态15项(短缺/货运/梦魇/瘟病/匪患/黑道会面/跳蚤市场/增援/朝圣/竞争/繁殖/生机/集会等)各带效果说明。',
]
out = dict(
    date='2026-10-13', source=str(SRC), sha256=hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
    strg_count=count, feeds=feeds, sources=sources, perks=perks, states=states,
    crime=crime, ui=ui, notes=notes,
)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(feeds=len(feeds), sources=len(sources), perks=len(perks),
                      states=len(states), crime=len(crime), ui=len(ui)), ensure_ascii=False))
