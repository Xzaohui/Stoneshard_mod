from pathlib import Path
from PIL import Image
import hashlib, json, shutil, base64, zipfile

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'Assets/EnemyDesigns/20261013/first_six'
OUT = Path(__file__).resolve().parent
BRIEF = json.loads((BASE / 'action_continuation_brief_v1.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def row(p,base):
    r={'path':str(p.relative_to(base)),'sha256':sha(p),'bytes':p.stat().st_size}
    if p.suffix=='.png':
        im=Image.open(p); r.update(mode=im.mode,dimensions=list(im.size))
    return r
def audit():
    for i in BRIEF['items'][-2:]:
        d=ROOT/i['planned_generation']['output_directory_if_later_executed']; role=i['role']; pose=i['proposed_keypose']['pose_id']
        raw=d/f'{role}_{pose}_raw_v1.png';selected=d/f'{role}_{pose}_transparent.png'
        args=json.loads((d/'tool_args_v1.json').read_text());ret=json.loads((d/'tool_return_v1.json').read_text())
        assert base64.b64decode(ret['image_url'].split(',',1)[1])==raw.read_bytes()
        assert selected.read_bytes()==raw.read_bytes()
        assert args['prompt']==(d/'prompt_v1.txt').read_text()==i['planned_generation']['prompt']
        assert args['transparent_background'] is True
        inputs=[]
        for r in i['planned_generation']['reference_order']:
            p=ROOT/r['path'];assert sha(p)==r['sha256'];inputs.append({**r,'current_hash_match':True,'actually_viewed':True})
        (d/'execution_log.json').write_text(json.dumps({'tool':'builtin image_gen','generation_calls':1,'hard_error_revisions_used':0,'input_images':inputs,'tool_args':row(d/'tool_args_v1.json',d),'full_tool_return':row(d/'tool_return_v1.json',d),'raw':row(raw,d),'selected':row(selected,d),'prompt':row(d/'prompt_v1.txt',d),'prompt_exactly_matches_brief_string':True,'artifact_save_note':'005 full JSON initially exceeded shell argument limit; result retained in memory and saved with apply_patch. No repeated image generation. 006 saved directly with apply_patch.','alpha_cleanup':False,'anatomy_painting':False,'git_actions':False,'uploads':False,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False},ensure_ascii=False,indent=2))
        sources=d/'sources'
        (sources/'snapshot_inventory.json').write_text(json.dumps({'files':[row(p,sources) for p in sorted(sources.rglob('*')) if p.is_file() and p.name!='snapshot_inventory.json'],'originals_modified':False},ensure_ascii=False,indent=2))
        shutil.copy2(OUT/'build_delivery.py',d/'build_delivery_reference.py')
        shutil.copy2(OUT/'audit_and_package.py',d/'audit_and_package_reference.py')
        shutil.copy2(OUT/'continuation_005_006_adjacent_light_dark_zh.png',d/'adjacent_light_dark_zh.png')
        shutil.copy2(OUT/'board_manifest.json',d/'board_manifest.json')
def package():
    deliveries=[]
    for i in BRIEF['items'][-2:]:
        d=ROOT/i['planned_generation']['output_directory_if_later_executed'];role=i['role'];pose=i['proposed_keypose']['pose_id']
        assert json.loads((d/'FINAL_STATUS.json').read_text())['selected'] is True
        files=[row(p,d) for p in sorted(d.rglob('*')) if p.is_file() and p!=d/'manifest.json']
        (d/'manifest.json').write_text(json.dumps({'schema_version':1,'concept_id':i['concept_id'],'role':role,'pose_id':pose,'status':'selected_independent_QA_passed_frozen','new_independent_keyposes':1,'generation_calls':1,'hard_error_revisions_used':0,'raw_outputs':[f'{role}_{pose}_raw_v1.png'],'selected_output':f'{role}_{pose}_transparent.png','rejected_outputs':[],'transparent_background':True,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False,'precise_anchor_registration_verified':False,'files':files},ensure_ascii=False,indent=2))
        z=OUT/f'{i["id"]}_{role}_{pose}_full_source.zip'
        with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for p in sorted(d.rglob('*')):
                if p.is_file():archive.write(p,str(Path(role)/pose/p.relative_to(d)))
        with zipfile.ZipFile(z) as archive:
            assert archive.testzip() is None
            for p in sorted(d.rglob('*')):
                if p.is_file():assert archive.read(str(Path(role)/pose/p.relative_to(d)))==p.read_bytes()
        assert z.stat().st_size<18*1024*1024
        deliveries.append(row(OUT/f'{role}_{pose}_transparent.png',OUT));deliveries.append(row(z,OUT))
    deliveries.append(row(OUT/'continuation_005_006_adjacent_light_dark_zh.png',OUT))
    (OUT/'delivery_manifest.json').write_text(json.dumps({'attachment_count':5,'new_transparent_png_count':2,'chinese_light_dark_adjacent_board_count':1,'full_source_zip_count':2,'each_zip_limit_bytes':18*1024*1024,'files':deliveries,'continuous_animation_verified':False,'runtimeVerified':False},ensure_ascii=False,indent=2))
    print(json.dumps(deliveries,ensure_ascii=False,indent=2))
if __name__=='__main__':
    import sys
    audit()
    if '--package' in sys.argv:package()
