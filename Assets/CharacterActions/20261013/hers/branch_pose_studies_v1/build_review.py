from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); D=R/'Assets/CharacterActions/20261013/hers/branch_pose_studies_v1'
anchor=R/'Assets/CharacterDesigns/20261013/expressive/hers/hers_raw_imagegen.png'
paths=[anchor,D/'escape_preparation_raw_imagegen.png',D/'remain_guarded_raw_imagegen.png']
ims=[Image.open(p).convert('RGBA') for p in paths]
# Alpha-only removal of near-invisible background residue; RGB and body geometry unchanged.
for im in ims: im.putalpha(im.getchannel('A').point(lambda v: 0 if v < 32 else v))
crops=[im.crop(im.getchannel('A').getbbox()) for im in ims]
scale=min(0.48,570/max(im.height for im in crops),370/max(im.width for im in crops))
for name,im in zip(['anchor_reference','escape_preparation','remain_guarded'],ims): im.save(D/(name+'_transparent.png'))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=lambda n:ImageFont.truetype(font,n)
for theme,bg,fg,minor in [('light',(239,234,222),(37,35,31),(83,77,68)),('dark',(35,39,43),(241,232,211),(198,194,180))]:
 board=Image.new('RGB',(1260,860),bg);dr=ImageDraw.Draw(board)
 dr.text((35,20),'赫斯 · N17 条件姿态对照',font=f(30),fill=fg)
 dr.text((35,68),'不同条件下的替代选择，不按左右顺序连播；两张新增姿态，零新增人物。',font=f(20),fill=minor)
 titles=['原锚参考','转身准备逃离','留场空手戒备']
 subs=['中性站姿 · 身份与服装参照','N17-R-defection · 无人替他挡价','N17-R-shutdown · 失去装置优势']
 foots=['同一人物，原图未改。','准备离开，尚未逃脱。','对峙姿态，尚未反击。']
 for i,im in enumerate(crops):
  x=i*410+25
  dr.text((x+8,112),titles[i],font=f(24),fill=fg);dr.text((x+8,150),subs[i],font=f(17),fill=minor)
  new=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
  board.paste(new,(x+(395-new.width)//2,755-new.height),new)
  dr.text((x+8,774),foots[i],font=f(19),fill=fg)
 dr.text((35,822),'静态人物概念；非跑步循环、战斗结算或游戏内实现。',font=f(18),fill=minor)
 board.save(D/f'hers_branch_pose_review_zh_{theme}.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[anchor,R/'design/04_人物/人物_赫斯·白.md',R/'design/04_人物/城市人物/人物_NPC-HERS_赫斯·白.md',R/'design/05_主线/台本/台本_N17_残光之井.md',R/'Assets/CharacterDesigns/20261013/expressive/roster.json']
roster=json.loads(sources[-1].read_text())
def get(x):
 if isinstance(x,dict):
  if x.get('id')=='NPC-HERS':return x
  for v in x.values():
   r=get(v)
   if r:return r
 if isinstance(x,list):
  for v in x:
   r=get(v)
   if r:return r
(D/'source_roster_record.json').write_text(json.dumps(get(roster),ensure_ascii=False,indent=2)+'\n')
manifest={'character_id':'NPC-HERS','aliases':['NPC10','CITY-NPC-NPC-HERS'],'new_character_count':0,'accepted_new_pose_count':2,'mode':'builtin imagegen, identity-preserve','sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in sources], 'branch_evidence':[{'route':'N17-R-defection','line':55,'quote':'赫斯没有人替他挡价后可逃或独战，账页不丢。','pose':'escape_preparation','boundary':'仅转身准备，未逃脱'},{'route':'N17-R-shutdown','line':54,'quote':'切两处可达支路，避开守卫视线后对峙；赫斯失去装置优势仍可能作有限反击。','pose':'remain_guarded','boundary':'仅空手戒备，未反击'}], 'relationship':'mutually conditional alternatives, NOT sequential animation','processing':{'alpha':'alpha values below 32 cleared to remove near-invisible background residue; original raw alpha preserved in raw files','body_transform':'none','board_transform':'common uniform nearest-neighbor scale','common_scale':scale,'crop':'alpha bounding boxes for boards only'},'rejected':[{'file':'escape_preparation_rejected_raw_imagegen.png','reason':'extra third hand/arm in first generation; superseded with exactly two hands'}], 'runtime_integrated':False,'gif_created':False,'independent_review':'pending','files':[{'path':p.name,'sha256':sha(p)} for p in sorted(D.iterdir()) if p.is_file()]}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'common_scale':scale,'image_sizes':[im.size for im in ims],'alpha_extrema':[im.getchannel('A').getextrema() for im in ims]},ensure_ascii=False))
