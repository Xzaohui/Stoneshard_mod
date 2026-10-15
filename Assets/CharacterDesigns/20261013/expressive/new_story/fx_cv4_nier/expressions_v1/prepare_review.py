from pathlib import Path
import json,hashlib,shutil,datetime,sys
from PIL import Image,ImageDraw,ImageFont
import numpy as np
p=Path(sys.argv[1]);c=json.loads((p/'sources/character_brief.json').read_text());slug=c['slug'];logs=json.loads((p/'generation-log.json').read_text());out=[];alpha=[]
for e in c['expressions']:
 r=next(x for x in reversed(logs) if x['expression']==e['id']);raw=p/r['raw'];dst=p/'selected'/f"{e['output_stem']}_transparent.png";shutil.copy2(raw,dst);im=Image.open(dst).convert('RGBA');a=np.array(im);mask=a[:,:,3]
 r.update({'label_zh':e['label_zh'],'selected':str(dst.relative_to(p)),'selected_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'selected_matches_raw_bytes':True,'revisions_used':0,'maximum_hard_error_revisions':1,'status':'author_selected_pending_independent_review'})
 alpha.append({'expression':e['id'],'size':list(im.size),'mode':'RGBA','alpha_min':int(mask.min()),'alpha_max':int(mask.max()),'zero_alpha_pixels':int((mask==0).sum()),'nonzero_rgb_under_zero_alpha':int(((mask==0)&np.any(a[:,:,:3]!=0,axis=2)).sum()),'alpha_bbox':list(im.getchannel('A').getbbox()),'hidden_rgb_is_not_visible_background':True,'asset_processing':'byte-exact raw copy; no pixel edits, scaling, quantization or alpha normalization'})
 out.append(im)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(font,42);sub=ImageFont.truetype(font,28);note=ImageFont.truetype(font,22)
for theme,bg,fg in [('light',(242,237,227,255),(54,47,38,255)),('dark',(32,36,41,255),(234,224,203,255))]:
 board=Image.new('RGBA',(1700,1530),bg);draw=ImageDraw.Draw(board);draw.text((70,30),c['name']+'｜两种表情概念',font=title,fill=fg);draw.text((72,94),c['canonical_id']+' · 单人全身 · 透明原稿',font=note,fill=fg)
 for i,(e,im) in enumerate(zip(c['expressions'],out)):
  scale=min(740/im.width,1230/im.height);small=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);x=50+i*825+(800-small.width)//2;y=175+(1230-small.height)//2;board.alpha_composite(small,(x,y));draw.text((95+i*825,135),e['id']+' · '+e['label_zh'],font=sub,fill=fg)
 draw.text((70,1450),'可逆美术提案；情绪不代表任务结案、付款、同意或关系变化。',font=note,fill=fg);draw.text((70,1488),'保持本人母图比例、衣物和道具；未验证游戏网格、装备兼容或动画。',font=note,fill=fg);board.convert('RGB').save(p/'review'/f'{slug}_expressions_{theme}_zh.png')
(p/'generation-log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n');(p/'alpha_report.json').write_text(json.dumps(alpha,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'selected':[x['selected'] for x in logs],'alpha':alpha},ensure_ascii=False))
