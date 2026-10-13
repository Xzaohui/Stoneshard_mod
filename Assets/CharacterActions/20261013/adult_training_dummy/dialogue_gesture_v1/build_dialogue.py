from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil,zipfile
P=Path(__file__).parent
S=935/761
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda s:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',s)
source=P.parent/'interaction_v1/frames/I0_stand.png'
shutil.copy2(source,P/'frames/D0_stand_reuse_I0.png')
frames=[Image.open(source).convert('RGBA')]; records=[{'id':'D0','source':'../interaction_v1/frames/I0_stand.png','sha256':sha(source),'new_drawing':False,'transform':'byte-identical copy'}]
for key in ['D1_explain','D2_withdraw']:
 src=P/'raw'/f'{key}.png'; raw=Image.open(src).convert('RGBA');a=np.array(raw)
 removed=int(((a[:,:,3]>0)&(a[:,:,3]<128)).sum());a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0
 im=Image.fromarray(a).resize(tuple(round(v*S) for v in raw.size),Image.Resampling.NEAREST)
 dy=1380-im.getbbox()[3];can=Image.new('RGBA',(1536,1536));can.alpha_composite(im,(0,dy));can.save(P/'frames'/f'{key}.png');frames.append(can)
 records.append({'id':key,'source':f'raw/{key}.png','raw_sha256':sha(src),'frame_sha256':sha(P/'frames'/f'{key}.png'),'raw_size':raw.size,'new_drawing':True,'scale':S,'translation':[0,dy],'bbox':can.getbbox(),'low_alpha_pixels_removed':removed,'alpha_policy':'alpha >=128 opaque, otherwise zero; transparent RGB zero','mirrored':False})
shutil.copy2(P/'frames/D0_stand_reuse_I0.png',P/'frames/D3_stand_reuse_D0.png');frames.append(frames[0].copy());records.append({'id':'D3','source':'frames/D0_stand_reuse_I0.png','sha256':sha(P/'frames/D3_stand_reuse_D0.png'),'new_drawing':False,'transform':'byte-identical copy'})
seq=[]
for im in frames:
 thumb=im.resize((768,768),Image.Resampling.NEAREST);bg=Image.new('RGB',(768,768),(43,46,52));bg.paste(thumb,(0,0),thumb);seq.append(bg)
seq[0].save(P/'dialogue_gesture_once.gif',save_all=True,append_images=seq[1:],duration=[700,1100,600,900],disposal=2,optimize=False)
review=Image.new('RGB',(1600,1240),(239,238,232));d=ImageDraw.Draw(review)
d.text((25,20),'无武器对话手势｜站立 → 摊掌解释 → 收手 → 回稳',font=F(33),fill='#222831')
d.text((25,75),'新增2张身体姿态；站姿复用已有I0，末帧复用首帧。原创概念，未验原版兼容。',font=F(23),fill='#555b62')
for i,(im,label) in enumerate(zip(frames,['D0 自然站立（复用）','D1 摊掌解释（新绘）','D2 收回手臂（新绘）','D3 回稳（复用D0）'])):
 x=15+i*395;thumb=im.resize((384,384),Image.Resampling.NEAREST);review.paste(thumb,(x,120),thumb);d.line((x,465,x+384,465),fill='#b4b6b7');d.text((x+5,520),label,font=F(21),fill='#30363d')
for i,key in enumerate([1,2]):
 crop=frames[key].crop((615,500,1195,1010));review.paste(crop,(120+i*740,620),crop)
 d.text((45+i*790,570),['解释：眉眼与开放掌形','收手：前臂回到身前'][i],font=F(24),fill='#30363d')
d.text((25,1150),'共同倍率935/761；仅透明清理、最近邻统一缩放、平移。脸、衣褶、鞋口仍有生成漂移。',font=F(22),fill='#555b62')
d.text((25,1190),'四个稀疏阶段，GIF仅示意节奏；不等于完整补间、骨骼恒定或无滑脚动画。',font=F(22),fill='#555b62');review.save(P/'dialogue_gesture_review_zh.png')
m={'status':'awaiting_independent_review','classification':'original_dialogue_keypose_concept','character':'anonymous adult training dummy','new_body_images':2,'reused_existing_source_body_images':1,'unique_body_poses_total':3,'phase_count':4,'reused_display_phases':2,'canvas':[1536,1536],'common_new_raw_scale':S,'reference_visible_body_height':935,'frames':records,'gif_sequence':['D0 existing I0','D1 new','D2 new','D3 reused D0'],'gif_duration_ms':[700,1100,600,900],'gif_loop_extension':False,'new_images_tool':'builtin imagegen','image_processing_authorization':'User approved continued alignment and tool optimization; raw sources retained','runtime_verified':False,'native_ready':False,'equipment_compatibility_verified':False,'engine_origin':None,'native_fps':None,'collision':None,'limitations':['稀疏关键姿态，不是完整补间','脸、衣褶、鞋口有轻微生成漂移','统一尺度与地线不代表骨长/连续足轨迹固定','没有武器/物品/剧情事件，不核原作同类动作','身体为整张平面，不代表原版部件或隐藏结构']}
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
h={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name not in ['SHA256.json','dialogue_gesture_review_package.zip']};(P/'SHA256.json').write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(P/'dialogue_gesture_review_package.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(P.rglob('*')):
  if p.is_file() and p.suffix!='.zip':z.write(p,str(p.relative_to(P)))
print(json.dumps(h,indent=2))
