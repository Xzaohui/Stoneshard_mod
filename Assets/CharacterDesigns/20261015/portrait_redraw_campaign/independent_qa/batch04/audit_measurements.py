"""Independent batch04 QA. Reads production files; writes only this directory.
Reimplements the declared derivative and independently hashes raw, tool image,
source copies, manifest inventories and SHA256SUMS. Author scripts never run.
"""
from pathlib import Path
from PIL import Image
from collections import Counter
from datetime import datetime, timezone
import base64, hashlib, json
OUT=Path(__file__).resolve().parent
CAMPAIGN=OUT.parent.parent
REPO=CAMPAIGN.parents[3]
SLUGS=['aren','rowen','maya','anla']
CONFIG_PATH=OUT/'reproduction_config.json'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def measure(p):
 with Image.open(p) as source: mode=source.mode; im=source.convert('RGBA')
 px=list(im.getdata());a=Counter(p[3] for p in px);c=Counter(p[:3] for p in px if p[3]);sizes=[]
 if im.width*im.height<=10000:
  remain={(i%im.width,i//im.width) for i,p in enumerate(px) if p[3]}
  while remain:
   todo=[remain.pop()];n=1
   while todo:
    x,y=todo.pop()
    for k in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if k in remain:remain.remove(k);todo.append(k);n+=1
   sizes.append(n)
 return {'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size,'size':list(im.size),'mode':mode,'visible_rgb_colors':len(c),'alpha_values':sorted(a),'visible_pixels':sum(c.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in [0,255]),'alpha_bbox':im.getchannel('A').getbbox(),'transparent_rgb_nonzero_pixels':sum(1 for p in px if not p[3] and p[:3]!=(0,0,0)),'alpha_connected_component_sizes_4way':sorted(sizes,reverse=True) if sizes else None}
def derive(raw,config):
 image=Image.open(raw).convert('RGBA')
 assert config['crop'] is None,'Undeclared crop unsupported'
 sampled=image.resize((74,100),Image.Resampling.NEAREST)
 mask=sampled.getchannel('A').point(lambda v:255 if v>=config['alpha_threshold'] else 0)
 opaque=[p[:3] for p,a in zip(sampled.getdata(),mask.getdata()) if a]
 strip=Image.new('RGB',(len(opaque),1));strip.putdata(opaque)
 method={'MEDIANCUT':Image.Quantize.MEDIANCUT,'MAXCOVERAGE':Image.Quantize.MAXCOVERAGE}[config['quantizer']]
 pal=strip.quantize(colors=32,method=method,dither=Image.Dither.NONE)
 q=sampled.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(mask)
 q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 return q

def verify_source_copies(root):
 p=root/'sources/source_manifest.json'
 if not p.exists():return []
 content=json.loads(p.read_text());items=content if isinstance(content,list) else content.get('sources',[]);result=[]
 for e in items:
  source=e.get('source',e.get('original_path',e.get('source_path',e.get('path'))));copy=e.get('snapshot',e.get('snapshot_path',e.get('copy',e.get('local_copy'))))
  if source and copy and 'sha256' in e:
   s=REPO/source;c=root/copy
   result.append({'source':source,'snapshot':copy,'source_hash_match':s.exists() and sha(s)==e['sha256'],'snapshot_hash_match':c.exists() and sha(c)==e['sha256'],'bytes_equal':s.exists() and c.exists() and s.read_bytes()==c.read_bytes()})
 return result

config=json.loads(CONFIG_PATH.read_text());roster=json.loads((CAMPAIGN/'campaign_roster.json').read_text())
entries={c['suggested_slug']:c for c in roster['characters'] if c.get('suggested_slug') in SLUGS}
result={'inspected_utc':datetime.now(timezone.utc).isoformat(),'scope':'batch04 independent QA; technical checks do not imply native pixel authorship or user approval','reproduction_config_sha256':sha(CONFIG_PATH),'source_checks':[],'characters':[]}
for slug in SLUGS:
 c=entries[slug];root=CAMPAIGN/slug;entry={'slug':slug,'canonical_id':c['canonical_id'],'name':c['name'],'candidates':[]}
 for e in c['current_cards']+[c['identity_master'],c['master_selection_evidence']]+c['master_manifests']:
  p=REPO/e['path'];result['source_checks'].append({'character':slug,'path':e['path'],'expected_sha256':e['sha256'],'sha256':sha(p) if p.exists() else None,'hash_match':p.exists() and sha(p)==e['sha256']})
 for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
  stem=target.name.split('_74x100_')[0];rawstem=stem.removesuffix('_maxcoverage');raw=root/'raw'/f'{rawstem}_raw_imagegen.png';retpath=root/'tool_returns'/f'{rawstem}.json'
  m={'target':measure(target),'raw':measure(raw) if raw.exists() else None}
  if retpath.exists():
   ret=json.loads(retpath.read_text());data=base64.b64decode(ret['image_url'].split(',',1)[1]);m.update({'tool_return_path':str(retpath.relative_to(REPO)),'tool_return_sha256':sha(retpath),'decoded_tool_image_sha256':hashlib.sha256(data).hexdigest(),'raw_equals_tool_return_bytes':raw.exists() and raw.read_bytes()==data})
  if raw.exists() and slug in config:
   cfg=dict(config[slug]);cfg['quantizer']=config[slug].get('named_export_quantizers',{}).get(stem,cfg['quantizer']);reproduced=derive(raw,cfg);output=OUT/f'{slug}_{stem}_independently_reproduced.png';reproduced.save(output)
   m.update({'reproduction_config':cfg,'independent_export':str(output.relative_to(REPO)),'independent_export_sha256':sha(output),'independent_RGBA_equal':reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes(),'independent_PNG_bytes_equal':output.read_bytes()==target.read_bytes()})
  t=m['target'];m['technical_pass']=t['size']==[74,100] and t['visible_rgb_colors']<=32 and set(t['alpha_values'])<={0,255} and m.get('raw_equals_tool_return_bytes',False) and m.get('independent_RGBA_equal',False)
  entry['candidates'].append(m)
 manifest=root/'manifest.json'
 if manifest.exists():
  d=json.loads(manifest.read_text());files=d.get('files',[]);checks=[]
  for f in files:
   p=root/f['path'];checks.append({'path':f['path'],'exists':p.exists(),'hash_match':p.exists() and sha(p)==f['sha256'],'bytes_match':p.exists() and ('bytes' not in f or p.stat().st_size==f['bytes'])})
  selected=d.get('selected_portrait');sp=root/selected if isinstance(selected,str) else None
  entry.update({'manifest_sha256':sha(manifest),'manifest_file_checks':checks,'manifest_all_file_hashes_match':bool(checks) and all(f['hash_match'] and f['bytes_match'] for f in checks),'declared_selected_portrait':selected,'declared_selected_sha256':d.get('selected_sha256'),'measured_selected_sha256':sha(sp) if sp and sp.exists() else None,'declared_generation_calls':d.get('generation_calls'),'declared_native_authored':d.get('native_authored'),'declared_runtime_integrated':d.get('runtime_integrated')})
  if d.get('selected_sha256'):entry['selected_sha256_field_match']=sp is not None and sp.exists() and sha(sp)==d['selected_sha256']
  rendered=[p for p in (root/'tool_returns').glob('portrait_v*.json') if 'image_url' in json.loads(p.read_text())];entry['tool_return_count']=len(rendered);entry['within_two_generation_limit']=entry['tool_return_count']<=2;entry['nonrendering_tool_events']=[{'path':str(p.relative_to(root)),'data':json.loads(p.read_text())} for p in (root/'tool_returns').glob('portrait_v*.json') if p not in rendered]
 sourcechecks=verify_source_copies(root);entry['source_copy_checks']=sourcechecks;entry['source_copies_all_match']=bool(sourcechecks) and all(s['source_hash_match'] and s['snapshot_hash_match'] and s['bytes_equal'] for s in sourcechecks)
 sums=root/'SHA256SUMS.txt'
 if sums.exists():
  checks=[]
  for line in sums.read_text().splitlines():
   if not line.strip():continue
   h,rel=line.split('  ',1);p=root/rel;checks.append({'path':rel,'hash_match':p.exists() and sha(p)==h})
  entry['sha256sums_checks']=checks;entry['sha256sums_all_match']=bool(checks) and all(x['hash_match'] for x in checks)
 result['characters'].append(entry)
output=OUT/'independent_measurements.json';output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(output.relative_to(REPO)),'all_source_hashes_match':all(x['hash_match'] for x in result['source_checks']),'characters':[{'slug':c['slug'],'targets':[{'sha':m['target']['sha256'],'colors':m['target']['visible_rgb_colors'],'technical_pass':m['technical_pass'],'RGBA_equal':m.get('independent_RGBA_equal'),'PNG_bytes_equal':m.get('independent_PNG_bytes_equal')} for m in c['candidates']],'manifest_matches':c.get('manifest_all_file_hashes_match'),'source_copies_match':c.get('source_copies_all_match'),'sums_match':c.get('sha256sums_all_match')} for c in result['characters']]},ensure_ascii=False,indent=2))
