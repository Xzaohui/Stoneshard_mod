import json,pathlib,hashlib
from PIL import Image
r=pathlib.Path(__file__).resolve().parents[2];b=r/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012';d=json.load(open(b/'coverage-cast-through-batch35.json'));a=[];errors=[];new=set()
for n in range(36,40):
 for x in json.load(open(b/f'batch{n}/manifest.json'))['assets']:
  p=pathlib.Path(x['saved_file']);im=Image.open(p)
  if hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append([x['filename'],'output SHA'])
  if [im.width,im.height]!=[x['width'],x['height']]:errors.append([x['filename'],'size'])
  for field in ['source_sha256','reference_sha256']:
   for s,h in x[field].items():
    if hashlib.sha256((r/s).read_bytes()).hexdigest()!=h:errors.append([x['filename'],field,s])
  if not x['visual_reviewed'] or not x.get('qa'):errors.append([x['filename'],'missing QA'])
  for id in x['coverage']:
   id=id.removeprefix('CHAR-');match=[z for z in d['roster'] if z['id']==id]
   if len(match)!=1:errors.append([id,'missing or ambiguous roster'])
   else:
    z=match[0]
    if z['status']=='dedicated-review-covered':errors.append([id,'duplicate coverage'])
    z.update(status='dedicated-review-covered',file=f'batch{n}/'+x['filename']);new.add(id)
  a.append({'file':f'batch{n}/'+x['filename'],'coverage':x['coverage'],'sha256':x['sha256'],'size':[x['width'],x['height']],'qa':x['qa']})
d.update(batch_images=len(a),new_distinct_actor_ids=len(new),png_total_at_audit=len(list(b.rglob('*.png'))),validation_errors=errors,assets=a)
d['counts']={'cards':len(d['roster']),'dedicated_review_covered':sum(z['status']=='dedicated-review-covered' for z in d['roster']),'no_dedicated_image_recorded':sum(z['status']!='dedicated-review-covered' for z in d['roster'])}
(b/'coverage-cast-through-batch39.json').write_text(json.dumps(d,ensure_ascii=False,indent=2));print(json.dumps({k:d[k] for k in ['batch_images','new_distinct_actor_ids','png_total_at_audit','validation_errors','counts']},ensure_ascii=False))
print('Remaining by region:')
from collections import Counter
print(Counter(z['id'].split('-')[0] for z in d['roster'] if z['status']!='dedicated-review-covered'))
