from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,datetime,sys
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');s=sys.argv[1];d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/s/'concept_v1';raw=d/f'{s}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');hist=im.getchannel('A').histogram();px=im.load();cleared=0;hidden=0
for y in range(im.height):
 for x in range(im.width):
  r,g,b,a=px[x,y]
  if a<=8:
   if a:cleared+=1
   if (r,g,b)!=(0,0,0):hidden+=1
   px[x,y]=(0,0,0,0)
im.save(d/f'{s}_transparent.png')
c=json.loads((d/'character_brief.json').read_text());ft=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',40);fs=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
for mode,bg,fg in [('light',(238,231,216,255),(43,40,33)),('dark',(34,39,43,255),(237,228,211))]:
 can=Image.new('RGBA',(im.width+160,im.height+300),bg);can.alpha_composite(im,(80,155));dr=ImageDraw.Draw(can);dr.text((60,28),f"{c['name']}  {c['canonical_id']} ｜ {c['story_role']}",font=ft,fill=fg);dr.text((60,91),'原创单人全身概念 · 中性成年可逆提案 · 待独立审查',font=fs,fill=fg)
 note='左手旧缺指可读；具体指位未定，像素手指为简化提案。' if s=='wuer' else '布条钩杆、腰圈旧绳与手上旧痕；关节细定位需后续手部小样。'
 dr.text((60,can.height-104),note,font=fs,fill=fg);dr.text((60,can.height-64),'脸型、发型、配色均可逆；游戏运行与装备兼容未验证。',font=fs,fill=fg);can.convert('RGB').save(d/f'{s}_{mode}_board.png')
(d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes());log={'generator':'builtin image_gen.imagegen','transparent_background':True,'raw_size':im.size,'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'raw_alpha_histogram':hist,'alpha_1_to_8_cleared_pixels':cleared,'hidden_rgb_cleared_pixels':hidden,'alpha_bbox_gt8':im.getchannel('A').getbbox(),'allowed_operations':'Only alpha<=8 set zero, RGB cleared on resulting alpha zero; full uncropped raw original-size RGBA composition onto boards. No character painting, recoloring, resampling, local transformations, cropping or geometry changes.','revision_count':0,'runtime_verified':False};(d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));print(s,cleared,hidden)
