from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label
import numpy as np,json,hashlib,shutil,sys
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
bp=R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements_03.json';brief=json.loads(bp.read_text())
for k in sys.argv[1:]:
 b=next(x for x in brief['characters'] if x['canonical_id']==('NPC09' if k=='oda' else 'NPC11'));p=R/f'Assets/CharacterActions/20261013/{k}/story_gesture_v1';(p/'frames').mkdir(exist_ok=True)
 sources=[R/b['current_anchor']['path']]+list(sorted(p.glob('raw_*.png')))
 hashes=[]
 for x in [b['current_anchor']]+b['sources']+b['scripts']:
  a=H(R/x['path']);assert a==x['sha256'];hashes.append({'path':x['path'],'sha256':a})
 hashes.append({'path':str(bp.relative_to(R)),'sha256':H(bp)})
 (p/'source_hashes.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2));(p/'brief_snapshot.json').write_text(json.dumps(b,ensure_ascii=False,indent=2))
 titles=['原锚 · 静态参考','垂眼检查原腰绳','停下检查 · 看向请求者'] if k=='oda' else ['原锚 · 空手站姿','收臂戒备 · 重新估量']
 seq=[0,1,2,0] if k=='oda' else [0,1,0];count=len(sources)-1;records=[];frames=[]
 for i,s in enumerate(sources):
  im=Image.open(s).convert('RGBA');a=np.array(im);labs,n=label(a[:,:,3]>=128,np.ones((3,3)));counts=np.bincount(labs.ravel());counts[0]=0;mask=labs==counts.argmax();removed=int(np.count_nonzero((a[:,:,3]>0)&~mask));a[~mask]=0;a[a[:,:,3]==0]=0;clean=Image.fromarray(a);bb=clean.getbbox();clean.save(p/'frames'/f'clean_{i:02d}_source.png')
  pad=Image.new('RGBA',(1120,1410));pad.alpha_composite(clean);small=pad.resize((448,564),Image.Resampling.NEAREST);dy=560-small.getbbox()[3];fr=Image.new('RGBA',(480,600));fr.alpha_composite(small,(16,dy));fr.save(p/'frames'/f'frame_{i:02d}.png');frames.append(fr)
  records.append({'stage':i,'title':titles[i],'source':str(s.relative_to(R)),'sha256':H(s),'source_size':list(im.size),'body_bbox':bb,'removed_alpha_pixels':removed,'common_scale':[0.4,0.4],'translation':[16,dy],'resampling':'NEAREST','new_pose':i>0})
 boundary='腰绳始终收纳闭合、未开船；不代表N8到场或运输约已成立。' if k=='oda' else '始终空手、肩包闭合；仅trace条件反应，不表明交割或结案。'
 name=b['name'];w=480*len(seq)
 for theme,bg,fg in [('light',(237,229,211),(37,35,33)),('dark',(35,42,49),(241,232,214))]:
  board=Image.new('RGB',(w,790),bg);d=ImageDraw.Draw(board);d.text((26,18),f'{name}｜主线关键姿态评审 · {b["canonical_id"]}',font=F(30),fill=fg);d.text((26,62),f'{count} 张新姿态 / 0 新人 / 概念设定，非连续动画或运行资源',font=F(21),fill=fg)
  for j,i in enumerate(seq):
   board.paste(frames[i],(j*480,110),frames[i]);d.text((j*480+20,706),'末帧复用原锚' if j==len(seq)-1 else titles[i],font=F(22),fill=fg)
  d.text((26,750),boundary,font=F(20),fill=fg);board.save(p/f'{k}_story_gesture_review_zh_{theme}.png')
 gif=[]
 for j,i in enumerate(seq):
  page=Image.new('RGB',(480,710),(237,229,211));page.paste(frames[i],(0,45),frames[i]);d=ImageDraw.Draw(page);d.text((16,10),f'{name} · {j+1}/{len(seq)}',font=F(24),fill=(37,35,33));d.text((16,647),'末帧复用原锚' if j==len(seq)-1 else titles[i],font=F(22),fill=(37,35,33));d.text((16,682),'稀疏关键姿态 / 非连续动画',font=F(19),fill=(37,35,33));gif.append(page)
 durations=[950,1350,1500,950] if k=='oda' else [950,1700,950];gp=p/f'{k}_story_gesture_preview_once.gif';gif[0].save(gp,save_all=True,append_images=gif[1:],duration=durations,disposal=2,optimize=False);gi=Image.open(gp);assert gi.n_frames==len(seq) and 'loop' not in gi.info
 m={'canonical_id':b['canonical_id'],'status':'author_candidate_awaiting_independent_review','new_characters':0,'new_unique_poses':count,'generator':'builtin image_gen__imagegen','runtime_integrated':False,'brief':b,'source_hashes':hashes,'frames':records,'animation_sequence':seq,'gif':{'frames':len(seq),'loop_extension':False,'duration_ms':durations},'processing':'Largest alpha>=128 8-connected body only; clear exterior RGBA and hidden RGB. Pad to 1120x1410; common 0.4 nearest-neighbor isotropic scaling, grounding translation only. No drawing, anatomy construction, stretch, warp or tween.','boundaries':boundary,'prompts':[{'file':s.name,'sha256':H(s)} for s in sorted(p.glob('prompt_*.txt'))],'raw':[{'file':s.name,'sha256':H(s)} for s in sorted(p.glob('raw_*.png'))]}
 (p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
 (p/'README.md').write_text(f'# {name}：主线关键姿态\n\n{count}张新增全身图，0新人。{boundary}\n\n'+('GIF：原锚→新姿一→新姿二→原锚。' if k=='oda' else 'GIF：原锚→唯一新姿→原锚。三阶段仅一张新增，复用不计新增。')+'\n\n内置imagegen生成人体；脚本仅透明安全清理、共同等比nearest缩放、接地平移、中文双底排板与单次GIF。保留raw、prompt和来源SHA。未修改roster或游戏内容；待独审。\n')
 provenance={'generator':'builtin image_gen__imagegen','transparent_background':True,'outputs':[{'file':'raw_01.png','original_saved_path':'/workspace/scratch/5ed8df2c5d81/generated_images/'+('exec-5f26961a-97ad-4a8b-8dcf-342783abc60c.png' if k=='oda' else 'exec-4b6527f1-6d60-40db-a216-0cd413589b78.png'),'references':[b['current_anchor']],'prompt':'prompt_01.txt'}]}
 if k=='oda':provenance['outputs'].append({'file':'raw_02.png','original_saved_path':'/workspace/scratch/5ed8df2c5d81/generated_images/exec-9210347a-5a2a-4dfc-9180-174d095f9dfe.png','references':[{'path':str((p/'raw_01.png').relative_to(R)),'sha256':H(p/'raw_01.png')},b['current_anchor']],'prompt':'prompt_02.txt'})
 (p/'generation_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2));shutil.copyfile(__file__,p/'build_review.py');print(k,records)
