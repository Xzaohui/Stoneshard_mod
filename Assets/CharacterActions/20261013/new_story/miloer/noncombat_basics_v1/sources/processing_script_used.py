from PIL import Image
import pathlib,numpy as np,json,hashlib,shutil,re,sys,base64
r=pathlib.Path(__file__).resolve().parents[6]
# Resolve repository by invariant directory name.
while r.name!='Stoneshard_mod':r=r.parent
slug,key=sys.argv[1:3]
p=r/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'
ret=json.loads((p/'raw'/f'{key}_tool_return.json').read_text())
m=re.search(r'as (/[^\n]+\.png) by default',ret.get('output_hint',''))
raw=p/'raw'/f'{key}_raw.png'
assert not raw.exists(),str(raw)
if m:shutil.copyfile(m[1],raw)
else:raw.write_bytes(base64.b64decode(ret['image_url'].split(',',1)[1]))
im=Image.open(raw).convert('RGBA');a=np.array(im);n=int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum());a[a[:,:,3]<=8]=0;out=Image.fromarray(a);out.save(p/'exports'/f'{key}_transparent.png')
for name,color in [('light',(239,233,219,255)),('dark',(29,34,38,255))]:
 board=Image.new('RGBA',im.size,color);board.alpha_composite(out);board.convert('RGB').save(p/'review'/f'{key}_{name}.png')
report={'raw_mode':im.mode,'size':im.size,'alpha_only_cleanup_threshold':8,'cleaned_near_zero_alpha_pixels':n,'body_pixels_modified':False,'files':{}}
for f in [raw,p/'raw'/f'{key}_tool_return.json',p/'exports'/f'{key}_transparent.png',p/'prompts'/f'{key}.txt',p/'prompts'/f'{key}_parameters.json']:
 report['files'][str(f.relative_to(p))]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
(p/'raw'/f'{key}_provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
