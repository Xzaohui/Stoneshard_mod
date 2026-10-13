from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,hashlib,math,zipfile
p=Path(__file__).resolve().parent;S=(1536,1536);k=935/761
sha=lambda q:hashlib.sha256(Path(q).read_bytes()).hexdigest()
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def norm(im,dy):
 im=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);out=Image.new('RGBA',S);out.alpha_composite(im,(0,dy));return clean(out)
def save(im,q):clean(im).save(p/q)
raw=clean(Image.open(p/'raw/equipment.png'));bow=raw.crop((80,0,320,1205));ImageDraw.Draw(bow).rectangle((90,1124,240,1205),fill=(0,0,0,0));bow=bow.crop(bow.getbbox());bs=920/bow.height;bow=bow.resize((round(bow.width*bs),920),Image.Resampling.NEAREST);save(bow,'layers/canonical_bow.png')
arrow=raw.crop((180,1124,1210,1225));arrow=arrow.crop(arrow.getbbox());arrow=arrow.resize((700,round(arrow.height*700/arrow.width*0.65)),Image.Resampling.NEAREST);save(arrow,'layers/canonical_arrow.png')
# Bow source local points based on visible tips and center leather grip.
bg=((270-88)*bs,(615-11)*bs);tip1=((103-88)*bs,(31-11)*bs);tip2=((103-88)*bs,(1178-11)*bs)
conf=[('A0','搭箭预备（已搭箭轻拉）','A0',(970,638),(597,645),(931,593,1005,675),(557,613,606,671)),('A1','拉弦瞄准','A1',(1025,602),(610,596),(990,561,1059,648),(568,549,619,608)),('A2','松弦随势（箭已离画）','A2',(1025,602),None,(990,561,1059,648),(415,478,515,557)),('A3','回稳（复用A0身体，无新箭）','A0',(970,638),None,(931,593,1005,675),(557,613,606,671))]
frames=[];checks=[]
for id,phase,src,grip,nock,br,dr in conf:
 body0=clean(Image.open(p/f'raw/{src}.png'));scaled=body0.resize((round(body0.width*k),round(body0.height*k)),Image.Resampling.NEAREST);dy=1380-scaled.getbbox()[3];body=norm(body0,dy)
 cv=lambda v:(v[0]*k,v[1]*k+dy)
 g=cv(grip);n=cv(nock) if nock else None;offset=(round(g[0]-bg[0]),round(g[1]-bg[1]));b=Image.new('RGBA',S);b.alpha_composite(bow,offset);ends=[(offset[0]+t[0],offset[1]+t[1]) for t in [tip1,tip2]]
 center=n if n else ((ends[0][0]+ends[1][0])/2,g[1]);string=Image.new('RGBA',S);d=ImageDraw.Draw(string);d.line([ends[0],center,ends[1]],fill=(88,67,46,255),width=6);d.line([ends[0],center,ends[1]],fill=(206,186,139,255),width=2)
 arr=Image.new('RGBA',S);angle=0
 if n:
  # Straight arrow follows nock to the shelf just above the bow hand; fixed 700px source.
  shelf=(g[0],g[1]-28);angle=math.atan2(shelf[1]-n[1],shelf[0]-n[0]);c=math.cos(angle);s=math.sin(angle);ay=(arrow.height-1)/2
  arr=arrow.transform(S,Image.Transform.AFFINE,(c,s,-c*n[0]-s*n[1],-s,c,ay+s*n[0]-c*n[1]),resample=Image.Resampling.NEAREST)
 layers={'string_state':string,'body_complete':body,'bow_rigid':b,'arrow_rigid':arr};masks=[]
 for label,rect in [('bow_hand',br),('draw_hand',dr)]:
  m=Image.new('L',body0.size);ImageDraw.Draw(m).rectangle(rect,fill=255);mask=norm(Image.merge('RGBA',(m,m,m,m)),dy).getchannel('A');mask.save(p/f'masks/{id}_{label}.png');fg=Image.new('RGBA',S);fg.paste(body,(0,0),mask);layers[label+'_foreground']=fg;masks.append(f'masks/{id}_{label}.png')
 final=Image.new('RGBA',S);paths={}
 for name,im in layers.items():
  q=f'layers/{id}_{name}.png';save(im,q);paths[name]=q;final=Image.alpha_composite(final,im)
 save(final,f'frames/{id}.png');re=Image.new('RGBA',S)
 for q in paths.values():re=Image.alpha_composite(re,Image.open(p/q))
 check=dict(id=id,pixel_exact_recomposition=bool(np.array_equal(np.array(clean(re)),np.array(Image.open(p/f'frames/{id}.png')))),body_bbox=body.getbbox(),bow_bbox=b.getbbox(),arrow_bbox=arr.getbbox(),arrow_length_px=700 if n else None,nock_string_center_error_px=0 if n else None)
 checks.append(check);frames.append(dict(id=id,phase=phase,source=f'raw/{src}.png',body_reuse='A0' if id=='A3' else None,body_scale=k,translation=[0,dy],bow_grip=g,bow_offset=offset,bow_scale=1,bow_string_endpoints=ends,string_center=center,arrow_nock=n,arrow_angle_degrees=math.degrees(angle),arrow_state='nocked' if n else 'outside_canvas_after_release; no arrow in hand',layers=paths,masks=masks,support='双靴均支撑；无滑步意图。生成的足边缘有少量像素差异。'))
