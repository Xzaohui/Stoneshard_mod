from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/first_four_expression_brief.json';brief=json.loads(B.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',34);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
for c in brief['characters'][:2]:
 slug=c['slug'];out=R/f'Assets/CharacterDesigns/20261013/expressive/new_story/{slug}/expressions_v1'; alpha=[]; log=[]; imgs=[]
 for e in c['expressions']:
  stem=e['output_stem'];raw=out/'raw'/f'{stem}_v1.png'; final=out/'selected'/f'{stem}_transparent.png';src=Image.open(raw);assert src.mode=='RGBA';a=np.array(src);mask=a[:,:,3]<=8;a[mask]=0;clean=Image.fromarray(a);im=Image.new('RGBA',(clean.width+96,clean.height+96));im.paste(clean,(48,48));im.save(final);imgs.append(im)
  av=np.array(im)[:,:,3];alpha.append({'expression':e['id'],'mode':im.mode,'raw_size':src.size,'selected_size':im.size,'alpha_zero':int((av==0).sum()),'alpha_partial':int(((av>0)&(av<255)).sum()),'alpha_opaque':int((av==255).sum()),'bbox':im.getbbox(),'operation':'Only source alpha <=8 pixels set to RGBA zero, then 48px transparent padding on every side; alpha >8 pixels preserved exactly. No repaint/crop/quantize/stretch.'})
  log.append({'expression':e['id'],'tool':'builtin image_gen.imagegen','variant':'v1','reference':c['source_anchor']['selected_transparent'],'prompt':f'prompts/{stem}_v1.txt','prompt_sha256':sha(out/'prompts'/f'{stem}_v1.txt'),'raw':str(raw.relative_to(out)),'raw_sha256':sha(raw),'selected':str(final.relative_to(out)),'selected_sha256':sha(final),'revisions_used':0,'maximum_hard_error_revisions':1})
 for theme,bg,fg in [('light',(237,233,222),(39,40,38)),('dark',(34,39,44),(237,233,221))]:
  board=Image.new('RGB',(1680,1320),bg);d=ImageDraw.Draw(board);d.text((45,24),c['name']+'｜两种日常情绪',font=font,fill=fg);d.text((45,78),c['canonical_id']+' · 人物外观概念 · 两幅互不代表剧情先后',font=small,fill=fg)
  for k,(e,im) in enumerate(zip(c['expressions'],imgs)):
   n=im.copy();n.thumbnail((780,1050),Image.Resampling.NEAREST);board.paste(n,(k*840+(840-n.width)//2,156+(1060-n.height)//2),n);d.text((k*840+55,125),e['label_zh'],font=font,fill=fg)
  d.text((45,1260),'只表达可逆心情；不代表接班、续约、付款、治疗、任务完成或游戏已实现。',font=small,fill=fg);board.save(out/'review'/f'{slug}_expressions_{theme}.png')
 (out/'alpha_report.json').write_text(json.dumps(alpha,ensure_ascii=False,indent=2));(out/'generation-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));shutil.copyfile(__file__,out/'export_assets.py')
 print(slug,[(x['expression'],x['selected_sha256']) for x in log])
