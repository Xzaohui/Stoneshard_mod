from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,json,hashlib,numpy as np,zipfile
p=Path(__file__).resolve().parent;old=p.parent/'attack_v2_geometry';sz=(1536,1536);k=1536/1254
sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
def safe(im):
 a=np.array(im.convert('RGBA'));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def save(im,path):safe(im).save(path)
sw=Image.open(old/'layers/canonical_wood_sword.png').convert('RGBA');sw.save(p/'layers/canonical_wood_sword.png')
r=Image.open(p/'raw/wood_shield_raw.png').convert('RGBA');bbox=r.getchannel('A').point(lambda x:255 if x>=16 else 0).getbbox();r=r.crop(bbox);factor=416/max(r.size);r=r.resize(tuple(round(x*factor) for x in r.size),Image.Resampling.NEAREST);shield=Image.new('RGBA',(432,432));shield.alpha_composite(r,((432-r.width)//2,(432-r.height)//2));shield=shield.resize((54,54),Image.Resampling.NEAREST).resize((432,432),Image.Resampling.NEAREST);save(shield,p/'layers/canonical_wood_shield.png')
def rigid(im,anchor,target,degrees):
 t=math.radians(degrees);c=math.cos(t);s=math.sin(t);x,y=target;ax,ay=anchor
 return im.transform(sz,Image.Transform.AFFINE,(c,s,ax-c*x-s*y,-s,c,ay+s*x-c*y),resample=Image.Resampling.NEAREST)
def pt(q):return [round(v*k) for v in q]
conf=[('S0','准备',None,[982,1030],45,[545,1015],-10,None),('S1','举盾护上身','S1_raise',pt((827,774)),40,pt((597,693)),0,[(791,735),(825,729),(867,753),(864,800),(829,820),(794,794)]),('S2','承压收紧','S2_brace',pt((770,785)),60,pt((620,690)),8,[(735,752),(773,744),(803,762),(807,792),(784,817),(749,808)]),('S3','回稳（复用准备）',None,[982,1030],45,[545,1015],-10,None)]
frames=[];checks=[]
for id,phase,raw,grip,deg,sg,sd,poly in conf:
 if raw:
  body=Image.open(p/'raw'/f'{raw}.png').convert('RGBA').resize(sz,Image.Resampling.NEAREST)
  mask=Image.new('L',sz);ImageDraw.Draw(mask).polygon([pt(q) for q in poly],fill=255);hand=Image.new('RGBA',sz);hand.paste(body,(0,0),mask)
  sword=rigid(sw,(64,80),grip,deg-90).resize((192,192),Image.Resampling.NEAREST).resize(sz,Image.Resampling.NEAREST)
 else:
  body=Image.open(old/'layers/D0_guard_body_base.png').convert('RGBA');hand=Image.open(old/'layers/D0_guard_hand_foreground.png').convert('RGBA');sword=Image.open(old/'layers/D0_guard_sword_rigid.png').convert('RGBA');mask=Image.open(old/'masks/D0_guard_hand_foreground_mask.png').convert('L')
 if not raw:
  patch=Image.open(p/'raw/S0_closed_glove.png').convert('RGBA').resize(sz,Image.Resampling.NEAREST);pm=Image.new('L',sz);ImageDraw.Draw(pm).rectangle((486,954,610,1092),fill=255);body.paste(patch,(0,0),pm);pm.save(p/'masks'/f'{id}_local_closed_glove_patch_mask.png')
 sl=rigid(shield,(216,216),sg,sd);occ=sl.getchannel('A');out=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(body,sword),hand),sl)
 layers={}
 for name,im in [('body_base',body),('sword_rigid',sword),('sword_hand_foreground',hand),('shield_rigid',sl)]:
  path=f'layers/{id}_{name}.png';save(im,p/path);layers[name]=path
 mask.save(p/'masks'/f'{id}_sword_hand_mask.png');occ.save(p/'masks'/f'{id}_shield_occlusion_mask.png');save(out,p/'frames'/f'{id}.png')
 rec=Image.new('RGBA',sz)
 for path in layers.values():rec=Image.alpha_composite(rec,Image.open(p/path))
 final=np.array(Image.open(p/'frames'/f'{id}.png'));checks.append(dict(id=id,pixel_exact_recomposition=bool(np.array_equal(np.array(safe(rec)),final)),alpha0_rgb_zero=bool((final[final[:,:,3]==0,:3]==0).all())))
 frames.append(dict(id=id,phase=phase,raw=f'raw/{raw}.png' if raw else None,reused_body=None if raw else '../attack_v2_geometry/D0_guard',frame_path=f'frames/{id}.png',sha256=sha(p/'frames'/f'{id}.png'),layers=layers,sword_hand_mask=f'masks/{id}_sword_hand_mask.png',shield_occlusion_mask=f'masks/{id}_shield_occlusion_mask.png',sword_grip=grip,sword_degrees_screen_axis=deg,shield_grip_hidden_behind_boss=sg,shield_rotation_clockwise=sd,shield_scale=1,body_normalization=k if raw else 1,body_bbox=body.getbbox(),extended_bbox=out.getbbox(),support='Both boots grounded; visually estimated, not physically validated',screen_left_foot=pt((476,1110)) if raw else [620,1345],screen_right_foot=pt((811,1110)) if raw else [928,1370]))
