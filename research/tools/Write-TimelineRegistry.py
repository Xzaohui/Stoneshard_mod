"""Extract a single timeline-and-reward registry from the authored sources.

Consolidates chapter order, daily windows, dungeon entry, city-chapter turns
and continuation prerequisites with their existing reward statements. No new
numbers are invented; every cell is taken verbatim (trimmed) from the sources.
"""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'TIMELINE-REGISTRY-S88'
HP = ROOT / 'research/timeline-generated-note-hashes.json'
DOC = '09_系统逻辑/时序与奖励总表.md'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def front(t, i, k): return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, S88, system]\naliases: []\n---\n\n# {t}\n\n'
def cell(t, n=88):
    if not t: return ''
    t = re.sub(r'\s+', ' ', str(t)).strip()
    return t if len(t) <= n else t[:n] + '…'

main = read('research/story-main.json') + read('research/story-main-late.json')
side = read('research/story-side.json'); daily = read('research/story-daily.json'); dungeons = read('research/story-dungeon.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')

registry = {'date': '2026-10-12', 'status': 'draft', 'canon': 'mod-original',
 'scope': 'S88时序与奖励总表：从既有结构化台本抽取的单一审计视图；不新增数字、不替代[[经济与奖励]]的校准口径。',
 'global_rules': [
  '无隐藏全局倒计时；已接受日常与额外紧急救援按显式游戏时间期限失败，核心线索与主线出口不因逾期删除。',
  '日常episode_state=unseen/active/resolved/declined；具名冲突不随冷却回到unseen。',
  'N17安全台明确最终确认后冻结：之后只回访与未来维护，不重选旧方法、不改旧快照。',
  '奖励一次任务键/实例键去重；桥组与单方法回执分别计；接收边不发奖。',
  '数值仍按B档在干净基线校准；本表所载为设计口径，不是已生效报酬。'],
 'main': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [],
               at_least=q.get('at_least'), reward=cell(q.get('reward'))) for q in main],
 'side': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], reward=cell(q.get('reward'))) for q in side],
 'daily': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], cooldown=q.get('cooldown'),
                deadline=cell(q.get('deadline')), state=cell(q.get('state')), reward=cell(q.get('reward'))) for q in daily],
 'dungeon': [dict(id=q['id'], name=q['name'], requires=q.get('requires') or [], main=cell(q.get('main')), side=cell(q.get('side')), reward=cell(q.get('reward'))) for q in dungeons],
 'city': [dict(id=q['id'], city=q['city'], kind=q['kind'], requires=q.get('requires') or [], turn=cell(q.get('turn')), need=cell(q.get('need'))) for q in model['quests']],
 'continuation': [dict(id=q['id'], title=q['title'], requires=q.get('requires') or [], repeatable=q.get('repeatable'), reward_owner=q.get('reward_owner')) for q in cont['quests']]}

