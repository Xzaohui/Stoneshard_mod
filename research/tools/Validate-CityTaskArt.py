"""Validate actual saved PNGs, provenance, existing task/space mappings and bidirectional links."""
from pathlib import Path
from PIL import Image
import json,hashlib,re,os
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
m=load('research/city-task-art-20261012.json');model=load('research/city-campaign.json');qs={q['id']:q for q in model['quests']};cs={c['id']:c for c in model['cities']}
checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
check(m['status']=='draft' and m['canon']=='mod-original' and m['runtimeVerified'] is False,'draft-art-scope')
check({b['id'] for b in m['boards']}=={'SKO','YOS'} and len(m['boards'])==2,'two-unique-boards')
associated=set()
for b in m['boards']:
 cid=b['id'];c=cs[cid];out=(ROOT/b['selected']).resolve();note=ROOT/b['note'];text=note.read_text(encoding='utf-8-sig')
 check(out.is_relative_to(V/'12_美术参考/城市概念') and sha(out)==b['sha256'],cid+'-saved-selected-hash')
 with Image.open(out) as im:
  check(im.format=='PNG' and im.width>=1000 and im.width>im.height and list(im.size)==b['dimensions'],cid+'-readable-landscape-png');im.verify()
 check(bool(b['review']) and 'status: draft' in text,cid+'-manual-review-and-draft-note')
 for ref in b['references']:check(sha(ROOT/ref['path'])==ref['sha256'],cid+'-unchanged-reference-'+Path(ref['path']).name)
 for p in b['prompts']:
  check(sha(ROOT/p['path'])==p['sha256'] and len((ROOT/p['path']).read_text(encoding='utf-8'))>400,cid+'-full-prompt-'+Path(p['path']).name)
 if b.get('previous'):
  check(sha(ROOT/b['previous']['path'])==b['previous']['sha256'] and b['actual_edit_reference']==b['previous'],cid+'-prior-candidate-preserved-and-edit-input')
 # These fingerprints describe generation time. Later authored dialogue may advance
 # legitimately; current associations below must still resolve to real tasks/nodes.
 check(bool(re.fullmatch('[a-f0-9]{64}',b['generation_baseline']['city_model_sha256'])),cid+'-generation-time-model-fingerprint')
 check(bool(re.fullmatch('[a-f0-9]{64}',b['generation_baseline']['dialogue_draft_sha256'])) and (ROOT/b['generation_baseline']['dialogue_draft_source']).exists(),cid+'-generation-time-dialogue-fingerprint-and-source')
 check([p['label'] for p in b['panels']]==list('ABCDEF'),cid+'-six-ordered-labels')
 nodes={n['id'] for n in c['nodes']}
 for panel in b['panels']:
  check(panel['space'] in nodes and '`'+panel['space']+'`' in text,cid+'-'+panel['label']+'-real-planned-node')
  for qid in panel['quests']:
   check(qid in qs and qs[qid]['city']==cid and '[['+Path(qs[qid]['file']).stem+']]' in text,cid+'-'+panel['label']+'-'+qid+'-valid-task-link');associated.add(qid)
 for rel in b['linked_notes']:
  p=ROOT/rel;t=p.read_text(encoding='utf-8-sig');expected=Path(os.path.relpath(out,p.parent)).as_posix()
  check(t.count('<!-- CITY-TASK-ART-20261012:BEGIN -->')==1 and '('+expected+')' in t and '[['+note.stem+']]' in t,rel+'-one-image-block-and-backlink')
 check('research/city-task-art-20261012.json' in text,cid+'-provenance-link')
check(len(associated)==8,'eight-existing-tasks-associated')
for rel in ['design/12_美术参考/原素材参考与城市概念图.md','design/12_美术参考/城市美术与图片目录.md','design/00_导航/城市与聚落设计总索引.md']:
 text=(ROOT/rel).read_text(encoding='utf-8-sig');check(all('[['+Path(b['note']).stem+']]' in text for b in m['boards']),rel+'-discoverable-both-boards')
report=dict(date='2026-10-12',scope='saved artwork, provenance and existing Obsidian links; no collision or game-runtime verification',boards=2,panels=12,associated_tasks=8,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/city-task-art-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False));raise SystemExit(1 if errors else 0)
