from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
R=Path(__file__).resolve().parents[6]
A=R/'Assets/CharacterActions/20261013'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
settings=[('osin','sleeve_settle_v1','奥辛·锤','BRY-NPC-OSIN','O1','osin_raw_imagegen_v2.png','跨身压稳原卷袖'),('vasen','apron_brush_v1','瓦森·磨','OSB-NPC-VAS','V1','vasen_raw_imagegen.png','前屈拂原围裙粉痕')]
for slug,branch,name,cid,key,anchor,label in settings:
 d=A/slug/branch
 if Path(__file__).resolve()!=d/'scripts/build_review.py':shutil.copy2(__file__,d/'scripts/build_review.py')
 shutil.copy2(R/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md',d/'sources/STYLE_DIRECTION.md')
 shutil.copy2(R/f'Assets/CharacterDesigns/20261013/expressive/{slug}/QA-independent.json',d/'sources/anchor_QA-independent.json')
 (d/'sources/source_sha256.json').write_text(json.dumps({str(p.relative_to(d)):sha(p) for p in sorted((d/'sources').iterdir()) if p.name!='source_sha256.json'},ensure_ascii=False,indent=2))
 stats=[];imgs=[]
 for p,k in [(d/'sources'/anchor,'anchor'),(d/f'raw/{key}_raw_imagegen.png',key)]:
  im=Image.open(p).convert('RGBA');hist=im.getchannel('A').histogram(); im.putalpha(im.getchannel('A').point(lambda a:0 if a<32 else a));out=d/f'transparent/{k}.png';im.save(out);imgs.append(im)
  stats.append({'id':k,'input':str(p.relative_to(d)),'input_sha256':sha(p),'output':str(out.relative_to(d)),'output_sha256':sha(out),'canvas':im.size,'bbox':im.getbbox(),'alpha_cleanup':'Only alpha <32 becomes 0; all retained RGB and alpha unchanged','pixels_cleared':sum(hist[1:32]),'raw_unchanged':True})
 transforms=[]
 for theme,bg,fg in [('light',(239,234,220),(48,43,37)),('dark',(31,34,38),(240,233,216))]:
  board=Image.new('RGB',(1120,930),bg);dr=ImageDraw.Draw(board)
  dr.text((30,20),name+'｜独立工作关键姿态',font=F(32),fill=fg)
  dr.text((30,70),'1张新姿＋原锚对照；静态概念，不代表剧情完成或游戏运行。',font=F(20),fill=fg)
  for j,(im,lab) in enumerate(zip(imgs,['原锚：既有静态',key+'：'+label])):
   padded_size=(im.width+im.width%2,im.height+im.height%2)
   padded=Image.new('RGBA',padded_size,(0,0,0,0));padded.paste(im,(0,0))
   size=(padded.width//2,padded.height//2)
   resized=padded.resize(size,Image.Resampling.NEAREST);bbox=resized.getbbox();x=j*560+(560-size[0])//2;y=780-bbox[3];board.paste(resized,(x,y),resized)
   dr.text((j*560+25,805),lab,font=F(22),fill=fg)
   transforms.append({'theme':theme,'id':['anchor',key][j],'full_input_size':im.size,'transparent_canvas_padding_right_bottom':[im.width%2,im.height%2],'padded_size':padded_size,'full_output_size':size,'scale_x':'1/2','scale_y':'1/2','resample':'NEAREST','translation':[x,y],'crop':None,'rotation':0,'flip':False})
  dr.text((30,852),'原衣物接触；无新增工具；不作为连续动画或已落地精灵。',font=F(20),fill=fg)
  dr.text((30,892),'左右手职责为等价构图变体：图左拂粉，图右夹边。' if slug=='vasen' else '腰侧黄色工作手套仍为悬挂装备；不穿戴、不新增手。',font=F(19),fill=fg)
  board.save(d/f'{slug}_review_zh_{theme}.png')
 (d/'transforms.json').write_text(json.dumps(transforms,ensure_ascii=False,indent=2))
 author={'character_id':cid,'selected':f'raw/{key}_raw_imagegen.png','new_static_pose_count':1,'method':'实际查看完整原锚与所选raw；双底板随后复看。','status':'ready_for_independent_final_review','identity':'保原成年脸、头发帽子、厚实体型、短腿与原衣装；奥辛画幅占高略增。','contact':'跨身手夹浅色原卷袖，另一空手下垂，黄色手套仍挂腰。' if slug=='osin' else '图左开放手掌贴围裙粉痕，图右夹住下侧缘；围裙仍穿身上。','composition_variation':None if slug=='osin' else '左右职责与brief对调，独审认定合理等价构图，不是身份或惯用手错误。','author_revision_calls':0 if slug=='osin' else 1,'unselected_research':[] if slug=='osin' else ['raw/V1_revision_unselected_raw_imagegen.png'],'runtime_verified':False,'technical':stats,'limits':['只有一个新静态姿态，不声称连续动画、装备兼容或剧情结果。','未进行原生尺寸/碰撞/游戏运行验收。']}
 (d/'QA-author.json').write_text(json.dumps(author,ensure_ascii=False,indent=2))
 calls=[{'pose':key,'prompt':f'prompts/{key}.txt','raw':f'raw/{key}_raw_imagegen.png','raw_sha256':sha(d/f'raw/{key}_raw_imagegen.png'),'reference_inputs':['sources/'+anchor],'selected':True}]
 if slug=='vasen':calls.append({'pose':'V1_revision_unselected','prompt':'prompts/V1_revision.txt','raw':'raw/V1_revision_unselected_raw_imagegen.png','raw_sha256':sha(d/'raw/V1_revision_unselected_raw_imagegen.png'),'reference_inputs':['raw/V1_raw_imagegen.png','sources/'+anchor],'selected':False,'reason':'Hand roles were swapped before review; independent review accepted first draft as equivalent composition. Retained as unselected research, not a necessary identity correction.'})
 (d/'generation_log.json').write_text(json.dumps({'tool':'builtin image_gen.imagegen','raw_calls':calls,'selected_key_pose_count':1,'processing':'scripts/build_review.py; alpha<32 cleanup, whole-image exact uniform 1/2 nearest scaling and translation only; exact transforms.json. No anatomy drawing/stretching/quantization/rotation/mirroring.','raw_preserved':True,'frozen_before_final_review':True},ensure_ascii=False,indent=2))
 (d/'README_zh.md').write_text('# '+name+'｜工作关键姿态\n\n1张新静态姿态＋原锚并列。内置imagegen完成绘画；原稿均保留。无GIF，不构成连续动画、剧情完成或游戏运行验收。\n\n仅透明清理与整图等比nearest排版，精确记录在transforms.json；人物身体未用脚本绘制或拉伸。\n\n'+('瓦森所选首稿左右手职责与brief对调，属合理等价构图；唯一修订已在复核消息到达前调用，仅保留为未选研究。\n' if slug=='vasen' else '')+'\n冻结manifest含generation_log；后续终审只新增QA与FINAL_STATUS。\n')
 print(d)
