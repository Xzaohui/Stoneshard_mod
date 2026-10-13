from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,math,json,hashlib,shutil
p=Path(__file__).resolve().parent;old=p.parent/'attack_v2_geometry';sz=(1536,1536);scale=1536/1254
sw=Image.open(old/'layers/canonical_wood_sword.png').convert('RGBA');sw.save(p/'layers/canonical_wood_sword.png')
def safe(im):
 a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def save(im,path):safe(im).save(path)
meta=[]
# raw coordinates are authored landmark estimates, not skeleton sockets
conf=[('G1_upper_guard_v2','defense','G1',(793,608),-80,(0,0),[(754,583),(782,572),(815,580),(832,604),(823,632),(790,644),(763,624)],[(482,1110),(804,1111)],(620,775)),('G2_recover','defense','G2',(840,772),40,(0,0),[(808,741),(842,739),(870,758),(870,788),(844,812),(815,795)],[(482,1110),(804,1111)],(620,775)),('E1_shift','dodge','E1',(748,848),40,(-70,8),[(721,821),(750,813),(775,829),(785,857),(768,879),(739,881),(715,862)],[(535,1107),(921,1106)],(590,802)),('E2_support_v2','dodge','E2',(799,858),45,(0,8),[(766,830),(800,816),(831,836),(834,864),(816,890),(783,886),(759,868)],[(478,1111),(757,1087)],(593,775))]
for raw,seq,id,grip,deg,off,poly,feet,pelvis in conf:
 im=Image.open(p/'raw'/f'{raw}.png').convert('RGBA')
 # localized white artifact and faint fringe removal only, preserving surrounding hand silhouette
 if id=='G2':
  a=np.array(im);region=a[850:879,462:510];m=(region[:,:,:3].min(2)>145)|(region[:,:,3]<200);region[m]=(0,0,0,0);im=Image.fromarray(a)
 im=im.resize(sz,Image.Resampling.NEAREST);body=Image.new('RGBA',sz);body.alpha_composite(im,off)
 def pt(q):return [round(q[0]*scale+off[0]),round(q[1]*scale+off[1])]
 grip=pt(grip);mask=Image.new('L',sz);ImageDraw.Draw(mask).polygon([pt(x) for x in poly],fill=255);hand=Image.new('RGBA',sz);hand.paste(body,(0,0),mask)
 th=math.radians(deg-90);c=math.cos(th);s=math.sin(th);gx,gy=grip;coeff=(c,s,64-c*gx-s*gy,-s,c,80+s*gx-c*gy)
 weapon=sw.transform(sz,Image.Transform.AFFINE,coeff,resample=Image.Resampling.NEAREST).resize((192,192),Image.Resampling.NEAREST).resize(sz,Image.Resampling.NEAREST)
 out=Image.alpha_composite(Image.alpha_composite(body,weapon),hand)
 for name,x in [('body_base',body),('sword_rigid',weapon),('hand_foreground',hand)]:save(x,p/'layers'/f'{id}_{name}.png')
 mask.save(p/'masks'/f'{id}_hand_foreground_mask.png');save(out,p/'frames'/seq/f'{id}.png')
 def swordpt(y):return [round(gx-s*(y-80),3),round(gy+c*(y-80),3)]
 meta.append(dict(id=id,sequence=seq,raw=f'raw/{raw}.png',frame_path=f'frames/{seq}/{id}.png',body_base=f'layers/{id}_body_base.png',sword_layer=f'layers/{id}_sword_rigid.png',foreground_hand=f'layers/{id}_hand_foreground.png',hand_mask=f'masks/{id}_hand_foreground_mask.png',grip_anchor=grip,rotation_degrees_screen_axis=deg,blade_base=swordpt(140),blade_tip=swordpt(460),canonical_blade_length=320,scale=1,source_canvas_normalization=scale,registration_translation=list(off),screen_left_foot=pt(feet[0]),screen_right_foot=pt(feet[1]),pelvis_proxy_not_true_mass_center=pt(pelvis),head_center=pt((625,510 if id!='E1' else 563)),support='both feet' if seq=='defense' else 'screen-left primary; screen-right transitional',body_bbox=list(body.getbbox()),extended_bbox=list(out.getbbox()),marker_precision='manual estimate approximately +/-16px; no bone/skeleton inference'))
