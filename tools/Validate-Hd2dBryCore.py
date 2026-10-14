"""Validate authored Brynn core art, provenance and proposed routes; no native runtime."""
from pathlib import Path
from collections import deque
import json, hashlib, importlib.util, contextlib, io
from PIL import Image, ImageChops, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
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
    rgb={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/bry_core_128.json')['colors']}
    check(len(rgb)==128,'fixed128palette');check(m['native_cell_size']==26,'26pixel-cell');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids')
    for a in m['assets']:
        rel=Path(a['path']);f=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(f.is_file() and sha(f)==a['sha256'],'sha-'+a['id']);q=Image.open(f);check(q.mode=='RGBA' and q.format=='PNG','format-'+a['id']);check(list(q.size)==a['size'],'size-'+a['id']);px=set(q.get_flattened_data());check(all(c[3] in [0,255] for c in px),'binary-alpha-'+a['id']);check(all(c[:3] in rgb for c in px if c[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],q.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):check(q.getchannel('A').getbbox()[3]==a['origin'][1],'foot-baseline-'+a['id'])
    expected={'bry_d'+str(i).zfill(2)+z for i in range(1,7) for z in ['', '_a','_b']};byid={s['id']:s for s in m['scenes']};check(set(byid)==expected,'six-streets-twelve-independent-spaces')
    campaign=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));city=next(c for c in campaign['cities'] if c['id']=='BRY') if isinstance(campaign,dict) and 'cities' in campaign else next(c for c in campaign if c['id']=='BRY');nodes={n['id']:n for n in city['nodes']}
    for s in m['scenes']:
        rid=s['id'];cs=cells(s);cm=mask(s['size'],cs);check(s['size']==[a*26 for a in s['cells']],'grid-dimensions-'+rid);check(ImageChops.difference(Image.open(P/f'guides/{rid}_walkable.png').convert('L'),cm).getbbox() is None,'current-guide-'+rid);check(ImageChops.difference(im(rid,'floor').getchannel('A'),cm).getbbox() is None,'exact-floor-mask-'+rid);seen=reach(cs,tuple(s['exits'][0]['cell']));check(seen==cs,'all-land-connected-'+rid)
        for key in ['structure','foreground']:
            q=im(rid,key).getchannel('A');check(ImageChops.multiply(q,cm).getbbox() is None,'boundary-outside-floor-'+rid+'-'+key)
            for e in s['door_clear_boxes']:
                a,y,c,d=e['rect'];check(q.crop((a,y,c+1,d+1)).getbbox() is None,'clear-door-'+rid+'-'+key+'-'+e['exit'])
        check(len(s['objects'])==len({o['instance_id'] for o in s['objects']}),'distinct-object-instances-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:check(tuple(o['cell']) in seen,'prop-foot-on-land-'+o['instance_id'])
        if s.get('window_wall_rect'):
            x,y,w,h=s['window_wall_rect'];check(y>=0 and cm.crop((x,y,x+w,y+h)).getbbox() is None,'window-outside-floor-'+rid)
        for decal in s.get('wall_decal_rects',[]):
            x,y,w,h=decal['rect'];check(y>=0 and cm.crop((x,y,x+w,y+h)).getbbox() is None,'decal-on-wall-'+rid+'-'+decal['id'])
        profile=nodes[s['location']];source=profile.get('space',dict(layout=next(p['layout'] for p in city['space_plans'] if p['district']==s['location']),purpose=profile['purpose'])) if profile['kind']=='district' else profile['space'];check(s['source_profile']==source,'canonical-space-profile-'+rid)
        if rid.count('_')==2:check(len([e for e in s['exits'] if e['id'].startswith('street_')])==2,'two-street-returns-'+rid)
        else:
            public=cs-{tuple(e['cell']) for e in s['exits'] if e['id'] in ['A','B','B_west','B_east','staff_only']}-rc(s.get('staff_only_rectangles',[]));ends=[e for e in s['exits'] if e['id'].startswith('D')];check(all(tuple(e['cell']) in reach(public,tuple(ends[0]['cell'])) for e in ends),'street-route-with-private-doors-denied-'+rid)
        paths.append(dict(scene=rid,walkable_cells=len(cs),reachable_cells=len(seen),exits=[e['id'] for e in s['exits']]))
    for rid,ident in [('bry_d01_b','bry_sealed_change_pouch'),('bry_d04_a','bry_maker_mark_sample')]:
        s=byid[rid];o=next(o for o in s['objects'] if o['id']==ident);check(o.get('surface_attachment') and o.get('draw_after_instance') in {v['instance_id'] for v in s['objects']},'surface-attachment-host-'+ident);sp=next(v for v in b['sprites'] if v['id']==ident);q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');x=o['cell'][0]*26+13-sp['origin'][0];y=o['cell'][1]*26+13-sp['origin'][1];crop=im(rid,'props_preview').crop((x,y,x+q.width,y+q.height));check(all(src==dst for src,dst in zip(q.get_flattened_data(),crop.get_flattened_data()) if src[3]),'surface-attachment-visible-'+ident)
    d03=byid['bry_d03'];high=cells(d03)-rc(d03['low_walk_closed_rectangles']);check(set(map(tuple,d03['high_tide_walkable_cells']))==high,'high-tide-current-calibrated-grid');hs=reach(high,tuple(d03['exits'][0]['cell']));check(hs==high,'high-tide-all-land-connected')
    for e in d03['exits']+d03['reserved']:check(tuple(e['cell']) in hs,'high-tide-return-'+e['id'])
    for o in d03['objects']:check(tuple(o['cell']) in hs,'high-tide-prop-foot-'+o['instance_id'])
    hm=mask(d03['size'],high);check(ImageChops.difference(im('bry_d03','high_tide_floor').getchannel('A'),hm).getbbox() is None,'high-tide-floor-exact')
    for key in ['structure','foreground']:
        q=im('bry_d03','high_tide_'+key).getchannel('A');check(ImageChops.multiply(q,hm).getbbox() is None,'high-tide-boundary-outside-floor-'+key)
        for e in d03['high_tide_door_clear_boxes']:
            a,y,c,d=e['rect'];check(q.crop((a,y,c+1,d+1)).getbbox() is None,'high-tide-clear-door-'+key+'-'+e['exit'])
    check(d03['low_walk_closed_rectangles']==[[12,24,31,29]],'only-specified-middle-low-strip-closed');check(d03['illustration_variants']['tide']['default'] is False and d03['illustration_variants']['tide']['game_state_commit'] is False,'high-tide-default-off-no-game-commit')
    d02=byid['bry_d02'];check(all(tuple(p) in cells(d02) for p in d02['public_under_stair_path']),'open-middle-under-stair-route');check(rc(d02['public_stair_rectangles'])<=cells(d02),'public-stair-illustration-on-proposed-land')
    traces=byid['bry_d02_b']['wall_decal_rects'];check(len(traces)==2 and traces[0]['id']!=traces[1]['id'],'two-separate-wall-traces');check(sha(P/'assets/items/bry_soot_hand_left.png')!=sha(P/'assets/items/bry_soot_hand_right.png'),'trace-images-distinct')
    for rid in ['bry_d04','bry_d04_a']:
        s=byid[rid];public=cells(s)-rc(s['staff_only_rectangles']);ends=[e for e in s['exits'] if e['id']!='staff_only'];seen=reach(public,tuple(ends[0]['cell']));check(all(tuple(e['cell']) in seen for e in ends),'visitor-return-with-staff-area-inaccessible-'+rid)
    model=byid['bry_d05_b'];check(sum(o['id']=='bry_sluice_lever' for o in model['objects'])==2,'two-independent-sluice-levers');check(model['illustration_variants']['model']==dict(default=False,game_state_commit=False,floor_unchanged=True,real_water_unchanged=True),'dry-model-no-game-water-floor-commit')
    o=next(o for o in model['objects'] if o['id']=='bry_drain_sand_model');sp=next(s for s in b['sprites'] if s['id']==o['id']);x=o['cell'][0]*26+13-sp['origin'][0];y=o['cell'][1]*26+13-sp['origin'][1];allowed=Image.new('L',tuple(model['size']));ImageDraw.Draw(allowed).rectangle((x,y,x+sp['size'][0]-1,y+sp['size'][1]-1),fill=255);demo=im(model['id'],'model_demo').getchannel('A');check(demo.getbbox() is not None and ImageChops.multiply(demo,ImageChops.invert(allowed)).getbbox() is None,'model-demo-only-inside-model-canvas')
    hall=byid['bry_d06_a'];check([o['cell'] for o in hall['objects'] if o['id']=='bry_short_meeting_table']==[[8,10],[25,10],[16,20]],'exact-three-short-tables');a,y,c,d=hall['empty_center_rectangle'];check(im(hall['id'],'props_preview').getchannel('A').crop((a*26,y*26,(c+1)*26,(d+1)*26)).getbbox() is None,'central-floor-empty');check(sum(o['id']=='bry_unlit_memorial_lantern' for o in byid['bry_d06_b']['objects'])==3,'three-independent-unlit-lamps')
    for ident in [s['id'] for s in b['sprites'] if s['architecture']]:
        a=next(a for a in m['assets'] if a['id']==ident);check(a['roof_variants_pending'] is False and a['roof_variants']=={part:f'assets/items/{ident}__{part}.png' for part in ['body','roof']},'resolved-roof-metadata-'+ident);q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(body.size==roof.size==q.size,'roof-canvas-'+ident);check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==q.tobytes(),'roof-exact-reconstruct-'+ident);check(body.getchannel('A').getbbox() is not None and roof.getchannel('A').getbbox() is not None,'roof-body-nonempty-'+ident)
    for key in ['paving','stone','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/bry_{key}_v{j}.png').convert('RGBA') for j in range(9)]
        for i,q in enumerate(tiles):
            for j,other in enumerate(tiles):check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+key+f'-{i}-{j}');check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+key+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/bry_buildings_props.png').convert('RGBA');frames=read('sheets/manifest.json')['frames'];check(len(frames)==40 and atlas.size==(1560,3380),'40entry-unclipped-large-canvas-atlas')
    for f in frames:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-exact-copy-'+f['id'])
    r=read('region-layout.json');check(len(r['nodes'])==6 and len(r['edges'])==6,'six-mod-task-nodes-not-official-quarters');check({frozenset(e) for e in r['core_edges']}=={frozenset(e) for e in city['local_edges'] if all(k in nodes and (nodes[k]['kind']=='district' or k.endswith(('-A','-B'))) for k in e)},'canonical-core-eighteen-edges');check('four original' in r['authority'],'four-original-area-reference-boundary')
    check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==37,'37original-core-view-slots')
    for k,n in m['inventory_requests'].items():check((P/n).is_file(),'view-slot-'+k)
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'story-source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generation-output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'generation-lock-'+r['id']);check(list(Image.open(P/r['output']).size)==r['original_size'],'actual-raw-size-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generation-input-'+r['id']+'-'+inp['path'])
    check(len(log['records'])==9 and all(r.get('output_sha256') for r in log['records']),'nine-generation-requests-complete')
    spec=importlib.util.spec_from_file_location('bry_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    if not errors:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(date='2026-10-14',batch=m['batch'],scope='37coreview PNGs, dimensions/palettes/alpha/origins, roof reconstruction, proposed return paths, private-route independence and provenance; not native collision/runtime',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],independent_sprites=40,material_tiles=36,view_slots=37,checks_passed=len(checks),errors=errors,passed=not errors,paths=paths,asset_manifest_sha256=sha(P/'manifest.json'),runtime_verified=False,visual_review=['Open rental-block middle arcade and public stair illustration.','Two separated soot wall traces and no actor images.','Three short tables with central empty floor, three separate unlit lamps.','High/low dock paths, empty berth and no boat or missing-person verdict.','Two sluice levers and dry sand model with gray tray lining.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','passed','errors']},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
