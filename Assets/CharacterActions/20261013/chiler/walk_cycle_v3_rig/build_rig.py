from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,math,json,hashlib
base=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler');p=base/'walk_cycle_v3_rig';prev=base/'walk_cycle_v2'
# Stable identity already manually separated in v2; no generated face regeneration.
upper=Image.open(prev/'layers/identity_upper_master.png').convert('RGBA');upper.save(p/'layers/identity_upper_master.png')
# Shared boot appearance extracted non-destructively from generated K0; reconstructed leg segments use its palette.
src=Image.open(prev/'frames/K0_A_contact.png').convert('RGBA');box=(830,1230,1070,1390);boot=src.crop(box);mask=Image.new('L',boot.size);ImageDraw.Draw(mask).polygon([(18,15),(134,15),(144,82),(230,82),(230,155),(10,155),(10,70)],fill=255);a=np.array(boot);a[:,:,3]=np.minimum(a[:,:,3],np.array(mask));a[a[:,:,3]==0]=0;boot=Image.fromarray(a);boot.save(p/'layers/boot_master_A.png');mask.save(p/'masks/boot_source_extract_mask.png');boot_anchor=(82,80)
# These straight segment masters are original pixel reconstruction from source colors,
# not supposed recovered hidden image layers. Consistent 100/120px joint spacing.
masters={}
for typ,L,width in [('thigh',100,96),('shin',120,88)]:
 im=Image.new('RGBA',(128,L+56));d=ImageDraw.Draw(im);x0=64-width//2;x1=64+width//2;y1=L+48;edge=(43,31,31,255);dark=(65,45,43,255);mid=(96,67,61,255);light=(111,79,66,255)
 d.polygon([(x0+8,0),(x1-8,0),(x1,16),(x1,L+32),(x1-16,y1),(x0+16,y1),(x0,L+32),(x0,16)],fill=edge)
 d.polygon([(x0+16,8),(x1-16,8),(x1-8,24),(x1-8,L+24),(x1-24,L+40),(x0+16,L+40),(x0+8,L+24),(x0+8,24)],fill=mid)
 d.rectangle((x0+8,24,x0+24,L+24),fill=dark);d.rectangle((x0+24,16,x0+48,47),fill=light);d.rectangle((x0+40,48,x1-8,71),fill=(87,60,55,255));d.rectangle((x0+24,88,x0+47,L+20),fill=light)
 im.save(p/'layers'/f'{typ}_master.png');masters[typ]=im

def rigid(im,anchor,pos,angle,shade=1):
 th=math.radians(angle);c=math.cos(th);s=math.sin(th);ax,ay=anchor;gx,gy=pos;coeff=(c,s,ax-c*gx-s*gy,-s,c,ay+s*gx-c*gy);out=im.transform((1536,1536),Image.Transform.AFFINE,coeff,resample=Image.Resampling.NEAREST)
 out=out.resize((192,192),Image.Resampling.NEAREST).resize((1536,1536),Image.Resampling.NEAREST);a=np.array(out)
 if shade!=1:a[:,:,:3]=(a[:,:,:3].astype(float)*shade).clip(0,255).astype('uint8')
 a[a[:,:,3]==0]=0;return Image.fromarray(a)

def boot_extent(angle):
 im=rigid(boot,boot_anchor,(768,768),angle);a=np.array(im);ys,xs=np.where(a[:,:,3]>128);return int(ys.max())-768

def ik(hip,ankle):
 hx,hy=hip;ax,ay=ankle;dx=ax-hx;dy=ay-hy;dist=math.hypot(dx,dy);L1,L2=100,120
 if not(abs(L1-L2)<dist<=L1+L2):raise ValueError(('unreachable',hip,ankle,dist))
 q=(L1*L1-L2*L2+dist*dist)/(2*dist);h=math.sqrt(max(0,L1*L1-q*q));cx=hx+dx*q/dist;cy=hy+dy*q/dist;choices=[(cx-dy*h/dist,cy+dx*h/dist),(cx+dy*h/dist,cy-dx*h/dist)];return max(choices,key=lambda v:v[0])

