from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
B=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive');J=json.loads((B/'briefs/next_main_cast_expressions_morren_rey_01.json').read_text());F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
land={'morlen':[(91,883),(112,918),(72,880)],'leo':[(80,825),(113,909),(30,805)]}
notes={'morlen':['内眉微提 · 疲惫下视 · 松闭唇','一眉略起 · 低侧视 · 小幅启唇','眉心收低 · 清醒直视 · 短句口形'],'leo':['非对称眉 · 窄眼侧看 · 收紧唇','内眉稍起 · 衡量目光 · 松开唇','眉心压稳 · 明确直视 · 发话口形']}
allims={}
for c in J['characters']:
 s=c['slug'];o=B/s/'expressions_v1';shutil.copy2(__file__,o/'build_review.py');ims=[];stats=[]
 for e in c['expressions']:
  revision = (s=='morlen' and e['key'].startswith('morlen_E2')) or (s=='leo' and e['key'].startswith('leo_E3'))
  p=o/'raw'/(e['key']+('_revision1' if revision else '')+'_raw_imagegen.png');im=Image.open(p).convert('RGBA');a=np.array(im);mask=a[:,:,3]<32;n=int(np.sum((a[:,:,3]>0)&mask));a[mask]=0;clean=Image.fromarray(a);q=o/'selected'/(e['key']+'_transparent.png');clean.save(q);ims.append(clean);stats.append({'raw':str(p.relative_to(o)),'selected':str(q.relative_to(o)),'raw_sha256':sha(p),'selected_sha256':sha(q),'dimensions':list(im.size),'processing':'Only zero RGBA for original alpha <32; all other pixels unchanged; selected unscaled.','nonzero_alpha_pixels_cleared':n,'preserved_pixels_exact':bool(np.array_equal(a[~mask],np.array(im)[~mask]))})
 allims[s]=ims
 for theme,bg,fg in [('light','#eee8dc','#302b29'),('dark','#202630','#eee8dc')]:
  board=Image.new('RGB',(1800,900),bg);d=ImageDraw.Draw(board);d.text((30,20),c['name']+' · 三态表情设定',font=F(34),fill=fg);d.text((30,70),'独立条件场景｜同一人物与衣装｜五官表演研究，未接入游戏',font=F(23),fill=fg)
  for i,im in enumerate(ims):
   crown,chin=land[s][i];sc=340/(chin-crown);box=im.getbbox();crop=im.crop(box);sz=(round(crop.width*sc),round(crop.height*sc));thumb=crop.resize(sz,Image.Resampling.NEAREST);board.paste(thumb,(i*600+(600-sz[0])//2,125),thumb);d.text((i*600+30,730),f'E{i+1}  '+c['expressions'][i]['label'],font=F(27),fill=fg);d.text((i*600+30,775),notes[s][i],font=F(22),fill=fg)
  d.text((30,850),'不是连续悔改或结案；存活、在场、愿谈、核验与本人授权仍以台本为准。',font=F(23),fill=fg);board.save(o/'review'/f'{s}_expressions_review_zh_{theme}.png')
 qa={'character':s,'status':'author_review_pending_independent','raw_actually_viewed':True,'boards_actually_viewed':False,'revision_count':1,'notes':notes[s],'processing':stats,'landmarks_crown_chin_y':land[s],'board_processing':'Alpha bbox crop; each image uniform NEAREST scaling to head height 340px; never face warp or redraw.','limitations':['概念胸像，非动画／运行精灵；围巾和肩甲透视有小幅生成差异。','莫伦E2已用唯一修订，眉不对称与开口更清楚；最终以独审为准。' if s=='morlen' else '雷奥E3已用唯一修订恢复粗簇、长眼和块状胡茬；最终以独审为准。']};(o/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(o/'README.md').write_text('# '+c['name']+' 表情设定\n\n内置imagegen逐幅绘制，raw完整保留。selected仅清除alpha<32的低透明边缘，其余像素不变。中文浅深板只做等比最近邻缩放、排版。不是连续悔改／结案，不证明治愈、护理完成、付款、签约或监督承诺。本人存活、在场、愿谈、核验与授权条件见sources原brief/台本。未接入游戏，未改roster；独审结果以QA-independent.json及FINAL_STATUS.json为准。\n')
D=B/'morlen_leo_expressions_v1_delivery';D.mkdir(exist_ok=True)
for theme in ['light','dark']:
 canvas=Image.new('RGB',(1800,1800));
 for i,s in enumerate(['morlen','leo']):canvas.paste(Image.open(B/s/'expressions_v1/review'/f'{s}_expressions_review_zh_{theme}.png'),(0,i*900))
 canvas.save(D/f'morlen_leo_expressions_zh_{theme}.png')
