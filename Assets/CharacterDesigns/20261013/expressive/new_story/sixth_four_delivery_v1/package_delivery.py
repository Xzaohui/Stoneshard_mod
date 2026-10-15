from pathlib import Path
import json,hashlib,zipfile,datetime,shutil
O=Path(__file__).resolve().parent;R=O.parents[5];B=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
Q=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_visual_qa_sixth_four_20261013.json'
# QA must be final before packaging; hash recorded below
q=json.loads(Q.read_text());assert q['delivery_binding_status']=='all_four_final_clean_and_presentation_pass'
slugs=['erwei','chenger','weier','fouer'];characters=[]
for s in slugs:
 D=B/s/'concept_v1';M=D/'manifest.json';m=json.loads(M.read_text())
 entries=m.get('files',m.get('artifact_files'))
 if isinstance(entries,dict): entries=[dict(v,path=k) if isinstance(v,dict) else {'path':k,'sha256':v} for k,v in entries.items()]
 for f in entries:
  p=D/f['path'];assert sha(p)==f['sha256']
  if 'bytes' in f: assert p.stat().st_size==f['bytes']
 P=D/f'{s}_transparent.png';characters.append({'slug':s,'canonical_id':json.loads((D/'character_brief.json').read_text())['canonical_id'],'directory':str(D.relative_to(R)),'transparent':str(P.relative_to(R)),'transparent_sha256':sha(P),'frozen_manifest':str(M.relative_to(R)),'frozen_manifest_sha256':sha(M)})
status={'status':'all_four_final_concept_pass_ready_for_delivery','review':str(Q.relative_to(R)),'review_sha256':sha(Q),'characters':characters,'runtime':'unknown','equipment_compatibility':'unknown','user_delivery':'not_uploaded','notes':['Original raw files retained; all four selected transparent exports independently reviewed.','Low-alpha cleanup only; no anatomy scaling or scripted face drawing.','Overview display alone trims empty transparent margins and scales uniformly with nearest neighbor.','Erwei does not hold luggage or promise guidance; Chenger stays outside the cellar; Weier does not claim ownership; Fouer does not disclose any names or vouch for people.']}
(O/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
shutil.copyfile(Q,O/'independent_visual_qa_sixth_four_20261013.json')
brief=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/sixth_four_production_brief.json';shutil.copyfile(brief,O/'sixth_four_production_brief.json')
(O/'交付说明.md').write_text('# 新增剧情人物第六批交付\n\n珥薇 FX-RLY、埕珥 FX-GH2、苇珥 FX-HOM、缶珥 FX-CP5。\n\n四人均为新增原创人物外观概念，独审通过；旧人物资源与名单未改。四张透明选稿位于各自 concept_v1/ 下，全部 raw（含未选初稿）、提示、来源快照、制作脚本、作者QA、冻结manifest原样保留。联合终审与状态见本目录独审JSON与FINAL_STATUS.json。\n\n共享风格参考在各角色来源索引中登记；源包保留所有角色目录，不做隐式去重。概览仅裁透明空边并等比最近邻排版，不表示四人相对身高。\n\n仅作外观概念：不证明剧情结算、许可、照护承诺、退款、治疗、装备兼容、原版部件/帧表或游戏运行。\n')
common=[p for p in O.iterdir() if p.is_file() and p.suffix!='.zip' and p.name not in ('delivery.json','archive_inventory.json')]
def make_zip(name,ss):
 zpath=O/name
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for s in ss:
   for p in sorted((B/s/'concept_v1').rglob('*')):
    if p.is_file():z.write(p,str(p.relative_to(B)))
  for p in common:z.write(p,'delivery/'+p.name)
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  entries=[{'path':i.filename,'bytes':i.file_size} for i in z.infolist()]
 return zpath,entries
z,entries=make_zip('新增剧情人物_第六批完整源包.zip',slugs)
if z.stat().st_size>=18*1024*1024:
 # The single combined trial is not a deliverable; retain it outside the repository.
 shutil.move(z,Path('/tmp')/'sixth_four_combined_oversize.zip')
 pairs=[make_zip('新增剧情人物_珥薇埕珥源包.zip',slugs[:2]),make_zip('新增剧情人物_苇珥缶珥源包.zip',slugs[2:])]
else:pairs=[(z,entries)]
archives=[]
for z,entries in pairs:
 assert z.stat().st_size<18*1024*1024
 archives.append({'path':str(z.relative_to(R)),'sha256':sha(z),'bytes':z.stat().st_size,'entry_count':len(entries)})
(O/'archive_inventory.json').write_text(json.dumps([{'archive':z.name,'entries':e} for z,e in pairs],ensure_ascii=False,indent=2))
overview=O/'第六批四人_中文概览.png'
delivery={'status':'ready_not_uploaded','characters':characters,'overview':{'path':str(overview.relative_to(R)),'sha256':sha(overview),'bytes':overview.stat().st_size},'archives':archives,'independent_qa':{'path':str(Q.relative_to(R)),'sha256':sha(Q)},'final_status':str((O/'FINAL_STATUS.json').relative_to(R)),'manifest_files_unchanged':True,'zip_integrity':'testzip pass','packaging_only':True}
(O/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2))
print(json.dumps(delivery,ensure_ascii=False,indent=2))
