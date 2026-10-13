from pathlib import Path
from PIL import Image
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch47/177_trade_liqui_cast.png'
card=R/'design/04_人物/城市人物/人物_TRADE-NPC-LIQUI_莉葵.md'
meta=R/'Assets/ReferenceAudit/20261013/original-reference-metadata.json'
refs=[r for r in json.loads(meta.read_text())['references'] if r['name'] in ['Frid','Bert','Jurg','Gunda']]
inputs=[old,card,meta,R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch47/manifest.json',R/'Assets/ReferenceAudit/20261013/character_redraw_triage.json',R/'Assets/ReferenceAudit/20261013/character_native_refs_contact.png']+[R/r['path'] for r in refs]
x={'date':'2026-10-13','character_id':'TRADE-NPC-LIQUI','coverage':['CHAR-TRADE-NPC-LIQUI'],'pose':'one neutral front stance','status':'structure-study-candidate','generated_with':'built-in image_gen, two calls','generation_inputs':{'v1':['old 177','Frid/Bert/Jurg nearest contact','Gunda native'],'v2':['concept v1','Frid/Bert/Jurg nearest contact','Gunda native']},'new_identity_count':0,'narrative_changes':False,'style_pass':False,'native_production_pass':False,'runtimeVerified':False,'global_indexes_modified':False,'sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in inputs],'native_reference_metadata':refs,'old_image_unchanged':sha(old)=='34b9c159bd0539a0f4977d1eb3db7e7fda99c53fe51783ae85d903d9386e7dfe','candidate':{'canvas':[35,44],'visible_bbox':[8,4,28,38],'visible_size':[20,34],'nontransparent_colors':18,'pixel_edits':len(json.loads((D/'pixel_edit_log.json').read_text())['edits']),'not_engine_standard':True},'actual_review':['old 177 full sheet','Frid/Bert/Jurg native contact','Gunda native and 10x nearest','concept v1','concept v2','pre-edit native','post-edit 16x nearest','same-scale four NPC comparison','old/concept/native comparison'],'outputs':[]}
for p in sorted(D.iterdir()):
 if p.is_file() and p.name!='manifest.json':
  o={'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size}
  if p.suffix=='.png':
   im=Image.open(p);o.update(size=list(im.size),mode=im.mode)
  if 'comparison' in p.name or 'gunda' in p.name:o['classification']='comparison only; includes copyrighted references, exclude from original generated counts'
  x['outputs'].append(o)
(D/'manifest.json').write_text(json.dumps(x,ensure_ascii=False,indent=2))
print(json.dumps({'old_image_unchanged':x['old_image_unchanged'],'outputs':len(x['outputs']),'native_sha256':sha(D/'liqui_native_v1.png')},indent=2))
