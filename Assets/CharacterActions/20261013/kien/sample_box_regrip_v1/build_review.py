from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[5]; D=Path(__file__).resolve().parent
slug='kien'; ids=['anchor','K1','K2','anchor']; titles=['原锚 · 提柄低提','提柄不松、空手托底','双手腹前低抱','原锚复用 · 结束示意']
anchor=R/f'Assets/CharacterDesigns/20261013/expressive/{slug}/{slug}_raw_imagegen.png'
paths=[anchor,D/'raw/K1_raw_imagegen.png',D/'raw/K2_raw_imagegen.png',anchor]
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
 b=Image.new('RGB',(1640,820),bg);d=ImageDraw.Draw(b);d.text((25,16),'奇恩 · 小闭箱换握',font=font(29),fill=fg)
 d.text((25,60),'2 张新姿态 · 原锚首末复用 · 人物基础动作概念',font=font(19),fill=fg)
 for n,f in enumerate(frames):
  d.text((n*410+25,105),titles[n],font=font(21),fill=fg);b.paste(f,(n*410,120),f)
 d.text((25,773),'仅调整原小闭箱持握；不表示交货、验收、来源合法化或游戏运行。',font=font(20),fill=fg)
 b.save(D/f'kien_review_zh_{theme}.png')
# No GIF until independent continuity check resolves finger/inner-edge reading.
brief=R/'Assets/CharacterDesigns/20261013/expressive/briefs/town_work_pose_candidates_01.json'
source=R/'design/04_人物/城市人物/人物_ALD-NPC-KIEN_奇恩.md'
manifest={'character_id':'ALD-NPC-KIEN','name':'奇恩','status':'static_candidate_pending_independent_review','new_pose_count':2,'mode':'builtin imagegen identity-preserve','sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in [anchor,source,brief]],'sequence':ids,'gif_created':False,'gif_gate':'小闭箱侧面与高度随透视有变化，待独审确认同物尺寸；暂只静态候选。','processing':{'common_uniform_nearest_scale':scale,'alpha_cleanup':'alpha below 32 cleared; raw retained','body_synthesis':False,'nonuniform_stretch':False,'grounding':'common bottom y620'},'runtime_integrated':False,'story_boundary':['非交货验收完成','非款项到手','非来源合法化或通关'],'files':[{'path':str(p.relative_to(D)),'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='manifest.json']}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(D/'QA-author.json').write_text(json.dumps({'reviewed_raws':['anchor','K1','K2'],'decision':'static_candidate_pending_independent_review','observations':['脸、发型、衣装与双足保留；K1低头托底，K2抬脸腹前低抱，姿态差别清楚。','两张均为原提柄手在上、原空手托底，小箱闭合无字；未见悬空或第三手。','木箱正面高度基本接近，但锚到K2上表面可见量与箱厚有变化，请独审尺寸连续性。','暂未生成GIF；四列为锚—K1—K2—锚的静态比较。'],'limitations':['像素概念，不是native精灵或游戏运行']},ensure_ascii=False,indent=2)+'\n')
print(D)
