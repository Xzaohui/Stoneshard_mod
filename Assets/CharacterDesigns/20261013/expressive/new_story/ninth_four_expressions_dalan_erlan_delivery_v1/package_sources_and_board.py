from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,zipfile,zlib,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=R/'Assets/CharacterDesigns/20261013/expressive/new_story';out=base/'ninth_four_expressions_dalan_erlan_delivery_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();items=[];freeze=[]
for slug,name in [('dalan','妲兰'),('erlan','珥兰')]:
 b=base/slug/'expressions_v1';m=json.loads((b/'manifest.json').read_text());f=json.loads((b/'FINAL_STATUS.json').read_text());assert sha(b/'manifest.json')==f['manifest_sha256']
 for p,h in f['files'].items():assert sha(b/p)==h
 freeze.append({'slug':slug,'manifest_path':str((b/'manifest.json').relative_to(R)),'manifest_sha256':sha(b/'manifest.json'),'final_status_path':str((b/'FINAL_STATUS.json').relative_to(R)),'final_status_sha256':sha(b/'FINAL_STATUS.json')})
 for i,e in enumerate(m['selected'],1):
  src=b/e['path'];dst=out/f'{name}_E{i}_{e["label_zh"]}_透明.png';shutil.copy2(src,dst);assert sha(src)==sha(dst)==e['sha256'];items.append({'character':slug,'name':name,'expression':f'E{i}','label_zh':e['label_zh'],'source':str(src.relative_to(R)),'path':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size})
board=Image.new('RGBA',(2400,2150),'#efeade');font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';draw=ImageDraw.Draw(board)
for row,(tag,bg,fg,sub) in enumerate([('浅底','#efeade','#292c2b','#625e54'),('深底','#23282e','#efe7d6','#b7b4ab')]):
 y=row*1075;draw.rectangle((0,y,2400,y+1074),fill=bg);draw.text((48,y+23),'妲兰与珥兰 · 四种表情 · '+tag,font=ImageFont.truetype(bold,42),fill=fg);draw.text((50,y+82),'各自独立、可逆的情绪提案；保留本人衣具与比例',font=ImageFont.truetype(font,25),fill=sub)
 for col,it in enumerate(items):
  im=Image.open(out/it['path']).convert('RGBA');bb=im.getchannel('A').getbbox();im=im.crop(bb);scale=min(520/im.width,825/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);board.alpha_composite(im,(col*600+(600-im.width)//2,y+190+825-im.height));draw.text((col*600+38,y+127),it['name']+' · '+it['expression']+' '+it['label_zh'],font=ImageFont.truetype(bold,27),fill=fg)
 draw.text((50,y+1032),'全身像素概念 · 不代表任务结果、关系变化或游戏运行',font=ImageFont.truetype(font,24),fill=sub)
bp=out/'妲兰珥兰_四种表情_浅深合板.png';board.convert('RGB').save(bp)
archives=[]
for slug,name in [('dalan','妲兰'),('erlan','珥兰')]:
 b=base/slug/'expressions_v1';files=[(p,slug+'/expressions_v1/'+str(p.relative_to(b))) for p in sorted(b.rglob('*')) if p.is_file()];audit=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_expression_independent_details';files += [(p,'independent_evidence/'+p.name) for p in sorted(audit.glob(slug+'_*')) if p.is_file()];files += [(audit/'baseline_source_verification.json','independent_evidence/baseline_source_verification.json')];zp=out/(name+'_两种表情_完整源包.zip')
 with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p,arc in files:z.write(p,arc)
 entries=[]
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  assert len(z.infolist())==len(files)
  for p,arc in files:
   raw=z.read(arc);zi=z.getinfo(arc);assert hashlib.sha256(raw).hexdigest()==sha(p);assert zlib.crc32(raw)&0xffffffff==zi.CRC;entries.append({'name':arc,'source_path':str(p.relative_to(R)),'sha256':sha(p),'bytes':len(raw),'crc32':f'{zi.CRC:08x}'})
 assert zp.stat().st_size<18*1024*1024
 archives.append({'character':slug,'path':zp.name,'sha256':sha(zp),'bytes':zp.stat().st_size,'mib':round(zp.stat().st_size/(1024**2),3),'member_count':len(entries),'all_members_exact_source_sha':True,'all_crc32_pass':True,'all_members':entries})
for f in freeze:
 assert sha(R/f['manifest_path'])==f['manifest_sha256'];assert sha(R/f['final_status_path'])==f['final_status_sha256']
record={'schema_version':1,'status':'author_packaged_pending_board_view_and_independent_delivery_review','created_utc':now,'selected_count':4,'selected':items,'review_board':{'path':bp.name,'sha256':sha(bp),'bytes':bp.stat().st_size,'dimensions':[2400,2150],'composition':'四列两行，同一透明原图浅深对照。展示层只裁去透明留白和等比nearest排版，不改变任何原图。','author_actually_viewed':False},'source_archives':archives,'source_freezes':freeze,'attachment_count':7,'not_uploaded':True,'not_committed':True,'not_deployed':True,'runtime_verified':False}
(out/'delivery.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');(out/'zip_member_audit.json').write_text(json.dumps({'created_utc':now,'archives':archives},ensure_ascii=False,indent=2)+'\n');(out/'README.md').write_text('# 妲兰与珥兰：四种表情\n\n交付附件共7份：4张透明选稿、1张中文浅深对照板、2个完整人物源包。\n\n妲兰：E1 闻夸蹙眉，E2 侧听警觉。\n珥兰：E1 谈猎稍缓，E2 冷拒撤陷。\n\n两源包完整保留冻结后的 raw、选稿、母图与来源快照、逐字实际 prompt、工具参数、完整返回、逐条 SHA、作者及独立视觉 QA、中文浅深板与终态记录，并附相应独审原图合成及冻结读回证据。每个包均小于18 MiB。\n\n各图是独立可逆美术提案，不表示任务、雇佣、人物关系或剧情结算；未做游戏落地或连续动画验收。珥兰E1生成画布为1070×1470，其余为1118×1407，保留原返回尺寸而不拉伸。\n')
print(json.dumps({'attachments':len(items)+1+len(archives),'archives':[{'path':a['path'],'mib':a['mib'],'members':a['member_count']} for a in archives],'board':str(bp),'delivery_sha256':sha(out/'delivery.json')},ensure_ascii=False,indent=2))
