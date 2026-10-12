"""Static S63 coverage and limited-receipt reference model, not game validation."""
from pathlib import Path
import json,hashlib,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'))
cs={c['id']:c for c in m['cities']};qs={q['id']:q for q in m['quests']};errs=[];checks=[];scenarios=[]
def check(ok,label):
 (checks if ok else errs).append(label)
def connected(ids,edges,start):
 reached={start}
 while True:
  old=len(reached)
  for a,b in edges:
   if a in reached:reached.add(b)
   if b in reached:reached.add(a)
  if len(reached)==old:return ids<=reached
check(set(cs)==set('BRY ALD MAE OSB MNS DEN SKO YOS KOR EED FOR RAT PAS ASH HIG'.split()),'all-12-named-plus-3-original')
check(len(qs)==73 and len(m['quests'])==73,'73-unique-chapters')
check(len(m['effects'])==len({e['id'] for e in m['effects']}),'unique-effect-identifiers')
check(connected(set(cs),m['travel'],'OSB'),'planned-transport-reaches-all-regions')
check(sum(len(c['satellites']) for c in cs.values())==33,'33-satellite-settlements')
check(sum(len(c['nodes']) for c in cs.values())==297,'297-planned-functional-nodes-not-rooms')
for c in cs.values():
 check((V/c['file']).exists(),c['id']+'-city-note')
 check(len(c['side_ids'])==(10 if c['id']=='BRY' else 6 if c['id'] in ['ALD','MAE'] else 3),c['id']+'-density')
 check(c['main_id'] in qs,c['id']+'-regional-main')
 ids={n['id'] for n in c['nodes']}
 check(len(ids)==len(c['nodes']),c['id']+'-unique-node-ids')
 check(all(set(e)<=ids for e in c['local_edges']),c['id']+'-local-edge-targets')
 check(connected(ids,c['local_edges'],c['id']+'-D01'),c['id']+'-all-interiors-and-satellites-return')
 check((V/c['map']).exists(),c['id']+'-map-asset')
 check(set(x['node'] for x in qs[c['main_id']]['location_work'])=={n['id'] for n in c['nodes'] if n['kind']=='district'},c['id']+'-district-plot-purpose')
 for s in c['satellites']:
  check(bool(s['quests']),s['id']+'-own-story-scene')
  check((V/s['file']).exists() and (V/s['map']).exists(),s['id']+'-note-and-picture')
  for qid in s['quests']:
   check(qs[qid]['satellite']==s['id'] and s['id']+'-3' in qs[qid]['locations'],s['id']+'-'+qid+'-scene-owned')
  check(wl:=Path(c['file']).stem in (V/s['file']).read_text(encoding='utf-8'),s['id']+'-backlink')
 for direction in ['source','target']:
  check(any(e['id'].startswith('CX') and e[direction] in qs and qs[e[direction]]['city']==c['id'] for e in m['effects']),c['id']+'-cross-city-'+direction)
for q in qs.values():
 c=cs[q['city']];text=(V/q['file']).read_text(encoding='utf-8');ids={n['id'] for n in c['nodes']}
 check(len(q['stages'])==len(q['locations'])>=3,q['id']+'-scene-coverage')
 check(all(n in ids for n in q['locations']),q['id']+'-real-planned-locations')
 check(len(q['routes'])>=2,q['id']+'-multiple-methods')
 check(len({r['key'] for r in q['routes']})==len(q['routes']),q['id']+'-exclusive-method-ids')
 check(len({r['action'] for r in q['routes']})==len(q['routes']),q['id']+'-distinct-action-text')
 for r in q['routes']:
  check(all(r.get(k) for k in ['key','label','action','cost','result','line']),q['id']+'-'+r['key']+'-action-cost-result-return')
 check(all(x in text for x in ['中断','死亡优先','不同到达顺序','关闭均不写','不复制唯一奖励']),q['id']+'-lifecycle-contract')
 check(bool([e for e in m['effects'] if e['source']==q['id']]) and bool([e for e in m['effects'] if e['target']==q['id']]),q['id']+'-incoming-outgoing')
 for r in q['requires']:check(r in qs or r in m['legacy_home'],q['id']+'-prerequisite-target')
