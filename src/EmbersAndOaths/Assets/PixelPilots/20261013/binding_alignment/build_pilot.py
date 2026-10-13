#!/usr/bin/env python3
"""Deterministic N6 source-pixel layer pilot. No model call, scaling or runtime changes."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_fill_holes, find_objects

def sha(b): return hashlib.sha256(b).hexdigest()
def file_sha(p): return sha(p.read_bytes())
def save_arr(a,p): Image.fromarray(a).save(p)
def build(source,out):
 out.mkdir(parents=True,exist_ok=True)
 rgb=np.array(Image.open(source).convert('RGB'));h,w=rgb.shape[:2]
 assert (w,h)==(1254,1254)
 lab,n=label(rgb[:,:,0]>140)
 comps=[lab==i for i in range(1,n+1) if (lab==i).sum()>100000]
 comps.sort(key=lambda m: np.where(m)[1].min()); assert len(comps)==2
 outers=[];holes=[]
 for core in comps:
  outer=np.zeros((h,w),bool)
  for y in np.where(core.any(axis=1))[0]:
   xs=np.where(core[y])[0];outer[y,max(0,xs[0]-1):min(w,xs[-1]+2)]=True
  hh=binary_fill_holes(core)&~core
  ll,nn=label(hh);hh=np.isin(ll,[i for i in range(1,nn+1) if (ll==i).sum()>50])
  assert label(hh)[1]==3
  outers.append(outer);holes.append(hh)
 original_b_holes=holes[1].copy()
 aligned_b_holes=np.zeros_like(holes[0]);aligned_b_holes[:,535:]=holes[0][:,:-535]
 fill=original_b_holes&~aligned_b_holes;cut=aligned_b_holes&~original_b_holes
 # Explicit one-time art proposal: two newly opaque pixels take B's same-row pixel 32px right.
 b_rgb=rgb.copy()
 yy,xx=np.where(fill);b_rgb[yy,xx]=rgb[yy,xx+32]
 holes[1]=aligned_b_holes
 canonical=[];bounds=[];hole_local=[]
 for name,outer,hole,color in zip(('A','B'),outers,holes,(rgb,b_rgb)):
  alpha=outer&~hole
  rgba=np.dstack((color,alpha.astype('uint8')*255));rgba[~alpha,:3]=0
  ys,xs=np.where(outer);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))
  x0,y0,x1,y1=box;crop=rgba[y0:y1,x0:x1];canonical.append(crop);bounds.append(box)
  save_arr(crop,out/f'layer_{name}.png');save_arr(alpha.astype('uint8')*255,out/f'mask_{name}_full.png')
  save_arr(hole.astype('uint8')*255,out/f'holes_{name}_full.png')
  ll,nn=label(hole);records=[]
  for s in find_objects(ll):
   records.append({'bbox':[s[1].start-x0,s[0].start-y0,s[1].stop-x0,s[0].stop-y0], 'center_bbox':[(s[1].start+s[1].stop-1)/2-x0,(s[0].start+s[0].stop-1)/2-y0]})
  hole_local.append(records)
 save_arr(original_b_holes.astype('uint8')*255,out/'holes_B_before_full.png')
 changes=np.zeros((h,w,4),dtype='uint8');changes[fill]=[0,255,128,255];changes[cut]=[255,80,80,255]
 save_arr(changes,out/'B_hole_correction_mask.png')
 frames=[];records=[];A,B=canonical
 background=Image.new('RGBA',(w,h),(57,43,32,255));background.save(out/'background.png')
 for i,bx in enumerate((703,524,346,168)):
  frame=background.copy();frame.alpha_composite(Image.fromarray(A),(168,313));frame.alpha_composite(Image.fromarray(B),(bx,313))
  p=out/f'frame_{i:02}.png';frame.save(p);frames.append(frame)
  # Render independently using integer array assignment and compare complete canvas bytes.
  expected=np.array(background)
  layer_hashes={}
  for name,arr,x in [('A',A,168),('B',B,bx)]:
   ht,wd=arr.shape[:2];region=expected[313:313+ht,x:x+wd];opaque=arr[:,:,3]==255;region[opaque]=arr[opaque]
   placed=np.zeros((h,w,4),dtype='uint8');placed[313:313+ht,x:x+wd]=arr
   recovered=placed[313:313+ht,x:x+wd]
   assert np.array_equal(recovered,arr)
   layer_hashes[name]=sha(recovered.tobytes())
  assert np.array_equal(expected,np.array(frame))
  records.append({'frame':p.name,'B_position':[bx,313],'B_delta_from_initial':[bx-703,0], 'A_position':[168,313], 'layer_raw_rgba_sha256':layer_hashes, 'frame_sha256':file_sha(p),'canvas':[w,h]})
 assert len({r['layer_raw_rgba_sha256']['A'] for r in records})==1
 assert len({r['layer_raw_rgba_sha256']['B'] for r in records})==1
 assert hole_local[0]==hole_local[1]
 sheet=Image.new('RGBA',(w*2,h*2),(57,43,32,255))
 for i,f in enumerate(frames): sheet.paste(f,((i%2)*w,(i//2)*h))
 sheet.save(out/'spritesheet_2x2.png')
 # Human-facing hole review uses actual 1:1 crops enlarged nearest-neighbor, never downsampled scenes.
 crops=[frames[0].crop((178,408,250,460)),frames[0].crop((713,408,785,460)),frames[-1].crop((178,408,250,460)),frames[-1].crop((178,832,250,884))]
 preview=Image.new('RGB',(72*8*2,52*8*2),(57,43,32))
 for i,c in enumerate(crops):preview.paste(c.resize((72*8,52*8),Image.Resampling.NEAREST),((i%2)*576,(i//2)*416))
 preview.save(out/'holes_nearest_8x.png')
 frames[-1].crop((490,300,615,985)).resize((250,1370),Image.Resampling.NEAREST).save(out/'overlap_edge_nearest_2x.png')
 # Shared palette GIF is a preview only; PNG/layers are lossless evidence.
 palette=sheet.convert('RGB').quantize(colors=256)
 gif=[f.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 gif[0].save(out/'binding_motion.gif',save_all=True,append_images=gif[1:],duration=[1000,400,400,1600],loop=0,disposal=2,optimize=False)
 doc={'status':'rigid-layer-continuity-pilot','engineReady':False,'runtimeVerified':False,'source':str(source),'source_sha256':file_sha(source),
 'method':'Source RGB extraction; binary alpha; one-time B hole correction; integer translation only; no scene resampling or generation.',
 'canvas':[w,h],'background':'new explicit flat #392b20; original generated background is not reconstructed',
 'extraction':'Core red>140 connected papers; row extent expanded by one pixel; internal dark components >50px become holes. This mask interpretation is authored, not source-provided alpha.',
 'layer_bounds_source':dict(zip(('A','B'),bounds)), 'layer_sizes':{'A':[A.shape[1],A.shape[0]],'B':[B.shape[1],B.shape[0]]},
 'hole_geometry_local':dict(zip(('A','B'),hole_local)),
 'B_initial_correction':{'art_proposal':True,'newly_opaque_pixels':int(fill.sum()),'newly_transparent_pixels':int(cut.sum()),'fill_pixels_xy':[[int(x),int(y)] for y,x in zip(yy,xx)],'fill_source':'same row, x+32 in original B','purpose':'Make all three binary hole masks exactly match A translated +535px; not asserted to be original geometry'},
 'frames':records,'validation':{'A_hash_constant':True,'B_hash_constant':True,'integer_translations':True,'fixed_canvas':True,'exact_hole_mask_alignment_final':bool(np.array_equal(holes[0][:,:-535],holes[1][:,535:])), 'identical_local_hole_geometry':True,'independent_array_compositor_match':True,'unchanged_layer_dimensions':True,'right_underlayer_strip_nominal_px':52},
 'limits':['Not a final native-grid game sprite. Source-resolution geometry pilot only.','No marginal text or receipt; does not represent full N6 evidence certification.','No shadows reconstructed. Binary segmentation may retain a one-pixel source-background fringe.','GIF palette conversion is lossy preview. PNG and layer hashes are authoritative.']}
 (out/'manifest.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(doc['validation'],indent=2));print('Output',out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--source',type=Path);a=ap.parse_args()
 source=a.source or Path(__file__).resolve().parents[3]/'ConceptDrafts/20261012/batch64/45_keyframe01_adjacent.png'
 build(source,a.out)
