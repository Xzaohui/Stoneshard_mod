from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,sys
r=Path.cwd();slug=sys.argv[1];b=json.loads((r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/fifth_new_character_actions_brief.json').read_text());c=next(x for x in b['characters'] if x['slug']==slug);d=r/c['proposed_output_directory']
selected=[c['plans'][0]['key']+('_v2' if slug=='wadun' else '_v1'),c['plans'][1]['key']+'_v1']
paths=[r/c['mother_image']['transparent']]+[d/'exports'/f'{s}_transparent.png' for s in selected]
labels=['已审母图']+[p['title_zh'] for p in c['plans']]
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,30);small=ImageFont.truetype(font,22);title=ImageFont.truetype(font,39)
out=Image.new('RGB',(1664,1816),(239,234,221));dr=ImageDraw.Draw(out);dr.text((32,20),f"{c['name']} {c['canonical_id']}｜母图与两张独立基础动作",font=title,fill=(35,40,43));dr.text((32,78),'上排浅底 · 下排深底｜同一完整图等比 nearest 排版',font=small,fill=(66,70,71));layout=[]
for row,bg in enumerate([(239,234,221,255),(33,37,41,255)]):
 y=122+row*822
 if row:dr.rectangle((0,y,1664,y+822),fill=bg[:3])
 for col,(p,label) in enumerate(zip(paths,labels)):
  im=Image.open(p).convert('RGBA');scale=min(500/im.width,750/im.height);sz=(round(im.width*scale),round(im.height*scale));scaled=im.resize(sz,Image.Resampling.NEAREST);panel=Image.new('RGBA',sz,bg);panel.alpha_composite(scaled);x=32+col*544+(500-sz[0])//2;py=y+54
  out.paste(panel.convert('RGB'),(x,py));dr.text((32+col*544,y+5),label,font=f,fill=((35,40,43) if row==0 else (235,232,219)))
  layout.append({'source':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'placement_xy':[x,py],'render_dimensions':list(sz),'uniform_scale':scale,'resize':'NEAREST','cropped':False,'body_modified':False,'background_rgba':bg})
note='原创可逆演出提案；非连续动画，不代表剧情结果或游戏落地。'
if slug=='endai': note+=' A1俯头后比例有轻微漂移，已审可用。'
dr.text((28,1776),note,font=ImageFont.truetype(font,20),fill=(35,40,43))
path=d/'review'/f'{c["name"]}_母图动作浅深对照.png';out.save(path)
(d/'review/board_layout.json').write_text(json.dumps({'board':str(path.relative_to(r)),'board_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'canvas':[1664,1816],'panels':layout,'selected_stems':selected},ensure_ascii=False,indent=2));print(str(path))
