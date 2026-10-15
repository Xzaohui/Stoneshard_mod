#!/usr/bin/env python3
"""Independent read-only source audit and deterministic export reproduction.
Writes only to this audit directory. Does not execute producer scripts or alter artwork.
"""
from pathlib import Path
from PIL import Image
import base64, collections, datetime, hashlib, io, json, re, sys
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
REPO=CAMP.parents[3]
SLUGS=('herlin','ive','jotin','loda')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def data_sha(b): return hashlib.sha256(b).hexdigest()
def info(p):
 im=Image.open(p).convert('RGBA'); colors=collections.Counter(v[:3] for v in im.getdata() if v[3]); alpha=collections.Counter(im.getchannel('A').getdata())
 return {'sha256':sha(p),'bytes':p.stat().st_size,'size':list(im.size),'mode':Image.open(p).mode,'visible_rgb_colors':len(colors),'alpha_values':sorted(alpha),'partial_alpha_pixels':sum(n for v,n in alpha.items() if v not in (0,255)),'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(colors.values()),'transparent_rgb_zero':all(v[:3]==(0,0,0) for v in im.getdata() if v[3]==0),'opaque_edge_counts':{'left':sum(im.getpixel((0,y))[3]>=128 for y in range(im.height)),'right':sum(im.getpixel((im.width-1,y))[3]>=128 for y in range(im.height)),'top':sum(im.getpixel((x,0))[3]>=128 for x in range(im.width)),'bottom':sum(im.getpixel((x,im.height-1))[3]>=128 for x in range(im.width))}}
def reproduce(raw,method,out):
 sampled=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
 alpha=sampled.getchannel('A').point(lambda x:255 if x>=128 else 0)
 pixels=list(sampled.getdata()); mask=list(alpha.getdata()); visible=[p[:3] for p,a in zip(pixels,mask) if a]
 train=Image.new('RGB',(len(visible),1));train.putdata(visible)
 palette=train.quantize(colors=32,method=getattr(Image.Quantize,method),dither=Image.Dither.NONE)
 dst=sampled.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');dst.putalpha(alpha)
 dst.putdata([p if p[3] else (0,0,0,0) for p in dst.getdata()]);dst.save(out)
 return dst
report={'audit_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':list(SLUGS),'read_only_inputs':True,'native_pixel_approval':False,'runtime_verified':False,'actors':{},'hard_errors':[]}
for slug in SLUGS:
 p=CAMP/slug; errors=[]; a={'sources':[],'raw_integrity':[],'candidates':[],'manifest':{},'errors':errors};report['actors'][slug]=a
 sm=json.loads((p/'sources/source_manifest.json').read_text());entries=sm if isinstance(sm,list) else sm['files']
 for s in entries:
  origin=REPO/(s.get('original_path') or s['source_path']);snap=p/s['snapshot_path']; expected=s['sha256']
  row={'origin':str(origin.relative_to(REPO)),'snapshot':s['snapshot_path'],'expected_sha256':expected,'origin_exists':origin.exists(),'snapshot_exists':snap.exists()}
  if origin.exists() and snap.exists():
   row.update(origin_sha256=sha(origin),snapshot_sha256=sha(snap),byte_identical=origin.read_bytes()==snap.read_bytes(),hash_matches=sha(origin)==sha(snap)==expected)
  if not row.get('hash_matches'):errors.append('source mismatch: '+row['origin'])
  a['sources'].append(row)
 for ret in sorted((p/'tool_returns').glob('portrait_v*.json')):
  d=json.loads(ret.read_text()); raw=p/'raw'/f'{ret.stem}_raw_imagegen.png';encoded=d['image_url'];assert encoded.startswith('data:image/png;base64,')
  payload=base64.b64decode(encoded.split(',',1)[1],validate=True)
  rr={'version':ret.stem,'tool_return_sha256':sha(ret),'tool_payload_sha256':data_sha(payload),'raw':str(raw.relative_to(p)),'raw_equals_tool_return_bytes':raw.exists() and payload==raw.read_bytes()}
  if raw.exists():rr['raw_metrics']=info(raw)
  hints=re.findall(r'/workspace/[^\s]+\.png',d.get('output_hint','')); originals=[]
  for h in sorted(set(hints)):
   hp=Path(h);originals.append({'path':h,'exists':hp.exists(),'sha256':sha(hp) if hp.exists() else None,'equals_saved_raw':hp.exists() and hp.read_bytes()==payload})
  rr['generated_originals']=originals
  if not rr['raw_equals_tool_return_bytes']:errors.append('raw differs from tool return: '+ret.stem)
  if any(o['exists'] and not o['equals_saved_raw'] for o in originals):errors.append('generated original differs: '+ret.stem)
  a['raw_integrity'].append(rr)
 for c in sorted((p/'candidates').glob('portrait_v*_74x100_candidate.png')):
  version=re.match(r'portrait_v[0-9]+',c.name).group(0)
  raw=p/'raw'/f'{version}_raw_imagegen.png';method='MEDIANCUT' if '_mediancut' in c.name else ('MAXCOVERAGE' if slug in ('herlin','ive') or '_maxcoverage' in c.name else 'MEDIANCUT')
  reproduced=OUT/f'{slug}_{c.stem}_independently_reproduced.png';dst=reproduce(raw,method,reproduced)
  ci=info(c);original=Image.open(c).convert('RGBA');ci.update(path=str(c.relative_to(p)),reproduction_method=method,reproduced_sha256=sha(reproduced),byte_identical=c.read_bytes()==reproduced.read_bytes(),pixel_identical=original.size==dst.size and original.tobytes()==dst.tobytes())
  ci['spec_pass']=ci['size']==[74,100] and ci['visible_rgb_colors']<=32 and set(ci['alpha_values'])<={0,255}
  preview=p/'previews'/c.name.replace('_74x100_candidate','_8x')
  ci['8x_preview_exists']=preview.exists()
  ci['8x_exact_nearest_neighbor']=preview.exists() and Image.open(preview).convert('RGBA').tobytes()==dst.resize((592,800),Image.Resampling.NEAREST).tobytes()
  if not(ci['byte_identical'] and ci['spec_pass'] and ci['8x_exact_nearest_neighbor']):errors.append('candidate checks: '+c.name)
  a['candidates'].append(ci)
 manifest=p/'manifest.json'
 if manifest.exists():
  m=json.loads(manifest.read_text());checks=[]
  for f in m.get('files',[]):
   fp=p/f['path'];checks.append({'path':f['path'],'exists':fp.exists(),'hash_matches':fp.exists() and sha(fp)==f['sha256'],'bytes_match':fp.exists() and fp.stat().st_size==f.get('bytes',fp.stat().st_size)})
  sel=p/m['selected_portrait']; selected_record=m.get('selected_portrait_sha256',m.get('selected_sha256'))
  a['manifest']={'sha256':sha(manifest),'selected_portrait':m['selected_portrait'],'selected_recorded_sha256':selected_record,'selected_actual_sha256':sha(sel),'selected_hash_matches':sha(sel)==selected_record,'generation_calls':m.get('generation_calls'),'actual_saved_tool_return_count':len(a['raw_integrity']),'generation_count_matches':m.get('generation_calls')==len(a['raw_integrity']),'file_checks':checks,'native_authored':m.get('native_authored'),'runtime_verified':m.get('runtime_verified'),'independent_qa':m.get('independent_qa')}
  if isinstance(m.get('independent_qa'),dict) and m['independent_qa'].get('report_sha256'):
   qp=REPO/m['independent_qa']['report'];matches=qp.exists() and sha(qp)==m['independent_qa']['report_sha256'];a['manifest']['independent_report_hash_matches']=matches
   if not matches:errors.append('independent report hash mismatch')
  if not a['manifest']['selected_hash_matches']:errors.append('manifest selected hash mismatch')
  if not a['manifest']['generation_count_matches']:errors.append('manifest generation count mismatch')
  errors.extend('manifest file mismatch: '+f['path'] for f in checks if not(f['hash_matches'] and f['bytes_match']))
 else:errors.append('manifest missing')
 sums=p/'SHA256SUMS.txt' if (p/'SHA256SUMS.txt').exists() else p/'SHA256SUMS'; sumrows=[]
 if sums.exists():
  for line in sums.read_text().splitlines():
   if not line.strip():continue
   expected,fn=line.split(maxsplit=1); fp=p/fn.lstrip('*');sumrows.append({'path':fn,'hash_matches':fp.exists() and sha(fp)==expected})
  errors.extend('SHA256SUMS mismatch: '+f['path'] for f in sumrows if not f['hash_matches'])
 else:errors.append('SHA256SUMS missing')
 a['SHA256SUMS']=sumrows
 report['hard_errors'].extend(slug+': '+e for e in errors)
report['all_technical_checks_pass']=not report['hard_errors']
name=sys.argv[1] if len(sys.argv)>1 else 'technical_audit.json'
(OUT/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':str((OUT/name).relative_to(REPO)),'all_technical_checks_pass':report['all_technical_checks_pass'],'hard_errors':report['hard_errors'],'actors':{k:{'sources':len(v['sources']),'raws':len(v['raw_integrity']),'candidates':len(v['candidates']),'selected':v['manifest'].get('selected_portrait')} for k,v in report['actors'].items()}},ensure_ascii=False,indent=2))
