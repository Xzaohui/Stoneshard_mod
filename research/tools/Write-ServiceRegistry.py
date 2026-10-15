"""Render the S90 service-registry (one paid service per city) into the vault."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'SERVICE-REGISTRY-S90'
HP = ROOT / 'research/service-generated-note-hashes.json'
DOC = '09_系统逻辑/城市服务班与有限库存.md'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def front(t, i, k): return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, S90, system]\naliases: []\n---\n\n# {t}\n\n'

data = read('research/service-registry.json')
model = read('research/city-campaign.json')
manifests = {}
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    try: h = read('research/' + p.name)
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    for rel, expected in h.items():
        if sha(ROOT / rel) != expected: raise SystemExit('Preserve/reconcile prior note: ' + rel)
    manifests[p] = h

t = front('城市服务班与有限库存', 'SYS-SERVICE-S90', 'system')
t += '本页落实各城既有规则「每城只新设一个普通有偿服务班，一批案件结束前不刷新库存」，把十五个地域的服务班写到可制作粒度：名称、经办人、职能、有限库存、档位便利与边界。与[[城镇声望与信任系统]]的档位语义配套；与原生商店/银行/海关/官署不重叠。\n\n## 共享规则\n\n'
for r in data['shared_rules']:
    t += f'- {r}\n'
t += '\n## 一览\n\n| 城 | 服务班 | Service | 经办人 |\n| --- | --- | --- | --- |\n'
for s in data['services']:
    t += f"| {s['city']} | {s['name_cn']} | {s['name_en']} | {s['operator']} |\n"
for s in data['services']:
    t += f"\n## {s['city']}：{s['name_cn']}\n\n"
    t += f"**{s['name_en']}**；经办：{s['operator']}。\n\n**职能**：{s['function_cn']}<br>{s['function_en']}\n\n"
    t += '**有限库存**：\n' + '\n'.join(f'- {x}' for x in s['stock']) + '\n\n'
    t += f"**档位便利**：{s['convenience_cn']}<br>{s['convenience_en']}\n\n**刷新**：{s['refresh_cn']}<br>{s['refresh_en']}\n\n**边界**：{s['bounds_cn']}<br>{s['bounds_en']}\n"
t += '\n## 校验与边界\n\n- 覆盖：十五城各一班；库存为设计上限，价格与数值待实机校准。\n- 校验：`research/tools/Validate-ServiceRegistry.py`；机器通过不代表经济校准或游戏运行。\n\n[[经济与奖励]] · [[城镇声望与信任系统]] · [[城市与聚落设计总索引]] · [[系统逻辑索引]] · [[设计库生成与校验流程]]\n'
p = V / DOC; p.write_text(t, encoding='utf-8')
changed = {'design/' + DOC}; generated = {'design/' + DOC: sha(p)}

summary = '## S90城市服务班与有限库存（当前登记）\n\n[[城市服务班与有限库存]]。十五城各一个普通有偿服务班（名称中英／经办人／职能／有限库存／档位便利／边界），落实「一批案件结束前不刷新库存」；档位只改范围与便利（−2关闭／−1限范围／0基础／+1一处小便利／+2预约与转介），不改授权、不无限供给。校验脚本不替代经济校准或游戏运行。'
for name in ['经济与奖励', '城市与聚落设计总索引', '系统逻辑索引', '城市篇章与跨区域任务网']:
    q = next(V.rglob(name + '.md')); rel = q.relative_to(V).as_posix()
    body = q.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; blk = a + '\n' + summary + '\n' + z
    q.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + blk + '\n', encoding='utf-8')
    changed.add('design/' + rel)
for s in data['services']:
    c = next(x for x in model['cities'] if x['id'] == s['city'])
    q = V / c['file']
    body = q.read_text(encoding='utf-8-sig')
    blk = f"## 本城服务与信任（S90）\n\n本城普通有偿服务班：**{s['name_cn']}**（{s['name_en']}，经办：{s['operator']}）；范围与库存见[[城市服务班与有限库存]]，档位语义见[[城镇声望与信任系统]]，人物细描见[[人物细描与随身物]]。"
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; n = a + '\n' + blk + '\n' + z
    q.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: n, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + n + '\n', encoding='utf-8')
    changed.add('design/' + c['file'])

for p2, h in manifests.items():
    touched = False
    for rel in changed & set(h):
        h[rel] = sha(ROOT / rel); touched = True
    if touched:
        p2.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
HP.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

rule = '2026-10-12 S90：用户要求继续完成项目。research/service-registry.json登记十五城各一个普通有偿服务班（名称中英／经办人／职能／有限库存／档位便利／边界），落实「一批案件结束前不刷新库存」与「不刷新成玩家跑腿任务」；同一块挂到十五张城市页（服务/信任/人物细描三链）。入口design/09_系统逻辑/城市服务班与有限库存.md；档位便利与[[城镇声望与信任系统]]配套，只改范围与便利、不越授权、不无限供给。运行Validate-ServiceRegistry.py及既有检查；价格数值、美术与游戏未验收，不部署。'
for p3 in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md', ROOT / 'CHANGELOG.md']:
    body = p3.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; blk = a + '\n' + rule + '\n' + z
    p3.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + blk + '\n')
print(json.dumps({'services': len(data['services']), 'generated': len(generated), 'changed': len(changed)}, ensure_ascii=False))
