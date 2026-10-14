from pathlib import Path
import json,hashlib,datetime,shutil,zipfile
R=Path.cwd(); B=R/'Assets/CharacterDesigns/20261013/expressive'; D=B/'new_story/eleventh_four_expressions_weier_ink_moer_delivery_v1'; J=json.loads((B/'new_story_audit/eleventh_four_expression_brief.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
freeze_summaries=[];attachments=[];zip_checks=[]
for c in J['characters'][:2]:
 d=B/'new_story'/c['slug']/'expressions_v1'; assert not (d/'FINAL_STATUS.json').exists(),'Already frozen; do not mutate'
 for n in ['QA-independent-raw-visual.json','QA-independent.json']:
  assert (d/n).exists(),'Missing independent QA: '+str(d/n)
  qa=json.loads((d/n).read_text());print(c['slug'],n,qa.get('status'))
  assert 'pass' in qa.get('status','').lower(),'Independent QA not PASS'
 logs=json.loads((d/'generation-log.json').read_text())['entries']
 for l in logs:
  assert sha(d/l['raw'])==l['raw_sha256'] and sha(d/l['selected'])==l['selected_sha256']
  assert sha(d/l['original_tool_return'])==l['original_tool_return_sha256']
  args=json.loads((d/l['parameters_path']).read_text());assert (d/l['prompt_path']).read_text()==args['prompt']
 source=json.loads((d/'sources/source_index.json').read_text())
 assert all(sha(R/x['original_path'])==x['sha256']==sha(d/x['snapshot_path']) for x in source['files'])
 manifest={'schema_version':1,'character_slug':c['slug'],'canonical_id':c['canonical_id'],'name':c['name'],'status':'frozen_pass','selected_count':2,'generation_count':2,'revision_count':0,'source_anchor':c['source_anchor'],'selected':[{'key':l['expression'],'label_zh':l['label_zh'],'path':l['selected'],'sha256':l['selected_sha256'],'raw_path':l['raw'],'raw_sha256':l['raw_sha256'],'size':l['technical']['size'],'attempt':'initial'} for l in logs],'all_raw':[{'path':l['raw'],'sha256':l['raw_sha256'],'bytes':(d/l['raw']).stat().st_size} for l in logs],'files':[{'path':str(p.relative_to(d)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(d.rglob('*')) if p.is_file() and p.name not in ['FINAL_STATUS.json'] and p!=d/'manifest.json'],'runtime_verified':False,'user_approval_claimed':False,'tool_returns_preserved':True}
 save(d/'manifest.json',manifest)
 status={'schema_version':1,'status':'final_clean_and_presentation_pass','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'character':c['slug'],'canonical_id':c['canonical_id'],'selected_count':2,'blocked_count':0,'manifest_sha256':sha(d/'manifest.json'),'independent_qa_sha256':sha(d/'QA-independent.json'),'independent_raw_qa_sha256':sha(d/'QA-independent-raw-visual.json'),'all_raw_preserved':True,'raw_output_count':2,'generation_calls':2,'revisions_used':0,'blocking_issues':[],'files':{str(p.relative_to(d)):sha(p) for p in sorted(d.rglob('*')) if p.is_file() and p.name!='FINAL_STATUS.json'},'author_sole_writer_freeze':True,'freeze_policy':'Source tree frozen after FINAL_STATUS; later checks and delivery copies remain outside this directory.','not_uploaded':True,'not_deployed':True,'runtime_verified':False,'user_approval_claimed':False}
 save(d/'FINAL_STATUS.json',status)
 assert all(sha(d/p)==s for p,s in status['files'].items());assert all(sha(d/x['path'])==x['sha256'] for x in manifest['files'])
 freeze_summaries.append({'character':c['slug'],'FINAL_STATUS_sha256':sha(d/'FINAL_STATUS.json'),'manifest_sha256':sha(d/'manifest.json'),'files_verified':len(status['files'])})
 for l in logs:
  dst=D/(c['name']+'_'+l['label_zh']+'.png');shutil.copyfile(d/l['selected'],dst);assert sha(dst)==l['selected_sha256'];attachments.append({'path':str(dst.relative_to(R)),'sha256':sha(dst),'bytes':dst.stat().st_size,'type':'selected_png'})
 z=D/(c['name']+'_两表情完整源包.zip')
 with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
  for p in sorted(d.rglob('*')):
   if p.is_file():out.write(p,arcname=c['slug']+'/expressions_v1/'+str(p.relative_to(d)))
  # Common delivery image included to retain exact review artifact in each independent package.
  out.write(D/'韦珥摩珥_四表情_中文浅深合板.png',arcname='delivery/韦珥摩珥_四表情_中文浅深合板.png')
 assert z.stat().st_size<18*1024*1024
 with zipfile.ZipFile(z) as check:
  assert check.testzip() is None
  source_files=[p for p in d.rglob('*') if p.is_file()]
  for p in source_files:
   n=c['slug']+'/expressions_v1/'+str(p.relative_to(d));assert hashlib.sha256(check.read(n)).hexdigest()==sha(p)
  zip_checks.append({'zip':z.name,'member_count':len(check.infolist()),'source_files_verified':len(source_files),'all_source_files_byte_identical':True,'crc_pass':True,'sha256':sha(z),'bytes':z.stat().st_size})
 attachments.append({'path':str(z.relative_to(R)),'sha256':sha(z),'bytes':z.stat().st_size,'type':'complete_source_zip','character':c['slug']})
board=D/'韦珥摩珥_四表情_中文浅深合板.png';attachments.append({'path':str(board.relative_to(R)),'sha256':sha(board),'bytes':board.stat().st_size,'type':'combined_chinese_light_dark_board'})
assert len(attachments)==7
attachments=[a for a in attachments if a['type']=='selected_png']+[a for a in attachments if a['type']=='combined_chinese_light_dark_board']+[a for a in attachments if a['type']=='complete_source_zip']
save(D/'delivery_manifest.json',{'status':'packaged_awaiting_final_delivery_readback','characters':['weier_ink','moer'],'selected_count':4,'generation_calls':4,'revision_calls':0,'attachments':attachments,'source_archives':'两个独立完整源ZIP，分别为韦珥与摩珥；每包包含该人整个冻结expressions_v1源树及相同中文浅深合板，不是分卷压缩，无需合并才能解压。','freeze_checks':freeze_summaries,'zip_checks':zip_checks,'not_uploaded':True,'runtime_verified':False})
(D/'README_交付说明.md').write_text('# 韦珥、摩珥四表情交付\n\n4张透明PNG、1张中文浅深合板、2个独立完整源ZIP，共7附件。\n\n韦珥：待客询问／围城收声。摩珥：旧账自嘲／免账正色。每张首稿通过，0次修订。\n\n两个ZIP分别保存一人的完整冻结expressions_v1源树，含所有原始raw、逐字prompt、实际参数、完整原tool返回、输入来源、作者与独审、manifest、FINAL_STATUS；均可单独解压。重复合板仅为展示核验，不作该角色额外表情计数。\n\n这批是静态、可逆表情概念；不代表任务结算、连续动画、装备兼容或游戏运行通过。未上传、未部署。\n')
print(json.dumps({'attachments':attachments,'freeze_checks':freeze_summaries,'zip_checks':zip_checks},ensure_ascii=False,indent=2))
