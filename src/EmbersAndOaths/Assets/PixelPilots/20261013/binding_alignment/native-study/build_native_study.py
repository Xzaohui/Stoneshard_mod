#!/usr/bin/env python3
"""256px experimental pixel-grid study, not an engine size specification."""
from pathlib import Path
import argparse,json,hashlib
from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes,label
sha=lambda b:hashlib.sha256(b).hexdigest()
def build(out):
 here=Path(__file__).resolve().parent;out.mkdir(parents=True,exist_ok=True)
 input_layers=[here.parent/f'layer_{n}.png' for n in ('A','B')]
 arr=[np.array(Image.open(p).resize(size,Image.Resampling.NEAREST)) for p,size in zip(input_layers,((87,131),(77,131)))]
 # Fix the binary aperture template once in this new grid. Preserve A's sampled apertures.
 masks=[a[:,:,3]>0 for a in arr];holes=[binary_fill_holes(m)&~m for m in masks]
 assert label(holes[0])[1]==3
 bholes=np.zeros_like(holes[1]);bholes[:,:]=holes[0][:,:77]
 fill=holes[1]&~bholes;cut=bholes&~holes[1]
 yy,xx=np.where(fill);arr[1][yy,xx,:3]=arr[1][yy,xx+6,:3]
 masks[1]=(masks[1]|fill)&~cut
 # Shared 20-color paper palette; include only actual paper samples when deriving it.
 pix=np.concatenate([a[:,:,:3][m] for a,m in zip(arr,masks)])
 palette=Image.fromarray(pix.reshape(1,-1,3)).quantize(colors=20,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 for i,(a,m) in enumerate(zip(arr,masks)):
  rgb=np.array(Image.fromarray(a[:,:,:3]).quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB'))
  a[:,:,:3]=rgb;a[:,:,3]=m.astype('uint8')*255;a[~m,:3]=0
  Image.fromarray(a).save(out/f'layer_{"AB"[i]}.png')
  Image.fromarray(m.astype('uint8')*255).save(out/f'mask_{"AB"[i]}.png')
 colors=sorted(set(tuple(int(v) for v in c) for a,m in zip(arr,masks) for c in a[:,:,:3][m]))
 bg=(57,43,32,255);frames=[];records=[]
 for i,x in enumerate((141,105,70,34)):
  im=Image.new('RGBA',(256,256),bg);im.alpha_composite(Image.fromarray(arr[0]),(34,63));im.alpha_composite(Image.fromarray(arr[1]),(x,63));im.save(out/f'frame_{i:02}.png');frames.append(im)
  # Independent exact compositing and transported-layer recovery.
  expected=np.array(Image.new('RGBA',(256,256),bg));hashes={}
  for name,a,px in [('A',arr[0],34),('B',arr[1],x)]:
   ht,wd=a.shape[:2];reg=expected[63:63+ht,px:px+wd];m=a[:,:,3]>0;reg[m]=a[m]
   placed=np.zeros((256,256,4),dtype='uint8');placed[63:63+ht,px:px+wd]=a
   recovered=placed[63:63+ht,px:px+wd];assert np.array_equal(recovered,a);hashes[name]=sha(recovered.tobytes())
  assert np.array_equal(np.array(im),expected)
  records.append({'frame':f'frame_{i:02}.png','A_position':[34,63],'B_position':[x,63],'B_delta':[x-141,0],'layer_raw_sha256':hashes,'opaque_RGB_color_count':len(im.convert('RGB').getcolors(65536))})
 sheet=Image.new('RGBA',(512,512),bg)
 for i,f in enumerate(frames):sheet.paste(f,((i%2)*256,(i//2)*256))
 sheet.save(out/'spritesheet.png');sheet.resize((2048,2048),Image.Resampling.NEAREST).save(out/'spritesheet_nearest_4x.png')
 frames[-1].resize((1024,1024),Image.Resampling.NEAREST).save(out/'final_nearest_4x.png')
 frames[-1].crop((33,78,50,177)).resize((136,792),Image.Resampling.NEAREST).save(out/'holes_nearest_8x.png')
 gp=sheet.convert('RGB').quantize(colors=32,dither=Image.Dither.NONE);gif=[f.convert('RGB').quantize(palette=gp,dither=Image.Dither.NONE) for f in frames]
 gif[0].save(out/'motion.gif',save_all=True,append_images=gif[1:],duration=[1000,400,400,1600],loop=0,disposal=2,optimize=False)
 hh0=binary_fill_holes(masks[0])&~masks[0];hh1=binary_fill_holes(masks[1])&~masks[1];assert np.array_equal(hh0[:,:77],hh1)
 from scipy.ndimage import find_objects
 boxes=[]
 for s in find_objects(label(hh0)[0]):boxes.append([s[1].start,s[0].start,s[1].stop,s[0].stop])
 doc={'status':'experimental-256-grid-study','engineReady':False,'runtimeVerified':False,'input_sha256':{p.name:sha(p.read_bytes()) for p in input_layers},'canvas':[256,256],'layer_sizes':[[87,131],[77,131]],'sampling':'One-time nearest-neighbor layer resize. Ratios differ slightly due to rounding dimensions; shape and texture changed versus source. No per-frame scaling.','palette':'Shared 20-color paper palette via median cut; background adds at most one color; no dithering; binary alpha.','palette_rgb':colors,'paper_color_count':len(colors),'B_once_correction':{'fill':int(fill.sum()),'cut':int(cut.sum())},'hole_bboxes_local':boxes,'frames':records,'validation':{'fixed_canvas':True,'integer_translation':True,'constant_A_B_layer_hashes':all(len({r['layer_raw_sha256'][n] for r in records})==1 for n in ('A','B')),'final_apertures_exact':True,'underlayer_strip_nominal_px':10,'independent_compositor_exact':True},'limits':['Experimental pixel grid, no confirmed game target grid or animation timing.','One-time downsampling loses texture and changes edge steps; not a source-pixel-preserving artifact.','Inherited masks still contain edge coloration; no final art polish or game deployment.']}
 (out/'manifest.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n');print(json.dumps(doc['validation'],indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);a=p.parse_args();build(a.out)
