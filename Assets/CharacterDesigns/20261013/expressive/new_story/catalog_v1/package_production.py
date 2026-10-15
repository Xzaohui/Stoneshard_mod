#!/usr/bin/env python3
"""Package small reproducible layout materials, excluding original and browse images."""
from pathlib import Path
import hashlib,json,zipfile
B=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[
 'README_制作说明.md','build_catalog.py','package_production.py','OUTPUTS.json',
 'LAYOUT_VERIFICATION.json','REPRODUCTION_QA.json','FINAL_SOURCE_FREEZE_QA.json',
 'source_audit/selection_audit.json','source_audit/audit_summary.json',
 'source_audit/build_selection_audit.py','source_audit/verify_freeze_chain.py',
 'production/embedded_manifest.json','production/layout_objects.json',
 'production/fonts/NotoSansCJKsc-catalog.otf','production/fonts/Noto-CJK-LICENSE.txt',
 'review/PDF_IMAGE_DECODE_QA.json','review/QA-independent-layout.json',
]
for rel in files: assert (B/rel).is_file(),rel
manifest={'schema_version':1,'package_purpose':'Small layout-production and source-audit materials for the 44-character catalogue.','not_complete_original_source_collection':True,'not_standalone_without_original_selected_artwork':True,'excluded':['original selected PNGs','browse derivative PNGs','raw generations','rejected drafts','tool-return logs','original delivery source ZIPs','final PDF and overview delivered separately'],'members':[{'path':p,'bytes':(B/p).stat().st_size,'sha256':sha(B/p)} for p in files],'self_manifest_excluded_from_own_hash_list':True}
(B/'SOURCE_PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
files.append('SOURCE_PACKAGE_MANIFEST.json')
out=B/'output/新增剧情人物44人_图册制作资料_v1.zip'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for rel in sorted(files):
  info=zipfile.ZipInfo(rel,date_time=(2026,10,14,3,16,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,(B/rel).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for rel in files: assert z.read(rel)==(B/rel).read_bytes(),rel
print(json.dumps({'path':str(out.relative_to(B)),'bytes':out.stat().st_size,'sha256':sha(out),'members':len(files)},ensure_ascii=False,indent=2))
