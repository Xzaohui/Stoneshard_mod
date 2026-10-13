from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil,zipfile
P=Path(__file__).parent;S=935/761
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda s:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',s)
source=P.parent/'interaction_v1/frames/I0_stand.png'
shutil.copy2(source,P/'frames/H0_stand_reuse_I0.png')
frames=[Image.open(source).convert('RGBA')];records=[{'id':'H0','source':'../interaction_v1/frames/I0_stand.png','sha256':sha(source),'new_drawing':False,'transform':'byte-identical copy'}]
for key,rawname in [('H1_recoil','H1_recoil_v2'),('H2_settle','H2_settle')]:
 src=P/'raw'/f'{rawname}.png';raw=Image.open(src).convert('RGBA');a=np.array(raw)
 removed=int(((a[:,:,3]>0)&(a[:,:,3]<128)).sum());a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0
 im=Image.fromarray(a).resize(tuple(round(v*S) for v in raw.size),Image.Resampling.NEAREST)
 dy=1380-im.getbbox()[3];can=Image.new('RGBA',(1536,1536));can.alpha_composite(im,(0,dy));can.save(P/'frames'/f'{key}.png');frames.append(can)
 records.append({'id':key,'source':f'raw/{rawname}.png','raw_sha256':sha(src),'frame_sha256':sha(P/'frames'/f'{key}.png'),'raw_size':raw.size,'new_drawing':True,'scale':S,'translation':[0,dy],'bbox':can.getbbox(),'low_alpha_pixels_removed':removed,'alpha_policy':'alpha>=128 opaque, otherwise zero; transparent RGB zero','mirrored':False})
shutil.copy2(P/'frames/H0_stand_reuse_I0.png',P/'frames/H3_stand_reuse_H0.png');frames.append(frames[0].copy());records.append({'id':'H3','source':'frames/H0_stand_reuse_I0.png','sha256':sha(P/'frames/H3_stand_reuse_H0.png'),'new_drawing':False,'transform':'byte-identical copy'})
seq=[]
for im in frames:
 thumb=im.resize((768,768),Image.Resampling.NEAREST);bg=Image.new('RGB',(768,768),(43,46,52));bg.paste(thumb,(0,0),thumb);seq.append(bg)
seq[0].save(P/'hit_recovery_once.gif',save_all=True,append_images=seq[1:],duration=[700,500,800,900],disposal=2,optimize=False)
review=Image.new('RGB',(1600,1240),(239,238,232));d=ImageDraw.Draw(review)
d.text((25,20),'轻度受击后回稳｜站立 → 后仰屈膝 → 稳住重心 → 站立',font=F(32),fill='#222831')
d.text((25,75),'新增2种身体姿态；首末复用已有站姿。无流血、伤口、倒地或剧情身份。',font=F(23),fill='#555b62')
for i,(im,label) in enumerate(zip(frames,['H0 自然站立（复用）','H1 后仰屈膝（新绘）','H2 稳住重心（新绘）','H3 站立（复用H0）'])):
 x=15+i*395;thumb=im.resize((384,384),Image.Resampling.NEAREST);review.paste(thumb,(x,120),thumb);d.line((x,465,x+384,465),fill='#b4b6b7');d.text((x+5,520),label,font=F(21),fill='#30363d')
for i,k in enumerate([1,2]):
 crop=frames[k].crop((430,800,1210,1410)).resize((663,518),Image.Resampling.NEAREST);review.paste(crop,(50+i*790,615),crop)
 d.text((45+i*790,575),['后仰：手臂反射展开，屈膝支撑','回稳：胸腹回正，双手下落'][i],font=F(24),fill='#30363d')
d.text((25,1150),'共同倍率935/761；仅透明清理、统一最近邻缩放和平移。首稿偏高，已另存并重绘修正。',font=F(22),fill='#555b62')
d.text((25,1190),'4个稀疏阶段，非完整补间；脸、衣褶和鞋形有轻微漂移，骨长/足轨迹/runtime未验。',font=F(22),fill='#555b62');review.save(P/'hit_recovery_review_zh.png')
m={'status':'awaiting_independent_review','classification':'original_light_hit_recovery_keypose_concept','character':'anonymous adult training dummy','new_body_poses_final':2,'generation_outputs':3,'discarded_pose_versions':1,'reused_existing_source_body_images':1,'unique_body_poses_total':3,'phase_count':4,'reused_display_phases':2,'canvas':[1536,1536],'common_new_raw_scale':S,'frames':records,'gif_sequence':['H0 existing I0','H1 new v2','H2 new','H3 reused H0'],'gif_duration_ms':[700,500,800,900],'gif_loop_extension':False,'tool':'builtin imagegen','authorization_message':'Sentinel_cd750e0413208191ad349263d4850431','runtime_verified':False,'native_ready':False,'equipment_compatibility_verified':False,'engine_origin':None,'native_fps':None,'collision':None,'revision':'H1 original approximately825px tall versus761px stance, retained as H1_recoil.png and byte-identical H1_recoil_v1_scale_drift.png; H1_v2 actual generated redraw selected, not frame-specific scaling','limitations':['稀疏关键姿态，不是完整补间','脸、衣褶和鞋形有生成漂移','统一尺度与地线不代表骨长/连续足轨迹固定','不增加剧情伤害、事件或技能','身体为整张平面，不代表原版部件或隐藏结构'],'reference_sources':[{'path':'../interaction_v1/raw/I0_stand.png','sha256':sha(P.parent/'interaction_v1/raw/I0_stand.png')},{'path':'../interaction_v1/frames/I0_stand.png','sha256':sha(source)}]}
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
h={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name not in ['SHA256.json','hit_recovery_review_package.zip']};(P/'SHA256.json').write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(P/'hit_recovery_review_package.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(P.rglob('*')):
  if p.is_file() and p.suffix!='.zip':z.write(p,str(p.relative_to(P)))
print(json.dumps({'records':records,'deliverables':{n:sha(P/n) for n in ['hit_recovery_review_zh.png','hit_recovery_once.gif','hit_recovery_review_package.zip','manifest.json']}},indent=2))
