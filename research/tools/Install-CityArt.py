"""Copy selected generated concept boards and catalogue originals; never edit pixels."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
results=json.loads((ROOT/'research/city-art-results.json').read_text(encoding='utf-8'))
briefs=json.loads((ROOT/'research/city-art-briefs.json').read_text(encoding='utf-8'))
bm={b['id']:b for b in briefs['briefs']};records=[]
additions=json.loads((ROOT/'research/city-art-prompt-additions.json').read_text(encoding='utf-8'))
cache=Path(r'C:\Users\83912\.codex\generated_images').resolve()
for r in results['records']:
 src=Path(r['source_path']).resolve();dst=(ROOT/r['output']).resolve()
 if not src.is_relative_to(cache) or not dst.is_relative_to(ROOT/'design/12_美术参考/城市概念'):raise SystemExit('Unexpected image path')
 h=hashlib.sha256(src.read_bytes()).hexdigest()
 if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest()!=h:raise SystemExit('Do not overwrite existing image: '+str(dst))
 dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists():shutil.copy2(src,dst)
 record=dict(**r,sha256=h,reference_paths=bm[r['id']]['reference_paths'],reference_hashes=bm[r['id']]['reference_hashes'],
   city_note=bm[r['id']]['city_note'],satellite_notes=bm[r['id']]['satellite_notes'],prompt_id=r['id'],
   initial_prompt_file='research/city-art-briefs.json',generation_tool='built-in image_gen.imagegen')
 record['actual_generation_reference_paths']=record['reference_paths']
 record['actual_generation_reference_hashes']=record['reference_hashes']
 if r.get('revised_prompt_id'):
  edit=additions['revisions'][r['revised_prompt_id']]
  record['actual_generation_reference_paths']=edit['reference_paths']
  record['actual_generation_reference_hashes']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in edit['reference_paths']}
  record['edit_prompt_file']='research/city-art-prompt-additions.json'
 if r.get('prompt_addition'):record['addition_prompt_file']='research/city-art-prompt-additions.json'
 records.append(record)
mp=ROOT/'research/city-art-manifest.json';m=json.loads(mp.read_text(encoding='utf-8'))
m['reference_based_boards']=records;m['prompt_set']='research/city-art-briefs.json';m['completed_boards']=len(records)
m['prompt_additions']='research/city-art-prompt-additions.json'
m['style_reference']='user stoneshard-assets-sample, inspected atlas-020/083/088/060/099; frame names/coordinates are design references, not official settlement layouts'
m['limitations']=['Concept boards are original proposed compositions based on the user-provided game style references, not canon geography.','No collision, layered room files, tilesets or gameplay validation.','Surrounding settlements appear as labelled vignettes in parent boards; they are not separate sprite exports.']
m['pending_boards']=[b['id'] for b in briefs['briefs'] if b['id'] not in {r['id'] for r in records}]
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(copied_or_verified=len(records),pending=m['pending_boards']),ensure_ascii=False))
