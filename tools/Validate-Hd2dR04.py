"""Validate all22 R04 view outputs, routes, splits and provenance; never native runtime."""
from pathlib import Path
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R04-pass-v1'
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
    rgb={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/pas_r04_128.json')['colors']};check(len(rgb)==128,'fixed128color-palette');check(m['native_cell_size']==26,'26pixel-cell');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids')
    for a in m['assets']:
        rel=Path(a['path']);f=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(f.is_file() and sha(f)==a['sha256'],'sha-'+a['id']);q=Image.open(f);check(q.mode=='RGBA' and q.format=='PNG','format-'+a['id']);check(list(q.size)==a['size'],'size-'+a['id']);pixels=set(q.get_flattened_data());check(all(c[3] in [0,255] for c in pixels),'binary-alpha-'+a['id']);check(all(c[:3] in rgb for c in pixels if c[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],q.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):
            box=q.getchannel('A').getbbox();check(box is not None and box[3]==a['origin'][1],'foot-baseline-'+a['id'])
    expected_scene_ids={'r04_'+x for x in ['inn','cellar','scale','mason','cart','camp','drug','market','seal','bypass','inn_hall','inn_care','cellar_main','cellar_oil','cellar_damaged','cellar_ditch']};byid={s['id']:s for s in m['scenes']};check(set(byid)==expected_scene_ids,'ten-sites-six-interiors')
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
    main=byid['r04_cellar_main'];check(main['cells']==[40,32] and main['axis_rect']==[2,14,37,18],'D06-long-axis40x32');check(main['oil_separate_scene']=='r04_cellar_oil' and byid['r04_cellar_oil']['optional_hazard'] and byid['r04_cellar_oil']['core_evidence_not_here'],'oil-room-independent-optional-no-core-proof')
    closed=cells(main)-{tuple(e['cell']) for e in main['exits'] if e['id'] in ['authorized_yard','oil_room']};a,b1,c,d=main['paired_zone'];closed-={(x,y) for y in range(b1,d+1) for x in range(a,c+1)};seen=reach(closed,tuple(next(e['cell'] for e in main['exits'] if e['id']=='damaged_store')))
    for k in ['ditch','damaged_store']:check(tuple(next(e['cell'] for e in main['exits'] if e['id']==k)) in seen,'return-with-official-pair-oil-closed-'+k)
    for k in ['numbered_cabinets','stop_log','neutral_record']:check(tuple(next(e['cell'] for e in main['reserved'] if e['id']==k)) in seen,'alternate-evidence-stays-reachable-'+k)
    inn=byid['r04_inn_care'];check(inn['bedding_proposal']==1 and sum(o['id']=='r04_empty_bed' for o in inn['objects'])==1,'one-inn-care-bed-proposal');check(sum(o['id']=='r04_two_medicine_bowls' for o in inn['objects'])==1,'one-sprite-exact-two-medicine-bowls')
    check({'r04_drug_cabinet','r04_return_mail_cabinet'}<=set(o['id'] for o in byid['r04_inn_hall']['objects']) and any(o['id']=='r04_case_cabinet' for o in inn['objects']),'medicine-mail-cases-visually-separated')
    check(any(o['id']=='r04_sealed_pair' for o in main['objects']) and not any(o['id']=='r04_sealed_pair' for s in m['scenes'] if s['id']!=main['id'] for o in s['objects']),'stopped-assembly-only-in-paired-room')
    check(byid['r04_drug']['id']!=byid['r04_cart']['id'] and byid['r04_drug']['objects']!=byid['r04_cart']['objects'],'unloading-and-cart-distinct-scenes');bypass=byid['r04_bypass'];check({'R02_pending','R03_pending','R05_pending'}<=set(e['id'] for e in bypass['exits']),'three-cross-region-interfaces-proposed')
    for s in ['r04_camp','r04_bypass']:
        check(len(byid[s]['exits'])>=2 and reach(cells(byid[s]),tuple(byid[s]['exits'][0]['cell']))==cells(byid[s]),'ordinary-camp-and-bypass-return-'+s)
    for ident in [s['id'] for s in b['sprites'] if s['architecture']]:
        a=next(a for a in m['assets'] if a['id']==ident);check(a['roof_variants_pending'] is False and a['roof_variants']=={part:f'assets/items/{ident}__{part}.png' for part in ['body','roof']},'resolved-roof-variant-metadata-'+ident)
        q=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(body.size==roof.size==q.size,'roof-body-canvas-'+ident);check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==q.tobytes(),'roof-body-exact-reconstruct-'+ident);check(body.getchannel('A').getbbox() is not None and roof.getchannel('A').getbbox() is not None,'nonempty-body-roof-'+ident)
    for key in ['cobble','brick','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/r04_{key}_v{j}.png').convert('RGBA') for j in range(9)]
        for i,q in enumerate(tiles):
            for j,other in enumerate(tiles):check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+key+f'-{i}-{j}');check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+key+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/r04_buildings_props.png').convert('RGBA');frames=read('sheets/manifest.json')['frames'];check(len(frames)==29,'29independent-sprite-atlas-entries')
    for f in frames:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-exact-copy-'+f['id'])
    r=read('region-layout.json');source=next(s for s in json.loads((ROOT/'research/story-regions.json').read_text(encoding='utf-8')) if s['id']=='R04');check(len(r['nodes'])==10 and len(r['edges'])==11 and {frozenset(e) for e in r['edges']}=={frozenset('R04-'+n for n in e) for e in source['edges']},'ten-nodes-eleven-canonical-design-edges')
    graph={n['id']:set() for n in r['nodes']}
    for a,b1 in r['edges']:graph[a].add(b1);graph[b1].add(a)
    reachable={next(iter(graph))};todo=list(reachable)
    while todo:
        for n in graph[todo.pop()]-reachable:reachable.add(n);todo.append(n)
    check(reachable==set(graph),'all-regional-sites-connected');check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==22,'all22original-view-slots')
    for k,n in m['inventory_requests'].items():check((P/n).is_file(),'view-slot-'+k)
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'story-source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generation-output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'generation-lock-'+r['id']);check(list(Image.open(P/r['output']).size)==r['original_size'],'actual-raw-size-record-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generation-input-'+r['id']+'-'+inp['path'])
    old=read('versions/materials-v1/materials-manifest.json')
    for a in old['assets']:check(sha(P/'versions/materials-v1'/a['path'])==a['sha256'],'old-material-retained-'+a['id'])
    check(read('materials-manifest.json')['selected_material_master']=='r04-materials-v2','fine-scale-material-edit-selected');check(any(r['id']=='r04-props-b-v2' and r['selected'] for r in log['records']),'four-row-medicine-cabinet-edit-selected')
    spec=importlib.util.spec_from_file_location('r04_skill_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    if not errors:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(date='2026-10-14',batch=m['batch'],scope='All22view PNGs, palettes/alpha/dimensions/origins, roof reconstruction, proposed route/evidence independence and provenance; no native runtime test',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],independent_sprites=29,material_tiles=36,view_slots=22,checks_passed=len(checks),errors=errors,passed=not errors,paths=paths,asset_manifest_sha256=sha(P/'manifest.json'),runtime_verified=False,visual_review=['Medicine cabinet v2 has12blank drawers, one empty care bed and exactly two medicine bowls; no inventory/cure claim.','Stopped treatment bed and empty carrier trough remain distinct; no patient drawn.','Material v2 reduces oversized paving features; v1snapshot retained.','Six roofs use explicit source polygons and unchanged silhouette canvases.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['batch','production_pngs','checks_passed','passed','errors']},ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
