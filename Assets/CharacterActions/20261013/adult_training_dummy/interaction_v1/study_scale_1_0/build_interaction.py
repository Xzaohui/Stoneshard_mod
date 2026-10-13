from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np,json,hashlib,zipfile
P=Path(__file__).parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def F(s):return ImageFont.truetype(font,s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ids=['I0_stand','I1_bend','I2_reach']
trans=[(141,252),(141,257),(141,266)]
phases=['站立准备 · 双手空置','屈膝俯身 · 左侧手扶膝','近地伸手 · 不指认拾取物']
# Landmark coordinates are visual estimates in raw image coordinates, not engine data.
marks=[{'head':[624,500],'screen_left_hand':[451,852],'screen_right_hand':[792,865],'screen_left_knee':[543,935],'screen_right_knee':[722,947],'reach_tip':[795,910]}, {'head':[750,661],'screen_left_hand':[526,869],'screen_right_hand':[843,982],'screen_left_knee':[529,936],'screen_right_knee':[716,940],'reach_tip':[866,1037]}, {'head':[775,721],'screen_left_hand':[532,868],'screen_right_hand':[890,1041],'screen_left_knee':[530,935],'screen_right_knee':[721,940],'reach_tip':[935,1086]}]
frames=[];records=[]
for i,key in enumerate(ids):
 src=P/'raw'/f'{key}.png'; a=np.array(Image.open(src).convert('RGBA')); removed=int(((a[:,:,3]>0)&(a[:,:,3]<128)).sum());a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0
 im=Image.fromarray(a);can=Image.new('RGBA',(1536,1536));can.alpha_composite(im,trans[i]); arr=np.array(can);arr[arr[:,:,3]==0,:3]=0;can=Image.fromarray(arr);can.save(P/'frames'/f'{key}.png');frames.append(can)
 # Disjoint whole-character layer plus empty FX: truthful flat source, no invented recovered anatomy.
 can.save(P/'layers'/f'{key}_body_flat.png'); Image.new('RGBA',can.size).save(P/'layers'/f'{key}_fx_empty.png')
 lm={k:[v[0]+trans[i][0],v[1]+trans[i][1]] for k,v in marks[i].items()}
 records.append({'frame_id':key,'phase':phases[i],'source':str(src.relative_to(P)),'raw_sha256':sha(src),'frame_sha256':sha(P/'frames'/f'{key}.png'),'raw_size':[1254,1254],'translation':list(trans[i]),'scale':1.0,'mirrored':False,'alpha_policy':'Threshold at 128 to binary alpha; zero RGB when transparent; raw unchanged','removed_low_alpha_pixels':removed,'bbox':can.getbbox(),'ground_y':1380,'root':[768,1380],'support':'both boots; screen-right boot baseline aligned, screen-left minor generated contour drift','landmarks_estimated':lm,'reach_tip_ground_gap_estimate':1380-lm['reach_tip'][1],'weapon':None,'held_item':None,'layers':[f'layers/{key}_body_flat.png',f'layers/{key}_fx_empty.png']})
frames[0].save(P/'frames/I3_recover_reuse_I0.png')
seq=[0,1,2,1,0]; durations=[600,450,850,450,850]
preview=[]
for idx in seq:
 c=Image.new('RGB',(768,768),(39,42,48));c.paste(frames[idx].resize((768,768),Image.Resampling.NEAREST),(0,0),frames[idx].resize((768,768),Image.Resampling.NEAREST));preview.append(c)
preview[0].save(P/'interaction_preview_once.gif',save_all=True,append_images=preview[1:],duration=durations,disposal=2,optimize=False)
review=Image.new('RGB',(1600,1100),(238,237,230)); d=ImageDraw.Draw(review);d.text((28,20),'近地交互：原创关键姿态提案｜全程无武器',font=F(34),fill=(30,35,40));d.text((28,72),'3张新身体图；回稳复用站姿。不是原版复刻、完整补间动画或运行资产。',font=F(23),fill=(55,60,65))
for j,idx in enumerate([0,1,2,0]):
 x=20+j*395; thumb=frames[idx].resize((384,384),Image.Resampling.NEAREST);review.paste(thumb,(x,135),thumb);d.line((x,480,x+384,480),fill=(140,145,150));d.text((x+8,535),['I0 站立准备','I1 屈膝俯身','I2 近地伸手','I3 回稳（复用I0）'][j],font=F(22),fill=(30,35,40))
# Lower body detail at 1:1, explicit no anatomical layer reconstruction.
for j,idx in enumerate([1,2]):
 crop=frames[idx].crop((550,1070,1100,1400));review.paste(crop,(40+j*770,615),crop)
 d.text((40+j*770,970),['膝、衣摆与扶膝手','近地伸手：指尖约28px离地'][j],font=F(24),fill=(30,35,40))
d.text((28,1030),'固定1536²画布 / 全程比例1.0 / 仅透明清理与平移对齐 / 近脚底y1380',font=F(22),fill=(55,60,65)); review.save(P/'interaction_review_zh.png')
m={'status':'awaiting_independent_review','classification':'original_mod_keypose_proposal','character':'adult_training_dummy; no narrative identity','canvas':[1536,1536],'unique_new_body_images':3,'phase_count':4,'preview_sequence':['I0','I1','I2','I1 reused as rise intermediate','I0 reused as recovered'],'preview_only':True,'preview_loop_extension':False,'source_animation_evidence':'No verified original near-ground interaction joint animation; no new search performed','reference_paths':['../../../../ReferenceAudit/20261013/actions/REFERENCE_AUDIT.md','../../../../ReferenceAudit/20261013/actions/KEYFRAME_BRIEF.md'],'input_reference':'../attack_v2_geometry/layers/D0_guard_body_base.png','input_reference_sha256':sha(P.parent/'attack_v2_geometry/layers/D0_guard_body_base.png'),'engine_origin':None,'collision':None,'texture_trim_offset':None,'native_fps':None,'native_directions':None,'layers_note':'Body retained flat; FX transparent. Not native skeletal layers. No weapon layer necessary.','frames':records}
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
