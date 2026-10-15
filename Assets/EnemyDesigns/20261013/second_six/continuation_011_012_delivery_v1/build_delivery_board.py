from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
brief=json.loads((ROOT.parent/'action_continuation_brief_v1.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',21)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',17)
board=Image.new('RGB',(1440,1590),(222,218,208));draw=ImageDraw.Draw(board)
draw.text((20,12),'011 / 012 新增关键姿态｜母图与相邻阶段对照',font=font,fill=(25,25,25))
draw.text((20,45),'浅深底为真实RGBA合成；旧图只做等比最近邻排版。新图为独立关键阶段，非完整连续动画。',font=small,fill=(40,40,40))
for group,x in enumerate(brief['items'][-2:]):
 p=REPO/x['planned_output_directory'];f=json.loads((p/'FINAL_STATUS.json').read_text());sel=p/f['selected_image']['path']
 dst=ROOT/('011_喉胸前送释放.png' if group==0 else '012_手铃外摆端点.png');shutil.copy2(sel,dst)
 refs=[REPO/a['source_path'] for a in x['source_images']]+[sel]
 labels=['母图（身份与风格）','旧：喉胸蓄势','旧：下压蹲姿','新增：喉胸前送释放'] if group==0 else ['母图（成熟紧凑版）','旧：举铃蓄势','旧：落低收铃','新增：手铃外摆端点']
 y0=85+group*725;draw.text((20,y0),x['concept_id']+' '+x['working_name']+'｜新增正选 v'+str(f['selected_version']),font=font,fill=(25,25,25))
 for row,bg in enumerate([(236,231,219),(32,35,40)]):
  for col,(path,label) in enumerate(zip(refs,labels)):
   src=Image.open(path).convert('RGBA');bbox=src.getchannel('A').point(lambda a:255 if a>=32 else 0).getbbox();crop=src.crop(bbox);scale=min(320/crop.width,280/crop.height);sz=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(sz,Image.Resampling.NEAREST)
   cell=Image.new('RGBA',(360,335),bg+(255,));cell.alpha_composite(crop,((360-sz[0])//2,322-sz[1]));d=ImageDraw.Draw(cell);d.text((12,8),label,font=small,fill=((32,32,32,255) if row==0 else (230,230,230,255)));board.paste(cell.convert('RGB'),(col*360,y0+35+row*335))
draw.text((20,1550),'未验证：连续帧时序、精确锚点、装备绑定、碰撞与游戏运行。',font=small,fill=(40,40,40))
board.save(ROOT/'011_012_相邻关键姿态_浅深对照.png')
