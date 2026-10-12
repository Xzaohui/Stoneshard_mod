"""S75 explicit placement, semantic regression anchors, egress and preserved story ownership."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(ROOT/'research/city-campaign.json');p=read(ROOT/'research/city-space-profiles.json')
old=read(ROOT/'backups/city-spaces-20261012-s75/research/city-campaign.json');oq={q['id']:q for q in old['quests']};qs={q['id']:q for q in m['quests']}
village_profiles=read(ROOT/'research/satellite-space-profiles.json')['settlements']
checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
check(set(qs)==set(oq),'same-73-quest-identities')
check(m['effects']==old['effects'],'314-existing-receipts-and-their-conditions-preserved')
check(m['travel']==old['travel'] and m['rules']==old['rules'],'world-topology-ending-and-ownership-rules-preserved')
check(m['verified_runtime'] is False,'no-runtime-claim')
room_names=[];placements=0;residents=[];village_scenes=[]
for c in m['cities']:
 cid=c['id'];nodes={n['id']:n for n in c['nodes']};plans=c['space_plans']
 check(len(plans)==len(c['districts'])==len(p['regions'][cid]),cid+'-all-districts-authored')
 check((V/c['space_file']).exists(),cid+'-architecture-note')
 for plan in plans:
  did=plan['district'];check(set(plan['rooms'])=={did+'-A',did+'-B'},did+'-stable-room-identities')
  check(bool(plan['layout'].strip()) and bool(plan['access'].strip()),did+'-layout-and-access-alternative-recorded')
  check(c['main_id'] in plan['quests'],did+'-regional-purpose-linked')
  for rid in plan['rooms']:
   n=nodes[rid];s=n['space'];room_names.append(n['name'])
   check(n['name'] not in [nodes[did]['name']+'·工作间',nodes[did]['name']+'·侧室'],rid+'-distinct-place-name')
   check(bool(s['observable'].strip()) and bool(s['interaction'].strip()),rid+'-object-and-executable-use-recorded')
   check(s['egress']==[did] and [did,rid] in c['local_edges'],rid+'-independent-return-to-district')
   check(s['quests'] and all(qid in qs for qid in s['quests']),rid+'-known-related-tasks')
   check(rid in (V/c['space_file']).read_text(encoding='utf-8'),rid+'-documented-room')
 for i,qid in enumerate(c['side_ids']):
  q=qs[qid];placements+=1;first,last=p['district_assignments'][cid][i];si=p['satellite_assignments'][cid][i]
  expected=[f'{cid}-D{first:02}',f'{cid}-S{si:02}-3',f'{cid}-D{last:02}']
  check(q['locations']==expected,qid+'-explicit-three-scene-assignment')
  sat=next(s for s in c['satellites'] if s['id']==q['satellite'])
  check(qid in sat['quests'] and sat['id']==f'{cid}-S{si:02}',qid+'-correct-satellite-backlink')
 for sat in c['satellites']:
  check(set(sat['quests'])=={q['id'] for q in qs.values() if q.get('satellite')==sat['id']},sat['id']+'-no-stale-task-association')
  check(sat['id'] in village_profiles,sat['id']+'-independent-authored-profile')
  r=sat['resident'];residents.append(r['id']);village_scenes.append(nodes[sat['id']+'-3']['name'])
  check(r['id']==sat['id']+'-NPC' and (V/r['file']).exists(),sat['id']+'-stable-resident-identity-and-card')
  card=(V/r['file']).read_text(encoding='utf-8');check('\nid: '+r['id']+'\n' in card,sat['id']+'-card-id-matches-model')
  check('先把人当作接收名单' not in r['arc'] and all(r.get(k) for k in ['name','role','arc','line']),sat['id']+'-replaced-generic-resident-arc')
  check(bool(sat['space']['layout']) and bool(sat['space']['observable']) and bool(sat['space']['interaction']),sat['id']+'-independent-life-scene')
  check('[['+Path(sat['file']).stem+']]' in card and '[['+Path(r['file']).stem+']]' in (V/sat['file']).read_text(encoding='utf-8'),sat['id']+'-mutual-person-place-links')
 for q in [q for q in m['quests'] if q['city']==cid]:
  for key in ['routes','requires','title','need','turn','kind','file']:
   check(q[key]==oq[q['id']][key],q['id']+'-'+key+'-preserved')
  for before,now in zip(oq[q['id']]['stages'],q['stages']):check(before[1:]==now[1:],q['id']+'-scene-content-preserved')
  check(len(q['scene_spaces'])==len(q['stages']),q['id']+'-all-scenes-with-space-options')
  for scene in q['scene_spaces']:
   check(scene['location'] in nodes and all(rid in nodes for rid in scene['candidates']),q['id']+'-scene-options-exist')
  text=(V/q['file']).read_text(encoding='utf-8');check('[['+Path(c['space_file']).stem+']]' in text,q['id']+'-space-reference')
check(placements==58 and len(room_names)==132,'58-explicit-placements-and-132-interiors')
check(len(set(room_names))==132,'132-distinct-room-names')
check(len(set(residents))==33 and len(set(village_scenes))==33,'33-unique-residents-and-life-scenes')
# Hand-authored thematic anchors catch known real mismatches, beyond checking the generator against its own table.
anchors={'CS-ALD-01':'白缝村','CS-ALD-02':'石礼驿','CS-MNS-01':'桶石驿','CS-YOS-01':'羊坡村','CS-YOS-02':'缓梭镇',
 'CS-KOR-01':'留灯驿','CS-KOR-02':'双门里','CS-KOR-03':'留灯驿','CS-RAT-03':'静铃驿','CS-PAS-01':'石角驿','CS-ASH-03':'冷苇集','CS-MAE-03':'根灯镇'}
for qid,name in anchors.items():check(qs[qid]['stages'][1][0]==name,qid+'-authored-thematic-anchor-'+name)
for fname in ['city-space-note-hashes.json','city-generated-note-hashes.json']:
 for rel,h in read(ROOT/'research'/fname).items():check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S75 spatial design, authored placement anchors, safe intended egress and preserved quest models; not collision, art quality, literary quality, economy or runtime',
 regions=15,districts=66,interiors=132,satellite_residents=len(residents),satellite_scenes=len(village_scenes),explicit_side_placements=placements,checks_passed=len(checks),errors=errors,passed=not errors)
(ROOT/'research/city-space-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False));raise SystemExit(1 if errors else 0)
