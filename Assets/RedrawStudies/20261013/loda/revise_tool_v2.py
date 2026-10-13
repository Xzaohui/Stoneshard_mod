from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);a=p.parse_args();base=a.base;out=a.output or base/'v2';out.mkdir(parents=True,exist_ok=True)
src=base/'loda_native_v1.png';before=Image.open(src).convert('RGBA');im=before.copy();d=ImageDraw.Draw(im)
# Remove old hammer only and repair apron edge/empty space. Hand above is untouched.
changes={(8,28):(221,160,113,255),(9,28):(221,160,113,255),(10,28):(189,121,81,255),(8,29):(189,121,81,255),(9,29):(189,121,81,255),(10,29):(189,121,81,255),(8,30):(0,0,0,0),(9,30):(0,0,0,0),(10,30):(48,40,35,255),(8,31):(0,0,0,0),(9,31):(0,0,0,0),(10,31):(0,0,0,0),(8,32):(0,0,0,0),(9,32):(0,0,0,0)}
for xy,col in changes.items():im.putpixel(xy,col)
# A single restrained hanging hammer, a separated metal crosshead and short wooden shaft.
# y30 negative space below hand over x5..9. Thin hanger joins belt at x10 only.
d=ImageDraw.Draw(im);d.point((10,31),fill='#543a28');d.line((5,31,9,31),fill='#302823');d.line((6,31,8,31),fill='#afb1a0');d.line((6,32,8,32),fill='#302823');d.line((7,32,7,33),fill='#976b44');d.point((7,34),fill='#302823')
im.save(out/'loda_native_v2.png');im.save(out/'loda_1x.png');im.resize((280,352),Image.Resampling.NEAREST).save(out/'loda_8x.png')
diff=[{'x':x,'y':y,'before':list(before.getpixel((x,y))),'after':list(im.getpixel((x,y)))} for y in range(44) for x in range(35) if before.getpixel((x,y))!=im.getpixel((x,y))]
for scale in [1,8]:
 w=max(170,35*scale+35);s=Image.new('RGB',(w*2,44*scale+60),'#ddddda');sd=ImageDraw.Draw(s)
 for i,(label,img) in enumerate([('v1: tool near hand',before),('v2: separate crosshead',im)]):
  img=img.resize((35*scale,44*scale),Image.Resampling.NEAREST);s.paste(img,(i*w+20,25),img);sd.text((i*w+10,8),label,fill='#202020');sd.line((i*w,25+38*scale,(i+1)*w-1,25+38*scale),fill='#aa4b48')
 s.save(out/f'tool_before_after_{scale}x.png')
# Exact unchanged-region assertions, not a whole-character redraw.
for name,box in {'head_face':(0,0,35,28),'rope':(22,27,29,34),'feet':(0,35,35,44)}.items():
 assert before.crop(box).tobytes()==im.crop(box).tobytes(),name
m={'method':'Local manual hammer separation only; original v1 kept byte-for-byte. No image generation.','changed_pixels':diff,'changed_pixel_count':len(diff),'unchanged_regions_verified':{'head_face_y0_27':True,'rope_x22_28_y27_33':True,'feet_y35_43':True},'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}}
(out/'tool_pixel_diff.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print('changed',len(diff))
