from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
root=p.parents[4]
src=root/'Assets/CharacterDesigns/20261013/expressive/mia/ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png'
files=[src,p/'raw/mia_adjust_raw_imagegen.png',p/'raw/mia_return_raw_imagegen.png',src]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=lambda n:ImageFont.truetype(font,n)
bg='#efece5'; ink='#293e41'; soft='#5a6969'
titles=['01 静抱 · 复用批准图','02 低头理毯 · 新绘','03 抱回身前 · 新绘','04 静抱 · 复用批准图']
notes=['基准不改，不算新增身体','左掌抚平上折面，右手托底','左手托底，右手收拢上缘','同一原图回置，仅作结束示意']
records=[]; frames=[]
board=Image.new('RGB',(1880,1010),bg); d=ImageDraw.Draw(board)
d.text((40,25),'米娅 · 理一下叠毯，再抱回身前',font=ft(36),fill=ink)
d.text((40,82),'2 张新绘全身关键姿态 + 2 次批准基准复用｜单次日常动作概念',font=ft(24),fill=soft)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA'); a=im.getchannel('A'); bbox=a.point(lambda v:255 if v>5 else 0).getbbox()
 # Only alpha<=5 is cleared. Above-threshold RGBA pixels are not repainted.
 im.putalpha(a.point(lambda v:0 if v<=5 else v))
 dy=1329-bbox[3]
 # One shared scale, derived from approved Mia art. No per-frame rescale or deformation.
 disp=im.resize((559,704),Image.Resampling.NEAREST)
 frame=Image.new('RGB',(640,930),bg); fd=ImageDraw.Draw(frame)
 fd.text((28,22),'米娅 · 理毯关键姿态',font=ft(29),fill=ink)
 frame.paste(disp,((640-559)//2,94+round(dy*.5)),disp)
 fd.text((28,803),titles[i],font=ft(26),fill=ink)
 fd.text((28,848),notes[i],font=ft(22),fill=soft)
 fd.text((28,893),'概念示意 · 非完整动画／游戏落地',font=ft(20),fill=soft)
 frame.save(p/f'mia_blanket_stage_{i+1:02d}_zh.png');frames.append(frame)
 x=i*470+(470-559)//2
 board.paste(disp,(x,156+round(dy*.5)),disp)
 d.text((22+i*470,880),titles[i],font=ft(25),fill=ink)
 d.text((22+i*470,922),notes[i],font=ft(20),fill=soft)
 records.append({'stage':i+1,'role':'reused_approved_reference' if i in [0,3] else 'new_generated_body','file':str(f.relative_to(root)),'sha256':sha(f),'canvas':list(im.size),'alpha_gt5_bbox':bbox,'shared_display_scale':0.5,'translation_y_before_scale':dy,'foot_baseline_source_y':1329})
 if i in [1,2]: im.save(p/('mia_adjust.png' if i==1 else 'mia_return.png'))
d.text((40,972),'同一普通叠毯；无新增护理技能、治愈或任务结果。保留姿态间生图漂移，未补中间帧。',font=ft(20),fill=soft)
board.save(p/'mia_blanket_adjust_review_zh.png')
# No loop extension means a single playback. No interpolation / synthetic body frames.
frames[0].save(p/'mia_blanket_adjust_once.gif',save_all=True,append_images=frames[1:],duration=[950,1100,1100,1200],disposal=2,optimize=False)
manifest={'character':'NPC-MIA','date':'2026-10-13','status':'awaiting_independent_review','concept_only':True,'runtimeVerified':False,'new_generated_bodies':2,'reused_approved_stages':2,'display_stages':4,'generated_repair_attempts':0,'generator':'builtin image_gen','approved_source_unchanged':sha(src)=='3f2060ae7a0e1694995540c51160fd515a72c8013e548d2e9313cee857d493fd','assets':records,'processing':'Only alpha <=5 cleared; shared 0.5 nearest-neighbor uniform scale; sole-baseline translation and layout. No repaint, frame-specific scaling, warping or interpolation. GIF uses format-required indexed colors; PNG originals retained.','gif':{'frames':4,'duration_ms':[950,1100,1100,1200],'total_duration_ms':4350,'loop_extension':False,'single_play':True},'limitations':['Two key poses, not a complete smooth animation','Small hair/head/cloth silhouette generation drift remains','Opening and closing stage repeat the identical approved standing reference','No gameplay, equipment-layer or runtime validation','Ordinary blanket motion adds no care skill, treatment, recovery or quest outcome']}
manifest['deliverables']=[{'file':f.name,'sha256':sha(f)} for f in sorted(p.glob('*.png'))]+[{'file':'mia_blanket_adjust_once.gif','sha256':sha(p/'mia_blanket_adjust_once.gif')}]
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(p/'sourcehash.json').write_text(json.dumps({'approved_reference':records[0],'source_card':{'file':'design/04_人物/城市人物/人物_NPC-MIA_米娅.md','sha256':sha(root/'design/04_人物/城市人物/人物_NPC-MIA_米娅.md')},'prompts':[{'file':str(f.relative_to(p)),'sha256':sha(f)} for f in sorted((p/'prompts').glob('*.txt'))],'raw':[{'file':str(f.relative_to(p)),'sha256':sha(f)} for f in sorted((p/'raw').glob('*.png'))]},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest['deliverables'],ensure_ascii=False,indent=2))
