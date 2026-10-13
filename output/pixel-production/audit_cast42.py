import json,pathlib,hashlib,collections
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2];b=root/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012';old=json.loads((b/'coverage-cast-through-batch39.json').read_text());roster=old['roster'];ids={x['id'] for x in roster};matches={};errors=[];assets=[]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in sorted(b.glob('batch*/manifest.json'),key=lambda p:int(p.parent.name[5:])):
 for a in json.loads(p.read_text()).get('assets',[]):
  for raw in a.get('coverage',[]):
   k=raw.removeprefix('CHAR-')
   if k in ids:matches[k]=str(p.parent.relative_to(b)/a['filename'])
  if int(p.parent.name[5:]) not in (40,41,42):continue
  f=p.parent/a['filename']
  if h(f)!=a['sha256']:errors.append(str(f)+' SHA')
  with Image.open(f) as im:
   if im.size!=(a['width'],a['height']):errors.append(str(f)+' size')
  for key in ['source_sha256','reference_sha256']:
   for ref,sha in a[key].items():
    if h(root/ref)!=sha:errors.append(ref+' SHA')
  assets.append(dict(file=str(f.relative_to(b)),coverage=a['coverage'],sha256=a['sha256'],size=[a['width'],a['height']],qa=a['qa']))
for x in roster:
 if x['id'] in matches:x.update(status='dedicated-review-covered',file=matches[x['id']])
c=collections.Counter(x['status'] for x in roster)
d=dict(date='2026-10-12',scope=old['scope'],batch_images=len(assets),new_distinct_actor_ids=21,recovered_prior_coverage=['EED-NPC-SUJIN','EED-NPC-GELI'],png_total_at_audit=len(list(b.rglob('*.png'))),validation_errors=errors,assets=assets,roster=roster,counts=dict(cards=len(roster),dedicated_review_covered=c['dedicated-review-covered'],no_dedicated_image_recorded=c['no-dedicated-character-image-recorded']),caveats=old['caveats'])
(b/'coverage-cast-through-batch42.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(d['counts'],d['png_total_at_audit'],errors)
print('Remaining by region',collections.Counter(x['id'].split('-')[0] for x in roster if not x['file']))
