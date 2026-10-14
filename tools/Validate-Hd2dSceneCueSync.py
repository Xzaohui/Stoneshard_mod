"""Reuse regional validators, then verify delta provenance and conditional visibility."""
from pathlib import Path
import json,hashlib,importlib.util,contextlib,io,copy,argparse
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013';C=P/'batches/Scene-cues-20261014-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--batch',choices=['R01-camp-canal-v2','R02-river-v2']);args=ap.parse_args()
    pam=module('cue_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(C)
    (C/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');assert passed,'Cue skill validator'
    cm=read(C/'manifest.json');cb=read(C/'brief.json');cl=read(C/'generation-log.json')
    assert all(sha(ROOT/n)==h for n,h in cb['source_sha256'].items()),'Cue story snapshot changed'
    assert sha(C/cl['records'][0]['output'])==cl['records'][0]['output_sha256']
    palettes=read(C/'palettes/shared.json')['regional_palettes']
    for a in cm['assets']:
        assert sha(C/a['path'])==a['sha256'];im=Image.open(C/a['path']);colors={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in palettes[a['palette']]}
        assert list(im.size)==a['size'] and im.mode=='RGBA';assert all(v[3] in [0,255] and (not v[3] or v[:3] in colors) for v in im.get_flattened_data())
    cm['status']='static_export_verified_runtime_unverified';write(C/'manifest.json',cm)
    write(C/'validation.json',dict(passed=True,requested_skill_validator=True,production_pngs=6,generated_masters=1,source_current=True,runtime_verified=False))
    for batch,validator in [('R01-camp-canal-v2','Validate-Hd2dR01.py'),('R02-river-v2','Validate-Hd2dR02.py')]:
        if args.batch and args.batch!=batch:continue
        folder=P/'batches'/batch;v=module('cue_base_'+batch.replace('-','_'),ROOT/'tools'/validator);v.P=folder;buf=io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:v.main()
            except SystemExit as e:assert e.code==0,buf.getvalue()
        (folder/'notes/base-validation.json').write_text(buf.getvalue(),encoding='utf-8');report=read(folder/'validation.json');m=read(folder/'manifest.json');old=P/'batches'/m['supersedes']['batch'];om=read(old/'manifest.json');checks=[];errors=[]
        def check(value,key):(checks if value else errors).append(key)
        check(sha(old/'manifest.json')==m['supersedes']['manifest_sha256'],'immutable-parent-manifest')
        check(sorted(m['inventory_requests'])==m['supersedes']['inventory_requests']==sorted(om['inventory_requests']),'same-view-slot-scope')
        check(sha(folder/'spec_lock.md')==sha(old/'spec_lock.md'),'inherited-generation-lock-preserved')
        check(m['source_review']['geometry_unchanged'] and not m['source_review']['NPC_files_edited'],'scene-only-scope')
        oldscenes={s['id']:s for s in om['scenes']}
        for s in m['scenes']:
            clean=copy.deepcopy(s);clean.pop('scene_cues',None);check(clean==oldscenes[s['id']],'unchanged-geometry-'+s['id'])
        for n,h in m['inherited_assets'].items():
            check(sha(old/n)==h,'original-asset-preserved-'+n)
            if n not in m['replaced_asset_paths']:check(sha(folder/n)==h,'inherited-byte-identical-'+n)
        ext=read(folder/'generation-log.json')['external_generation_records'][0]
        for key,hkey in [('prompt','prompt_sha256'),('output','output_sha256'),('spec_lock','spec_lock_sha256')]:check(sha(folder/ext[key])==ext[hkey],'cue-provenance-'+key)
        check(ext['inputs']==[] and ext['transparent_background'],'new-transparent-master-no-commercial-input')
        check(ext['output_sha256']==cl['records'][0]['output_sha256'],'same-shared-master')
        check({a['id'] for a in m['assets'] if 'scene_cue_role' in a}==set(m['cue_contract']['selected_sprite_ids']),'six-cues-split-by-region')
        ids={a['id']:a for a in m['assets']};cues=[]
        for s in m['scenes']:
            rid=s['id'];cs=v.cells(s) if hasattr(v,'cells') else {(x,y) for a,b,c,d in s['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}-{(x,y) for a,b,c,d in s['blocked_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
            for c in s.get('scene_cues',[]):
                cues.append(c);check(tuple(c['cell']) in cs,'cue-foot-on-land-'+c['id']);check(c['collision'] is None,'cue-no-invented-collision-'+c['id']);check(c['pixel_anchor']==[c['cell'][i]*26+13+c['pixel_offset'][i] for i in range(2)],'cue-placement-formula-'+c['id'])
                if c['condition']:check(not c['default_visible'] and c['condition']['default'] is False,'conditional-off-by-default-'+c['id'])
            if not s.get('scene_cues'):continue
            for name in {c['render_layer'] for c in s['scene_cues']}:
                layer=Image.open(folder/f'assets/backgrounds/{rid}__{name}.png');check(layer.getchannel('A').getbbox() is not None,'nonempty-cue-layer-'+rid+'-'+name)
                for e in s.get('door_clear_boxes',[]):
                    a,b,c,d=e['rect'];check(layer.getchannel('A').crop((a,b,c+1,d+1)).getbbox() is None,'cue-clear-door-'+rid+'-'+e['exit'])
            if all(not c['default_visible'] for c in s['scene_cues']):
                check(sha(folder/f'assets/backgrounds/{rid}__environment.png')==sha(old/f'assets/backgrounds/{rid}__environment.png'),'default-scene-unchanged-'+rid)
                q=Image.open(folder/f'assets/backgrounds/{rid}__conditional_environment.png');base=Image.open(folder/f'assets/backgrounds/{rid}__environment.png');check(ImageChops.difference(q.convert('RGB'),base.convert('RGB')).getbbox() is not None,'conditional-scene-distinct-'+rid)
        if batch.startswith('R02'):
            byid={c['id']:c for c in cues};check(byid['r02_red_water_buckets']['bucket_count']==2,'exact-two-red-buckets-metadata')
            check(byid['r02_bridge_note']['parent_instance']=='r02_repair__r02_road_sign__2','note-overlays-existing-sign')
            check(byid['r02_bridge_note']['condition']['id']=='SQ04_refusal_return_visit' and 'transport_harm' in byid['r02_bridge_note']['condition']['description'],'note-condition-preserves-harm')
            check(byid['r02_rope_shoe_stall']['condition']['id']=='N18_return_visit','shoe-stall-return-condition')
        report.update(date='2026-10-14',new_generated_masters=len(read(folder/'generation-log.json')['records'])+1,shared_cue_master_sha256=ext['output_sha256'],independent_sprites=sum(a['role']=='independent_environment_sprite' for a in m['assets']),delta_checks_passed=len(checks),checks_passed=report['checks_passed']+len(checks),errors=report['errors']+errors,passed=report['passed'] and not errors,visual_review=['Master reviewed: ordinary ash, blank sealed stub, freshly painted notice, exactly two red buckets, pair of small partly woven rope sandals, paper with nail only'],asset_manifest_sha256=sha(folder/'manifest.json'))
        write(folder/'validation.json',report);print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','delta_checks_passed','passed','errors']},ensure_ascii=False));assert report['passed'],batch
if __name__=='__main__':main()
