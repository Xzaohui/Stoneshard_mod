from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).parent

def stats(p):
 im=Image.open(p).convert('RGBA'); px=list(im.getdata()); a=im.getchannel('A')
 return dict(path=str(p.relative_to(ROOT)),size=list(im.size),mode='RGBA',visible_rgb_colors=len({v[:3] for v in px if v[3]}),alpha_values=sorted(set(a.getdata())),alpha_bbox=a.getbbox(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def export(name,size,ncolors):
 source=ROOT/'raw'/f'{name}.png'; im=Image.open(source).convert('RGBA')
 # Authorized deterministic derivative only: no hand-painted features, geometry or pixel edits.
 small=im.resize(size,Image.Resampling.NEAREST)
 alpha=small.getchannel('A').point(lambda v:255 if v>=128 else 0)
 positions=[i for i,v in enumerate(alpha.getdata()) if v]
 pixels=list(small.getdata()); visible=Image.new('RGB',(len(positions),1)); visible.putdata([pixels[i][:3] for i in positions])
 quant=visible.quantize(colors=ncolors,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
 result=[(0,0,0,0)]*(size[0]*size[1])
 for i,rgb in zip(positions,quant.getdata()):result[i]=(*rgb,255)
 out=Image.new('RGBA',size);out.putdata(result)
 dest=ROOT/'assets'/f'{name}_{size[0]}x{size[1]}.png';out.save(dest)
 out.resize((size[0]*8,size[1]*8),Image.Resampling.NEAREST).save(ROOT/'previews'/f'{name}_8x.png')
 # QA panel contains unmodified 1x and integer nearest enlargement over neutral ground.
 panel=Image.new('RGB',(size[0]*8+170,size[1]*8+50),(91,91,91)); d=ImageDraw.Draw(panel)
 d.text((12,10),f'{name}: 1x',fill='white');d.text((154,10),'8x nearest',fill='white')
 panel.paste(out,(12,36),out);big=out.resize((size[0]*8,size[1]*8),Image.Resampling.NEAREST);panel.paste(big,(154,36),big)
 panel.save(ROOT/'previews'/f'{name}_1x_8x.png')
 report={'source':stats(source),'target':stats(dest),'derivation':{'resize':'nearest-neighbor entire raw canvas','crop':None,'alpha':'threshold 128','palette':'median-cut visible sampled pixels','dither':False,'drawn_character_geometry':False},'source_is_native_target_dimensions':im.size==size,'native_pixel_grid_claim':False,'quality_decision':'pending visual review'}
 (ROOT/'qa'/f'{name}_metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
 import sys
 name=sys.argv[1]; kind='portrait' if name.startswith('portrait') else 'map'
 export(name,(74,100) if kind=='portrait' else (35,44),32 if kind=='portrait' else 20)
