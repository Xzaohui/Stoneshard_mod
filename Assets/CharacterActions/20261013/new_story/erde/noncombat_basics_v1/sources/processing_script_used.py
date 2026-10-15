from PIL import Image
import pathlib,numpy as np,json,hashlib,shutil,re,sys,base64
R=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
slug,key=sys.argv[1:3]
p=R/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'
retpath=p/'raw'/f'{key}_tool_return.json';ret=json.loads(retpath.read_text());raw=p/'raw'/f'{key}_raw.png'; assert not raw.exists()
payload=base64.b64decode(ret['image_url'].split(',',1)[1]);raw.write_bytes(payload)
im=Image.open(raw);original_mode=im.mode; assert original_mode=='RGBA';a=np.array(im);alpha=a[:,:,3].copy();n=int(((alpha>0)&(alpha<=8)).sum());a[alpha<=8]=0;out=Image.fromarray(a);op=p/'exports'/f'{key}_transparent.png';out.save(op)
for name,color in [('light',(239,233,219,255)),('dark',(29,34,38,255))]:
 board=Image.new('RGBA',im.size,color);board.alpha_composite(out);board.convert('RGB').save(p/'review'/f'{key}_{name}.png')
pa=json.loads((p/'prompts'/f'{key}_parameters.json').read_text()); prompt=(p/'prompts'/f'{key}.txt').read_text();assert prompt==pa['prompt'];a2=np.array(out.getchannel('A'));bbox=out.getbbox()
report={'raw_mode':original_mode,'size':im.size,'raw_alpha_min_max':[int(alpha.min()),int(alpha.max())],'selected_alpha_min_max':[int(a2.min()),int(a2.max())],'selected_transparent_pixels':int((a2==0).sum()),'selected_opaque_pixels':int((a2==255).sum()),'selected_semialpha_pixels':int(((a2>0)&(a2<255)).sum()),'alpha_only_cleanup_threshold':8,'cleaned_near_zero_alpha_pixels':n,'body_pixels_modified':False,'raw_matches_tool_payload':raw.read_bytes()==payload,'prompt_file_equals_actual_parameter':prompt==pa['prompt'],'reference_hashes':[{'path':x,'sha256':hashlib.sha256(pathlib.Path(x).read_bytes()).hexdigest()} for x in pa['referenced_image_paths']],'bbox':bbox,'margins':[bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3]],'files':{}}
for f in [raw,retpath,op,p/'prompts'/f'{key}.txt',p/'prompts'/f'{key}_parameters.json']+[p/'review'/f'{key}_{s}.png' for s in ['light','dark']]:
 report['files'][str(f.relative_to(p))]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
(p/'raw'/f'{key}_provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
