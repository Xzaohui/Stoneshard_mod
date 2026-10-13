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
 h,w=a.shape[:2]
 # Three value bands per sheet: calm field, deliberate stepped edge wear,
 # broad upper-left light. A has one deeper edge tone. No glyphs or new cuts.
 colors={'A':[(229,185,118),(219,169,101),(237,198,141),(202,152,89)],'B':[(239,210,161),(232,195,135),(244,219,178),(232,195,135)]}[n]
 im=Image.new('RGB',(w,h),colors[0]);d=ImageDraw.Draw(im)
 # Limited large corner fields; all boundaries on original pixel grid.
 d.polygon([(0,0),(w-1,0),(w-1,5),(w-5,5),(w-5,3),(w-15,3),(w-15,2),(18,2),(18,3),(7,3),(7,8),(3,8),(3,18),(0,18)],fill=colors[1])
 d.polygon([(0,h-1),(w-1,h-1),(w-1,h-20),(w-3,h-20),(w-3,h-10),(w-6,h-10),(w-6,h-6),(w-14,h-6),(w-14,h-3),(14,h-3),(14,h-5),(6,h-5),(6,h-11),(2,h-11),(2,h-24),(0,h-24)],fill=colors[1])
 d.polygon([(3,9),(7,9),(7,5),(21,5),(21,4),(w-18,4),(w-18,6),(w-32,6),(w-32,8),(18,8),(18,10),(10,10),(10,16),(7,16),(7,29),(4,29),(4,43),(3,43)],fill=colors[2])
 # Sparse connected wear clusters, all >=5 pixels, near outer edge only.
 for pts in [[(w-4,31),(w-2,31),(w-2,37),(w-3,37),(w-3,34),(w-4,34)],[(1,77),(3,77),(3,82),(2,82),(2,86),(1,86)],[(w-8,h-5),(w-4,h-5),(w-4,h-9),(w-3,h-9),(w-3,h-3),(w-8,h-3)]]:
  d.polygon(pts,fill=colors[1])
 if n=='A':
  for pts in [[(0,0),(13,0),(13,1),(3,1),(3,3),(0,3)],[(w-2,h-14),(w-1,h-14),(w-1,h-1),(w-12,h-1),(w-12,h-2),(w-3,h-2),(w-3,h-5),(w-2,h-5)]]:d.polygon(pts,fill=colors[3])
 rgb=np.array(im);out=a.copy();m=a[:,:,3]>0;out[m,:3]=rgb[m];return out

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
 report={'status':'art-cleanup-experiment','runtimeVerified':False,'engineReady':False,'source':'../binding_alignment/native-study','source_tree_sha256':before,'method':'Hand-authored limited, stepped edge-wear color fields on each immutable RGBA layer, once; no resampling, dithering or per-frame repaint.','before_shared_opaque_colors_including_background':21,'after_shared_opaque_colors_including_background':len(colors),'after_shared_palette':colors,'layers':stats,'frames':records,'QA':checks,'limitations':['Experimental 256px canvas; game target resolution and playback not verified.','Original masks and rectangular apertures deliberately retained; this is texture polish, not geometry redesign.']}
 (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'QA':checks,'colors':len(colors),'stats':stats},indent=2))
if __name__=='__main__':
 here=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=here);p.add_argument('--source',type=Path,default=here.parent/'binding_alignment/native-study');a=p.parse_args();build(a.out,a.source)
