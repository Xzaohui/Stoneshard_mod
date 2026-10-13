from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json,shutil,sys
root=Path(__file__).resolve().parents[6]
who=sys.argv[1] if len(sys.argv)>1 else 'tor'
base=root/'Assets/CharacterDesigns/20261013/expressive'/who;p=base/'turnaround_v1'
cn={'tor':'托雷','rhea':'蕾雅'}[who]
anchor=base/('period_costume_v2/tor_period_costume_v2_transparent.png' if who=='tor' else 'rhea_raw_imagegen.png')
files=[anchor]+[p/f'{who}_{v}_raw_imagegen.png' for v in ['left','back']]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
ft=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',n)
board=Image.new('RGB',(1500,1120),'#efebe3');d=ImageDraw.Draw(board)
d.text((50,30),cn+' · 人物转面设定',font=ft(38),fill='#27383b')
d.text((50,90),'前3/4概念锚复用  /  新补左侧与背面  /  非精确正交图',font=ft(22),fill='#52615f')
qa=Image.new('RGB',(1500,1800),'white');ImageDraw.Draw(qa).rectangle((0,900,1500,1800),fill='black')
records=[]
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');a=im.getchannel('A');bbox=a.point(lambda v:255 if v>5 else 0).getbbox();crop=im.crop(bbox);disp=crop.resize((round(crop.width*.60),round(crop.height*.60)),Image.Resampling.NEAREST)
 board.paste(disp,(250+i*500-disp.width//2,910-disp.height),disp)
 for row in range(2):qa.paste(disp,(250+i*500-disp.width//2,row*900+840-disp.height),disp)
 d.text((55+i*500,945),['前3/4 · 现行概念锚','左侧 · 新增视图','背面 · 新增视图'][i],font=ft(25),fill='#27383b')
 d.text((55+i*500,990),['原图复用，未改比例','保留同人衣装与持物','未见背部结构为设计推定'][i],font=ft(18),fill='#52615f')
 if i:
  out=p/f'{who}_{["front","left","back"][i]}_transparent.png';shutil.copyfile(f,out)
  for bg in ['white','black']:
   bgim=Image.new('RGBA',im.size,bg);bgim.alpha_composite(im);bgim.convert('RGB').save(p/f'{who}_{["front","left","back"][i]}_{bg}.png')
 records.append({'file':str(f.relative_to(root)),'sha256':sha(f),'canvas':list(im.size),'alpha_gt5_bbox':bbox,'transparent_pixels':sum(v==0 for v in a.getdata()),'partial_alpha_pixels':sum(0<v<255 for v in a.getdata()),'display_scale':.60})
d.text((50,1060),'人物概念研究；未改变故事结果。非方向动画、原生精灵、换装兼容或运行验收。',font=ft(21),fill='#52615f')
board.save(p/f'{who}_turnaround_review_zh.png');qa.save(p/'QA_background_comparison.png')
sources=[root/'design/04_人物/人物_玛拉与伊沃.md',base.parent/'STYLE_DIRECTION.md',base.parent/'roster.json',base/('period_costume_v2/QA-independent.json' if who=='tor' else 'QA-independent.json')]
sourcehash={'anchor':records[0],'sources':[{'file':str(f.relative_to(root)),'sha256':sha(f)} for f in sources]}
(p/'sourcehash.json').write_text(json.dumps(sourcehash,ensure_ascii=False,indent=2)+'\n')
manifest={'character':'n1_'+who,'date':'2026-10-13','concept_only':True,'runtimeVerified':False,'equipment_compatibility_verified':False,'equipment_mechanism':'unknown','directional_animation':False,'generator':'builtin image_gen','new_selected_images':2,'generation_calls':2,'new_characters':0,'anchor_unchanged':True,'user_approved':False,'assets':records,'processing':'Raw and individual transparent PNGs byte-identical. Review boards crop by alpha>5 bbox only for layout, retain source alpha; all panels common 0.60 nearest-neighbor uniform scale and foot translation. No shape, anatomy, color edits or per-view stretching. Black/white single-image composites preserve full canvas.','design_inferences':['背面未见发束、素色衣片、披肩/斜带结构作保守设计推定，不新增身份、道具或剧情结果。'],'status':'awaiting independent review','prompts':[{'file':f.name,'sha256':sha(f),'full_text':f.read_text()} for f in sorted(p.glob('*_prompt.txt'))],'deliverables':[{'file':f.name,'sha256':sha(f)} for f in sorted(p.glob('*.png'))]}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
qa_author={'reviewer':'author self-review, not independent','status':'candidate_ready_for_independent_review','actually_viewed':['anchor','left raw','back raw','review board','black/white comparison'],'observations':(['棕发短须、紧凑头身与朴素直边中世纪外衣保持；不使用旧西装翻领马甲。','右手闭账本无字、左腰包；背面右手在画面右、包在画面左。','背面轻侧展示角，后背普通棕布与斜带为推定。'] if who=='tor' else ['短刘海低髻、宽颌坚定表情、蓝披灰裙旧靴保持。','解剖左手抱普通卷毯；背面卷毯在画面左，右手空垂。无婴儿或新增人。','背面为轻侧展示角，后披肩三角下摆、灰裙背面为保守推定。']),'limitations':['非机械正交图；生成式轻微比例/像素漂移待独立审看。','保留raw alpha，非原生二值透明精灵。','未作装备、合成、运行验收。']}
(p/'QA-author.json').write_text(json.dumps(qa_author,ensure_ascii=False,indent=2)+'\n')
(p/'README.md').write_text(f'# {cn}转面候选\n\n前3/4现行锚复用，新左侧与背面各1图。透明单图等同raw，中文三列统一0.60最近邻缩放、脚底平移。背面未见结构为设计推定。概念候选待独审；不计新人物，不改roster，不代表用户批准、方向动画、换装或游戏运行。\n')
print(json.dumps(records,ensure_ascii=False))
