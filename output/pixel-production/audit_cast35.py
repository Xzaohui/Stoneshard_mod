import pathlib,json,re,hashlib
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2];b=root/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];assets=[]
for n in range(33,36):
 p=b/f'batch{n}/manifest.json';d=json.loads(p.read_text())
 for x in d['assets']:
  f=p.parent/x['filename']
  if h(f)!=x['sha256']:errors.append(str(f))
  with Image.open(f) as im:
   if [im.width,im.height,im.mode]!=[x['width'],x['height'],x['mode']]:errors.append('dimensions '+str(f))
  for key in ['source_sha256','reference_sha256']:
   for name,digest in x[key].items():
    if h(root/name)!=digest:errors.append('source '+name)
  if not x['visual_reviewed']:errors.append('QA '+str(f))
  assets.append({'file':str(f.relative_to(b)),'coverage':x['coverage'],'sha256':x['sha256'],'size':[x['width'],x['height']],'qa':x['qa']})
coverage={}
for x in assets:
 for cid in x['coverage']:coverage[cid.removeprefix('CHAR-')]=x['file']
# Explicit existing dedicated character mapping, checked against filenames and previous manifests.
old={
'BRY-NPC-SELA':'batch01/01_sela_turnaround.png','BRY-NPC-YANI':'batch01/02_yani_dialogue_poses.png','BRY-NPC-ROAN':'batch02/06_roan_four_views.png','BRY-NPC-MARIS':'batch02/07_maris_four_views.png','BRY-NPC-ELEN':'batch03/11_elen_four_views.png','BRY-NPC-DARAN':'batch03/12_daran_four_views.png','BRY-NPC-SEV':'batch04/16_sev_four_views.png','BRY-NPC-MIRO':'batch04/19_miro_rena_character_pair.png','BRY-NPC-RENA':'batch04/19_miro_rena_character_pair.png','MAE-NPC-KAEM':'batch09/41_sena_kaem_lyd_cast.png','NPC-SENA':'batch09/41_sena_kaem_lyd_cast.png','NPC-LYD':'batch09/41_sena_kaem_lyd_cast.png','NPC-REY':'batch10/46_leo_moren_aren_cast.png','NPC-MORREN':'batch10/46_leo_moren_aren_cast.png','NPC-MIA':'batch11/51_mia_caregiver_cast.png','NPC-MAYA':'batch20/86_maya_he_character_four_poses.png','NPC-HERS':'batch32/124_hers_white_debt_controller_cast.png','HIG-NPC-ARO':'batch32/125_aro_map_keeper_cast.png','ALD-S02-NPC':'batch19/82_ald_fenko_sore_character_review.png','ALD-NPC-SORE':'batch19/82_ald_fenko_sore_character_review.png'}
for k,v in old.items():assert (b/v).exists();coverage[k]=v
roster=[]
for folder in ['城市人物','聚落人物']:
 for p in sorted((root/'design/04_人物'/folder).glob('*.md')):
  txt=p.read_text();name=p.stem.split('_',2)[2];cid=p.stem.split('_',2)[1]
  work=re.search(r'\*\*(?:日常工作|工作)\*\*[：:]\s*([^\r\n]+)',txt)
  if not work:work=re.search(r'\*\*工作\*\*[：:]\s*([^\r\n]+)',txt)
  roster.append({'id':cid,'name':name,'source':str(p.relative_to(root)),'source_sha256':h(p),'role':work.group(1) if work else None,'status':'dedicated-review-covered' if cid in coverage else 'no-dedicated-character-image-recorded','file':coverage.get(cid)})
result={'date':'2026-10-12','scope':'City and satellite character cards only; no claim that other actor/card types or scene/animation gaps are exhausted','batch_images':len(assets),'new_distinct_actor_ids':len({c for x in assets for c in x['coverage']}),'png_total_at_audit':len(list(b.glob('batch*/*.png'))),'validation_errors':errors,'assets':assets,'roster':roster,'counts':{'cards':len(roster),'dedicated_review_covered':sum(x['file'] is not None for x in roster),'no_dedicated_image_recorded':sum(x['file'] is None for x in roster)},'caveats':['Appearance remains proposal, not narrative canon.','Image board has independent views, not multiple simultaneous bodies or an executed quest outcome.','No exact native grid/palette/pivot/runtime or animation verification.','Scene crowds do not count as dedicated character art.']}
(b/'coverage-cast-through-batch35.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['batch_images','new_distinct_actor_ids','png_total_at_audit','validation_errors','counts']},ensure_ascii=False))
for city in ['BRY','ALD','MAE','PAS','ASH','HIG']:
 print(city,[(x['id'],x['name']) for x in roster if x['id'].startswith(city) and not x['file']])