for e in m['effects']:
 check(e['source'] in qs or e['source'] in m['legacy_home'],e['id']+'-source')
 check(e['target'] in qs or e['target'] in m['legacy_home'],e['id']+'-target')
 if e['source'] in qs:check(e['route'] in [r['key'] for r in qs[e['source']]['routes']],e['id']+'-source-method')
 check(len(e['guards'])==4 and e['line'] and e['change'] and e['receipt'],e['id']+'-scoped-response')
 check('不改' in e['timing'] and '不重复' in e['reward'],e['id']+'-late-and-reward-bounds')
check(len(m['legacy_home'])==51,'all-51-legacy-screenplays-mapped')
for p in (V/'12_美术参考/城市示意').glob('*.svg'):
 try:ET.parse(p);check(True,p.stem+'-valid-svg')
 except ET.ParseError:check(False,p.stem+'-valid-svg')

class Ledger:
 def __init__(self):self.resolve={};self.receipts={};self.alive=True;self.present=True;self.allowed=True;self.confirmed=set();self.target_done=False;self.history=[];self.ending='sealed';self.once=set()
 def execute(self,qid,route,confirmed=False):
  if not confirmed:return False
  if qid in self.resolve:return False
  self.resolve[qid]=route;self.confirmed.add(qid);self.history.append((qid,route));return True
 def grant(self,e):
  if e['source'] in self.confirmed and self.resolve[e['source']]==e['route'] and self.allowed:self.receipts[e['id']]=e['receipt'];return True
  return False
 def receive(self,e):
  if not(self.alive and self.present and self.allowed and self.receipts.get(e['id'])==e['receipt']):return None
  return {'line':e['line'],'change':e['change'] if not self.target_done else '回访：'+e['change'],'ending':self.ending}
 def reward(self,qid):
  if qid not in self.confirmed or qid in self.once:return False
  self.once.add(qid);return True

# Exercise every cross-city method and denial condition; this evaluator is independent of the renderer.
for e in [e for e in m['effects'] if e['id'].startswith('CX')]:
 l=Ledger();check(not l.execute(e['source'],e['route']) and not l.resolve,e['id']+'-preview-does-not-write')
 check(not l.grant(e) and l.receive(e) is None,e['id']+'-no-unearned-receipt')
 check(l.execute(e['source'],e['route'],True) and l.grant(e),e['id']+'-actual-execution-produces-limited-receipt')
 check(l.receive(e)['line']==e['line'],e['id']+'-specific-response')
 for field in ['alive','present','allowed']:
  setattr(l,field,False);check(l.receive(e) is None,e['id']+'-'+field+'-denial');setattr(l,field,True)
 check(l.reward(e['source']) and not l.reward(e['source']),e['id']+'-unique-reward')
 l.target_done=True;before=list(l.history);r=l.receive(e)
 check(r and r['change'].startswith('回访') and l.history==before and r['ending']=='sealed',e['id']+'-late-arrival-does-not-retcon-or-unseal')
 check(not l.execute(e['source'],'other',True),e['id']+'-no-reselect-after-resolution')
 scenarios.append(dict(effect=e['id'],source=e['source'],target=e['target'],validated=['preview','actual-receipt','death','absence','refusal','reward-once','late-arrival','ending-freeze']))

hashes=json.loads((ROOT/'research/city-generated-note-hashes.json').read_text(encoding='utf-8'))
for rel,h in hashes.items():check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
for p in V.rglob('*.md'):
 text=p.read_text(encoding='utf-8-sig')
 for raw in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
  if not raw.startswith(('http:','https:','data:')):check((p.parent/raw).resolve().exists(),str(p.relative_to(V))+'-embedded-image')
report=dict(date='2026-10-12',scope='S63 static document topology and reference receipt evaluator; not literary quality, economy or game runtime',
 cities=len(cs),satellites=33,quests=len(qs),effects=len(m['effects']),nodes=297,checks_passed=len(checks),scenarios=scenarios,errors=errs,passed=not errs)
(ROOT/'research/city-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='scenarios'},ensure_ascii=False));raise SystemExit(1 if errs else 0)
