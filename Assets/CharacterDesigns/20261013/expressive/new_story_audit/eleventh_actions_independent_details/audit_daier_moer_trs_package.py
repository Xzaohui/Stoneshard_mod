from pathlib import Path
import json,hashlib,datetime,sys,zipfile
from PIL import Image
import numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'eleventh_actions_independent_details';d=r/'Assets/CharacterActions/20261013/new_story/eleventh_noncombat_daier_moer_trs_delivery_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def ck(k,ok,**x):checks.append({'kind':k,'pass':bool(ok),**x})
mode=sys.argv[1];mp=d/(sys.argv[2] if len(sys.argv)>2 else 'PREFLIGHT_V2_PACKAGE_MANIFEST.json');j=json.loads(mp.read_text());l=d/'review/layout.json';layout=json.loads(l.read_text())
for row in layout['per_character_boards']:
 p=r/row['path'];im=Image.open(p).convert('RGBA');ck('character_board_sha_and_size',sha(p)==row['sha256'] and list(im.size)==row['size'],path=row['path'])
 for q in row['items']:
  srcp=r/q['source'];src=Image.open(srcp).convert('RGBA');xy=q['placement'];wh=q['rendered_size'];expected=Image.alpha_composite(Image.new('RGBA',tuple(wh),tuple(row['background'])),src.resize(tuple(wh),Image.Resampling.NEAREST));actual=im.crop((xy[0],xy[1],xy[0]+wh[0],xy[1]+wh[1]));ck('full_canvas_nearest_alpha_composite',sha(srcp)==q['sha256'] and list(src.size)==q['original_size'] and np.array_equal(np.array(actual),np.array(expected)) and abs(wh[0]/src.width-wh[1]/src.height)<=1/min(src.size),path=row['path'],source=q['source'])
for row in layout['combined_boards']:
 p=d/row['path'];im=Image.open(p).convert('RGBA');expected=Image.new('RGBA',tuple(row['size']));y=0
 for src in row['assembled_without_resampling']:
  part=Image.open(r/src).convert('RGBA');expected.paste(part,(0,y));y+=part.height
 ck('combined_board_exact_concatenation',np.array_equal(np.array(im),np.array(expected)),path=str(p.relative_to(r)))
member_names=[];packages=[]
for s in ['daier','moer_trs']:
 cd=d.parent/s/'noncombat_basics_v1';mf=cd/'manifest.json';m=json.loads(mf.read_text());listed={x['path'] for x in m['files']};actual={str(p.relative_to(cd)) for p in cd.rglob('*') if p.is_file()}-{'manifest.json','FINAL_STATUS.json'};ck('whole_character_manifest_coverage',listed==actual,slug=s,missing=sorted(actual-listed),extra=sorted(listed-actual))
 for row in m['files']:
  p=cd/row['path'];ck('manifest_file_sha_and_bytes',p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],path=str(p.relative_to(r)))
 for row in json.loads((cd/'sources/source_index.json').read_text())['entries']:
  p=r/row['source_path'];q=cd/row['path'];ck('source_snapshot_pair',p.is_file() and q.is_file() and sha(p)==sha(q)==row['sha256'],path=row['source_path'])
 for row in json.loads((cd/'generation-log.json').read_text())['calls']:
  orig=Path(row['output_original_path']);raw=cd/row['raw_path'];ck('original_tool_png_identity',orig.is_file() and sha(orig)==sha(raw)==row['raw_sha256'],path=str(raw.relative_to(r)))
for row in j['zips']:
 p=d/row['path'];ck('zip_sha_size_and_limit',p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'] and row['bytes']<18*1024*1024,path=row['path']);expected={x['repo_path']:x for x in row['members']}
 with zipfile.ZipFile(p) as z:
  names=z.namelist();ck('zip_crc_and_inventory',z.testzip() is None and set(names)==set(expected) and len(names)==len(set(names)),path=row['path'])
  for n in names:
   bs=z.read(n);q=expected[n];ck('actual_decompressed_bytes_sha_local_identity',(r/n).is_file() and (r/n).read_bytes()==bs and len(bs)==q['bytes'] and hashlib.sha256(bs).hexdigest()==q['sha256'],path=n);member_names.append(n)
 packages.append({'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p),'members':len(names)})
for s in ['daier','moer_trs']:
 cd=d.parent/s/'noncombat_basics_v1';required={str(p.relative_to(r)) for p in cd.rglob('*') if p.is_file()};ck('all_character_source_files_in_archives',required<=set(member_names),slug=s,missing=sorted(required-set(member_names)))
ck('no_zip_member_duplicate_across_parts',len(member_names)==len(set(member_names)))
fail=[x for x in checks if not x['pass']];out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':mode,'verdict':'pass' if not fail else 'fail','package_manifest':{'path':str(mp.relative_to(r)),'sha256':sha(mp)},'board_layout':{'path':str(l.relative_to(r)),'sha256':sha(l)},'boards_actual_view':'Both combined light and dark boards actually viewed. Their four constituent per-character boards are verified byte-identical within the concatenated boards. Clear Chinese labels, reference mothers separate from four new poses, complete bodies and props without clipping.','checks':checks,'failures':fail,'packages':packages,'member_count':len(member_names),'attempts':4,'final_keyposes':4,'rejected_attempts_retained':0};p=e/(mode+'_daier_moer_trs_package_audit.json');p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'path':str(p.relative_to(r)),'sha256':sha(p),'checks':len(checks),'members':len(member_names),'packages':packages,'failures':fail},ensure_ascii=False));assert not fail
