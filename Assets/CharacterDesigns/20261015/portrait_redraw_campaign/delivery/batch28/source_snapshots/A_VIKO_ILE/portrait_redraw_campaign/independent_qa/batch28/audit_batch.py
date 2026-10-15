"""Independent batch28 read-only author audit; writes only beneath this QA directory.
Author derive source was inspected before reproduction; outputs are reconstructed here,
never by running author finalization or by changing original candidates.
"""
from pathlib import Path
import base64, hashlib, io, json, shutil, subprocess, sys
from datetime import datetime, timezone
from PIL import Image, __version__ as PIL_VERSION
Q=Path(__file__).resolve().parent
P=Q.parent.parent
R=P.parents[3]
SLUGS=sys.argv[1:] or ['viko','ile','harlen','belo']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for slug in SLUGS:
 w=P/slug
 report={'slug':slug,'checked_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'pillow':PIL_VERSION,'derive_script_sha256':sha(w/'derive_portrait.py'),'versions':[]}
 source_manifest=json.loads((w/'sources/source_manifest.json').read_text())
 report['source_validation']=[]
 for e in source_manifest.get('items',source_manifest.get('sources',[])):
  origin=e.get('original_path',e.get('source',e.get('path')));snap=e.get('snapshot_path',e.get('snapshot'))
  b=subprocess.check_output(['git','show',origin[4:]],cwd=R) if origin.startswith('git ') else (R/origin).read_bytes()
  report['source_validation'].append({'source':origin,'snapshot':snap,'declared_sha256':e['sha256'],'actual_sha256':hashlib.sha256(b).hexdigest(),'snapshot_sha256':sha(w/snap),'all_equal':hashlib.sha256(b).hexdigest()==e['sha256']==sha(w/snap)})
 for raw in sorted((w/'raw').glob('*_raw_imagegen.png')):
  version=raw.name.removesuffix('_raw_imagegen.png')
  returned=w/'tool_returns'/f'{version}.json';prompt=w/'prompts'/f'{version}.json'
  encoded=json.loads(returned.read_text())['image_url'].split(',',1)[1]
  src=Image.open(raw).convert('RGBA');a=src.getchannel('A');binary=a.point(lambda v:255 if v>=128 else 0)
  p=json.loads(prompt.read_text())
  v={'version':version,'raw_path':str(raw.relative_to(P)),'raw_sha256':sha(raw),'raw_size':list(src.size),'tool_return_sha256':sha(returned),'raw_equals_return':base64.b64decode(encoded)==raw.read_bytes(),'raw_alpha_bbox_gt0':a.getbbox(),'raw_alpha_bbox_ge128':binary.getbbox(),'raw_border_opaque':{'top':sum(binary.getpixel((x,0))>0 for x in range(src.width)),'bottom':sum(binary.getpixel((x,src.height-1))>0 for x in range(src.width)),'left':sum(binary.getpixel((0,y))>0 for y in range(src.height)),'right':sum(binary.getpixel((src.width-1,y))>0 for y in range(src.height))},'prompt_text_equals_exact_args':p['prompt']==(w/'prompts'/f'{version}.txt').read_text().rstrip('\n'),'transparent_background':p['transparent_background'],'references':[{'path':f,'sha256':sha(Path(f))} for f in p['referenced_image_paths']],'derivatives':[]}
  v['raw_boundary_thresholds']={}
  for threshold in [1,5,16,128,255]:
   mask=a.point(lambda z:255 if z>=threshold else 0);ww,hh=src.size
   borders={'top':[x for x in range(ww) if mask.getpixel((x,0))], 'bottom':[x for x in range(ww) if mask.getpixel((x,hh-1))], 'left':[y for y in range(hh) if mask.getpixel((0,y))], 'right':[y for y in range(hh) if mask.getpixel((ww-1,y))]}
   v['raw_boundary_thresholds'][str(threshold)]={'bbox':mask.getbbox(),'border_counts':{k:len(z) for k,z in borders.items()},'border_ranges':{k:[min(z),max(z)] if z else None for k,z in borders.items()}}
  dst=Q/'reproduction'/slug;dst.mkdir(parents=True,exist_ok=True)
  for candidate in sorted((w/'candidates').glob(f'{version}*_74x100_candidate.png')):
   tag=candidate.name.removesuffix('_74x100_candidate.png');fit=(72,98) if tag.endswith('_inset') else (74,100)
   scale=min(fit[0]/src.width,fit[1]/src.height);size=(round(src.width*scale),round(src.height*scale))
   small=src.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(74,100),(0,0,0,0));canvas.paste(small,((74-size[0])//2,(100-size[1])//2))
   alpha=canvas.getchannel('A').point(lambda x:255 if x>=128 else 0)
   visible=[rgb[:3] for rgb,a in zip(canvas.getdata(),alpha.getdata()) if a]
   samples=Image.new('RGB',(len(visible),1));samples.putdata(visible)
   palette=samples.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
   q=canvas.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB')
   out=Image.new('RGBA',(74,100));out.putdata([(*rgb,a) if a else (0,0,0,0) for rgb,a in zip(q.getdata(),alpha.getdata())])
   reconstructed=dst/candidate.name;out.save(reconstructed);actual=Image.open(candidate).convert('RGBA')
   previews={};one=w/'previews'/f'{tag}_1x.png';eight=w/'previews'/f'{tag}_8x.png'
   expected8=out.resize((592,800),Image.Resampling.NEAREST);b=io.BytesIO();expected8.save(b,format='PNG');expected8.save(dst/f'{tag}_8x.png')
   previews['1x_bytes_equal']=one.read_bytes()==candidate.read_bytes();previews['8x_exact_NN_pixels']=Image.open(eight).size==expected8.size and Image.open(eight).convert('RGBA').tobytes()==expected8.tobytes();previews['8x_byte_reproduction']=eight.read_bytes()==b.getvalue()
   board=Image.new('RGB',(238,108),(100,100,100))
   for i,bg in enumerate([(20,20,22),(115,115,115),(235,231,220)]):
    tile=Image.new('RGBA',(74,100),(*bg,255));tile.alpha_composite(out);board.paste(tile.convert('RGB'),(4+i*78,4))
   for factor in [1,4]:
    ref=w/'previews'/f'{tag}_{factor}x_backgrounds.png';expected=board if factor==1 else board.resize((952,432),Image.Resampling.NEAREST);b=io.BytesIO();expected.save(b,format='PNG');previews[f'{factor}x_backgrounds_byte_reproduction']=ref.read_bytes()==b.getvalue()
   values=set(actual.getchannel('A').getdata());colors={p[:3] for p in actual.getdata() if p[3]}
   v['derivatives'].append({'path':str(candidate.relative_to(P)),'sha256':sha(candidate),'dimensions':list(actual.size),'stored_mode':Image.open(candidate).mode,'visible_rgb_colors':len(colors),'alpha_values':sorted(values),'alpha_bbox':actual.getchannel('A').getbbox(),'transparent_rgb_zero':all(p[:3]==(0,0,0) for p in actual.getdata() if p[3]==0),'valid_format':actual.size==(74,100) and Image.open(candidate).mode=='RGBA' and len(colors)<=32 and values=={0,255},'byte_reproduction':candidate.read_bytes()==reconstructed.read_bytes(),'pixel_reproduction':actual.tobytes()==out.tobytes(),'fit_box':fit,'previews':previews})
  report['versions'].append(v)
 report['style_reference_NN_checks']=[]
 for n in ['mara','iwo','leiya','tore']:
  base=w/'sources'/f'{n}_style_reference.png';enlarged=w/'sources'/f'{n}_style_reference_8x.png'
  if enlarged.exists():
   im=Image.open(base).convert('RGBA');exp=im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST);buf=io.BytesIO();exp.save(buf,format='PNG');actual=Image.open(enlarged).convert('RGBA')
   report['style_reference_NN_checks'].append({'reference':n,'source_sha256':sha(base),'enlarged_sha256':sha(enlarged),'pixels_exact_8x_NN':actual.tobytes()==exp.tobytes() and actual.size==exp.size,'bytes_exact_8x_NN':enlarged.read_bytes()==buf.getvalue()})
 report['generation_count']=len(report['versions']);report['within_two_successful_generation_limit']=report['generation_count']<=2
 if (w/'manifest.json').exists():
  m=json.loads((w/'manifest.json').read_text());report['manifest_sha256']=sha(w/'manifest.json');report['manifest_selected_path']=m.get('selected_portrait',m.get('selected_candidate'));report['manifest_selected_sha256']=m.get('selected_sha256');checks=[]
  sel=report['manifest_selected_path'];selected=w/sel if sel else None;report['manifest_selected_actual_sha256']=sha(selected) if selected and selected.exists() else None;report['manifest_selected_hash_matches']=bool(selected and selected.exists() and sha(selected)==m.get('selected_sha256'))
  report['manifest_false_native_runtime_flags']={k:m.get(k) for k in ['native_authored','native_pixel_approved','runtime_integrated','runtime_verified']}
  for f in m.get('files',[]):
   file=w/f['path'];checks.append({'path':f['path'],'declared':f['sha256'],'actual':sha(file) if file.exists() else None,'declared_bytes':f.get('bytes'),'actual_bytes':file.stat().st_size if file.exists() else None,'matches':file.exists() and sha(file)==f['sha256'] and (f.get('bytes') is None or f['bytes']==file.stat().st_size)})
  report['manifest_file_checks']=checks;report['manifest_all_hashes_match']=all(x['matches'] for x in checks)
  expected={str(f.relative_to(w)) for f in w.rglob('*') if f.is_file() and f.name not in ['manifest.json','SHA256SUMS','SHA256SUMS.txt']};report['manifest_missing_files']=sorted(expected-{x['path'] for x in checks})
  for name in ['SHA256SUMS','SHA256SUMS.txt']:
   if (w/name).exists():
    checks=[]
    for line in (w/name).read_text().splitlines():
     h,rel=line.split('  ',1);f=w/rel;checks.append({'path':rel,'matches':f.exists() and sha(f)==h})
    report['sha256sums_file']=name;report['sha256sums_count']=len(checks);report['sha256sums_all_match']=all(x['matches'] for x in checks);report['sha256sums_failures']=[x for x in checks if not x['matches']];report['sha256sums_missing_files']=sorted({str(f.relative_to(w)) for f in w.rglob('*') if f.is_file() and f.name not in ['SHA256SUMS','SHA256SUMS.txt']}-{x['path'] for x in checks})
 (Q/f'{slug}_technical_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');rows.append({'slug':slug,'generations':report['generation_count'],'raw_equals_return':all(v['raw_equals_return'] for v in report['versions']),'reproduction':all(d['byte_reproduction'] for v in report['versions'] for d in v['derivatives']),'manifest_all_hashes_match':report.get('manifest_all_hashes_match'),'manifest_missing_files':report.get('manifest_missing_files')})
print(json.dumps(rows,ensure_ascii=False,indent=2))
