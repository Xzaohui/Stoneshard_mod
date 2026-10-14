from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,hashlib,sys,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=json.loads((r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/first_four_expression_brief.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for c in b['characters']:
 if c['slug'] not in ['deru','hoer']:continue
 d=r/f"Assets/CharacterDesigns/20261013/expressive/new_story/{c['slug']}/expressions_v1";stats=[]
 for e in c['expressions']:
  p=d/'raw'/f"{e['key']}_v1.png";im=Image.open(p).convert('RGBA');a=np.array(im); old=a.copy();low=a[:,:,3]<16;a[low]=0;a[a[:,:,3]==0,:3]=0
  out=d/'selected'/f"{e['key']}_transparent.png";Image.fromarray(a).save(out)
  stats.append({'id':e['id'],'label_zh':e['label_zh'],'raw':str(p.relative_to(d)),'raw_sha256':sha(p),'selected':str(out.relative_to(d)),'selected_sha256':sha(out),'size':list(im.size),'alpha_zero_pixels':int((a[:,:,3]==0).sum()),'alpha_partial_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),'hidden_RGB_nonzero_after':int(np.count_nonzero(np.any(a[:,:,:3],axis=2)&(a[:,:,3]==0))),'cleanup':'Only set alpha<16 fringe RGBA to zero; zero hidden RGB. Visible character RGB untouched; no paint or geometry edits.','bbox':list(Image.fromarray(a).getbbox()),'prompt':f"prompts/{e['key']}_v1.txt",'revision_count':0})
 for mode,bg,fg in [('light',(239,233,219,255),(39,35,30)),('dark',(27,33,43,255),(237,228,212))]:
  canvas=Image.new('RGBA',(1500,1150),bg);dr=ImageDraw.Draw(canvas);dr.text((35,20),c['name']+'｜日常情绪设定',font=ImageFont.truetype(font,32),fill=fg)
  ims=[Image.open(r/c['source_anchor']['selected_transparent']['path']).convert('RGBA')]+[Image.open(d/x['selected']).convert('RGBA') for x in stats]
  labs=['静态母图']+[e['label_zh'] for e in c['expressions']]
  for i,(im,lab) in enumerate(zip(ims,labs)):
   im=im.crop(im.getbbox());scale=min(450/im.width,780/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);canvas.alpha_composite(im,(i*500+(500-im.width)//2,140+(930-im.height)));dr.text((i*500+40,90),lab,font=ImageFont.truetype(font,28),fill=fg)
  dr.text((35,1100),'条件式情绪美术提案 · 非剧情完成/游戏实现证明',font=ImageFont.truetype(font,23),fill=fg);canvas.convert('RGB').save(d/'review'/f"{c['slug']}_expressions_{mode}.png")
 (d/'generation-log.json').write_text(json.dumps({'tool':'builtin image_gen.imagegen','reference':c['source_anchor']['selected_transparent'],'items':stats},ensure_ascii=False,indent=2))
 print(c['slug'],json.dumps(stats,ensure_ascii=False))