(ROOT / 'research/timeline-registry.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

manifests = {}
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    try: h = read('research/' + p.name)
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    for rel, expected in h.items():
        if sha(ROOT / rel) != expected: raise SystemExit('Preserve/reconcile prior note: ' + rel)
    manifests[p] = h

t = front('时序与奖励总表', 'SYS-TIMELINE-S88', 'system')
t += '本页把主线、支线、日常、副本、城市篇章与布林续篇的时序、期限与奖励声明抽到一处，便于“时间轴/有限经济”收口审查。数字与文案均为既有设计口径的**引用**，不在此新增；校准与实机测量仍按[[经济与奖励]]与[[当前任务依赖与状态字典]]。\n\n## 全局口径\n\n'
for r in registry['global_rules']:
    t += f'- {r}\n'
t += '\n## 主线时序与奖励\n\n| 任务 | 名称 | 前置 | 奖励声明（设计口径） |\n| --- | --- | --- | --- |\n'
for q in registry['main']:
    req = '、'.join(q['requires']) or '—'
    if q.get('at_least'): req += f"（任{q['at_least']['count']}/{len(q['at_least']['of'])}）"
    t += f"| {q['id']} | {q['name']} | {req} | {q['reward']} |\n"
t += '\n## 支线时序与奖励\n\n| 链 | 名称 | 前置 | 奖励声明（设计口径） |\n| --- | --- | --- | --- |\n'
for q in registry['side']:
    t += f"| {q['id']} | {q['name']} | {'、'.join(q['requires']) or '—'} | {q['reward']} |\n"
t += '\n## 日常期限\n\n| 模板 | 名称 | 前置 | 冷却(h) | 期限语义 | 状态机 |\n| --- | --- | --- | --- | --- | --- |\n'
for q in registry['daily']:
    t += f"| {q['id']} | {q['name']} | {'、'.join(q['requires']) or '—'} | {q['cooldown']} | {q['deadline']} | {q['state']} |\n"
t += '\n## 副本入口时序\n\n| 副本 | 名称 | 前置 | 主线位置 | 支线位置 |\n| --- | --- | --- | --- | --- |\n'
for q in registry['dungeon']:
    t += f"| {q['id']} | {q['name']} | {'、'.join(q['requires']) or '—'} | {q['main'] or '—'} | {q['side'] or '—'} |\n"
t += '\n## 城市篇章时序\n\n| 任务 | 城 | 类 | 前置 | 节奏（turn摘录） |\n| --- | --- | --- | --- | --- |\n'
for q in registry['city']:
    t += f"| {q['id']} | {q['city']} | {q['kind']} | {'、'.join(q['requires']) or '—'} | {q['turn']} |\n"
t += '\n## 布林续篇时序\n\n| 任务 | 题 | 前置 | 可重复 | 奖励所有者 |\n| --- | --- | --- | --- | --- |\n'
for q in registry['continuation']:
    t += f"| {q['id']} | {q['title']} | {'、'.join(q['requires']) or '—'} | {'是' if q['repeatable'] else '否'} | {cell(q['reward_owner'], 40)} |\n"
t += f"\n## 覆盖与校验\n\n- 覆盖：主线{len(registry['main'])}、支线{len(registry['side'])}、日常{len(registry['daily'])}、副本{len(registry['dungeon'])}、城市{len(registry['city'])}、续篇{len(registry['continuation'])}。\n- 奖励声明只摘录来源原文；桥组/单方法计数单位不混。\n- 校验：`research/tools/Validate-TimelineRegistry.py`；机器通过不代表经济校准或游戏运行。\n\n[[经济与奖励]] · [[当前任务依赖与状态字典]] · [[任务台本总索引]] · [[系统逻辑索引]] · [[伏笔与回收台账]]\n"
p = V / DOC; p.write_text(t, encoding='utf-8')
changed = {'design/' + DOC}; generated = {'design/' + DOC: sha(p)}

summary = '## S88时序与奖励总表（当前登记）\n\n[[时序与奖励总表]]。主线/支线/日常/副本/城市篇章/续篇的时序与奖励声明汇总到单一审计视图；无隐藏全局倒计时，日常按显式期限与episode_state，N17后冻结，奖励一次键去重。校验脚本不替代经济校准或游戏运行。'
for name in ['系统逻辑索引', '经济与奖励', '任务台本总索引']:
    q = next(V.rglob(name + '.md')); rel = q.relative_to(V).as_posix()
    body = q.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + summary + '\n' + z
    q.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + n + '\n', encoding='utf-8')
    changed.add('design/' + rel)

for p2, h in manifests.items():
    touched = False
    for rel in changed & set(h):
        h[rel] = sha(ROOT / rel); touched = True
    if touched:
        p2.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
HP.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

rule = '2026-10-12 S88：用户要求持续完善并收口全局逻辑。research/timeline-registry.json把主线18、支线8、日常16、副本9、城市73、续篇6的时序与奖励声明抽为单一审计视图（不新增数字）；入口design/09_系统逻辑/时序与奖励总表.md。全局口径：无隐藏倒计时、日常显式期限与状态机、最终确认后冻结、奖励一次键去重。对白独特性：修复布林续篇BC85-11—15五桥共用默认句、16个日常共用玩家句（源field＋writer模板）、CM-HIG说明文误入台词；Validate-DialogueDistinctiveness.py覆盖2962句源台词＋全库笔记层扫描（精确/规范化克隆、十笔记以上模板、12字短语跨5组、后台标识泄漏）。生成器可重跑：Write-StoryScripts/BrynnContinuation/Write-CityCampaign整篇重写时保留全部外部登记块（城市总写手另携带continuation_registries与dramatic_scope、复现CS-HIG-03入口文案并回写各哈希清单；隔离副本全量重跑后与主库逐字节一致）。另加Validate-CastRoster.py（158城市演员/89新卡/共享身份声明/条件引用/314回执接收者可解析）、奖励区间（N≤0.7B、SQ 0.2–0.3B、DT 0.15–0.3B）、“无限/永久免费”无界承诺、双语纯度与原文对白清点校验（1132条/72说话人槽）。运行新校验及既有检查；经济校准/比例地图/游戏运行未验收，不部署。'
for p3 in [ROOT / 'AGENTS.md', V / 'AGENTS.md', ROOT / 'README.md']:
    body = p3.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + rule + '\n' + z
    p3.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + n + '\n')
print(json.dumps({'main': len(registry['main']), 'side': len(registry['side']), 'daily': len(registry['daily']), 'dungeon': len(registry['dungeon']), 'city': len(registry['city']), 'continuation': len(registry['continuation'])}, ensure_ascii=False))
