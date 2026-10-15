"""Validate the S102 stage acceptance record: numbers match sources, rendering and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
inv = read('research/special-location-inventory.json'); rd = read('research/original-npc-reading.json')
fx = read('research/field-npc-dialogue.json'); sg = read('research/field-signs.json')
fd = read('research/field-docs.json'); xc = read('research/mod-location-crosscheck.json')
led = read('research/foreshadow-ledger.json')
stems = {p.stem for p in V.rglob('*.md')}
card = (V / '11_管理/特殊地点与野外NPC阶段验收记录.md').read_text(encoding='utf-8')
check('# 特殊地点与野外NPC阶段验收记录' in card and '## 剩余项' in card and '## 校验记录' in card, 'card-structure')
lines_count = sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][k]) for k in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs'])
expect = {
 'inv-regions': f"{len(inv['map_regions'])} / {len(inv['rumor_sites'])} / {len(inv['site_types'])}",
 'reading-slots': f"{rd['slots']} 槽 / {len(rd['groups'])} 组",
 'npc-tags': f"{len(rd['npc_tags'])} 组 / 引擎侧",
 'field-npcs': f"{len(fx['npcs'])} 人 / {lines_count} 条",
 'sites': f"{len(inv['rumor_sites'])} 处 / 6 地域",
 'signs': f"{len(sg['signs'])} 处",
 'docs': f"{len(fd['docs'])} 份",
 'xcheck': f"{len(xc['dungeons'])} 副本 / {len(xc['brynn_spaces'])} 场景 / {len(xc['field_npcs'])} 人",
 'ledger': f"{sum(1 for t in led['threads'] if t['bucket'] == 'reference')} 组 / 共 {len(led['threads'])} 线程",
}
for k, v in expect.items():
    check(v in card, 'count-' + k)
for name in ['特殊地点与野外NPC清点', '野外NPC口吻与闲谈参照', '台本_FX_野外人物对白', '特殊地点设计卡总表',
             '野外迹象与观察', '文书_FX_野外地点短稿', 'Mod特殊地点与人物交叉核对', '伏笔与回收台账', '逻辑验收记录', '城市扩展验收记录']:
    check(f'[[{name}]]' in card, 'entry-' + name)
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
for key, txt in [('economy', '经济数值'), ('maps', '比例地图与生成点'), ('runtime', '运行验证'), ('english', '中英对照'), ('engine', '触发距离')]:
    check(txt in card, 'pending-' + key)
import re as _re
rows = _re.findall(r'\| ([0-9]+) 项 \|', card)
live = []
for n in ['special-location', 'npc-reading', 'npc-reading', 'field-npc', 'site-cards', 'field-signs', 'field-docs', 'mod-loc-xcheck',
          'foreshadow-ledger', 'field-flows', 'region-map', 'field-npc']:
    live.append(str(json.loads((ROOT / f'research/{n}-validation.json').read_text(encoding='utf-8'))['checks_passed']))
check(rows == live, 'record-counts-match-live-validation')
for a2, b2 in zip(rows, live):
    check(a2 == b2, f'record-count-{a2}-vs-{b2}')
check('44 处传闻地点全部有内容落点' in card, 'coverage-claim')
check('FS-33' in card and 'FS-36' in card, 'ledger-refs')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('FIELD-STAGE-S102:BEGIN' in plan and '[[特殊地点与野外NPC阶段验收记录]]' in plan, 'plan-block-and-link')
check('FIELD-STAGE-S102:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/field-stage-note-hashes.json')
check(len(h) == 4, 'own-manifest-4')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S102 stage record: delivered counts match sources, pending list present, links and chain; not economy, maps, runtime or English',
              npcs=len(fx['npcs']), lines=lines_count, checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/field-stage-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
