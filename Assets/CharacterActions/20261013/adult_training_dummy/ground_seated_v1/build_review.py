from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=np.array(Image.open(D/'raw/G1_ground_seated.png').convert('RGBA'))
low=(a[:,:,3]>0)&(a[:,:,3]<=8);n=int(low.sum());a[a[:,:,3]<=8]=0;a[a[:,:,3]==0,:3]=0
im=Image.fromarray(a);im.save(D/'frames/G1_ground_seated.png')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=lambda n:ImageFont.truetype(font,n)
trans=[]
# All complete figures use one scalar per whole image. No limb, face or axis edits.
# I0 hood span x629..907 (~278); G1 hood x457..697 (~240), observed manually.
panels=[('I0 原身份锚','sources/I0_stand.png',(35,170),.48),('G1 新绘 · 屈膝地坐','frames/G1_ground_seated.png',(350,260),.48*278/240),('R2 坐凳 · 旧图','sources/R2_seated.png',(850,210),.36),('K1 单膝 · 旧图','sources/K1_single_knee_rest_alpha.png',(1200,240),.36),('R1 侧卧 · 旧图','sources/R1_reclined_rest.png',(1535,320),.30)]
for theme,bg,fg in [('light',(236,234,225),(34,37,41)),('dark',(34,38,44),(239,236,223))]:
 b=Image.new('RGB',(2050,1360),bg);dr=ImageDraw.Draw(b)
 dr.text((35,20),'成人训练样板 · G1 空手屈膝地坐 / 单张静态概念',font=f(34),fill=fg)
 dr.text((35,78),'新增静态1候选 · 原I0直接派生 · 对照旧图不计新 · 无GIF / 无新人物 / 非游戏运行验证',font=f(23),fill=fg)
 for label,src,xy,s in panels:
  q=Image.open(D/src).convert('RGBA');box=q.getbbox();c=q.crop(box);v=c.resize((round(c.width*s),round(c.height*s)),Image.Resampling.NEAREST);b.paste(v,xy,v);dr.text((xy[0],135),label,font=f(22),fill=fg)
  trans.append({'theme':theme,'source':src,'crop':box,'scale':s,'position':xy,'resample':'NEAREST'})
 dr.text((35,735),'I0 / G1 按近似兜帽宽度全图等比显示；其余旧图缩略对照支撑类型，不用坐姿总高拟合站姿。',font=f(22),fill=fg)
 crops=[('G1 原尺寸头帽 / 脸',(430,405,715,725),(35,830),1),('G1 臀地支撑 / 双膝—双靴',(395,775,1000,1140),(390,830),1),('G1 原图整体（0.55× nearest）',im.getbbox(),(1110,810),.55)]
 for title,box,xy,s in crops:
  c=im.crop(box);v=c.resize((round(c.width*s),round(c.height*s)),Image.Resampling.NEAREST);b.paste(v,xy,v);dr.text((xy[0],xy[1]-40),title,font=f(21),fill=fg)
 dr.text((35,1300),'保留raw与来源证据；仅清除极低透明噪点及排版。姿态/身份/支撑是否通过以独立QA为准。',font=f(23),fill=fg)
 b.save(D/f'ground_seated_review_{theme}_zh.png')
log={'generation_calls':1,'generated_pose_candidates':1,'body_pixel_editing':False,'raw_preserved':True,'alpha_cleanup':{'rule':'Set RGBA=0 where alpha<=8; clear hidden RGB where alpha=0; all remaining RGBA unchanged','nonzero_alpha_removed_count':n,'original_size':im.size,'clean_bbox':im.getbbox()},'layout_transforms':trans,'head_comparison':'manual approximate hood width I0 278px, G1 240px; whole image uniform scale only; no standing-height fit','detail_crops':crops,'raw_sha256':sha(D/'raw/G1_ground_seated.png'),'output_sha256':sha(D/'frames/G1_ground_seated.png')}
(D/'processing_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(json.dumps(log,ensure_ascii=False,indent=2))
