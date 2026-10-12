"""Check saved DEN/MNS concepts against provenance, existing tasks and Obsidian links."""
from pathlib import Path
from PIL import Image
import json,hashlib,os,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
m=load('research/shore-vine-task-art-20261012.json');model=load('research/city-campaign.json');qs={q['id']:q for q in model['quests']};cs={c['id']:c for c in model['cities']}
checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
check(m['status']=='draft' and m['canon']=='mod-original' and not m['runtimeVerified'],'original-draft-not-runtime')
check({b['id'] for b in m['boards']}=={'DEN','MNS'} and len(m['boards'])==2,'two-unique-boards')
associated=set()
for b in m['boards']:
 cid=b['id'];c=cs[cid];out=ROOT/b['selected'];note=ROOT/b['note'];t=note.read_text(encoding='utf-8-sig')
 check(out.resolve().is_relative_to(V/'12_美术参考/城市概念') and sha(out)==b['sha256'],cid+'-selected-saved-hash')
 with Image.open(out) as im:
  check(im.format=='PNG' and im.width>im.height and im.width>=1000 and list(im.size)==b['dimensions'],cid+'-valid-landscape');im.verify()
 check(bool(b['review']) and 'status: draft' in t and '不是逐格' in t,cid+'-review-and-production-limit')
 prior=b['previous'];check(sha(ROOT/prior['path'])==prior['sha256'] and b['actual_edit_reference']=={k:prior[k] for k in ['path','sha256']},cid+'-v1-preserved-and-edit-input')
 check(b['actual_generation_references']==[r['path'] for r in b['references']],cid+'-exact-generation-input-order')
 for r in b['references']:check(sha(ROOT/r['path'])==r['sha256'],cid+'-reference-'+Path(r['path']).name)
 for p in b['prompts']:check(sha(ROOT/p['path'])==p['sha256'] and len((ROOT/p['path']).read_text(encoding='utf-8'))>400,cid+'-full-prompt-'+Path(p['path']).name)
 baseline=b['generation_baseline']
 check(all(re.fullmatch('[a-f0-9]{64}',baseline[k]) for k in ['city_model_sha256','dialogue_draft_sha256']) and (ROOT/baseline['dialogue_draft_source']).exists(),cid+'-generation-time-fingerprints')
 check([p['label'] for p in b['panels']]==list('ABCDEF'),cid+'-six-panel-labels')
 nodes={n['id']:n for n in c['nodes']}
 for p in b['panels']:
  check(p['space'] in nodes and p['name']==nodes[p['space']]['name'] and '`'+p['space']+'`' in t,cid+'-'+p['label']+'-actual-space-id-and-name')
  for qid in p['quests']:
   check(qid in qs and qs[qid]['city']==cid and '[['+Path(qs[qid]['file']).stem+']]' in t,cid+'-'+p['label']+'-'+qid+'-real-task-link');associated.add(qid)
 for rel in b['linked_notes']:
  p=ROOT/rel;s=p.read_text(encoding='utf-8-sig');image=Path(os.path.relpath(out,p.parent)).as_posix()
  check(s.count('<!-- '+b['link_marker']+':BEGIN -->')==1 and '('+image+')' in s and '[['+note.stem+']]' in s,rel+'-single-embed-and-backlink')
 check(all('[['+Path(x['file']).stem+']]' in t for x in c['satellites']),cid+'-satellite-forward-links')
 check('research/shore-vine-task-art-20261012.json' in t,cid+'-provenance-discoverable')
check(associated=={q['id'] for q in model['quests'] if q['city'] in ['DEN','MNS']},'all-eight-existing-tasks-associated')
for rel in ['design/12_美术参考/原素材参考与城市概念图.md','design/12_美术参考/城市美术与图片目录.md','design/00_导航/城市与聚落设计总索引.md','design/11_管理/丹布里与曼郡人物演出审查.md']:
 t=(ROOT/rel).read_text(encoding='utf-8-sig');check(all('[['+Path(b['note']).stem+']]' in t for b in m['boards']),rel+'-both-art-notes-discoverable')
backup=ROOT/'backups/shore-vine-task-art-20261012'
for rel in ['research/denbrie-drama.json','research/mannshire-drama.json','research/denbrie-feedback.json','research/mannshire-feedback.json','research/city-task-art-20261012.json']:
 check(sha(ROOT/rel)==sha(backup/rel),'unchanged-narrative-and-prior-manifest-'+Path(rel).name)
# The generation-time model fingerprint is historical. New unrelated city
# authoring may legitimately add casts/scenes, while this art's mapped tasks,
# topology, receipts and scoped actors must remain the same as its baseline.
before=json.loads((backup/'research/city-campaign.json').read_text(encoding='utf-8'))
for key in ['effects','rules','travel','verified_runtime']:
 check(model[key]==before[key],'unchanged-art-baseline-'+key)
beforeqs={q['id']:q for q in before['quests']}
for cid in ['DEN','MNS']:
 check(model['dramatic_casts'][cid]==before['dramatic_casts'][cid],cid+'-unchanged-art-cast')
 for q in model['quests']:
  if q['city']==cid:check(q==beforeqs[q['id']],q['id']+'-unchanged-art-task')
old=load('research/city-task-art-20261012.json')
for b in old['boards']:
 for rel in [b['selected'],b.get('previous',{}).get('path')]:
  if rel:check(sha(ROOT/rel)==sha(backup/rel),'prior-selected-and-candidate-'+Path(rel).name)
report=dict(date='2026-10-12',scope='saved concepts, reference/prompt/candidate hashes and task-space links; not proportional map, collision or game runtime',boards=2,panels=12,associated_tasks=8,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/shore-vine-task-art-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(1 if errors else 0)
