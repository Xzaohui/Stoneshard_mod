from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil,zipfile
P=Path(__file__).parent; S=935/761
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda s:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',s)
# Only a rigid prop is drawn procedurally. Body pixels all originate in imagegen.
prop=Image.new('RGBA',(232,112));d=ImageDraw.Draw(prop)
d.polygon([(24,0),(192,0),(216,16),(232,40),(232,88),(208,112),(16,112),(0,88),(0,32)],fill='#46352d')
d.polygon([(24,8),(192,8),(208,24),(224,40),(224,88),(200,104),(24,104),(8,88),(8,32)],fill='#c3ad88')
d.polygon([(24,16),(88,16),(104,24),(152,16),(192,16),(208,32),(200,40),(168,48),(120,80),(80,88),(24,72),(16,40)],fill='#dfcfae')
d.polygon([(16,72),(72,88),(112,88),(168,56),(208,32),(216,40),(176,64),(128,96),(80,104),(24,96)],fill='#ab9474')
d.polygon([(32,24),(64,32),(80,32),(80,40),(56,40),(32,32)],fill='#b49b78')
d.line([(208,48),(192,72),(176,88),(152,104)],fill='#e5d6b5',width=8)
prop.save(P/'layers/parcel_fixed_source.png')
polys={
'O0_hold': [[(462,736),(482,715),(504,714),(508,703),(533,702),(544,713),(544,731),(531,738),(538,746),(560,746),(577,755),(576,771),(556,784),(511,788),(462,777)],[(629,765),(651,751),(675,748),(673,740),(659,732),(664,720),(687,714),(711,727),(735,730),(753,744),(754,776),(725,788),(661,794),(632,782)]],
'O1_offer': [[(695,713),(710,692),(737,685),(763,693),(804,685),(819,677),(832,672),(846,679),(851,691),(845,700),(832,705),(836,715),(852,721),(865,722),(873,735),(859,753),(813,762),(759,751),(706,751)],[(934,740),(949,725),(974,715),(980,710),(968,703),(970,690),(989,684),(1005,686),(1015,700),(1034,705),(1042,720),(1038,740),(1017,756),(975,764),(943,755)]]}
frames=[];records=[]
for key,pos in [('O0_hold',(496,666)),('O1_offer',(808,630))]:
 raw=Image.open(P/'raw'/f'{key}.png').convert('RGBA');a=np.array(raw);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0;flat=Image.fromarray(a)
 mask=Image.new('L',raw.size);md=ImageDraw.Draw(mask)
 for poly in polys[key]:md.polygon(poly,fill=255)
 # Extract brown glove and near-black outline only, not beige parcel or blue sleeves.
 aa=np.array(flat);rgb=aa[:,:,:3].astype(float);select=((rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)&(rgb[:,:,0]<180))|(rgb.max(2)<66)
 maska=np.array(mask);keep=(maska>0)&select&(aa[:,:,3]>0);hands=np.zeros_like(aa);hands[keep]=aa[keep];hands=Image.fromarray(hands)
 obj=Image.new('RGBA',raw.size);obj.alpha_composite(prop,pos)
 # source_flat remains a truthful flattened source, including hidden generated parcel.
 comp=flat.copy();comp.alpha_composite(obj);comp.alpha_composite(hands)
 dy=1380-round(flat.getbbox()[3]*S)
 def transform(im):
  sc=im.resize(tuple(round(v*S) for v in raw.size),Image.Resampling.NEAREST);out=Image.new('RGBA',(1536,1536));out.alpha_composite(sc,(0,dy));return out
 for label,im in [('source_flat',flat),('parcel',obj),('hands_foreground',hands)]:transform(im).save(P/'layers'/f'{key}_{label}.png')
 can=transform(comp);can.save(P/'frames'/f'{key}.png');frames.append(can)
 records.append({'id':key,'new_body_pose':True,'raw_sha256':sha(P/'raw'/f'{key}.png'),'source_size':raw.size,'scale':S,'translation':[0,dy],'parcel_translation_in_source':pos,'frame_sha256':sha(P/'frames'/f'{key}.png'),'bbox':can.getbbox()})
