"""Static art/palette/grid/roof/route/provenance validation; no runtime claims."""
from pathlib import Path
from collections import deque
import hashlib,json,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-streets-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=read('manifest.json');log=read('generation-log.json');brief=read('brief.json');region=read('region-layout.json')
    checks=[];errors=[]
    def check(v,k):(checks if v else errors).append(k)
    colors={tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in read('palettes/bry_r01_128.json')['colors']}
    check(len(colors)==128,'fixed-128-colors');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-assets')
    check(m['native_cell_size']==26,'native-26px-cells')
    for a in m['assets']:
        rel=Path(a['path']);p=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id'])
        check(p.is_file() and sha(p)==a['sha256'],'sha-'+a['id']);im=Image.open(p)
        check(im.format=='PNG' and im.mode=='RGBA','format-'+a['id']);check(list(im.size)==a['size'],'size-'+a['id'])
        px=set(im.get_flattened_data());check(all(v[3] in (0,255) for v in px),'binary-alpha-'+a['id']);check(all(v[:3] in colors for v in px if v[3]),'palette-'+a['id'])
        check(0<=a['origin'][0]<im.width and 0<=a['origin'][1]<im.height,'origin-'+a['id'])
        if a.get('foot_anchor'):
            box=im.getchannel('A').getbbox();check(box is not None and abs(box[3]-a['origin'][1])<=1,'foot-baseline-'+a['id'])
    paths=[]
    for s in m['scenes']:
        rid=s['id'];cs={(x,y) for a,b,c,d in s['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
        for a,b,c,d in s['blocked_rectangles']:cs-={(x,y) for y in range(b,d+1) for x in range(a,c+1)}
        check(s['size']==[v*26 for v in s['cells']],'grid-size-'+rid)
        mask=Image.open(P/f'guides/{rid}_walkable.png').convert('L');floor=Image.open(P/f'assets/backgrounds/{rid}__floor.png').getchannel('A')
        check(ImageChops.difference(mask,floor).getbbox() is None,'exact-floor-mask-'+rid)
        for layer in ['structure','foreground']:
            a=Image.open(P/f'assets/backgrounds/{rid}__{layer}.png').getchannel('A');check(ImageChops.multiply(a,mask).getbbox() is None,'no-floor-obstruction-'+rid+'-'+layer)
            for e in s['door_clear_boxes']:check(a.crop(e['rect']).getbbox() is None,'boundary-door-clear-'+rid+'-'+layer+'-'+e['exit'])
        start=tuple(s['exits'][0]['cell']);seen={start};queue=deque([start])
        while queue:
            x,y=queue.popleft()
            for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if q in cs and q not in seen:seen.add(q);queue.append(q)
        check(seen==cs,'all-land-connected-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:check(tuple(o['cell']) in seen,'prop-foot-on-land-'+rid+'-'+o['id'])
        paths.append(dict(scene=rid,walkable_cells=len(cs),reachable_cells=len(seen),exits=[e['id'] for e in s['exits']]))
    for ident in ['r01_port_kiosk','r01_hearing_canopy','r01_rental_house','r01_forge_building','r01_abandoned_post']:
        full=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA')
        check(ImageChops.multiply(roof.getchannel('A'),body.getchannel('A')).getbbox() is None,'disjoint-body-roof-'+ident)
        check(Image.alpha_composite(body,roof).tobytes()==full.tobytes(),'reconstruct-body-roof-'+ident)
        check(full.size==body.size==roof.size,'same-layer-canvas-'+ident)
    hearing=next(s for s in m['scenes'] if s['id']=='r01_hearing');workshop=next(s for s in m['scenes'] if s['id']=='r01_workshop');rental=next(s for s in m['scenes'] if s['id']=='r01_rental')
    check(any(e['id']=='rental_private' for e in hearing['exits']) and len(hearing['exits'])==4,'three-public-exits-plus-private-rental')
    check(set(o['id'] for o in rental['objects'])=={'r01_twin_ledger_table','r01_drying_rack','r01_ash_stove'},'rental-working-room-no-invented-beds')
    check({'r01_forge_building','r01_basic_repair_bench','r01_stamp_bench'}<=set(o['id'] for o in workshop['objects']),'large-forge-basic-repair-printing-separate')
    expected={frozenset(x) for x in [['R01-salt','R01-port'],['R01-port','R01-camp'],['R01-camp','R01-hearing'],['R01-camp','R01-canal'],['R01-canal','R01-workshop'],['R01-workshop','R01-hearing'],['R01-hearing','R01-port']]}
    check(len(region['edges'])==7 and {frozenset(x) for x in region['edges']}==expected,'seven-R01-schematic-edges')
    check(len(region['nodes'])==6 and set(region['art_anchor_pixels'])==set(n['id'] for n in region['nodes']),'six-schematic-nodes')
    check(region['size']==[1664,1248] and region['runtime_verified'] is False,'schematic-not-runtime-room')
    for key,point in region['art_anchor_pixels'].items():check(0<=point[0]<1664 and 0<=point[1]<1248,'map-anchor-'+key)
    atlas=Image.open(P/'sheets/r01_streets_architecture_props.png').convert('RGBA')
    for f in read('sheets/manifest.json')['frames']:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f'assets/items/{f["id"]}.png').convert('RGBA').tobytes(),'atlas-reconstruct-'+f['id'])
    for p,h in m['source_sha256'].items():check((ROOT/p).is_file() and sha(ROOT/p)==h,'source-'+p)
    for p,h in m['raw_sources'].items():check(sha(P/'raw'/p)==h,'immutable-raw-'+p)
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'output-'+r['id'])
        check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'generation-lock-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'input-'+r['id']+'-'+inp['path'])
    for r in log['reuse_sources']:check(sha(ROOT/r['path'])==sha(P/r['batch_copy'])==r['sha256'],'reuse-'+r['batch_copy'])
    check(m['inventory_requests']==brief['inventory_requests'] and len(m['inventory_requests'])==9,'nine-view-slots')
    for key,path in m['inventory_requests'].items():check((P/path).exists(),'request-'+key)
    spec=importlib.util.spec_from_file_location('pam_streets_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    report=dict(date='2026-10-13',batch=m['batch'],scope='Static PNG imports, authored grid proposals, paths, roof splits, schematic topology and provenance; no native game/NPC test',production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],view_slots=9,checks_passed=len(checks),errors=errors,paths=paths,passed=not errors,runtime_verified=False,
      visual_review=['Five south-facing structures and eight independent props inspected before and after normalization.',
      'Dry ground replaces the generated port guide pools; all actual floors use exact authored masks.',
      'Rental stove/desk/drying sheets separate; no invented bedroom.',
      'Public hearing exits remain separate from private rental; basic repair remains distinct from furnace.',
      'Regional map follows seven design edges but does not register native world coordinates.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if report['passed']:
        m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
