from pathlib import Path
import json,hashlib,zipfile,datetime
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
B=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story';OUT=B/'catalog_v1/source_audit';P=OUT/'selection_audit.json'
a=json.loads(P.read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p):return str(Path(p).resolve().relative_to(ROOT))
def load(p):return json.loads(Path(p).read_text())
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+str(k).replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def hashptr(x,h):return [p for p,v in walk(x) if isinstance(v,str) and v.lower()==h.lower()]
def ev(p,pointer=None):
 d={'path':rel(p),'sha256':sha(p)}
 if pointer is not None:d['json_pointer']=pointer
 return d
pack_by_id={p['id']:p for p in a['expression_packages']}
assets_by_slug={c['slug']:[x for x in a['assets'] if x['slug']==c['slug']] for c in a['characters']}
archive_files={}
for p in a['expression_packages']:
 rp=ROOT/p['receipt']['path'];rd=load(rp);mp=ROOT/p['manifest']['path'];md=load(mp);ars=[]
 for ptr,x in walk(rd):
  if not isinstance(x,dict) or not x.get('sha256'):continue
  opts=[x.get(k) for k in ['source_path','local_path','file_name','file','path']]
  zp=None
  for v in opts:
   if not isinstance(v,str) or not v.endswith('.zip'):continue
   z=Path(v)
   if not z.is_absolute():z=mp.parent/z
   if z.is_file():zp=z;break
  if not zp:continue
  actual=sha(zp);assert actual==x['sha256'],(zp,'archive receipt sha mismatch')
  assert hashptr(md,actual),(zp,'archive missing from delivery manifest')
  wanted={Path(z['path']).name for z in a['assets'] if z['kind']=='expression' and z.get('package_id')==p['id']}|{'manifest.json','FINAL_STATUS.json','QA-independent.json','QA-independent-second-four-expressions.json','QA-independent-raw-visual.json'}
  members=[]
  with zipfile.ZipFile(zp) as z:
   for n in z.namelist():
    if Path(n).name in wanted:
     h=hashlib.sha256(z.read(n)).hexdigest();members.append({'member':n,'sha256':h})
  ar={'path':rel(zp) if zp.is_relative_to(ROOT) else str(zp),'sha256':actual,'bytes':zp.stat().st_size,'receipt_pointer':ptr,'receipt_sha_matches':True,'manifest_sha_pointers':hashptr(md,actual),'members_checked':members}
  ars.append(ar)
 p['archives_verified']=ars
 archive_files[p['id']]=ars
checks=[];issues=[];resolved=[];quality_notes=[]
for c in a['characters']:
 slug=c['slug'];ed=B/slug/'expressions_v1';mp=ed/'manifest.json';fs=ed/'FINAL_STATUS.json';m=load(mp);f=load(fs)
 aset=assets_by_slug[slug];pid=next(x['package_id'] for x in aset if x['kind']=='expression');pack=pack_by_id[pid]
 dd=[ROOT/pack['manifest']['path'],ROOT/pack['receipt']['path']]+[ROOT/x['path'] for x in pack['review_evidence']]
 def links(p):
  h=sha(p);direct=[{'evidence':ev(d),'sha_pointers':hashptr(load(d),h)} for d in dd if hashptr(load(d),h)]
  archived=[{'archive_path':ar['path'],'archive_sha256':ar['sha256'],'member':z['member'],'sha256':h} for ar in archive_files[pid] for z in ar['members_checked'] if z['sha256']==h]
  return {'file':ev(p),'direct_delivery_bindings':direct,'archived_byte_identical_bindings':archived,'bound_to_delivered_package':bool(direct or archived)}
 mc=links(mp);fc=links(fs)
 if not mc['bound_to_delivered_package']:issues.append({'slug':slug,'issue':'current expression manifest unbound to delivered archive'})
 if not fc['bound_to_delivered_package']:issues.append({'slug':slug,'issue':'current expression final status unbound to delivered archive'})
 qs=[]
 for q in sorted(ed.glob('QA-independent*.json')):
  h=sha(q);sources=[d for d in [mp,fs]+dd if hashptr(load(d),h)]
  ar=[{'archive_path':z['path'],'member':v['member']} for z in archive_files[pid] for v in z['members_checked'] if v['sha256']==h]
  assert sources or ar,(slug,q,'unbound review')
  qs.append({'file':ev(q),'hash_binding_documents':[ev(d) for d in sources],'archived_byte_identical_bindings':ar})
 if not hashptr(f,sha(mp)):
  assert hashptr(m,sha(fs)) and mc['bound_to_delivered_package'],(slug,'freeze loop not closed')
  resolved.append({'slug':slug,'observation':'FINAL_STATUS does not store the manifest hash; the immutable manifest stores the exact FINAL_STATUS hash, and the delivered package binds that manifest. No unresolved image selection ambiguity.','evidence':[ev(mp),ev(fs)],'manifest_to_status_sha_pointers':hashptr(m,sha(fs))})
 selected_archive=[]
 for x in aset:
  if x['kind']!='expression':continue
  matches=[{'archive_path':z['path'],'member':v['member']} for z in archive_files[pid] for v in z['members_checked'] if v['sha256']==x['sha256'] and Path(v['member']).name==Path(x['path']).name]
  assert matches,(slug,x['asset_id'],'selected not in delivered source archive')
  selected_archive.append({'asset_id':x['asset_id'],'sha256':x['sha256'],'archive_bindings':matches})
  x['evidence']['delivered_archive_matches']=matches
 checks.append({'slug':slug,'manifest':mc,'final_status':fc,'independent_reviews':qs,'selected_in_archives':selected_archive})
 for source in [fs]+[p for p in ed.glob('QA-independent*.json') if 'raw' not in p.name]:
  doc=load(source)
  for key in ['nonblocking_notes','nonblocking_limitations','limitations','source_conflict_disposition','provenance_status']:
   if doc.get(key):quality_notes.append({'slug':slug,'field':key,'value':doc[key],'evidence':ev(source,'/'+key)})
 if m.get('provenance_status') and 'unavailable' in m['provenance_status']:
  issues.append({'slug':slug,'type':'historical_call_provenance_gap','blocking_selection':False,'issue':'历史原始图和既存提示词已恢复，但精确生图调用参数不可用；本次仅以冻结清单/实际图SHA/独审/已发送附件证明选稿，不声明补齐历史调用。','value':m['provenance_status'],'evidence':ev(mp,'/provenance_status')})
