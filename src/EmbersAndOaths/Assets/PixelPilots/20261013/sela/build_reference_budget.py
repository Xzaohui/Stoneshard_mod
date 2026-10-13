#!/usr/bin/env python3
"""Third bounded reference-budget experiment; preserve A/B and comparison.png."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,tempfile
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,default=HERE);OUT=parser.parse_args().out.resolve();OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Recreate A/B only in a temporary workspace; do not rewrite their original files.
with tempfile.TemporaryDirectory(prefix='sela-budget-') as td:
 t=Path(td)
 subprocess.run([sys.executable,str(HERE/'build_pilot.py'),'--out',str(t)],check=True,stdout=subprocess.DEVNULL)
 for p in t.iterdir():
  dest=OUT/p.name
  if not dest.exists():dest.write_bytes(p.read_bytes())
  elif p.suffix=='.png':assert sha(dest)==sha(p),f'Existing A/B output changed: {dest}'
cut=np.array(Image.open(OUT/'intermediate_cutout_full.png'))
m=json.loads((OUT/'manifest.json').read_text()); box=m['source']['crop_bbox'];cut=cut[box[1]:box[3],box[0]:box[2]]
pal=json.loads((OUT/'palette.json').read_text());COL=np.array([tuple(bytes.fromhex(p['hex'][1:])) for p in pal],dtype=np.uint8)
f=cut[:,:,:3].astype(np.float32); mask=cut[:,:,3]>0
nearest=(((f[:,:,None,:]-COL[None,None,:,:])**2)*np.array([0.8,1.2,1.0])).sum(3).argmin(2)
w,h=15,34;content=np.zeros((h,w,4),dtype=np.uint8)
for y in range(h):
 for x in range(w):
  x0,x1=round(x*cut.shape[1]/w),round((x+1)*cut.shape[1]/w);y0,y1=round(y*cut.shape[0]/h),round((y+1)*cut.shape[0]/h)
  visible=mask[y0:y1,x0:x1]
  if visible.mean()>=.45:
   idx=np.bincount(nearest[y0:y1,x0:x1][visible],minlength=len(COL)).argmax();content[y,x]=[*COL[idx],255]
im=Image.new('RGBA',(32,48));im.paste(Image.fromarray(content),(8,12));im.save(OUT/'c_32x48_reference_budget_baseline.png')
edits=[]
def pixel(x,y,index,reason):
 before=list(im.getpixel((x,y)));after=[*map(int,COL[index]),255] if index is not None else [0,0,0,0]
 if before!=after:im.putpixel((x,y),tuple(after));edits.append(dict(x=x,y=y,before=before,after=after,reason=reason))
for y in range(22):
 for x in range(32):
  c=im.getpixel((x,y))
  if c[3] and c[:3] in [tuple(COL[i]) for i in [17,18,19]]:pixel(x,y,3 if c[:3]==tuple(COL[17]) else 4,'Consolidate brown hair clusters')
# Limited repairs for the lower information budget, without widening the silhouette.
pixel(13,17,7,'Separate one dark eye pixel from heavy forehead edge')
for x,y in [(17,30),(17,31),(16,32),(16,33),(17,34)]:pixel(x,y,21,'Reduce rope to a compact readable loop and knot')
for x,y in [(18,31),(18,32),(18,33),(18,34)]:pixel(x,y,20,'Two-shade rope edge at reference height budget')
for x,y in [(17,32),(17,33)]:pixel(x,y,0,'Preserve two-pixel rope interior; no subpixel detail')

im.save(OUT/'c_32x48_reference_budget_idle_view01_f000.png')
(OUT/'c_32x48_reference_budget_pixel_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
scale=8;big=im.resize((256,384),Image.Resampling.NEAREST);panel=Image.new('RGB',big.size);d=ImageDraw.Draw(panel)
for y in range(0,384,8):
 for x in range(0,256,8):d.rectangle((x,y,x+7,y+7),fill=('#a6aaa7' if (x//8+y//8)%2 else '#bec1bb'))
panel.paste(big,mask=big.getchannel('A'));panel.save(OUT/'c_32x48_reference_budget_preview_8x.png')
board=Image.new('RGB',(1100,640),'#f1e8d5');d=ImageDraw.Draw(board)
for n,ox,label in [('a_32x48',25,'A 32x48 / 20x44 visible'),('b_48x64',335,'B 48x64 / 26x58 visible'),('c_32x48_reference_budget',775,'C 32x48 / 15x34 budget')]:
 panel=Image.open(OUT/f'{n}_preview_8x.png');board.paste(panel,(ox,65));d.text((ox,20),label,fill='#27241f');d.text((ox,40),'NEAREST x8 / NOT RUNTIME',fill='#27241f')
 d.text((ox,600),'EXPERIMENTAL CANVAS',fill='#27241f')
board.save(OUT/'comparison_v2.png')
arr=np.array(im);vis=arr[:,:,3]>0;ys,xs=np.where(vis);_,num=ndi.label(vis,structure=np.ones((3,3),int));p=OUT/'c_32x48_reference_budget_idle_view01_f000.png'
r={'name':'c_32x48_reference_budget','filename':p.name,'sha256':sha(p),'canvas':[32,48],'content_target':[15,34],'offset':[8,12],'foot_anchor':[16,45],'visible_bbox':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],'visible_color_count':len(set(map(tuple,arr[vis,:3]))),'alpha_values':np.unique(arr[:,:,3]).tolist(),'visible_pixels':int(vis.sum()),'eight_connected_components':num,'engine_origin':None,'collision':None,'runtime_verified':False,'proportion_note':'Approximately uniform scale: source 362x827 becomes 15x34 after integer rounding. Height 34 references only one Verren PNG visible budget, not universal anatomy.'}
r['checks']={'binary_alpha':set(r['alpha_values'])=={0,255},'palette_subset':set(map(tuple,arr[vis,:3])).issubset(set(map(tuple,COL))),'sole_row_matches_anchor':int(ys.max())==45,'clear_canvas_border':not (vis[0].any() or vis[-1].any() or vis[:,0].any() or vis[:,-1].any()),'transparent_rgb_zero':bool((arr[~vis,:3]==0).all()),'visible_height_34':int(ys.max()-ys.min()+1)==34}
assert all(r['checks'].values()),r
m['candidates']=[c for c in m['candidates'] if c['name']!=r['name']]+[r]
# Derive repository-relative reference path from the verified source path's root.
root=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
ref=root/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/references/original-characters/verren_npc_community_wiki.png'
m['reference_budget_reference']={'path':str(ref.relative_to(root)),'sha256':sha(ref),'canvas':[25,38],'visible_bbox':[2,2,23,36],'visible_color_count':19,'role':'One public NPC PNG visible-height comparison only; no copied pixels; not official universal specification'}
m['supplemental_reference_budget_script_sha256']=sha(Path(__file__))
m['reference_budget_extension']='One additional 15x34 visible-budget experiment, approximately uniform scale with integer rounding. Original A/B and comparison.png byte-preserved.'
m['artifacts'].update({p.name:sha(p) for p in OUT.glob('c_*.png')});m['artifacts']['comparison_v2.png']=sha(OUT/'comparison_v2.png')
(OUT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(r,indent=2))
