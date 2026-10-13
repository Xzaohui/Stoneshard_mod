from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent
root=p.parents[5]
src=root/'Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png'
files=[src,p/'raw/sela_side_raw_imagegen.png',p/'raw/sela_back_raw_imagegen.png']
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(src)=='c61337a497f4a6e6cdccb8d1cee8b8a49dba7aa9cfc13057678bce7e9fbc026a'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
ft=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1500,1120),'#efebe3');d=ImageDraw.Draw(board)
d.text((50,30),'瑟拉 · 人物转面设定',font=ft(38),fill='#27383b')
d.text((50,90),'BRY-NPC-SELA  /  批准G基准复用  /  新补侧面与背面',font=ft(22),fill='#52615f')
records=[]
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');a=im.getchannel('A');bbox=a.point(lambda v:255 if v>5 else 0).getbbox();crop=im.crop(bbox)
 scale=.60;disp=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 x=250+i*500-disp.width//2;y=910-disp.height;board.paste(disp,(x,y),disp)
 d.text((55+i*500,945),['四分之三 · 批准G','左侧 · 新补视图','背面 · 新补视图'][i],font=ft(25),fill='#27383b')
 d.text((55+i*500,990),['原图不改，沿用瑟拉自身比例','原配色与环状物按形延续','肩巾背形与束发结构：设计推定'][i],font=ft(18),fill='#52615f')
 if i:shutil.copyfile(f,p/('sela_side.png' if i==1 else 'sela_back.png'))
 records.append({'file':str(f.relative_to(root)),'sha256':sha(f),'canvas':im.size,'mode':im.mode,'alpha_gt5_bbox':bbox,'transparent_pixels':sum(v==0 for v in a.getdata()),'partial_alpha_pixels':sum(0<v<255 for v in a.getdata()),'display_scale':scale})
d.text((50,1060),'仅人物概念补图，不增人物数；非方向动画、原版精灵、换装兼容或游戏运行验收。',font=ft(21),fill='#52615f')
board.save(p/'sela_turnaround_review_zh.png')
(p/'sourcehash.json').write_text(json.dumps({'approved_source':records[0],'source_card':'design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md','source_card_sha256':sha(root/'design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md')},ensure_ascii=False,indent=2)+'\n')
m={'character':'BRY-NPC-SELA','date':'2026-10-13','concept_only':True,'runtimeVerified':False,'directional_animation':False,'generator':'builtin image_gen','new_generated_images':2,'new_characters':0,'approved_source_unchanged':True,'assets':records,'processing':'Raw copies retained. Individual PNGs are exact byte copies. Board uses identical 0.60 nearest-neighbor uniform scaling and translation only; no character painting or proportions changes. Alpha preserved.','design_inferences':['Rear gathered hair structure','Plain short teal shoulder cape rear continuation','Dark rear torso; cream front panel occluded','Source golden-brown loop continued at anatomical left waist, no functional identity invented'],'status':'awaiting independent review','limitations':['Concept only; not runtime or equipment compatible sprite','Minor generation drift in individual pixel clusters','Hidden rear details are design proposals, not original canon']}
m['deliverables']=[{'file':f.name,'sha256':sha(f)} for f in [p/'sela_side.png',p/'sela_back.png',p/'sela_turnaround_review_zh.png']]
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(m['deliverables'],indent=2))