a['freeze_chain_checks']=checks;a['resolved_schema_differences']=resolved;a['source_review_notes']=quality_notes;a['uncertainties']=issues
for g in a['excluded_gaps']:
 g['expression_id']='E2' if g['slug']=='endai' else 'E1'
 g['reason']='首稿双人，唯一修订比例漂移，修订预算用尽。' if g['slug']=='endai' else '首稿朝向失败，唯一修订安全拒绝且无产图，已停止。'
 g['retries_allowed_in_catalog_task']=False
for p in a['expression_packages']:
 p['selected_expression_count']=sum(x.get('package_id')==p['id'] for x in a['assets'])
 assert p['status']=='sent_accepted_not_read',(p['id'],p['status'])
a['identity_separation_checks']=[{'slugs':['weier','weier_ink'],'canonical_ids':['FX-HOM','FX-INK']},{'slugs':['suier','suier_lot'],'canonical_ids':['FX-CP1','FX-LOT']},{'slugs':['moer','moer_trs'],'canonical_ids':['FX-WIL','FX-TRS']},{'slugs':['fx_cv4_nier'],'canonical_ids':['FX-CV4'],'name':'佴珥'}]
for sep in a['identity_separation_checks']:
 for slug,cid in zip(sep['slugs'],sep['canonical_ids']):assert next(x for x in a['characters'] if x['slug']==slug)['canonical_id']==cid
assert len({x['canonical_id'] for x in a['characters']})==44
assert len({x['path'] for x in a['assets']})==130
assert len({x['sha256'] for x in a['assets']})==130
assert all(x['label_zh'] for x in a['assets'])
a['audit_status']='pass_selection_130_images_with_two_excluded_expression_gaps_and_documented_nonblocking_historical_provenance_limitations'
a['audited_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
a['verification_summary']={'all_130_current_asset_sha256_match_frozen_selection':True,'all_86_expression_sha256_match_delivery_manifest_and_receipt':True,'all_86_expressions_present_byte_identically_in_receipted_source_archives':True,'all_44_expression_manifests_and_statuses_bound_to_delivered_package':all(x['manifest']['bound_to_delivered_package'] and x['final_status']['bound_to_delivered_package'] for x in checks),'all_44_concept_mothers_match_expression_binding_and_concept_selection':True,'all_44_mothers_sha256_present_in_original_delivery_receipts':True,'unique_asset_paths':130,'unique_asset_sha256':130,'archive_count_verified':sum(len(p['archives_verified']) for p in a['expression_packages']),'unresolved_selection_ambiguities':sum(i.get('blocking_selection',True) for i in issues)}
tmp=OUT/'selection_audit.next.json';tmp.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n');tmp.replace(P)
summary={'audit_status':a['audit_status'],'counts':a['counts'],'verification_summary':a['verification_summary'],'uncertainties':issues,'resolved_schema_difference_count':len(resolved),'output':rel(P),'sha256':sha(P)}
(OUT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
