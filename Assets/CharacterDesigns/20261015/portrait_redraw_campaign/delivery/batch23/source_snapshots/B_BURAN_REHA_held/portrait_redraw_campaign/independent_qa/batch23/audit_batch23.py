"""Read-only audit of actor directories. All writes stay in independent_qa/batch23.
Reviewed author exporter: no drawing, crop, or source mutations; runs only copied script.
"""
from pathlib import Path
import json, hashlib, base64, sys, subprocess, shutil, datetime, re
from PIL import Image
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
REPO=CAMP.parents[3]
SLUGS=['saler','wenno','buran','reha']
EXPECTED_DERIVE={'338febc664682900e78901a9b6ecb24df118d9d0de3e66b82c1a7859fce0e4c4','190a41689cdef6e20d8ead92150613143be1d9905077d79d3ac1297789da4871'}
EXPECTED_FINALIZER={'9bf5099e6433c37215a00da35f27db153fa9e6c1cdec62ce4881cfe4cb1728f3','cdebfae47ec4e81525a0feb195e307350cdc0d0bedf083f38f55dec62321e6b1','35e4a3c93366177c3a02690d8dca2c355165f93a685b5383eb48b2a8ae059d67'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def stats(p):
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); pix=list(im.getdata())
 return dict(size=list(im.size),mode=Image.open(p).mode,sha256=sha(p),visible_rgb_colors=len({x[:3] for x in pix if x[3]}),alpha_values=sorted(set(a.getdata())),alpha_bbox=a.getbbox(),transparent_rgb_zero=all(x[:3]==(0,0,0) for x in pix if x[3]==0))
