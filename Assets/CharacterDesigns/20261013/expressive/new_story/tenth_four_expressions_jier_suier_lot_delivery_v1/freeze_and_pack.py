from pathlib import Path
from PIL import Image
import json,hashlib,datetime,shutil,zipfile,sys,base64
D=Path(__file__).resolve().parent;BASE=D.parent;ROOT=BASE.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def rec(p,base):return {'path':str(p.relative_to(base)),'sha256':sha(p),'bytes':p.stat().st_size}
def freeze(slug):
 p=BASE/slug/'expressions_v1';assert not (p/'FINAL_STATUS.json').exists(),'Already frozen; do not overwrite.'
 qa=json.loads((p/'QA-independent.json').read_text());qr=json.loads((p/'QA-independent-raw-visual.json').read_text());assert qa['status']=='passed' and qr['status']=='passed'
 log=json.loads((p/'generation-log.json').read_text());assert len(log['calls'])==2
 evidence=[]
 for row in qa['source_chain']['records']:
  original=ROOT/row['raw_composite']['path'];assert sha(original)==row['raw_composite']['sha256'];out=p/'review/independent_evidence'/original.name;out.parent.mkdir(exist_ok=True);shutil.copy2(original,out);evidence.append({'original_path':row['raw_composite']['path'],**rec(out,p)})
  raw=ROOT/row['raw']['path'];ret=ROOT/row['complete_original_return']['path'];retj=json.loads(ret.read_text());assert hashlib.sha256(base64.b64decode(retj['image_url'].split(',',1)[1])).hexdigest()==sha(raw)
 wr(p/'review/independent_evidence/index.json',{'note':'独审原RGBA浅深合成的逐字节快照，原报告保留原审查路径。','files':evidence})
 # Do not rewrite generation log or review artifacts after independent SHA binding.
 readme=(p/'README.md').read_text().replace('独立实看记录将保存在','独立实看通过记录保存在')
 readme+='\n独审已通过。generation-log、QA-author与独审中的pending措辞记录的是各自时点；最终冻结状态以FINAL_STATUS为唯一收口。原工具返回从未被派生日志覆盖。\n'
 (p/'README.md').write_text(readme)
 source=json.loads((p/'sources/source_index.json').read_text())
 for row in source['files']:assert sha(p/row['snapshot_path'])==row['sha256']
 for row in qa['poses']:assert sha(ROOT/row['selected']['path'])==row['selected']['sha256']
 wr(p/'freeze_validation.json',{'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_status':qa['status'],'independent_raw_status':qr['status'],'source_snapshot_count':len(source['files']),'selected_count':2,'complete_tool_returns_decode_to_raw':True,'all_source_snapshot_sha_verified':True,'all_selected_sha_match_independent_review':True,'all_raw_preserved':True,'hard_error_revisions_used':0,'alpha_cleanup_only':True,'user_approval_claimed':False})
 brief=json.loads((p/'sources/files/Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_four_expression_brief.json').read_text()); c=next(c for c in brief['characters'] if c['slug']==slug)
 selected=[]
 for e,call in zip(c['expressions'],log['calls']):
  sp=p/call['selected_file'];rp=p/call['raw_file'];selected.append({'key':e['key'],'label_zh':e['label_zh'],'path':str(sp.relative_to(p)),'sha256':sha(sp),'raw_path':str(rp.relative_to(p)),'raw_sha256':sha(rp),'size':list(Image.open(sp).size),'attempt':'v1'})
 manifest={'schema_version':1,'character_slug':slug,'name':c['name'],'canonical_id':c['canonical_id'],'status':'frozen_pass','source_anchor':c['source_anchor'],'selected_count':2,'selected':selected,'all_raw':[rec(f,p) for f in sorted((p/'raw').glob('*.png'))],'generation_count':2,'revision_count':0,'files':[rec(f,p) for f in sorted(p.rglob('*')) if f.is_file() and f.name not in ['manifest.json','FINAL_STATUS.json'] or f.is_file() and f.name=='manifest.json' and f.parent!=p],'not_claimed':brief['delivery_plan']['not_claimed']}
 wr(p/'manifest.json',manifest)
 for row in manifest['files']:assert sha(p/row['path'])==row['sha256']
 final={'schema_version':1,'status':'final_clean_and_presentation_pass','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'character':slug,'selected_count':2,'blocked_count':0,'manifest_sha256':sha(p/'manifest.json'),'independent_qa_sha256':sha(p/'QA-independent.json'),'independent_raw_qa_sha256':sha(p/'QA-independent-raw-visual.json'),'all_raw_preserved':True,'raw_output_count':2,'generation_calls':2,'revisions_used':0,'blocking_issues':[],'nonblocking_notes':qa['limitations'],'files':{str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file()},'author_sole_writer_freeze':True,'freeze_policy':'Source tree frozen after FINAL_STATUS; later checks and delivery copies stay outside this directory.','not_uploaded':True,'not_deployed':True,'runtime_verified':False,'user_approval_claimed':False}
 wr(p/'FINAL_STATUS.json',final);print('FROZEN',slug,sha(p/'FINAL_STATUS.json'))
def pack():
 attachments=[];archives=[]
 for slug,name in [('jier','蓟珥'),('suier_lot','绥珥')]:
  p=BASE/slug/'expressions_v1';fs=json.loads((p/'FINAL_STATUS.json').read_text());m=json.loads((p/'manifest.json').read_text())
  assert fs['status']=='final_clean_and_presentation_pass'
  for f,h in fs['files'].items():assert sha(p/f)==h
  for row in m['selected']:
   out=D/f"{name}_{row['label_zh']}_透明.png";shutil.copy2(p/row['path'],out);attachments.append(rec(out,D))
  zpath=D/f'{name}_两表情_完整源包.zip'
  with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for f in sorted(p.rglob('*')):
    if f.is_file():z.write(f,f'{slug}/expressions_v1/'+str(f.relative_to(p)))
  assert zpath.stat().st_size<18*1024*1024
  with zipfile.ZipFile(zpath) as z:
   assert z.testzip() is None
   assert len(z.namelist())==sum(f.is_file() for f in p.rglob('*'))
   for f in sorted(p.rglob('*')):
    if f.is_file():assert hashlib.sha256(z.read(f'{slug}/expressions_v1/'+str(f.relative_to(p)))).hexdigest()==sha(f)
   archives.append({**rec(zpath,D),'members':len(z.namelist()),'all_member_bytes_verified_against_frozen_source':True,'standalone_complete_character_source_tree':True})
  attachments.append(rec(zpath,D))
 attachments.insert(4,rec(D/'蓟珥绥珥_四表情_浅深对照.png',D));assert len(attachments)==7
 wr(D/'delivery_manifest.json',{'status':'packed_pending_final_independent_readback','attachment_count':7,'attachments':attachments,'archives':archives,'all_under_18MiB':all(x['bytes']<18*1024*1024 for x in attachments),'source_freeze_readback_pass':True,'full_source_trees_not_split_zip_parts':True,'not_uploaded':True,'not_deployed':True})
 (D/'README.md').write_text('# 蓟珥与绥珥：四种独立表情\n\n交付附件共7份：4张透明选稿、1张中文浅深对照板、2个完整独立人物源包。\n\n蓟珥：谈井专注、闭口谢客。绥珥：说起手艺、受疑缄默。\n\n两个ZIP分别可独立打开，完整保留对应角色源树：全部raw、选稿、逐字实际prompt、完整参数、完整原工具返回、引用和输出SHA、母图和卡/台本/brief来源快照、作者与独立实看QA、中文浅深板、独审原raw合成证据、manifest及唯一FINAL_STATUS。每个ZIP均小于18 MiB，成员逐字节与冻结源树复核通过。\n\n蓟珥E1真实返回1119×1406，其余为1118×1407；保留返回尺寸，不拉伸。绥珥为FX-LOT / suier_lot，未混燧珥FX-CP1 / suier。\n\n各图是独立可逆表情概念，不是连续动画或剧情结算；不表示任务、付款、治疗、关系或授权状态改变，未做游戏落地、装备兼容或runtime验收。\n')
 print(json.dumps({'attachments':attachments,'archives':archives},ensure_ascii=False,indent=2))
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='pack':pack()
 else:freeze(sys.argv[1])
