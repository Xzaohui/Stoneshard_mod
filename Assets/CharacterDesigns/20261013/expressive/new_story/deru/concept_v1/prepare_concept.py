from pathlib import Path
from PIL import Image, ImageDraw
import json,hashlib,sys,datetime,shutil
who=sys.argv[1]; version=int(sys.argv[2]); root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1'; raw=d/f'{who}_v{version}_raw_imagegen.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.open(raw).convert('RGBA');a=im.getchannel('A'); hist=a.histogram(); changed=sum(hist[1:9]); im.putalpha(a.point(lambda x:0 if x<=8 else x)); output=d/f'{who}_transparent.png';im.save(output)
boards=[]
for name,color in [('light',(236,230,215,255)),('dark',(35,40,43,255))]:
 canvas=Image.new('RGBA',(im.width+160,im.height+160),color);canvas.alpha_composite(im,(80,80));p=d/f'{who}_{name}_board.png';canvas.convert('RGB').save(p);boards.append(p.name)
(d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes())
log={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation':'Preserve raw; transparent output zeros only alpha values <=8; RGB unchanged, alpha>8 unchanged. No crop, body/face drawing, quantization, resampling, or regional transformation. Boards composite same-size complete image onto light/dark background with 80px margins.','selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_1_to_8_cleared_pixels':changed,'output':output.name,'output_sha256':sha(output),'boards':boards,'generator':'built-in image_gen.imagegen','runtime_verified':False,'equipment_compatibility':'unknown','status':'pending final independent review; no upload/commit/push'}
(d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(log,ensure_ascii=False))