def independently_reconstruct(raw,profile,destination):
 src=Image.open(raw).convert('RGBA'); width,height={'full':(74,100),'inset':(72,98),'containment':(70,96)}[profile]
 scale=min(width/src.width,height/src.height); dims=tuple(round(d*scale) for d in src.size)
 layer=src.resize(dims,Image.Resampling.NEAREST); canvas=Image.new('RGBA',(74,100));canvas.paste(layer,((74-dims[0])//2,(100-dims[1])//2))
 pixels=list(canvas.getdata()); chosen=[v[:3] for v in pixels if v[3]>=128]
 sample=Image.new('RGB',(len(chosen),1));sample.putdata(chosen)
 pal=sample.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
 indexed=canvas.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGB')
 result=Image.new('RGBA',(74,100));result.putdata([(*rgb,255) if original[3]>=128 else (0,0,0,0) for rgb,original in zip(indexed.getdata(),pixels)])
 destination.parent.mkdir(parents=True,exist_ok=True);result.save(destination)
 return result

def raw_edges(p):
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); boxes={'left':(0,0,1,im.height),'right':(im.width-1,0,im.width,im.height),'top':(0,0,im.width,1),'bottom':(0,im.height-1,im.width,im.height)}
 return {'size':list(im.size),'alpha_gt5_bbox':a.point(lambda v:255 if v>5 else 0).getbbox(),'alpha128_bbox':a.point(lambda v:255 if v>=128 else 0).getbbox(),'border_max_alpha':{e:max(a.crop(b).getdata()) for e,b in boxes.items()},'scope':'True silhouette completeness also independently inspected visually. Low alpha <=5 residue is not silhouette.'}
roster=load(CAMP/'campaign_roster.json')
report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'independent batch23 QA','scope':'Technical verification only, visual judgement separately recorded. NN exports are derived candidates, not native pixel final or runtime verification.','roster_sha256':sha(CAMP/'campaign_roster.json'),'characters':[]}
for slug in SLUGS:
 w=CAMP/slug; r=next(x for x in roster['characters'] if x['suggested_slug']==slug)
 a={'slug':slug,'canonical_id':r['canonical_id'],'name':r['name'],'sources':[],'raw_integrity':[],'candidates':[],'replay':[],'errors':[],'pending':[]}
 sm=load(w/'sources/source_manifest.json')
 for item in sm.get('items',sm.get('sources',[])):
  source=item.get('original_path',item.get('source_path')); local=item.get('snapshot_path',item.get('local_path')); op=REPO/source; lp=w/local
  row={'source':source,'snapshot':local,'recorded_sha256':item['sha256'],'source_sha256':sha(op) if op.exists() else None,'snapshot_sha256':sha(lp) if lp.exists() else None}
  row['matches']=row['source_sha256']==row['snapshot_sha256']==row['recorded_sha256']
  if item.get('derived_from_sha256'):
   src_image=Image.open(op).convert('RGBA'); target_image=Image.open(lp).convert('RGBA')
   row['is_derived_preview']=True;row['source_expected_sha256']=item['derived_from_sha256'];row['exact_8x_NN']=target_image.size==(src_image.width*8,src_image.height*8) and target_image.tobytes()==src_image.resize(target_image.size,Image.Resampling.NEAREST).tobytes()
   row['matches']=row['source_sha256']==row['source_expected_sha256'] and row['snapshot_sha256']==row['recorded_sha256'] and row['exact_8x_NN']
  a['sources'].append(row)
  if not row['matches']: a['errors'].append('source integrity: '+source)
 a['roster_source_checks']=[]
 for item in r['current_cards']+[r['identity_master'],r['master_selection_evidence']]+r['master_manifests']:
  p=REPO/item['path']; row={'path':item['path'],'recorded_sha256':item['sha256'],'actual_sha256':sha(p) if p.exists() else None}; row['matches']=row['recorded_sha256']==row['actual_sha256'];a['roster_source_checks'].append(row)
  if not row['matches']:a['errors'].append('roster source changed: '+item['path'])
 a['exporter_review']={'derive_sha256':sha(w/'derive_portrait.py'),'finalizer_sha256':sha(w/'finalize_manifest.py'),'reviewed_before_execution':True}
 safe=a['exporter_review']['derive_sha256'] in EXPECTED_DERIVE and a['exporter_review']['finalizer_sha256'] in EXPECTED_FINALIZER
 a['exporter_review']['matches_read_reviewed_scripts']=safe
 if not safe:a['errors'].append('script changed; do not replay before review')
 for f in sorted((w/'tool_returns').glob('*.json')):
  d=load(f)
  if 'image_url' not in d:
   record={'path':str(f.relative_to(w)),'sha256':sha(f),'record':d,'recognized_pre_generation_validation':d.get('images_generated')==0 and 'at most 5' in d.get('error','') and len(d.get('request',{}).get('referenced_image_paths',[]))==6}
   a.setdefault('non_image_tool_records',[]).append(record)
   if not record['recognized_pre_generation_validation']:a['errors'].append('unrecognized non-image tool return: '+f.name)
   continue
  version=f.stem; raw=w/'raw'/f'{version}_raw_imagegen.png'; payload=base64.b64decode(d['image_url'].split(',',1)[1],validate=True)
  row={'version':version,'return_sha256':sha(f),'payload_sha256':hashlib.sha256(payload).hexdigest(),'raw_sha256':sha(raw) if raw.exists() else None,'byte_identical_to_return':raw.exists() and raw.read_bytes()==payload}
  if raw.exists():row['edges']=raw_edges(raw)
  else:a['pending'].append('missing raw '+version)
  if raw.exists() and not row['byte_identical_to_return']:a['errors'].append('tool/raw mismatch '+version)
  prompt=w/'prompts'/f'{version}.json'
  if prompt.exists():
   pp=load(prompt);pp=pp.get('arguments',pp.get('args',pp));row['prompt_sha256']=sha(prompt);row['transparent_background_requested']=pp.get('transparent_background');row['references']=[{'path':s,'exists':Path(s).exists(),'sha256':sha(Path(s)) if Path(s).exists() else None} for s in pp.get('referenced_image_paths',[])]
   if not all(x['exists'] for x in row['references']):a['errors'].append('missing prompt reference '+version)
  else:a['errors'].append('missing prompt '+version)
  a['raw_integrity'].append(row)
 if len(a['raw_integrity'])>2:a['errors'].append('more than 2 successful images')
 a['successful_image_returns']=len(a['raw_integrity'])
 if not a['raw_integrity']:a['pending'].append('no generated image yet')
 for f in sorted((w/'candidates').glob('*_74x100_candidate.png')):
  tag=f.name.removesuffix('_74x100_candidate.png'); version=re.match(r'portrait_v\d+',tag).group(0); profile='containment' if tag.endswith('_containment') else 'inset' if tag.endswith('_inset') else 'full'
  independent_path=OUT/'independent_reconstruction'/slug/f.name
  independent_image=independently_reconstruct(w/'raw'/f'{version}_raw_imagegen.png',profile,independent_path)
  row=stats(f);row['path']=str(f.relative_to(w));row['independent_reconstruction_png_byte_identical']=independent_path.read_bytes()==f.read_bytes();row['independent_reconstruction_sha256']=sha(independent_path);row['specification_pass']=row['size']==[74,100] and row['mode']=='RGBA' and row['visible_rgb_colors']<=32 and row['alpha_values']==[0,255] and row['transparent_rgb_zero']
  im=Image.open(f).convert('RGBA'); pre=w/'previews'/f'{tag}_8x.png';p1=w/'previews'/f'{tag}_1x.png';bg1=w/'previews'/f'{tag}_1x_backgrounds.png';bg4=w/'previews'/f'{tag}_4x_backgrounds.png'
  row['preview_1x_exact']=p1.exists() and Image.open(p1).convert('RGBA').tobytes()==im.tobytes() and Image.open(p1).size==im.size
  row['preview_8x_exact_NN']=pre.exists() and Image.open(pre).convert('RGBA').tobytes()==im.resize((592,800),Image.Resampling.NEAREST).tobytes() and Image.open(pre).size==(592,800)
  row['background_4x_exact_NN']=bg1.exists() and bg4.exists() and Image.open(bg4).convert('RGB').tobytes()==Image.open(bg1).convert('RGB').resize((952,432),Image.Resampling.NEAREST).tobytes() and Image.open(bg4).size==(952,432)
  if safe:
   rp=OUT/'reproduction'/slug/tag
   for sub in ['raw','tool_returns','candidates','previews','qa']:(rp/sub).mkdir(parents=True,exist_ok=True)
   for src,dst in [(w/'derive_portrait.py',rp/'derive_portrait.py'),(w/'raw'/f'{version}_raw_imagegen.png',rp/'raw'/f'{version}_raw_imagegen.png'),(w/'tool_returns'/f'{version}.json',rp/'tool_returns'/f'{version}.json')]:shutil.copyfile(src,dst)
   run=subprocess.run([sys.executable,str(rp/'derive_portrait.py'),version,profile],capture_output=True,text=True,cwd=rp)
   dest=rp/str(f.relative_to(w)); replay={'candidate':str(f.relative_to(w)),'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'reproduced_file':str(dest.relative_to(OUT)),'png_byte_identical':dest.exists() and dest.read_bytes()==f.read_bytes()}
   replay['all_preview_byte_matches']={str(src.relative_to(w)): (rp/src.relative_to(w)).exists() and (rp/src.relative_to(w)).read_bytes()==src.read_bytes() for src in [p1,pre,bg1,bg4]}
   a['replay'].append(replay);row['reproduced_png_byte_identical']=replay['png_byte_identical'];row['all_previews_byte_identical']=all(replay['all_preview_byte_matches'].values())
  if not all(row.get(k,False) for k in ['specification_pass','preview_1x_exact','preview_8x_exact_NN','background_4x_exact_NN','reproduced_png_byte_identical','all_previews_byte_identical','independent_reconstruction_png_byte_identical']):a['errors'].append('candidate validation '+str(f.relative_to(w)))
  a['candidates'].append(row)
 mp=w/'manifest.json'
 if mp.exists():
  m=load(mp); rows=[]
  for item in m['files']:
   p=w/item['path'];rows.append({'path':item['path'],'exists':p.exists(),'sha256_matches':p.exists() and sha(p)==item['sha256'],'bytes_matches':p.exists() and p.stat().st_size==item['bytes']})
  inventory={x['path'] for x in rows}; actual={str(p.relative_to(w)) for p in w.rglob('*') if p.is_file()}; omitted=sorted(actual-inventory-{'manifest.json','SHA256SUMS'})
  sel=m.get('selected_portrait') or m.get('held_evidence_portrait'); sp=w/sel
  a['manifest']={'sha256':sha(mp),'selected':sel,'selected_sha256':sha(sp),'selected_hash_matches':(m.get('selected_sha256') or m.get('held_evidence_sha256'))==sha(sp),'held_evidence_only':m['status'].startswith('held'),'author_selected_is_null':m.get('selected_portrait') is None,'status':m['status'],'generation_count_matches':m['generation_calls']==len(a['raw_integrity']),'boundary_flags':{k:m.get(k) for k in ['native_authored','native_pixel_approved','runtime_integrated','runtime_verified']},'file_checks':rows,'omitted':omitted}
  if not a['manifest']['selected_hash_matches'] or any(not x['sha256_matches'] or not x['bytes_matches'] for x in rows) or omitted:a['errors'].append('manifest inventory or selected integrity')
  if any(a['manifest']['boundary_flags'].values()):a['errors'].append('manifest boundary overclaim')
  if not a['manifest']['generation_count_matches']:a['errors'].append('generation count mismatch')
  sums=w/'SHA256SUMS'; sr=[]
  if sums.exists():
   for ln in sums.read_text().splitlines():
    digest,rel=ln.split('  ',1);p=w/rel;sr.append({'path':rel,'matches':p.exists() and sha(p)==digest})
   a['sha256sums']={'sha256':sha(sums),'all_match':all(x['matches'] for x in sr),'count':len(sr),'omitted':sorted(actual-{x['path'] for x in sr}-{'SHA256SUMS'}),'checks':sr}
   if not a['sha256sums']['all_match'] or a['sha256sums']['omitted']:a['errors'].append('SHA256SUMS mismatch/omitted')
 else:a['pending'].append('no manifest yet')
 report['characters'].append(a)
report['technical_checks_pass']=all(not a['errors'] and not a['pending'] for a in report['characters'])
name=sys.argv[1] if len(sys.argv)>1 else 'technical_audit.json'; write(OUT/name,report)
print(json.dumps({'output':name,'pass':report['technical_checks_pass'],'characters':[{k:a[k] for k in ['slug','successful_image_returns','errors','pending']} for a in report['characters']]},ensure_ascii=False,indent=2))
