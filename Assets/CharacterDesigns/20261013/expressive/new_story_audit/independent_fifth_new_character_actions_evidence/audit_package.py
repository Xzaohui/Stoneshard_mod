from pathlib import Path
import json,hashlib,zipfile,sys
from datetime import datetime,timezone
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');A=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
group=sys.argv[1];delivery=root/sys.argv[2];dm=json.loads(delivery.read_text());globalqa=json.loads((A/'independent_fifth_new_character_actions_20261014.json').read_text());errors=[];atts=[];zips=[]
passed={r['pose_version']:next(f for f in r['files'] if '/exports/' in f['path'])['sha256'] for r in globalqa['pose_reviews'] if r['verdict']=='pass'}
for att in dm['attachments']:
 p=root/att['path'];ok=p.is_file() and p.stat().st_size==att['bytes'] and sha(p)==att['sha256'];check={'path':att['path'],'bytes':p.stat().st_size,'sha256':sha(p),'matches_delivery_manifest':ok,'under_18_MiB':p.stat().st_size<18*1024*1024}
 if not ok:errors.append(['attachment_hash',att['path']])
 if not check['under_18_MiB']:errors.append(['attachment_oversize',att['path']])
 if p.suffix=='.png' and 'transparent' in att['kind']:
  check['matches_passed_visual_selected']=sha(p) in passed.values()
  if not check['matches_passed_visual_selected']:errors.append(['not_passed_selected',att['path']])
 atts.append(check)
 if p.suffix=='.zip':
  slug=att['character']; tree=root/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1';treefiles={str(f.relative_to(root)):f for f in tree.rglob('*') if f.is_file()};manifest=json.loads((tree/'manifest.json').read_text());inventory_name='manifest.json' if 'files' in manifest else 'FILES_SHA256.json'; inventory=manifest if 'files' in manifest else json.loads((tree/inventory_name).read_text());rows=inventory['files'];rows=[{'path':k,**v} for k,v in rows.items()] if isinstance(rows,dict) else rows; mf={r['path']:r for r in rows};expected={str(f.relative_to(tree)) for f in treefiles.values()}-{inventory_name};ze=[];members=[]
  if set(mf)!=expected:ze.append(['manifest_tree_set',sorted(expected-set(mf)),sorted(set(mf)-expected)])
  for n,r in mf.items():
   f=tree/n
   if not f.is_file() or f.stat().st_size!=r['bytes'] or sha(f)!=r['sha256']:ze.append(['manifest_file',n])
  with zipfile.ZipFile(p) as z:
   crc=z.testzip();names=[n for n in z.namelist() if not n.endswith('/')]
   # Accept either repository-relative paths or paths relative to the character tree root.
   if set(names)==set(treefiles): pairs={n:treefiles[n] for n in names}
   elif set(names)=={str(f.relative_to(tree)) for f in treefiles.values()}:pairs={n:tree/n for n in names}
   elif set(names)=={str(f.relative_to(tree.parent.parent)) for f in treefiles.values()}:pairs={n:tree.parent.parent/n for n in names}
   else:pairs={n:root/n for n in names};ze.append(['zip_tree_set','missing',sorted(set(treefiles)-set(names)),'extra',sorted(set(names)-set(treefiles))])
   if len(names)!=len(set(names)):ze.append(['duplicate_zip_names'])
   if crc:ze.append(['crc_error',crc])
   for n,f in pairs.items():
    b=z.read(n);s=hashlib.sha256(b).hexdigest();members.append({'member':n,'bytes':len(b),'sha256':s,'crc32':f'{z.getinfo(n).CRC:08x}'})
    if not f.is_file() or f.stat().st_size!=len(b) or sha(f)!=s:ze.append(['zip_bytes_vs_tree',n])
  sm=json.loads((tree/'sources/SOURCE_MANIFEST.json').read_text());sm=sm['files'] if isinstance(sm,dict) and 'files' in sm else sm
  for r in sm:
   for f in [root/r['path'],tree/r.get('snapshot_path',r.get('archive_path',''))]:
    if not f.is_file() or sha(f)!=r['sha256'] or f.stat().st_size!=r['bytes']:ze.append(['source_snapshot',str(f)])
  zips.append({'character':slug,'zip':att['path'],'zip_bytes':p.stat().st_size,'zip_sha256':sha(p),'members':len(members),'crc_all_pass':crc is None,'zip_tree_membership_and_bytes_sha_closed':not ze,'inventory_file':inventory_name,'inventory_covers_full_tree_except_itself':set(mf)==expected,'source_snapshots_and_unchanged_originals_verified':not any(x[0]=='source_snapshot' for x in ze),'errors':ze,'manifest_sha256':sha(tree/'manifest.json'),'final_status_sha256':sha(tree/'FINAL_STATUS.json') if (tree/'FINAL_STATUS.json').exists() else None,'member_fingerprints':members});errors+=ze
out={'status':'pass' if not errors else 'fail','reviewed_utc':datetime.now(timezone.utc).isoformat(),'group':group,'delivery_manifest':str(delivery.relative_to(root)),'delivery_manifest_sha256':sha(delivery),'attachments_checked':atts,'zips':zips,'errors':errors,'note':'Read-only package verification; reviewer changed only independent review files. No runtime, animation, upload or user acceptance claim.'};target=A/f'independent_fifth_new_character_actions_{group}_package_gate_20261014.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['zips']},ensure_ascii=False,indent=2));print([(z['character'],z['members'],z['zip_bytes'],z['errors']) for z in zips])
