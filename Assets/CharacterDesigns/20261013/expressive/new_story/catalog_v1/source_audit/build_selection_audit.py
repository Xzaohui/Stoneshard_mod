from pathlib import Path
import json,re,hashlib,datetime
from PIL import Image
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
B=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story'
A=B.parent/'new_story_audit'
OUT=B/'catalog_v1/source_audit'
cache={}
def read(p):
 p=Path(p)
 if p not in cache:cache[p]=json.loads(p.read_text())
 return cache[p]
def rel(p):return str(Path(p).resolve().relative_to(ROOT))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ev(p,pointer=None):
 x={'path':rel(p),'sha256':sha(p)}
 if pointer is not None:x['json_pointer']=pointer
 return x
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def strings(x):return [(p,v) for p,v in walk(x) if isinstance(v,str)]
def contains_hash(x,h):return [p for p,v in strings(x) if v.lower()==h.lower()]
def resolve(s,base):
 p=Path(s)
 if p.is_absolute():return p
 if s.startswith('Assets/') or s.startswith('design/'):return ROOT/p
 return base/p
def file_record(p):
 p=Path(p);d={'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size}
 return d
roster_path=A/'new_characters_44.json';roster=read(roster_path)['characters'];roster_ids={x['canonical_id']:x for x in roster}
briefs={}
for p in sorted(A.glob('*expression_brief.json')):
 for i,c in enumerate(read(p).get('characters',[])):
  if isinstance(c,dict) and c.get('slug'):briefs[c['slug']]=(p,c,f'/characters/{i}')
# Sources are explicit links in the delivery index, never inferred from directory naming.
idx=B/'EXPRESSION_DELIVERY_INDEX.md';idxtext=idx.read_text();packages=[]
for section in re.split(r'^## ',idxtext,flags=re.M)[1:]:
 title=section.splitlines()[0]
 refs=[(label,(B/link).resolve()) for label,link in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',section)]
 if not refs:continue
 receipt=[p for label,p in refs if p.name=='DELIVERY_RECEIPT.json'][0]
 manifest=refs[0][1];r=read(receipt)
 qa=[p for label,p in refs if ('QA' in label or '独审' in label) and p!=receipt]
 packages.append({'id':manifest.parent.name,'title':title,'manifest':ev(manifest),'receipt':ev(receipt),'review_evidence':[ev(p) for p in qa], 'message_id':r.get('message_id'),'status':r.get('status'),'sent_at':r.get('sent_at') or r.get('sent_utc'), '_manifest_path':manifest,'_receipt_path':receipt,'_qa_paths':qa})
assert len(packages)==22,len(packages)
# Read concept packages for mother delivery verification, only existing receipts establish delivery.
concept_packages=[]
for p in sorted(B.glob('*four_delivery_v1/DELIVERY_RECEIPT.json')):
 if 'expressions' in p.parent.name:continue
 docs=[p]+list(p.parent.glob('delivery.json'))+list(p.parent.glob('*independent*.json'))+list(p.parent.glob('FINAL_STATUS.json'))
 concept_packages.append((p,docs))
assets=[];chars=[];issues=[];gaps=[]
for mp in sorted(B.glob('*/expressions_v1/manifest.json')):
 slug=mp.parent.parent.name;ed=mp.parent;m=read(mp);cm=ed.parent/'concept_v1/manifest.json';cd=read(cm)
 bp,brief,bptr=briefs[slug]
 cid=m.get('canonical_id') or cd.get('canonical_id') or brief['canonical_id']
 assert cid==brief['canonical_id'] and cid in roster_ids,(slug,cid)
 name=roster_ids[cid]['name']
 fs=ed/'FINAL_STATUS.json';status=read(fs)
 qas=sorted(ed.glob('QA-independent*.json'))
 final_qa=[p for p in qas if 'raw' not in p.name.lower()]
 assert final_qa,(slug,'no final independent qa')
 sel_key=next(k for k in ['selected','selected_bindings','expressions','assets'] if k in m)
 sel=m[sel_key];assert isinstance(sel,list)
 selected=[]
 for i,x in enumerate(sel):
  sp=x.get('selected') or x.get('selected_path') or x.get('path');assert isinstance(sp,str),(slug,x)
  img=resolve(sp,ed);actual=sha(img);declared=x.get('selected_sha256') or x.get('sha256')
  assert declared==actual,(slug,sp,'sha mismatch')
  eid=x.get('expression_id') or x.get('expression') or x.get('id')
  if eid not in ['E1','E2']:eid=re.search(r'_E([12])_',img.name).group(0)[1:-1]
  label=x.get('label_zh') or x.get('label');label_ev=ev(mp,f'/{sel_key}/{i}')
  if not label:
   expr=brief.get('expressions',[])
   if isinstance(expr,dict):expr=list(expr.values())
   opts=[]
   for j,z in enumerate(expr):
    if not isinstance(z,dict):continue
    zs=json.dumps(z,ensure_ascii=False)
    if (z.get('id')==eid or z.get('expression_id')==eid or z.get('expression')==eid or f'_{eid}_' in zs):
     l=z.get('label_zh') or z.get('label') or z.get('name_zh')
     if l:opts.append((l,j))
   if len(opts)==1:label,j=opts[0];label_ev=ev(bp,bptr+f'/expressions/{j}')
   else:issues.append({'slug':slug,'expression_id':eid,'problem':'label unresolved','options':opts})
  matches=[]
  for pack in packages:
   ps=pack['_manifest_path'];pp=pack['_receipt_path']
   mh=contains_hash(read(ps),actual);rh=contains_hash(read(pp),actual)
   if mh or rh:
    matches.append((pack,mh,rh))
  assert len(matches)==1,(slug,eid,[(p['id'],mh,rh) for p,mh,rh in matches])
  pack,mh,rh=matches[0]
  qa_matches=[]
  for q in final_qa:
   for pt in contains_hash(read(q),actual):qa_matches.append(ev(q,pt))
  if not qa_matches:issues.append({'slug':slug,'expression_id':eid,'problem':'final character QA lacks selected SHA literal; review linkage retained'})
  fsh=contains_hash(status,sha(mp))
  if not fsh:issues.append({'slug':slug,'problem':'final status lacks current manifest SHA literal'})
  evidence={'selection_manifest':ev(mp,f'/{sel_key}/{i}'),'final_status':ev(fs),'independent_review':qa_matches or [ev(q) for q in final_qa], 'delivery_manifest':ev(pack['_manifest_path']), 'delivery_receipt':ev(pack['_receipt_path']), 'delivery_review':pack['review_evidence'],'label':label_ev,'delivery_asset_sha_pointers':mh,'receipt_asset_sha_pointers':rh}
  with Image.open(img) as im:props={'width':im.width,'height':im.height,'mode':im.mode}
  asset={'asset_id':f'{slug}_{eid}','slug':slug,'canonical_id':cid,'name':name,'kind':'expression','expression_id':eid,'label_zh':label,**file_record(img),**props,'documented_sha256':declared,'sha256_matches':True,'package_id':pack['id'],'delivery_message_id':pack['message_id'],'evidence':evidence}
  assets.append(asset);selected.append(asset['asset_id'])
 # Bind mother from expression manifest first, then final review, then frozen character brief.
 candidates=[]
 docs=[(mp,m,'expression_manifest')]+[(q,read(q),'expression_independent_review') for q in final_qa]+[(ed/fn,read(ed/fn),'expression_brief') for fn in ['brief.json','character_brief.json','brief-character.json'] if (ed/fn).exists()]+[(bp,brief,'expression_batch_brief')]
 for dp,doc,source_kind in docs:
  for pointer,node in walk(doc):
   if not isinstance(node,dict):continue
   for k,v in node.items():
    if not isinstance(v,str) or not v.endswith('.png') or Path(v).name!=f'{slug}_transparent.png' or f'/{slug}/concept_v1/' not in v or 'expressions_v1' in v or v.startswith('sources/'):continue
    mother=resolve(v,dp.parent)
    h=node.get('sha256') or node.get(k+'_sha256')
    if not h:continue
    if mother.exists():candidates.append((mother,h,dp,pointer+'/'+k,source_kind))
  if candidates:break
 assert candidates,(slug,'no explicitly bound mother')
 uniq={(str(p),h) for p,h,dp,ptr,k in candidates};assert len(uniq)==1,(slug,'ambiguous mothers',uniq)
 mother,decl,bind_doc,bind_ptr,bind_kind=candidates[0];bind_ptr=(bptr+bind_ptr if bind_kind=='expression_batch_brief' else bind_ptr);assert sha(mother)==decl,(slug,'mother hash')
 # Cross-check concept selection, not an arbitrary concept PNG.
 declared_trans=cd.get('selected_transparent') or cd.get('transparent')
 if isinstance(declared_trans,dict):declared_trans=declared_trans.get('path')
 assert declared_trans and resolve(declared_trans,cm.parent).resolve()==mother.resolve(),(slug,'concept selected mismatch',declared_trans,mother)
 ch=contains_hash(cd,decl);assert ch,(slug,'concept manifest lacks actual mother SHA')
 concept_qa_paths=sorted(set(list(cm.parent.glob('*independent*.json'))+list(cm.parent.glob('*QA*.json'))))
 # Global concept independent QA has authoritative complete review for all batches.
 concept_qa_paths+=sorted(A.glob('independent_visual_qa_*four_20261013.json'))
 mother_qa=[(q,pt) for q in concept_qa_paths for pt in contains_hash(read(q),decl)]
 mother_del=[]
 for rp,dps in concept_packages:
  for dp in dps:
   for pt in contains_hash(read(dp),decl):mother_del.append((rp,dp,pt))
 if not mother_qa:issues.append({'slug':slug,'problem':'mother independent review lacks actual SHA literal'})
 if not mother_del:issues.append({'slug':slug,'problem':'mother original delivery lacks actual SHA literal'})
 with Image.open(mother) as im:props={'width':im.width,'height':im.height,'mode':im.mode}
 evidence={'expression_mother_binding':ev(bind_doc,bind_ptr),'binding_type':bind_kind,'concept_selection_manifest':ev(cm),'concept_selection_field': 'selected_transparent' if 'selected_transparent' in cd else 'transparent','concept_sha_pointers':ch,'independent_review':[ev(q,pt) for q,pt in mother_qa],'original_delivery':[{'receipt':ev(rp),'matching_document':ev(dp,pt)} for rp,dp,pt in mother_del]}
 assets.append({'asset_id':f'{slug}_base','slug':slug,'canonical_id':cid,'name':name,'kind':'concept','expression_id':'BASE','label_zh':'基础母图',**file_record(mother),**props,'documented_sha256':decl,'sha256_matches':True,'selected_raw':cd.get('selected_raw'),'evidence':evidence})
 chars.append({'slug':slug,'canonical_id':cid,'name':name,'id':cid,'story_role':roster_ids[cid].get('story_role'),'roster_pointer':f"/characters/{next(i for i,x in enumerate(roster) if x['canonical_id']==cid)}",'base_asset_id':f'{slug}_base','expression_asset_ids':selected,'expression_count':len(sel),'final_status':status.get('status') or status.get('state'), 'final_status_evidence':ev(fs),'expression_brief':ev(bp,bptr)})
 for z in m.get('blocked',[]):gaps.append({'slug':slug,'canonical_id':cid,'name':name,'manifest_evidence':ev(mp,'/blocked'),'blocked_record':z,'final_status_evidence':ev(fs),'excluded_from_assets':True,'retry_performed':False})
# Sort in roster order for stable downstream reading; base then E1/E2.
order={x['canonical_id']:i for i,x in enumerate(roster)}
assets.sort(key=lambda x:(order[x['canonical_id']],x['expression_id']))
chars.sort(key=lambda x:order[x['canonical_id']])
public_packs=[{k:v for k,v in p.items() if not k.startswith('_')} for p in packages]
result={'schema_version':1,'audited_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'只读选稿与来源链核验。未重新生图、改稿、做新视觉验收、上传或运行Git。所有SHA256由当前文件重新计算。','repository_root':str(ROOT),'path_base':'repository_root','roster':ev(roster_path),'expression_delivery_index':ev(idx),'counts':{'characters':len(chars),'base_images':sum(x['kind']=='concept' for x in assets),'qualified_expressions':sum(x['kind']=='expression' for x in assets),'selected_images':len(assets),'expression_packages':len(packages)},'assets':assets,'characters':chars,'expression_packages':public_packs,'excluded_gaps':gaps,'uncertainties':issues,'limits':['历史独审结论按来源保留，本次仅核选择/身份/字节和回执链。','发送回执 sent_accepted_not_read 仅表示发送请求接受，不证明送达或阅读。','原生像素网格、动画连续性、装备兼容与游戏运行未在此验收。']}
assert result['counts']=={'characters':44,'base_images':44,'qualified_expressions':86,'selected_images':130,'expression_packages':22},result['counts']
p=OUT/'selection_audit.json';p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':rel(p),'counts':result['counts'],'uncertainties':issues,'gaps':gaps},ensure_ascii=False,indent=2))
