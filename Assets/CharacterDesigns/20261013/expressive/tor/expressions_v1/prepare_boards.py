from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import hashlib,json,shutil,datetime
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
BASE=ROOT/'Assets/CharacterDesigns/20261013/expressive'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
common=['design/04_人物/人物_玛拉与伊沃.md','design/05_主线/台本/台本_N1_无钟之夜.md','Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md']
for actor,name,ids,labels in [('rhea','蕾雅',['01_listening','02_reminder','03_resolve'],['警惕倾听','清楚提醒','柔和但坚定']),('tor','托雷',['01_scrutiny','02_question','03_weighing'],['克制审视','谨慎质询','权衡迟疑'])]:
 d=BASE/actor/'expressions_v1'; selected=[]; alpha=[]
 for id,label in zip(ids,labels):
  src=d/(id+('_costume_fixed_raw_imagegen.png' if actor=='tor' else '_raw_imagegen.png'))
  raw=Image.open(src).convert('RGBA'); im=raw.crop((0,0,1254,1120)); a=im.getchannel('A'); removed=sum(1 for v in a.getdata() if 0<v<=5); im.putalpha(a.point(lambda v:0 if v<=5 else v))
  out=d/(id+'_transparent.png'); im.save(out);selected.append(im)
  alpha.append({'id':id,'label':label,'raw':src.name,'candidate':out.name,'raw_sha256':sha(src),'candidate_sha256':sha(out),'alpha_le5_cleaned_pixels_in_crop':removed,'crop':[0,0,1254,1120]})
 for mode,bg,fg in [('white',(255,255,255,255),(30,25,22)),('black',(18,18,20,255),(240,234,224))]:
  board=Image.new('RGBA',(1921,704),bg);draw=ImageDraw.Draw(board)
  draw.text((24,12),name+' · 三种表情',font=ImageFont.truetype(font,30),fill=fg)
  draw.text((24,660),'静态人物概念 · 未逐人批准 · 不代表剧情结果或游戏落地',font=ImageFont.truetype(font,21),fill=fg)
  for i,(im,label) in enumerate(zip(selected,labels)):
   x=10+i*637;board.alpha_composite(im.resize((627,560),Image.Resampling.NEAREST),(x,88))
   draw.text((x+313,55),label,font=ImageFont.truetype(font,25),fill=fg,anchor='mt')
  board.convert('RGB').save(d/(actor+'_expressions_'+mode+'_zh.png'))
 white=Image.open(d/(actor+'_expressions_white_zh.png'));black=Image.open(d/(actor+'_expressions_black_zh.png'))
 bw=Image.new('RGB',(1921,1408));bw.paste(white,(0,0));bw.paste(black,(0,704));bw.save(d/(actor+'_expressions_black_white_zh.png'))
 
 if Path(__file__).resolve() != (d/'prepare_boards.py').resolve(): shutil.copy(__file__,d/'prepare_boards.py')
 anchor=BASE/('tor/period_costume_v2/tor_period_costume_v2_transparent.png' if actor=='tor' else 'rhea/rhea_raw_imagegen.png')
 sources=[{'path':p,'sha256':sha(ROOT/p)} for p in common]+[{'path':str(anchor.relative_to(ROOT)),'sha256':sha(anchor)}]
 qa={'actor':'n1_'+actor,'status':'author_visual_pass_pending_independent_review','userApproved':False,'new_characters':0,'new_expressions':3,'visual_findings':(['Same brown hair, full short beard, angular nose and mature chin maintained. Scrutiny has tight eyes and closed level mouth; question raised brow and open speaking mouth; weighing inner brow rise and off-center pressed mouth.','Initial busts regressed to folded lapels; one built-in costume-only repair per expression removed all lapels, preserving face/expression perceptually. Repair raw and prompts are retained.','No verdict, official insignia, canceled debt or villain caricature.'] if actor=='tor' else ['Same short fringe, low bun, strong nose and wide mature chin maintained; blue shawl and grey dress unchanged in identity.','Alert listening, open speaking reminder, and softly closed firm smile differ at both brows/eyes and mouth. Third expression is mild warmth, not happy evacuation or a childlike sweet face.','Rolled blanket spiral remains obvious in all three; no baby, child, mother-child relationship or completed evacuation.']), 'technical_checks':{'same_source_canvas':[1254,1254],'common_crop':[0,0,1254,1120],'candidate_dimensions':[1254,1120],'board_image_scale':0.5,'resampling':'nearest','no_anisotropic_stretch':True,'raw_untouched':True,'alpha_cleanup':'only alpha <=5 to zero inside common crop; RGB unchanged','crop_scope':'intentional uniform lower-chest truncation removes varying lower arm/waist framing; hair and shoulders retained'},'runtimeVerified':False,'equipmentCompatibilityVerified':False,'equipmentMechanism':'unknown','independentReview':'pending'}
 (d/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 manifest={'actor':'n1_'+actor,'version':'expressions_v1','createdAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generation':'built-in image_gen; separate call per expression; transparent_background=true','new_character_count':0,'new_expression_count':3,'sources':sources,'expressions':alpha,'postprocessing':'Common crop [0,0,1254,1120]; alpha <=5 zeroed; no RGB repaint. Boards use exactly 0.5x nearest-neighbor isotropic scale. Chinese labels outside art. Raw images untouched.','presentationBoard':actor+'_expressions_white_zh.png','blackWhiteBoard':actor+'_expressions_black_white_zh.png','authorQA':'QA-author.json','independentReview':'pending','userApproved':False,'conceptOnly':True,'runtimeIntegrated':False,'runtimeVerified':False,'equipmentCompatibilityVerified':False,'equipmentMechanism':'unknown','outputs':[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(d.iterdir()) if p.is_file() and p.name!='manifest.json']}
 (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(actor,[(x['id'],x['candidate_sha256']) for x in alpha])