shutil.copy2(P/'frames/O0_hold.png',P/'frames/O2_retract_reuse_O0.png');frames.append(frames[0].copy())
seq=[]
for im in frames:
 th=im.resize((768,768),Image.Resampling.NEAREST);bg=Image.new('RGB',th.size,'#2c3038');bg.paste(th,mask=th);seq.append(bg)
seq[0].save(P/'item_offer_once.gif',save_all=True,append_images=seq[1:],duration=[900,1200,1000],disposal=2,optimize=False)
review=Image.new('RGB',(1600,1200),'#efeee8');d=ImageDraw.Draw(review)
d.text((24,20),'双手递包｜胸腹稳持 → 前递仍持 → 收回',font=F(34),fill='#222831')
d.text((24,76),'2个新身体姿态，3个逻辑阶段；末帧复用首帧。无人接走，不代表交付或任务完成。',font=F(23),fill='#555b62')
for i,(im,label) in enumerate(zip(frames,['O0 胸腹稳持（新绘）','O1 双臂前递（新绘）','O2 收回稳持（复用O0）'])):
 th=im.resize((460,460),Image.Resampling.NEAREST);x=35+i*520;review.paste(th,(x,100),th);d.line((x,514,x+460,514),fill='#b4b6b7');d.text((x,555),label,font=F(24),fill='#30363d')
for i,(im,box) in enumerate(zip(frames[:2],[(530,770,980,1000),(805,730,1300,990)])):
 crop=im.crop(box).resize((int((box[2]-box[0])*1.35),int((box[3]-box[1])*1.35)),Image.Resampling.NEAREST);review.paste(crop,(70+i*760,660),crop)
 d.text((40+i*780,610),['稳持：拇指与包面、掌根与包底','前递：双肩—肘—腕连贯，仍未松手'][i],font=F(24),fill='#30363d')
d.text((24,1040),'同一232×112源像素布包，仅平移；独立物件层＋原手前景。共同人物倍率935/761。',font=F(24),fill='#555b62')
d.text((24,1088),'身体底层保留原合成小包，固定包覆盖其上；属于遮挡合成概念，不是干净原生部件。',font=F(23),fill='#555b62')
d.text((24,1136),'三阶段单次GIF仅示意节奏；收回反用首姿态，连续运动、足轨迹和游戏运行未验。',font=F(23),fill='#555b62');review.save(P/'item_offer_review_zh.png')
m={'status':'awaiting_independent_review','classification':'sparse_item_offer_compositing_concept','new_body_poses':2,'phase_count':3,'reuse':{'O2':'O0 byte identical'},'canvas':[1536,1536],'common_scale':S,'parcel_source_size':[232,112],'parcel_source_sha256':sha(P/'layers/parcel_fixed_source.png'),'layers':'Flattened imagegen source (with occluded generated parcel) + translated fixed parcel + extracted original glove foreground. Not clean native body/part assets.','frames':records,'gif_durations_ms':[900,1200,1000],'gif_loop_extension':False,'runtime_verified':False,'native_ready':False,'equipment_compatibility_verified':False,'limits':['动作仅两关键姿态；反向复用不是新绘收回过程','原生层未拆，身体底层含被覆盖原包','衣褶和手套轮廓有生成漂移','没有接收人，布包始终在双手中，无交付/完成/奖励语义'],'source_reference':{'path':'../interaction_v1/raw/I0_stand.png','sha256':sha(P.parent/'interaction_v1/raw/I0_stand.png')}}
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(P/'README.md').write_text('# 双手递包概念\n\n新增2个身体姿态，3阶段；O2字节复用O0。所有身体像素来自builtin imagegen，脚本仅透明清理、统一尺度、固定小包层、原手前景提取与排版。身体底层保留被覆盖的原包，不是干净原生拆层。小包源尺寸232×112，所有阶段固定；无人接收、不产生剧情交付。独审前不称通过。\n')
h={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name not in ['SHA256.json','item_offer_review_package.zip']};(P/'SHA256.json').write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(P/'item_offer_review_package.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(P.rglob('*')):
  if p.is_file() and p.suffix!='.zip':z.write(p,str(p.relative_to(P)))
print(json.dumps({k:v for k,v in h.items() if k in ['manifest.json','item_offer_review_zh.png','item_offer_once.gif']},indent=2))
