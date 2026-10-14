#!/usr/bin/env python3
"""Small production/QA package; deliberately excludes artwork and page PNGs."""
import hashlib,json,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
LIMIT=18*1024*1024
FILES=[
'build_catalog.py','verify_catalog.py','package_production.py','README_制作说明.md','requirements.txt',
'source_audit/build_selection_audit.py','source_audit/selection_audit.json','source_audit/old_catalog_fingerprints.json','source_audit/old_source_fingerprints.json','source_audit/eleventh_source_fingerprints.json','source_audit/ACTION_DELIVERY_INDEX_snapshot.md',
'production/fonts/NotoSansCJKsc-catalog.otf','production/fonts/Noto-CJK-LICENSE.txt','production/embedded_manifest.json','production/layout_objects.json',
'LAYOUT_VERIFICATION.json','review/PDF_IMAGE_DECODE_QA.json','review/RENDER_MANIFEST.json','review/ALL_PAGE_VISUAL_QA.json',
'FINAL_SOURCE_FREEZE_QA.json','REPRODUCTION_QA.json','OUTPUTS.json',
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def main():
 records=[]
 for name in FILES:
  p=HERE/name;assert p.is_file(),p
  records.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
 manifest={'schema_version':1,'purpose':'Layout scripts, fonts, source path/SHA index and QA only; not a complete raw/artwork package.','excluded':['128 original PNG images','128 browse derivative PNG images','raw images','failed candidates','full generation tool payloads','original complete source ZIP files','24 page preview PNGs'],'rebuild_requires':'Original Stoneshard_mod project and the 128 selected image files with matching SHA.','members':records,'self_manifest_excluded_from_own_member_hash_list':True}
 save(HERE/'SOURCE_PACKAGE_MANIFEST.json',manifest)
 out=HERE/'output/新增剧情人物44人_动作图册制作资料_v1.zip'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name in FILES+['SOURCE_PACKAGE_MANIFEST.json']:
   # Fixed timestamp makes packaging deterministic.
   zi=zipfile.ZipInfo(name,(2026,10,14,9,30,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o644<<16
   z.writestr(zi,(HERE/name).read_bytes())
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  assert len(z.namelist())==len(FILES)+1 and len(z.namelist())==len(set(z.namelist()))
  for r in records:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
 assert out.stat().st_size<LIMIT
 outputs=json.loads((HERE/'OUTPUTS.json').read_text())
 result={'schema_version':1,'status':'ready_for_parent_review_and_delivery','outputs':[dict(kind=k,**v) for k,v in outputs.items()]+[{'kind':'production_sources','path':str(out.relative_to(HERE)),'bytes':out.stat().st_size,'sha256':sha(out)}],'all_files_below_18MiB':all(v['bytes']<LIMIT for v in outputs.values()) and out.stat().st_size<LIMIT,'package_member_count':len(FILES)+1,'zip_crc_and_member_sha_pass':True,'new_images_generated':False,'git_performed':False,'uploaded_by_catalog_worker':False,'sent_by_catalog_worker':False,'all_sources_retained':True,'user_style_approval_claimed':False,'runtime_verified':False}
 save(HERE/'DELIVERY_MANIFEST.json',result)
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