manifest=dict(classification='Mod原创基础弓箭动作概念，不是原版兼容资产',canvas=S,canonical_reference='../interaction_v1/frames/I0_stand.png',canonical_body_height_px=935,normalization='全组三身体同一935/761倍率，整画布最近邻缩放，仅按脚底平移；不逐帧bbox拉伸',unique_new_body_images=3,new_equipment_sources=1,unique_pose_count=3,phase_count=4,bow_canonical_length_px=920,arrow_canonical_length_px=700,bow_source_crop=[88,11,311,1204],bow_local_grip=bg,bow_local_tips=[tip1,tip2],string_note='独立绘制三段式拉弦/两段式回弹状态；弓本体为固定轮廓概念，不模拟弓臂弹性',equipment_hand_assignment='解剖左手持弓（画面右），解剖右手拉弦（画面左），不镜像',reference_evidence='已读REFERENCE_AUDIT与KEYFRAME_BRIEF，未取得原版弓箭具体关节帧；本稿原创。',native_fps=None,engine_origin=None,collision=None,runtime_verified=False,independent_review='pending',preview_only=True,loop=False,frames=frames)
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(p/'recomposition_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
prov=json.loads((p/'generation_provenance.json').read_text());prov=[r for r in prov if r['id']!='equipment'];prov.append(dict(id='equipment',raw='raw/equipment.png',raw_sha256=sha(p/'raw/equipment.png'),prompt='prompts/equipment.txt',reference=None,method='built-in image_gen'));(p/'generation_provenance.json').write_text(json.dumps(prov,ensure_ascii=False,indent=2))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,23);h=ImageFont.truetype(font,34);board=Image.new('RGB',(2000,1280),(35,40,45));d=ImageDraw.Draw(board);d.text((28,18),'普通木弓 · 基础动作原创提案',font=h,fill='white');d.text((28,72),'同一木弓 / 同一箭长 / 独立弦状态与手遮罩；第三阶段箭已离画，回稳不补出第二箭。',font=f,fill='white');ims=[]
for i,fr in enumerate(frames):
 im=Image.open(p/f"frames/{fr['id']}.png");thumb=im.resize((500,500),Image.Resampling.NEAREST);board.paste(thumb,(i*500,110),thumb);d.text((i*500+10,620),fr['id']+' '+fr['phase'],font=f,fill=(231,214,166))
 crop=im.crop((450,530,1390,880)).resize((490,183),Image.Resampling.NEAREST);board.paste(crop,(i*500+5,685),crop)
 b=Image.open(p/fr['layers']['body_complete']);crop=b.crop((440,540,1370,920)).resize((490,200),Image.Resampling.NEAREST);board.paste(crop,(i*500+5,910),crop)
 bg2=Image.new('RGB',(768,768),(35,40,45));im2=im.resize((768,768),Image.Resampling.NEAREST);bg2.paste(im2,(0,0),im2);ims.append(bg2)
d.text((28,1150),'中排：箭尾、弦中点、持弓手与面部。下排：关闭装备后的完整肩肘腕。',font=f,fill='white');d.text((28,1200),'关键姿态讨论稿；未补连续中间帧，不代表射速、命中判定、引擎组合或换装兼容。',font=f,fill='white');board.save(p/'archery_review_zh.png');ims[0].save(p/'archery_preview_once.gif',save_all=True,append_images=ims[1:],duration=[900,1100,700,1600],disposal=2)
print(json.dumps(checks,indent=2))
