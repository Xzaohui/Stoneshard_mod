from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,sys,numpy as np
from scipy.ndimage import label
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
for k in sys.argv[1:]:
 p=R/f'Assets/CharacterActions/20261013/{k}/story_gesture_v1';b=json.loads((p/'brief_snapshot.json').read_text());anchor=R/b['current_anchor']['path'];assert H(anchor)==b['current_anchor']['sha256'];(p/'frames').mkdir(exist_ok=True)
 sources=[anchor,p/'raw_01.png',p/'raw_02.png'];titles=['独立静态参考','低头检查闭匣接缝','放低闭匣侧头听核验'] if k=='leo' else ['独立静态参考（无纸）','低头核本人抄写段','收纸近身要求说完'];fs=[];recs=[]
 for i,s in enumerate(sources):
  im=Image.open(s).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>=128,np.ones((3,3)));counts=np.bincount(labs.ravel());counts[0]=0;mask=labs==counts.argmax();removed=int(np.count_nonzero((a[:,:,3]>0)&~mask));a[~mask]=0;a[a[:,:,3]==0]=0;clean=Image.fromarray(a);bb=clean.getbbox();clean.save(p/'frames'/f'clean_{i:02d}_source.png')
  pad=Image.new('RGBA',(1120,1410));pad.alpha_composite(clean);small=pad.resize((448,564),Image.Resampling.NEAREST);dy=560-small.getbbox()[3];f=Image.new('RGBA',(480,600));f.alpha_composite(small,(16,dy));f.save(p/'frames'/f'frame_{i:02d}.png');fs.append(f);recs.append({'stage':i,'title':titles[i],'source':str(s.relative_to(R)),'sha256':H(s),'source_size':im.size,'body_bbox':bb,'removed_alpha_pixels':removed,'common_scale':[0.4,0.4],'translation':[16,dy],'resampling':'NEAREST','new_pose':i>0})
 seq=[0,1,2,0] if k=='leo' else [1,2,1];name=b['name'];boundary='始终闭匣、不递交、不认证封印；动作不等于接管、签约或结盟。' if k=='leo' else '纸外侧空白，不公开姓名地址；未制作取纸过程，原无纸锚不进入动作序列。'
 for theme,bg,fg in [('light',(237,229,211),(37,35,33)),('dark',(35,42,49),(241,232,214))]:
  board=Image.new('RGB',(1920,780),bg);d=ImageDraw.Draw(board);d.text((26,18),f'{name}｜主线关键姿态评审 · {b["canonical_id"]}',font=F(30),fill=fg);d.text((26,62),'2 张新姿态 / 0 新人 / 概念设定，非连续插帧或运行资源',font=F(21),fill=fg)
  slots=[0,1,2,0] if k=='leo' else [0,1,2,1]
  for j,i in enumerate(slots):
   board.paste(fs[i],(j*480,110),fs[i]);d.text((j*480+20,700),titles[i] if j<3 else ('末帧复用锚' if k=='leo' else '末帧复用新姿一'),font=F(22),fill=fg)
  d.text((26,741),boundary,font=F(21),fill=fg);board.save(p/f'{k}_story_gesture_review_zh_{theme}.png')
 gif=[]
 for j,i in enumerate(seq):
  page=Image.new('RGB',(480,710),(237,229,211));page.paste(fs[i],(0,45),fs[i]);d=ImageDraw.Draw(page);d.text((16,10),f'{name} · {j+1}/{len(seq)}',font=F(24),fill=(37,35,33));d.text((16,647),titles[i],font=F(22),fill=(37,35,33));d.text((16,682),'稀疏关键姿态 / 非完整取物动作',font=F(19),fill=(37,35,33));gif.append(page)
 durations=[950,1350,1500,950] if k=='leo' else [1350,1500,950];gif[0].save(p/f'{k}_story_gesture_preview_once.gif',save_all=True,append_images=gif[1:],duration=durations,disposal=2,optimize=False)
 m={'canonical_id':b['canonical_id'],'status':'author_candidate_awaiting_independent_review','new_characters':0,'new_unique_poses':2,'generator':'builtin image_gen__imagegen','runtime_integrated':False,'brief':b,'source_hashes':json.loads((p/'source_hashes.json').read_text()),'frames':recs,'animation_sequence':seq,'gif':{'frames':len(seq),'loop_extension':False,'duration_ms':durations},'paper_acquisition_drawn':False if k=='lyd' else None,'processing':'Largest alpha>=128 8-connected body only; clear exterior RGBA and hidden RGB. Pad to 1120x1410; common 0.4 nearest-neighbor isotropic scaling, grounding translation only. No drawing, anatomy construction, stretch, warp or tween.','boundaries':boundary,'prompts':[{'file':s.name,'sha256':H(s)} for s in sorted(p.glob('prompt_*.txt'))],'raw':[{'file':s.name,'sha256':H(s)} for s in sorted(p.glob('raw_*.png'))]};(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
 (p/'README.md').write_text(f'# {name}：主线关键姿态\n\n2张新增全身图，0新人。{boundary}\n\n'+('GIF：原锚→新姿一→新姿二→原锚。' if k=='leo' else '原锚独立参考；GIF：新姿一→新姿二→新姿一。没有取纸第三姿，不能当完整取纸动作。')+'\n\n内置imagegen生成人体；脚本仅透明安全清理、共同等比nearest缩放、接地平移、中文双底排板与单次GIF。保留raw、prompt和来源SHA。未修改roster或游戏内容；待独审。\n')
 import shutil;shutil.copyfile(__file__,p/'build_review.py')
 print(k,[(x['body_bbox'],x['removed_alpha_pixels']) for x in recs])