# Explicit ankle x, boot rotation, sole target for each image-side leg, and upper bob.
configs=[('K0',0,{'A':(906,0,1380),'B':(620,30,1370)}),('K1',-20,{'A':(790,0,1380),'B':(780,-15,1340)}),('K2',-12,{'A':(712,0,1380),'B':(875,-10,1350)})]
meta=[]
for fid,bob,legs in configs:
 canvas=Image.new('RGBA',(1536,1536));pts={};debug=Image.new('RGBA',(1536,1536));dr=ImageDraw.Draw(debug)
 for role in ['B','A']:
  x,angle,sole=legs[role];ext=boot_extent(angle);ankle=(x,sole-ext);hip=(800 if role=='A' else 740,1125+bob);knee=ik(hip,ankle);shade=1 if role=='A' else .87;leglayer=Image.new('RGBA',(1536,1536));poses=[]
  for typ,start,end in [('thigh',hip,knee),('shin',knee,ankle)]:
   deg=math.degrees(math.atan2(end[1]-start[1],end[0]-start[0]))-90;part=rigid(masters[typ],(64,24),start,deg,shade);leglayer=Image.alpha_composite(leglayer,part);part.save(p/'layers'/f'{fid}_{role}_{typ}.png');poses.append({'segment':typ,'start':list(start),'end':list(end),'length':math.dist(start,end),'rotation_deg':deg})
  # Pixel knee cover removes double outline where the fixed segments overlap.
  patch=Image.new('RGBA',(1536,1536));pd=ImageDraw.Draw(patch);kx,ky=knee;pd.ellipse((kx-31,ky-29,kx+31,ky+29),fill=(int(96*shade),int(67*shade),int(61*shade),255));pd.rectangle((kx-16,ky-16,kx+8,ky+7),fill=(int(111*shade),int(79*shade),int(66*shade),255));patch=patch.resize((192,192),Image.Resampling.NEAREST).resize((1536,1536),Image.Resampling.NEAREST);pa=np.array(patch);la=np.array(leglayer);pa[:,:,3]=np.minimum(pa[:,:,3],la[:,:,3]);pa[pa[:,:,3]==0]=0;patch=Image.fromarray(pa);leglayer=Image.alpha_composite(leglayer,patch);patch.save(p/'layers'/f'{fid}_{role}_knee_cover.png')
  foot=rigid(boot,boot_anchor,ankle,angle,shade);leglayer=Image.alpha_composite(leglayer,foot);foot.save(p/'layers'/f'{fid}_{role}_boot.png');leglayer.save(p/'layers'/f'{fid}_{role}_leg.png');canvas=Image.alpha_composite(canvas,leglayer)
  pts[role]={'hip':list(hip),'knee':list(knee),'ankle':list(ankle),'boot_angle_deg':angle,'sole_target_y':sole,'boot_master':'layers/boot_master_A.png','segments':poses,'shade':shade};col=(85,180,240) if role=='A' else(240,165,75);dr.line([hip,knee,ankle],fill=col,width=5)
  for xx,yy in [hip,knee,ankle]:dr.ellipse((xx-8,yy-8,xx+8,yy+8),fill=col)
 u=Image.new('RGBA',(1536,1536));u.alpha_composite(upper,(0,bob));canvas=Image.alpha_composite(canvas,u);a=np.array(canvas);a[a[:,:,3]==0]=0;canvas=Image.fromarray(a);canvas.save(p/'frames'/f'{fid}.png');check=Image.alpha_composite(canvas,debug);check.save(p/'debug'/f'{fid}_joint_overlay.png');meta.append({'id':fid,'upper_bob':[0,bob],'legs':pts,'path':f'frames/{fid}.png','sha256':hashlib.sha256((p/'frames'/f'{fid}.png').read_bytes()).hexdigest()})
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';h=ImageFont.truetype(font,32);f=ImageFont.truetype(font,23);s=ImageFont.truetype(font,21);sheet=Image.new('RGB',(1536,750),(35,39,43));d=ImageDraw.Draw(sheet);d.text((30,16),'齐勒 · 固定腿段与靴形半步研究',font=h,fill=(244,230,194));d.text((30,62),'相同100 / 120px腿段与同一靴形 / 原创像素关节重构',font=s,fill=(163,183,188));seq=[]
for i,(fid,bob,_) in enumerate(configs):
 im=Image.open(p/'frames'/f'{fid}.png');c=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(c,(i*512,112),c);d.line((i*512,572,i*512+511,572),fill=(57,105,115));d.text((i*512+24,607),['K0：前足接触 / 后足蹬离','K1：中段支撑 / 摆过','K2：晚支撑 / 前摆待落'][i],font=f,fill=(240,231,212));bg=Image.new('RGBA',im.size,(35,39,43,255));bg.alpha_composite(im);seq.append(bg.convert('RGB').resize((768,768),Image.Resampling.NEAREST))
d.text((30,664),'头脸身份不重绘；上身起伏0 / -20 / -12px，几何稳定不等于动作美感通过。',font=s,fill=(205,210,212));d.text((30,699),'当前只半步，待实看关节、遮挡和脚点后再补交替半步；不是原生动画或换装系统。',font=s,fill=(145,165,173));sheet.save(p/'chiler_rig_halfstep_review_zh.png');seq[0].save(p/'chiler_rig_halfstep_once.gif',save_all=True,append_images=seq[1:],duration=[200,200,600]);(p/'manifest.json').write_text(json.dumps({'method':'original fixed-segment pixel reconstruction using source colors and one extracted boot; not imagegen new per-frame body','canvas':[1536,1536],'segment_lengths':[100,120],'grid':8,'identity_source':'../walk_cycle_v2/layers/identity_upper_master.png','boot_source':'../walk_cycle_v2/frames/K0_A_contact.png','boot_source_rect':list(box),'boot_local_anchor':list(boot_anchor),'frames':meta,'runtime_verified':False,'complete_cycle':False,'status':'author_visual_review_pending'},ensure_ascii=False,indent=2))
