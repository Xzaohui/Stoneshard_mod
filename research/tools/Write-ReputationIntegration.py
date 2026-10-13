"""S136: link the S134/S135 vanilla reference cards into the town-reputation design.

Adds one preserved block to each reputation design note mapping the Mod's three
ledgers onto the vanilla structures, and re-renders the two reference cards so
they point back at the design notes.
"""
from pathlib import Path
import json, hashlib, re, subprocess, sys
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'REP-BASE-LINK-S136'
SYS_DOC = '09_系统逻辑/城镇声望与信任系统.md'
BIL_DOC = '09_系统逻辑/城镇声望系统中英对照.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
block_zh = ('## 原作对照（S134/S135）\n\n'
            '原作的契据与声誉结构见 [[原作契据任务与声誉结构参照]]（设置项、聚落结算模板、按地牢类型的声誉收益、预支/外溢/竞争）与 [[原作声誉档位与地方状态参照]]（村落/阵营/全域三层信息流、20 类来源、正负档位、两档通缉、15 项地方状态）。\n\n'
            '对应关系：原作的村落/阵营两级＝本页「原作声誉」层，保持原样不改写；本页新增「城镇信任」五档只作语气、有限服务与回访伏笔，不写原版档位消息、不作结局资格、不重复计同一行为。'
            '原作的库存/价格/预支/外溢/特殊商贩等档位数值不引入；本Mod信任档只改范围与便利（[[城市服务班与有限库存]]），单渠道折扣≤15%（[[经济与奖励]]）。'
            '原作的 15 项地方状态带价格/库存/难度修正，本Mod只写文本状态与回执。原作有犯罪计数与两档通缉，本Mod罪行另行处理、不改原版通缉。\n\n'
            '边界：对照只作结构参照，不复制原文；原作片段≤46字，未做运行时验证。')
block_en = ('## Base-game cross-reference (S134/S135)\n\n'
            'Vanilla contract and reputation structures: [[原作契据任务与声誉结构参照]] (settings, per-settlement settlement feed, reputation gain by dungeon type, advance/spillover/competition) and [[原作声誉档位与地方状态参照]] '
            '(village/faction/global feeds, 20 sources, positive and negative tiers, two wanted states, 15 local states).\n\n'
            'Mapping: the vanilla village/faction levels remain the untouched Original Reputation ledger; the new Town Trust scale only shapes tone, limited services and callbacks - it never writes vanilla tier messages, grants no ending standing and never double-counts one deed. '
            'Vanilla numeric tier effects (stock/price/advance/spillover/special vendors) are not adopted; Mod trust bands change scope and convenience only ([[城市服务班与有限库存]]), with a single-channel discount cap of 15% ([[经济与奖励]]). '
            'Vanilla local states carry price/stock/difficulty modifiers; the Mod writes text states and receipts only. Vanilla keeps crime counters and two wanted states; the Mod handles crimes separately and never rewrites them.\n\n'
            'Boundary: structural reference only; no source text copied; snippets are clipped to 46 characters; no runtime verification.')
t = (V / SYS_DOC).read_text(encoding='utf-8-sig')
blk = a + '\n' + block_zh + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(SYS_DOC, t2)
t = (V / BIL_DOC).read_text(encoding='utf-8-sig')
blk2 = a + '\n' + block_zh + '\n\n' + block_en + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk2 + '\n'
put(BIL_DOC, t2)
own = ROOT / 'research/rep-base-link-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
# refresh the two reference-card writers so their link lines include the design notes
ANCHORS = {
    'Write-ContractReference.py': ('[[势力关系总览]] · [[原创物品与装备总表]]\\n',
                                   '[[势力关系总览]] · [[原创物品与装备总表]] · [[城镇声望与信任系统]] · [[城镇声望系统中英对照]]\\n'),
    'Write-ReputationReference.py': ('[[城市服务班与有限库存]] · [[经济与奖励]]\\n',
                                     '[[城市服务班与有限库存]] · [[经济与奖励]] · [[城镇声望与信任系统]] · [[城镇声望系统中英对照]]\\n'),
}
for tool, (old_a, new_a) in ANCHORS.items():
    p = ROOT / 'research/tools' / tool
    s = p.read_text(encoding='utf-8')
    if '[[城镇声望与信任系统]]' not in s:
        assert old_a in s, tool
        p.write_text(s.replace(old_a, new_a), encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(notes=len(generated)), ensure_ascii=False))
