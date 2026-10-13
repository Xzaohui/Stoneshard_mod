from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PAL=['#241e1d','#3b2c25','#554033','#76543c','#94704c','#b18b5a',
     '#675942','#484631','#34392e','#7d7159','#a89a7b','#c9b798','#e0d2b3','#f0e4cb']
rgb=np.array([tuple(bytes.fromhex(c[1:])) for c in PAL],dtype=np.int32)
src=Image.open(HERE/'concept_imagegen.png').convert('RGBA')
a=np.array(src); mask=a[:,:,3]>=128
ys,xs=np.where(mask); crop=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
small=src.crop(crop).resize((17,42),Image.Resampling.BOX)
arr=np.array(small); dist=((arr[:,:,:3,None].astype(np.int32)-rgb.T[None,None,:,:])**2).sum(axis=2)
out=np.zeros_like(arr); out[:,:,:3]=rgb[dist.argmin(axis=2)];out[:,:,3]=np.where(arr[:,:,3]>=128,255,0)
out[out[:,:,3]==0,:3]=0
canvas=Image.new('RGBA',(32,48));canvas.paste(Image.fromarray(out),(7,3))
canvas.save(HERE/'native_before_edits.png')
# Explicit per-pixel changes are versioned in edits.json; alpha zero preserves rope negative space.
edits=json.loads((HERE/'edits.json').read_text())
for e in edits:
    c=(0,0,0,0) if e['palette'] is None else (*rgb[e['palette']].tolist(),255)
    canvas.putpixel(tuple(e['xy']),c)
canvas.save(HERE/'native_32x48.png')
canvas.resize((256,384),Image.Resampling.NEAREST).save(HERE/'native_8x.png')
def backing(im,color):
    b=Image.new('RGBA',im.size,color);b.alpha_composite(im);return b.convert('RGB')
for name,col in [('neutral','#77766e'),('dark','#272c29'),('light','#cac6b8')]:
    backing(canvas,col).save(HERE/f'view_1x_{name}.png')
    backing(canvas,col).resize((256,384),Image.Resampling.NEAREST).save(HERE/f'view_8x_{name}.png')
qa={'canvas':list(canvas.size),'alpha_bbox':list(canvas.getbbox()),'visible_extent':[canvas.getbbox()[2]-canvas.getbbox()[0],canvas.getbbox()[3]-canvas.getbbox()[1]],'opaque_colors':len({p[:3] for p in canvas.getdata() if p[3]}),'alpha_values':sorted({p[3] for p in canvas.getdata()}),'concept_crop':crop,'resample':'BOX to 17x42; nearest fixed palette; threshold alpha at 128; explicit per-pixel edits; no smoothing','palette':PAL,'explicit_pixel_edits':len(edits),'runtime_verified':False,'engine_dimensions_verified':False}
(HERE/'qa_metrics.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
