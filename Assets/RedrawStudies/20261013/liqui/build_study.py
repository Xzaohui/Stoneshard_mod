from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, json, hashlib
D=Path(__file__).resolve().parent
R=D.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=np.array(Image.open(D/'liqui_structure_concept_v2.png').convert('RGBA'))
# Generated transparent edge alpha is thresholded; do not interpret subthreshold dust as anatomy.
m=a[:,:,3]>128; yy,xx=np.where(m); box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1))
a[:,:,3]=np.where(m,255,0)
im=Image.fromarray(a).crop(box).resize((20,34),Image.Resampling.NEAREST)
pal=['21191c','382322','613b2d','925039','b4774e','e8a06e','f3bb85','c57755','334037','4c5944','697351','896629','b18739','604632','876246','b68b58','453c37','87766a']
p=np.array([tuple(bytes.fromhex(c)) for c in pal],dtype=np.int32)
b=np.array(im); dist=((b[:,:,:3,None].astype(int)-p.T[None,None,:,:])**2).sum(axis=2); ids=dist.argmin(axis=2); b[:,:,:3]=p[ids]; b[b[:,:,3]==0,:3]=0
out=Image.new('RGBA',(35,44)); out.paste(Image.fromarray(b),(8,4)); out.save(D/'liqui_native_before_pixel_edits.png'); out.resize((560,704),Image.Resampling.NEAREST).save(D/'liqui_before_preview.png')
# Pixel edits applied below after inspection; each entry stores explicit before/after values.
edits=[]
for item in json.loads((D/'pixel_edits_spec.json').read_text()) if (D/'pixel_edits_spec.json').exists() else []:
 x,y,color,reason=item; old=out.getpixel((x,y)); new=tuple(bytes.fromhex(color))+(255,) if color else (0,0,0,0)
 if old!=new: out.putpixel((x,y),new);edits.append({'x':x,'y':y,'before':old,'after':new,'reason':reason})
out.save(D/'liqui_native_v1.png'); out.resize((560,704),Image.Resampling.NEAREST).save(D/'liqui_native_preview_16x.png')
(D/'pixel_edit_log.json').write_text(json.dumps({'source_concept':'liqui_structure_concept_v2.png','crop_alpha_threshold':128,'crop_box':box,'sampling':'NEAREST 20x34 then palette nearest RGB distance, positioned at (8,4) on 35x44 research canvas','palette':pal,'edits':edits},ensure_ascii=False,indent=2))
print('bbox',out.getbbox(),'colors',len(out.getcolors()),'edits',len(edits))
