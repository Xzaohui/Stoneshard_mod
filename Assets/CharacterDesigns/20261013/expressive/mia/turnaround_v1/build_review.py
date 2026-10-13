from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[6] # repository root
p=root/'Assets/CharacterDesigns/20261013/expressive/mia/turnaround_v1'
src=root/'Assets/CharacterDesigns/20261013/expressive/mia/ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png'
files=[src,p/'raw/mia_side_raw_imagegen.png',p/'raw/mia_back_raw_imagegen.png']
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def ft(n):return ImageFont.truetype(font,n)
board=Image.new('RGB',(1500,1120),'#efebe3'); d=ImageDraw.Draw(board)
d.text((50,30),'米娅 · 人物转面设定',font=ft(38),fill='#27383b')
d.text((50,90),'批准基准复用  /  新补左侧与背面  /  仅人物概念研究',font=ft(22),fill='#52615f')
records=[]
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA'); a=im.getchannel('A'); bbox=a.point(lambda v:255 if v>5 else 0).getbbox(); crop=im.crop(bbox)
 # All three share precisely the same display scale. No per-view proportion edits.
 scale=.60; disp=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 x=250+i*500-disp.width//2; y=910-disp.height
 board.paste(disp,(x,y),disp)
 name=['四分之三 · 批准基准','左侧 · 新增视图','背面 · 新增视图'][i]
 d.text((55+i*500,945),name,font=ft(25),fill='#27383b')
 d.text((55+i*500,990),['复用原图，不改脸或比例','单眼侧投影，双手仍抱叠毯','披肩背形与辫根：设计推定'][i],font=ft(18),fill='#52615f')
 if i:
  im.save(p/('mia_side.png' if i==1 else 'mia_back.png'))
 records.append({'file':str(f.relative_to(root)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'canvas':im.size,'mode':im.mode,'alpha_gt5_bbox':bbox,'transparent_pixels':sum(v==0 for v in a.getdata()),'partial_alpha_pixels':sum(0<v<255 for v in a.getdata()),'display_scale':scale})
d.text((50,1060),'前方叠毯在背视图被遮挡。未新增背饰、武器或包；非方向动画、原版精灵或引擎兼容验收。',font=ft(21),fill='#52615f')
board.save(p/'mia_turnaround_review_zh.png')
(p/'sourcehash.json').write_text(json.dumps({'approved_source':records[0],'source_card':'design/04_人物/城市人物/人物_NPC-MIA_米娅.md'},ensure_ascii=False,indent=2)+'\n')
manifest={'character':'NPC-MIA','date':'2026-10-13','concept_only':True,'runtimeVerified':False,'directional_animation':False,'generator':'builtin image_gen','new_generated_images':2,'approved_source_unchanged':records[0]['sha256']=='3f2060ae7a0e1694995540c51160fd515a72c8013e548d2e9313cee857d493fd','assets':records,'processing':'Only identical 0.60 nearest-neighbor uniform scaling and translation for review layout; generated character pixels and original alpha preserved. Individual files are lossless PNG re-exports, with raw originals retained.','design_inferences':['Rear plain V-draped shawl structure','Nape braid attachment and rear hair arrangement','Blanket remains held in front and is occluded from rear view'],'status':'awaiting independent review','limitations':['Concept turnaround only; not production sprite or animation','Face and hair pixel clusters have minor generation drift','Rear structure is a proposal, not new story information','No equipment, mask, origin or runtime compatibility tested']}
manifest['deliverables']=[{'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [p/'mia_side.png',p/'mia_back.png',p/'mia_turnaround_review_zh.png']]
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest['deliverables'],indent=2))
