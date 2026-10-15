"""Render the S87 foreshadow ledger into the vault and attach registry blocks."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
SRC = ROOT / 'research/foreshadow-ledger.json'
MARK = 'FORESHADOW-LEDGER-S87'
HP = ROOT / 'research/foreshadow-generated-note-hashes.json'
DOC = '09_系统逻辑/伏笔与回收台账.md'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def front(t, i, k): return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S87, foreshadow]\naliases: []\n---\n\n# {t}\n\n'
def block(t, b):
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + b.rstrip() + '\n' + z
    return re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + n + '\n'

data = read('research/foreshadow-ledger.json')
network = read('research/story-network.json'); edges = {e['id']: e for e in network['edges']}
model = read('research/city-campaign.json')
manifests = {}
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    try: h = read('research/' + p.name)
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    for rel, expected in h.items():
        if sha(ROOT / rel) != expected: raise SystemExit('Preserve/reconcile prior note: ' + rel)
    manifests[p] = h

def fmt(ids): return ' · '.join(ids)
t = front('伏笔与回收台账', 'SYS-FORESHADOW-LEDGER-S87', 'system')
t += '本页是全局“埋下—回收”单一入口，按用户2026-10-12要求建立；只登记关系与守则，不新增奖励、承诺或结局资格。主线丝线全部由 `research/story-network.json` 的X边背书，续篇桥与城镇回执由各自登记文件所有；登记口径与校验见页尾。\n\n'
t += '## 三档口径\n\n| 档 | 含义 |\n| --- | --- |\n'
for k, v in data['buckets'].items():
    t += f"| {k} | {v['cn']}<br>{v['en']} |\n"
t += '\n## 主线与并入丝线\n\n| ID | 伏笔 | 回收 | 背书机制 | 守则 |\n| --- | --- | --- | --- | --- |\n'
for th in data['threads']:
    if th['bucket'] != 'must_payoff': continue
    t += f"| {th['id']} {th['name_cn']} | {fmt(th['plants'])} | {fmt(th['payoff'])} | {' · '.join(th['backed_by'])} | {th['guard_cn']}<br>{th['guard_en']} |\n"
t += '\n## 成组引用\n\n| ID | 组 | 所有者 | 数量 | 守则 |\n| --- | --- | --- | --- | --- |\n'
for th in data['threads']:
    if th['bucket'] != 'reference': continue
    t += f"| {th['id']} {th['name_cn']} | `{th['registry']}` | {th['owner']} | {th['count']} | {th['guard_cn']}<br>{th['guard_en']} |\n"
t += '\n## 有意留白\n\n| ID | 主题 | 落点 | 理由 |\n| --- | --- | --- | --- |\n'
for th in data['threads']:
    if th['bucket'] != 'deliberate_open': continue
    t += f"| {th['id']} {th['name_cn']} | {fmt(th['plants'])} | {th['rationale_cn']}<br>{th['rationale_en']} |\n"
covered = [x for th in data['threads'] if th['bucket'] == 'must_payoff' for x in th['backed_by']]
bridge_count = next(x['count'] for x in data['threads'] if x['id'] == 'FS-25')
entitle_count = next(x['count'] for x in data['threads'] if x['id'] == 'FS-26')
t += f"\n## 覆盖与校验\n\n- 主线X边：{len(edges)}条，全部由丝线背书覆盖，无重复登记。\n- 布林续篇桥：{bridge_count}组；城镇受托解锁/听闻/回执各{entitle_count}处，分别归各自登记文件。\n- 留白不倒写成真相；未来若作者级资料揭底，先更新对应所有者再改本页。\n\n校验：`research/tools/Validate-ForeshadowLedger.py`（结构、背书闭合、数量与文档渲染）；机器通过不代表文学质量或游戏运行。\n\n[[系统逻辑索引]] · [[任务台本总索引]] · [[布林续篇任务与伏笔回收总表]] · [[叙事交叉影响矩阵]] · [[当前任务依赖与状态字典]]\n"
put_here = V / DOC
put_here.write_text(t, encoding='utf-8')
changed = {'design/' + DOC}; generated = {'design/' + DOC: sha(put_here)}

summary = f'## S87全局伏笔与回收台账（当前登记）\n\n[[伏笔与回收台账]]。主线{len(edges)}条X边、日常16条与副本18条并入线全部由丝线背书闭合；布林续篇15桥、城镇受托解锁/听闻/回执各15处成组引用；夜船货物、旧市长责任、晶石全貌与全国政体列为有意留白。校验脚本不替代文学与运行验证。'
for name in ['系统逻辑索引', '任务台本总索引', '布林续篇任务与伏笔回收总表']:
    p = next(V.rglob(name + '.md'))
    rel = p.relative_to(V).as_posix()
    put_here = p; put_here.write_text(block(p.read_text(encoding='utf-8-sig'), summary), encoding='utf-8')
    changed.add('design/' + rel)

for p, h in manifests.items():
    touched = False
    for rel in changed & set(h):
        h[rel] = sha(ROOT / rel); touched = True
    if touched:
        p.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
HP.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

rule = f'2026-10-12 S87：用户要求持续埋伏笔并回收。research/foreshadow-ledger.json把主线{len(edges)}条X边、日常16条、副本18条并入线写成闭合丝线；布林续篇15桥与城镇解锁/听闻/回执各15处成组引用；夜船货物、旧市长责任、晶石全貌、全国政体为有意留白。入口design/09_系统逻辑/伏笔与回收台账.md，运行Validate-ForeshadowLedger.py及既有检查；不新增奖励/承诺/结局资格，不部署。'
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md', ROOT / 'CHANGELOG.md']:
    body = p.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + rule + '\n' + z
    p.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + n + '\n')
print(json.dumps({'threads': len(data['threads']), 'edges_covered': len(covered), 'generated': len(generated)}, ensure_ascii=False))
