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
    save(name,data)
events=read('event-stubs.json')
from HeavyEdges import support_stubs
events['route_state_stubs']=support_stubs(net)
save('event-stubs.json',events)
hooks=read('hook-mapping.json')
hooks['heavy_edge_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'],
                                  engine_event=None, when=s['when']) for s in stubs]
hooks['route_state_bindings']=[dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'], engine_event=None, when=s['when']) for s in events['route_state_stubs']]
save('hook-mapping.json',hooks)
print(json.dumps(dict(effects=len(effects),stubs=len(stubs),keys=len(keys))))
