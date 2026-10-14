import json,hashlib,shutil,zipfile
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/CharacterDesigns/20261013/expressive/new_story';D=Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
attachments=[];audits=[];character_statuses=[]
for slug,name in [('suoda','索妲'),('kelin','珂琳')]:
 d=B/slug/'expressions_v1';f=json.loads((d/'FINAL_STATUS.json').read_text());m=json.loads((d/'manifest.json').read_text());assert f['status']=='final_clean_and_presentation_pass';assert sha(d/'manifest.json')==f['manifest_sha256'];assert len(m['selected'])==2
 for p,h in f['files'].items():assert sha(d/p)==h,(slug,p)
 q=json.loads((d/'QA-independent.json').read_text());reviewed={x['key']:x['selected']['sha256'] for x in q['poses']}
 for s in m['selected']:
  assert sha(d/s['path'])==s['sha256']==reviewed[s['key']];out=D/(name+'_'+s['key'].split('_')[1]+'_'+s['label_zh']+'_透明.png');shutil.copy2(d/s['path'],out);attachments.append({'kind':'selected_png','name':out.name,'path':str(out.relative_to(R)),'sha256':sha(out),'bytes':out.stat().st_size,'source':str((d/s['path']).relative_to(R))})
 zpath=D/(name+'_两种表情_完整源包.zip')
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(d.rglob('*')):
   if p.is_file():z.write(p,slug+'/expressions_v1/'+str(p.relative_to(d)))
 members=[]
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for p in sorted(d.rglob('*')):
   if p.is_file():
    n=slug+'/expressions_v1/'+str(p.relative_to(d));h=hashlib.sha256(z.read(n)).hexdigest();assert h==sha(p);members.append({'member':n,'sha256':h,'bytes':p.stat().st_size})
 assert zpath.stat().st_size<18*1024*1024
 attachments.append({'kind':'complete_source_zip','name':zpath.name,'path':str(zpath.relative_to(R)),'sha256':sha(zpath),'bytes':zpath.stat().st_size,'member_count':len(members),'scope':'One complete frozen character source tree, no members omitted.'});audits.append({'archive':zpath.name,'sha256':sha(zpath),'crc_pass':True,'all_members_match_frozen_source':True,'members':members});character_statuses.append({'slug':slug,'status_sha256':sha(d/'FINAL_STATUS.json'),'manifest_sha256':sha(d/'manifest.json')})
attachments=[x for x in attachments if x['kind']=='selected_png']+[x for x in attachments if x['kind']=='complete_source_zip']
board=Image.new('RGB',(2920,2320),'#ece7df')
for row,tag in enumerate(['light','dark']):
 for col,slug in enumerate(['suoda','kelin']):board.paste(Image.open(B/slug/'expressions_v1/review'/(slug+'_expressions_review_zh_'+tag+'.png')),(col*1460,row*1160))
bp=D/'索妲珂琳_四种表情_浅深合板.png';board.save(bp);attachments.insert(4,{'kind':'chinese_light_dark_board','name':bp.name,'path':str(bp.relative_to(R)),'sha256':sha(bp),'bytes':bp.stat().st_size,'size':list(board.size),'layout':'Top row light, bottom row dark. Left Suoda, right Kelin. Original Chinese review boards placed 1:1.'})
write(D/'zip_member_audit.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'archives':audits});write(D/'delivery.json',{'schema_version':1,'status':'packaged_pending_final_delivery_review','characters':character_statuses,'selected_count':4,'raw_count':4,'generation_calls':4,'revision_count':0,'attachments':attachments,'attachment_count':len(attachments),'all_source_archives_below_18_MiB':True,'source_archive_policy':'Two standalone ZIPs, each contains one complete character source tree including all raw, original returns, prompts, source snapshots, QA, manifest and FINAL_STATUS.','not_uploaded':True,'not_deployed':True,'runtime_verified':False})
(D/'README.md').write_text('# 索妲、珂琳 · 第十批四种表情\n\n交付附件共7个：4张独立透明PNG、1张中文浅深合板、2个完整源ZIP。索妲与珂琳各自源ZIP是完整独立目录，不是缺文件的预览包；所有raw、逐字prompt、工具参数、原返回、来源快照、QA、manifest与FINAL_STATUS均在对应包内。\n\n每表情仅生成首稿1次，共4次，无修订。作者与独审均实际看过母图、raw、透明和浅深底。冻结源树不再改写。\n\n仅为人物表情概念；不表示剧情、任务、配药、康复、动画、装备兼容或游戏运行通过。\n')
print(json.dumps({'attachments':[(a['name'],a['bytes'],a['sha256']) for a in attachments]},ensure_ascii=False,indent=2))
