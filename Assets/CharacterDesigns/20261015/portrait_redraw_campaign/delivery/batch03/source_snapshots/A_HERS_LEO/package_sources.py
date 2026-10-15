#!/usr/bin/env python3
"""Build ordinary audited source ZIPs only after independent QA has frozen batch03."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, shutil, subprocess, sys, tempfile, zipfile, zlib
D=Path(__file__).resolve().parent; R=D.parent.parent; REPO=R.parents[3]
ORDER=['hers','leo','elaine','kaem']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=R/'independent_qa/batch03'
gate=json.loads((D/'freeze_gate.json').read_text()); assert gate['approved_to_package'] is True
assert sha(qa/'final_selection.json')==gate['selection_sha256']
selected=json.loads((D/'selected_delivery_manifest.json').read_text()); final=json.loads((qa/'final_selection.json').read_text())
assert len(final['selection'])==4
for x in selected['characters']:
    s=next(y for y in final['selection'] if y['slug']==x['actor'])
    assert (REPO/s['selected_path']).resolve()==(R/x['source']).resolve()
    assert s['selected_sha256']==x['source_sha256']==sha(R/x['source'])==sha(D/x['delivery_file'])
visual=json.loads((D/'delivery_visual_QA.json').read_text())
assert visual['actually_viewed_via_view_image'] and visual['board_sha256']==sha(D/selected['board']['file'])
for item in json.loads((qa/'QA_FILE_INVENTORY.json').read_text())['files']:
    assert sha(qa/item['path'])==item['sha256'],item['path']
original_hashes={}; production_checks=[]
for c in ORDER:
    root=R/c; m=json.loads((root/'manifest.json').read_text())
    assert 'frozen' in m.get('production_status',m.get('status',''))
    for line in (root/'SHA256SUMS.txt').read_text().splitlines():
        h,rel=line.split('  ',1); assert sha(root/rel)==h,(c,rel)
    for item in m['files']: assert sha(root/item['path'])==item['sha256'],(c,item['path'])
    source_checks=[]
    for item in json.loads((root/'sources/source_manifest.json').read_text()):
        p=item.get('source',item.get('original_path')); s=item.get('snapshot',item.get('snapshot_path'))
        assert sha(REPO/p)==item['sha256']==sha(root/s),(c,p)
        source_checks.append({'original':p,'snapshot':s,'sha256':item['sha256'],'original_and_snapshot_identical':True})
    returns=list((root/'tool_returns').glob('portrait_v[12].json')); assert len(returns)==2
    for retpath in returns:
        data=json.loads(retpath.read_text()); raw=root/'raw'/f'{retpath.stem}_raw_imagegen.png'
        assert raw.read_bytes()==base64.b64decode(data['image_url'].split(',',1)[1])
    for p in sorted(root.rglob('*')):
        if p.is_file():
            assert not p.is_symlink(),p
            original_hashes[p.relative_to(R).as_posix()]=sha(p)
    production_checks.append({'actor':c,'manifest_sha256':sha(root/'manifest.json'),'sha256sums_valid':True,'manifest_inventory_valid':True,'raw_toolreturn_byte_identical':True,'source_checks':source_checks})
for p in sorted(qa.rglob('*')):
    if p.is_file(): original_hashes[p.relative_to(R).as_posix()]=sha(p)
# References remain path/hash only; commercial baseline pixels are never copied.
commercial=REPO/'Assets/CharacterDesigns/20261015/native_style_pilot/mara/sources/user_style_reference.png'
excluded=[{'original_path':commercial.relative_to(REPO).as_posix(),'sha256':sha(commercial),'bytes':commercial.stat().st_size,'included_bytes':False,'role':'Campaign background comparative reference containing native commercial art; not a direct input asserted for this batch.'}]
js(D/'DELIVERY_EXCLUSIONS.json',{'commercial_reference_pixels_included':False,'items':excluded,'policy':'Only the four production folders and their independently generated QA plus delivery files enter these packages. No commercial native-reference image or source sprite atlas is included. The original manifests and tool calls are retained unchanged.'})
js(D/'production_source_verification.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'production_checks':production_checks,'all_pass':True})
(D/'README_交付说明.md').write_text('''# 第三批四人头像重绘交付

2026-10-15｜赫斯 HERS v2、雷奥 LEO v2、伊莲 ELAINE v2、凯姆 KAEM v2。

## 交付与边界

- 4 张独立 PNG 均为 74×100、RGBA、二值 alpha 的冻结 candidate，逐字节复制独立 QA 所选版本。可见 RGB 色数依次为 31、31、32、32。≤32 色为本批临时预算。
- 中文手机总览每人含 1× 原尺寸和 4× 整数最近邻。仅排版，无补画、改色、裁切角色或插值平滑；每块展示区域已逐像素核对，并实际查看总览。
- 四人各完成两次实质 imagegen 生图；候选为高分辨率 raw 经整幅 NEAREST 缩放、alpha 阈值 128、无抖动 MEDIANCUT 量化的派生。伊莲和凯姆另留 v1 MAXCOVERAGE 比较稿，不是额外一次生成。
- 仍是可审阅 candidate，非原生手工逐像素终稿，未接入游戏、未实机验证，也不表示用户已批准本批新稿。
- 赫斯灰胡茬略重，耳后小疤不保证缩小后稳定可读；雷奥发量偏多，仍有少量短茬颗粒和紧眉；伊莲眼白偏暖、发束层次略多，左侧发梢两组像素只以对角相接、8 邻域完整连接；凯姆灰茬下缘仍略碎、眉间偏紧。均如实保留，完整独立评价见 QA_REPORT.md。

## 两个普通源 ZIP

1. batch03_source_A_HERS_LEO.zip：赫斯、雷奥完整生产过程。
2. batch03_source_B_ELAINE_KAEM.zip：伊莲、凯姆完整生产过程。

各自可独立解压，不是分卷压缩包。每包含该两人所有 raw、完整提示词参数与工具返回、历版候选、预览、导出与收尾脚本、人物卡/故事/身份图/自有风格图快照、作者 QA 与 manifest/SHA256SUMS。赫斯未出图的参数校验失败记录也原样保留。

两个包均附全组独立 QA、所选四图和手机总览、交付与冻结记录、来源逐项核验、复现脚本和独立的包内清单。可解压至同一目录；公共文件内容一致。商业原生参考像素不附带，只保留路径和 SHA 引用。

作者和 QA 历史脚本原样保留，其中部分依赖完整原仓库路径；包内便携脚本用于不联网复现候选。源文件中的生产清单描述原生产目录；实际 ZIP 内容以 package_inventory.json 和 PACKAGE_SHA256SUMS.txt 为准。

## 核验与复现

- python3 verify_source_package.py <源包.zip>：全 ZIP CRC、每个文件 SHA-256、目录成员完整性。
- 安装 Pillow 后，在解压目录运行 python3 reproduce_candidates.py --output <新的空目录路径>：核验 raw 与工具返回的字节，按原整幅最近邻与量化算法复现该包全部候选，核对 RGBA 像素及 PNG 字节。脚本只写新目录，不改冻结文件。
- 封包使用 Pillow 12.3.0；不同 Pillow 版本可能影响导出字节，报告会保留版本号。本次 10 张候选均已便携复现并通过；4 张最终选稿的来源、独立 QA、交付副本 SHA 完全一致。
- 工具返回含完整生成图 data URL，供离线核验，无需登录、服务密钥或再调用生成服务。

本次只完成这四人的素材交付，整个角色头像重绘仍继续。
''',encoding='utf-8')
common=['README_交付说明.md','DELIVERY_EXCLUSIONS.json','verify_source_package.py','selected_delivery_manifest.json','delivery_visual_QA.json','freeze_gate.json','production_source_verification.json','build_delivery.py','package_sources.py','reproduce_candidates.py',selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]
results=[]
for suffix,characters in [('A_HERS_LEO',['hers','leo']),('B_ELAINE_KAEM',['elaine','kaem'])]:
    snap=D/'source_snapshots'/suffix; assert not snap.exists(),'Refuse overwrite of existing snapshot'; snap.mkdir(parents=True)
    origins={}
    for c in characters:
        for p in sorted((R/c).rglob('*')):
            if not p.is_file(): continue
            rel=p.relative_to(R).as_posix(); dst=snap/'portrait_redraw_campaign'/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,dst)
            assert sha(dst)==original_hashes[rel]
            origins[dst.relative_to(snap).as_posix()]={'kind':'production','original':rel,'sha256':original_hashes[rel]}
    for p in sorted(qa.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(R).as_posix(); dst=snap/'portrait_redraw_campaign'/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,dst)
        assert sha(dst)==original_hashes[rel]
        origins[dst.relative_to(snap).as_posix()]={'kind':'independent_qa','original':rel,'sha256':original_hashes[rel]}
    for name in common:
        shutil.copyfile(D/name,snap/name); origins[name]={'kind':'delivery','original':name,'sha256':sha(D/name)}
    with tempfile.TemporaryDirectory(prefix='batch03-reproduce-') as tmp:
        cmd=[sys.executable,str(snap/'reproduce_candidates.py'),'--output',str(Path(tmp)/'new-output')]
        run=subprocess.run(cmd,check=True,capture_output=True,text=True)
        report=json.loads(run.stdout); assert report['all_pass']
    js(snap/'portable_reproduction_verification.json',report)
    origins['portable_reproduction_verification.json']={'kind':'portable_reproduction','sha256':sha(snap/'portable_reproduction_verification.json')}
    files=[]
    excluded_hashes={x['sha256'] for x in excluded}
    for p in sorted(snap.rglob('*')):
        if not p.is_file(): continue
        b=p.read_bytes(); h=hashlib.sha256(b).hexdigest(); assert h not in excluded_hashes
        files.append({'path':p.relative_to(snap).as_posix(),'bytes':len(b),'sha256':h,'crc32':f'{zlib.crc32(b)&0xffffffff:08x}','source':origins[p.relative_to(snap).as_posix()]})
    js(snap/'package_inventory.json',{'package':suffix,'characters':characters,'commercial_reference_pixels_included':False,'self_inventory_excluded':['package_inventory.json','PACKAGE_SHA256SUMS.txt'],'files':files})
    (snap/'PACKAGE_SHA256SUMS.txt').write_text(''.join(f'{x["sha256"]}  {x["path"]}\n' for x in files)+f'{sha(snap/"package_inventory.json")}  package_inventory.json\n',encoding='utf-8')
    out=D/f'batch03_source_{suffix}.zip'; assert not out.exists(),'Refuse replacing archive'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(snap.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(snap).as_posix())
    assert out.stat().st_size<18*1024*1024
    run=subprocess.run([sys.executable,str(D/'verify_source_package.py'),str(out)],check=True,capture_output=True,text=True)
    checks=json.loads(run.stdout)
    with tempfile.TemporaryDirectory(prefix='batch03-zip-replay-') as tmp:
        folder=Path(tmp)/'extracted'; folder.mkdir()
        with zipfile.ZipFile(out) as z: z.extractall(folder)
        replay=subprocess.run([sys.executable,str(folder/'reproduce_candidates.py'),'--output',str(Path(tmp)/'reproduced')],check=True,capture_output=True,text=True)
        assert json.loads(replay.stdout)==report
    results.append({'file':out.name,'bytes':out.stat().st_size,'MiB':round(out.stat().st_size/1024**2,3),'sha256':sha(out),'crc_all_pass':True,'member_hash_all_pass':True,'actual_extracted_zip_reproduction_all_pass':True,'reproduction':report,'checks':checks})
for rel,h in original_hashes.items(): assert sha(R/rel)==h,('Frozen source changed during packaging',rel)
js(D/'package_verification.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'production_stable_during_packaging':True,'all_pass':True,'packages':results})
attachments=[selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]+[x['file'] for x in results]; assert len(attachments)<=10
js(D/'upload_request.json',{'uploads':[{'local_path':str(D/n),'purpose':'create_library_file','library_artifact_type':'image' if n.endswith('.png') else 'other'} for n in attachments]})
print(json.dumps({'attachments':attachments,'packages':[{k:v for k,v in x.items() if k not in ['checks','reproduction']} for x in results],'production_stable':True},ensure_ascii=False,indent=2))
