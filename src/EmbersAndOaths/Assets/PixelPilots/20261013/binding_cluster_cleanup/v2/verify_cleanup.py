#!/usr/bin/env python3
"""Independent readback: source integrity, geometry, placement and GIF fidelity."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes,label
p=Path(__file__).resolve().parent;s=p.parent.parent/'binding_alignment/native-study'
m=json.loads((p/'manifest.json').read_text());sm=json.loads((s/'manifest.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
checks={};checks['source_tree_hashes_match_before_build']=all((s/f).is_file() and sha((s/f).read_bytes())==h for f,h in m['source_tree_sha256'].items())
checks['source_tree_file_list_unchanged']=set(m['source_tree_sha256'])=={str(f.relative_to(s)) for f in s.rglob('*') if f.is_file()}
old={n:np.array(Image.open(s/f'layer_{n}.png')) for n in 'AB'};new={n:np.array(Image.open(p/f'layer_{n}.png')) for n in 'AB'}
for n in 'AB':
 a,b=old[n],new[n];checks[n+'_alpha_identical']=np.array_equal(a[:,:,3],b[:,:,3]);checks[n+'_mask_export_identical']=np.array_equal(np.array(Image.open(p/f'mask_{n}.png')),np.array(Image.open(s/f'mask_{n}.png')))
 ha=binary_fill_holes(a[:,:,3]>0)&(a[:,:,3]==0);hb=binary_fill_holes(b[:,:,3]>0)&(b[:,:,3]==0)
 checks[n+'_three_hole_masks_identical']=label(hb)[1]==3 and np.array_equal(ha,hb)
 checks[n+'_transparent_RGB_identical']=np.array_equal(a[a[:,:,3]==0],b[b[:,:,3]==0])
g=Image.open(p/'motion.gif');frames=[];visibility=[]
for i,r in enumerate(sm['frames']):
 expected=np.zeros((256,256,4),dtype='uint8');expected[:]=(57,43,32,255)
 owners_old=np.zeros((256,256),dtype='uint8');owners_new=owners_old.copy()
 for j,n in enumerate('AB'):
  x,y=r[n+'_position'];a=new[n];h,w=a.shape[:2];mask=a[:,:,3]>0;expected[y:y+h,x:x+w][mask]=a[mask]
  owners_old[y:y+h,x:x+w][old[n][:,:,3]>0]=j+1;owners_new[y:y+h,x:x+w][mask]=j+1
 actual=np.array(Image.open(p/f'frame_{i:02}.png'));frames.append(actual)
 checks[f'frame_{i}_exact_fixed_layer_composite']=np.array_equal(actual,expected)
 checks[f'frame_{i}_visible_A_B_background_masks_identical']=np.array_equal(owners_old,owners_new)
 checks[f'frame_{i}_positions_and_delta_identical']=all(m['frames'][i][k]==r[k] for k in ['A_position','B_position','B_delta'])
 g.seek(i);checks[f'GIF_{i}_exact_RGB']=np.array_equal(np.array(g.convert('RGB')),actual[:,:,:3]);visibility.append(int((owners_new==1).sum()))
checks['GIF_four_frames']=g.n_frames==4
checks['final_uncovered_nominal_width_10']=old['A'].shape[1]-old['B'].shape[1]==10
checks['shared_opaque_palette_11']=len({tuple(c) for a in frames for c in a[:,:,:3].reshape(-1,3)})==11
checks['exported_sheet_exact']=np.array_equal(np.array(Image.open(p/'spritesheet.png')),np.concatenate([np.concatenate(frames[:2],axis=1),np.concatenate(frames[2:],axis=1)],axis=0))
assert all(checks.values()),checks
result={'passed':True,'checks':checks,'visible_A_pixels_per_frame':visibility,'output_file_sha256':{f.name:sha(f.read_bytes()) for f in sorted(p.iterdir()) if f.suffix in ['.png','.gif','.py']}}
(p/'QA-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
