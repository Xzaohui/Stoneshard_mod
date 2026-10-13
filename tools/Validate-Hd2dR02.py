"""Validate import files, meaningful R02 route/privacy/repair invariants, never game runtime."""
from pathlib import Path
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R02-river-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(s):
    cs={(x,y) for a,b,c,d in s['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
    for a,b,c,d in s['blocked_rectangles']+s.get('cutout_rectangles',[]):cs-={(x,y) for y in range(b,d+1) for x in range(a,c+1)}
    return cs
def mask(size,cs):
    from PIL import ImageDraw
    q=Image.new('L',size);d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def reach(cs,start):
    seen={start};todo=deque([start])
    while todo:
        x,y=todo.popleft()
        for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if q in cs and q not in seen:seen.add(q);todo.append(q)
    return seen
def main():
    m=read('manifest.json');b=read('brief.json');log=read('generation-log.json');checks=[];errors=[];paths=[]
    def check(v,k):(checks if v else errors).append(k)
    cols={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/den_r02_128.json')['colors']};check(len(cols)==128,'fixed128palette');check(m['native_cell_size']==26,'26pxcells')
    check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-asset-ids')
    for a in m['assets']:
        rel=Path(a['path']);p=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id']);check(p.exists() and sha(p)==a['sha256'],'sha-'+a['id'])
        im=Image.open(p);check(im.format=='PNG' and im.mode=='RGBA','format-'+a['id']);check(list(im.size)==a['size'],'size-'+a['id']);px=set(im.get_flattened_data())
        check(all(v[3] in [0,255] for v in px),'binary-alpha-'+a['id']);check(all(v[:3] in cols for v in px if v[3]),'palette-'+a['id']);check(all(0<=x<lim for x,lim in zip(a['origin'],im.size)),'origin-'+a['id'])
        if a.get('foot_anchor'):
            bbox=im.getchannel('A').getbbox();check(bbox is not None and abs(bbox[3]-a['origin'][1])<=1,'foot-baseline-'+a['id'])
    for s in m['scenes']:
        rid=s['id'];cs=cells(s);check(s['size']==[v*26 for v in s['cells']],'grid-size-'+rid)
        expected=mask(tuple(s['size']),cs);floor=Image.open(P/f'assets/backgrounds/{rid}__floor.png').getchannel('A');check(ImageChops.difference(expected,floor).getbbox() is None,'exact-floor-alpha-'+rid)
        for layer in ['structure','foreground']:
            q=Image.open(P/f'assets/backgrounds/{rid}__{layer}.png').getchannel('A');check(ImageChops.multiply(q,expected).getbbox() is None,'no-boundary-on-floor-'+rid+'-'+layer)
            for e in s['door_clear_boxes']:
                a,b1,c,d=e['rect'];check(q.crop((a,b1,c+1,d+1)).getbbox() is None,'door-aperture-'+rid+'-'+layer+'-'+e['exit'])
        start=tuple(s['exits'][0]['cell']);seen=reach(cs,start);check(seen==cs,'all-land-connected-'+rid)
        check(len(s['exits'])==len({tuple(e['cell']) for e in s['exits']}),'distinct-door-cells-'+rid)
        check(len(s['objects'])==len({o['instance_id'] for o in s['objects']}),'distinct-prop-instances-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:check(tuple(o['cell']) in seen,'prop-foot-on-land-'+o['instance_id'])
        if s.get('repaired_add_cells'):
            repaired=cs|{tuple(x) for x in s['repaired_add_cells']};q=Image.open(P/f'assets/backgrounds/{rid}__repaired_floor.png').getchannel('A')
            check(ImageChops.difference(mask(tuple(s['size']),repaired),q).getbbox() is None,'repaired-alpha-'+rid)
            check(reach(repaired,start)==repaired,'repair-all-land-connected-'+rid)
            for layer in ['structure','foreground']:
                q=Image.open(P/f'assets/backgrounds/{rid}__repaired_{layer}.png').getchannel('A')
                check(ImageChops.multiply(q,mask(tuple(s['size']),repaired)).getbbox() is None,'no-boundary-on-repaired-floor-'+rid+'-'+layer)
            ford={(x,y) for a,b1,c,d in s.get('ford_rectangles',s.get('bridge_rectangles',[])[:1]) for y in range(b1,d+1) for x in range(a,c+1)}
            check(ford<=cs and ford<=repaired,'permanent-foot-return-kept-'+rid)
        paths.append(dict(scene=rid,walkable_cells=len(cs),reachable_cells=len(seen),repaired_add_cells=len(s.get('repaired_add_cells',[]))))
    byid={s['id']:s for s in m['scenes']};tax=byid['r02_tax_main'];check(tax['cells']==[42,32] and byid['r02_tax_yard']['cells']==[30,22],'D03-screenplay-dimensions')
    # Closing toll-house/permit approach cannot remove the independent ford.
    cs=cells(tax);closed=cs-{tuple(e['cell']) for e in tax['exits'] if e['id'] in ['yard_permit','tax_office']};seen=reach(closed,tuple(tax['exits'][0]['cell']))
    check(tuple(next(e for e in tax['exits'] if e['id']=='yard_ford')['cell']) in seen,'ford-reachable-with-permit-and-office-closed')
    check(tuple(next(e for e in tax['exits'] if e['id']=='repair')['cell']) in seen,'return-reachable-with-permit-and-office-closed')
    common=byid['r02_inn_common'];a,b1,c,d=common['private_zone'];public=cells(common)-{(x,y) for y in range(b1,d+1) for x in range(a,c+1)};seen=reach(public,tuple(common['exits'][0]['cell']))
    for key in ['public_table','case_ledger','soup_service']:check(tuple(next(e for e in common['reserved'] if e['id']==key)['cell']) in seen,'public-service-with-private-name-zone-closed-'+key)
    check(not any('bed' in o['id'] for o in common['objects']),'no-invented-inn-bed-capacity')
    well=byid['r02_well'];check(len(well['cutout_rectangles'])==3 and len([o for o in well['objects'] if o['id']=='r02_sample_bucket'])==3,'three-independent-sample-sites')
    check({'r02_case_cabinet','r02_name_cabinet'}<=set(o['id'] for o in well['objects']),'case-and-name-cabinets-separated')
    for ident in ['r02_ferry_inn','r02_tax_house','r02_filter_shelter','r02_repair_canopy','r02_inspection_shed']:
        full=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA')
        check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'roof-body-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==full.tobytes(),'roof-body-reconstruct-'+ident)
    for material in ['gravel','grass','boards','wetstone']:
        tiles=[Image.open(P/f'assets/tiles/r02_{material}_v{i}.png').convert('RGBA') for i in range(9)]
        for i,q in enumerate(tiles):
            check(q.crop((0,0,26,1)).tobytes()==q.crop((0,25,26,26)).tobytes(),'vertical-wrap-'+material+'-'+str(i))
            check(q.crop((0,0,1,26)).tobytes()==q.crop((25,0,26,26)).tobytes(),'horizontal-wrap-'+material+'-'+str(i))
            for j,other in enumerate(tiles):
                check(q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes(),'tile-y-join-'+material+'-'+str(i)+'-'+str(j))
                check(q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes(),'tile-x-join-'+material+'-'+str(i)+'-'+str(j))
    atlas=Image.open(P/'sheets/r02_buildings_props.png').convert('RGBA')
    for f in read('sheets/manifest.json')['frames']:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-copy-'+f['id'])
    region=read('region-layout.json');expected={frozenset(x) for x in [['R02-fork','R02-inn'],['R02-inn','R02-well'],['R02-well','R02-ferryold'],['R02-inn','R02-tracks'],['R02-tracks','R02-tax'],['R02-tax','R02-repair'],['R02-repair','R02-ford'],['R02-ford','R02-inn'],['R02-ford','R02-fork']]}
    check(len(region['nodes'])==8 and len(region['edges'])==9 and {frozenset(x) for x in region['edges']}==expected,'eight-nodes-nine-design-edges')
    check(m['inventory_requests']==b['inventory_requests'] and len(m['inventory_requests'])==18,'eighteen-view-slots')
    for key,path in m['inventory_requests'].items():check((P/path).is_file(),'request-'+key)
    for p,h in m['source_sha256'].items():check(sha(ROOT/p)==h,'source-'+p)
    for p,h in m['raw_sources'].items():check(sha(P/'raw'/p)==h,'immutable-raw-'+p)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'generated-output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'lock-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'input-'+r['id']+'-'+inp['path'])
    for r in log['reuse_sources']:check(sha(ROOT/r['path'])==sha(P/r['batch_copy'])==r['sha256'],'reuse-'+r['batch_copy'])
    spec=importlib.util.spec_from_file_location('pam_r02_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    report=dict(date='2026-10-14',batch=m['batch'],scope='Static PNG/palette/alpha/origin/tile seams and authored routes/privacy/repair/topology/provenance; no native runtime test',production_pngs=len(m['assets']),new_generated_masters=9,independent_sprites=18,material_tiles=36,view_slots=18,checks_passed=len(checks),errors=errors,paths=paths,passed=not errors,runtime_verified=False)
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if report['passed']:
        m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
