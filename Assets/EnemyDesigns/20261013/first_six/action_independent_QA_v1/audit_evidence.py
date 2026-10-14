from pathlib import Path
from PIL import Image
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'Assets/EnemyDesigns/20261013/first_six'
OUT=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]; manifests=[]; snapshots=[]
for slug in ['border_spear_rebel','canal_club_brigand']:
 for stage in ['idle_v1','action_v1']:
  d=BASE/slug/stage
  for p in d.rglob('manifest.json'):
   obj=json.loads(p.read_text());checks=[]
   manifest_base=(BASE/slug/'idle_v1') if 'sources' in p.parts else p.parent
   for f in obj.get('files',[]):
    q=(ROOT if f['path'].startswith('Assets/') else manifest_base)/f['path'];checks.append({'path':str(q.relative_to(ROOT)),'exists':q.exists(),'sha_matches':q.exists() and sha(q)==f['sha256'],'bytes_matches':q.exists() and ('bytes' not in f or q.stat().st_size==f['bytes'])})
   manifests.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'checks':checks})
  for p in list(d.glob('source_snapshot.json'))+list(d.glob('source_snapshot_manifest.json')):
   obj=json.loads(p.read_text());checks=[]
   if isinstance(obj,dict): obj=obj.get('sources',obj.get('files',[]))
   for f in obj:
    q=ROOT/f['path'];checks.append({'path':f['path'],'exists':q.exists(),'sha_matches':q.exists() and sha(q)==f['sha256']})
   snapshots.append({'path':str(p.relative_to(ROOT)),'checks':checks})
  for p in d.rglob('*.png'):
   if 'sources' in p.parts or not ('transparent' in p.name or 'raw_imagegen' in p.name): continue
   im=Image.open(p);rec={'path':str(p.relative_to(ROOT)),'sha256':sha(p),'size':list(im.size),'mode':im.mode}
   if im.mode=='RGBA':
    a=im.getchannel('A'); h=a.histogram();rec.update(alpha_bbox=a.getbbox(),alpha_extrema=a.getextrema(),zero_alpha_pixels=h[0],low_alpha_1_to_8=sum(h[1:9]),edge_max_alpha=max(max(a.crop(box).getdata()) for box in [(0,0,im.width,1),(0,im.height-1,im.width,im.height),(0,0,1,im.height),(im.width-1,0,im.width,im.height)]))
   records.append(rec)
result={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'two static anchors and all 001/002 action candidates; no original files modified','manifests':manifests,'source_snapshots':snapshots,'images':records}
(OUT/'technical_evidence.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('ROOT',ROOT,'manifests',len(manifests),'images',len(records)); print('manifest failures',[c for m in manifests for c in m['checks'] if not c['sha_matches'] or not c['bytes_matches']]);print('snapshot failures',[c for m in snapshots for c in m['checks'] if not c['sha_matches']])
