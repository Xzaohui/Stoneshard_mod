"""Validate all22 R06 view outputs, routes, splits and provenance; never native runtime."""
from pathlib import Path
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(s):
    def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
    return rc(s['walkable_rectangles'])-rc(s['blocked_rectangles'])
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
    rgb={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/hig_r06_128.json')['colors']};check(len(rgb)==128,'fixed128color-palette');check(m['native_cell_size']==26,'26pixel-cell');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids')
    for a in m['assets']:
        rel=Path(a['path']);f=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(f.is_file() and sha(f)==a['sha256'],'sha-'+a['id']);q=Image.open(f);check(q.mode=='RGBA' and q.format=='PNG','format-'+a['id']);check(list(q.size)==a['size'],'size-'+a['id']);pixels=set(q.get_flattened_data());check(all(c[3] in [0,255] for c in pixels),'binary-alpha-'+a['id']);check(all(c[:3] in rgb for c in pixels if c[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],q.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):
            box=q.getchannel('A').getbbox();check(box is not None and box[3]==a['origin'][1],'foot-baseline-'+a['id'])
    expected_scene_ids={'r06_'+x for x in ['station','echo','residual','sign','shed','trial','table','seal','drain','slope','station_hall','shed_room','table_hall','echo_front','echo_maintenance','residual_main','residual_safe','residual_maintenance']};byid={s['id']:s for s in m['scenes']};check(set(byid)==expected_scene_ids,'ten-sites-eight-independent-interiors')
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
    echo=byid['r06_echo_front'];main=byid['r06_residual_main'];check(echo['cells']==[42,30] and echo['asymmetric_measurement_positions']==[[9,9],[23,7],[33,13]],'D09-42x30-three-asymmetric-measurement-stations')
    check(echo['safety_line_rectangles']==[[5,5,12,13]],'D09-safety-white-line');check({'r06_cooling_gauge','r06_return_valve','r06_residual_gauge','r06_medium_niche'}<=set(o['id'] for o in echo['objects']),'D09-three-readings-and-sealed-medium-separate')
    remote=byid['r06_echo_maintenance'];check(remote['no_echo_entry_required'] and remote['maintenance_return_always'] and {'cooling_remote','return_remote','residual_remote'}<=set(e['id'] for e in remote['reserved']),'D09-independent-remote-method-and-return')
    check(main['cells']==[48,40] and len(main['outer_ring_rectangles'])==4,'D10-48x40-double-ring')
    outer={(x,y) for a,b1,c,d in main['outer_ring_rectangles'] for y in range(b1,d+1) for x in range(a,c+1)};seen=reach(outer,tuple(next(e['cell'] for e in main['exits'] if e['id']=='entry')))
    for key in ['maintenance','safe_table']:check(tuple(next(e['cell'] for e in main['exits'] if e['id']==key)) in seen,'D10-outer-return-with-inner-ring-inaccessible-'+key)
    reserve={e['id']:e['cell'] for e in main['reserved']};check(reserve['carrier_rescue_space']!=reserve['boss_proposed_anchor'] and sum(abs(a-b1) for a,b1 in zip(reserve['carrier_rescue_space'],reserve['boss_proposed_anchor']))>=6,'carrier-rescue-and-boss-reservations-distinct')
    couplings=[o['cell'] for o in main['objects'] if o.get('coupling_variant')];check(couplings==[[14,16],[33,19],[24,26]] and len({p[1] for p in couplings})==3,'three-staggered-aux-couplings')
    check(any(o['id']=='r06_empty_carrier_trough' and o['cell']==[23,20] for o in main['objects']) and any(o['id']=='r06_ledger_table' and o['cell'][0]<12 for o in main['objects']),'central-empty-carrier-and-side-ledger')
    check(byid['r06_residual_safe']['ending_snapshot_not_drawn'] and byid['r06_residual_safe']['return_without_final_confirmation'] and byid['r06_station']['safe_services_outside_final_area'],'safe-confirmation-and-services-independent-of-ending-choice')
    palette=read('palettes/hig_r06_128.json');violet={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in palette['violet_colors']};check(len(violet)==8,'eight-reserved-violet-colors-from-own-concept')
    medium=Image.open(P/'assets/items/r06_medium_niche.png').convert('RGBA');check(sum(c[3]>0 and c[:3] in violet for c in medium.get_flattened_data())>=30,'violet-limited-medium-compartment-present')
    for a in m['assets']:
        if a['role'] in ['flat_wrapped_312px_material_surface_not_room','flat_edge_matched_material_variant','nonwalkable_background','exact_proposed_walkable_floor','unlit_vertical_wall_not_floor','unlit_window_patch_not_door']:
            q=Image.open(P/a['path']);check(not any(c[3] and c[:3] in violet for c in set(q.get_flattened_data())),'ordinary-materials-not-violet-'+a['id'])
    check(len([a for a in m['assets'] if a['role']=='hand_pixel_neutral_engine_control_glyph_no_state'])==8,'eight26pixel-independent-hand-glyphs')
    alt=main['illustration_variants'];check(all(v['default'] is False and v['game_state_commit'] is False and v['floor_unchanged'] is True for v in alt.values()),'coupling-warning-illustrative-default-off-no-game-state')
    base=Image.open(P/'assets/backgrounds/r06_residual_main__props_preview.png').convert('RGBA');variant=Image.open(P/alt['coupling']['props']).convert('RGBA');delta=ImageChops.difference(base,variant);allowed=Image.new('L',base.size)
    from PIL import ImageDraw
    d=ImageDraw.Draw(allowed)
    for x,y in couplings:d.rectangle((x*26+13-52,y*26+13-65,x*26+13+51,y*26+13+12),fill=255)
    check(delta.convert('RGB').getbbox() is not None and all(ImageChops.multiply(ch,ImageChops.invert(allowed)).getbbox() is None for ch in delta.split()),'disconnected-variant-changes-only-three-couplings')
    warning=Image.open(P/alt['warning']['overlay']).getchannel('A');floor=Image.open(P/'assets/backgrounds/r06_residual_main__floor.png').getchannel('A');check(warning.getbbox() is not None and ImageChops.multiply(warning,ImageChops.invert(floor)).getbbox() is None,'warning-proposal-is-separate-floor-clipped-overlay')
    for ident in ['r06_echo','r06_residual']:
        for suffix,source in [('plan_overview','plan'),('working_overview','environment')]:
            a=next(a for a in m['assets'] if a['id']==ident+'__'+suffix);q=Image.open(P/a['path']).convert('RGBA');sh=a['sheet_layout'];check(list(q.size)==sh['size'],'overview-size-'+ident+'-'+suffix)
            for rid,x,y in sh['parts']:
                room=Image.open(P/f'assets/backgrounds/{rid}__{source}.png').convert('RGBA');check(q.crop((x,y,x+room.width,y+room.height)).tobytes()==room.tobytes(),'overview-1to1-pixel-preservation-'+rid+'-'+suffix)
    for ident in [s['id'] for s in b['sprites'] if s['architecture']]:
        a=next(a for a in m['assets'] if a['id']==ident);check(a['roof_variants_pending'] is False and a['roof_variants']=={part:f'assets/items/{ident}__{part}.png' for part in ['body','roof']},'resolved-roof-variant-metadata-'+ident)
        q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(body.size==roof.size==q.size,'roof-body-canvas-'+ident);check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==q.tobytes(),'roof-body-exact-reconstruct-'+ident);check(body.getchannel('A').getbbox() is not None and roof.getchannel('A').getbbox() is not None,'nonempty-body-roof-'+ident)
    for key in ['paving','stone','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/r06_{key}_v{j}.png').convert('RGBA') for j in range(9)]
        for i,q in enumerate(tiles):
            for j,other in enumerate(tiles):check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+key+f'-{i}-{j}');check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+key+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/r06_buildings_props.png').convert('RGBA');frames=read('sheets/manifest.json')['frames'];check(len(frames)==38,'38independent-sprite-atlas-entries')
    for f in frames:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-exact-copy-'+f['id'])
    r=read('region-layout.json');source=next(s for s in json.loads((ROOT/'research/story-regions.json').read_text(encoding='utf-8')) if s['id']=='R06');check(len(r['nodes'])==10 and len(r['edges'])==11 and {frozenset(e) for e in r['edges']}=={frozenset('R06-'+n for n in e) for e in source['edges']},'ten-nodes-eleven-canonical-design-edges')
    graph={n['id']:set() for n in r['nodes']}
    for a,b1 in r['edges']:graph[a].add(b1);graph[b1].add(a)
    reachable={next(iter(graph))};todo=list(reachable)
    while todo:
        for n in graph[todo.pop()]-reachable:reachable.add(n);todo.append(n)
    check(reachable==set(graph),'all-regional-sites-connected');check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==23,'all23original-view-slots')
    for k,n in m['inventory_requests'].items():check((P/n).is_file(),'view-slot-'+k)
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'story-source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generation-output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'generation-lock-'+r['id']);check(list(Image.open(P/r['output']).size)==r['original_size'],'actual-raw-size-record-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generation-input-'+r['id']+'-'+inp['path'])
    check(any(r['id']=='r06-coupling-capped-v2' and r['selected'] for r in log['records']),'two-solid-cap-coupling-revision-selected');check(all(r.get('output_sha256') for r in log['records']),'all-generation-requests-complete')
    spec=importlib.util.spec_from_file_location('r06_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    if not errors:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(date='2026-10-14',batch=m['batch'],scope='All23view PNGs, palettes/alpha/dimensions/origins, roof reconstruction, proposed route/evidence independence and provenance; no native runtime test',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],independent_sprites=38,material_tiles=36,view_slots=23,checks_passed=len(checks),errors=errors,passed=not errors,paths=paths,asset_manifest_sha256=sha(P/'manifest.json'),runtime_verified=False,visual_review=['Three blank mechanical gauges distinct; sealed violet compartment no originalcrystal copy or baked light.','D09asymmetric white-line front and independent remote maintenance room.','D10double ring,centralempty carrier,side ledger,three staggeredcouplings,distinct actor reservations and separate safety table.','Disconnected coupling v2 has two obvious solid cap plates; raw v1 preserved.','Six roofs use reviewed source masks; eight glyphs are hand pixels and not quest outcomes.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','passed','errors']},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
