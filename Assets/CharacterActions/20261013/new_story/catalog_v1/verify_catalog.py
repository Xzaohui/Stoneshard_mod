#!/usr/bin/env python3
"""Read-only source preservation, image resource, link and complete page rendering QA."""
import json,hashlib,collections
from pathlib import Path
import fitz
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 data=read(HERE/'source_audit/selection_audit.json');outputs=read(HERE/'OUTPUTS.json');pdf=HERE/outputs['pdf']['path'];doc=fitz.open(pdf)
 emb=read(HERE/'production/embedded_manifest.json')['assets'];resources={}
 for page in doc:
  for inf in page.get_images(full=True):resources[inf[0]]=inf
 expected={}; seen=[]
 for e in emb:
  p=HERE/e['embedded_path'];assert sha(p)==e['embedded_sha256'];im=Image.open(p).convert('RGBA')
  original=Image.open(ROOT/e['source_path']).convert('RGBA'); expected_im=original.resize(im.size,Image.Resampling.NEAREST)
  assert expected_im.tobytes()==im.tobytes(),('Browse derivative mismatch',e['key'])
  k=(im.width,im.height,digest(im.convert('RGB').tobytes()),digest(im.getchannel('A').tobytes()))
  assert k not in expected;expected[k]=e
 for xref,inf in resources.items():
  pix=fitz.Pixmap(doc,xref);assert pix.n==3,(xref,pix.n)
  mask=fitz.Pixmap(doc,inf[1]);assert mask.n==1
  key=(pix.width,pix.height,digest(pix.samples),digest(mask.samples));assert key in expected,('PDF image mismatch',xref)
  e=expected.pop(key);seen.append({'key':e['key'],'pdf_xref':xref,'embedded_sha256':e['embedded_sha256'],'rgb_and_alpha_exact':True})
 assert not expected and len(seen)==128
 save(HERE/'review/PDF_IMAGE_DECODE_QA.json',{'status':'PASS','pdf_sha256':sha(pdf),'unique_images':128,'decoded_rgb_and_alpha_exact_to_browse_png':True,'all_128_browse_pngs_exact_to_source_nearest_resize':True,'files':seen})
 errors=[];checked=0
 for fn in ['old_catalog_fingerprints.json','old_source_fingerprints.json','eleventh_source_fingerprints.json']:
  d=read(HERE/'source_audit'/fn)
  for r in d['files']:
   p=ROOT/r['path'];checked+=1
   if not p.exists() or p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:errors.append(r['path'])
 for a in data['assets']:
  assert sha(ROOT/a['path'])==a['sha256'];checked+=1
 references={}
 def collect_refs(v):
  if isinstance(v,dict):
   if isinstance(v.get('path'),str) and v['path'].startswith('Assets/') and isinstance(v.get('sha256'),str): references[v['path']]=v['sha256']
   for child in v.values():collect_refs(child)
  elif isinstance(v,list):
   for child in v:collect_refs(child)
 collect_refs(data)
 evidence_errors=[p for p,h in references.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
 errors.extend(evidence_errors)
 save(HERE/'FINAL_SOURCE_FREEZE_QA.json',{'status':'PASS' if not errors else 'FAIL','files_checked':checked,'source_evidence_references_checked':len(references),'source_evidence_mismatches':evidence_errors,'changed_or_missing':errors,'selected_images':128,'original_sources_modified':False,'prior_catalog_files_modified':False})
 assert not errors,errors
 pages=[];render=HERE/'review/pages';render.mkdir(exist_ok=True)
 for p in doc:
  out=render/f'page-{p.number+1:02d}.png';p.get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(out)
  assert len(p.get_links())==(44 if p.number==1 else 1 if p.number>1 else 0)
  pages.append({'page':p.number+1,'path':str(out.relative_to(HERE)),'bytes':out.stat().st_size,'sha256':sha(out),'render':'PyMuPDF 1.25x; no post-edit'})
 texts='\n'.join(p.get_text() for p in doc)
 for c in data['characters']:assert c['name'] in texts and c['canonical_id'] in texts,c
 for s in ['图里','锉珥','苇珥','栎珥']:assert s in texts
 assert len(doc)==24 and len(doc.get_toc())==24
 save(HERE/'review/RENDER_MANIFEST.json',{'pdf_path':str(pdf.relative_to(HERE)),'pdf_sha256':sha(pdf),'pages':pages,'all_pages_rendered':True,'links':66,'bookmarks':24})
 print(json.dumps({'images_exact':len(seen),'preserved_files_checked':checked,'rendered_pages':len(pages),'pdf_bytes':pdf.stat().st_size}))
if __name__=='__main__':main()
