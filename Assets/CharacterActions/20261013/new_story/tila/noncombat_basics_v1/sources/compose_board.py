from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=R/'Assets/CharacterActions/20261013/new_story'; delivery=base/'fourth_noncombat_erde_tila_delivery_v1';delivery.mkdir(exist_ok=True)
fontpath='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';font=ImageFont.truetype(fontpath,24);small=ImageFont.truetype(fontpath,19);titlefont=ImageFont.truetype(bold,34);headfont=ImageFont.truetype(bold,25)
W,H=2908,1580; canvas=Image.new('RGB',(W,H),(230,223,208));dr=ImageDraw.Draw(canvas);dr.text((28,16),'珥德 / 缇菈 · 日常基础动作对照',font=titlefont,fill=(40,40,36));dr.text((30,66),'母图＋两张独立全身关键姿态  ·  真实透明素材在浅 / 深底合成  ·  非连续动画',font=font,fill=(70,69,62))
light=(239,233,219,255);dark=(29,34,38,255);layout={'schema_version':1,'canvas':[W,H],'background':[230,223,208],'resampling':'NEAREST','uniform_scale':0.4,'cells':[],'scope':'展示合板；仅最近邻等比、背景合成与文字标注，无人体修改'}
for row,slug in enumerate(['erde','tila']):
 p=base/slug/'noncombat_basics_v1';c=json.loads((p/'source_brief.json').read_text());name=c['name'];items=[('母图',R/c['mother_image']['transparent'])]+[(a['title_zh'],p/'exports'/(a['key']+'_v1_transparent.png')) for a in c['plans']]
 y=110+row*715
 dr.text((30,y),f'{name}  /  {c["canonical_id"]}',font=headfont,fill=(40,40,36))
 for col in range(6):
  label,path=items[col%3];tone='浅底' if col<3 else '深底';bg=light if col<3 else dark;x=28+col*476;top=y+43;cw,ch=464,647
  panel=Image.new('RGBA',(cw,ch),bg);d=ImageDraw.Draw(panel);fg=(44,45,42,255) if col<3 else (234,234,220,255);d.text((14,10),label,font=font,fill=fg);d.text((14,46),tone,font=small,fill=fg)
  src=Image.open(path).convert('RGBA');sz=(round(src.width*.4),round(src.height*.4));im=src.resize(sz,Image.Resampling.NEAREST);pos=((cw-sz[0])//2,ch-12-sz[1]);panel.alpha_composite(im,pos);canvas.paste(panel.convert('RGB'),(x,top));layout['cells'].append({'character':slug,'label':label,'tone':tone,'source':str(path.relative_to(R)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'background_rgba':list(bg),'cell_bbox':[x,top,x+cw,top+ch],'image_xy_in_cell':list(pos),'source_size':list(src.size),'scaled_size':list(sz),'uniform_scale':0.4})
board=delivery/'珥德_缇菈_母图动作浅深对照.png';canvas.save(board);layout['board']={'path':str(board.relative_to(R)),'sha256':hashlib.sha256(board.read_bytes()).hexdigest()};(delivery/'board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
for slug in ['erde','tila']:
 p=base/slug/'noncombat_basics_v1';shutil.copyfile(board,p/'review'/board.name);shutil.copyfile(delivery/'board_layout.json',p/'review/board_layout.json');shutil.copyfile(__file__,p/'sources/compose_board.py');q=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_fourth_new_character_actions_erde_tila_visual_gate_20261014.json';shutil.copyfile(q,p/'review'/q.name)
print(board);print(board.stat().st_size);print('SHA',layout['board']['sha256'])
