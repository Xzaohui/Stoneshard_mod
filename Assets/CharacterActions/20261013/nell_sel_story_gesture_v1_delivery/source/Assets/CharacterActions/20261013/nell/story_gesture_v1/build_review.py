from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,numpy as np
from scipy.ndimage import label
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font=lambda n:ImageFont.truetype(F,n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
configs={'nell':('妮尔','NPC-N-NELL',['raw_01_ledger_boundary_v2.png','raw_02_limited_account_v2.png'],['静态锚点','护住闭簿','限定自述','回到锚点'],['N3-R-testimony；N3-S03-L01','N3-R-testimony-L01；N3-R-collective-L01；X06'], '不公开姓名住址；不焚页；保护不等于免责。'), 'sel':('塞尔','NPC-N-SEL',['raw_01_bargain_offer_v2.png','raw_02_cost_acknowledgement.png'],['静态锚点','空手邀谈','面对成本','回到锚点'],['N4-DEFAULT；N4-R-shift','N4-R-installments-L01；N4-R-liquidate-L01'], '不默认签票、停炉、售产或清债；腰钳不用于攻击。')}
for k,(name,cid,raws,titles,loc,boundary) in configs.items():
 p=R/f'Assets/CharacterActions/20261013/{k}/story_gesture_v1';(p/'frames').mkdir(exist_ok=True)
 anchor=R/f'Assets/CharacterDesigns/20261013/expressive/{k}/{k}_v2_raw_imagegen.png'
 src=[anchor,p/raws[0],p/raws[1],anchor];frames=[];records=[]
 for i,s in enumerate(src):
  im=Image.open(s).convert('RGBA');a=np.array(im); labs,n=label(a[:,:,3]>=128,np.ones((3,3))); sizes=np.bincount(labs.ravel());sizes[0]=0; mask=labs==sizes.argmax();a[~mask,3]=0;clean=Image.fromarray(a);box=clean.getbbox();clean.save(p/'frames'/f'clean_{i:02d}_source.png')
  padded=Image.new('RGBA',(1120,1410));padded.alpha_composite(clean,(0,0));scaled=padded.resize((448,564),Image.Resampling.NEAREST);b=scaled.getbbox();dx=16;dy=560-b[3]
  out=Image.new('RGBA',(480,600));out.alpha_composite(scaled,(dx,dy));out.save(p/'frames'/f'frame_{i:02d}.png');frames.append(out)
  records.append({'stage':i,'label':titles[i],'source':str(s.relative_to(R)),'source_sha256':sha(s),'source_body_bbox':box,'scale_common':[0.4,0.4],'resampling':'NEAREST','translation':[dx,dy],'body_rgb_unchanged_before_common_resize':True,'cleaning':'keep largest 8-connected alpha>=128 component; clear alpha elsewhere only','newly_generated':i in [1,2]})
 for theme,bg,fg in [('light',(237,229,211),(37,35,33)),('dark',(35,42,49),(241,232,214))]:
  board=Image.new('RGB',(1920,760),bg);d=ImageDraw.Draw(board);d.text((26,18),f'{name}｜主线基础动作 · 关键姿态评审（{cid}）',font=font(30),fill=fg)
  d.text((26,62),'2 张新增姿态 + 首末复用锚点｜四阶段演示，不是连续插帧或游戏精灵',font=font(21),fill=fg)
  for i,im in enumerate(frames):
   board.paste(im,(i*480,105),im);d.text((i*480+30,690),f'{i+1:02d} {titles[i]}',font=font(23),fill=fg)
  d.text((26,727),boundary,font=font(19),fill=fg);board.save(p/f'{k}_story_gesture_review_zh_{theme}.png')
 gif=[]
 for i,im in enumerate(frames):
  page=Image.new('RGB',(480,680),(237,229,211));page.paste(im,(0,35),im);d=ImageDraw.Draw(page);d.text((20,10),f'{name} · {i+1}/4 · {titles[i]}',font=font(22),fill=(37,35,33));d.text((20,639),'关键姿态演示 / 非运行验收',font=font(20),fill=(37,35,33));gif.append(page)
 gif[0].save(p/f'{k}_story_gesture_preview_once.gif',save_all=True,append_images=gif[1:],duration=[900,1200,1400,900],disposal=2,optimize=False)
 sources=[R/'design/04_人物/台本新增人物与知识边界.md',R/'design/05_主线/台本/台本_N3_听审前的灯.md',R/'design/05_主线/台本/台本_N4_第一张空白债票.md',R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements.json']
 manifest={'canonical_id':cid,'name':name,'status':'author_candidate_awaiting_independent_review','new_characters':0,'new_unique_poses':2,'stages':4,'generator':'builtin image_gen__imagegen','runtime_integrated':False,'story_locators':loc,'story_boundary':boundary,'sources':[{'path':str(s.relative_to(R)),'sha256':sha(s)} for s in sources],'frames':records,'prompt_files':[{'path':s.name,'sha256':sha(s)} for s in p.glob('prompt*.txt')],'raw_files':[{'path':s.name,'sha256':sha(s)} for s in p.glob('raw*.png')],'not_selected_raws':[s.name for s in p.glob('raw*.png') if s.name not in raws],'processing':'alpha-only background residue cleanup; a single common nearest resize for all stages; whole-canvas ground translation; no body construction, warp, individual scaling or in-between generation','gif':{'frames':4,'loop_extension':False,'duration_ms':[900,1200,1400,900]},'author_visual_notes':['已实看锚与所有raw。','保留生成模型自然微差，未逐帧拉伸。妮尔两姿已按锚点重生成恢复头身比；塞尔腰钳轮廓随新姿态有轻微像素差。','首末同锚仅表示演示起落，不提交任何任务结果。']}
 (p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (p/'README.md').write_text(f'# {name}：主线基础动作 v1\n\n原创 {cid}，0 新人。仅补两张有表情的全身关键姿态，四阶段采用锚点→姿态一→姿态二→锚点。GIF单次播放，不是连续游戏动作。\n\n{boundary}\n\n故事定位：'+ '；'.join(loc)+'。所有路线仍按原台本条件使用。\n\n深浅双底板用于检查轮廓及残留，透明PNG位于frames。raw与完整提示词均保留，manifest记录来源SHA。仅内置生图造身体；脚本只做alpha清理、共同nearest严格等比缩放（全图补透明边至1120×1410，再统一0.4倍）、接地平移及排板。未逐帧拉伸。\n\n作者候选，等待独立审查。未打最终包、上传、改roster、runtime、安装或git。\n')
 print(k,[(r['source_body_bbox'][3]-r['source_body_bbox'][1]) for r in records])
