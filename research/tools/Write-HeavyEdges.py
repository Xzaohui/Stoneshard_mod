"""Render only the HX conditional extension; never rewrite screenplays or rules."""
from pathlib import Path
import json, re, hashlib
from HeavyEdges import project, resolve_keys
ROOT = Path(__file__).resolve().parents[2]
def read(name): return json.loads((ROOT / 'research' / name).read_text(encoding='utf-8'))
def save(name, data): (ROOT / 'research' / name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
net = read('story-network.json')
state=read('state-keys.json')
# S62 route enums supersede the older screenplay choices for the same key.
for item in state['keys']:
    if item['key'] in resolve_keys(net):
        task=item['key'][8:].replace('_','-')
        if task in net['tasks']:
            item['values']=['none']+[r['key'] for r in net['tasks'][task]['routes']]
            item['source']='research/story-network.json'
save('state-keys.json',state)
effects, stubs, keys = project(net,state['keys'])
for name, field, value in [('design-model.json','conditional_influences',effects),
                            ('event-stubs.json','heavy_edge_stubs',stubs),
                            ('state-keys.json','heavy_edge_keys',keys)]:
    data=read(name); data[field]=value; save(name,data)
hooks=read('hook-mapping.json')
hooks['heavy_edge_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'],
                                  engine_event=None) for s in stubs]
save('hook-mapping.json',hooks)
rows='\n'.join('| `'+e['id']+'` | '+', '.join(p['task'] for p in e['sources'])+' → '+', '.join(p['task'] for p in e['targets'])+' | '+', '.join('`evt_'+e['id']+'_'+p+'`' for p in ['receipt','evaluate','commit'])+' | `receipt_'+e['id']+'` |' for e in effects)
block=('<!-- HX-WIRING:BEGIN -->\n## HX 条件影响接线扩展\n\n'
       'HX01—HX26 独立登记于 design-model 的 `conditional_influences`、event-stubs 的 `heavy_edge_stubs`、state-keys 的 `heavy_edge_keys` 和 hook-mapping 的 `heavy_edge_bindings`；原条件流计数保持其原范围。'
       '同名状态键复用；S62 的 resolve 枚举以 story-network 为准，替代旧台本 choices 的同名枚举；引擎键一律 `EAO_` 前缀。源写手重跑后由 `Write-HeavyEdges.py` 同步此扩展。\n\n'
       'receipt：源实际结算后 `on_state_change` 交付有限回执；evaluate：目标入口 `on_state_read` 重评未来参数（只读）；commit：源实际处置 `on_route_selected` 写已登记历史后果。'
       '死亡、缺席、拒绝、授权优先；未交付回执不视为已知。HX07 仅三路最后实际完成的一路读取 `order_HX07` 的 late 变体。'
       '已结案不回滚，N17 快照冻结后只作地方回访；不写证据、奖励或硬前置。\n\n'
       '| HX | 源→目标 | 事件桩 | 回执键 |\n|---|---|---|---|\n'+rows+'\n\n'
       '条件与分支见 [[后果分级与重边]]、[[城市主线回流S201]]；此为待实现接线规格，不声明真实引擎事件号或运行通过。\n<!-- HX-WIRING:END -->\n')
changed={}
for rel in ['09_系统逻辑/后果分级与重边.md','09_系统逻辑/城市主线回流S201.md',
            '09_系统逻辑/事件桩映射总表.md','09_系统逻辑/状态键映射总表.md',
            '11_管理/触发器接线点映射.md']:
    p=ROOT/'design'/rel; t=p.read_text(encoding='utf-8')
    t=re.sub(r'<!-- HX-WIRING:BEGIN -->.*?<!-- HX-WIRING:END -->\n?', '',t,flags=re.S)
    p.write_bytes((t.rstrip()+'\n\n'+block).replace('\n','\r\n').encode('utf-8'))
    changed['design/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
# Writer owns the appended block and reconciles all existing owners of these pages.
for p in (ROOT/'research').glob('*note-hashes.json'):
    d=json.loads(p.read_text(encoding='utf-8'))
    if isinstance(d,dict) and all(isinstance(v,str) for v in d.values()):
        touched=False
        for rel,h in changed.items():
            if rel in d and d[rel]!=h: d[rel]=h; touched=True
        if touched: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(effects=len(effects),stubs=len(stubs),keys=len(keys))))
