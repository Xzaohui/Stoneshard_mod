from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent
palette=['18151c','302328','51372e','744a32','975e3d','be8054','713f33','a45640','c07952','f3ac78','e28671','ad6259','6d5150','514138','726156','8c8378','666970','b2b0a7']
pal=np.array([tuple(bytes.fromhex(s)) for s in palette],dtype=np.int32)
im=Image.open(D/'anla_redraw_concept_v2.png').convert('RGBA');bbox=(507,84,989,976)
p=im.crop(bbox).resize((20,34),Image.Resampling.NEAREST);a=np.array(p);rgb=a[:,:,:3].astype(np.int32);ix=((rgb[:,:,None,:]-pal[None,None,:,:])**2).sum(3).argmin(2);a[:,:,:3]=pal[ix];a[:,:,3]=np.where(a[:,:,3]>=128,255,0)
out=Image.new('RGBA',(35,44));out.alpha_composite(Image.fromarray(a),(8,4));out.save(D/'anla_native_v3_baseline.png')
edits=[]
def put(x,y,c,reason):
 out.putpixel((x,y),tuple(pal[c])+(255,) if c>=0 else (0,0,0,0));edits.append({'x':x,'y':y,'palette':c,'reason':reason})
# Native-scale edits: legibility of the clasp, split apron and belt stamp.
for x,y,c in [(17,26,17),(18,26,16),(17,27,16),(18,27,17),(19,26,0),(19,27,2)]:put(x,y,c,'two-by-two ordinary steel clasp and separating edge')
for yy in (30,31,32):
 for xx in (15,16,17,18):put(xx,yy,3 if xx in (16,17) else 2,'flat left leather apron panel')
 for xx in (20,21,22):put(xx,yy,3 if xx==21 else 2,'flat right leather apron panel')
 put(19,yy,0 if yy==32 else 1,'short split apron seam')
for x,y,c in [(24,28,16),(24,29,2),(24,30,2)]:put(x,y,c,'one small belt stamp silhouette')

out.save(D/'anla_native_v3.png');out.resize((280,352),Image.Resampling.NEAREST).save(D/'anla_native_v3_8x.png')
R=D.parents[2]/'ReferenceAudit'/'20261013'/'originals'
items=[('Anla v3 / redraw',D/'anla_native_v3.png'),('Gunda / original',R/'s_peasantfemale_09_0.png'),('Jurg / original',R/'s_npc_carpenter_0.png'),('Frid / original',R/'s_npc_herbalist_0.png')]
board=Image.new('RGB',(1120,405),(77,77,82));dr=ImageDraw.Draw(board)
for i,(label,fp) in enumerate(items):
 p=Image.open(fp).convert('RGBA').resize((280,352),Image.Resampling.NEAREST);board.paste(p,(i*280,30),p);dr.text((i*280+12,9),label,fill='white');dr.line((i*280,334,(i+1)*280-1,334),fill=(96,103,103))
board.save(D/'comparison_native_v3_8x.png')
(D/'geometry_v3.json').write_text(json.dumps({'source':'anla_redraw_concept_v2.png','crop':bbox,'canvas':[35,44],'native_body_size':[20,34],'paste':[8,4],'feet_bottom_exclusive':38,'palette':palette,'alpha_threshold':128,'filter':'NEAREST','dither':False,'pixel_edits':edits,'warning':'reference-budget study, not engine standard or runtime-approved asset'},indent=2))