# existing neutral serves both starts, no false new-pose count
for seq,id in [('defense','G0'),('dodge','E0')]:
 out=Image.open(old/'frames/D0_guard.png');save(out,p/'frames'/seq/f'{id}.png')
 for suf in ['body_base','sword_rigid','hand_foreground']:save(Image.open(old/'layers'/f'D0_guard_{suf}.png'),p/'layers'/f'{id}_{suf}.png')
 meta.append(dict(id=id,sequence=seq,reused_pose='../attack_v2_geometry/D0',frame_path=f'frames/{seq}/{id}.png',body_base=f'layers/{id}_body_base.png',sword_layer=f'layers/{id}_sword_rigid.png',foreground_hand=f'layers/{id}_hand_foreground.png',grip_anchor=[982,1030],rotation_degrees_screen_axis=45,blade_base=[1024.426,1072.426],blade_tip=[1250.701,1298.701],canonical_blade_length=320,scale=1,screen_left_foot=[620,1345],screen_right_foot=[928,1370],pelvis_proxy_not_true_mass_center=[754,974],head_center=[764,600],support='both feet',body_bbox=list(Image.open(old/'layers/D0_guard_body_base.png').getbbox()),extended_bbox=list(out.getbbox())))
meta.sort(key=lambda q:q['id'])
checks=[]
for m in meta:
 fp=p/m['frame_path'];m['sha256']=hashlib.sha256(fp.read_bytes()).hexdigest();rec=Image.alpha_composite(Image.alpha_composite(Image.open(p/m['body_base']),Image.open(p/m['sword_layer'])),Image.open(p/m['foreground_hand']));a=np.array(Image.open(fp));checks.append(dict(id=m['id'],pixel_exact_recomposition=bool(np.array_equal(np.array(safe(rec)),a)),alpha_zero_rgb_zero=bool((a[a[:,:,3]==0,:3]==0).all())))
manifest=dict(asset_id='UNNAMED_ADULT_TRAINING_MODEL_DEFENSE_DODGE_V1',logical_canvas=list(sz),logical_ground_y=1380,not_a_story_character=True,scope='Mod original guard and lateral weight-shift key-pose study; not native Stoneshard animation reproduction',handedness='same screen-right weapon hand; anatomical side unverified',canonical_weapon='layers/canonical_wood_sword.png',canonical_weapon_sha256=hashlib.sha256((p/'layers/canonical_wood_sword.png').read_bytes()).hexdigest(),canonical_grip=[64,80],canonical_blade_base=[64,140],canonical_blade_tip=[64,460],layer_order=['body_base','sword_rigid','hand_foreground'],frames=meta,engine_origin=None,collision=None,texture_trim_offset=None,native_fps=None,native_directions=None,runtime_verified=False,equipment_compatibility_verified=False,preview_only=True,status='awaiting independent review',new_articulated_poses=4,generated_raw_variants=6,notes=['G1 v1 rejected for scale drift; G1 v2 retains G2 camera/scale','E2 v1 open glove rejected; E2 v2 closes same glove','All selected new bodies normalized at one identical factor 1536/1254; no per-frame bounding-box scaling','Canonical sword copied unchanged from reviewed geometry asset; rigid rotation/translation only, 8px contour sampling','G2 isolated white foreign pixels and narrow fringe removed to transparency; finger silhouette preserved; raw unchanged','Dodge has coarse articulated weight shift and regaining support, not complete locomotion or invulnerability mechanism','Feet and pelvis are hand-marked visual references; continuous trajectories and foot slip remain unvalidated'])
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'recomposition_checks.json').write_text(json.dumps(checks,indent=2))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';h=ImageFont.truetype(font,34);f=ImageFont.truetype(font,25)
sheet=Image.new('RGB',(1536,1320),(35,39,43));d=ImageDraw.Draw(sheet);d.text((28,15),'训练动作 · 防御与侧撤关键姿态',font=h,fill=(242,231,208));d.text((28,64),'4 个新身体姿态 / 同一木剑层 / 原创动作提案',font=f,fill=(169,190,197))
for row,(seq,ids,labels) in enumerate([('defense',['G0','G1','G2'],['① 预备','② 护住上身','③ 回稳']),('dodge',['E0','E1','E2'],['① 预备','② 移重侧撤','③ 重新支撑'])]):
 ims=[]
 for i,(id,label) in enumerate(zip(ids,labels)):
  im=Image.open(p/'frames'/seq/f'{id}.png');thumb=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(thumb,(i*512,110+row*565),thumb);d.text((i*512+42,598+row*565),label,font=f,fill=(236,222,193))
  bg=Image.new('RGB',(768,768),(35,39,43));r=im.resize((768,768),Image.Resampling.NEAREST);bg.paste(r,(0,0),r);ims.append(bg)
 ims[0].save(p/f'{seq}_preview_once.gif',save_all=True,append_images=ims[1:],duration=[650,700,1400],disposal=2)
d.text((28,1232),'单次关键帧检视；中间过渡、连续足轨迹与动作时序仍待补。',font=f,fill=(183,199,203));d.text((28,1273),'未接游戏运行，不代表原生技能、换装或无敌帧已完成。',font=f,fill=(183,199,203));sheet.save(p/'defense_dodge_review_zh.png')
print(checks)
