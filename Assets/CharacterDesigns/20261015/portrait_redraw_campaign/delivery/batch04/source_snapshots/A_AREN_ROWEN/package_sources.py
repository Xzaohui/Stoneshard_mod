#!/usr/bin/env python3
"""Build ordinary audited source ZIPs only after independent QA has frozen batch04."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, shutil, subprocess, sys, tempfile, zipfile, zlib
D=Path(__file__).resolve().parent; R=D.parent.parent; REPO=R.parents[3]
ORDER=['aren','rowen','maya','anla']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=R/'independent_qa/batch04'
gate=json.loads((D/'freeze_gate.json').read_text()); assert gate['approved_to_package'] is True
assert sha(qa/'selection.json')==gate['selection_sha256']
selected=json.loads((D/'selected_delivery_manifest.json').read_text()); final=json.loads((qa/'selection.json').read_text())
assert len(final['selected'])==4
for x in selected['characters']:
    s=next(y for y in final['selected'] if y['slug']==x['actor'])
    assert (REPO/s['selected_portrait']).resolve()==(R/x['source']).resolve()
    assert s['selected_sha256']==x['source_sha256']==sha(R/x['source'])==sha(D/x['delivery_file'])
visual=json.loads((D/'delivery_visual_QA.json').read_text())
assert visual['actually_viewed_via_view_image'] and visual['board_sha256']==sha(D/selected['board']['file'])
for item in json.loads((qa/'QA_FILE_INVENTORY.json').read_text())['files']:
    assert sha(qa/item['path'])==item['sha256'],item['path']
original_hashes={}; production_checks=[]
for c in ORDER:
    root=R/c; m=json.loads((root/'manifest.json').read_text())
    independent=next(x for x in final['selected'] if x['slug']==c)
    assert sha(root/'manifest.json')==independent['manifest_sha256']
    for line in (root/'SHA256SUMS.txt').read_text().splitlines():
        h,rel=line.split('  ',1); assert sha(root/rel)==h,(c,rel)
    for item in m['files']: assert sha(root/item['path'])==item['sha256'],(c,item['path'])
    source_checks=[]
    for item in json.loads((root/'sources/source_manifest.json').read_text())['sources']:
        p=item.get('path',item.get('source_path')); s=item.get('local_copy',item.get('snapshot_path'))
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
(D/'README_交付说明.md').write_text('# 第四批四人头像重绘交付\n\n2026-10-15｜艾伦 AREN、罗温 ROWEN、玛娅 MAYA、安菈 ANLA，均为 v2 候选。\n\n## 交付与边界\n\n- 4 张独立 PNG 均为 74×100、RGBA、二值 alpha；逐字节复制独立 QA 选稿。可见 RGB 色数依次为 32、32、30、32。≤32 色为本批临时预算，不代表原作统一色板已验收。\n- 中文手机总览每人含 1× 原尺寸和 4× 整数最近邻。仅排版，无补画、改色、裁切角色或平滑插值；每块展示区域已逐像素核对，并实际查看整张总览。\n- 四人各完成两次实质 imagegen 生图（首稿＋唯一一次必要修订）；候选为高分辨率 raw 经整幅 NEAREST 缩放、alpha 阈值128、无抖动量化派生。艾伦、罗温、安菈选 MAXCOVERAGE，玛娅选 MEDIANCUT；玛娅/安菈还留同 raw 的量化对照，未增加生成次数。\n- 全部仍是可审阅 candidate，非原生手工逐像素终稿，未接入游戏、未实机验证，也不表示用户已批准本批新稿。\n- 艾伦眼白仍略亮；罗温发束仍有规则斜纹。玛娅眼白与肤色较近、局部轮廓偏柔；安菈视线偏侧、表情较严肃，眼白稍宽且皮肤有少量碎斑。玛娅/安菈紧头像不代替完整围裙及全身服装交付。完整独立结论见 QA_REPORT.md。\n\n## 两个普通源 ZIP\n\n1. batch04_source_A_AREN_ROWEN.zip：艾伦、罗温完整生产过程。\n2. batch04_source_B_MAYA_ANLA.zip：玛娅、安菈完整生产过程。\n\n各自可独立解压，不是分卷压缩包。每包保留该两人的全部 raw、完整提示词参数与工具返回、历版候选、预览、导出与收尾脚本、人物卡/剧情/身份图/自有风格图快照、作者 QA 与 manifest/SHA256SUMS。\n\n两包均含全组独立 QA、所选四张 PNG 和总览、交付及冻结记录、来源逐项核验、便携复现脚本及包内清单。可解压至同一目录，公共文件内容相同。商业原生参考像素不附带，只保留路径及 SHA 引用。\n\n作者及 QA 历史脚本原样保留，部分依赖原仓库绝对路径；便携脚本用于不联网复现候选。源目录中的生产清单描述原生产范围；实际 ZIP 内容以 package_inventory.json 和 PACKAGE_SHA256SUMS.txt 为准。\n\n## 核验与复现\n\n- python3 verify_source_package.py <源包.zip>：全 ZIP CRC、逐文件 SHA-256、目录成员完整性核验。\n- 安装 Pillow 后，在解压目录执行 python3 reproduce_candidates.py --output <新的空目录路径>：检查 raw 与完整工具返回字节，以原整幅最近邻/量化算法复现该包全部候选，比较 RGBA 像素和 PNG 字节。只写新的输出目录，不改冻结文件。\n- 本次使用 Pillow 12.3.0；不同版本可能影响导出字节，报告保留版本号。10 张候选全部便携复现通过；4 张选稿的生产来源、独立 QA 与交付副本 SHA 一致。\n- 源包已实际解压并再次复现全部候选；逐项报告见各包 portable_reproduction_verification.json。所有原生产目录与独立 QA 在封包前后哈希一致。\n- 工具返回包含完整生成图 data URL，供离线复核，无需服务账号、密钥或再次生成。\n\n本次交付只涵盖这四人，全部角色头像重绘继续。\n',encoding='utf-8')
common=['README_交付说明.md','DELIVERY_EXCLUSIONS.json','verify_source_package.py','selected_delivery_manifest.json','delivery_visual_QA.json','freeze_gate.json','production_source_verification.json','build_delivery.py','package_sources.py','reproduce_candidates.py',selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]
results=[]
for suffix,characters in [('A_AREN_ROWEN',['aren','rowen']),('B_MAYA_ANLA',['maya','anla'])]:
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
    with tempfile.TemporaryDirectory(prefix='batch04-reproduce-') as tmp:
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
    out=D/f'batch04_source_{suffix}.zip'; assert not out.exists(),'Refuse replacing archive'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(snap.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(snap).as_posix())
    assert out.stat().st_size<18*1024*1024
    run=subprocess.run([sys.executable,str(D/'verify_source_package.py'),str(out)],check=True,capture_output=True,text=True)
    checks=json.loads(run.stdout)
    with tempfile.TemporaryDirectory(prefix='batch04-zip-replay-') as tmp:
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
