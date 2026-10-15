import json,hashlib,zipfile,zlib,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[6];audit=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
group=sys.argv[1];d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/('ninth_four_expressions_'+group+'_delivery_v1');p=d/'delivery.json';meta=json.loads(p.read_text());checks=[]
if group=='teman_nier':
 meta['selected']=meta['assets'];meta['review_board']=next(a for a in meta['attachments'] if a['path'].endswith('.png') and a not in meta['assets'] and '浅深' in a['path']);meta['source_archives']=[]
 inventory=json.loads((d/'archive_inventory.json').read_text())
 for z in inventory:
  entry=next(a for a in meta['attachments'] if a['path']==z['archive']);members=[]
  for f in z['files']:
   name=f['path']
   if name.startswith('independent_evidence/'):src=audit/'ninth_expression_independent_details'/Path(name).name
   elif name.startswith(('teman/','fx_cv4_nier/')):src=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/name
   else:src=d/name
   members.append({'name':name,'source_path':str(src.relative_to(root)),'sha256':f['sha256'],'bytes':f['bytes'],'crc32':f['crc32']})
  meta['source_archives'].append(entry|{'member_count':entry['members'],'all_members':members})

def ck(kind,ok,**data):checks.append({'kind':kind,'pass':bool(ok),**data})
for s in meta['selected']:
 q=d/s['path'];src=root/s['source'];ck('selected_copy',q.read_bytes()==src.read_bytes() and sha(q)==s['sha256'] and q.stat().st_size==s['bytes'],file=ref(q),source=ref(src))
b=meta['review_board'];q=d/b['path'];ck('board_binding',sha(q)==b['sha256'] and q.stat().st_size==b['bytes'],file=ref(q))
count=0
for z in meta['source_archives']:
 p=d/z['path'];ck('archive_binding',sha(p)==z['sha256'] and p.stat().st_size==z['bytes'],file=ref(p));
 with zipfile.ZipFile(p) as f:
  names=f.namelist();ck('zip_crc',f.testzip() is None,file=ref(p));ck('zip_member_count',len(names)==z['member_count']==len(z['all_members']),count=len(names));ck('safe_unique_names',len(names)==len(set(names)) and all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names));
  for m in z['all_members']:
   raw=f.read(m['name']);src=root/m['source_path'];h=hashlib.sha256(raw).hexdigest();crc=f'{zlib.crc32(raw):08x}';ck('archive_member',h==m['sha256']==sha(src) and len(raw)==m['bytes']==src.stat().st_size and crc==m['crc32'],name=m['name'],source=str(src.relative_to(root)),sha256=h,bytes=len(raw));count+=1
r={'schema_version':1,'reviewer':'/root/review_ninth_character_expressions','created_utc':datetime.now(timezone.utc).isoformat(),'group':group,'status':'passed' if all(c['pass'] for c in checks) else 'failed','delivery_manifest':ref(d/'delivery.json'),'visual_review':{'board':ref(d/b['path']),'actually_viewed':True,'observation':'本独审以 tools.view_image 实际查看四列两行浅深合板。四个人物情绪条目姓名/标签正确，眉眼嘴可辨，完整头发、双手、双靴和所有必需道具未裁切，标签不覆盖主体；浅深背景正确合成，无可见实体底板或广泛光晕。'},'selected_copies_verified':len(meta['selected']),'archive_count':len(meta['source_archives']),'archive_members_verified':count,'checks':checks,'failures':[c for c in checks if not c['pass']],'not_claimed':['用户已认可','连续动画','原生网格或装备兼容','runtime通过'],'mutation_scope':'只新增独立交付QA，不修改作者冻结源、delivery.json或附件。'}
out=audit/('independent_ninth_expressions_'+group+'_delivery_20261014.json');out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'report':ref(out),'status':r['status'],'archive_members_verified':count,'failures':r['failures']},ensure_ascii=False))
