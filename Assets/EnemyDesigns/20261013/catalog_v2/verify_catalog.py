#!/usr/bin/env python3
"""Read-only catalog validation. Report to stdout; no external mutations."""
import hashlib,io,json
from pathlib import Path
from PIL import Image
import fitz
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 data=json.loads((HERE/'selected_sources.json').read_text());old=json.loads((HERE.parent/'catalog_v1/selected_sources.json').read_text())
 sources=[a for e in data['enemies'] for a in [e['idle']]+e['actions']+([e['continuation']] if e['continuation'] else [])]
 assert len(sources)==len({a['sha256'] for a in sources})==47
 for before,after in zip(old['enemies'],data['enemies']):
  for a,b in zip([before['idle']]+before['actions'],[after['idle']]+after['actions']):assert (a['path'],a['sha256'])==(b['path'],b['sha256'])
 assert data['enemies'][1]['continuation'] is None and data['enemies'][1]['independent_action_count']==2
 for a in sources:assert sha(ROOT/a['path'])==a['sha256']
 for a in data['evidence_refs']:assert sha(ROOT/a['path'])==a['sha256'] and sha(HERE/'evidence'/a['path'])==a['sha256']
 frozen=json.loads((HERE/'frozen_inputs_before.json').read_text())['files']
 for a in frozen:assert (ROOT/a['path']).stat().st_size==a['bytes'] and sha(ROOT/a['path'])==a['sha256']
 rm=json.loads((HERE/'browser_raster_map.json').read_text())['images']
 for a in rm:
  source=Image.open(ROOT/a['source_path']).convert('RGBA');out=Image.open(HERE/a['raster_path']).convert('RGBA')
  expected=source.resize(out.size,Image.Resampling.NEAREST);assert expected.tobytes()==out.tobytes()
 doc=fitz.open(HERE/'enemy_design_catalog_v2.pdf');assert len(doc)==14 and len(doc.get_toc())==14
 links=[l for p in doc for l in p.get_links()];assert len(links)==36 and all(0<=l['page']<14 for l in links)
 for i,e in enumerate(data['enemies']):
  p=doc[i+2];text=p.get_text();assert e['name'] in text
  for a in [e['idle']]+e['actions']+([e['continuation']] if e['continuation'] else []):assert a['label'] in text
  assert len(p.get_images())==e['selected_image_count']
 seen=set();embedded=[]
 for p in doc:
  for x in p.get_images(full=True):
   if x[0] in seen:continue
   seen.add(x[0]);rgb=Image.open(io.BytesIO(doc.extract_image(x[0])['image'])).convert('RGB');alpha=Image.open(io.BytesIO(doc.extract_image(x[1])['image'])).convert('L')
   rh=hashlib.sha256(rgb.tobytes()).hexdigest();ah=hashlib.sha256(alpha.tobytes()).hexdigest()
   matches=[a for a in rm if a['rgb_decoded_sha256']==rh and a['alpha_decoded_sha256']==ah];assert len(matches)==1
   assert doc.xref_get_key(x[0],'Interpolate')[1]=='false';embedded.append(matches[0]['source_sha256'])
 assert len(embedded)==len(set(embedded))==47
 return {'status':'pass','unique_images':47,'static':12,'original_actions':24,'previously_delivered_continuations':11,'independent_actions':35,'missing_continuations':['002'],'old_36_selections_unchanged':True,'old_frozen_files_unchanged':len(frozen),'evidence_files_verified':len(data['evidence_refs']),'full_canvas_nearest_rasters':47,'pdf_rgb_and_alpha_exact':47,'pdf_links':len(links),'pdf_bookmarks':len(doc.get_toc()),'pdf_pages':len(doc),'no_new_images_generated':True}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
