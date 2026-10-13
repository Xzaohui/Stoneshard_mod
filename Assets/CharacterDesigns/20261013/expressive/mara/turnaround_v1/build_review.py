from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json,sys,shutil
root=Path(__file__).resolve().parents[6]; who=sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent.parent.name; cn={'mara':'玛拉','ivo':'伊沃'}[who]; base=root/'Assets/CharacterDesigns/20261013/expressive'/who;p=base/'turnaround_v1'
ver='_v2' if who=='mara' else ''
files=[base/f'{who}_raw_imagegen_v2.png']+[p/f'raw/{who}_{v}{("_v3" if who=="mara" and v=="side" else ver)}_raw_imagegen.png' for v in ['side','back']]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; ft=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1500,1120),'#efebe3');d=ImageDraw.Draw(board)
d.text((50,30),cn+' · 人物转面设定',font=ft(38),fill='#27383b');d.text((50,90),'前3/4概念锚复用  /  新补左侧与背面  /  未获逐人批准',font=ft(22),fill='#52615f')
records=[]
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');a=im.getchannel('A'); bbox=a.point(lambda v:255 if v>5 else 0).getbbox();crop=im.crop(bbox);scale=.60;disp=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 board.paste(disp,(250+i*500-disp.width//2,910-disp.height),disp)
 d.text((55+i*500,945),['前3/4 · 现行概念锚','左侧 · 新增视图','背面 · 新增视图'][i],font=ft(25),fill='#27383b')
 d.text((55+i*500,990),['复用原图，不改脸或比例','保留身份服装；非精确正交','未见背部结构为设计推定'][i],font=ft(18),fill='#52615f')
 if i: shutil.copyfile(f,p/(who+('_side.png' if i==1 else '_back.png')))
 records.append({'file':str(f.relative_to(root)),'sha256':sha(f),'canvas':im.size,'mode':im.mode,'alpha_gt5_bbox':bbox,'transparent_pixels':sum(v==0 for v in a.getdata()),'partial_alpha_pixels':sum(0<v<255 for v in a.getdata()),'display_scale':scale})
d.text((50,1060),'仅人物概念研究，未改变故事结果；非方向动画、原生精灵、换装兼容或运行验收。',font=ft(21),fill='#52615f');board.save(p/f'{who}_turnaround_review_zh.png')
qa=Image.new('RGB',(1500,1800));dd=ImageDraw.Draw(qa)
for row,bg in enumerate(['#ffffff','#000000']):
 dd.rectangle((0,row*900,1500,(row+1)*900),fill=bg)
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGBA');box=im.getchannel('A').point(lambda v:255 if v>5 else 0).getbbox();im=im.crop(box);im=im.resize((round(im.width*.60),round(im.height*.60)),Image.Resampling.NEAREST);qa.paste(im,(250+i*500-im.width//2,row*900+840-im.height),im)
qa.save(p/'QA_background_comparison.png')
card=root/'design/04_人物/人物_玛拉与伊沃.md';roster=root/'Assets/CharacterDesigns/20261013/expressive/roster.json'
(p/'sourcehash.json').write_text(json.dumps({'concept_anchor':records[0],'source_card':{'file':str(card.relative_to(root)),'sha256':sha(card)},'roster_snapshot_sha256':sha(roster),'prior_review':{'file':str((base/'QA-independent.json').relative_to(root)),'sha256':sha(base/'QA-independent.json')},'user_approved':False},ensure_ascii=False,indent=2)+'\n')
inferences=['后背素色裙片、领口与围裙系带结构','低发髻的后方发束连接；围巾端留前方','前方补丁在背面遮挡，右手绳圈仍保留'] if who=='mara' else ['软帽后方折褶与后脑头发排列','灰绿外衣背片、旧斜带的背部走向','工具刀位置为原有左腰，后视遮挡属于视角变化']
manifest={'character':'n1_'+who,'date':'2026-10-13','concept_only':True,'runtimeVerified':False,'directional_animation':False,'generator':'builtin image_gen','new_selected_images':2,'total_generation_calls':5 if who=='mara' else 2,'concept_anchor_unchanged':True,'user_approved':False,'assets':records,'processing':'Review boards only: identical 0.60 nearest-neighbor uniform scaling and translation to common foot baseline. Raw images and original alpha preserved; individual files byte-identical raw copies. No character drawn, stretched or repainted by script.','design_inferences':inferences,'status':'awaiting independent review','limitations':['概念转面，非精确正交或动作精灵','脸发像素与视角存在生成漂移，待独立审看','背面结构为设计推定，不作原作事实','无装备兼容或运行验证']}
manifest['prompts']=[{'file':str(f.relative_to(p)),'sha256':sha(f),'full_text':f.read_text()} for f in sorted((p/'prompts').glob('*.txt'))]
manifest['raw_versions']=[{'file':str(f.relative_to(p)),'sha256':sha(f)} for f in sorted((p/'raw').glob('*.png'))]
manifest['deliverables']=[{'file':f.name,'sha256':sha(f)} for f in [p/f'{who}_side.png',p/f'{who}_back.png',p/f'{who}_turnaround_review_zh.png',p/'QA_background_comparison.png']]
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(p/'README.md').write_text(f'# {cn}转面候选\n\n仅人物设定研究。现行前3/4概念锚未改，尚无用户逐人批准。新左侧/背面候选待独立视觉审看。\n\n三列统一0.60 nearest等比缩放、脚底平移对齐，无机械拉伸或脚本造人物。透明单图逐字节复制选中raw；黑白底为检查板。完整提示词与来源SHA在manifest/sourcehash。\n\n背面未见结构均为原创设计推定，非原作事实；不表示剧情结局、换装、方向动画或游戏实现。\n')
# Script is retained beside the review assets; no external generator script needed.
print(json.dumps(records,ensure_ascii=False))
