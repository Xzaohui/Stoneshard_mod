#!/usr/bin/env python3
"""Add one locked pose; read-only reuse of accepted four-frame unlatched swing."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;SRC=OUT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda f:Image.open(SRC/f).convert('RGBA')
P=json.loads((SRC/'palette.json').read_text());colors=[tuple(bytes.fromhex(c[1:])) for c in P['colors']]
accepted=[SRC/f'frame_{i:02}.png' for i in range(4)];before={p.name:sha(p) for p in SRC.iterdir() if p.is_file()}
original=load('leaf_and_latch_local.png')
base=Image.new('RGBA',(70,9));base.paste(original,(0,0));d=ImageDraw.Draw(base)
# Recover proposed housing floor underneath the formerly visible bolt head.
# This small local interpretation is authored, not an extraction of hidden original art.
d.rectangle((60,3,62,5),fill=colors[15]+(255,));d.line((63,3,63,5),fill=colors[14]+(255,))
cover=Image.new('RGBA',(70,9));cover.paste(original.crop((49,1,60,8)),(49,1))
bolt=Image.new('RGBA',(8,3),colors[16]+(255,));bolt.save(OUT/'sliding_bolt_local.png');base.save(OUT/'housing_floor_local.png');cover.save(OUT/'housing_cover_local.png')
def assembly(shift):
 im=base.copy();im.alpha_composite(bolt,(56+shift,3));im.alpha_composite(cover);return im
retracted=assembly(0);extended=assembly(5)
assert np.array_equal(np.array(retracted)[:,:65],np.array(original));assert not np.array(retracted)[:,65:,3].any()
def compose(local):
 f=load('background.png')
 for name in ['wall_frame_fixed.png','keeper_fixed.png']:f.alpha_composite(load(name))
 f.alpha_composite(local,(32,88));f.alpha_composite(load('hinge_fixed.png'));return f
reconstructed=compose(retracted);assert np.array_equal(np.array(reconstructed),np.array(load('frame_00.png')))
locked=compose(extended);locked.save(OUT/'closed_locked.png');extended.save(OUT/'leaf_locked_local.png')
frames=[locked]+[load(f'frame_{i:02}.png') for i in range(4)]
names=['closed_locked.png','closed_retracted.png','inward_30.png','inward_60.png','inward_90.png']
for name,im in zip(names[1:],frames[1:]):im.save(OUT/name)
sheet=Image.new('RGBA',(128*5,128))
for i,im in enumerate(frames):sheet.paste(im,(i*128,0))
sheet.save(OUT/'spritesheet_5x1.png');sheet.resize((2560,512),Image.Resampling.NEAREST).save(OUT/'preview_nearest_4x.png')
closeup=Image.new('RGBA',(768,216))
for i,im in enumerate(frames[:2]):closeup.paste(im.crop((76,83,108,101)).resize((384,216),Image.Resampling.NEAREST),(i*384,0))
closeup.save(OUT/'latch_engagement_nearest_12x.png')
pal=Image.new('P',(1,1));pal.putpalette(sum((list(v) for v in colors),[])+[0]*(768-len(colors)*3))
gif=[im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE) for im in frames]
for a,b in zip(gif,frames):assert np.array_equal(np.array(a.convert('RGB')),np.array(b.convert('RGB')))
gif[0].save(OUT/'full_sequence.gif',save_all=True,append_images=gif[1:],duration=[1000,750,500,500,1500],loop=0,disposal=2,optimize=False)
# The only allowed closed-pose difference is the bolt travel strip.
a=np.array(locked);b=np.array(frames[1]);diff=np.any(a!=b,axis=2);ys,xs=np.where(diff)
allowed=np.zeros((128,128),bool);allowed[91:94,92:101]=True
assert not (diff&~allowed).any()
# The keeper dark recess is x99..100, y90..94. Extended bolt passes into y91..93.
contact=np.zeros((128,128),bool);contact[91:94,99:101]=True
assert np.all(a[contact,:3]==colors[16]);assert np.all(b[contact,:3]==colors[0])
assert before=={p.name:sha(p) for p in SRC.iterdir() if p.is_file()}
report={'status':'authored locked-to-retracted-to-inward opening proposal','runtimeVerified':False,'physicalLockVerified':False,'accepted_four_frames_changed':False,'accepted_parent_files_sha256':before,'script_sha256':sha(Path(__file__)),'frames':[{'file':name,'sha256':sha(OUT/name),'state':state,'angle':angle} for name,state,angle in zip(names,['locked','retracted','retracted','retracted','retracted'],[0,0,30,60,90])],'mechanism':{'same_sliding_bolt_size':[8,3],'retracted_local_xy':[56,3],'extended_local_xy':[61,3],'translation':[5,0],'hidden_tail':'At retracted pose local x56..59 is occluded by the unchanged housing cover; exposed head x60..63 matches accepted frame exactly.','keeper_recess_global_xyxy':[99,90,100,94],'extended_bolt_engagement_xyxy':[99,91,100,93],'insert_depth_in_recess_px':2,'housing_floor':'Restored authored colors at local x60..63,y3..5; hidden geometry proposal only.'},'validation':{'retracted_reconstruction_pixel_identical':True,'accepted_four_png_pixels_identical':True,'parent_files_byte_identical':True,'same_bolt_only_translated':True,'same_pivot_wall_keeper_housing':True,'diff_only_bolt_travel_strip':True,'changed_pixels_locked_to_retracted':int(diff.sum()),'diff_bbox_xyxy':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'expected_bolt_keeper_engagement_pixels':int(contact.sum()),'gif_rgb_identical':True},'limits':['Keeper lip overlap and 2px wall-side recess insertion are expected bolt engagement, not wooden door-panel penetration.','The native plan-view drawing cannot prove real socket depth, contact, manufacturing tolerances or physical lock function.','Five poses only; no intermediate bolt-travel interpolation or continuous swept-volume verification.','GIF loop jumps back to locked for preview; it does not implement reverse closing/locking.','Does not certify rescue, evacuation, consent, evidence or engine integration.'],'outputs':[{'file':p.name,'sha256':sha(p)} for p in sorted(OUT.iterdir()) if p.suffix in ['.png','.gif']]}
(OUT/'metadata.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report['validation']))
