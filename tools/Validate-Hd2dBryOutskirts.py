"""Validate all27 Brynn remaining art views; native runtime is explicitly unverified."""
from pathlib import Path
from collections import deque
import json,hashlib,re,importlib.util,contextlib,io
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-outskirts-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
def cells(s):return rc(s['walkable_rectangles'])-rc(s['blocked_rectangles'])
def reach(cs,start):
    todo=deque([start]);seen={start}
    while todo:
        x,y=todo.popleft()
        for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if q in cs and q not in seen:seen.add(q);todo.append(q)
    return seen
def mask(size,cs):
    q=Image.new('L',tuple(size));d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def main():
    m=read('manifest.json');b=read('brief.json');log=read('generation-log.json');checks=[];errors=[];paths=[]
    def check(v,k):(checks if v else errors).append(k)
    def im(rid,suffix):return Image.open(P/f'assets/backgrounds/{rid}__{suffix}.png').convert('RGBA')
    rgb={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/bry_outskirts_128.json')['colors']};check(len(rgb)==128,'128approved-palette');check(m['native_cell_size']==26,'26pixel-cell');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids');check({a['path'] for a in m['assets']}=={f.relative_to(P).as_posix() for f in (P/'assets').rglob('*.png')},'manifest-covers-entire-production-directory')
    for a in m['assets']:
        rel=Path(a['path']);f=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(f.is_file() and sha(f)==a['sha256'],'sha-'+a['id']);q=Image.open(f);check(q.mode=='RGBA' and q.format=='PNG','format-'+a['id']);check(list(q.size)==a['size'],'size-'+a['id']);px=set(q.get_flattened_data());check(all(c[3] in [0,255] for c in px),'binary-alpha-'+a['id']);check(all(c[:3] in rgb for c in px if c[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],q.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):check(q.getchannel('A').getbbox()[3]==a['origin'][1],'foot-baseline-'+a['id'])
        if a.get('source_path'):check(sha(ROOT/a['source_path'])==a['sha256'],'unchanged-owncore-reuse-'+a['id'])
    city=next(c for c in json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'))['cities'] if c['id']=='BRY');cont=json.loads((ROOT/'research/brynn-continuation.json').read_text(encoding='utf-8'));profiles={s['id']:s for s in city['satellites']+cont['spaces']};byid={s['id']:s for s in m['scenes']};expected={'bryo_s0'+str(i)+'_'+z for i in range(1,4) for z in ['ext','living','work']}|{'bryo_x'+str(i)+'_'+z for i in range(11,17) for z in ['ext','work']};check(set(byid)==expected,'nine-sites-21independent-zones')
    for s in m['scenes']:
        rid=s['id'];cs=cells(s);cm=mask(s['size'],cs);seen=reach(cs,tuple(s['exits'][0]['cell']));check(seen==cs,'all-proposed-terrain-connected-'+rid);check(s['size']==[a*26 for a in s['cells']],'26grid-dimensions-'+rid);check(ImageChops.difference(Image.open(P/f'guides/{rid}_walkable.png').convert('L'),cm).getbbox() is None,'current-walk-guide-'+rid);check(ImageChops.difference(im(rid,'floor').getchannel('A'),cm).getbbox() is None,'exact-floor-mask-'+rid)
        source=profiles[s['location']];check(s['source_profile']==source.get('space',dict(layout=source.get('layout'),alternative=source.get('alternative'))),'canonical-source-profile-'+rid);check(s['source_file']=='design/'+source['file'],'canonical-source-file-'+rid)
        for key in ['structure','foreground']:
            q=im(rid,key).getchannel('A');check(ImageChops.multiply(q,cm).getbbox() is None,'boundary-outside-floor-'+rid+'-'+key)
            for e in s['door_clear_boxes']:
                a,y,c,z=e['rect'];check(q.crop((a,y,c+1,z+1)).getbbox() is None,'clear-door-'+rid+'-'+key+'-'+e['exit'])
        if s.get('window_wall_rect'):
            x,y,w,h=s['window_wall_rect'];check(y>=0 and cm.crop((x,y,x+w,y+h)).getbbox() is None,'window-outside-floor-'+rid)
        check(len(s['objects'])==len({o['instance_id'] for o in s['objects']}),'distinct-object-instances-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:
            if o.get('water_object'):check(tuple(o['cell']) in rc(s.get('water_rectangles',[]))-cs,'boat-not-player-floor-'+o['instance_id'])
            elif o.get('boundary_object'):check(tuple(o['cell']) in rc(s['blocked_rectangles']),'rail-in-blocked-trial-region-'+o['instance_id'])
            elif o.get('ground_decoration'):check(tuple(o['cell']) in rc(s['salt_field_rectangles'])-cs,'ridge-in-low-field-'+o['instance_id'])
            else:check(tuple(o['cell']) in seen,'prop-foot-on-terrain-'+o['instance_id'])
        for e in s['object_canvas_rects']:
            x,y,w,h=e['rect'];check(x>=0 and y>=0 and x+w<=s['size'][0] and y+h<=s['size'][1],'complete-unclipped-instance-'+e['instance_id'])
        if s.get('fixture_block_rectangles'):
            nav=cs-rc(s['fixture_block_rectangles']);r=reach(nav,tuple(s['exits'][0]['cell']));check(r==nav,'proposed-fixture-bypass-connected-'+rid)
            for e in s['exits']+s['reserved']:check(tuple(e['cell']) in r,'fixture-bypass-interaction-'+rid+'-'+e['id'])
        if s.get('privacy_rectangles'):
            public=cs-rc(s['privacy_rectangles']);r=reach(public,tuple(s['exits'][0]['cell']));check(all(tuple(e['cell']) in r for e in s['exits']),'privacy-refusal-public-return-'+rid)
        paths.append(dict(scene=rid,terrain_cells=len(cs),reachable_cells=len(seen),proposed_fixture_cells=len(rc(s.get('fixture_block_rectangles',[]))),exits=[e['id'] for e in s['exits']]))
    for rid in ['bryo_s01_living','bryo_s02_living','bryo_s03_living']:
        s=byid[rid];beds=[o for o in s['objects'] if o['id']=='bryo_communal_bed'];check(len(beds)==2 and s['design_bed_capacity']==2,'exact-two-short-stay-beds-'+rid);check(len([o for o in s['objects'] if o['id']=='bryo_common_cookstove'])==1,'one-ordinary-stove-'+rid);boxes={e['instance_id']:e['rect'] for e in s['object_canvas_rects']};a=boxes[beds[0]['instance_id']];c=boxes[beds[1]['instance_id']];check(a[0]+a[2]<=c[0] or c[0]+c[2]<=a[0] or a[1]+a[3]<=c[1] or c[1]+c[3]<=a[1],'bed-canvases-disjoint-'+rid)
    check(byid['bryo_s01_ext']['same_location_extension_of']=='R01-camp' and byid['bryo_s01_ext']['original_R01_scene_untouched'],'S01-existing-camp-backliving-extension');check(any(o['id']=='bry_berth_canopy' for o in byid['bryo_s01_ext']['objects']),'wage-table-has-working-awning');check(any(o['id']=='bry_berth_canopy' for o in byid['bryo_s03_ext']['objects']),'dry-skeleton-has-working-awning')
    salt=byid['bryo_s02_ext'];check(not salt['water_rectangles'] and bool(salt['salt_field_rectangles']),'low-salt-soil-not-deepwater');check(ImageChops.multiply(im(salt['id'],'salt_field').getchannel('A'),im(salt['id'],'floor').getchannel('A')).getbbox() is None,'salt-field-separate-from-high-path');check(rc(salt['high_path_rectangles'])-rc(salt['blocked_rectangles'])==cells(salt),'canonical-dry-high-path')
    single=byid['bryo_x11_work'];boats=[o for s in m['scenes'] for o in s['objects'] if o['id']=='bryo_rental_skiff'];check(len(single['exits'])==1 and single['single_return_entrance'],'single-return-entry-preserved');check(len(boats)==2 and {o.get('physical_entity') for o in boats}=={'X11_single_rental_boat'},'one-boat-represented-in-two-views-not-two-boats');check(sum(o['id']=='bryo_detached_support' for o in single['objects'])==single['support_sets']==1,'exactly-one-detached-support-set');public=cells(single)-rc(single['privacy_rectangles']);check(tuple(next(e['cell'] for e in single['reserved'] if e['id']=='public_waiting')) in reach(public,tuple(single['exits'][0]['cell'])),'public-loading-wait-with-private-area-denied')
    trial=byid['bryo_x12_ext'];alley=rc(trial['public_alley_rectangles'])&cells(trial);ends=[e for e in trial['exits'] if e['id']!='trial_entry'];check(all(tuple(e['cell']) in reach(alley,tuple(ends[0]['cell'])) for e in ends),'trial-fence-independent-public-alley');check(byid['bryo_x12_work']['exact_two_material_batches'] and byid['bryo_x12_work']['exact_three_test_types'],'two-finite-batches-three-test-types')
    binding=byid['bryo_x13_work'];check(sum(o['id']=='bryo_binding_chair' for o in binding['objects'])==1,'one-restoration-seat');check({'bryo_original_page_tray','bryo_added_page_tray','bryo_sample_binding_page'}<=set(o['id'] for o in binding['objects']),'original-added-and-blank-method-pages-separate');check(sha(P/'assets/items/bryo_original_page_tray.png')!=sha(P/'assets/items/bryo_added_page_tray.png'),'original-and-added-tray-images-distinct')
    hazard=byid['bryo_x14_work'];check(not (rc(hazard['hazard_rectangles'])&cells(hazard)) and hazard['default_hazard_inaccessible'],'danger-area-closed-by-default');check(hazard['illustration_variants']['hazard']==dict(default=False,game_state_commit=False,floor_unchanged=True),'hazard-outline-default-off-no-game-change');check(im(hazard['id'],'hazard_markings').getchannel('A').getbbox() is not None,'hazard-outline-present');check(hazard['closure_is_valid_result'] and hazard['no_forced_combat'],'closed-shed-and-safe-outer-method-preserved')
    claim=byid['bryo_x15_work'];check({'bry_sealed_change_pouch','bryo_fee_dish','bryo_binding_chair'}<=set(o['id'] for o in claim['objects']) and claim['private_claim_without_public_name'] and claim['no_whole_batch_paid_baked'],'batch-purse-fee-and-private-claim-separated')
    hearing=byid['bryo_x16_work'];check(sum(o['id']=='bryo_ring_table' for o in hearing['objects'])==1 and sum(o['id']=='bryo_binding_chair' for o in hearing['objects'])==5,'one-ringtable-five-empty-chairs');check(hearing['independent_side_table'] and sum(o['id']=='bry_account_witness_table' for o in hearing['objects'])==1,'independent-side-desk');ring=Image.open(P/'assets/items/bryo_ring_table.png').convert('RGBA');check(ring.getpixel((104,60))[3]==0,'ring-table-center-actually-open')
    for s in m['scenes']:
        for o in s['objects']:
            if not o.get('surface_attachment'):continue
            check(o.get('draw_after_instance') in {v['instance_id'] for v in s['objects']},'surface-host-exists-'+o['instance_id']);sp=next(v for v in b['sprites']+b['reused_sprites'] if v['id']==o['id']);q=Image.open(P/f'assets/items/{o["id"]}.png').convert('RGBA');x=o['cell'][0]*26+13-sp['origin'][0];y=o['cell'][1]*26+13-sp['origin'][1];crop=im(s['id'],'props_preview').crop((x,y,x+q.width,y+q.height));check(all(src==dst for src,dst in zip(q.get_flattened_data(),crop.get_flattened_data()) if src[3]),'surface-object-visible-'+o['instance_id'])
    for a in [a for a in m['assets'] if a.get('sheet_layout')]:
        q=Image.open(P/a['path']).convert('RGBA');layer='plan' if a['id'].endswith('plan_overview') else 'environment';sh=a['sheet_layout'];check(list(q.size)==sh['size'],'overview-size-'+a['id'])
        for rid,x,y in sh['parts']:
            part=im(rid,layer);check(q.crop((x,y,x+part.width,y+part.height)).tobytes()==part.tobytes(),'overview-exact-native-pixels-'+a['id']+'-'+rid)
    arch=[s['id'] for s in b['sprites']+b['reused_sprites'] if s.get('architecture')];check(len(arch)==9,'eight-new-buildings-plus-one-owncore-awning')
    for ident in arch:
        a=next(a for a in m['assets'] if a['id']==ident);check(a['roof_variants_pending'] is False and a['roof_variants']=={part:f'assets/items/{ident}__{part}.png' for part in ['body','roof']},'resolved-roof-paths-'+ident);q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(q.size==body.size==roof.size,'roof-body-canvas-'+ident);check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==q.tobytes(),'roof-exact-reconstruction-'+ident);check(body.getchannel('A').getbbox() is not None and roof.getchannel('A').getbbox() is not None,'nonempty-roof-body-'+ident)
    for key in ['paving','stone','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/bry_{key}_v{j}.png').convert('RGBA') for j in range(9)]
        for i,q in enumerate(tiles):
            for j,other in enumerate(tiles):check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+key+f'-{i}-{j}');check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+key+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/bryo_buildings_props.png').convert('RGBA');sheet=read('sheets/manifest.json');check(len(sheet['frames'])==60 and list(atlas.size)==sheet['size'],'60independent-sprite-atlas')
    for f in sheet['frames']:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-unclipped-exact-'+f['id'])
    check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==27,'all27remaining-original-view-slots')
    for k,n in m['inventory_requests'].items():check((P/n).is_file(),'view-slot-'+k)
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generation-output-'+r['id']);check(sha(P/r.get('spec_lock_path','spec_lock.md'))==r['spec_lock_sha256'],'original-generation-lock-'+r['id']);check(list(Image.open(P/r['output']).size)==r['original_size'],'actual-raw-size-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generation-input-'+r['id']+'-'+inp['path'])
    check(len(log['records'])==7 and all(r.get('output_sha256') for r in log['records']),'seven-completed-masters');old=(P/'spec_lock.generation-v1.md').read_text(encoding='utf-8');new=(P/'spec_lock.md').read_text(encoding='utf-8');check(set(re.findall(r'#[0-9A-F]{6}',old))==set(re.findall(r'#[0-9A-F]{6}',new)) and '- base_size:26x26' in old and '- base_size:26x26' in new,'format-repair-preserves-palette-cell-contract');fix=read('notes/spec-lock-format-repair.json');check(sha(P/fix['original_lock'])==fix['original_lock_sha256'] and sha(P/fix['current_lock'])==fix['current_lock_sha256'],'format-repair-old-and-v2-hashes-preserved');check(sha(P/'spec_lock.md')==read('notes/reused-awning-extension.json')['current_lock_sha256'],'current-final-lock-hash')
    spec=importlib.util.spec_from_file_location('bryo_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    if not errors:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(date='2026-10-14',batch=m['batch'],scope='All27view art outputs and21authored terrain grids; fixture/return proposals, roofs, palette/alpha/atlas/1to1overviews/provenance. Native object collisions,doors/stairs/save/weather remain unverified.',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],independent_sprites=60,new_independent_sprites=48,reused_independent_sprites=12,material_tiles=36,view_slots=27,checks_passed=len(checks),errors=errors,passed=not errors,paths=paths,asset_manifest_sha256=sha(P/'manifest.json'),runtime_verified=False,visual_review=['Eight new facade silhouettes and reused owncore workingawning.','Three separate2bed livingrooms, commoncookstoves unlit; blankwage/seed/seat observables independent.','Dry boat ribs differ clearly from intact single rental skiff; one supportset and sealed flat historybag.','Two batchtrays,three testtypes and detachedcrack are discrete; lowframe not a weapon or bodytrial.','Original/additionalpage trays and sampleblank paper differ; restorationchair one.','Weak support versus fixedsafeouterbrace and closed dangerousplanks, no death/repair verdict.','One open-center ringtable,five emptychairs and independent sidetable, no actor images.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','passed','errors']},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
