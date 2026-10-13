from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,math,hashlib,zipfile
p=Path(__file__).resolve().parent;sz=(1536,1536);k=1478/1254
sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def save(im,q):clean(im).save(q)
def norm(im,dy):
 im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);out=Image.new('RGBA',sz);out.alpha_composite(im,(28,dy));return clean(out)
r=clean(Image.open(p/'raw/staff.png'));box=r.getbbox();r=r.crop(box);staff=r.resize((1000,round(r.height*1000/r.width)),Image.Resampling.NEAREST);save(staff,p/'layers/canonical_wood_staff.png');sy=(staff.height-1)/2
conf=[('T0','准备','T0',[(528,746),(867,762)],[(483,708,570,780),(824,729,899,790)]),('T1','后收蓄力','T1_fix2',[(409,727),(748,733)],[(354,691,443,758),(714,700,805,765)]),('T2','向前短刺','T2',[(698,684),(1037,678)],[(653,649,740,716),(999,641,1096,714)])]
frames=[];checks=[]
for id,phase,raw,g,rects in conf:
 im=clean(Image.open(p/'raw'/f'{raw}.png'));b=im.getbbox();dy=1380-im.resize((1478,1478),Image.Resampling.NEAREST).getbbox()[3];body=norm(im,dy)
 points=[(28+x*k,y*k+dy) for x,y in g];a,bp=points;angle=math.atan2(bp[1]-a[1],bp[0]-a[0]);c=math.cos(angle);s=math.sin(angle)
 # Fixed two grip positions 350 and 750 on a single rigid staff. Minor generated fist drift stays within their drawn grasp area.
 grip2=(a[0]+400*c,a[1]+400*s)
 prop=staff.transform(sz,Image.Transform.AFFINE,(c,s,350-c*a[0]-s*a[1],-s,c,sy+s*a[0]-c*a[1]),resample=Image.Resampling.NEAREST)
 layers={'body_base':body,'staff_rigid':prop};masks=[]
 for tag,rect in zip(['rear','front'],rects):
  m=Image.new('L',im.size);ImageDraw.Draw(m).rectangle(rect,fill=255);ma=norm(Image.merge('RGBA',(m,m,m,m)),dy).getchannel('A');ma.save(p/'masks'/f'{id}_{tag}_fingers_mask.png');fg=Image.new('RGBA',sz);fg.paste(body,(0,0),ma);layers[tag+'_fingers_foreground']=fg;masks.append(f'masks/{id}_{tag}_fingers_mask.png')
 final=Image.new('RGBA',sz);paths={}
 for name,layer in layers.items():
  dest=f'layers/{id}_{name}.png';save(layer,p/dest);paths[name]=dest;final=Image.alpha_composite(final,layer)
 save(final,p/'frames'/f'{id}.png');re=Image.new('RGBA',sz)
 for q in paths.values():re=Image.alpha_composite(re,Image.open(p/q))
 checks.append(dict(id=id,pixel_exact_recomposition=bool(np.array_equal(np.array(clean(re)),np.array(Image.open(p/'frames'/f'{id}.png')))),canvas=list(sz),body_bbox=body.getbbox(),complete_staff_bbox=prop.getbbox(),axis_perpendicular_error_px=[0,0],rigid_grip_separation_px=400,front_grip_vs_generated_center_px=math.dist(grip2,bp)))
 frames.append(dict(id=id,phase=phase,source=f'raw/{raw}.png',translation=[28,dy],shared_body_scale=k,root=[768,1380],grips={'rear':a,'front':grip2},staff_angle_degrees=math.degrees(angle),staff_scale=1,body_bbox=body.getbbox(),layers=paths,masks=masks,support='两靴支撑；短刺前膝弯曲、后腿延展。足底轮廓生成漂移未作物理校验'))
