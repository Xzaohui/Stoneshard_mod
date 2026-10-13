from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,sys
import numpy as np
from scipy.ndimage import label
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
B=R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements.json'
cfg={'sena':('塞娜·里德','NPC-SENA',['01_archive_boundary','02_cede_explanation'],['静态锚点','限定查阅','让出解释位置','回到锚点'],'闭册闭袋；不替莉德授权、不开放整库、不宣告成长免责。'),'kaem':('凯姆','MAE-NPC-KAEM',['01_defensive_argument','02_yield_the_floor'],['静态锚点','小幅辩解','放低空手听完','回到锚点'],'闭筒不交接；不增印章、不重新授印、不把沉默当认罪。')}
for k in sys.argv[1:] or ['sena','kaem']:
 name,cid,keys,titles,boundary=cfg[k];p=R/f'Assets/CharacterActions/20261013/{k}/story_gesture_v1';(p/'frames').mkdir(exist_ok=True)
 brief=next(c for c in json.loads(B.read_text())['characters'] if c['canonical_id']==cid)
 anchor=R/brief['current_anchor']['path'];assert H(anchor)==brief['current_anchor']['sha256']
 sources=[anchor,p/f'raw_{keys[0]}.png',p/f'raw_{keys[1]}.png',anchor];frames=[];records=[]
 for i,s in enumerate(sources):
  im=Image.open(s).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>=128,np.ones((3,3)));counts=np.bincount(labs.ravel());counts[0]=0;mask=labs==counts.argmax();a[~mask]=0;a[a[:,:,3]==0]=0
  clean=Image.fromarray(a);bb=clean.getbbox();clean.save(p/'frames'/f'clean_{i:02d}_source.png')
  padded=Image.new('RGBA',(1120,1410));padded.alpha_composite(clean,(0,0));scaled=padded.resize((448,564),Image.Resampling.NEAREST);box=scaled.getbbox();dx=16;dy=560-box[3]
  frame=Image.new('RGBA',(480,600));frame.alpha_composite(scaled,(dx,dy));frame.save(p/'frames'/f'frame_{i:02d}.png');frames.append(frame)
  records.append({'stage':i,'label':titles[i],'source':str(s.relative_to(R)),'source_sha256':H(s),'source_size':im.size,'source_body_bbox':bb,'scale_common':[0.4,0.4],'translation':[dx,dy],'resampling':'NEAREST','newly_generated':i in [1,2]})
 for theme,bg,fg in [('light',(237,229,211),(37,35,33)),('dark',(35,42,49),(241,232,214))]:
  board=Image.new('RGB',(1920,760),bg);d=ImageDraw.Draw(board);d.text((26,18),f'{name}｜主线基础动作 · 关键姿态评审（{cid}）',font=F(30),fill=fg)
  d.text((26,62),'2 张新增姿态 + 首末复用锚点｜四阶段演示，不是连续插帧或游戏精灵',font=F(21),fill=fg)
  for i,im in enumerate(frames):board.paste(im,(i*480,105),im);d.text((i*480+28,690),f'{i+1:02d} {titles[i]}',font=F(23),fill=fg)
  d.text((26,727),boundary,font=F(19),fill=fg);board.save(p/f'{k}_story_gesture_review_zh_{theme}.png')
 gif=[]
 for i,im in enumerate(frames):
  page=Image.new('RGB',(480,680),(237,229,211));page.paste(im,(0,35),im);d=ImageDraw.Draw(page);d.text((20,10),f'{name} · {i+1}/4 · {titles[i]}',font=F(21),fill=(37,35,33));d.text((20,639),'关键姿态演示 / 非运行验收',font=F(20),fill=(37,35,33));gif.append(page)
 gif[0].save(p/f'{k}_story_gesture_preview_once.gif',save_all=True,append_images=gif[1:],duration=[900,1200,1400,900],disposal=2,optimize=False)
 paths=[B]+[R/s['path'] for s in brief['source_cards']]+[R/s['path'] for s in brief['related_main_scripts']]
 manifest={'canonical_id':cid,'name':name,'status':'author_candidate_awaiting_independent_review','new_characters':0,'new_unique_poses':2,'stages':4,'generator':'builtin image_gen__imagegen','runtime_integrated':False,'brief':brief,'sources':[{'path':str(s.relative_to(R)),'sha256':H(s)} for s in paths],'frames':records,'prompt_files':[{'path':s.name,'sha256':H(s)} for s in p.glob('prompt*.txt')],'raw_files':[{'path':s.name,'sha256':H(s)} for s in p.glob('raw*.png')],'processing':'Keep largest alpha>=128 8-connected body component; clear outside RGBA, clear hidden RGB when alpha=0. Pad without stretch to 1120x1410, common 0.4 nearest isotropic resize, ground translation, boards and GIF only. No body construction, per-pose resizing, warp or interpolation.','gif':{'frames':4,'loop_extension':False,'duration_ms':[900,1200,1400,900]}}
 (p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (p/'README.md').write_text(f'# {name}：主线基础动作 v1\n\n{cid}，0 新人。两张新全身姿态，锚点→姿态一→姿态二→锚点，共四阶段。单次GIF仅演示，不是连续游戏动作。\n\n{boundary}\n\n透明逐帧、中文深浅板、完整提示词、raw和来源SHA均保留。身体由内置imagegen生成；脚本仅透明清理、共同nearest等比缩放、接地平移和排板。\n\n作者候选，等待独立审查。未改roster、运行包、安装或git。\n')
 print(k,[(r['source_body_bbox'][3]-r['source_body_bbox'][1]) for r in records])
