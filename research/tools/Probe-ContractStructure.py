"""Read-only probe of the vanilla contract (契据任务) structure.

Bounded: keys, counts, locators and <=46-character snippets only; no full
dialogue text is stored. Sections:
- Contract_* settings labels (CN/EN);
- contract feed/counter keys (CN/EN);
- every localized row whose Chinese text mentions 契据 (locator + snippet);
- named-contract dialogue key families (keys only) with a few state snippets;
- identifier-side contract data names (count + sample).
"""
from pathlib import Path
import hashlib, json, re, struct

GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
SRC = GAME / 'vanilla.win'
OUT = Path(__file__).resolve().parents[1] / 'contract-structure-probe.json'
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
    return best if best_n >= 1 else ''

def en_of(parts):
    for p in parts[1:]:
        if len(p) >= 4 and re.fullmatch(r"[A-Za-z0-9 ,.'!?%\-:;()\[\]…\"]+", p) and ' ' in p:
            return p
    return ''

def clip(s, n=46):
    s = s.strip().replace('\n', ' ')
    return s if len(s) <= n else s[:n] + '…'

b, count, texts = read_strg(SRC)
rows = []
for k in range(count):
    raw = texts[k].decode('utf-8', 'replace')
    if ';' in raw:
        rows.append((k, raw.split(';')))
    else:
        rows.append((k, [raw]))

settings = []
feeds = []
zh_hits = []
fam_keys = {}
for k, parts in rows:
    if len(parts) < 2:
        continue
    key = parts[0] if parts else ''
    z = zh_of(parts)
    if key.startswith('Contract_') and z:
        settings.append(dict(locator=k, key=key, zh=clip(z), en=clip(en_of(parts))))
    if key in ('contract', 'contractFail', 'contracts', 'contractsFailed', 'contractsCompleted') and z:
        feeds.append(dict(locator=k, key=key, zh=clip(z), en=clip(en_of(parts))))
    if z and '契据' in z:
        zh_hits.append(dict(locator=k, key=key, zh=clip(z)))
    if re.match(r'^[A-Za-z_]*contract[A-Za-z0-9_]*$', key):
        fam_keys.setdefault(key, k)
troll = [dict(locator=k, key=parts[0], zh=clip(zh_of(parts))) for k, parts in rows
         if parts and parts[0].startswith('trollcontract') and zh_of(parts)]
troll.sort(key=lambda r: r['locator'])

ident = []
for k, parts in rows:
    if len(parts) == 1 and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', parts[0]) and 'ontract' in parts[0]:
        ident.append(parts[0])
ident = sorted(set(ident))

notes = [
    '只读静态结构;不保存原作完整对白,片段不超过46字。',
    '契据任务(contract)按聚落领取;设置项含时间限制、可领数量与按地牢类型的声誉收益(地下经堂/墓穴/棱堡/通用)。',
    '完成与失败有信息流模板:%town_name%+%contract_name%+%rep_amount%;另有完成/失败计数。',
    '具名契据(巨魔)使用状态化对白(未接/进行/去过/已击杀+语气变体),可作为本Mod条件对白状态的对照。',
]
out = dict(
    date='2026-10-13', source=str(SRC), sha256=hashlib.sha256(SRC.read_bytes()).hexdigest().upper(),
    strg_count=count, settings=settings, feeds=feeds, zh_mentions=zh_hits,
    contract_key_count=len(fam_keys), contract_keys_sample=sorted(fam_keys)[:20],
    troll_rows=troll, identifier_contract_names=ident, notes=notes,
)
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(settings=len(settings), feeds=len(feeds), zh_mentions=len(zh_hits),
                      contract_keys=len(fam_keys), troll=troll and len(troll) or 0,
                      ident=len(ident)), ensure_ascii=False))
