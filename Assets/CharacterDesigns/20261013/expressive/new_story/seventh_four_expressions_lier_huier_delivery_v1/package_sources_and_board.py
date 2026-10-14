from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,datetime,zipfile,zlib
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=R/'Assets/CharacterDesigns/20261013/expressive/new_story';out=base/'seventh_four_expressions_lier_huier_delivery_v1';out.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();data=[];roots={};now=datetime.datetime.now(datetime.timezone.utc).isoformat();brief=json.loads((R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/seventh_four_expression_brief.json').read_text());names={'lier':'栎珥','huier':'洄珥'}
for s in names:
 D=base/s/'expressions_v1';f=json.loads((D/'FINAL_STATUS.json').read_text());assert f['status']=='final_frozen_concept_expression_pass';roots[s]={str(p.relative_to(D)):sha(p) for p in sorted(D.rglob('*')) if p.is_file()}
 for e in f['selected']:
  p=D/e['path'];target=out/p.name;assert sha(p)==e['sha256'];shutil.copy2(p,target);data.append({'character':s,'name':names[s],'expression':e['expression'],'label_zh':e['label_zh'],'source':str(p.relative_to(R)),'path':p.name,'sha256':sha(target),'bytes':target.stat().st_size})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',30);title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',44);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
board=Image.new('RGB',(2400,1860),'#eee6d3');dr=ImageDraw.Draw(board);dr.rectangle((0,945,2400,1860),fill='#1f232a');dr.text((45,25),'栎珥 · 洄珥｜四种表情 · 浅深对照',font=title,fill='#2a241f');dr.text((45,88),'两人各两张全身透明概念；独立表情可逆，不代表任务完成或剧情结局',font=small,fill='#554e43')
for row in range(2):
 ink='#2a241f' if row==0 else '#eee6d3';labely=142 if row==0 else 980;iy=195 if row==0 else 1033
 for i,e in enumerate(data):
  dr.text((i*600+35,labely),e['name']+'｜'+e['label_zh'],font=font,fill=ink);im=Image.open(out/e['path']).convert('RGBA');im.thumbnail((550,700),Image.Resampling.NEAREST);board.paste(im,(i*600+(600-im.width)//2,iy+(700-im.height)//2),im)
 dr.text((45,909 if row==0 else 1815),'透明原图与完整来源另附｜游戏网格、装备、动画及实际运行未验证',font=small,fill=ink)
bp=out/'栎珥_洄珥_四种表情_浅深对照.png';board.save(bp)
archives=[]
for s in names:
 D=base/s/'expressions_v1';zp=out/f'{names[s]}_两种表情_完整源包.zip'
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for rel in roots[s]:z.write(D/rel,f'{s}/expressions_v1/{rel}')
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None;members=[];expected={f'{s}/expressions_v1/{rel}' for rel in roots[s]};assert set(z.namelist())==expected and len(z.namelist())==len(expected)
  for info in z.infolist():
   raw=z.read(info.filename);rel=info.filename.split('/expressions_v1/',1)[1];h=hashlib.sha256(raw).hexdigest();assert h==roots[s][rel];assert (zlib.crc32(raw)&0xffffffff)==info.CRC;members.append({'name':info.filename,'sha256':h,'bytes':len(raw),'crc32':f'{info.CRC:08x}'})
 assert zp.stat().st_size<18*1024*1024
 assert roots[s]=={str(p.relative_to(D)):sha(p) for p in sorted(D.rglob('*')) if p.is_file()}
 archives.append({'character':s,'path':zp.name,'sha256':sha(zp),'bytes':zp.stat().st_size,'mib':round(zp.stat().st_size/1048576,3),'member_count':len(members),'all_members_exact_source_sha':True,'all_crc32_pass':True,'all_members':members})
entry={'schema_version':1,'status':'packaged_waiting_delivery_board_visual_and_independent_readback','created_utc':now,'selected_count':4,'selected':data,'review_board':{'path':bp.name,'sha256':sha(bp),'bytes':bp.stat().st_size,'dimensions':[2400,1860],'composition':'四列两行，同一透明原图浅深对照；仅展示板等比nearest缩放，不改变原图。'},'source_archives':archives,'source_final_status':[{'path':str((base/s/'expressions_v1/FINAL_STATUS.json').relative_to(R)),'sha256':sha(base/s/'expressions_v1/FINAL_STATUS.json')} for s in names],'source_files_unchanged_after_packaging':True,'uploaded':False,'git_committed':False,'runtime_verified':False}
(out/'delivery.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n');(out/'INDEX.md').write_text('# 栎珥 · 洄珥｜第七批表情交付\n\n4张独审通过的透明全身概念、1张中文浅深对照、2份完整源包。\n\n- 栎珥：笑谈树龄、谈水敛笑\n- 洄珥：忧看雨势、闻响警觉\n\n源包保留原始输出、实际prompt与参数、完整原返回、母图及文字来源快照、作者QA、独审、冻结清单与最终状态。每包均小于18 MiB，全部ZIP成员已与冻结源文件逐SHA及CRC核对。\n\n选稿与原始工具PNG逐字节相同，原RGBA及alpha0隐藏RGB保留；浅深合成未见可见污染。对照板仅作等比nearest展示排版。\n\n每图为可逆演出提案，不代表任务完成、关系变化或永久身份。原生像素网格、部件遮罩锚点、装备动画与游戏运行未验证。本次本地封包尚未上传或git提交。\n',encoding='utf-8');shutil.copy2(__file__,out/'package_sources_and_board.py');print(out);print([(a['path'],a['mib'],a['member_count']) for a in archives])
