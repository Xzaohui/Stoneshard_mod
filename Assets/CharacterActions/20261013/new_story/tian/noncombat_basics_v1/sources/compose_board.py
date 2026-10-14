from PIL import Image,ImageDraw,ImageFont
import pathlib,json
r=pathlib.Path(__file__).resolve()
while r.name!='Stoneshard_mod':r=r.parent
d=r/'Assets/CharacterActions/20261013/new_story/third_noncombat_tian_lein_delivery_v1'
selection=json.loads((d/'selection.json').read_text())
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(font,36);small=ImageFont.truetype(font,25);lab=ImageFont.truetype(font,29)
w=1800;rowh=660;top=135;bottom=95
board=Image.new('RGBA',(w,top+4*rowh+bottom),(239,233,219,255));dr=ImageDraw.Draw(board)
dr.text((40,24),'缇安 · 蕾因｜非战斗基础动作',font=title,fill='#292521')
dr.text((40,78),'每人两张独立静态姿态 · 母图对照 · 浅／深底复核',font=small,fill='#514A43')
layout=[]
for ci,c in enumerate(selection):
 for bi,(bg,name,fg) in enumerate([((239,233,219,255),'浅底','#292521'),((29,34,38,255),'深底','#EEE8DB')]):
  y=top+(ci*2+bi)*rowh;dr.rectangle((0,y,w,y+rowh),fill=bg)
  dr.text((36,y+17),c['name']+' · '+name,font=lab,fill=fg)
  imgs=[(c['mother'],'已审母图，仅对照')]+[(x['path'],x['label']) for x in c['selected']]
  for col,(file,label) in enumerate(imgs):
   im=Image.open(r/file).convert('RGBA');bbox=im.getbbox();cut=im.crop(bbox);scale=min(530/cut.width,515/cut.height);size=(round(cut.width*scale),round(cut.height*scale));cut=cut.resize(size,Image.Resampling.NEAREST)
   x=col*600+(600-size[0])//2;yy=y+75+515-size[1];board.alpha_composite(cut,(x,yy));dr.text((col*600+40,y+607),label,font=small,fill=fg)
   layout.append({'row':ci*2+bi,'col':col,'file':file,'source_alpha_bbox':bbox,'destination_xy':(x,yy),'destination_size':size,'resampling':'NEAREST','proportional':True,'RGBA_alpha_composite':True})
dr=ImageDraw.Draw(board);dr.text((40,top+4*rowh+15),'仅动作概念；未制作过渡／连续动画，未接入游戏。',font=small,fill='#514A43')
board.convert('RGB').save(d/'delivery/缇安_蕾因_母图动作浅深对照.png')
(d/'board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
