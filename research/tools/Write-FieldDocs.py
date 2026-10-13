"""Author S100 field-site readable documents (short texts) tied to S94/S99 NPCs.

Each entry records owner, copy state, where it is found and what reading does
(nothing: no reward, no task progress, no substitute for consent).
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FIELD-DOCS-S100'
CARD = '02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inv = json.loads((ROOT / 'research/special-location-inventory.json').read_text(encoding='utf-8'))
SITES = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
DOCS = [
 dict(id='DOC-PLG', title='封条与撒灰公告', site='rumor_plagueVillage1', holder='FX-PLG', state='原件（贴在村口木柱上）',
      where='村口上风处木柱', text='此地封存，外人不得入内。石灰每七日一撒，由看守记数。代领遗物者，先在篱笆外报名，名字写在木牌背面。',
      read='只读到封存与报名规矩；不给通行、不开启任何房屋。'),
 dict(id='DOC-LEP', title='物资清单（药房副件）', site='rumor_leprosy1', holder='FX-LEP', state='副件（原件在药房账柜）',
      where='篱笆内台阶上的木匣', text='本月到货：油膏两罐、麻布一卷、净水三桶。缺口：退热草、盐。送物者请照单放台阶，不得入内清点。',
      read='只说明缺什么；阅读不等于补货，也不解锁配方。'),
 dict(id='DOC-MIL', title='闸门刻记与纸抄', site='rumor_abandonedWatermill1', holder='FX-MIL', state='刻记（原件在闸板）＋纸抄（副件）',
      where='闸板下沿；纸抄夹在磨盘架', text='上闸三日一放，下闸五日记一次。黄水不放，浑水缓放。代开闸者，责任自负，写名于纸抄。',
      read='给的是水规与责任写法；不替玩家开闸，也不保证下游后果。'),
 dict(id='DOC-MIN', title='支撑木记号说明', site='rumor_mine1', holder='FX-MIN', state='原件（木牌挂在入口）',
      where='矿口第一排轨枕旁', text='横杠一：顶得住；横杠二：进两步退一步；叉号：别进。记号由捡拾人每日加一笔，擦改无效。',
      read='教读记号；不改变洞内实际塌方判定。'),
 dict(id='DOC-CV1', title='洞口径向记号', site='rumor_cave1', holder='FX-CV1', state='石堆刻痕（无副件）',
      where='洞口内三步处的石堆', text='三石为一步，五步一转。风停则返，灯灭则坐。记号只到第二处岔口，再往里无人担保。',
      read='只覆盖到第二处岔口；不承诺更深的路。'),
 dict(id='DOC-HUT', title='药棚账页（副件）', site='rumor_hermitHut1', holder='FX-HUT', state='副件（原账在师父柜中）',
      where='门槛内右侧的账匣', text='借出：止血粉半罐（驿馆，凭单）、干艾两束（自用）。归入：车前草三束。未归者不催，记一笔。',
      read='只看到借还记录；抓药仍须师父点头，账页不能当方子。'),
 dict(id='DOC-INK', title='赊账板', site='rumor_ralphSons1', holder='FX-INK', state='原件（挂在柜台内侧）',
      where='柜台内侧钉板', text='赊账三笔，两笔已销，一笔挂着。挂账者：过路商人，押铜扣一枚。销账凭本人到场，不凭字条。',
      read='看到账目与销账规矩；玩家不能凭此替人销账或领取抵押。'),
 dict(id='DOC-CMP', title='空营登记板', site='rumor_camp4', holder='FX-CMP', state='原件（清点人随身木板）',
      where='兵营旗杆座旁', text='在册：床架七、军旗杆座一、登记板一。缺：床架三（拆走）、旗（带走）。清点人每日核一遍，板不离人。',
      read='只说明缺件；不认领装备、不补发军械。'),
 dict(id='DOC-MAN', title='侧门钥匙说明（无主）', site='rumor_banditRuins1', holder='FX-MAN', state='原件（夹在门廊缝里，无主）',
      where='门廊立柱裂缝', text='侧门钥匙两把，一把断在锁里，一把在旧主人手里。此纸只作说明，不代钥匙。若有人拿此纸开门，后果自担。',
      read='纸不等于钥匙；不开启侧门、不指向任何财物。'),
 dict(id='DOC-RLY', title='灰坑旁留话', site='rumor_camp2', holder='FX-RLY', state='原件（压在灰坑石下）',
      where='灰坑边压石下', text='锅是我的，火你自己生。灰坑三日一清，别在坑上立杆。留物者自看，丢了我不管。要过桥，等第二块板修好。',
      read='只说明营地规矩与绕路；不代为保管物品。'),
 dict(id='DOC-LOT', title='染缸下的半张清单', site='rumor_homesteadLooted1', holder='FX-LOT', state='残件（半张，被撕）',
      where='染缸底下', text='蓝布四匹、灰布两匹、细线一束……（下沿撕缺）亲属凭布尺认领，认领前先说明来处。抢走的东西不在此单。',
      read='只认到自家布匹范围；不能替他人认领，也不指认抢掠者。'),
 dict(id='DOC-FRM', title='井绳上的结', site='rumor_homestead1', holder='FX-FRM', state='原件（绳结，无纸）',
      where='井台木架上', text='每打一桶记一结：满缸十二结，够用三日。结由住户自己打，外人不动绳。要水先问，不自己下桶。',
      read='只说明用水规矩；不改变井水判定，也不能替住户打水。'),
]
DOCS_EN = {'DOC-PLG': {'title_en': 'Seal and Lime Notice', 'text_en': 'This place is sealed; outsiders may not enter. Lime is spread every seventh day and counted by the keeper. Those claiming effects for others first give their names on the back of the board.', 'read_en': 'Covers the seal and the claiming rule only; grants no passage and opens no house.'}, 'DOC-LEP': {'title_en': 'Supply List (Infirmary Copy)', 'text_en': 'Arrivals this month: two pots of salve, one roll of linen, three buckets of clean water. Short: feverfew, salt. Deliveries go on the step per the list; no counting inside.', 'read_en': 'States what is short; reading is not restocking and unlocks no formula.'}, 'DOC-MIL': {'title_en': 'Sluice Marks and Paper Copy', 'text_en': 'Upper gate opened every third day, lower gate logged every fifth. Brown water stays; cloudy water opens slowly. Whoever opens for another writes a name on the copy and answers for it.', 'read_en': 'Gives the water rule and where responsibility is written; opens nothing and promises no downstream outcome.'}, 'DOC-MIN': {'title_en': 'Prop Mark Guide', 'text_en': 'One bar: holds. Two bars: two steps in, one back. Cross: keep out. The salvager adds a stroke daily; erasures do not count.', 'read_en': 'Teaches the marks only; it does not change what the mine decides.'}, 'DOC-CV1': {'title_en': 'Cave Mouth Markers', 'text_en': 'Three stones make a pace, five paces to a turn. Wind stops, turn back; lamp dies, sit. The marks reach the second fork and no further; nobody vouches beyond.', 'read_en': 'Covers only as far as the second fork; promises nothing deeper.'}, 'DOC-HUT': {'title_en': 'Drying Shed Ledger (Copy)', 'text_en': 'Out: half a jar of styptic powder (inn, by note), two bundles of dried mugwort (own use). In: three bundles of plantain. Late returns are not chased, only noted.', 'read_en': 'Shows borrowings and returns; dispensing still needs the master, and the ledger is no prescription.'}, 'DOC-INK': {'title_en': 'Credit Board', 'text_en': 'Three credits open, two struck, one hanging. Hanging: a passing trader, one brass clasp in pledge. Accounts close in person, not by note.', 'read_en': 'Shows the account and the closing rule; nobody may close another account or claim the pledge.'}, 'DOC-CMP': {'title_en': 'Empty Camp Register', 'text_en': 'On the books: seven bed frames, one banner pole base, one register. Missing: three frames, the banner. The clerk checks daily; the board stays with him.', 'read_en': 'States what is missing; it claims no gear and reissues no stores.'}, 'DOC-MAN': {'title_en': 'Side Door Note (Unclaimed)', 'text_en': 'Two side-door keys: one snapped in the lock, one with the former owner. This note explains; it does not stand for a key. Whoever opens with this note answers for it.', 'read_en': 'A note is not a key; it opens no side door and points to no goods.'}, 'DOC-RLY': {'title_en': 'Note by the Ash Pit', 'text_en': 'The pot is mine; make your own fire. The pit is cleared every third day; do not pitch a pole over it. Left goods look after themselves. To cross, wait until the second plank is fixed.', 'read_en': 'Covers camp rules and the detour only; nothing is held for anyone.'}, 'DOC-LOT': {'title_en': 'Half a List under the Dye Tub', 'text_en': 'Blue cloth four bolts, grey cloth two, fine thread one skein... (torn below). Kin claim by cloth measure and first state where it came from. Looted goods are not on this list.', 'read_en': 'Claims only the household cloth; it claims for no one else and names no looters.'}, 'DOC-FRM': {'title_en': 'Knots on the Well Rope', 'text_en': 'One knot per bucket: twelve knots fill the vat, three days of use. The householder ties them; outsiders leave the rope alone. Ask for water; do not lower your own bucket.', 'read_en': 'States the water rule; it changes no well and draws no water for anyone.'}}
for d in DOCS: d.update(DOCS_EN[d['id']])
assert len({d['id'] for d in DOCS}) == len(DOCS)
for d in DOCS:
    assert d['site'] in SITES, d['id'] + ' site'
    assert d['holder'].startswith('FX-'), d['id'] + ' holder'
    assert (V / f"04_人物/野外人物/人物_{d['holder']}_").exists() or any(
        p.stem.startswith(f"人物_{d['holder']}_") for p in (V / '04_人物/野外人物').glob('*.md')), d['id'] + ' holder card'
    assert 20 <= len(d['text']) <= 120, d['id'] + ' text length'
    assert re.search(r'[\u4e00-\u9fff]', d['text']) and not re.search(r'[A-Za-z]', d['text']), d['id'] + ' text purity'
    for k in ('title', 'state', 'where', 'read'): assert d[k].strip(), d['id'] + ' ' + k
    for k in ('title_en', 'text_en', 'read_en'):
        s2 = d[k]
        assert s2.strip() and not re.search(r'[\u4e00-\u9fff]', s2) and len(s2) <= 260, d['id'] + ' en ' + k
out = dict(date='2026-10-13', scope='S100 field-site readable documents: owner, copy state, find spot, short text and read limits; reading grants no reward, no task progress and no substitute for consent',
           rules=['文书均为Mod原创，不复用原作文本；阅读只给信息，不完成任何任务、不发奖励',
                  '原件／副件／残件分记：副件与残件不具原件效力，不能替代本人到场',
                  '读到的内容不越本人授权：代领、销账、认领、开闸、开门均须当事人点头',
                  '文本短、可读，长文本另存；不堆商业资源'],
           docs=DOCS)
(ROOT / 'research/field-docs.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "文书_FX_野外地点短稿"\nid: FX-FIELD-DOCS\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S100, field-npc, document]\naliases: []\n---\n\n'
     '# 文书_FX_野外地点短稿\n\n'
     f"本页是[[特殊地点与野外NPC对白扩展计划]]的文书产出：{len(DOCS)} 份野外地点短文书，与[[台本_FX_野外人物对白]]的人物和[[特殊地点设计卡总表]]的地点对应。"
     '全部为Mod原创短稿（中英对照，英文为Mod原创新稿，不冒充原版译文）；阅读只给信息，不完成任何任务、不发奖励，也不替代当事人到场。原件／副件／残件分记。\n\n'
     '| 文书 | 地点 | 保管人 | 状态 | 所在 |\n|---|---|---|---|---|\n')
for d in DOCS:
    n += f"| {d['title']}（`{d['id']}`） | `{d['site']}` {SITES[d['site']]} | [[人物_{d['holder']}_" + next(p.stem.split('_')[-1] for p in (V / '04_人物/野外人物').glob(f'人物_{d["holder"]}_*.md')) + f"]] | {d['state']} | {d['where']} |\n"
for d in DOCS:
    n += f"\n## {d['title']} / {d['title_en']}\n\n**地点**：`{d['site']}` {SITES[d['site']]}；**保管人**：见上表；**状态**：{d['state']}；**所在**：{d['where']}。\n\n"
    n += f"> {d['text']}\n>\n> {d['text_en']}\n\n**阅读所得与边界**：{d['read']}\n\n**Reading limits (EN)**：{d['read_en']}\n"
n += ('\n## 边界\n\n- 文书均为Mod原创，未复用原作文本；不新增物品栏条目，不设“读三纸”式收集。\n'
      '- 副件与残件不具原件效力：认领、销账、开闸、开门均须当事人点头；阅读本身不推进任何台本。\n'
      '- 未做：比例位置与摆放、实际交互脚本、英文稿。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[台本_FX_野外人物对白]] · [[特殊地点设计卡总表]] · [[原创物品与装备总表]] · [[文书与现场文本台本]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S100野外地点文书短稿（当前登记）\n\n'
           f"[[文书_FX_野外地点短稿]]：{len(DOCS)} 份Mod原创短文书（封条公告、物资清单、闸记、支撑木记号、洞口径向、药棚账页、赊账板、空营登记板、侧门说明、灰坑留话、染缸清单、井绳结），原件／副件／残件分记；阅读只给信息、不发奖励、不替代当事人同意。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/field-docs-note-hashes.json'
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
rule = ('\n<!-- FIELD-DOCS-S100:BEGIN -->\n2026-10-13 S100：用户要求扩充特殊地点内容。'
        f'research/field-docs.json 登记 {len(DOCS)} 份Mod原创野外地点短文书（原件/副件/残件分记，绑S94/S99人物与S92地点），入口design/02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md。'
        '阅读只给信息：不完成任务、不发奖励、不替代当事人同意；不设收集式门槛。运行Validate-FieldDocs.py及既有检查；摆放与交互脚本仍待做，不部署游戏包。\n<!-- FIELD-DOCS-S100:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- FIELD-DOCS-S100:BEGIN -->.*?<!-- FIELD-DOCS-S100:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- FIELD-DOCS-S100:BEGIN -->.*?<!-- FIELD-DOCS-S100:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md', '入口 [文书_FX_野外地点短稿](design/02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md)'), encoding='utf-8')
print(json.dumps(dict(docs=len(DOCS), notes=len(generated)), ensure_ascii=False))
