from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,numpy as np
D=Path(__file__).resolve().parent
B=json.loads((D/'sources/files/Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_four_expression_brief.json').read_text())
C=next(c for c in B['characters'] if c['slug']==D.parent.name)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
alpha=[]; calls=[]
for E in C['expressions']:
 key=E['key']+'_v1'; raw=D/'raw'/f'{key}.png'
 if not raw.exists():continue
 im=Image.open(raw).convert('RGBA'); a=np.array(im); original=a.copy(); mask=a[:,:,3]>=128
 a[:,:,3]=np.where(mask,255,0);a[~mask,:3]=0
 out=D/'selected'/f"{E['key']}_transparent.png"; Image.fromarray(a).save(out)
 alpha.append({'expression':E['key'],'raw':str(raw.relative_to(D)),'raw_sha256':sha(raw),'selected':str(out.relative_to(D)),'selected_sha256':sha(out),'dimensions':list(im.size),'alpha_only_cleanup':'alpha threshold 128; alpha>=128 set opaque; alpha<128 cleared; RGB of retained pixels unchanged; no shape edits, stretching, quantization or resampling','retained_pixels':int(mask.sum()),'partial_alpha_source_pixels':int(((original[:,:,3]>0)&(original[:,:,3]<255)).sum()),'visible_rgb_unchanged':bool((a[mask,:3]==original[mask,:3]).all()),'bbox':Image.fromarray(a).getbbox()})
 event=json.loads((D/'tool_returns'/f'{key}.event.json').read_text()); params=json.loads((D/'prompts'/f'{key}.parameters.json').read_text()); assert params['prompt']==(D/'prompts'/f'{key}.txt').read_text()
 event.update({'prompt_file':f'prompts/{key}.txt','prompt_sha256':sha(D/'prompts'/f'{key}.txt'),'parameters_sha256':sha(D/'prompts'/f'{key}.parameters.json'),'reference_inputs':[{'path':p,'sha256':sha(Path(p))} for p in params['referenced_image_paths']],'raw_sha256':sha(raw),'raw_dimensions':list(im.size),'original_return_sha256':sha(D/'tool_returns'/f'{key}.original.json'),'selected_file':str(out.relative_to(D)),'selected_sha256':sha(out),'selection_reason':'作者初检未发现身份/衣具/比例/面部情绪硬错；交独审复核','status':'selected_pending_independent_review'})
 calls.append(event)
(D/'alpha_report.json').write_text(json.dumps(alpha,ensure_ascii=False,indent=2)+'\n');(D/'generation-log.json').write_text(json.dumps({'tool':'builtin image_gen.imagegen','all_original_returns_retained':True,'calls':calls,'revision_calls':0,'not_claimed':B['delivery_plan']['not_claimed']},ensure_ascii=False,indent=2)+'\n')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; title=ImageFont.truetype(font,40); label=ImageFont.truetype(font,29); small=ImageFont.truetype(font,21)
for theme,bg,fg in [('light',(239,233,219),(49,43,35)),('dark',(29,35,45),(239,231,213))]:
 board=Image.new('RGB',(1400,1120),bg); dr=ImageDraw.Draw(board); dr.text((48,28),C['name']+' · 两种独立表情',font=title,fill=fg)
 for i,E in enumerate(C['expressions']):
  p=D/'selected'/f"{E['key']}_transparent.png"
  if not p.exists():continue
  im=Image.open(p).convert('RGBA');scale=min(640/im.width,880/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST); x=350+700*i-im.width//2;board.paste(im,(x,122+(880-im.height)//2),im)
  dr.text((90+700*i,96),E['id']+'  '+E['label_zh'],font=label,fill=fg)
 dr.text((48,1063),'透明背景选稿 · 表情概念 · 独立提案',font=small,fill=fg);board.save(D/'review'/f"{C['slug']}_expressions_{theme}.png")
print(json.dumps({'slug':C['slug'],'images':alpha},ensure_ascii=False))
