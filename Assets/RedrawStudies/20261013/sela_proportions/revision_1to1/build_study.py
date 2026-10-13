#!/usr/bin/env python3
"""Sela single-pose structural study. Does not write source/pilots/runtime."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE);OUT=p.parse_args().out.resolve();OUT.mkdir(parents=True,exist_ok=True)
PILOT=ROOT/'src/EmbersAndOaths/Assets/PixelPilots/20261013/sela'
SRC=ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch79/01_sela_sprite_calibration_v2.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
OLD=HERE.parent
protected={str(p.relative_to(ROOT)):sha(p) for p in [SRC,*PILOT.glob('*'),*OLD.glob('*')] if p.is_file()}
palette=json.loads((PILOT/'palette.json').read_text());COL=np.array([tuple(bytes.fromhex(p['hex'][1:])) for p in palette],dtype=np.uint8)
a=np.array(Image.open(SRC).convert('RGB'))
bg=(a.max(2).astype(int)-a.min(2)<18)&(a.mean(2)>70)
l,n=ndi.label(bg);outer=np.unique(np.r_[l[0],l[-1],l[:,0],l[:,-1]]);mask=~np.isin(l,outer[outer!=0]);l,n=ndi.label(mask);sizes=np.bincount(l.ravel());sizes[0]=0;mask=l==sizes.argmax()
im=Image.new('RGBA',(35,44))
segments=[dict(name='head_hair_true_chin',source_box=[458,228,820,450],target_box=[5,4,29,21]),dict(name='compressed_neck',source_box=[458,450,820,515],target_box=[9,21,26,22]),dict(name='cape_rolls_belt',source_box=[458,515,820,688],target_box=[9,22,26,29]),dict(name='hands_rope_trousers_boots',source_box=[458,688,820,1055],target_box=[9,29,26,38])]
for s in segments:
 x0,y0,x1,y1=s['source_box'];tx,ty,tx1,ty1=s['target_box'];w,h=tx1-tx,ty1-ty
 rgb=a[y0:y1,x0:x1];m=mask[y0:y1,x0:x1];f=rgb.astype(float)
 nearest=(((f[:,:,None,:]-COL[None,None,:,:])**2)*np.array([.8,1.2,1])).sum(3).argmin(2)
 for y in range(h):
  for x in range(w):
   sx0,sx1=round(x*rgb.shape[1]/w),round((x+1)*rgb.shape[1]/w);sy0,sy1=round(y*rgb.shape[0]/h),round((y+1)*rgb.shape[0]/h)
   visible=m[sy0:sy1,sx0:sx1]
   if visible.mean()>=.45:
    idx=int(np.bincount(nearest[sy0:sy1,sx0:sx1][visible],minlength=len(COL)).argmax());im.putpixel((tx+x,ty+y),tuple(map(int,COL[idx]))+(255,))
im.save(OUT/'sela_structural_baseline.png');edits=[]
def pixel(x,y,index,reason):
 before=list(im.getpixel((x,y)));after=[*map(int,COL[index]),255] if index is not None else [0,0,0,0]
 if before!=after:im.putpixel((x,y),tuple(after));edits.append(dict(x=x,y=y,before=before,after=after,reason=reason))
for y in range(21):
 for x in range(35):
  c=im.getpixel((x,y))
  if c[3] and c[:3] in [tuple(COL[i]) for i in [17,18,19]]:pixel(x,y,3 if c[:3]==tuple(COL[17]) else 4,'Consolidate source hair into shared brown hair ramps')
# Keep the old warm palette; only geometry/readability repairs.
for x,y,c in [(14,13,6),(15,13,6),(13,15,7),(14,15,7),(14,16,7)]:pixel(x,y,c,'Separate one horizontal eye mark from source long vertical eye and fringe')
pixel(10,17,7,'Recover nose projection in widened face')
pixel(16,17,6,'Cheek side-plane with unchanged skin ramp')
pixel(12,18,5,'Single compact mouth accent with existing skin shadow')
pixel(13,18,6,'Mouth transition, unchanged palette')
pixel(12,20,6,'Broaden jaw instead of stretching a narrow pointed chin')
for x,y,c in [(11,30,6),(11,31,5),(23,30,6),(23,31,5)]:pixel(x,y,c,'Retain prior candidate palm width and hand shadows')
for x,y,c in [(20,28,21),(20,29,20),(19,30,21),(19,31,21),(20,32,21),(21,31,20),(21,30,20),(20,30,0),(20,31,0)]:pixel(x,y,c,'Retain prior waist-rope knot and loop; no added equipment')
im.save(OUT/'sela_structural_idle_view01_f000.png')
(OUT/'pixel_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(OUT/'palette.json').write_text(json.dumps(palette,indent=2)+'\n')
refs=[('Gunda','Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png'),('Bert','Assets/ReferenceAudit/20261013/originals/s_npc_merchant01_0.png'),('Prior Sela',str((OLD/'sela_structural_idle_view01_f000.png').relative_to(ROOT)))]
items=[(name,Image.open(ROOT/path).convert('RGBA')) for name,path in refs]+[('Sela 1to1',im)]
# Equal canvas and sole; no per-item display zoom.
aligned=[]
for name,img in items:
 b=img.getbbox();c=Image.new('RGBA',(35,44));crop=img.crop(b);c.paste(crop,((35-crop.width)//2,38-crop.height));aligned.append((name,c))
for scale,filename in [(8,'comparison_ground_aligned_8x.png'),(1,'comparison_native_1x.png')]:
 cell=35*scale+24;board=Image.new('RGB',(cell*len(items)+20,44*scale+78),'#b3b5ad');d=ImageDraw.Draw(board)
 for k,(name,img) in enumerate(aligned):
  ox=10+k*cell;oy=35;large=img.resize((35*scale,44*scale),Image.Resampling.NEAREST);board.paste(large,(ox,oy),large);d.text((ox,9),name if scale==8 else name.replace('Sela 1to1','Sela'),fill='#201b1a');d.line((ox,oy+38*scale,ox+35*scale,oy+38*scale),fill='#95513f')
 d.text((10,board.height-20),f'Same ground / nearest x{scale} / structural candidate, not accepted' if scale==8 else 'Native x1 / same ground / candidate',fill='#201b1a');board.save(OUT/filename)
big=im.resize((280,352),Image.Resampling.NEAREST);bg=Image.new('RGB',big.size,'#b3b5ad');bg.paste(big,(0,0),big);bg.save(OUT/'sela_structural_preview_8x.png')

landmarks=[dict(name='Gunda',crown_y=4,last_chin_skin_y=20,chin_outline_y=21,sole_y=37,head_pixels=17,below_chin_pixels=17,head_to_body_ratio=1.0,skull_width_approx=16,shoulder_width_approx=18),dict(name='Bert',crown_y=4,last_chin_skin_y=20,chin_outline_y=21,sole_y=37,head_pixels=17,below_chin_pixels=17,head_to_body_ratio=1.0,skull_width_approx=17,shoulder_width_approx=18),dict(name='Prior Sela',crown_y=4,last_chin_skin_y=17,chin_outline_y=18,sole_y=37,head_pixels=14,below_chin_pixels=20,head_to_body_ratio=.7,skull_width_approx=12,shoulder_width_approx=16),dict(name='Sela 1to1',crown_y=4,last_chin_skin_y=20,chin_outline_y=21,sole_y=37,head_pixels=17,below_chin_pixels=17,head_to_body_ratio=1.0,skull_x_inclusive=[8,22],skull_width_approx=15,bun_x_inclusive=[23,27],shoulder_x_inclusive=[10,25],shoulder_width_approx=16,independent_neck_rows=[21])]
(OUT/'landmarks.json').write_text(json.dumps(dict(coordinates='original 35x44 canvas; y down; ranges inclusive; chin skin excludes neck; references +/-1 pixel interpretive uncertainty',measurements=landmarks),indent=2)+'\n')
for scale,filename in [(8,'comparison_landmarks_8x.png'),(1,'comparison_landmarks_1x.png')]:
 cell=35*scale+24;board=Image.new('RGB',(cell*len(items)+20,44*scale+112),'#b3b5ad');d=ImageDraw.Draw(board)
 for k,((name,img),m) in enumerate(zip(aligned,landmarks)):
  ox=10+k*cell;oy=35;large=img.resize((35*scale,44*scale),Image.Resampling.NEAREST);board.paste(large,(ox,oy),large);d.text((ox,9),name if scale==8 else ['Gunda','Bert','Prior','New'][k],fill='#201b1a')
  for yy,col in [(4,'#466e95'),(m['last_chin_skin_y']+1,'#a33e71'),(38,'#95513f')]:
   for x in range(ox,ox+35*scale,4*scale):d.line((x,oy+yy*scale,min(x+2*scale,ox+35*scale),oy+yy*scale),fill=col)
  label=f"{m['head_pixels']}:{m['below_chin_pixels']}"
  d.text((ox,oy+44*scale+4),label,fill='#201b1a')
  if scale==8:d.text((ox,oy+44*scale+20),f"Crown4 / chin{m['last_chin_skin_y']} / sole37",fill='#201b1a')
 d.text((10,board.height-18),'Blue crown / pink below chin / red sole' if scale==8 else 'Head:body / chin marked',fill='#201b1a');board.save(OUT/filename)

arr=np.array(im);v=arr[:,:,3]>0;ys,xs=np.where(v);_,n=ndi.label(v,structure=np.ones((3,3),int));colors=set(map(tuple,arr[v,:3]))
qa=dict(canvas=list(im.size),visible_bbox=list(im.getbbox()),visible_height=int(ys.max()-ys.min()+1),visible_width=int(xs.max()-xs.min()+1),colors=len(colors),visible_pixels=int(v.sum()),eight_connected_components=n,alpha_values=np.unique(arr[:,:,3]).tolist(),dither=False,runtime_verified=False,original_style_accepted=False,engine_origin=None,collision=None)
qa['checks']=dict(binary_alpha=set(qa['alpha_values'])=={0,255},palette_subset=colors.issubset(set(map(tuple,COL))),transparent_rgb_zero=bool((arr[~v,:3]==0).all()),height_34=qa['visible_height']==34,sole_row_37=int(ys.max())==37,single_body=n==1,protected_inputs_unchanged=all(sha(ROOT/path)==h for path,h in protected.items()))
assert all(qa['checks'].values()),qa
(OUT/'QA-producer.json').write_text(json.dumps(qa,indent=2)+'\n')
manifest=dict(status='structural_rearrangement_candidate_not_original_style_acceptance',source=dict(path=str(SRC.relative_to(ROOT)),sha256=sha(SRC)),segments=segments,method='Re-extract gray background from full source. Per-segment weighted RGB palette mapping, dominant area cells, coverage >=0.45; explicit per-pixel corrections. No old-C upscaling.',transformation_note='Head full crop width24 vs body17; visible jaw source skin ends ~449; head crop stops450 and maps skin chin to row20. Outline and short neck source450..515 map to row21. Head maps to17 rows, independent neck to1 row, cape-to-belt7 rows, hands-legs9 rows. Skull excludes right bun; anatomy verified visually, not inferred from these bands alone.',references=[dict(name=name,path=path,sha256=sha(ROOT/path),copied_pixels=False) for name,path in refs],protected_inputs=protected,script_sha256=sha(Path(__file__)),artifacts={p.name:sha(p) for p in OUT.glob('*.png')},runtime_changes=False)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(qa,indent=2))
