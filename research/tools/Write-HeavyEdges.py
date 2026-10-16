"""Render only the HX conditional extension; never rewrite screenplays or rules."""
from pathlib import Path
import json
from HeavyEdges import project
ROOT = Path(__file__).resolve().parents[2]
def read(name): return json.loads((ROOT / 'research' / name).read_text(encoding='utf-8'))
def save(name, data):
    # Keep the repository JSON newline convention across chained rebuilds.
    (ROOT / 'research' / name).write_bytes((json.dumps(data, ensure_ascii=False, indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
net = read('story-network.json')
state=read('state-keys.json')
effects, stubs, keys = project(net,state['keys'])
for name, field, value in [('event-stubs.json','heavy_edge_stubs',stubs),
                            ('state-keys.json','heavy_edge_keys',keys)]:
    data=read(name); data[field]=value
    if name == 'state-keys.json':
        data['heavy_edge_families']={'route':sum(k.get('kind') == 'route' for k in keys), 'state':sum(k.get('kind') != 'route' for k in keys)}
    if name == 'state-keys.json':
        prefix='HX 缺省值代表未发生的键：'
        data['conventions']=[c for c in data.get('conventions',[]) if not c.startswith(prefix)] + [prefix+'、'.join(k['key'] for k in keys if k.get('note','').startswith('缺省值代表未发生'))+'；初始化即提供缺省值，无需为其建立实际处置生产者。sylang_state=alive 是初始生存状态，不表示发生死亡。']
    save(name,data)
events=read('event-stubs.json')
from HeavyEdges import support_stubs
events['route_state_stubs']=support_stubs(net)
events['resolve_settle_stubs']=support_stubs(net, settlement=True)
events['route_state_rule']='仅写 route_* 或独立状态；不得写 resolve_*，不代播旧 callback。'
events['resolve_settle_rule']='仅在对应旧 choice 实际处置确认后写 resolve_*；取值限旧 state-keys.keys 值域，不写路线/独立状态。'
save('event-stubs.json',events)
hooks=read('hook-mapping.json')
hooks['heavy_edge_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'],
                                  engine_event=None, when=s['when']) for s in stubs]
hooks['route_state_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'], engine_event=None, when=s['when']) for s in events['route_state_stubs']]
hooks['resolve_settle_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'], engine_event=None, when=s['when']) for s in events['resolve_settle_stubs']]
hooks['route_state_rule']=events['route_state_rule']
hooks['resolve_settle_rule']=events['resolve_settle_rule']
save('hook-mapping.json',hooks)
print(json.dumps(dict(effects=len(effects),stubs=len(stubs),keys=len(keys))))

import re
section = ('<!-- HX-SUPPORT-S206A:BEGIN -->\n## S206a 路线、状态与旧结算分节\n\n'
           f"`route_state_stubs`：{len(events['route_state_stubs'])} 项，只写 `route_*` 或独立状态，禁止写 `resolve_*`。\n\n"
           f"`resolve_settle_stubs`：{len(events['resolve_settle_stubs'])} 项，只写旧 `resolve_*` 且沿用 `state-keys.keys` 的旧值域；对应 choice 实际处置确认后提交，旧 callback 语义保留。\n\n"
           '`hook-mapping.json` 分别使用 `route_state_bindings` 与 `resolve_settle_bindings`，事件名保留。\n\n'
           '`custody_signed=none` 表示尚未签认，删除无实际签认意义的 `evt_N17_custody_signed_none`；N17 仅实际签认 MG/CO/GA/dispersed 时复制意向并冻结。初始化缺省值已可读取，校验无需另找缺省值生产者。\n\n'
           '逐键缺省含义见 `state-keys.json` 的 `heavy_edge_keys.note` 与 `conventions`；不增奖励、证据或运行声明。\n'
           '<!-- HX-SUPPORT-S206A:END -->')
for rel in ('design/09_系统逻辑/事件桩映射总表.md', 'design/11_管理/触发器接线点映射.md', 'design/09_系统逻辑/状态键映射总表.md'):
    path=ROOT/rel; raw=path.read_bytes(); text=raw.decode('utf-8-sig').replace('\r\n','\n')
    pattern=r'<!-- HX-SUPPORT-S206A:BEGIN -->.*?<!-- HX-SUPPORT-S206A:END -->'
    text=re.sub(pattern, lambda _: section, text, flags=re.S) if '<!-- HX-SUPPORT-S206A:BEGIN -->' in text else text.rstrip()+'\n\n'+section+'\n'
    path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\n','\r\n').encode('utf-8'))
