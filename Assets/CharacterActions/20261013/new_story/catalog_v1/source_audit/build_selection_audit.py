#!/usr/bin/env python3
"""Read-only final-selection audit. Does not alter source artwork or prior catalogs."""
import json,hashlib,re,argparse
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
BASE=ROOT/'Assets/CharacterActions/20261013/new_story'
OLD=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story/catalog_v1/source_audit/selection_audit.json'
AUD=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
MISSING={'turi':'A1','cuoer':'A1','weier':'A1','lier':'A1'}
LAST={'weier_ink','moer','daier','moer_trs'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def info(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}
def resolve(s,parent):
 p=Path(s)
 if p.is_absolute():return p
 return ROOT/p if s.startswith('Assets/') else parent/p
def walk(x,ptr=''):
 yield ptr,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,ptr+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,ptr+'/'+str(i))
def normalize(v,parent):
 if 'transparent' in v and isinstance(v['transparent'],dict): q=v['transparent']; path=q['path'];h=q['sha256']
 else:
  path=next((v[k] for k in ['selected_path','transparent_path','transparent_file','path','selected'] if isinstance(v.get(k),str) and v[k].endswith('.png')),None)
  h=next((v[k] for k in ['selected_sha256','transparent_sha256','sha256'] if v.get(k)),None)
 assert path and h,(parent,v)
 p=resolve(path,parent); assert p.is_file(),p
 assert '/raw/' not in str(p) and ('/selected/' in str(p) or '/exports/' in str(p)),p
 assert sha(p)==h,(p,h,sha(p))
 return {'path':str(p.relative_to(ROOT)),'sha256':h,'key':v.get('key') or v.get('stem') or p.stem,'label_zh':v.get('title_zh') or v.get('label_zh') or '', 'selected_record':v}
