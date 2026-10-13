from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib
p=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterActions/20261013/adult_training_dummy/sideview_contact_pilot_v1')
files=['S0_stand.png','S1_contact_right_front.png','S2_contact_left_front.png']
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=ImageFont.truetype(font,24); small=ImageFont.truetype(font,19)
board=Image.new('RGB',(1881,820),'#efece4'); d=ImageDraw.Draw(board)
d.text((28,16),'真侧视接触位试验｜整组独审未通过，仅保留静态研究',font=f,fill='#272727')
labels=['S0 侧视静站（已通过独审）','S1 未通过：靴形漂移','S2 未通过：腰扣错位']
for i,(name,label) in enumerate(zip(files,labels)):
 im=Image.open(p/'raw'/name).convert('RGBA').resize((627,627),Image.Resampling.NEAREST)
 board.paste(im,(627*i,68),im)
 d.text((627*i+24,56),label,font=f,fill='#272727')
 notes=[['侧视是设计推定','远腿、远手多被遮挡'],['近腿前伸、近臂后摆','前靴翘尖／鞋体积需审'],['近腿后伸、近臂前摆','腰扣位置漂移／前足接触需审']][i]
 for j,t in enumerate(notes):d.text((627*i+24,710+28*j),t,font=small,fill='#413b34')
d.text((24,786),'全图统一0.5倍最近邻排版；未拼改身体、未逐帧拉伸、未制作GIF。',font=small,fill='#413b34')
board.save(p/'sideview_contact_review_zh.png')
m=json.loads((p/'manifest.json').read_text())
m['status']='FAILED contact study: S1 boot shape/length changed; S2 belt buckle moved behind torso. S0 sideview concept independently passed. Hard cap reached; no further generation.'
m['new_images_used']=3
m['S0_review']='QA-independent-S0.json'
m['outputs']=[]
for fn in files:
 q=p/'raw'/fn; im=Image.open(q); a=im.getchannel('A')
 m['outputs'].append({'path':'raw/'+fn,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'size':list(im.size),'mode':im.mode,'alpha_ge_128_bbox':a.point(lambda x:255 if x>=128 else 0).getbbox(),'body_edits':False,'reference':'original I0' if fn==files[0] else 'raw/S0_stand.png'})
m['limits'][0]='Three raw images only, hard cap reached. No extra generation or repairs. No GIF or continuous/natural walking claim.'
m['limits'][2]='S0 was independently approved before S1/S2 generation. S1/S2 contact study failed independent review. S0 pass remains valid.'
m['review_board']={'path':'sideview_contact_review_zh.png','operation':'unmodified full canvases, common 0.5 nearest-neighbor scale, pasted on neutral background with labels; no body reconstruction'}
m['contact_self_review']={'S1':'Near lighter leg forward, near arm back; heel contact suggested but upturned toe/boot length drift requires independent review.','S2':'Near lighter leg backward, near arm forward, far darker leg forward; hip overlap changes visibly. Front sole flatter than intended heel contact. Belt buckle position drifts to rear side.','scope':'These are observations, not animation acceptance or proven anatomical continuity.'}
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(p/'README.md').write_text('''# 真侧视接触位试验 v1\n\n全试验3张新图已用尽，停止生图及补救。S0先通过独立相机／比例／衣装／近靴审查（QA-independent-S0.json），随后各生成1张S1/S2；接触位整组独审未通过，S1靴尖卷翘／靴长改变原设计，S2腰扣移到身体后侧；S0侧视门槛仍通过。\n\n角色是同一成年训练样板。原锚interaction_v1/raw/I0_stand.png，锚及所有原稿SHA见manifest.json。新侧视仅是原创设计推定，不是Stoneshard实际规格。prompts保留每次完整内置imagegen提示词。\n\nraw内S0_stand.png、S1_contact_right_front.png、S2_contact_left_front.png均为完整未修改工具原稿，没有脚本拼腿、镜像、修身体或逐帧拉伸。S1和S2均使用通过的S0为唯一图像锚。\n\nsideview_contact_review_zh.png使用整张画布统一0.5倍最近邻排版，未按人物包围框分别拉伸；只贴图及说明文字，不修改身体。原稿画布都是1254²，但各图人物覆盖范围仍略有差别。\n\n自检：S1近亮腿向前、近臂向后；S2近亮腿向后、近臂向前，髋部遮挡方向有变化。S1前靴翘尖与鞋长可能漂移；S2前靴较平，腰扣位置从前侧漂到后侧。独审确认这些是整组未通过的硬错；不再追加修图，保留失败研究。S0可单独作为侧视概念候选，不计新完整角色。\n\n只交静态研究原稿与对照，不制作步行GIF，不宣称完整自然步行已解决，不做引擎落地。\n''')
h={str(q.relative_to(p)):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(p.rglob('*')) if q.is_file() and q.name!='SHA256.json'}
(p/'SHA256.json').write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n')
