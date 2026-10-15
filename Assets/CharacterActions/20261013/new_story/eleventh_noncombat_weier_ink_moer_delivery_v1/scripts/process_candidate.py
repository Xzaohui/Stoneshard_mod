from pathlib import Path
from PIL import Image
import json,base64,hashlib,re,sys,numpy as np
R=Path.cwd();slug,key,version=sys.argv[1:];d=R/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1';tag=f'{key}_{version}'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=d/'raw'/f'{tag}_tool_return.json';j=json.loads(p.read_text());data=base64.b64decode(j['image_url'].split(',',1)[1]);raw=d/'raw'/f'{tag}_raw.png'
if raw.exists():assert raw.read_bytes()==data
else:raw.write_bytes(data)
orig=Path(re.search(r'as (/[^\n]+\.png) by',j['output_hint']).group(1));assert orig.read_bytes()==data
im=Image.open(raw).convert('RGBA');a=np.asarray(im).copy();old=a.copy();a[a[:,:,3]<=8]=0;a[a[:,:,3]==0,:3]=0;clean=Image.fromarray(a);cand=d/'review'/f'{tag}_transparent.png';clean.save(cand)
for mode,src in [('raw',im),('selected',clean)]:
 for kind,bg in [('light',(242,236,220,255)),('dark',(31,36,44,255))]:
  base=Image.new('RGBA',im.size,bg);base.alpha_composite(src);base.convert('RGB').save(d/'review'/f'{tag}_{mode}_{kind}.png')
assert np.array_equal(a[old[:,:,3]>8],old[old[:,:,3]>8])
args_path=d/'prompts'/f'{tag}_tool_args.json';args=json.loads(args_path.read_text());prompt_path=d/'prompts'/f'{tag}.txt';assert args['prompt']==prompt_path.read_text()
rec={'key':key,'version':version,'raw':str(raw.relative_to(R)),'raw_sha256':sha(raw),'tool_return_sha256':sha(p),'tool_payload_matches_raw':True,'tool_saved_original_matches_raw':True,'raw_size':im.size,'raw_alpha_minmax':[int(old[:,:,3].min()),int(old[:,:,3].max())],'alpha_le8_cleared_pixels':int(np.sum((old[:,:,3]>0)&(old[:,:,3]<=8))),'hidden_rgb_cleared_pixels':int(np.sum((old[:,:,3]==0)&np.any(old[:,:,:3]!=0,axis=2))),'visible_pixels_gt8_unchanged':True,'transparent_candidate':str(cand.relative_to(R)),'transparent_sha256':sha(cand),'alpha_bbox':clean.getbbox(),'nontransparent_edge_pixels':int((a[0,:,3]>0).sum()+(a[-1,:,3]>0).sum()+(a[:,0,3]>0).sum()+(a[:,-1,3]>0).sum()),'postprocess':'Only alpha <=8 and hidden RGB cleanup. No resize, crop, draw, anatomy edits, quantization, or recoloring. True same-dimension RGBA composites.','prompt_sha256':sha(prompt_path),'exact_saved_arguments_sha256':sha(args_path),'reference_files':[{'path':str(Path(x).relative_to(R)),'sha256':sha(Path(x))} for x in args['referenced_image_paths']]}
(d/'review'/f'{tag}_technical_QA.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False))
