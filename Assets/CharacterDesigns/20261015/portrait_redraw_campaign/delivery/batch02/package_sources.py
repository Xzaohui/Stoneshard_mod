#!/usr/bin/env python3
"""Package a frozen, auditable snapshot; never mutate production files."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,zipfile,zlib,base64
D=Path(__file__).resolve().parent; R=D.parent.parent
ORDER=['toman','sena','lyd','morlen']
def hbytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return hbytes(p.read_bytes())
def js(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=R/'independent_qa/batch02'; final=json.loads((qa/'selection.json').read_text())
assert sha(qa/'selection.json')=='9b6358e748ae7665772801f3c9ad049a56ce28d65e7fdd98ac67a6afd20a5ccd'
assert len(final['selected'])==4 and all(x['status']=='candidate' for x in final['selected'])
selected=json.loads((D/'selected_delivery_manifest.json').read_text())
for x in selected['characters']:
 s=next(y for y in final['selected'] if y['slug']==x['actor'])
 assert (qa/s['candidate']).resolve()==(R/x['source']).resolve() and s['sha256']==x['source_sha256']==sha(R/x['source'])==sha(D/x['delivery_file'])
for line in (qa/'SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);assert sha(qa/rel)==h,rel
# Verify every original producer inventory before taking a snapshot.
production_checks=[]; original_hashes={}; exclusions=[]
for c in ORDER:
 root=R/c; m=json.loads((root/'manifest.json').read_text()); assert m['image_generation_frozen']
 for line in (root/'SHA256SUMS.txt').read_text().splitlines():
  h,rel=line.split('  ',1); assert sha(root/rel)==h,(c,rel)
 for p in sorted(root.rglob('*')):
  if not p.is_file():continue
  assert not p.is_symlink(),p
  rel=p.relative_to(R).as_posix(); original_hashes[rel]=sha(p)
  if p.name=='user_style_reference.png':
   exclusions.append({'path':rel,'sha256':sha(p),'bytes':p.stat().st_size,'reason':'User-supplied comparative board includes commercial native pixels. Provenance metadata only; image bytes excluded.'})
 for returned in sorted((root/'tool_returns').glob('portrait_v*.json')):
  raw=root/'raw'/f'{returned.stem}_raw_imagegen.png'
  ret=json.loads(returned.read_text())
  assert hbytes(base64.b64decode(ret['image_url'].split(',',1)[1]))==sha(raw)
 production_checks.append({'actor':c,'manifest_sha256':sha(root/'manifest.json'),'sha256sums_valid':True,'raw_toolreturn_byte_identical':True})
for p in sorted(qa.iterdir()):
 if p.is_file():original_hashes[p.relative_to(R).as_posix()]=sha(p)
original_hashes['batch_02_next.json']=sha(R/'batch_02_next.json')
js(D/'DELIVERY_EXCLUSIONS.json',{'items':exclusions,'notes':'Excluded only commercial-reference image bytes. Original provenance/manifests are retained unchanged, including their historical references to excluded files. Those historical SHA256SUMS describe production folders, not this delivery package; package_inventory.json describes the actual package.'})
readme='# 第二批四人头像重绘交付\n\n2026-10-15｜托曼 TOMAN v1、塞娜 SENA v2、莉德 LYD v2、莫伦 MORLEN v1。\n\n## 使用与状态\n\n- 4 张独立 PNG 是冻结 candidate，74×100、RGBA、二值 alpha，逐字节复制选稿。可见 RGB 色数依次 30、31、32、32；≤32 色只是本批临时上限。\n- 中文手机总览为每人 1× 原尺寸＋4× 最近邻。只排版，没有补画、重绘或改色；1×/4×区域均逐像素核对。\n- 本批使用内置生图完成实质重绘；高分辨率 raw 经整幅最近邻缩小、alpha 阈值 128、无抖动量化派生。托曼/塞娜使用 MEDIANCUT；莉德/莫伦使用 MAXCOVERAGE。\n- 不是原生手工逐像素终稿；尚未接入游戏、未做实机验证，也不代表用户已认可本批新稿。\n- 托曼：兜帽使脸略小、灰须细纹；塞娜：底部围巾仍约 16 像素；莉德：眼白略亮、发髻仍偏大、脸放大幅度有限；莫伦：眼白略亮、须发细纹和围巾面积。以上为独立 QA 非阻断余项，完整结论见 QA_REPORT.md。\n\n## 源包\n\n两个文件是各自可解压的普通 ZIP，不是分卷压缩包：\n1. batch02_source_A_TOMAN_SENA.zip：托曼、塞娜全部制作过程与来源。\n2. batch02_source_B_LYD_MORLEN.zip：莉德、莫伦全部制作过程与来源。\n\n每包共有：全组独立 QA、中文总览与 4 张选稿、交付清单、来源排除清单、校验和、核验脚本，以及便携复现脚本。每个角色保留全部 raw、提示词、完整工具返回、历版候选、导出脚本、预览、来源人物卡/身份图/风格图、作者 QA 与原始 manifest。\n\n商业原生参考像素不随包分发；其原始路径与 SHA 保留在来源清单和 DELIVERY_EXCLUSIONS.json。自有生成身份/风格参考保留。生产 SHA256SUMS 原样留档，可能引用主动排除的商业图，不能当作实际包内容清单；实际封包清单为 package_inventory.json / PACKAGE_SHA256SUMS.txt。\n\n两个包可解压到同一空目录，公共文件字节完全一致。历史作者与审查脚本原样保留，部分依赖完整原仓库路径，不能直接据此断言解压即能跑完整仓库审计。\n\n## 复现与核验\n\n- python3 verify_source_package.py <源包.zip>：校验全部 ZIP CRC 与逐项 SHA-256。\n- 安装 Pillow 后，在任一解压目录运行 python3 reproduce_candidates.py --output <新的空目录路径>：只读取包内 raw/tool_returns/candidates，按对应量化算法复现该包角色的全部候选，在单独输出目录逐像素与 PNG 字节比对。不会改动冻结文件。封包测试使用 Pillow 12.3.0；其他版本输出字节可能不同。\n- 全组六张候选已独立复现；所选四张 SHA 与 selection.json、作者 manifest 和交付 PNG 一致。\n- 包内工具返回保留完整 data URL，仅用于审计与复现；不需要登录、服务密钥或调用外部生成服务。\n\n这批交付只关闭四人的本次素材整理与交付步骤，全体头像生产继续推进。\n'
(D/'README_交付说明.md').write_text(readme,encoding='utf-8')
verify='''from pathlib import Path\nimport sys,json,hashlib,zipfile\np=Path(sys.argv[1])\nwith zipfile.ZipFile(p) as z:\n assert z.testzip() is None,'ZIP CRC failed'\n inv=json.loads(z.read('package_inventory.json'))\n for x in inv['files']:\n  data=z.read(x['path'])\n  assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'],x['path']\n print('PASS:',p.name,len(inv['files']),'file hashes; all ZIP CRCs')\n'''
(D/'verify_source_package.py').write_text(verify,encoding='utf-8')
js(D/'delivery_visual_QA.json',{'board_file':selected['board']['file'],'board_sha256':selected['board']['sha256'],'actually_viewed_via_view_image':True,'viewed_utc':'2026-10-15T08:29:29Z','inspection':'Chinese names, all four portraits at 1x and 4x, per-person limits and pipeline footnote visible; no crop, text collision or native-reference pixels.','portrait_geometry_or_color_edits':False,'copy_and_nearest_composite_checks':selected['board']['portrait_checks']})
common_names=['README_交付说明.md','DELIVERY_EXCLUSIONS.json','verify_source_package.py','selected_delivery_manifest.json','delivery_visual_QA.json','build_delivery.py','package_sources.py','reproduce_candidates.py','portable_reproduction_verification.json',selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]
excluded={x['path'] for x in exclusions}
package_results=[]
for suffix,characters in [('A_TOMAN_SENA',['toman','sena']),('B_LYD_MORLEN',['lyd','morlen'])]:
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
 for p in [R/'batch_02_next.json']+sorted(qa.iterdir()):
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
 out=D/f'batch02_source_{suffix}.zip';assert not out.exists(),'Refuse replacing package'
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
