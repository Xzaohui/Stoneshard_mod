from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,zipfile
P=Path(__file__).parent; S=935/761; C=(1536,1536)
for x in ['frames','layers']: (P/x).mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def font(n):return ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
# Original geometric prop, drawn on 8px grid then nearest-neighbour. Fixed layer all frames.
st=Image.new('RGBA',(192,192));d=ImageDraw.Draw(st)
def poly(p,c):d.polygon(p,fill=c)
outline='#382b24';mid='#76503a';light='#a17a50';dark='#553b2b'
# Three visible fixed legs; far fourth is hidden by the seat/figure.
poly([(73,137),(78,139),(75,169),(70,169)],outline);poly([(74,141),(76,141),(73,167),(72,167)],mid)
poly([(95,135),(100,136),(104,166),(99,166)],outline);poly([(97,139),(99,139),(102,164),(100,164)],mid)
poly([(84,141),(90,141),(90,172),(84,172)],outline);poly([(86,144),(88,144),(88,170),(86,170)],light)
poly([(74,156),(100,154),(101,158),(74,160)],dark)
# Seat geometry: top must meet the seated butt around (640,1120).
poly([(68,135),(89,130),(104,136),(83,143)],outline)
poly([(69,135),(89,131),(102,136),(83,141)],light)
poly([(69,136),(83,142),(103,137),(103,141),(83,146),(69,140)],outline)
poly([(70,137),(83,143),(83,145),(70,139)],mid)
poly([(84,143),(102,138),(102,140),(84,145)],dark)
d.line([(76,134),(90,139)],fill=mid,width=1);d.line([(84,132),(98,137)],fill=mid,width=1)
st=st.resize(C,Image.Resampling.NEAREST);st.save(P/'layers/stool_fixed.png')
# Latest canonical standing sprite copied without rescale; same new-frame S for both generated images.
stand=Image.open(P.parent/'interaction_v1/frames/I0_stand.png').convert('RGBA'); out=Image.new('RGBA',C);out.alpha_composite(stand,(55,0));stand=out
bodies=[stand];records=[{'id':'R0_stand','source':'../interaction_v1/frames/I0_stand.png','translation':[55,0],'scale':1,'new':False}]
for key,dx in [('R1_lower',0),('R2_seated',-55)]:
 raw=Image.open(P/'raw'/f'{key}.png').convert('RGBA');a=np.array(raw);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a).resize((round(raw.width*S),round(raw.height*S)),Image.Resampling.NEAREST)
 dy=1380-im.getbbox()[3];c=Image.new('RGBA',C);c.alpha_composite(im,(dx,dy));bodies.append(c)
 records.append({'id':key,'source':f'raw/{key}.png','translation':[dx,dy],'scale':S,'new':True,'raw_size':list(raw.size),'raw_sha256':sha(P/'raw'/f'{key}.png')})
seq=[0,1,2,1,0];names=['R0_stand','R1_lower','R2_seated','R3_rise_reuse_R1','R4_stand_reuse_R0'];frames=[]
for i,j in enumerate(seq):
 bodies[j].save(P/'layers'/f'{names[i]}_body_flat.png');c=st.copy();c.alpha_composite(bodies[j]);c.save(P/'frames'/f'{names[i]}.png');frames.append(c)
for i,r in enumerate(records):r.update({'body_bbox':bodies[i].getbbox(),'ground_y':1380,'weapon':None,'head_height_estimate_px':[328,327,329][i]})
review=Image.new('RGB',(1920,1210),'#e9e6dc');d=ImageDraw.Draw(review);d.text((28,18),'坐下 → 休息 → 起身｜原创关键姿态提案',font=font(38),fill='#252a31');d.text((28,74),'新增2张身体图 + 复用I0站姿；起身复用屈膝姿态。不是完整补间动画或运行资产。',font=font(25),fill='#43454b')
labels=['R0 凳前站立','R1 后移屈膝','R2 坐稳承重','R3 起身（复用R1）','R4 回站（复用R0）']
for i,im in enumerate(frames):
 x=i*384;t=im.resize((384,384),Image.Resampling.NEAREST);review.paste(t,(x,135),t);d.line((x,480,x+383,480),fill='#9b9c92');d.text((x+14,535),labels[i],font=font(21),fill='#252a31')
# Same-scale seating contact details, plus cross-group comparison.
for i,j in enumerate([1,2]):
 crop=frames[j].crop((480,990,1080,1410));review.paste(crop,(30+i*640,610),crop);d.text((30+i*640,1050),['屈膝接近座面（稀疏姿态）','坐稳：臀部压座面、双足落地'][i],font=font(25),fill='#252a31')
for i,im in enumerate([Image.open(P.parent/'interaction_v1/frames/I0_stand.png').convert('RGBA'),bodies[2]]):
 t=im.resize((300,300),Image.Resampling.NEAREST);review.paste(t,(1290+i*300,640),t)
d.text((1310,1050),'I0 / R2 同一尺度，头高约328px',font=font(23),fill='#252a31');d.text((28,1140),'固定1536²画布与木凳层｜人物和凳分层｜预览单次播放｜原稿保留｜无武器/无剧情身份',font=font(26),fill='#43454b');review.save(P/'rest_transition_review_zh.png')
prev=[]
for im in frames:
 t=im.resize((768,768),Image.Resampling.NEAREST);c=Image.new('RGB',(768,768),'#292c31');c.paste(t,(0,0),t);prev.append(c)
prev[0].save(P/'rest_transition_once.gif',save_all=True,append_images=prev[1:],duration=[600,500,1100,500,800],disposal=2,optimize=False)
m={'status':'awaiting_independent_review','classification':'original_mod_keypose_proposal','unique_new_body_images':2,'unique_body_poses_including_reused_I0':3,'phase_count':5,'canvas':list(C),'preview_only':True,'loop_extension':False,'sequence':names,'scale_policy':'R0 copied latest canonical I0 with translation only; both new raw 1254 square frames share 935/761 nearest factor, no per-frame bbox fitting','canonical_body_height':935,'stool_layer':'layers/stool_fixed.png','stool_sha256':sha(P/'layers/stool_fixed.png'),'stool_geometry':{'seat_top_polygon':[[544,1080],[712,1040],[832,1088],[664,1144]],'front_leg_bottom_y':1376,'same_every_frame':True},'ground_y':1380,'layers_note':'Flat character layers and original fixed geometric stool; not native skeletal layers','source_evidence':'No verified original sitting or getting-up joint animation. Original mod proposal.','engine_origin':None,'collision':None,'native_fps':None,'native_directions':None,'frames':records,'known_limits':['Sparse poses with repositioning feet, not a continuous joint animation.','Getting up reuses lowering pose, not separately drawn.','Boot contour and perspective vary between generated poses; no planted-foot lock claim.']}
(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
