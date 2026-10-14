"""Validate all22 R05 view outputs, routes, splits and provenance; never native runtime."""
from pathlib import Path
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(s):
    def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
    return (set(map(tuple,s['walkable_cells'])) if 'walkable_cells' in s else rc(s['walkable_rectangles']))-rc(s['blocked_rectangles'])
def reach(cs,start):
    todo=deque([start]);seen={start}
    while todo:
        x,y=todo.popleft()
        for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if q in cs and q not in seen:seen.add(q);todo.append(q)
    return seen
def main():
    m=read('manifest.json');b=read('brief.json');log=read('generation-log.json');checks=[];errors=[];paths=[]
    def check(v,key):(checks if v else errors).append(key)
    rgb={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/ash_r05_128.json')['colors']};check(len(rgb)==128,'fixed128color-palette');check(m['native_cell_size']==26,'26pixel-cell');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids')
    for a in m['assets']:
        rel=Path(a['path']);f=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(f.is_file() and sha(f)==a['sha256'],'sha-'+a['id']);q=Image.open(f);check(q.mode=='RGBA' and q.format=='PNG','format-'+a['id']);check(list(q.size)==a['size'],'size-'+a['id']);pixels=set(q.get_flattened_data());check(all(c[3] in [0,255] for c in pixels),'binary-alpha-'+a['id']);check(all(c[:3] in rgb for c in pixels if c[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],q.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):
            box=q.getchannel('A').getbbox();check(box is not None and box[3]==a['origin'][1],'foot-baseline-'+a['id'])
    expected_scene_ids={'r05_'+x for x in ['care','ward','well','village','reeds','shelter','drain','road','care_hall','care_beds','ward_main','ward_waste','ward_ritual','ward_exit','well_upper','well_middle','well_lower','well_research_refuge','well_workers_refuge','well_maintenance','shelter_room']};byid={s['id']:s for s in m['scenes']};check(set(byid)==expected_scene_ids,'eight-sites-thirteen-interior-or-exit-segments')
    for s in m['scenes']:
        rid=s['id'];cs=cells(s);check(s['size']==[a*26 for a in s['cells']],'grid-dimensions-'+rid);mask=Image.open(P/f'guides/{rid}_walkable.png').convert('L');floor=Image.open(P/f'assets/backgrounds/{rid}__floor.png').getchannel('A');check(ImageChops.difference(mask,floor).getbbox() is None,'exact-floor-mask-'+rid);seen=reach(cs,tuple(s['exits'][0]['cell']));check(seen==cs,'all-land-connected-'+rid)
        for key in ['structure','foreground']:
            q=Image.open(P/f'assets/backgrounds/{rid}__{key}.png').getchannel('A');check(ImageChops.multiply(q,mask).getbbox() is None,'boundary-outside-floor-'+rid+'-'+key)
            for e in s['door_clear_boxes']:
                a,b1,c,d=e['rect'];check(q.crop((a,b1,c+1,d+1)).getbbox() is None,'clear-door-'+rid+'-'+key+'-'+e['exit'])
        check(len(s['objects'])==len({o['instance_id'] for o in s['objects']}),'distinct-object-instances-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:check(tuple(o['cell']) in seen,'prop-foot-on-land-'+o['instance_id'])
        if s.get('window_wall_rect'):
            x,y,w,h=s['window_wall_rect'];check(y>=0 and mask.crop((x,y,x+w,y+h)).getbbox() is None,'window-entirely-outside-floor-'+rid)
        paths.append(dict(scene=rid,walkable_cells=len(cs),reachable_cells=len(seen),exits=[e['id'] for e in s['exits']]))
    main=byid['r05_ward_main'];check(main['cells']==[46,34] and main['horizontal_corridor']==[2,14,43,17],'D07-46x34-short-horizontal-corridor')
    closed=cells(main)-{tuple(e['cell']) for e in main['exits'] if e['id'] in ['ritual','waste']};seen=reach(closed,tuple(next(e['cell'] for e in main['exits'] if e['id']=='front')));check(tuple(next(e['cell'] for e in main['exits'] if e['id']=='safe_slope')) in seen,'ward-return-independent-of-ritual-waste')
    check(byid['r05_care']['basic_services_outside_ward'],'ordinary-water-care-outside-final-story-zone')
    for key,count in [('care_beds',2),('ward_main',3),('shelter_room',1)]:
        scene=byid['r05_'+key];check(scene['bedding_proposal']==count and sum(o['id']=='r05_empty_care_bed' for o in scene['objects'])==count,'finite-empty-bed-proposal-'+key)
    hall=byid['r05_care_hall'];check({'r05_case_cabinet','r05_name_cabinet'}<=set(o['id'] for o in hall['objects']),'anonymous-cases-and-private-names-separate')
    for level in ['upper','middle','lower']:
        scene=byid['r05_well_'+level];cs=cells(scene);check(scene['cells']==[38,38] and (18,18) not in cs and (19,19) not in cs,'D08-independent38x38nonwalkable-central-pit-'+level);check('maintenance' in {e['id'] for e in scene['exits']},'well-always-return-'+level)
        water=Image.open(P/f'assets/backgrounds/{scene["id"]}__water.png').getchannel('A');low=Image.open(P/f'assets/backgrounds/{scene["id"]}__water_lowered.png').getchannel('A');floor=Image.open(P/f'assets/backgrounds/{scene["id"]}__floor.png').getchannel('A');check(water.tobytes()==low.tobytes() and ImageChops.multiply(water,floor).getbbox() is None,'tide-mask-identical-outside-floor-'+level)
    lower=byid['r05_well_lower'];check(lower['separate_refuge_destinations']==['research_refuge','workers_refuge'] and len({tuple(e['cell']) for e in lower['exits'] if e['id'] in lower['separate_refuge_destinations']})==2,'two-distinct-refuge-doors-destinations')
    check(sha(P/'assets/items/r05_research_refuge_door.png')!=sha(P/'assets/items/r05_workers_refuge_door.png'),'refuge-door-visuals-distinct');check('fixed_safe_copy' in {e['id'] for e in byid['r05_well_upper']['reserved']} and any(o['id']=='r05_high_archive_shed' for o in byid['r05_well_upper']['objects']),'fixed-upper-safe-copy-and-canopy')
    check(any(o['id']=='r05_optional_parameter_shelf' for o in byid['r05_well_middle']['objects']),'optional-parameters-separate-middle-ring')
    for scene in m['scenes']:
        rid=scene['id'];variants=scene.get('illustration_variants',{})
        for key,v in variants.items():check(v['default'] is False and v['game_state_commit'] is False and v['floor_unchanged'] is True,'illustration-only-default-off-'+rid+'-'+key)
        if 'pipe' in variants:
            base=Image.open(P/f'assets/backgrounds/{rid}__props_preview.png').convert('RGBA');alt=Image.open(P/variants['pipe']['props']).convert('RGBA');delta=ImageChops.difference(base,alt);allow=Image.new('L',base.size)
            from PIL import ImageDraw
            d=ImageDraw.Draw(allow)
            for o in scene['objects']:
                if not o.get('pipe_variant'):continue
                x,y=o['cell'];d.rectangle((x*26+13-78,y*26+13-43,x*26+13+77,y*26+13+8),fill=255)
            outside=ImageChops.invert(allow);check(delta.convert('RGB').getbbox() is not None and all(ImageChops.multiply(ch,outside).getbbox() is None for ch in delta.split()),'pipe-only-new-line-art-changes-'+rid)
    for scene in m['scenes']:
        rid=scene['id'];f=P/f'assets/backgrounds/{rid}__water.png'
        if f.exists():check(ImageChops.multiply(Image.open(f).getchannel('A'),Image.open(P/f'guides/{rid}_walkable.png').convert('L')).getbbox() is None,'water-outside-floor-'+rid)
    supplement=read('notes/assembly-supplement.json');check(supplement['well_pages']==2 and supplement['room_dimensions_unchanged'] and supplement['execution_lock_sha256']==sha(P/'spec_lock.md'),'immutable-lock-two-overview-pages')
    for ident,sh in supplement['overview_layouts'].items():
        for suffix,source in [('plan_overview','plan'),('working_overview','environment')]:
            q=Image.open(P/f'assets/backgrounds/{ident}__{suffix}.png').convert('RGBA');check(list(q.size)==sh['size'],'contact-sheet-locked-size-'+ident+'-'+suffix)
            for rid,x,y in sh['parts']:
                room=Image.open(P/f'assets/backgrounds/{rid}__{source}.png').convert('RGBA');check(q.crop((x,y,x+room.width,y+room.height)).tobytes()==room.tobytes(),'contact-sheet-preserves-every-pixel-'+ident+'-'+suffix+'-'+rid)
    check(len({sha(P/f'assets/items/r05_{k}__window.png') for k in ['upper','middle','lower']})==3,'three-well-wall-window-themes')
    for ident in [s['id'] for s in b['sprites'] if s['architecture']]:
        a=next(a for a in m['assets'] if a['id']==ident);check(a['roof_variants_pending'] is False and a['roof_variants']=={part:f'assets/items/{ident}__{part}.png' for part in ['body','roof']},'resolved-roof-variant-metadata-'+ident)
        q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(body.size==roof.size==q.size,'roof-body-canvas-'+ident);check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==q.tobytes(),'roof-body-exact-reconstruct-'+ident);check(body.getchannel('A').getbbox() is not None and roof.getchannel('A').getbbox() is not None,'nonempty-body-roof-'+ident)
    for key in ['gravel','wetstone','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/r05_{key}_v{j}.png').convert('RGBA') for j in range(9)]
        for i,q in enumerate(tiles):
            for j,other in enumerate(tiles):check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+key+f'-{i}-{j}');check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+key+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/r05_buildings_props.png').convert('RGBA');frames=read('sheets/manifest.json')['frames'];check(len(frames)==40,'40independent-sprite-atlas-entries')
    for f in frames:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-exact-copy-'+f['id'])
    r=read('region-layout.json');source=next(s for s in json.loads((ROOT/'research/story-regions.json').read_text(encoding='utf-8')) if s['id']=='R05');check(len(r['nodes'])==8 and len(r['edges'])==9 and {frozenset(e) for e in r['edges']}=={frozenset('R05-'+n for n in e) for e in source['edges']},'eight-nodes-nine-canonical-design-edges')
    graph={n['id']:set() for n in r['nodes']}
    for a,b1 in r['edges']:graph[a].add(b1);graph[b1].add(a)
    reachable={next(iter(graph))};todo=list(reachable)
    while todo:
        for n in graph[todo.pop()]-reachable:reachable.add(n);todo.append(n)
    check(reachable==set(graph),'all-regional-sites-connected');check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==19,'all19original-view-slots')
    for k,n in m['inventory_requests'].items():check((P/n).is_file(),'view-slot-'+k)
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'story-source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generation-output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'generation-lock-'+r['id']);check(list(Image.open(P/r['output']).size)==r['original_size'],'actual-raw-size-record-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generation-input-'+r['id']+'-'+inp['path'])
    old=read('versions/materials-v1/materials-manifest.json')
    for a in old['assets']:check(sha(P/'versions/materials-v1'/a['path'])==a['sha256'],'old-material-retained-'+a['id'])
    check(read('materials-manifest.json')['selected_material_master']=='r05-materials-v2','fine-scale-material-edit-selected');check(all(r.get('output_sha256') for r in log['records']),'all-generation-requests-complete')
    spec=importlib.util.spec_from_file_location('r05_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    if not errors:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(date='2026-10-14',batch=m['batch'],scope='All19view PNGs, palettes/alpha/dimensions/origins, roof reconstruction, proposed route/evidence independence and provenance; no native runtime test',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],independent_sprites=40,material_tiles=36,view_slots=19,checks_passed=len(checks),errors=errors,passed=not errors,paths=paths,asset_manifest_sha256=sha(P/'manifest.json'),runtime_verified=False,visual_review=['Three38x38well rings around nonwalkablewater, distinctrefugedoors, upperfixedcopy and separatemaintenance.','D07threeempty beds and shortcorridor, oldlivingpipes retained and newwastepipe variants separate.','Fine-floor v2replaces oversizeflagstones and reducesgravelhighlights; v1snapshot preserved.','Sixindependent buildings split roofs; no NPC/capacity/consent/quest outcome drawn.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','passed','errors']},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
