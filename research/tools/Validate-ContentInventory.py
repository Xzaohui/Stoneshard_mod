"""Validate the S125 content inventory by recomputing counts from sources."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ci = read('research/content-inventory.json')
rows = {r['kind']: r for r in ci['rows']}
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json'); sg = read('research/field-signs.json')
ag = read('research/ambient-gossip.json'); tg = read('research/town-gossip.json'); bg = read('research/band-gossip.json')
ia = read('research/interior-ambient.json'); rep = read('research/town-reputation.json')
svc = read('research/service-registry.json'); items = read('research/item-registry.json')
cf = read('research/corpus-flows.json'); sk = read('research/state-keys.json'); es = read('research/event-stubs.json')
story = {n: read(f'research/{n}') for n in ['story-main.json', 'story-side.json', 'story-main-late.json', 'story-daily.json', 'story-dungeon.json']}
expect = {
 '城市支线台本': len(model['quests']), '布林续篇台本': len(cont['quests']),
 '主线/支线/后章/副本台本': sum(len(v) for k, v in story.items() if k != 'story-daily.json'),
 '日常台本': len(story['story-daily.json']), '野外人物（含条件回访）': len(fx['npcs']),
 '野外文书': len(fd['docs']), '野外迹象': len(sg['signs']), '地区闲谈': len(ag['lines']),
 '城镇闲谈': len(tg['lines']), '声望档街头反应': len(bg['lines']), '副本与日常氛围句': len(ia['lines']),
 '声望档柜台台词': sum(len(t['bands']) for t in rep['towns']), '城市服务班': len(svc['services']),
 '原创物品': len(items['items']), '条件流节点（桥接）': sum(len(f['nodes']) for f in cf['flows']),
 '状态键（桥接）': len(sk['keys']), '事件桩（桥接）': len(es['stubs']),
}
check(set(rows) == set(expect), 'row-kinds-match')
for k, v in expect.items():
    check(rows[k]['count'] == v, 'count-' + k)
user = (sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][kk]) for kk in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs'])
        + len(fd['docs']) * 3 + len(sg['signs']) * 4 + len(ag['lines']) + len(tg['lines']) + len(bg['lines']) + len(ia['lines'])
        + sum(len(t['bands']) for t in rep['towns']))
check(ci['user_facing_units'] == user, 'user-units')
check(len(ci['rows']) == 17, 'rows-17')
card = (V / '00_导航/叙事内容清单.md').read_text(encoding='utf-8')
check('# 叙事内容清单' in card and '## 边界' in card and '## 阅读顺序建议' in card, 'card-structure')
check(f"用户可见文本合计约 **{user}** 个单元" in card, 'card-user-units')
for k, r in rows.items():
    check(f"| {k} | {r['count']} {r['unit']} |" in card, 'card-row-' + k)
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('CONTENT-INVENTORY-S125:BEGIN' in plan and '[[叙事内容清单]]' in plan, 'plan-block-and-link')
check('CONTENT-INVENTORY-S125:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/content-inventory-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S125 content inventory: recomputed counts per kind, user-facing unit total, rendering and chain; index only, not literary or runtime validation',
              rows=len(ci['rows']), user_units=user, checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/content-inventory-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
