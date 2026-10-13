"""Read-only image SHA/dimension inspection; writes audit JSON only, never raster edits."""
import json,pathlib,hashlib
from PIL import Image
r=pathlib.Path(__file__).resolve().parents[2];b=r/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012';assets=[];errors=[]
for n in range(47,51):
 d=json.loads((b/f'batch{n}/manifest.json').read_text())
 for a in d['assets']:
  p=b/f'batch{n}'/a['filename'];im=Image.open(p)
  if hashlib.sha256(p.read_bytes()).hexdigest()!=a['sha256']:errors.append(str(p)+' SHA')
  if [im.width,im.height,im.mode]!=[a['width'],a['height'],a['mode']]:errors.append(str(p)+' dimensions')
  for key in ['source_sha256','reference_sha256']:
   for s,h in a[key].items():
    if hashlib.sha256((r/s).read_bytes()).hexdigest()!=h:errors.append(s+' source SHA')
  if not a['visual_reviewed']:errors.append(str(p)+' not visually reviewed')
  assets.append(dict(a,file=f'batch{n}/'+a['filename']))
old=json.loads((b/'coverage-audit-through-batch32.json').read_text());res=[]
for x in old['old_five_city_text_mapping_residuals']:
 row=dict(x);found=[a for a in assets if x['id'] in a['coverage']]
 if found:
  a=next((a for a in found if a.get('preferred')),found[-1]);row.update(status='distinct_function_review_draft_added',file=a['file'],reason='Old board and text compared; new image isolates previously missing function. Not native-ready.')
 elif x['id']=='BRY-D03-B':
  row.update(status='defer_duplicate_full_scene_shared_motif',file='design/12_美术参考/城市概念/BRY-任务场所-v2.png',panel='F',reason='Viewed old F: dry shore shelter, empty berth, preserved-board/rope motif already readable. D03 and S03 remain different locations; do not claim same geography. Exact berth-nail/withdrawal-knot/retained-name prop identification may merit a focused object detail only after checking existing 04 dock props.')
 elif x['id']=='YOS-D01-B':
  row.update(status='defer_duplicate_full_scene_shared_motif',file='design/12_美术参考/城市概念/YOS-任务场所-v2.png',panel='D',reason='Viewed old D: finite tied winter bundles/shelter and comparison table. D01 and S02 are different locations, not same geography. If care-promised bundle/household knot/sale-price distinction absent in older props, make a focused finite-allocation prop board, not another whole wool shelter.')
 else:
  row.update(status='not_yet_visually_audited_in_this_rotation',reason='DEN/MNS existing v2 boards must be viewed before deciding new assets; source and mapping paths retained.')
 res.append(row)
audit={'date':'2026-10-12','scope':'Batch47–50 and old five-city 22 residual mapping review; not global completion','png_total':len(list(b.glob('batch*/*.png'))),'new_png_count':len(assets),'new_base_concepts':13,'targeted_revision_count':2,'all_156_city_satellite_actor_cards_have_dedicated_review':True,'source_and_output_validation_errors':errors,'assets':assets,'old_five_city_residuals':res,'residual_counts':{'distinct_function_review_draft_added':sum(x['status']=='distinct_function_review_draft_added' for x in res),'defer_duplicate_full_scene_shared_motif':sum(x['status']=='defer_duplicate_full_scene_shared_motif' for x in res),'not_yet_visually_audited_in_this_rotation':sum(x['status']=='not_yet_visually_audited_in_this_rotation' for x in res)},'next_asset':188,'next_batch':51,'other_residual_scope':old['other_residual_scope'],'limits':['All are image_gen pixel-style concepts; exact native pixel grid, palette, animation anchors, collision and runtime unverified.','No story/runtime/csproj changes and no push.','Reference boards viewed before generation but not sent to generator; only 183/184 v2 used explicit image edit targets.','Source appearances remain proposals, not canon.']}
(b/'coverage-audit-through-batch50.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps({k:audit[k] for k in ['png_total','new_png_count','source_and_output_validation_errors','residual_counts']},ensure_ascii=False))
