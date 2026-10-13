from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib,shutil,sys
root=Path(__file__).resolve().parents[6];c=Path(__file__).resolve().parent.parent.name
p=root/f'Assets/CharacterDesigns/20261013/expressive/{c}/expressions_v1'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
if c=='mara':
 title='玛拉';names=['01_restrained_inquiry','02_guarded_reserve','03_slight_relief'];labels=['克制询问','警惕保留','稍松口气'];notes=['微提眉心，小幅开口','收眉闭口，保留话语','眉眼放松，担忧未消']
else:
 title='伊沃';names=['01_guarded_listening','02_difficult_explanation','03_firm_request'];labels=['戒备倾听','艰难解释','坚定请求'];notes=['紧眉侧听，闭口谨慎','眉心抬起，谨慎开口','凝目定眉，认真请求']
files=[p/'raw'/f'{n}_raw_imagegen.png' for n in names];ims=[Image.open(f).convert('RGBA') for f in files]
assert len(set(im.size for im in ims))==1
boxes=[im.getchannel('A').point(lambda a:255 if a>5 else 0).getbbox() for im in ims];box=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';ft=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1536,1120),'#efebe3');d=ImageDraw.Draw(board)
d.text((38,25),f'{title} · 对话表情研究',font=ft(38),fill='#293535');d.text((38,80),'同视角胸像 / 既有身份延续 / 三张静态情绪概念',font=ft(23),fill='#556361')
records=[]
for i,(f,im,n) in enumerate(zip(files,ims,names)):
 crop=im.crop(box);scale=min(455/crop.width,540/crop.height);disp=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
 board.paste(disp,(i*512+(512-disp.width)//2,145),disp)
 d.text((38+i*512,710),labels[i],font=ft(30),fill='#293535');d.text((38+i*512,758),notes[i],font=ft(21),fill='#556361')
 for j,bg in enumerate(['#ffffff','#101010']):
  small=crop.resize((round(crop.width*.15),round(crop.height*.15)),Image.Resampling.NEAREST);panel=Image.new('RGB',(220,190),bg);panel.paste(small,((220-small.width)//2,(190-small.height)//2),small);board.paste(panel,(36+i*512+j*224,820));panel.save(p/'checks'/f'{n}_{"white" if j==0 else "black"}.png')
 shutil.copyfile(f,p/f'{c}_{n}.png');a=im.getchannel('A');h=a.histogram()
 records.append({'file':str(f.relative_to(root)),'sha256':sha(f),'canvas':im.size,'mode':im.mode,'alpha_range':a.getextrema(),'alpha_gt5_bbox':boxes[i],'transparent_pixels':h[0],'partial_alpha_pixels':sum(h[1:255]),'label':labels[i],'prompt':f'prompts/{n}.txt','prompt_sha256':sha(p/'prompts'/f'{n}.txt'),'inputs':[f'../{c}_raw_imagegen_v2.png'] if i==0 else [f'raw/{names[0]}_raw_imagegen.png',f'../{c}_raw_imagegen_v2.png']})
d.text((38,1032),'下排为白／黑底透明检查；同组采用相同裁切与等比缩放，不拉伸脸部。',font=ft(23),fill='#556361');d.text((38,1073),'情绪不代表团圆、逃离成功、结案或免责。非动画、非游戏运行验收。',font=ft(23),fill='#556361')
board.save(p/f'{c}_expressions_review_zh.png')
src=root/f'Assets/CharacterDesigns/20261013/expressive/{c}/{c}_raw_imagegen_v2.png'
sourcefiles=[src,src.parent/'QA-independent.json',root/'design/04_人物/人物_玛拉与伊沃.md',root/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md',*sorted((root/'design/05_主线/台本').glob('台本_N[123]_*.md'))]
(p/'sourcehash.json').write_text(json.dumps({'sources':[{'file':str(f.relative_to(root)),'sha256':sha(f)} for f in sourcefiles],'source_unchanged':True,'source_user_approved':False},ensure_ascii=False,indent=2)+'\n')
manifest={'character':f'n1_{c}','date':'2026-10-13','concept_only':True,'runtimeVerified':False,'animation':False,'new_characters':0,'new_generated_images':3,'generator':'builtin image_gen','status':'awaiting independent review','user_approved':False,'assets':records,'processing':{'individual_pngs':'Exact byte copies of retained generated raws.','board':'Same union crop, same uniform nearest-neighbor scale; compositing on cream/white/black only. No face painting, quantization, alpha cleanup or nonuniform scaling.','common_crop':box,'common_scale':scale},'deliverables':[{'file':f.name,'sha256':sha(f)} for f in [*[p/f'{c}_{n}.png' for n in names],p/f'{c}_expressions_review_zh.png']]}
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
# The generator script is retained beside these assets.
print(json.dumps(manifest['deliverables'],ensure_ascii=False,indent=2))
