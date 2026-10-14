from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,base64,hashlib,sys,numpy as np,re,shutil,datetime
R=Path(__file__).resolve().parents[5]
# This script decodes original image bytes, copies RGBA without edits, validates hashes and makes review-only nearest-neighbor layouts.
slug,stem=sys.argv[1:3];o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';key,v=stem.rsplit('_v',1)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=o/'raw'/f'{stem}.tool_result.json';result=json.loads(r.read_text());raw=o/'raw'/f'{stem}.png'
data=base64.b64decode(result['image_url'].split(',',1)[1]);
if raw.exists(): assert raw.read_bytes()==data
else: raw.write_bytes(data)
args=o/'prompts'/f'{stem}.parameters.json';a=json.loads(args.read_text());prompt=o/'prompts'/f'{stem}.txt';assert a['prompt']==prompt.read_text()
im=Image.open(raw);assert im.mode=='RGBA';im.load();alpha=np.array(im.getchannel('A'));bbox=im.getbbox()
selected=o/'exports'/f'{stem}_transparent.png'
if selected.exists(): assert selected.read_bytes()==raw.read_bytes()
else: shutil.copy2(raw,selected)
orig=re.search(r'as (/[^\n]+?\.png) by default',result.get('output_hint',''))
origin=Path(orig.group(1)) if orig else None
if origin and origin.exists(): assert origin.read_bytes()==data
record={'key':key,'version':int(v),'tool':'builtin image_gen.imagegen','raw':str(raw.relative_to(o)),'raw_sha256':sha(raw),'raw_bytes':raw.stat().st_size,'transparent':str(selected.relative_to(o)),'transparent_sha256':sha(selected),'prompt':str(prompt.relative_to(o)),'prompt_sha256':sha(prompt),'parameters':str(args.relative_to(o)),'parameters_sha256':sha(args),'complete_tool_result':str(r.relative_to(o)),'complete_tool_result_sha256':sha(r),'original_generated_path':str(origin) if origin else None,'original_byte_copy_verified':bool(origin and origin.exists()),'input_references':[{'path':str(Path(x).relative_to(R)),'sha256':sha(Path(x))} for x in a['referenced_image_paths']],'alpha':{'mode':im.mode,'size':im.size,'zero':int((alpha==0).sum()),'partial':int(((alpha>0)&(alpha<255)).sum()),'opaque':int((alpha==255).sum()),'bbox':bbox,'corner_alpha':[int(alpha[0,0]),int(alpha[0,-1]),int(alpha[-1,0]),int(alpha[-1,-1])]},'processing':'Selected PNG is a byte-identical copy of imagegen RGBA. No alpha edit, quantization, body drawing, stretching or compositing. Review layouts use RGBA alpha_composite and aspect-preserving nearest-neighbor sizing only.'}
rec=o/'raw'/f'{stem}.receipt.json'
if rec.exists(): assert json.loads(rec.read_text())==json.loads(json.dumps(record))
else:rec.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
c=json.loads((o/'production_brief.json').read_text());p=next(x for x in c['plans'] if x['key']==key)
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',31);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
# Alpha-only cleanup removes stray low-alpha fringe and restores fully opaque pixel clusters.
clean=im.copy();clean.putalpha(Image.fromarray(np.where(alpha>=128,255,0).astype('uint8')))
cleanpath=o/'exports'/f'{stem}_transparent_clean.png';clean.save(cleanpath)
assert np.array_equal(np.array(clean)[:,:,:3],np.array(im)[:,:,:3])
processing={'input_raw':str(raw.relative_to(o)),'input_sha256':sha(raw),'output':str(cleanpath.relative_to(o)),'output_sha256':sha(cleanpath),'operation':'Alpha threshold only: A >= 128 becomes 255; A < 128 becomes 0. RGB byte values, canvas, pixel positions and anatomy unchanged.','alpha_bbox':clean.getbbox(),'alpha_values':[0,255],'rgba_layout':'Image.alpha_composite over fully opaque backgrounds; nearest-neighbor aspect-preserving only.'}
(o/'raw'/f'{stem}.processing.json').write_text(json.dumps(processing,ensure_ascii=False,indent=2)+'\n')
im=clean
m=Image.open(R/c['mother_image']['transparent']).convert('RGBA')
board=Image.new('RGBA',(2000,1600));
for row,(bg,fg,label) in enumerate([((239,235,224,255),(44,39,34,255),'浅底'),((28,33,40,255),(236,231,220,255),'深底')]):
 panel=Image.new('RGBA',(2000,800),bg);d=ImageDraw.Draw(panel);d.text((30,15),c['name']+'｜'+p['title_zh']+'｜'+label,font=font,fill=fg)
 for col,(img,caption) in enumerate([(m,'母图 · 身份与原道具'),(im,'新动作 v'+v+' · 独立静态姿态')]):
  n=img.copy();n.thumbnail((900,670),Image.Resampling.NEAREST);panel.alpha_composite(n,(1000*col+(1000-n.width)//2,100+(670-n.height)//2));d.text((1000*col+60,61),caption,font=small,fill=fg)
 board.alpha_composite(panel,(0,row*800))
board.convert('RGB').save(o/'review'/f'{stem}_clean_light_dark.png')
print(json.dumps(record,ensure_ascii=False))
