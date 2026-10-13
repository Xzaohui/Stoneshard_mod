"""Transparent cleanup and review layout only; never paints anatomy."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib
P=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected=['W0_left_contact','W1_passing_revision1','W2_right_contact_revision1']
records=[]
for p in sorted((P/'raw').glob('*.png')):
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 clean=Image.new('RGBA',im.size); im.putalpha(a); clean.paste(im,(0,0),a)
 dst=P/'frames'/p.name; clean.save(dst)
 records.append({'id':p.stem,'raw':str(p.relative_to(P)),'raw_sha256':sha(p),'frame':str(dst.relative_to(P)),'frame_sha256':sha(dst),'size':im.size,'visible_bbox':clean.getbbox(),'selected_for_review':p.stem in selected,'transform':{'alpha_threshold':128,'transparent_rgb_zero':True,'scale':1,'translation':[0,0]}})
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=ImageFont.truetype(font,25); title=ImageFont.truetype(font,35)
board=Image.new('RGB',(1740,1000),(233,230,221)); d=ImageDraw.Draw(board)
d.text((35,20),'成年训练样板｜自然短步关键姿态研究 v1',fill='#262d32',font=title)
d.text((35,76),'三阶段候选 + 两次定点修订；左右腿连续性未通过，不制 GIF',fill='#9b422d',font=f)
labels=['W0 左脚接触候选','W1 通过位修订｜腿侧存疑','W2 右脚接触修订｜仍似同腿']
notes=['后跟抬起、前靴着地可读','前足抬起可读；支撑侧未锁定','未清楚反转大腿遮挡关系']
for i,k in enumerate(selected):
 im=Image.open(P/'frames'/f'{k}.png')
 # common crop and nearest-neighbor scale for review, no per-frame fitting
 im=im.crop((360,325,900,1150)).resize((486,742),Image.Resampling.NEAREST)
 x=40+i*575
 board.paste(im,(x,150),im)
 d.text((x,113),labels[i],fill='#222b32',font=f)
 d.text((x,906),notes[i],fill='#753f32',font=f)
d.text((35,952),'保留5张生图原稿。只做透明清理与排版；非完整循环、非引擎资产验收。',fill='#42484c',font=f)
board.save(P/'basic_walk_review_zh.png')
ref=P.parent/'interaction_v1/raw/I0_stand.png'
manifest={'status':'research_only_hold_no_gif','generator':'builtin image_gen','character':'unidentified adult training dummy, not Chiler','requested_key_poses':3,'initial_body_generations':3,'targeted_revisions':2,'raw_image_count':5,'validated_alternating_walk':False,'gif_created':False,'runtime_verified':False,'native_ready':False,'source_reference':{'path':str(ref.relative_to(P.parents[4])),'sha256':sha(ref)},'records':records,'reference_graph':{'W0_left_contact':['I0_stand'],'W1_passing':['W0_left_contact','I0_stand'],'W1_passing_revision1':['W1_passing'],'W2_right_contact':['W0_left_contact'],'W2_right_contact_revision1':['W2_right_contact']},'review_board':{'file':'basic_walk_review_zh.png','sha256':sha(P/'basic_walk_review_zh.png'),'shared_crop':[360,325,900,1150],'shared_preview_scale':0.9},'limitations':['W1 initial pose remains trailing rather than passing.','W1 revision lifts the foot but support-side identity appears swapped.','W2 initial and revision fail to clearly reverse near/far thigh occlusion from W0.','Foot volume and cuff cluster drift remains; no fixed skeletal correspondence verified.','Contact coordinates do not establish temporal no-sliding.']}
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(P/'SHA256.json').write_text(json.dumps({str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name!='SHA256.json'},ensure_ascii=False,indent=2)+'\n')