def select(parent):
 final=read(parent/'FINAL_STATUS.json'); manifest=read(parent/'manifest.json')
 for k in ['final_selection','active_selected','selected_assets','selected']:
  if final.get(k) and isinstance(final[k],list) and isinstance(final[k][0],dict):return [normalize(v,parent) for v in final[k]],k
 if 'selected_file' in final:return [normalize({'path':final['selected_file'],'sha256':final['selected_sha256'],'key':final['selected_key']},parent)],'selected_file'
 for k in ['selected','selected_stems']:
  if final.get(k) and isinstance(final[k][0],str):
   stems=set(final[k]); values=[v for v in manifest.get('attempts',manifest.get('selected',[])) if isinstance(v,dict) and v.get('stem') in stems]
   assert len(values)==len(stems),(parent,stems)
   return [normalize(v,parent) for v in values],k+' + manifest'
 values=[v for v in manifest['files'] if v['path'].startswith('selected/') and v['path'].endswith('.png')]
 assert len(values)==final['selected_count']==2,parent
 return [normalize(v,parent) for v in values],'FINAL selected_count + manifest /files selected/'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--include-eleventh',action='store_true');a=ap.parse_args()
 old=read(OLD); chars=old['characters']; assert len({c['slug'] for c in chars})==len({c['canonical_id'] for c in chars})==44; assets=[]; details=[]; evidence_cache={}
 # Only original, top-level independent action QA records, not replicated source snapshots.
 for p in sorted(AUD.glob('*actions*.json')):
  if 'independent' in p.name:
   try:evidence_cache[p]=(p.read_text(),read(p))
   except Exception:pass
 for c in chars:
  slug=c['slug']; mother=next(x.copy() for x in old['assets'] if x['slug']==slug and x['kind']=='concept')
  p=ROOT/mother['path'];assert sha(p)==mother['sha256'],p
  mother.pop('expression_id',None);mother['action_id']='BASE';mother['evidence']['prior_catalog_audit']=info(OLD)
  assets.append(mother)
  if slug in LAST and not a.include_eleventh:continue
  parent=BASE/slug/'noncombat_basics_v1';rows,selection_basis=select(parent)
  expected=1 if slug in MISSING else 2;assert len(rows)==expected,(slug,len(rows))
  finalp=parent/'FINAL_STATUS.json';manp=parent/'manifest.json'
  # A hash must bind the actual transparent file in at least one independent QA record.
  local={}
  for p in list(parent.glob('*independent*.json'))+list(parent.glob('review/*independent*.json'))+list(parent.glob('review/independent/*.json')):
   try:local[p]=(p.read_text(),read(p))
   except Exception:pass
  docs={**evidence_cache,**local}
  mother_matches=[]
  for p in [parent/'manifest.json',parent/'spec_lock.json',parent/'source_hashes.json',parent/'source_index.json',parent/'production_brief.json']+list((parent/'prompts').glob('*spec_lock.json')):
   if p.exists() and mother['sha256'] in p.read_text():mother_matches.append(info(p))
  # fallback nested sources are a provenance snapshot; never considered action selection.
  if not mother_matches:
   for p in (parent/'sources').glob('*.json'):
    if mother['sha256'] in p.read_text():mother_matches.append(info(p))
  assert mother_matches,('missing mother binding',slug)
  charinfo={'slug':slug,'canonical_id':c['canonical_id'],'selection_basis':selection_basis,'final_status':info(finalp),'manifest':info(manp),'mother_binding':mother_matches,'action_keys':[]}
  for r in rows:
   aid=re.search(r'_A([12])(?:_|$)',r['key']);assert aid,r
   aid='A'+aid[1];assert not(slug in MISSING and aid=='A1')
   p=ROOT/r['path'];im=Image.open(p);assert im.mode=='RGBA'
   hits=[]
   for ep,(txt,d) in docs.items():
    if r['sha256'] in txt:
     pointers=[ptr for ptr,v in walk(d) if isinstance(v,str) and v==r['sha256']]
     hits.append({**info(ep),'matching_sha_pointers':pointers})
   assert hits,('missing independent hash binding',slug,aid,r['path'])
   asset={'asset_id':slug+'_'+aid,'slug':slug,'canonical_id':c['canonical_id'],'name':c['name'],'kind':'action','action_id':aid,'label_zh':r['label_zh'],'path':r['path'],'sha256':r['sha256'],'bytes':p.stat().st_size,'width':im.width,'height':im.height,'mode':im.mode,'source_key':r['key'],'selected_record':r['selected_record'],'evidence':{'final_status':info(finalp),'author_manifest':info(manp),'selection_basis':selection_basis,'independent_review':hits}}
   assets.append(asset);charinfo['action_keys'].append(asset['asset_id'])
  details.append(charinfo)
 assert len({x['asset_id'] for x in assets})==len(assets)
 assert len({x['path'] for x in assets})==len(assets)
 assert len({x['sha256'] for x in assets})==len(assets)
 handoff=None
 if a.include_eleventh:
  hp=AUD/'eleventh_actions_independent_details/final_selected_catalog_handoff.json'; hd=read(hp)
  assert hd['status']=='all_eight_final_frozen_and_independently_passed'
  assert len(hd['files'])==8
  for v in hd['files']:
   found=[x for x in assets if x['kind']=='action' and x['path']==v['path'] and x['sha256']==v['sha256']]
   assert len(found)==1,v
   for field in ['character_final_status','group_package_gate','group_freeze']:
    proof=v[field]; assert sha(ROOT/proof['path'])==proof['sha256'],proof
   found[0]['evidence']['eleventh_frozen_package_handoff']=v
  handoff=info(hp)
 counts={'characters':len(chars),'base_images':44,'qualified_actions':len(assets)-44,'selected_images':len(assets),'missing_actions':4}
 if a.include_eleventh:assert counts['selected_images']==128
 else:assert counts['selected_images']==120
 data={'schema_version':1,'audited_utc':datetime.now(timezone.utc).isoformat(),'scope':'Final selected transparent images only; missing A1 slots never draw failed raw; no expressions. Approval/review is not user style approval or runtime validation.','final':a.include_eleventh,'eleventh_final_frozen_handoff':handoff,'counts':counts,'missing_actions':[{'slug':s,'action_id':v} for s,v in MISSING.items()],'characters':chars,'assets':assets,'character_selection_evidence':details,'roster':old['roster'],'prior_mother_selection_audit':info(OLD),'action_delivery_index':info(BASE/'ACTION_DELIVERY_INDEX.md'),'no_duplicate_paths_ids_or_image_sha':True}
 save(HERE/('selection_audit.json' if a.include_eleventh else 'selection_audit_first40.json'),data)
 print(json.dumps(counts)); print('Missing label:',[(x['asset_id'],x['source_key']) for x in assets if x['kind']=='action' and not x['label_zh']])
if __name__=='__main__':main()
