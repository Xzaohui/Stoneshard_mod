#!/usr/bin/env python3
"""Build ordinary audited source ZIPs only after independent QA has frozen batch27."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, shutil, subprocess, sys, tempfile, zipfile, zlib
from source_validation import validate_sources, validate_prompts
D=Path(__file__).resolve().parent; R=D.parent.parent; REPO=R.parents[3]
ORDER=['odo','tanser','noze','sefin']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
qa=R/'independent_qa/batch27'
gate=json.loads((D/'freeze_gate.json').read_text()); assert gate['approved_to_package'] is True
selected=json.loads((D/'selected_delivery_manifest.json').read_text())
for x in selected['characters']:
    ref=next(y for y in gate['characters'] if y['slug']==x['actor'])
    assert (R/ref['selected_portrait']).resolve()==(R/x['source']).resolve()
    assert ref['selected_sha256']==x['source_sha256']==sha(R/x['source'])==sha(D/x['delivery_file'])
visual=json.loads((D/'delivery_visual_QA.json').read_text())
assert gate['qualified_candidate_count']==2 and gate['held_count']==2
assert visual['actually_viewed_via_view_image'] and visual['board_sha256']==sha(D/selected['board']['file'])
for name, expected in gate['qa_files'].items(): assert sha(qa/name)==expected,name
for line in ((qa/'SHA256SUMS').read_text().splitlines()):
    h,rel=line.split('  ',1); assert sha(qa/rel)==h,rel
original_hashes={}; production_checks=[]
frozen=gate
for c,items in frozen['frozen_character_files'].items():
    actual={p.relative_to(R/c).as_posix() for p in (R/c).rglob('*') if p.is_file()}
    assert actual=={i['path'] for i in items},c
    for item in items: assert sha(R/c/item['path'])==item['sha256'] and (R/c/item['path']).stat().st_size==item['bytes']
for c in ORDER:
    root=R/c; m=json.loads((root/'manifest.json').read_text())
    independent=next(x for x in gate['characters']+gate['held'] if x['slug']==c)
    assert sha(root/'manifest.json')==independent['production_manifest_sha256']
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if (root/'SHA256SUMS').exists():
        sum_rows={}
        for line in (root/'SHA256SUMS').read_text().splitlines():
            h,rel=line.split('  ',1); assert sha(root/rel)==h,(c,rel);sum_rows[rel]=h
        assert actual-{'SHA256SUMS'}==set(sum_rows),('SHA inventory mismatch',c)
        manifest_rows=m['files']; expected=actual-{'manifest.json','SHA256SUMS'}
    else:
        rows=json.loads((root/'file_hashes.json').read_text())['files']
        assert actual-{'file_hashes.json'}=={i['path'] for i in rows}
        for item in rows: assert sha(root/item['path'])==item['sha256'] and (root/item['path']).stat().st_size==item['bytes']
        manifest_rows=m['artifact_inventory']; expected=actual-{'manifest.json','file_hashes.json'}
    assert expected=={i['path'] for i in manifest_rows},('Manifest inventory mismatch',c)
    for item in manifest_rows: assert sha(root/item['path'])==item['sha256'] and (root/item['path']).stat().st_size==item['bytes']
    source_checks=validate_sources(root,REPO)
    prompt_checks=validate_prompts(root)
    returns=list((root/'tool_returns').glob('portrait_v[12].json')); assert len(returns)==m.get('generation_calls',m.get('generation_calls_completed',m.get('generated_image_count',m.get('generation',{}).get('attempts'))))
    for retpath in returns:
        data=json.loads(retpath.read_text()); raw=root/'raw'/f'{retpath.stem}_raw_imagegen.png'
        assert raw.read_bytes()==base64.b64decode(data['image_url'].split(',',1)[1])
    for p in sorted(root.rglob('*')):
        if p.is_file():
            assert not p.is_symlink(),p
            original_hashes[p.relative_to(R).as_posix()]=sha(p)
    production_checks.append({'actor':c,'manifest_sha256':sha(root/'manifest.json'),'sha256sums_valid':True,'manifest_inventory_valid':True,'raw_toolreturn_byte_identical':True,'source_checks':source_checks,'prompt_checks':prompt_checks})
for p in sorted(qa/name for name in gate['qa_files']):
    if p.is_file(): original_hashes[p.relative_to(R).as_posix()]=sha(p)
# References remain path/hash only; commercial baseline pixels are never copied.
commercial=REPO/'Assets/CharacterDesigns/20261015/native_style_pilot/mara/sources/user_style_reference.png'
excluded=[{'original_path':commercial.relative_to(REPO).as_posix(),'sha256':sha(commercial),'bytes':commercial.stat().st_size,'included_bytes':False,'role':'Campaign background comparative reference containing native commercial art; not a direct input asserted for this batch.'}]
js(D/'DELIVERY_EXCLUSIONS.json',{'commercial_reference_pixels_included':False,'omitted_duplicate_QA_replays':gate['qa_duplicated_replay_files_omitted'],'QA_omission_reason':'No independent QA files omitted; all independent files and replay outputs retained in both archives.','items':excluded,'policy':'Only the four production folders and their independently generated QA plus delivery files enter these packages. No commercial native-reference image or source sprite atlas is included. The original manifests and tool calls are retained unchanged.'})
js(D/'production_source_verification.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'production_checks':production_checks,'qualified_candidate_count':2,'held_count':2,'held_not_counted_as_success':True,'all_pass':True})
common=['source_validation.py','check_delivery.py','README_交付说明.md','DELIVERY_EXCLUSIONS.json','verify_source_package.py','selected_delivery_manifest.json','delivery_visual_QA.json','freeze_gate.json','production_source_verification.json','build_delivery.py','package_sources.py','reproduce_candidates.py','HELD_NOZE_SEFIN_说明.md','make_freeze_gate.py','independent_freeze_confirmation.json',selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]
results=[]
for suffix,characters in [('A_ODO_TANSER',['odo','tanser']),('B_NOZE_SEFIN_held',['noze','sefin'])]:
    snap=D/'source_snapshots'/suffix; assert not snap.exists(),'Refuse overwrite of existing snapshot'; snap.mkdir(parents=True)
    origins={}
    for c in characters:
        for p in sorted((R/c).rglob('*')):
            if not p.is_file(): continue
            rel=p.relative_to(R).as_posix(); dst=snap/'portrait_redraw_campaign'/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,dst)
            assert sha(dst)==original_hashes[rel]
            origins[dst.relative_to(snap).as_posix()]={'kind':'production','original':rel,'sha256':original_hashes[rel]}
    for p in sorted(qa/name for name in gate['qa_files']):
        if not p.is_file(): continue
        rel=p.relative_to(R).as_posix(); dst=snap/'portrait_redraw_campaign'/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,dst)
        assert sha(dst)==original_hashes[rel]
        origins[dst.relative_to(snap).as_posix()]={'kind':'independent_qa','original':rel,'sha256':original_hashes[rel]}
    for name in common:
        shutil.copyfile(D/name,snap/name); origins[name]={'kind':'delivery','original':name,'sha256':sha(D/name)}
    with tempfile.TemporaryDirectory(dir=D,prefix='batch27-reproduce-') as tmp:
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
    js(snap/'package_inventory.json',{'package':suffix,'characters':characters,'qualified_characters':[c for c in characters if c not in ['noze','sefin']],'held_characters':[c for c in characters if c in ['noze','sefin']],'held_is_not_success':True,'commercial_reference_pixels_included':False,'self_inventory_excluded':['package_inventory.json','PACKAGE_SHA256SUMS.txt'],'files':files})
    (snap/'PACKAGE_SHA256SUMS.txt').write_text(''.join(f'{x["sha256"]}  {x["path"]}\n' for x in files)+f'{sha(snap/"package_inventory.json")}  package_inventory.json\n',encoding='utf-8')
    out=D/f'batch27_source_{suffix}.zip'; assert not out.exists(),'Refuse replacing archive'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(snap.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(snap).as_posix())
    assert out.stat().st_size<18*1024*1024
    run=subprocess.run([sys.executable,str(D/'verify_source_package.py'),str(out)],check=True,capture_output=True,text=True)
    checks=json.loads(run.stdout)
    with tempfile.TemporaryDirectory(dir=D,prefix='batch27-zip-replay-') as tmp:
        folder=Path(tmp)/'extracted'; folder.mkdir()
        with zipfile.ZipFile(out) as z: z.extractall(folder)
        replay=subprocess.run([sys.executable,str(folder/'reproduce_candidates.py'),'--output',str(Path(tmp)/'reproduced')],check=True,capture_output=True,text=True)
        assert json.loads(replay.stdout)==report
    results.append({'file':out.name,'bytes':out.stat().st_size,'MiB':round(out.stat().st_size/1024**2,3),'sha256':sha(out),'crc_all_pass':True,'member_hash_all_pass':True,'actual_extracted_zip_reproduction_all_pass':True,'reproduction':report,'checks':checks})
for rel,h in original_hashes.items(): assert sha(R/rel)==h,('Frozen source changed during packaging',rel)
js(D/'package_verification.json',{'verified_utc':datetime.now(timezone.utc).isoformat(),'production_stable_during_packaging':True,'all_pass':True,'packages':results})
attachments=[selected['board']['file']]+[x['delivery_file'] for x in selected['characters']]+[x['file'] for x in results]; assert len(attachments)==5
js(D/'upload_request.json',{'uploads':[{'local_path':str(D/n),'purpose':'create_library_file','library_artifact_type':'image' if n.endswith('.png') else 'other'} for n in attachments]})
print(json.dumps({'attachments':attachments,'packages':[{k:v for k,v in x.items() if k not in ['checks','reproduction']} for x in results],'production_stable':True},ensure_ascii=False,indent=2))
