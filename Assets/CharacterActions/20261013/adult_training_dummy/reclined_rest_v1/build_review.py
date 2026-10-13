from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=np.array(Image.open(D/'raw/R1_reclined_rest_raw.png').convert('RGBA'))
low=(a[:,:,3]>0)&(a[:,:,3]<=8); n=int(low.sum());a[a[:,:,3]<=8]=0;a[a[:,:,3]==0,:3]=0
im=Image.fromarray(a);im.save(D/'frames/R1_reclined_rest.png')
bbox=im.getbbox(); ref=Image.open(D/'sources/I0_stand.png').convert('RGBA')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(n):return ImageFont.truetype(font,n)
trans=[]
for theme,bg,fg in [('light',(236,234,225),(34,37,41)),('dark',(34,38,44),(239,236,223))]:
 b=Image.new('RGB',(1900,1350),bg);dr=ImageDraw.Draw(b)
 dr.text((36,20),'成人训练样板 · R1 清醒侧卧短歇 / 单张静态研究',font=f(33),fill=fg)
 dr.text((36,74),'新增候选1张 · 原I0仅身份对照 · 无新人物 / 无GIF / 非引擎验证',font=f(23),fill=fg)
 rc=ref.crop(ref.getbbox()); rs=0.64; rv=rc.resize((round(rc.width*rs),round(rc.height*rs)),Image.Resampling.NEAREST)
 b.paste(rv,(40,170),rv);dr.text((36,125),'I0 原身份锚',font=f(23),fill=fg)
 # Hood horizontal span manual landmarks: I0 x629..907=278, R1 x168..510=342.
 # Use one scalar across ALL of R1. Never resize face or limbs separately.
 ns=rs*278/342; nc=im.crop(bbox);nv=nc.resize((round(nc.width*ns),round(nc.height*ns)),Image.Resampling.NEAREST)
 b.paste(nv,(520,280),nv);dr.text((520,150),'R1 候选 · 按近似同兜帽宽度等比对照（无身体拉伸）',font=f(23),fill=fg)
 dr.text((520,700),'原图局部复核：头—前臂支撑 / 交错腿靴（远靴仅小段）',font=f(23),fill=fg)
 dr.text((520,750),'遮挡限制：不证明双腿双靴完整可追踪，也不锁定鞋形或骨长。',font=f(21),fill=fg)
 crops=[('头颈与支撑',(70,165,860,780),(35,840),0.7),('髋腿与双靴',(970,420,1665,785),(760,840),0.98)]
 for title,box,xy,s in crops:
  c=im.crop(box);v=c.resize((round(c.width*s),round(c.height*s)),Image.Resampling.NEAREST);b.paste(v,xy,v);dr.text((xy[0],xy[1]-38),title,font=f(22),fill=fg)
 dr.text((36,1295),'保留raw与全部证据。独审结论见QA；未通过不计补缺。仅透明清理与全图等比nearest排版。',font=f(22),fill=fg)
 b.save(D/f'reclined_rest_review_{theme}_zh.png')
 trans.append({'board':theme,'I0_crop':list(ref.getbbox()),'I0_scale':rs,'R1_crop':list(bbox),'R1_scale':ns,'resample':'NEAREST','head_match':'approximate hood width I0 278px vs R1 342px','detail_crops':crops})
log={'generation_calls':1,'generated_pose_candidates':1,'body_pixel_editing':False,'raw_preserved':True,'alpha_cleanup':{'rule':'RGBA=0 wherever alpha<=8; clear RGB at alpha0; all remaining RGBA unchanged','nonzero_alpha_removed_count':n,'original_size':list(im.size),'clean_bbox':list(bbox)},'layout_transforms':trans,'source_sha256':sha(D/'sources/I0_stand.png'),'raw_sha256':sha(D/'raw/R1_reclined_rest_raw.png'),'output_sha256':sha(D/'frames/R1_reclined_rest.png')}
(D/'processing_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(json.dumps(log,ensure_ascii=False,indent=2))
