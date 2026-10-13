from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
B=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive');J=json.loads((B/'briefs/next_main_cast_expressions_lyd_hers_01.json').read_text());F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
notes={'lyd':['眉眼放松 · 慎重措辞 · 小幅启唇','眉心稳住 · 自主直视 · 短句发言'],'hers':['单眉反问 · 稳定对视 · 以代价辩护','内眉微提 · 侧移视线 · 压住下一句话']}
for c in J['characters']:
 s=c['slug'];o=B/s/'expressions_v1';shutil.copy2(__file__,o/'build_review.py');ims=[];stats=[]
 for i,e in enumerate(c['expressions'],1):
  p=o/'raw'/f'E{i}_raw_imagegen.png';im=Image.open(p).convert('RGBA');a=np.array(im);mask=a[:,:,3]<32;n=int(np.sum((a[:,:,3]>0)&mask));a[mask]=0;clean=Image.fromarray(a);q=o/'selected'/(e['key']+'_transparent.png');clean.save(q);ims.append(clean)
  stats.append({'raw':str(p.relative_to(o)),'selected':str(q.relative_to(o)),'raw_sha256':sha(p),'selected_sha256':sha(q),'dimensions':list(im.size),'processing':'Only zero RGBA for original alpha <32; all other pixels unchanged; selected unscaled.','nonzero_alpha_pixels_cleared':n,'preserved_pixels_exact':bool(np.array_equal(a[~mask],np.array(im)[~mask]))})
 transforms=[]
 for theme,bg,fg in [('light','#eee8dc','#302b29'),('dark','#202630','#eee8dc')]:
  board=Image.new('RGB',(1200,900),bg);d=ImageDraw.Draw(board);d.text((30,20),c['name']+' · 两态表情设定',font=F(34),fill=fg);d.text((30,70),'独立条件场景｜眉眼口型演出｜概念设定，未接入游戏',font=F(24),fill=fg)
  for i,im in enumerate(ims):
   size=(552,552);thumb=im.resize(size,Image.Resampling.NEAREST);xy=(i*600+24,140);board.paste(thumb,xy,thumb);d.text((i*600+30,730),f'E{i+1}  '+c['expressions'][i]['label'],font=F(28),fill=fg);d.text((i*600+30,782),notes[s][i],font=F(21),fill=fg)
   if theme=='light':transforms.append({'selected':stats[i]['selected'],'input_dimensions':list(im.size),'crop':None,'resize_dimensions':list(size),'uniform_scale':552/im.width,'resampling':'NEAREST','paste_xy':list(xy)})
  d.text((30,850),'两态不是连续剧情；本人存活、在场、核验与授权条件仍以现行台本为准。',font=F(23),fill=fg);board.save(o/'review'/f'{s}_expressions_review_zh_{theme}.png')
 qa={'character':s,'status':'author_review_pending_independent','raw_actually_viewed':True,'boards_actually_viewed':False,'revision_count':0,'notes':notes[s],'processing':stats,'board_transforms':transforms,'limitations':['概念胸像，非动画／运行精灵。','Lyd E2一小条上齿，待独审是否仍属于克制短句发言。' if s=='lyd' else '赫斯受挫只表示条件停顿，不是落败、认罪、魔化或死亡。']};(o/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(o/'README.md').write_text('# '+c['name']+' 表情设定\n\n内置imagegen逐幅绘制，raw完整保留。selected仅清除alpha<32的低透明边缘，其余像素不变。中文浅深板只做全图等比最近邻缩放、排版。两态为独立条件备选，不是连续剧情。\n\n'+ '\n'.join(e['label']+'：'+e['condition_and_limit'] for e in c['expressions'])+'\n\n未接入游戏，未改roster；独审结果以QA-independent.json及FINAL_STATUS.json为准。\n')
D=B/'lyd_hers_expressions_v1_delivery';D.mkdir(exist_ok=True)
canvas=Image.new('RGB',(1200,1800))
for i,s in enumerate(['lyd','hers']):canvas.paste(Image.open(B/s/'expressions_v1/review'/f'{s}_expressions_review_zh_light.png'),(0,i*900))
canvas.save(D/'lyd_hers_expressions_zh_light.png')
print(D)
