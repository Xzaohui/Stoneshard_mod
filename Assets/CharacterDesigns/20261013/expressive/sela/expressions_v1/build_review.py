from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent
root=p.parents[5]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
src=root/'Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png'
assert sha(src)=='c61337a497f4a6e6cdccb8d1cee8b8a49dba7aa9cfc13057678bce7e9fbc026a'
names=['01_friendly_greeting','02_serious_explanation','03_questioning_scrutiny']
labels=['亲切招呼','认真解释','疑惑审视']
notes=['舒展眉眼，温和微笑','眉眼收束，小幅张口','单侧挑眉，闭口审视']
files=[p/'raw'/f'{n}_raw_imagegen.png' for n in names]
ims=[Image.open(f).convert('RGBA') for f in files]
assert len(set(im.size for im in ims))==1
# All three use the same crop and uniform nearest-neighbor transform. No face painting.
bboxes=[im.getchannel('A').point(lambda a:255 if a>5 else 0).getbbox() for im in ims]
box=(min(b[0] for b in bboxes),min(b[1] for b in bboxes),max(b[2] for b in bboxes),max(b[3] for b in bboxes))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
ft=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1536,910),'#efebe3');d=ImageDraw.Draw(board)
d.text((45,28),'瑟拉 G · 同视角表情研究',font=ft(38),fill='#27383b')
d.text((45,85),'BRY-NPC-SELA   /   胸口以上 · 原发型与衣装延续',font=ft(22),fill='#52615f')
records=[]
for i,(f,im,n) in enumerate(zip(files,ims,names)):
 crop=im.crop(box);scale=.50
 disp=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 board.paste(disp,(i*512+(512-disp.width)//2,162),disp)
 d.text((45+i*512,710),labels[i],font=ft(30),fill='#27383b')
 d.text((45+i*512,760),notes[i],font=ft(20),fill='#52615f')
 shutil.copyfile(f,p/f'sela_{n}.png')
 a=im.getchannel('A')
 records.append({'file':str(f.relative_to(root)),'sha256':sha(f),'canvas':im.size,'mode':im.mode,'alpha_gt5_bbox':bboxes[i],'transparent_pixels':sum(v==0 for v in a.getdata()),'partial_alpha_pixels':sum(0<v<255 for v in a.getdata()),'label':labels[i],'prompt':f'prompts/{n}.txt','prompt_sha256':sha(p/'prompts'/f'{n}.txt'),'inputs':[str(src.relative_to(root))] if i==0 else [str(files[0].relative_to(root)),str(src.relative_to(root))]})
d.text((45,837),'人物概念研究：0 新人物；无剧情绑定。不是动画帧、装备兼容或游戏运行验收。',font=ft(23),fill='#52615f')
board.save(p/'sela_expressions_review_zh.png')
sourcefiles=[src,root/'design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md',root/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md',p.parent/'turnaround_v1/manifest.json',p.parent/'turnaround_v1/sela_turnaround_review_zh.png']
(p/'sourcehash.json').write_text(json.dumps({'sources':[{'file':str(f.relative_to(root)),'sha256':sha(f)} for f in sourcefiles],'approved_source_unchanged':True},ensure_ascii=False,indent=2)+'\n')
manifest={'character':'BRY-NPC-SELA','date':'2026-10-13','concept_only':True,'runtimeVerified':False,'animation':False,'new_characters':0,'new_generated_images':3,'targeted_revisions':0,'generator':'builtin image_gen','status':'awaiting independent review','assets':records,'processing':{'individual_pngs':'Exact byte copies of retained generated raws.','board':'Same union crop, same 0.50 nearest-neighbor scale, translation only; original alpha composited on cream board. No face paint, stretching, quantization or alpha cleanup.','common_crop':box,'common_scale':.50},'limitations':['Original G identity kept as reference; generated portraits have slightly more open eyes than original.','Minor generated cluster drift outside brows, eyes and mouth remains; not pixel-locked expression deltas.','Only concept studies; not runtime or final sprite assets.'],'deliverables':[{'file':f.name,'sha256':sha(f)} for f in [*[p/f'sela_{n}.png' for n in names],p/'sela_expressions_review_zh.png']]}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest['deliverables'],ensure_ascii=False,indent=2))
