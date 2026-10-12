"""Author-specific S75 locations, never modulo placement or game resource claims."""
from pathlib import Path
import json

def profiles(root):return json.loads((root/'research/city-space-profiles.json').read_text(encoding='utf-8'))

def side_placement(root,c,n):
 data=profiles(root);first,last=data['district_assignments'][c['id']][n-1]
 sat=data['satellite_assignments'][c['id']][n-1]
 return first-1,sat-1,last-1

def enrich_city_spaces(root,model):
 data=profiles(root);assert set(data['regions'])=={c['id'] for c in model['cities']}
 village_data=json.loads((root/'research/satellite-space-profiles.json').read_text(encoding='utf-8'))['settlements']
 byq={q['id']:q for q in model['quests']}
 for c in model['cities']:
  specs=data['regions'][c['id']];assert len(specs)==len(c['districts'])
  c['space_file']=f"02_世界与地图/任务空间/空间_{c['id']}_{c['name']}.md"
  nodes={n['id']:n for n in c['nodes']};c['space_plans']=[]
  for i,spec in enumerate(specs,1):
   assert len(spec)==8
   a,b,layout,oa,aa,ob,ab,access=spec;did=f"{c['id']}-D{i:02}"
   room_ids=[did+'-A',did+'-B']
   associated=[q['id'] for q in model['quests'] if q['city']==c['id'] and (did in q['locations'] or any(w['node']==did for w in q.get('location_work',[])))]
   plan=dict(district=did,layout=layout,access=access,rooms=room_ids,quests=associated)
   c['space_plans'].append(plan)
   for rid,name,obj,action in [(room_ids[0],a,oa,aa),(room_ids[1],b,ob,ab)]:
    n=nodes[rid];n.update(name=name,purpose=action,space=dict(layout=layout,observable=obj,interaction=action,
      access_and_alternative=access,egress=[did],quests=associated,implementation='unimplemented; architectural intent, not scaled collision data'))
   work=next(w for w in byq[c['main_id']]['location_work'] if w['node']==did)
   work['action']=aa+' '+ab
  c['space_scope']='S75 replaces generic room names and modulo side-scene placement; no new mandatory full-city investigation or runtime rooms.'
  for sat in c['satellites']:
   layout,service,scene,obj,interaction,name,role,arc,line=village_data[sat['id']]
   sat['space']=dict(layout=layout,observable=obj,interaction=interaction)
   sat['resident'].update(name=name,role=role,arc=arc,line=line,file=f"04_人物/聚落人物/人物_{sat['id']}-NPC_{name}.md")
   nodes[sat['id']+'-2'].update(name=service)
   nodes[sat['id']+'-3'].update(name=scene,purpose=interaction)
 for q in model['quests']:
  c=next(c for c in model['cities'] if c['id']==q['city']);nodes={n['id']:n for n in c['nodes']}
  q['scene_spaces']=[]
  for i,nid in enumerate(q['locations'],1):
   node=nodes[nid]
   rooms=[nid+'-A',nid+'-B'] if node['kind']=='district' else [nid]
   q['scene_spaces'].append(dict(scene=i,location=nid,candidates=rooms,
    scope='Listed rooms are options within this scene, not required visits. Keep the existing route action and consent guards; private refusal uses the route-specific independent alternative.'))
 return model

def add_city_space_links(root,relative,text,model):
 key=relative;c=next((c for c in model['cities'] if c['file']==key or any(s['file']==key for s in c['satellites'])),None)
 q=next((q for q in model['quests'] if q['file']==key),None)
 if q:c=next(c for c in model['cities'] if c['id']==q['city'])
 if c is None:return text
 link='[['+Path(c['space_file']).stem+']]'
 body='<!-- CITY-SPACES-S75:BEGIN -->\n## 任务空间细化（S75）\n\n'+link+'列出本地域的独立室内、观察物与可执行交互、权限替代和安全回程；[[任务空间与地点关联审查]]记录逐任务地点修订。已有方法、证据和奖励所有者保持，各室内不是新必访清单。\n\n'
 if q:
  body+='|场次|街区／聚落节点|可选空间|\n|---|---|---|\n'
  cands={n['id']:n for n in c['nodes']}
  for scene in q['scene_spaces']:
   body+=f"|{scene['scene']}|`{scene['location']}`|"+' / '.join('`'+rid+'` '+cands[rid]['name'] for rid in scene['candidates'])+'|\n'
  body+='\n观察仅支持该场既定反转，不自动写resolve、私下授权或物资到位；若物证不足则保留未知或用已有独立方案，不把所有房间搜一遍当进度。\n'
  if q.get('satellite'):
   sat=next(s for s in c['satellites'] if s['id']==q['satellite']);resident=sat['resident']
   body+='\n**当地住户**：[['+Path(resident['file']).stem+']]，'+resident['role']+'。现场生活话：「'+resident['line']+'」这里只作本人的有限立场与场面素材，不替台本当事人同意、发任务奖或提供外城秘密。\n'
 return text.rstrip()+'\n\n'+body+'<!-- CITY-SPACES-S75:END -->\n'
