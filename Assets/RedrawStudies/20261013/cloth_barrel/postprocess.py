"""Reproducible, project-only pixel reconstruction; no installs or runtime writes."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, hashlib
P=Path(__file__).resolve().parent
R=P.parents[3]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# Read-only provenance crop; output is review-only, never packed into runtime.
SOURCE=R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch53/197_mns_separate_use_barrel_inspection.png'
Image.open(SOURCE).crop((1300,384,1507,604)).save(P/'source197_right_barrel_crop.png')
# Authored constrained palette, deliberately no dithering.
PAL={'O':'#29272b','s':'#47342d','w':'#685040','m':'#8a6748','h':'#a17e56','i':'#3a3b42','j':'#575860','k':'#81817c','c':'#938673','b':'#b6aa90','a':'#d4c8ac','l':'#e1d6ba','r':'#7b5b38','t':'#b59159'}
COL={k:tuple(bytes.fromhex(v[1:]))+(255,) for k,v in PAL.items()}
raw=Image.open(P/'concept_v1.png').convert('RGBA'); a=np.array(raw);mask=a[:,:,3]>=128
# Largest connected alpha component, excluding stray generated wisps.
seen=np.zeros(mask.shape,bool); components=[]
for y,x in zip(*np.where(mask)):
 if seen[y,x]:continue
 stack=[(y,x)];seen[y,x]=1;pts=[]
 while stack:
  yy,xx=stack.pop();pts.append((yy,xx))
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
   ny,nx=yy+dy,xx+dx
   if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=1;stack.append((ny,nx))
 components.append(pts)
pts=max(components,key=len);ys,xs=zip(*pts);bbox=list(map(int,[min(xs),min(ys),max(xs)+1,max(ys)+1]))
clean=np.zeros_like(a);yy,xx=np.array(pts).T;clean[yy,xx]=a[yy,xx];clean[yy,xx,3]=255
small=Image.fromarray(clean).crop(bbox).resize((24,25),Image.Resampling.NEAREST)
base=Image.new('RGBA',(32,32));base.paste(small,(4,3))
z=np.array(base); palette=np.array(list(COL.values()));opaque=z[:,:,3]>0
rgb=z[:,:,:3].astype(int);dist=((rgb[:,:,None,:]-palette[None,None,:,:3])**2).sum(3);z[opaque]=palette[dist.argmin(2)[opaque]];z[~opaque]=0
base=Image.fromarray(z.astype('uint8'));base.save(P/'initial_quantized.png')
im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
def poly(pts,c):d.polygon(pts,fill=COL[c])
def line(pts,c,w=1):d.line(pts,fill=COL[c],width=w)
# 01 Rebuild compact bulging body, consistent near-orthographic axes.
poly([(8,5),(23,5),(26,8),(27,14),(27,22),(25,26),(21,28),(10,28),(6,26),(4,22),(4,14),(5,8)],'O')
poly([(8,7),(23,7),(25,10),(26,15),(26,22),(24,25),(20,27),(11,27),(7,25),(5,21),(5,14),(6,10)],'w')
poly([(8,9),(12,9),(12,27),(9,26),(7,24),(6,20),(6,13)],'h')
poly([(13,8),(17,8),(17,27),(13,27)],'m')
poly([(18,8),(21,9),(22,25),(19,27),(18,27)],'w')
poly([(22,10),(24,11),(25,16),(25,22),(23,25)],'s')
line([(11,13),(11,25)],'w');line([(17,14),(17,26)],'s');line([(22,15),(23,23)],'s')
# 02 Low-frequency curved hoops, two rows, no metal noise or nails.
poly([(5,13),(8,15),(12,16),(20,16),(24,14),(26,13),(26,16),(23,18),(19,19),(12,19),(8,18),(5,16)],'O')
poly([(5,13),(8,15),(12,16),(20,16),(24,14),(26,13),(26,15),(23,17),(19,18),(12,18),(8,17),(5,15)],'i')
line([(5,13),(8,15),(12,16),(19,16)],'j');line([(6,14),(8,15),(12,16)],'k')
poly([(6,22),(9,24),(13,25),(20,25),(24,23),(25,22),(25,25),(21,27),(12,28),(8,26),(6,24)],'O')
poly([(6,22),(9,24),(13,25),(20,25),(24,23),(25,22),(25,24),(21,26),(13,27),(9,25),(6,23)],'i')
line([(6,22),(9,24),(13,25),(20,25),(24,23)],'j');line([(7,23),(9,24),(13,25)],'k')
# 03 Short linen overhang: top is a flattened closed ellipse, not domed lid.
poly([(9,3),(22,3),(25,4),(27,6),(27,9),(29,12),(28,14),(25,13),(23,12),(21,14),(19,14),(17,12),(14,13),(12,12),(9,14),(7,13),(6,12),(3,13),(3,10),(5,8),(5,6),(7,4)],'O')
poly([(6,7),(26,7),(26,9),(28,11),(28,12),(25,12),(23,11),(21,13),(19,13),(17,11),(14,12),(12,11),(9,13),(7,11),(4,12),(4,10)],'c')
poly([(6,7),(24,7),(25,9),(24,11),(21,12),(20,12),(19,10),(16,10),(14,11),(12,10),(9,12),(8,10),(5,11),(6,9)],'b')
poly([(9,4),(22,4),(25,5),(26,6),(26,8),(23,9),(10,9),(6,7),(6,6)],'b')
poly([(10,4),(21,4),(24,5),(25,6),(24,7),(21,8),(11,8),(7,7),(7,6)],'a')
line([(10,5),(19,5)],'l');line([(8,6),(11,6)],'l')
# 04 Narrow rope and one modest knot, distinct from labels or bookings.
line([(5,8),(8,9),(12,10),(21,10),(25,9),(27,8)],'s')
line([(6,8),(9,9),(13,10),(20,10),(25,9)],'r')
line([(9,9),(12,10),(18,10)],'t')
poly([(7,9),(9,9),(10,10),(9,11),(9,13),(8,13),(8,11),(6,11),(6,10)],'s')
line([(7,10),(8,10),(8,12)],'t');line([(9,10),(10,11)],'r')
im.save(P/'candidate_water_container_native.png');im.resize((256,256),Image.Resampling.NEAREST).save(P/'candidate_water_container_8x.png')
base.resize((256,256),Image.Resampling.NEAREST).save(P/'initial_quantized_8x.png')
# Every changed native pixel is recorded against the honest quantized intermediate.
u=np.array(im);v=np.array(base);coords=np.argwhere(np.any(u!=v,axis=2))
changes=[{'x':int(x),'y':int(y),'before_rgba':v[y,x].tolist(),'after_rgba':u[y,x].tolist()} for y,x in coords]
(P/'pixel_edits.json').write_text(json.dumps({'reference':'initial_quantized.png','result':'candidate_water_container_native.png','method':'manual cluster reconstruction expressed by ordered pixel polygons in postprocess.py; not a quantization-only claim','changed_pixel_count':len(changes),'changes':changes},indent=2)+'\n')
# Reviewer contact sheet: scale context labeled honestly. Historical official sample read-only.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
board=Image.new('RGB',(940,570),'#24262b');bd=ImageDraw.Draw(board)
def label(x,y,t):bd.text((x,y),t,font=font,fill='#eee5d3')
def comp(x,y,obj):board.paste(obj,(x,y),obj if obj.mode=='RGBA' else None)
old=Image.open(P/'source197_right_barrel_crop.png');ref=Image.open(R/'Assets/ReferenceAudit/20261013/originals/Barrel_0.png').convert('RGBA')
label(20,12,'197 source crop (not native)');comp(20,38,old.resize((207,220),Image.Resampling.NEAREST))
label(252,12,'Generated volume concept');thumb=raw.copy();thumb.thumbnail((220,220));comp(255,38,thumb)
label(486,12,'Initial sample / 8x');comp(484,36,base.resize((256,256),Image.Resampling.NEAREST))
label(745,12,'Final / native 1x');comp(810,55,im)
label(20,310,'Historical barrel / 8x');comp(22,338,ref.resize((200,216),Image.Resampling.NEAREST))
label(252,310,'Candidate / 8x');comp(248,310,im.resize((256,256),Image.Resampling.NEAREST))
label(532,320,'32x32 TEST canvas; not an engine grid standard')
label(532,350,'One container; no tags, safety or delivery claim')
label(532,380,'Reference visible extent: 24x25')
label(532,410,'Body budget: 24x24; cloth silhouette: 27x26')
label(532,440,'Nearest-neighbor previews; binary transparency')
label(532,470,'No runtime / collision / pivot validation')
board.save(P/'old_new_reference_comparison.png')
# Background checks at a common nearest-neighbor scale.
qa=Image.new('RGB',(768,288));qd=ImageDraw.Draw(qa)
for n,bg in enumerate(['#f1eddd','#66665e','#171821']):
 qd.rectangle((n*256,0,n*256+255,287),fill=bg);qa.paste(im.resize((256,256),Image.Resampling.NEAREST),(n*256,24),im.resize((256,256),Image.Resampling.NEAREST))
qa.save(P/'native_background_QA.png')
alpha=u[:,:,3];colors=np.unique(u[alpha>0],axis=0);bb=im.getbbox()
report={'asset_name':'候选清水容器','status':'pixel-study-not-runtime','canvas':[32,32],'alpha_bbox':list(bb),'visible_extent':[bb[2]-bb[0],bb[3]-bb[1]],'body_budget':[24,24],'cloth_extension':'Body x=4..27; cloth x=3..29, extends 1px left and 2px right. Top begins y=3; overall ends y=28.','opaque_color_count':len(colors),'alpha_values':np.unique(alpha).tolist(),'hidden_rgb_nonzero':int(np.count_nonzero(u[alpha==0,:3])),'initial_crop_alpha_threshold':128,'initial_crop_largest_component_bbox':bbox,'initial_palette':'14 authored colors, nearest distance, no dithering','quantization_only':False,'changed_native_pixels':len(changes),'same_scale_reference':{'canvas':[25,27],'visible_extent':[24,25],'not_engine_grid_standard':True},'runtimeIntegrated':False,'collisionVerified':False,'pivotVerified':False,'safetyCertified':False,'content_review':['Single upright barrel only','No writing or booking tags','Closed linen covering cannot establish contents or safety','Two hoops and four main stave planes','Generated long cloth folds shortened in native reconstruction'],'checks':{'binary_alpha':set(np.unique(alpha))<={0,255},'low_palette_le_16':len(colors)<=16,'clear_canvas_border':not any([alpha[0].any(),alpha[-1].any(),alpha[:,0].any(),alpha[:,-1].any()]),'native_extent_max_28':max(bb[2]-bb[0],bb[3]-bb[1])<=28},'source_generator':'built-in image_gen','prompt':'concept_v1.prompt.txt'}
(P/'QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
