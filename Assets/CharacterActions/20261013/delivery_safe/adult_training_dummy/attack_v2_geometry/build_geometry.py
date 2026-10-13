from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,json,hashlib
from scipy import ndimage
import numpy as np
root=Path('Stoneshard_mod/Assets/CharacterActions/20261013/adult_training_dummy');p=root/'attack_v2_geometry';src=root/'attack_v1'
# One original pixel reconstruction from D0 style. The hidden full handle is new artwork,
# not recovered source pixels. Unchanging local blade base(64,140), tip(64,460).
sw=Image.new('RGBA',(128,488));d=ImageDraw.Draw(sw);dark=(61,38,29,255);mid=(155,100,53,255);base=(185,130,72,255);hi=(216,159,93,255)
d.rectangle((45,30,83,52),fill=dark);d.rectangle((53,36,75,46),fill=base)
d.rectangle((48,48,80,124),fill=dark);d.rectangle((56,48,72,124),fill=mid)
for y in range(54,119,16):d.rectangle((56,y,72,y+6),fill=(114,72,42,255))
d.polygon([(12,116),(116,116),(116,143),(96,143),(96,449),(81,460),(47,460),(32,449),(32,143),(12,143)],fill=dark)
d.rectangle((20,124,108,135),fill=base);d.rectangle((27,124,100,128),fill=hi)
d.rectangle((40,143,88,442),fill=base);d.rectangle((40,143,52,442),fill=hi);d.rectangle((76,143,88,444),fill=mid);d.rectangle((48,443,80,452),fill=base)
# blade endpoints use outside outline from y140 to460, projected320px
sw.save(p/'layers/canonical_wood_sword.png')
configs=[
('D0_guard',(982,1030),45,[(923,993),(961,977),(1002,992),(1025,1027),(1022,1059),(1000,1081),(967,1070),(944,1045)],[(988,1080),(1030,1021),(1076,1020),(1086,1080),(1300,1298),(1300,1349),(1245,1349),(1020,1125),(980,1130)]),
('D1_windup',(1144,589),-132,[(1030,626),(1065,605),(1075,562),(1104,534),(1142,530),(1175,550),(1190,578),(1200,611),(1165,639),(1142,645),(1135,675),(1105,718),(1060,710)],[(828,253),(887,257),(1124,493),(1165,481),(1180,521),(1130,567),(1221,618),(1221,670),(1165,670),(1080,590),(1045,594),(1038,557),(1077,518),(828,315)]),
('D2_forward',(1062,985),22,[(970,850),(1030,866),(1060,900),(1115,946),(1120,974),(1110,1009),(1060,1025),(999,1005),(976,955)],[(1108,940),(1152,927),(1170,970),(1508,1124),(1508,1192),(1450,1192),(1148,1060),(1100,1068),(1098,1018)]),
('D3_recovery',(948,1026),45,[(903,989),(930,980),(965,998),(989,1021),(989,1051),(969,1075),(933,1067),(911,1045)],[(962,1082),(1003,1025),(1047,1024),(1053,1081),(1248,1282),(1248,1340),(1195,1340),(992,1120),(954,1124)])]
meta=[]
for name,grip,deg,handpoly,erasepoly in configs:
 im=Image.open(src/'frames'/f'{name}.png').convert('RGBA');handmask=Image.new('L',im.size);ImageDraw.Draw(handmask).polygon(handpoly,fill=255);erasemask=Image.new('L',im.size);ImageDraw.Draw(erasemask).polygon(erasepoly,fill=255);erasemask=Image.fromarray(ndimage.maximum_filter(np.array(erasemask),size=41,mode="constant"))
 # Never erase a protected glove-front pixel.
 import numpy as np
 em=np.array(erasemask);hm=np.array(handmask);em[hm>0]=0;erasemask=Image.fromarray(em);arr=np.array(im);arr[:,:,3][em>0]=0;from scipy import ndimage
 labels,n=ndimage.label(arr[:,:,3]>0);sizes=np.bincount(labels.ravel());sizes[0]=0;arr[:,:,3][labels!=sizes.argmax()]=0;baseim=Image.fromarray(arr);baseim.save(p/'layers'/f'{name}_body_base.png')
 hand=Image.new('RGBA',im.size);hand.paste(im,(0,0),handmask);hand.save(p/'layers'/f'{name}_hand_foreground.png');handmask.save(p/'masks'/f'{name}_hand_foreground_mask.png');erasemask.save(p/'masks'/f'{name}_old_weapon_removal_mask.png')
 # Render canonical sword through an inverse rigid transform; nearest, no scale/shear.
 th=math.radians(deg-90);c=math.cos(th);s=math.sin(th);gx,gy=grip;ax,ay=64,80
 # inverse maps final(x,y) into local sword coords
 coeff=(c,s,ax-c*gx-s*gy,-s,c,ay+s*gx-c*gy)
 layer=sw.transform(im.size,Image.Transform.AFFINE,coeff,resample=Image.Resampling.NEAREST);layer=layer.resize((192,192),Image.Resampling.NEAREST).resize((1536,1536),Image.Resampling.NEAREST);layer.save(p/'layers'/f'{name}_sword_rigid.png')
 out=Image.alpha_composite(baseim,layer);out=Image.alpha_composite(out,hand);out.save(p/'frames'/f'{name}.png')
 def pt(x,y):return [round(gx+c*(x-ax)-s*(y-ay),3),round(gy+s*(x-ax)+c*(y-ay),3)]
 meta.append({'id':name[:2],'grip_anchor':list(grip),'rotation_degrees_screen_axis':deg,'scale':1,'render_grid':8,'render_note':'8px nearest-neighbor contour sampling; canonical320px axis retained, raster edge differs within grid tolerance','blade_base':pt(64,140),'blade_tip':pt(64,460),'canonical_blade_length':320,'sword_layer':f'layers/{name}_sword_rigid.png','body_base':f'layers/{name}_body_base.png','foreground_hand':f'layers/{name}_hand_foreground.png','erase_mask':f'masks/{name}_old_weapon_removal_mask.png','hand_mask':f'masks/{name}_hand_foreground_mask.png'})
