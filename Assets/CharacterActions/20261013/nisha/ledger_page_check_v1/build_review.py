from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
A=R/'Assets/CharacterActions/20261013'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=lambda n:ImageFont.truetype(font,n)
settings=[('nisha','ledger_page_check_v1','妮莎·炉','SKO-NPC-NIS',['N1','N2'],['原锚：闭册侧抱','N1：托脊打开、低头核看','N2：捻起一页、仍连书脊']),('doro','empty_bowl_present_v1','多罗','MAE-NPC-DORO',['D1'],['原锚：腹前围托空碗','D1：双手平托、向前待递'])]
for slug,branch,name,cid,poses,labels in settings:
 d=A/slug/branch
 shutil.copy2(__file__,d/'build_review.py')
 src=R/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md';shutil.copy2(src,d/'sources/STYLE_DIRECTION.md')
 sources=json.loads((d/'sources/SOURCE_SHA256.json').read_text());sources.append({'source':str(src.relative_to(R)),'copy':'sources/STYLE_DIRECTION.md','sha256':sha(src)});(d/'sources/SOURCE_SHA256.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2))
 inputs=[d/f'sources/{slug}_raw_imagegen.png']+[d/f'raw/{p}_raw_imagegen.png' for p in poses]
 imgs=[];stats=[]
 for p,key in zip(inputs,['anchor']+poses):
  im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); counts=a.histogram(); im.putalpha(a.point(lambda x:0 if x<32 else x)); out=d/f'transparent/{key}.png';im.save(out)
  bbox=im.getbbox();imgs.append(im)
  stats.append({'id':key,'input':str(p.relative_to(d)),'input_sha256':sha(p),'output':str(out.relative_to(d)),'canvas':im.size,'bbox_after_cleanup':bbox,'fully_transparent_before':counts[0],'alpha_cleanup':'Only alpha below 32 cleared; retained pixel RGB unchanged.','raw_preserved':True})
 scale=.46; cell=550; width=cell*len(imgs);height=920
 for theme,bg,fg,sub in [('light',(239,234,220),(48,43,37),(91,81,65)),('dark',(31,34,38),(240,233,216),(191,185,168))]:
  board=Image.new('RGB',(width,height),bg);dr=ImageDraw.Draw(board)
  dr.text((32,20),name+'｜独立工作关键姿态',font=F(31),fill=fg)
  dr.text((32,68),'原锚仅供对照；新增姿态为概念提案，不代表剧情完成或游戏运行。',font=F(19),fill=sub)
  for j,(im,label) in enumerate(zip(imgs,labels)):
   # Resize the complete image uniformly, never independent body or prop parts.
   resized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
   box=resized.getbbox(); x=j*cell+(cell-resized.width)//2;y=760-box[3]
   board.paste(resized,(x,y),resized)
   dr.text((j*cell+22,790),label,font=F(22),fill=fg)
  note='内页仅作无内容表面推定；无笔、无文字、无结算或免责。' if slug=='nisha' else '同一只空木碗；尚在双手承托中，无接收、喂食或治疗完成。'
  dr.text((32,838),note,font=F(19),fill=sub)
  dr.text((32,875),'仅静态对照，不制作或声称连续动画。',font=F(18),fill=sub)
  board.save(d/f'{slug}_review_zh_{theme}.png')
 author={'character_id':cid,'method':'作者实际查看原锚及每张完整raw；浅深板稍后实际目检。','provisional_decision':'ready_for_independent_review','new_poses':poses,'identity':'原脸型、发巾、衣裙、围裙及鞋保持；既有身颈稍长和细像素备注不洗掉。','contacts':'N1双手托开册；N2单页夹点及连脊可辨。' if slug=='nisha' else '两掌贴碗底/下外侧，空腔与水平碗口可见，前伸空间可辨。','no_new_prop':True,'story':'静态动作提案，不写回任何事件完成。','limitations':['概念图，非原生精灵、连续动画、装备兼容或runtime验收。','细像素与原比例备注保留。'],'revision_calls':0,'technical':stats}
 (d/'QA-author.json').write_text(json.dumps(author,ensure_ascii=False,indent=2))
 log={'tool':'builtin image_gen.imagegen','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_calls':[{'pose':p,'prompt':f'prompts/{p}.txt','raw':f'raw/{p}_raw_imagegen.png','sha256':sha(d/f'raw/{p}_raw_imagegen.png'),'reference_inputs':['sources/'+slug+'_raw_imagegen.png'] if p!='N2' else ['raw/N1_raw_imagegen.png','sources/'+slug+'_raw_imagegen.png']} for p in poses],'revision_calls':0,'processing':'build_review.py: alpha<32 cleared, whole-image uniform 0.46 nearest scale for board, translation only. No drawing, anatomy synthesis, nonuniform stretching, quantization or GIF.','raw_untouched':True}
 (d/'generation_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 (d/'README_zh.md').write_text(f'# {name} 工作关键姿态\n\n{len(poses)}张新全身静态姿态＋原锚对照。默认不做GIF，不包装为连续动画。\n\nraw保留全部生图原件；prompts保留完整提示词；sources含原锚、原卡、brief与SHA；transparent为只清理低alpha的导出。浅深板只将整幅图等比nearest缩放、平移排版，未拉伸身体。\n\n内置imagegen制作；角色机制unknown，runtime未验。独审结果另见QA与FINAL_STATUS。\n')
 print(d)