# byte-identical recovery
(p/'frames/T3.png').write_bytes((p/'frames/T0.png').read_bytes());frames.append(dict(id='T3',phase='回稳（复用准备）',reuses='T0',layers=frames[0]['layers'],masks=frames[0]['masks'],grips=frames[0]['grips']))
manifest=dict(classification='Mod原创双手长棍关键姿态 / grip compatibility study',canvas=sz,canonical_reference='../interaction_v1/frames/I0_stand.png',canonical_body_height_px=935,raw_ready_height_px=793,shared_scale=k,normalization='所有身体同一1478/1254最近邻倍率（整画布取1478，使准备身高精确935px）；仅平移到共用脚底，不逐帧bbox缩放',unique_final_body_poses=3,generated_raw_count=6,new_equipment_sources=1,discarded_body_variants=['raw/T1.png','raw/T1_fix.png'],discard_reason='初稿握距太窄；第一次修正握距过宽，均未用于成片。',staff_length_px=1000,staff_width_px=staff.height,staff_local_grips=[[350,sy],[750,sy]],staff_source_crop=box,staff_source='raw/staff.png',canonical_staff_sha256=sha(p/'layers/canonical_wood_staff.png'),layer_order=['body_base','staff_rigid','rear_fingers_foreground','front_fingers_foreground'],reference_evidence='ReferenceAudit/20261013/actions/REFERENCE_AUDIT.md：官方长柄动态图未取得，未证实具体关节帧。此为原创，不是游戏长柄技能实现。',frames=frames,engine_origin=None,native_fps=None,collision=None,runtime_verified=False,equipment_compatibility_verified=False,independent_review='pending')
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'recomposition_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
prov=[]
for f in (p/'raw').glob('*.png'):
 ref=None if f.stem=='staff' else '../interaction_v1/frames/I0_stand.png' if f.stem=='T0' else 'raw/T0.png' if f.stem in ['T1','T2'] else 'raw/T1.png'
 prov.append(dict(file=str(f.relative_to(p)),sha256=sha(f),prompt=f'prompts/{f.stem}.txt',reference=ref,reference_sha256=sha(p/ref) if ref else None,method='built-in image_gen'))
(p/'generation_provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,24);h=ImageFont.truetype(font,34)
board=Image.new('RGB',(1800,1180),(36,40,44));d=ImageDraw.Draw(board);d.text((24,20),'双手长棍 · 原创关键姿态与握点检视',font=h,fill='white');d.text((24,72),'准备 → 后收蓄力 → 向前短刺 → 回稳；同一1000px木棍，固定400px双握距。',font=f,fill=(209,211,203))
ims=[]
for n,fr in enumerate(frames):
 im=Image.open(p/'frames'/f"{fr['id']}.png");thumb=im.resize((450,450),Image.Resampling.NEAREST);board.paste(thumb,(n*450,120),thumb);d.text((n*450+20,578),fr['id']+' '+fr['phase'],font=f,fill=(239,218,173))
 body=Image.open(p/fr['layers']['body_base']);crop=body.crop((360,620,1320,1040)).resize((430,188),Image.Resampling.NEAREST);board.paste(crop,(n*450+10,635),crop)
 grips=fr['grips'];a=grips['rear'];b=grips['front'];crop=im.crop((int(a[0])-90,int(min(a[1],b[1]))-90,int(b[0])+90,int(max(a[1],b[1]))+90));crop.thumbnail((430,175),Image.Resampling.NEAREST);board.paste(crop,(n*450+10,865),crop)
 bg=Image.new('RGB',(768,768),(36,40,44));small=im.resize((768,768),Image.Resampling.NEAREST);bg.paste(small,(0,0),small);ims.append(bg)
d.text((24,1060),'中排：关闭装备核对完整肩肘腕。下排：两处握持遮挡。回稳与准备字节一致。',font=f,fill=(204,211,213));d.text((24,1105),'概念关键姿态，非原版技能或原生动画；未接runtime，未验换装/连续补间/判定。',font=f,fill=(204,211,213));board.save(p/'twohand_staff_review_zh.png')
ims[0].save(p/'twohand_staff_preview_once.gif',save_all=True,append_images=ims[1:],duration=[650,750,850,1400],disposal=2)
# Scale comparison with existing canonical, no scaling independently.
comparison=Image.new('RGB',(1536,850),(36,40,44));cd=ImageDraw.Draw(comparison)
for i,(q,label) in enumerate([(p.parent/'interaction_v1/frames/I0_stand.png','统一站立基准'),(p/'layers/T0_body_base.png','双手准备：同尺度')]):
 im=Image.open(q).resize((768,768),Image.Resampling.NEAREST);comparison.paste(im,(i*768,0),im);cd.text((i*768+150,780),label,font=h,fill='white')
comparison.save(p/'cross_action_scale_review.png');print(json.dumps(checks,indent=2))