manifest=dict(asset_id='UNNAMED_ADULT_TRAINING_SHIELD_GUARD_V1',logical_canvas=sz,logical_ground_y=1380,standing_body_reference_height_px=935,new_body_poses=2,new_prop_sources=1,generated_raw_count=4,local_glove_edit_count=1,presented_phases=4,recovery_reuses_preparation=True,scope='Mod原创持盾关键姿态，不是原版具体技能、完整动画或伤害命中',handedness='same screen-right sword hand, screen-left shield hand; no whole-person mirror',canonical_sword='layers/canonical_wood_sword.png',canonical_sword_sha256=sha(p/'layers/canonical_wood_sword.png'),canonical_sword_grip=[64,80],canonical_sword_blade_base=[64,140],canonical_sword_blade_tip=[64,460],canonical_blade_length=320,canonical_shield='layers/canonical_wood_shield.png',canonical_shield_sha256=sha(p/'layers/canonical_wood_shield.png'),shield_source_crop=bbox,shield_source_uniform_scale=factor,shield_content_diameter_px=416,shield_layer_size=[432,432],shield_grip=[216,216],shield_grip_type='center grip behind boss, hidden in front view; no strap rendering claim',layer_order=['body_base','sword_rigid','sword_hand_foreground','shield_rigid'],frames=frames,engine_origin=None,collision=None,native_fps=None,native_directions=None,runtime_verified=False,equipment_compatibility_verified=False,independent_review='pending root reviewer')
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'recomposition_checks.json').write_text(json.dumps(checks,indent=2))
provenance=[]
for name,source in [('wood_shield_raw',None),('S0_closed_glove',old/'layers/D0_guard_body_base.png'),('S1_raise',p.parent/'defense_dodge_v1/raw/G2_recover.png'),('S2_brace',p/'raw/S1_raise.png')]:provenance.append(dict(output=f'raw/{name}.png',sha256=sha(p/'raw'/f'{name}.png'),reference=str(source.relative_to(p.parent)) if source else None,reference_sha256=sha(source) if source else None))
(p/'generation_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,25);h=ImageFont.truetype(font,36)
board=Image.new('RGB',(1800,1080),(35,39,43));d=ImageDraw.Draw(board);d.text((32,20),'持盾防御 · 原创关键姿态',font=h,fill='white');d.text((32,76),'2个新身体姿态 + 1处闭手修正 + 1张木盾；回稳复用准备，装备固定尺寸。',font=f,fill=(190,208,210))
ims=[]
for i,fr in enumerate(frames):
 im=Image.open(p/fr['frame_path']);thumb=im.resize((450,450),Image.Resampling.NEAREST);board.paste(thumb,(i*450,125),thumb);d.text((i*450+25,575),fr['id']+' '+fr['phase'],font=f,fill=(238,221,186))
 body=Image.open(p/fr['layers']['body_base']);crop=body.crop((410,550,1110,1130)).resize((420,348),Image.Resampling.NEAREST);board.paste(crop,(i*450+15,620),crop)
 bg=Image.new('RGB',(768,768),(35,39,43));small=im.resize((768,768),Image.Resampling.NEAREST);bg.paste(small,(0,0),small);ims.append(bg)
d.text((28,972),'下排：盾层关闭，核对完整肩→肘→腕；盾后手未截断。',font=f,fill=(185,202,205));d.text((28,1015),'单次4阶段检视。未接runtime；未验证连续过渡、换装、原生方向或判定。',font=f,fill=(185,202,205));board.save(p/'shield_guard_review_zh.png')
ims[0].save(p/'shield_guard_preview_once.gif',save_all=True,append_images=ims[1:],duration=[650,800,850,1400],disposal=2)
print(checks)
