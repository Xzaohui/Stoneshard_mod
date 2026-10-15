#!/usr/bin/env python3
"""Package a frozen, auditable snapshot; never mutate production files."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,zipfile,zlib,base64
D=Path(__file__).resolve().parent; R=D.parent.parent
ORDER=['mia','ena','nara','nell','sel']
def hbytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return hbytes(p.read_bytes())
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=R/'independent_qa/batch01'; final=json.loads((qa/'final_selection.json').read_text())
assert final['status']=='final_independent_qa' and final['candidate_count']==5 and final['native_final_count']==0
selected=json.loads((D/'selected_delivery_manifest.json').read_text())
for x in selected['characters']:
 s=next(y for y in final['selections'] if y['actor']==x['actor'])
 assert s['target']==x['source'] and s['sha256']==x['source_sha256']==sha(R/x['source'])==sha(D/x['delivery_file'])
for x in json.loads((qa/'QA_FILE_INVENTORY.json').read_text()):assert sha(qa/x['path'])==x['sha256']
# Verify every original producer inventory before taking a snapshot.
production_checks=[]; original_hashes={}; exclusions=[]
for c in ORDER:
 root=R/c; m=json.loads((root/'manifest.json').read_text()); assert m['image_generation_frozen'] and m['source_files_frozen_for_delivery']
 for line in (root/'SHA256SUMS.txt').read_text().splitlines():
  h,rel=line.split('  ',1); assert sha(root/rel)==h,(c,rel)
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  assert not p.is_symlink(),p
  rel=p.relative_to(R).as_posix(); original_hashes[rel]=sha(p)
  if p.name=='user_style_reference.png':
   exclusions.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size,'reason':'User-supplied comparative board includes commercial native pixels. Provenance metadata only; image bytes excluded.'})
 for version in ['v1','v2']:
  raw=root/'raw'/f'portrait_{version}_raw_imagegen.png'
  ret=json.loads((root/'tool_returns'/f'portrait_{version}.json').read_text())
  assert hbytes(base64.b64decode(ret['image_url'].split(',',1)[1]))==sha(raw)
 production_checks.append({'actor':c,'manifest_sha256':sha(root/'manifest.json'),'sha256sums_valid':True,'raw_toolreturn_byte_identical':True})
for p in sorted(qa.iterdir()):
 if p.is_file():original_hashes[p.relative_to(R).as_posix()]=sha(p)
js(D/'DELIVERY_EXCLUSIONS.json',{'items':exclusions,'notes':'Excluded only commercial-reference image bytes. Original provenance/manifests are retained unchanged, including their historical references to excluded files. Those historical SHA256SUMS describe production folders, not this delivery package; package_inventory.json describes the actual package.'})
readme='''# 首批五人头像重绘交付\n\n2026-10-15｜米娅 MIA、艾娜 ENA、纳拉 NARA、妮尔 NELL、塞尔 SEL。\n\n## 使用与状态\n\n- 5 张独立 PNG 为最终冻结的 candidate，74×100、RGBA、二值 alpha，逐字节复制选稿。\n- 中文总览为每人 1×原尺寸＋4×最近邻；只做排版，没有补画、重绘或改色。\n- 来源为高分辨率生图，经全画布最近邻缩小、alpha 阈值 128、无抖动量化派生；不是原生手工逐像素终稿。\n- 尚未接入游戏、未做实机验证，也不代表用户已经认可这批新稿。≤32 色仅本批临时上限。\n- MIA 最终使用 v2 MAXCOVERAGE 保住暗青披肩；SEL 使用 v2 MEDIANCUT 减少皮肤盐斑；两者均为同 raw 的机械量化对照，没有增加生图。\n- ENA 保留 3 像素独立侧发簇 (3,74)、(3,75)、(4,75)。其余亮眼白、平行发带、自动近似色等局限见逐人 QA。\n\n## 源包\n\n三个文件是彼此独立的普通 ZIP，不是分卷压缩包：\n1. source_A_MIA_ENA.zip：MIA、ENA 完整过程与来源。\n2. source_B_NARA_NELL.zip：NARA、NELL 完整过程与来源。\n3. source_C_SEL.zip：SEL 完整过程与来源。\n每包都含同一份全组独立 QA、中文总览及五张选稿、交付清单和核验脚本。每个角色保留全部 raw、提示词、完整工具返回、候选、导出脚本、预览、来源、作者 QA 与清单；旧候选仅供追溯。\n\n商业原生参考图像不随包分发；其来源路径与哈希保留在原始来源清单及 DELIVERY_EXCLUSIONS.json 中。生成的旧身份图与自有风格参考可随包收录。生产清单 SHA256SUMS.txt 未改写，因此会包含被主动排除的商业参考项；验收实际源包请使用 package_inventory.json / PACKAGE_SHA256SUMS.txt。\n\n各包可独立解压查看。若要拼回完整工作副本，将三包解压到同一空目录，重叠公共文件字节一致。历史脚本原样保留，可能依赖原仓库路径与 Pillow 版本；请先阅读后在副本内运行，避免覆盖已冻结成果。完整派生算法与独立逐 RGBA 复现结果见 independent_qa/batch01。\n\n## 核验\n\n运行 python3 verify_source_package.py <源包.zip> 可检查所有 ZIP CRC 和清单内每项 SHA-256。交付前已对每个条目检查 CRC、包内 hash 与快照源文件 hash；选稿、中文板和源包关联见 selected_delivery_manifest.json。\n'''
(D/'README_交付说明.md').write_text(readme,encoding='utf-8')
verify='''from pathlib import Path\nimport sys,json,hashlib,zipfile\np=Path(sys.argv[1])\nwith zipfile.ZipFile(p) as z:\n assert z.testzip() is None,'ZIP CRC failed'\n inv=json.loads(z.read('package_inventory.json'))\n for x in inv['files']:\n  data=z.read(x['path'])\n  assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'],x['path']\n print('PASS:',p.name,len(inv['files']),'file hashes; all ZIP CRCs')\n'''
(D/'verify_source_package.py').write_text(verify,encoding='utf-8')
js(D/'delivery_visual_QA.json',{'board_file':selected['board']['file'],'board_sha256':selected['board']['sha256'],'actually_viewed_via_view_image':True,'inspection':'Chinese names, all five portraits at 1x and 4x, per-person limits and pipeline footnote visible; no crop, text collision or native-reference pixels.','portrait_geometry_or_color_edits':False,'copy_and_nearest_composite_checks':selected['board']['portrait_checks']})
common_names=['README_交付说明.md','DELIVERY_EXCLUSIONS.json','verify_source_package.py','selected_delivery_manifest.json','delivery_visual_QA.json','build_delivery.py',selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]
excluded={x['path'] for x in exclusions}
package_results=[]
for suffix,characters in [('A_MIA_ENA',['mia','ena']),('B_NARA_NELL',['nara','nell']),('C_SEL',['sel'])]:
 snap=D/'source_snapshots'/suffix
 assert not snap.exists(),'Snapshot already exists; refuse overwrite'
 snap.mkdir(parents=True)
 origin={}
 for c in characters:
  for p in sorted((R/c).rglob('*')):
   if not p.is_file():continue
   rel=p.relative_to(R).as_posix()
   if rel in excluded:continue
   dst=snap/'portrait_redraw_campaign'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
   assert sha(dst)==original_hashes[rel]
   origin[dst.relative_to(snap).as_posix()]={'type':'production','path':rel,'sha256':original_hashes[rel]}
 for p in sorted(qa.iterdir()):
  if not p.is_file():continue
  rel=p.relative_to(R).as_posix(); dst=snap/'portrait_redraw_campaign'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
  assert sha(dst)==original_hashes[rel]
  origin[dst.relative_to(snap).as_posix()]={'type':'independent_qa','path':rel,'sha256':original_hashes[rel]}
 for n in common_names:
  dst=snap/n;shutil.copyfile(D/n,dst)
  origin[n]={'type':'delivery','path':n,'sha256':sha(D/n)}
 files=[]
 for p in sorted(snap.rglob('*')):
  if p.is_file():
   data=p.read_bytes();rel=p.relative_to(snap).as_posix()
   files.append({'path':rel,'bytes':len(data),'sha256':hbytes(data),'source_crc32':f'{zlib.crc32(data)&0xffffffff:08x}','source':origin[rel]})
 js(snap/'package_inventory.json',{'package':suffix,'characters':characters,'commercial_reference_pixels_included':False,'self_inventory_excluded':['package_inventory.json','PACKAGE_SHA256SUMS.txt'],'files':files})
 (snap/'PACKAGE_SHA256SUMS.txt').write_text(''.join(f'{x["sha256"]}  {x["path"]}\n' for x in files)+f'{sha(snap/"package_inventory.json")}  package_inventory.json\n',encoding='utf-8')
 out=D/f'batch01_source_{suffix}.zip';assert not out.exists(),'Refuse replacing package'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(snap.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(snap).as_posix())
 assert out.stat().st_size<18*1024*1024
 checks=[]
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  assert not any(Path(n).name=='user_style_reference.png' for n in z.namelist())
  for info in z.infolist():
   data=z.read(info); source=(snap/info.filename).read_bytes()
   assert len(data)==len(source)==info.file_size and data==source
   assert zlib.crc32(source)&0xffffffff==info.CRC
   checks.append({'path':info.filename,'sha256':hbytes(data),'source_crc32':f'{zlib.crc32(source)&0xffffffff:08x}','archive_crc32':f'{info.CRC:08x}','source_bytes_match':True})
 package_results.append({'file':out.name,'characters':characters,'bytes':out.stat().st_size,'MiB':round(out.stat().st_size/1024**2,3),'sha256':sha(out),'crc_all_pass':True,'member_hash_all_pass':True,'files':checks})
# Detect changes after snapshot: frozen author/QA files must stay byte-identical.
for rel,h in original_hashes.items():assert sha(R/rel)==h,('Production changed during packaging',rel)
js(D/'package_verification.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'production_checks':production_checks,'production_stable_during_packaging':True,'excluded_commercial_files':exclusions,'packages':package_results})
attachments=[selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]+[x['file'] for x in package_results]
assert len(attachments)<=10
js(D/'upload_request.json',{'uploads':[{'local_path':str(D/f),'purpose':'create_library_file','library_artifact_type':'image' if f.endswith('.png') else 'other'} for f in attachments]})
print(json.dumps({'attachments':attachments,'packages':[{k:v for k,v in x.items() if k!='files'} for x in package_results],'production_stable':True},ensure_ascii=False,indent=2))
