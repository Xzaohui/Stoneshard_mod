#!/usr/bin/env python3
"""Authored pixel geometry proposal, reference v4 only; no source extraction or engine edits."""
from pathlib import Path
import hashlib, json, math
import numpy as np
from PIL import Image, ImageDraw
OUT=Path(__file__).resolve().parent
ROOT=next(p for p in OUT.parents if (p/'AGENTS.md').exists())
SOURCES=['src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch58/63_refuge_door_geometry_v4.png','src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch58/QA-independent.json','design/05_主线/台本/台本_N12_失踪者仍有名字.md','design/08_副本/台本/台本_D08_沉水档案井.md']
COLORS=['#272827','#383a38','#4c4d48','#64635b','#807b6e','#a19a87','#30291f','#4e3527','#6f4a32','#92623e','#b07b4a','#303633','#515754','#737a70','#533b20','#ac7834','#dfac54']
PAL=[tuple(bytes.fromhex(c[1:])) for c in COLORS]
W=128; H=128; P=np.array([32.,92.]); L=64.; ANGLES=[0,30,60,90]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blank(size=(W,H)):return Image.new('RGBA',size,(0,0,0,0))
def c(i):return PAL[i]+(255,)
def save(im,name):im.save(OUT/name)
def doc(name,x):(OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
# Same static wall layer, a single 75-pixel gap, no second passage.
wall=blank();d=ImageDraw.Draw(wall)
for xmin,xmax in [(0,24),(100,127)]:
 d.rectangle((xmin,82,xmax,107),fill=c(2))
 for row,y in enumerate(range(82,108,7)):
  for x in range(xmin-14+(row%2)*8,xmax+1,16):
   x0=max(xmin,x);x1=min(xmax,x+14)
   if x0<=x1:
    d.rectangle((x0,y,x1,min(107,y+5)),fill=c(3))
    d.line((x0,y,x1,y),fill=c(5));d.line((x0,y+1,x1,y+1),fill=c(4))
    if x1-x0>5:d.point((x0+3,y+3),fill=c(4))
save(wall,'wall_frame_fixed.png')
keeper=blank();d=ImageDraw.Draw(keeper);d.rectangle((98,88,101,96),fill=c(11));d.line((98,88,98,96),fill=c(13));d.rectangle((99,90,100,94),fill=c(0));save(keeper,'keeper_fixed.png')
hinge=blank();d=ImageDraw.Draw(hinge);d.rectangle((23,90,32,94),fill=c(11));d.line((23,90,32,90),fill=c(13));d.ellipse((27,87,37,97),fill=c(11));d.ellipse((28,88,36,96),fill=c(12));d.ellipse((30,90,34,94),fill=c(13));d.point((32,92),fill=c(2));save(hinge,'hinge_fixed.png')
# Canonical local coordinates: pivot=(0,4), tip=(64,4). Length measured between anchors=64.
leaf=blank((65,9));d=ImageDraw.Draw(leaf);d.rectangle((0,0,64,8),fill=c(6));d.rectangle((0,1,63,7),fill=c(8));d.line((2,1,62,1),fill=c(10));d.line((1,7,62,7),fill=c(7));d.line((1,3,62,3),fill=c(9));d.line((5,5,56,5),fill=c(7))
for x in [10,37]:
 d.rectangle((x,0,x+3,8),fill=c(11));d.line((x,0,x,8),fill=c(13));d.line((x+1,1,x+2,1),fill=c(12));d.point((x+2,6),fill=c(13))
save(leaf,'leaf_wood_local.png')
latch=blank((65,9));d=ImageDraw.Draw(latch);d.rectangle((49,1,63,7),fill=c(14));d.rectangle((50,2,62,6),fill=c(15));d.line((50,1,62,1),fill=c(16));d.rectangle((60,3,63,5),fill=c(16));d.point((52,3),fill=c(6));d.point((57,5),fill=c(6));save(latch,'latch_retracted_local.png')
canonical=leaf.copy();canonical.alpha_composite(latch);save(canonical,'leaf_and_latch_local.png')
Y,X=np.indices((H,W));dx=X-P[0];dy=Y-P[1]
def transform(im,a):
 t=math.radians(a);cs=math.cos(t);sn=math.sin(t)
 # Screen y points down: this forward matrix rotates toward the upper room.
 R=np.array([[cs,sn],[-sn,cs]])
 u=cs*dx-sn*dy;v=sn*dx+cs*dy+4
 ix=np.floor(u+.5).astype(int);iy=np.floor(v+.5).astype(int)
 arr=np.array(im);valid=(ix>=0)&(ix<65)&(iy>=0)&(iy<9)
 result=np.zeros((H,W,4),dtype=np.uint8);result[valid]=arr[iy[valid],ix[valid]]
 return Image.fromarray(result),R
background=Image.new('RGBA',(W,H),c(0));save(background,'background.png')
frames=[];metrics=[]
for i,a in enumerate(ANGLES):
 moving,R=transform(canonical,a);lat,_=transform(latch,a)
 save(moving,f'moving_{i:02}.png');save(lat,f'latch_{i:02}.png')
 composite=background.copy()
 for im in [wall,keeper,moving,hinge]:composite.alpha_composite(im)
 save(composite,f'frame_{i:02}.png');frames.append(composite)
 mask=np.array(moving)[:,:,3]>0;wmask=np.array(wall)[:,:,3]>0;kmask=np.array(keeper)[:,:,3]>0
 tip=P+R@np.array([L,0]);latch_anchor=P+R@np.array([56.,0]);pivot=P+R@np.array([0.,0.])
 assert np.allclose(R.T@R,np.eye(2));assert np.allclose(pivot,P);assert abs(np.linalg.norm(tip-P)-L)<1e-10
 assert not np.any(mask&wmask);assert not np.any(mask&kmask)
 assert np.all(np.array(lat)[np.array(lat)[:,:,3]>0]==np.array(moving)[np.array(lat)[:,:,3]>0])
 assert set(np.unique(np.array(moving)[:,:,3])).issubset({0,255})
 metrics.append({'file':f'frame_{i:02}.png','degrees_inward':a,'matrix':R.tolist(),'pivot':pivot.tolist(),'tip_anchor':tip.tolist(),'rigid_anchor_length':float(np.linalg.norm(tip-P)),'latch_anchor':latch_anchor.tolist(),'latch_distance_from_pivot':float(np.linalg.norm(latch_anchor-P)),'keeper_anchor':[99,92],'wall_overlap_pixels':int((mask&wmask).sum()),'keeper_overlap_pixels':int((mask&kmask).sum()),'rendered_opaque_pixels':int(mask.sum()),'sha256':sha(OUT/f'frame_{i:02}.png')})
sheet=blank((W*4,H))
for i,f in enumerate(frames):sheet.paste(f,(W*i,0))
save(sheet,'spritesheet_4x1.png');save(sheet.resize((W*4*4,H*4),Image.Resampling.NEAREST),'preview_nearest_4x.png')
# Lossless GIF palette uses precisely the authored shared palette, no quantizer/dither.
palette=Image.new('P',(1,1));palette.putpalette(sum((list(x) for x in PAL),[])+[0]*(768-3*len(PAL)))
gifs=[f.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
for f,g in zip(frames,gifs):assert np.array_equal(np.array(f.convert('RGB')),np.array(g.convert('RGB')))
gifs[0].save(OUT/'door_motion.gif',save_all=True,append_images=gifs[1:],duration=[1000,500,500,1500],loop=0,disposal=2,optimize=False)
# QA panel adds annotations separately; native frames remain clean.
qa=Image.new('RGB',(W*4,H+32),PAL[0]);qa.paste(sheet.convert('RGB'),(0,0));qd=ImageDraw.Draw(qa)
for i,a in enumerate(ANGLES):
 x=W*i;qd.line((x+32,92,x+96,92),fill=PAL[2]);qd.ellipse((x+30,90,x+34,94),outline=PAL[16]);qd.text((x+4,130),f'{a} deg / L=64',fill=PAL[16]);qd.text((x+4,143),'P=(32,92)',fill=PAL[5])
save(qa.resize((W*4*3,(H+32)*3),Image.Resampling.NEAREST),'QA_geometry_nearest_3x.png')
used={tuple(v) for f in frames for v in np.array(f.convert('RGB')).reshape(-1,3)};assert used<=set(PAL)
# Entire sequence is an unlatched swing study, not a new rescue-state animation.
doc('palette.json',{'colors':COLORS,'count':len(PAL),'dither':False,'alpha_values':[0,255]})
doc('QA-data.json',{'pass':True,'runtimeVerified':False,'engineReady':False,'nativeSpriteApproved':False,'checks':{'four_angles_only':len(frames)==4,'fixed_left_pivot':True,'same_canonical_leaf':True,'constant_64px_anchor_length':True,'latch_follows_same_matrix':True,'fixed_keeper_and_wall':True,'zero_sampled_wall_and_keeper_overlap':True,'shared_17_color_palette':True,'binary_alpha':True,'gif_rgb_exact_match':True},'frames':metrics,'limits':['Raster footprint and pixel count vary with nearest rotation; geometric anchor length is constant, not every raster silhouette measurement.','No continuous swept-volume, depth, contact, stress, collision-grid or engine test. Only four sampled 2D poses tested.','Closed frame is already unlatched; no lock engagement or retraction action is implemented.','One mechanism reference does not replace D08 two-source staging or N12 actual evacuation and consent checks.']})
doc('manifest.json',{'kind':'authored-native-grid-rigid-door-pixel-proposal','method':'Pillow integer pixel drawing and NumPy inverse nearest sampling; no image model; no original-game extraction. Stone/wood/iron/brass and overhead geometry referenced visually from v4; every small-grid pixel is authored.','canvas':[W,H],'angles':ANGLES,'pivot':[32,92],'local_pivot':[0,4],'local_tip':[64,4],'door_centerline_length':64,'local_rgba_size':[65,9],'room_direction':'negative screen Y / above wall','latch_state_all_frames':'retracted / unlatched','layer_order':['background','wall_frame_fixed','keeper_fixed','transformed_leaf_and_latch','hinge_fixed'],'sources':[{'path':p,'sha256':sha(ROOT/p)} for p in SOURCES],'script_sha256':sha(Path(__file__)),'outputs':[{'file':p.name,'sha256':sha(p)} for p in sorted(OUT.iterdir()) if p.suffix in ['.png','.gif']],'runtimeVerified':False,'engineReady':False,'originals_modified':False})
print(json.dumps({'frames':len(frames),'angles':ANGLES,'colors':len(used),'checks':'PASS','out':str(OUT)}))