(p/'manifest.json').write_text(json.dumps({'asset_id':'UNNAMED_ADULT_TRAINING_MODEL_ATTACK_GEOMETRY_V2','source':'../attack_v1','logical_canvas':[1536,1536],'canonical_weapon':'layers/canonical_wood_sword.png','canonical_grip':[64,80],'canonical_blade_base':[64,140],'canonical_blade_tip':[64,460],'construction':'single original pixel reconstruction from D0 appearance; hidden handle reconstructed, not recovered source layer','layer_order':['body_base','sword_rigid','hand_foreground'],'frames':meta,'runtime_verified':False,'equipment_compatibility_verified':False,'status':'author visual QA pending'},ensure_ascii=False,indent=2))
# review no claim yet
sheet=Image.new('RGB',(2048,750),(35,39,43));dd=ImageDraw.Draw(sheet);font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';h=ImageFont.truetype(font,34);f=ImageFont.truetype(font,24);small=ImageFont.truetype(font,23);dd.text((30,16),'训练攻击 · 固定木剑几何修正',font=h,fill=(244,230,194));dd.text((30,66),'同一剑层 / 固定320px刃段 / 刚性旋转 + 逐帧握点与手掌遮挡',font=small,fill=(163,183,188))
for i,(name,*_) in enumerate(configs):
 im=Image.open(p/'frames'/f'{name}.png');c=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(c,(i*512,112),c);dd.line((i*512,572,i*512+511,572),fill=(57,105,115));dd.text((i*512+45,607),['① 预备','② 蓄势','③ 挥出','④ 回收'][i],font=f,fill=(240,231,212))
dd.text((30,665),'保留四张身体与原始研究；新剑是像素重建，不声称恢复原生装备层。',font=small,fill=(205,210,212));dd.text((30,704),'身体足轨迹与完整连续动作仍待验证；当前不是可运行的换装系统。',font=small,fill=(145,165,173));sheet.save(p/'dummy_attack_geometry_v2_review_zh.png')
