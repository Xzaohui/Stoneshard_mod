from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[5]; D=Path(__file__).resolve().parent
slug='belo'; ids=['anchor','B1','anchor']; titles=['原锚 · 体侧持箍','抬箍检查箍缘','原锚复用 · 结束示意']
anchor=R/f'Assets/CharacterDesigns/20261013/expressive/{slug}/{slug}_raw_imagegen.png'
paths=[anchor,D/'raw/B1_raw_imagegen.png',anchor]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ims=[]
for p in paths:
 i=Image.open(p).convert('RGBA');i.putalpha(i.getchannel('A').point(lambda v:0 if v<32 else v));ims.append(i.crop(i.getchannel('A').getbbox()))
scale=min(.48,570/max(i.height for i in ims),350/max(i.width for i in ims)); frames=[]
(D/'frames').mkdir(exist_ok=True)
for n,i in enumerate(ims):
 i=i.resize((round(i.width*scale),round(i.height*scale)),Image.Resampling.NEAREST)
 f=Image.new('RGBA',(410,650));f.alpha_composite(i,((410-i.width)//2,620-i.height));f.save(D/f'frames/{n:02}_{ids[n]}.png');frames.append(f)
font=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
for theme,bg,fg in [('light','#efeade','#282828'),('dark','#252a30','#efe8d6')]:
 b=Image.new('RGB',(1230,820),bg);d=ImageDraw.Draw(b);d.text((25,16),'贝洛 · 抬箍检查箍缘',font=font(29),fill=fg)
 d.text((25,60),'1 张新姿态 · 原锚首末复用 · 人物基础动作概念',font=font(19),fill=fg)
 for n,f in enumerate(frames):
  d.text((n*410+25,105),titles[n],font=font(21),fill=fg);b.paste(f,(n*410,120),f)
 d.text((25,773),'仅观察原木箍；不表示改法通过、署名解决或游戏运行。',font=font(20),fill=fg)
 b.save(D/f'belo_review_zh_{theme}.png')
# No GIF until independent continuity check resolves finger/inner-edge reading.
brief=R/'Assets/CharacterDesigns/20261013/expressive/briefs/town_work_pose_candidates_01.json'
source=R/'design/04_人物/城市人物/人物_MNS-NPC-BELO_贝洛.md'
manifest={'character_id':'MNS-NPC-BELO','name':'贝洛','status':'static_candidate_pending_independent_review','new_pose_count':1,'mode':'builtin imagegen identity-preserve','sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in [anchor,source,brief]],'sequence':ids,'gif_created':False,'gif_gate':'指腹内缘触点仍待独审确认；静态候选不冒称连续性通过。','processing':{'common_uniform_nearest_scale':scale,'alpha_cleanup':'alpha below 32 cleared; raw retained','body_synthesis':False,'nonuniform_stretch':False,'grounding':'common bottom y620'},'runtime_integrated':False,'story_boundary':['非改箍通过','非师傅原谅','非署名或工具归属解决'],'files':[{'path':str(p.relative_to(D)),'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='manifest.json']}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(D/'QA-author.json').write_text(json.dumps({'reviewed_raws':['anchor','B1'],'decision':'static_candidate_pending_independent_review','observations':['脸、发型、衣装、双足一致；环为完整刚性单环，转向有更宽透视。','两只手接触木环，无穿透第三手；画面右手指腹贴在右边缘，内缘触检读法请独审。','未生成GIF；三列是锚—新姿—锚的静态比较。'],'limitations':['细像素概念，不是native精灵','原锚颈稍长既存备注保留']},ensure_ascii=False,indent=2)+'\n')
print(D)
