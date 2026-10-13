#!/usr/bin/env python3
"""One-time RGB art pass over immutable native-study masks; no per-frame filters."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_fill_holes, label
sha=lambda b:hashlib.sha256(b).hexdigest()
def snapshot(p): return {str(f.relative_to(p)):sha(f.read_bytes()) for f in sorted(p.rglob('*')) if f.is_file()}
def palette(a): return sorted({tuple(map(int,c)) for c in a[a[:,:,3]>0,:3]})
def component_counts(a):
 out={'singleton':0,'two_to_four':0,'five_plus':0}
 for c in palette(a):
  lab,n=label(np.all(a[:,:,:3]==c,axis=2)&(a[:,:,3]>0))
  sz=np.bincount(lab.ravel())[1:];out['singleton']+=int((sz==1).sum());out['two_to_four']+=int(((sz>=2)&(sz<=4)).sum());out['five_plus']+=int((sz>=5).sum())
 return out

def paint(a,n):
 from scipy.ndimage import gaussian_filter, binary_opening, minimum_filter, distance_transform_edt
 h,w=a.shape[:2];m=a[:,:,3]>0
 # New texture proposal: source-informed washes and sparse fiber clusters.
 # Five restrained values per sheet, no regular perimeter highlight.
 colors={'A':[(229,185,118),(225,180,113),(233,191,126),(218,170,102),(202,152,89)],'B':[(239,210,161),(235,204,151),(243,216,172),(230,195,138),(221,179,115)]}[n]
 lum=a[:,:,:3].astype(float).mean(axis=2)
 # Remove cut-outs from analysis only, never from actual mask.
 med=np.median(lum[m]);lum[~m]=med
 interior=np.zeros(m.shape,bool);interior[5:-5,5:-5]=True;interior &=m
 field=gaussian_filter(lum,3.0)
 lo,hi=np.percentile(field[interior],[25,80])
 shade=binary_opening(field<lo,structure=np.ones((2,2)))&m
 light=binary_opening(field>hi,structure=np.ones((2,2)))&m
 rgb=np.zeros((h,w,3),dtype='uint8');rgb[:]=colors[0];rgb[shade]=colors[1];rgb[light]=colors[2]
 # Worn perimeter follows old dark pigment, with no synthetic straight bevel.
 yy,xx=np.indices(m.shape);outer=np.minimum.reduce([xx,yy,w-1-xx,h-1-yy])
 edge=(outer<=2)&m&(lum<np.percentile(lum[m],12))
 labs,k=label(edge)
 for j in range(1,k+1):
  region=labs==j
  rgb[region]=colors[4] if region.sum()>=3 else colors[1]
 # Select low-tone source positions, spaced apart, then paint a few short
 # irregular fiber clusters, rather than scatter independent noise pixels.
 small=gaussian_filter(lum,1.1);score=small-gaussian_filter(lum,5)
 candidates=np.argwhere(interior & (score==minimum_filter(score,size=9)))
 candidates=sorted(candidates,key=lambda yx:score[tuple(yx)])
 chosen=[]
 templates=[[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(3,1)],[(0,0),(1,0),(1,1),(2,1),(3,1),(4,1)],[(0,0),(1,0),(0,1),(1,1),(2,1),(2,2),(3,2)],[(0,0),(1,0),(2,0),(3,0),(4,0),(1,1),(2,1)]]
 for y,x in candidates:
  if any((x-px)**2+(y-py)**2<15**2 for py,px in chosen):continue
  chosen.append((int(y),int(x)))
  for dx,dy in templates[(len(chosen)-1)%len(templates)]:
   if m[y+dy,x+dx]:rgb[y+dy,x+dx]=colors[3] if len(chosen)%3 else colors[2]
  if len(chosen)==18:break
 out=a.copy();out[m,:3]=rgb[m];return out

def build(out,source):
 out.mkdir(parents=True,exist_ok=True);before=snapshot(source)
 sm=json.loads((source/'manifest.json').read_text());old={n:np.array(Image.open(source/f'layer_{n}.png').convert('RGBA')) for n in 'AB'}
 arr={n:paint(old[n],n) for n in 'AB'};stats={};checks={}
 for n in 'AB':
  a=old[n];b=arr[n];m=a[:,:,3]>0
  assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[~m],b[~m])
  holes=binary_fill_holes(m)&~m;assert label(holes)[1]==3
  Image.fromarray(b).save(out/f'layer_{n}.png');Image.fromarray(a[:,:,3]).save(out/f'mask_{n}.png')
  diff=np.any(a[:,:,:3]!=b[:,:,:3],axis=2);Image.fromarray((diff*255).astype('uint8')).save(out/f'RGB_changes_{n}.png')
  stats[n]={'before_palette':palette(a),'after_palette':palette(b),'RGB_changed_opaque_pixels':int(diff.sum()),'alpha_changed_pixels':0,'transparent_RGBA_changed_pixels':0,'before_color_components_4connected':component_counts(a),'after_color_components_4connected':component_counts(b)}
 bg=(57,43,32,255);frames=[];records=[]
 for i,r in enumerate(sm['frames']):
  im=Image.new('RGBA',tuple(sm['canvas']),bg);expected=np.array(im);mask_old=np.zeros(expected.shape[:2],dtype='uint8');mask_new=mask_old.copy();owners=[]
  for n in 'AB':
   x,y=r[n+'_position'];a=arr[n];h,w=a.shape[:2];m=a[:,:,3]>0
   im.alpha_composite(Image.fromarray(a),(x,y));expected[y:y+h,x:x+w][m]=a[m]
   own=np.zeros(mask_old.shape,dtype=bool);own[y:y+h,x:x+w]=m;owners.append(own)
   mask_old[y:y+h,x:x+w][old[n][:,:,3]>0]=1;mask_new[y:y+h,x:x+w][m]=1
  assert np.array_equal(np.array(im),expected);assert np.array_equal(mask_old,mask_new)
  im.save(out/f'frame_{i:02}.png');frames.append(im)
  records.append({'frame':f'frame_{i:02}.png','A_position':r['A_position'],'B_position':r['B_position'],'B_delta':r['B_delta'],'visible_A_pixels':int((owners[0]&~owners[1]).sum()),'fixed_layer_raw_sha256':{n:sha(arr[n].tobytes()) for n in 'AB'}})
 sheet=Image.new('RGBA',(512,512),bg)
 for i,f in enumerate(frames):sheet.paste(f,((i%2)*256,(i//2)*256))
 sheet.save(out/'spritesheet.png');sheet.resize((2048,2048),Image.Resampling.NEAREST).save(out/'spritesheet_nearest_4x.png')
 frames[-1].resize((1024,1024),Image.Resampling.NEAREST).save(out/'final_nearest_4x.png')
 frames[-1].crop((33,78,50,177)).resize((136,792),Image.Resampling.NEAREST).save(out/'holes_nearest_8x.png')
 comparison=Image.new('RGBA',(1024,512),bg);comparison.paste(Image.open(source/'spritesheet.png'),(0,0));comparison.paste(sheet,(512,0));comparison.save(out/'comparison_before_left_after_right.png');comparison.resize((2048,1024),Image.Resampling.NEAREST).save(out/'comparison_nearest_2x.png')
 gp=sheet.convert('RGB').quantize(colors=16,dither=Image.Dither.NONE);g=[f.convert('RGB').quantize(palette=gp,dither=Image.Dither.NONE) for f in frames]
 g[0].save(out/'motion.gif',save_all=True,append_images=g[1:],duration=[1000,400,400,1600],loop=0,disposal=2,optimize=False)
 gif=Image.open(out/'motion.gif')
 for i,f in enumerate(frames):gif.seek(i);assert np.array_equal(np.array(gif.convert('RGB')),np.array(f.convert('RGB')))
 assert before==snapshot(source)
 colors=palette(np.array(sheet));checks={'old_source_tree_unchanged':True,'alpha_and_all_holes_pixel_identical':True,'transparent_RGBA_unchanged':True,'A_fixed_B_integer_translation_identical':True,'visible_underlayer_geometry_identical':True,'all_frames_exact_compositor':True,'GIF_roundtrip_exact':True,'single_RGB_pass_per_layer':True}
 report={'status':'art-cleanup-experiment','runtimeVerified':False,'engineReady':False,'source':'../../binding_alignment/native-study','source_tree_sha256':before,'method':'Source-informed broad low-contrast paper washes, sparse 6–7px irregular fiber clusters, and original pigment-driven uneven edge wear. One RGB texture repaint per immutable layer; no resampling or per-frame filters.','before_shared_opaque_colors_including_background':21,'after_shared_opaque_colors_including_background':len(colors),'after_shared_palette':colors,'layers':stats,'frames':records,'QA':checks,'limitations':['Experimental 256px canvas; game target resolution and playback not verified.','Original masks and rectangular apertures deliberately retained; this is texture polish, not geometry redesign.']}
 v1=source.parent.parent/'binding_cluster_cleanup/spritesheet.png'
 triple=Image.new('RGBA',(1536,512),bg);triple.paste(Image.open(source/'spritesheet.png'),(0,0));triple.paste(Image.open(v1),(512,0));triple.paste(sheet,(1024,0));triple.save(out/'comparison_source_v1_v2.png');triple.resize((3072,1024),Image.Resampling.NEAREST).save(out/'comparison_source_v1_v2_nearest_2x.png')
 (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'QA':checks,'colors':len(colors),'stats':stats},indent=2))
if __name__=='__main__':
 here=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=here);p.add_argument('--source',type=Path,default=here.parent.parent/'binding_alignment/native-study');a=p.parse_args();build(a.out,a.source)
