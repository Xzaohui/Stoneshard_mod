#!/usr/bin/env python3
"""Deterministic, non-runtime Sela pixel study. Requires existing Pillow/NumPy/SciPy."""
from pathlib import Path
import hashlib,json,sys,argparse
from collections import Counter
import PIL
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import scipy
from scipy import ndimage as ndi
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
parser=argparse.ArgumentParser(); parser.add_argument('--out',type=Path,default=HERE)
OUT=parser.parse_args().out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch79/01_sela_sprite_calibration_v2.png'
PALETTE=[('outline','#201b1a'),('deep_brown','#35271f'),('hair_dark','#493028'),('hair_mid','#664333'),('hair_light','#815638'),('skin_shadow','#b36641'),('skin_mid','#db9461'),('skin_light','#efbb82'),('cape_dark','#1d3439'),('cape_mid','#30525b'),('cape_light','#416773'),('cloth_shadow','#998773'),('cloth_mid','#c5b699'),('cloth_light','#e9d9b6'),('trouser_dark','#4b413b'),('trouser_mid','#68584c'),('trouser_light','#82715e'),('leather_shadow','#5f3a25'),('leather_mid','#8f5832'),('leather_light','#b47c47'),('rope_shadow','#a5804e'),('rope_light','#d2ac70')]
COL=np.array([tuple(bytes.fromhex(h[1:])) for _,h in PALETTE],dtype=np.uint8)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_sha=sha(SRC)
a=np.array(Image.open(SRC).convert('RGB'))
# Flood only near-neutral mid/light pixels connected to the image boundary.
# This removes the gray field and enclosed leg gaps while retaining outlined clothing.
chroma=a.max(2).astype(int)-a.min(2)
background_candidate=(chroma<18)&(a.mean(2)>70)
l,n=ndi.label(background_candidate)
outer=np.unique(np.r_[l[0],l[-1],l[:,0],l[:,-1]])
mask=~np.isin(l,outer[outer!=0])
l,n=ndi.label(mask); sizes=np.bincount(l.ravel()); sizes[0]=0
mask=l==sizes.argmax()
ys,xs=np.where(mask); box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
rgba=np.dstack([a,mask.astype(np.uint8)*255]); rgba[~mask,:3]=0
Image.fromarray(rgba).save(OUT/'intermediate_cutout_full.png')
a=a[box[1]:box[3],box[0]:box[2]]; mask=mask[box[1]:box[3],box[0]:box[2]]
# Map source samples to a single authored palette. No dithering, no diffusion.
# Colour mapping uses weighted RGB squared distance, with green contributing more.
f=a.astype(np.float32); dist=((f[:,:,None,:]-COL[None,None,:,:])**2*np.array([0.8,1.2,1.0])).sum(3)
nearest=dist.argmin(2)
records=[]
for name,canvas,content in [('a_32x48',(32,48),(20,44)),('b_48x64',(48,64),(26,58))]:
 w,h=content; result=np.zeros((h,w,4),dtype=np.uint8)
 for y in range(h):
  for x in range(w):
   x0,x1=round(x*a.shape[1]/w),round((x+1)*a.shape[1]/w)
   y0,y1=round(y*a.shape[0]/h),round((y+1)*a.shape[0]/h)
   m=mask[y0:y1,x0:x1]; coverage=m.mean()
   if coverage>=0.45:
    codes=nearest[y0:y1,x0:x1][m]
    # Dominant colour cell, rather than averaging foreground with backdrop.
    index=int(np.bincount(codes,minlength=len(COL)).argmax())
    result[y,x]=[*COL[index],255]
 # Retain main 8-connected body only. Record components rather than silently deleting details.
 labels,n=ndi.label(result[:,:,3]>0,structure=np.ones((3,3),int))
 counts=np.bincount(labels.ravel()); counts[0]=0
 removed=[]
 for k in range(1,n+1):
  if counts[k]<=1:
   py,px=np.where(labels==k); removed.extend([[int(x),int(y)] for x,y in zip(px,py)]);result[labels==k]=0
 # Sole anchor is fixed in canvas coordinates, independently of engine origin.
 foot=(canvas[0]//2,canvas[1]-3);offset=((canvas[0]-w)//2,foot[1]-(h-1))
 im=Image.new('RGBA',canvas);im.paste(Image.fromarray(result),offset)
 im.save(OUT/f'{name}_baseline.png')
 # Explicit reviewed pixel edits. Palette assignments are semantic, not a claim of hand drawing.
 edits=[]
 def pixel(x,y,index,reason):
  before=list(im.getpixel((x,y))); after=([*map(int,COL[index]),255] if index is not None else [0,0,0,0])
  if before!=after: im.putpixel((x,y),tuple(after)); edits.append(dict(x=x,y=y,before=before,after=after,reason=reason))
 # The brown hair picked leather shades during automatic mapping. Consolidate to hair clusters.
 hair_y=14 if name.startswith('a') else 19
 for y in range(hair_y):
  for x in range(canvas[0]):
   c=im.getpixel((x,y))
   if c[3] and c[:3] in [tuple(COL[i]) for i in [17,18,19]]:
    pixel(x,y,3 if c[:3]==tuple(COL[17]) else 4,'Consolidate hair material into broad brown clusters')
 if name.startswith('a'):
  for x,y in [(13,8),(13,10)]:pixel(x,y,7,'Reduce long vertical eye to a single dark mark')
  for x,y in [(18,25),(18,26),(17,27),(17,28),(18,29),(18,30),(19,31),(20,31)]:pixel(x,y,21,'Reconstruct simple closed rope loop at native resolution')
  for x,y in [(19,27),(20,28),(20,29),(20,30)]:pixel(x,y,20,'Rope shadow side, same closed loop')
  for x,y in [(18,27),(18,28),(19,28),(19,29),(19,30)]:pixel(x,y,0,'Keep rope interior legible against trousers')
 else:
  for x,y in [(20,14),(20,15)]:pixel(x,y,7,'Reduce long vertical eye to a single dark mark')
  for x,y in [(26,35),(27,35),(25,36),(26,36),(25,37),(25,38),(25,39),(26,39),(26,40),(27,41),(28,42),(29,42)]:pixel(x,y,21,'Unify rope highlight independently of skin and hair')
  for x,y in [(27,36),(28,37),(28,38),(29,38),(29,39),(29,40),(28,41),(29,41)]:pixel(x,y,20,'Unify rope shaded edge')
  pixel(14,44,None,'Remove one diagonal contour snag below left mitten; keep bun strand')
 im.save(OUT/f'{name}_idle_view01_f000.png')
 (OUT/f'{name}_pixel_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
 records.append(dict(name=name,canvas=list(canvas),content_target=list(content),offset=list(offset),foot_anchor=list(foot),removed_singleton_alpha_pixels_content_coordinates=removed))
(OUT/'palette.json').write_text(json.dumps([{'index':i,'name':n,'hex':h} for i,(n,h) in enumerate(PALETTE)],indent=2)+'\n')
# Layout: both alternatives use integer scale 8, so relative pixel density stays visible.
board=Image.new('RGB',(900,640),'#f1e8d5');d=ImageDraw.Draw(board)
for r,ox in zip(records,[50,430]):
 im=Image.open(OUT/f"{r['name']}_idle_view01_f000.png")
 scale=8; big=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
 panel=Image.new('RGB',big.size);pd=ImageDraw.Draw(panel)
 for y in range(0,big.height,8):
  for x in range(0,big.width,8):pd.rectangle((x,y,x+7,y+7),fill=('#a6aaa7' if (x//8+y//8)%2 else '#bec1bb'))
 panel.paste(big,mask=big.getchannel('A'));panel.save(OUT/f"{r['name']}_preview_8x.png")
 board.paste(panel,(ox,65));d.text((ox,20),r['name']+' / nearest x8',fill='#27241f')
 anchor=r['foot_anchor']; ay=65+(anchor[1]+1)*8;d.line((ox,ay,ox+big.width,ay),fill='#a74238',width=1)
 d.text((ox,ay+10),f"Sole datum y={anchor[1]}, origin unknown",fill='#27241f')
 d.text((ox,600),'SCRIPT-ASSISTED PIXEL STUDY / NOT RUNTIME',fill='#27241f')
board.save(OUT/'comparison.png')
checks=[]
for r in records:
 p=OUT/f"{r['name']}_idle_view01_f000.png";im=Image.open(p);arr=np.array(im);visible=arr[:,:,3]>0;ys,xs=np.where(visible)
 counts=Counter(map(tuple,arr[visible,:3]));components,n=ndi.label(visible,structure=np.ones((3,3),int))
 r.update(filename=p.name,sha256=sha(p),visible_bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],visible_color_count=len(counts),alpha_values=np.unique(arr[:,:,3]).tolist(),visible_pixels=int(visible.sum()),eight_connected_components=n,engine_origin=None,collision=None,runtime_verified=False)
 r['checks']={'binary_alpha':set(r['alpha_values'])=={0,255},'palette_subset':all(c in map(tuple,COL) for c in counts),'sole_row_matches_anchor':int(ys.max())==r['foot_anchor'][1],'clear_canvas_border':not (visible[0].any() or visible[-1].any() or visible[:,0].any() or visible[:,-1].any()),'transparent_rgb_zero':bool((arr[~visible,:3]==0).all()),'single_connected_body':n==1}
 assert all(r['checks'].values()),r
manifest={'status':'script_assisted_pixel_pilot_visual_reviewed_not_runtime','scope':'Sela idle view01 frame 0; two experimental canvases; not a native engine specification','method':'Boundary-connected gray extraction; fixed semantic palette; foreground dominant-area cell sampling; no dithering; explicit semantic hair, eye, rope and contour pixel corrections','source':{'path':str(SRC.relative_to(ROOT)),'sha256':source_sha,'crop_bbox':box},'parameters':{'background_chroma_lt':18,'background_mean_gt':70,'cell_alpha_coverage_gte':0.45,'palette_distance_weights':[0.8,1.2,1.0],'dither':False},'versions':{'python':sys.version.split()[0],'pillow':PIL.__version__,'numpy':np.__version__,'scipy':scipy.__version__},'candidates':records,'script_sha256':sha(Path(__file__)),'source_unchanged':sha(SRC)==source_sha,'runtime_changes':False,'global_concept_index_changes':False}
manifest['artifacts']={p.name:sha(p) for p in OUT.glob('*.png')}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
