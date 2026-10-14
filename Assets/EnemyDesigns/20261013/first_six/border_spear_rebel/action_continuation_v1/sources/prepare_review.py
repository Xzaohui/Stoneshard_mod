from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
root=Path(__file__).resolve().parents[5]
brief=json.loads((root/'Assets/EnemyDesigns/20261013/first_six/action_continuation_brief_v1.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
for r in brief['items'][:2]:
 o=root/r['planned_generation']['output_directory_if_later_executed'];role=r['role'];pose=r['proposed_keypose']['pose_id']
 for raw in sorted(o.glob('*_raw_v*.png')):
  v=raw.stem.rsplit('_',1)[1];im=Image.open(raw).convert('RGBA');a=np.asarray(im).copy();original=a.copy();clear=a[:,:,3]<=8;hidden=a[:,:,3]==0;a[clear]=0;clean=Image.fromarray(a);p=o/f'{role}_{pose}_transparent_candidate_{v}.png';clean.save(p)
  qa={'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':list(im.size),'mode':'RGBA','alpha_cleanup':'RGBA set 0 only where original alpha <= 8; RGB and alpha at alpha > 8 byte-exact unchanged','cleared_alpha_1_to_8':int(((original[:,:,3]>0)&clear).sum()),'hidden_rgb_pixel_count':int(((original[:,:,:3]!=0).any(2)&hidden).sum()),'visible_pixels_unchanged':bool(np.array_equal(a[~clear],original[~clear])),'bbox_alpha_gt8':list(clean.getbbox()),'edge_alpha_max':[int(a[0,:,3].max()),int(a[-1,:,3].max()),int(a[:,0,3].max()),int(a[:,-1,3].max())]};(o/f'alpha_QA_{v}.json').write_text(json.dumps(qa,indent=2))
  for tag,bg in [('light','#e6dfd0'),('dark','#23272e')]:
   canvas=Image.new('RGBA',im.size,bg);canvas.alpha_composite(clean);canvas.convert('RGB').save(o/f'review_{v}_{tag}.png')
  refs=[root/x['path'] for x in r['planned_generation']['reference_order'][:2]]
  if r['id']=='001':stages=[refs[1],refs[0],p];labels=['旧选稿：架矛戒备（原图未变）','旧选稿：短促前刺（原图未变）','新候选：短刺后收矛 '+v]
  else:stages=[refs[0],p,refs[1]];labels=['旧选稿：紧凑备击（原图未变）','新候选：短棍下挥中段 '+v,'旧选稿：收势回防（原图未变）']
  scale=.5;imgs=[Image.open(x).convert('RGBA') for x in stages];cellw=max(round(i.width*scale) for i in imgs)+30;cellh=max(round(i.height*scale) for i in imgs)+60;board=Image.new('RGB',(3*cellw,2*cellh+90),'#f3eee6');draw=ImageDraw.Draw(board);draw.text((24,15),f'{r["id"]} {r["working_name"]}｜相邻阶段候选对照（非已验证连续动画）',fill='#1e252d',font=font)
  for row,bg in enumerate(['#e6dfd0','#23272e']):
   for k,(im,label) in enumerate(zip(imgs,labels)):
    x=k*cellw;y=80+row*cellh;draw.rectangle((x,y,x+cellw,y+cellh),fill=bg);thumb=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);tmp=Image.new('RGBA',(cellw,cellh),bg);tmp.alpha_composite(thumb,((cellw-thumb.width)//2,45));board.paste(tmp.convert('RGB'),(x,y));draw.text((x+12,y+9),label,fill=('#1e252d' if row==0 else '#eee6d8'),font=font)
  board.save(o/f'adjacent_review_{v}.png');print(r['id'],v,qa)
