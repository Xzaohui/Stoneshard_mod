from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
B=D.parent
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
items=[
('001','叛军','边地长矛手','border_spear_rebel','border_spear_rebel_transparent.png','直立窄矛 · 警惕'),
('002','强盗','旧渠劫道者','canal_club_brigand','canal_club_brigand_transparent.png','矮壮短棍 · 戒备'),
('003','僵尸','渠墓腐尸','canal_tomb_restless','canal_tomb_restless_idle_transparent.png','斜曲腐化 · 保留皮肉'),
('004','幽灵','墓龛游魂','crypt_drifter_wraith','crypt_drifter_wraith_idle_transparent.png','碎袍烟尾 · 无实体靴'),
('005','吸血鬼','饥血潜行体','blood_hunger_mutant','blood_hunger_mutant_idle_transparent.png','低宽长臂 · 肉体异化'),
('006','邪教','债契仪式看守','debt_ritual_warden','debt_ritual_warden_idle_transparent.png','窄钟形袍 · 活人看守'),
]
info=[]
for mode,bg,fg,line in [('light','#f3eddf','#332f29','#d4c9b7'),('dark','#252a2d','#ede8da','#4b5154')]:
 out=Image.new('RGBA',(2400,2000),bg)
 dr=ImageDraw.Draw(out)
 dr.text((65,28),'六类敌人 · 首轮静态概念',font=ImageFont.truetype(font,48),fill=fg)
 dr.text((65,94),'原创外观候选｜美术分组不是原版六大阵营｜单帧概念，未接入游戏',font=ImageFont.truetype(font,28),fill=fg)
 for n,(cid,cat,name,slug,file,note) in enumerate(items):
  x=40+(n%3)*790;y=160+(n//3)*890
  dr.rectangle((x,y,x+760,y+862),outline=line,width=2)
  dr.text((x+24,y+18),cid+' '+cat+'｜'+name,font=ImageFont.truetype(font,30),fill=fg)
  p=B/slug/'idle_v1'/file
  im=Image.open(p).convert('RGBA');bbox=im.getbbox();crop=im.crop(bbox)
  scale=min(696/crop.width,735/crop.height)
  dims=(round(crop.width*scale),round(crop.height*scale))
  out.alpha_composite(crop.resize(dims,Image.Resampling.NEAREST),(x+(760-dims[0])//2,y+66+(735-dims[1])//2))
  dr.text((x+24,y+817),note,font=ImageFont.truetype(font,26),fill=fg)
  if mode=='light':info.append({'concept_id':cid,'category':cat,'name':name,'path':str(p.relative_to(B)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_size':im.size,'alpha_bbox':bbox,'board_display_size':dims,'resize':'proportional nearest-neighbor'})
 dr.text((65,1950),'仅讨论可逆外观；未新增剧情结局、敌对身份或战斗机制。',font=ImageFont.truetype(font,25),fill=fg)
 out.convert('RGB').save(D/('enemy_first_six_overview_'+mode+'_zh.png'))
(D/'overview_inputs.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
