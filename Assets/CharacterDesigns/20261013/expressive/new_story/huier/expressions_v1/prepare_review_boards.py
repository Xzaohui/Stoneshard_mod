from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,numpy as np,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/seventh_four_expression_brief.json';b=json.loads(B.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',32);title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',46);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
times={'lier_E1_fond_old_tree_chuckle':('2026-10-14T01:53:13.703Z','2026-10-14T01:53:55.893Z'),'lier_E2_sobering_at_hollow_water':('2026-10-14T01:55:10.791Z',None),'huier_E1_concerned_cloud_reading':('2026-10-14T01:56:48.686Z',None),'huier_E2_alert_to_upstream_rumble':('2026-10-14T01:58:03.242Z',None)}
for c in b['characters']:
 if c['slug'] not in ('lier','huier'):continue
 D=R/'Assets/CharacterDesigns/20261013/expressive/new_story'/c['slug']/'expressions_v1';checks=[]
 for e in c['expressions']:
  p=D/'raw'/f"{e['key']}_initial.png";out=D/'selected'/f"{e['key']}_transparent.png";shutil.copy2(p,out);im=Image.open(p).convert('RGBA');a=np.asarray(im);rawbbox=im.getchannel('A').getbbox();ys,xs=np.nonzero(a[:,:,3]>8);bbox=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));h=im.getchannel('A').histogram();checks.append({'key':e['key'],'raw':{'path':str(p.relative_to(D)),'sha256':sha(p)},'selected':{'path':str(out.relative_to(D)),'sha256':sha(out)},'raw_selected_byte_identical':sha(p)==sha(out),'mode':im.mode,'dimensions':list(im.size),'alpha_bbox_raw':list(rawbbox),'visible_alpha_gt8_bbox':list(bbox),'margins_ltrb':[bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3]],'alpha_zero_pixels':h[0],'alpha_partial_pixels':sum(h[1:255]),'alpha_opaque_pixels':h[255],'alpha_histogram':{str(i):x for i,x in enumerate(h) if x},'alpha_zero_nonzero_rgb_pixels':int(np.count_nonzero((a[:,:,3]==0)&np.any(a[:,:,:3]!=0,axis=2))),'processing':'无像素编辑。透明选稿逐字节复制原始工具输出；保留原始RGBA，不阈值化、不涂改、不变形、不调色、不量化。已先查看浅深背景合成，alpha0隐藏RGB不可见且不作实体瑕疵判定。'})
  assert checks[-1]['margins_ltrb'][0]>0 and min(checks[-1]['margins_ltrb'])>0
 for mode,bg,ink in [('light',(238,230,211),(42,36,31)),('dark',(31,35,42),(238,230,211))]:
  board=Image.new('RGB',(2356,1647),bg);dr=ImageDraw.Draw(board);dr.text((50,26),c['name']+' · '+c['canonical_id']+'｜两种表情',font=title,fill=ink);dr.text((50,88),'同一人物的可逆演出提案；表情不代表剧情结果',font=small,fill=ink)
  for i,e in enumerate(c['expressions']):
   dr.text((50+1178*i,137),e['id']+' '+e['label_zh'],font=font,fill=ink);im=Image.open(D/'selected'/f"{e['key']}_transparent.png").convert('RGBA');board.paste(im,(30+1178*i,192),im)
  dr.text((50,1608),'完整透明选稿另存｜游戏像素网格、装备、动画与运行未验证',font=small,fill=ink);board.save(D/'review'/f"{c['slug']}_expressions_{mode}_zh.png")
 write(D/'technical_qa.json',checks)
 log=json.loads((D/'generation-log.json').read_text());log['status']='all_four_initials_saved_author_reviewing';log['raw_return_storage']='完整返回对象以JSON序列化留存，image_url为完整原始data URL、output_hint原样；原始PNG与返回data URL解码及原生成路径三者SHA一致。'
 for x in log['calls']:
  x['time_called_utc']=times[x['key']][0]
  if times[x['key']][1]:x['time_tool_returned_utc']=times[x['key']][1]
  else:x['time_tool_returned_utc']=None;x['time_note']='调用开始时间精确记录；工具返回时间未单独截取，time_completed_utc为返回文件归档时刻的上界。'
  x['status']='selected_initial_author_visual_pass';x['revisions_used']=0;x['selection_reason']='表情可读，身份、年龄、服装、道具侧别及完整轮廓未见需修订硬错。'
 log['storage_incidents']=([{'action':'保存完整返回对象','state':'initial_shell_argument_too_long_before_execution','generation_repeated':False,'resolution':'从仍在会话中的完整原返回分块原样写盘；校验解码与原始生成路径SHA一致。'}] if c['slug']=='lier' else [])
 write(D/'generation-log.json',log)
 shutil.copy2(__file__,D/'prepare_review_boards.py')
 print(c['slug'],[(x['key'],x['selected']['sha256'],x['alpha_zero_nonzero_rgb_pixels'],x['margins_ltrb']) for x in checks])
