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
protected={str(p.relative_to(ROOT)):sha(p) for p in [SRC,*PILOT.glob('*')] if p.is_file()}
palette=json.loads((PILOT/'palette.json').read_text());COL=np.array([tuple(bytes.fromhex(p['hex'][1:])) for p in palette],dtype=np.uint8)
a=np.array(Image.open(SRC).convert('RGB'))
bg=(a.max(2).astype(int)-a.min(2)<18)&(a.mean(2)>70)
l,n=ndi.label(bg);outer=np.unique(np.r_[l[0],l[-1],l[:,0],l[:,-1]]);mask=~np.isin(l,outer[outer!=0]);l,n=ndi.label(mask);sizes=np.bincount(l.ravel());sizes[0]=0;mask=l==sizes.argmax()
im=Image.new('RGBA',(35,44))
segments=[dict(name='head_hair_chin',source_box=[458,228,820,463],target_box=[8,4,27,19]),dict(name='neck_cape_rolls_belt',source_box=[458,463,820,688],target_box=[9,19,26,29]),dict(name='hands_rope_trousers_boots',source_box=[458,688,820,1055],target_box=[9,29,26,38])]
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
for y in range(19):
 for x in range(35):
  c=im.getpixel((x,y))
  if c[3] and c[:3] in [tuple(COL[i]) for i in [17,18,19]]:pixel(x,y,3 if c[:3]==tuple(COL[17]) else 4,'Consolidate source hair into shared brown hair ramps')
# Reviewed native edits: keep three-quarter left-facing adult face, not a new front view.
pixel(15,13,7,'Shorten two-row source eye into a single eye mark')
pixel(16,12,6,'Separate eye from temple hair with a skin side-plane')
pixel(12,14,7,'Recover one-pixel nose projection from source profile')
pixel(16,15,6,'Add cheek side-plane using existing skin ramp')
pixel(14,16,5,'Compact mouth accent below nose; existing skin shadow')
pixel(15,16,6,'Soften mouth transition without new palette color')
pixel(16,17,6,'Chin side-plane; keep adult jaw outline')
for x,y,c in [(11,30,6),(11,31,5),(23,30,6),(23,31,5)]:pixel(x,y,c,'Recover palm width and hand shadow after lower-band compression')
for x,y,c in [(20,28,21),(20,29,20),(19,30,21),(19,31,21),(20,32,21),(21,31,20),(21,30,20),(20,30,0),(20,31,0)]:pixel(x,y,c,'Reconstruct compact waist-rope knot and loop; no added equipment')
pixel(16,25,12,'Merge isolated shirt shade into larger linen midtone cluster')
pixel(18,26,12,'Clarify shirt and waistband separation with shared linen tone')
im.save(OUT/'sela_structural_idle_view01_f000.png')
(OUT/'pixel_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(OUT/'palette.json').write_text(json.dumps(palette,indent=2)+'\n')
refs=[('Gunda','Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png'),('Jurg','Assets/ReferenceAudit/20261013/originals/s_npc_carpenter_0.png'),('Frid','Assets/ReferenceAudit/20261013/originals/s_npc_herbalist_0.png'),('Old C',str((PILOT/'c_32x48_reference_budget_idle_view01_f000.png').relative_to(ROOT)))]
items=[(name,Image.open(ROOT/path).convert('RGBA')) for name,path in refs]+[('Sela structure',im)]
# Equal canvas and sole; no per-item display zoom.
aligned=[]
for name,img in items:
 b=img.getbbox();c=Image.new('RGBA',(35,44));crop=img.crop(b);c.paste(crop,((35-crop.width)//2,38-crop.height));aligned.append((name,c))
for scale,filename in [(8,'comparison_ground_aligned_8x.png'),(1,'comparison_native_1x.png')]:
 cell=35*scale+24;board=Image.new('RGB',(cell*len(items)+20,44*scale+78),'#b3b5ad');d=ImageDraw.Draw(board)
 for k,(name,img) in enumerate(aligned):
  ox=10+k*cell;oy=35;large=img.resize((35*scale,44*scale),Image.Resampling.NEAREST);board.paste(large,(ox,oy),large);d.text((ox,9),name if scale==8 else name.replace('Sela structure','Sela'),fill='#201b1a');d.line((ox,oy+38*scale,ox+35*scale,oy+38*scale),fill='#95513f')
 d.text((10,board.height-20),f'Same ground / nearest x{scale} / structural candidate, not accepted' if scale==8 else 'Native x1 / same ground / candidate',fill='#201b1a');board.save(OUT/filename)
big=im.resize((280,352),Image.Resampling.NEAREST);bg=Image.new('RGB',big.size,'#b3b5ad');bg.paste(big,(0,0),big);bg.save(OUT/'sela_structural_preview_8x.png')
arr=np.array(im);v=arr[:,:,3]>0;ys,xs=np.where(v);_,n=ndi.label(v,structure=np.ones((3,3),int));colors=set(map(tuple,arr[v,:3]))
qa=dict(canvas=list(im.size),visible_bbox=list(im.getbbox()),visible_height=int(ys.max()-ys.min()+1),visible_width=int(xs.max()-xs.min()+1),colors=len(colors),visible_pixels=int(v.sum()),eight_connected_components=n,alpha_values=np.unique(arr[:,:,3]).tolist(),dither=False,runtime_verified=False,original_style_accepted=False,engine_origin=None,collision=None)
qa['checks']=dict(binary_alpha=set(qa['alpha_values'])=={0,255},palette_subset=colors.issubset(set(map(tuple,COL))),transparent_rgb_zero=bool((arr[~v,:3]==0).all()),height_34=qa['visible_height']==34,sole_row_37=int(ys.max())==37,single_body=n==1,protected_inputs_unchanged=all(sha(ROOT/path)==h for path,h in protected.items()))
assert all(qa['checks'].values()),qa
(OUT/'QA-producer.json').write_text(json.dumps(qa,indent=2)+'\n')
manifest=dict(status='structural_rearrangement_candidate_not_original_style_acceptance',source=dict(path=str(SRC.relative_to(ROOT)),sha256=sha(SRC)),segments=segments,method='Re-extract gray background from full source. Per-segment weighted RGB palette mapping, dominant area cells, coverage >=0.45; explicit per-pixel corrections. No old-C upscaling.',transformation_note='Head full crop width19 vs body17; source neck y463 and waist y688 approximate, chosen for this pose only. Head15 / neck-to-belt10 / hands-legs9 non-overlap bands; anatomical parts overlap these semantic bands.',references=[dict(name=name,path=path,sha256=sha(ROOT/path),copied_pixels=False) for name,path in refs],protected_inputs=protected,script_sha256=sha(Path(__file__)),artifacts={p.name:sha(p) for p in OUT.glob('*.png')},runtime_changes=False)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(qa,indent=2))
