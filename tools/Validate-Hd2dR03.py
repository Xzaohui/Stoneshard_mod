"""Static R03 art checks, including alternative routes and state-free source records."""
from pathlib import Path
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R03-maen-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cells(s):return {(x,y) for a,b,c,d in s['walkable_rectangles'] for x in range(a,c+1) for y in range(b,d+1)}-{(x,y) for a,b,c,d in s['blocked_rectangles'] for x in range(a,c+1) for y in range(b,d+1)}
def reach(cs,start):
    seen={start};q=deque([start])
    while q:
        x,y=q.popleft()
        for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if v in cs and v not in seen:seen.add(v);q.append(v)
    return seen
def main():
    m=read('manifest.json');brief=read('brief.json');log=read('generation-log.json');good=[];errors=[];paths=[]
    def check(ok,n):(good if ok else errors).append(n)
    cols={tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/mae_r03_128.json')['colors']}
    check(len(cols)==128,'fixed128palette');check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-assets');check(m['native_cell_size']==26,'26pxcells')
    for a in m['assets']:
        p=P/a['path'];im=Image.open(p);check(im.mode=='RGBA','RGBA-'+a['id']);check(list(im.size)==a['size'],'size-'+a['id']);check(sha(p)==a['sha256'],'sha-'+a['id'])
        px=list(im.get_flattened_data());check(set(v[3] for v in px)<={0,255},'binary-alpha-'+a['id']);check(set(v[:3] for v in px if v[3])<=cols,'palette-'+a['id']);check(not a['runtime_verified'],'no-false-runtime-'+a['id'])
        if a['role']=='independent_environment_sprite':
            bbox=im.getchannel('A').getbbox();check(bool(bbox) and bbox[3]==a['origin'][1],'foot-baseline-'+a['id']);check(a['foot_anchor']==a['origin'],'foot-origin-'+a['id']);check(a['collision'].startswith('Explicit'),'explicit-collision-'+a['id'])
    check(len(m['scenes'])==18,'eighteen-scenes');byid={s['id']:s for s in m['scenes']}
    for s in m['scenes']:
        cs=cells(s);start=tuple(s['exits'][0]['cell']);seen=reach(cs,start);check(start in cs and seen==cs,'all-cells-connected-'+s['id']);paths.append(dict(scene=s['id'],walkable_cells=len(cs),reachable_cells=len(seen)))
        check(len({tuple(e['cell']) for e in s['exits']})==len(s['exits']),'distinct-exits-'+s['id']);check(len({o['instance_id'] for o in s['objects']+s.get('conditional_objects',[])})==len(s['objects']+s.get('conditional_objects',[])),'instance-ids-'+s['id'])
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in cs,'point-walkable-'+s['id']+'-'+e['id'])
        fm=Image.open(P/f"assets/backgrounds/{s['id']}__floor.png").getchannel('A');expected=Image.new('L',tuple(s['size']));from PIL import ImageDraw
        d=ImageDraw.Draw(expected)
        for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
        check(fm.tobytes()==expected.tobytes(),'exact-floor-mask-'+s['id'])
        for part in ['structure','foreground']:
            im=Image.open(P/f"assets/backgrounds/{s['id']}__{part}.png").getchannel('A');check(ImageChops.multiply(im,fm).getbbox() is None,'nonwalkable-boundary-'+s['id']+'-'+part)
            for e in s['door_clear_boxes']:
                a,b,c,d1=e['rect'];check(im.crop((a,b,c+1,d1+1)).getbbox() is None,'clear-door-'+s['id']+'-'+part+'-'+e['exit'])
    lib=byid['r03_library_store'];check(lib['cells']==[36,30] and {z['id'] for z in lib['zones']}=={'front','dry','sealed','waste'},'D04-size-four-zones')
    check({o['id'] for o in lib['objects']} >= {'r03_technical_cabinet','r03_name_cabinet','r03_stop_cabinet'},'three-separate-D04-cabinets')
    cs=cells(lib)-{tuple(next(e for e in lib['exits'] if e['id']=='formal_front')['cell'])};start=tuple(next(e for e in lib['exits'] if e['id']=='waste_annex')['cell']);seen=reach(cs,start)
    check(tuple(next(e for e in lib['exits'] if e['id']=='unloading_return')['cell']) in seen and tuple(next(e for e in lib['reserved'] if e['id']=='outside_copy')['cell']) in seen,'D04-alternate-and-return-with-formal-door-denied')
    court=byid['r03_court'];check(court['cells']==[44,34] and len(court['annexes'])==4,'D05-size-four-annexes')
    check(len({(a['rect'][2]-a['rect'][0]+1,a['rect'][3]-a['rect'][1]+1) for a in court['annexes']})==4,'D05-four-asymmetric-footprints')
    check({a['material'] for a in court['annexes']}=={'earth','slate','boards','charred'},'D05-distinct-floor-materials');check({a['window_direction'] for a in court['annexes']}=={'north','west','east'},'D05-window-directions')
    for a in court['annexes']:
        x,y,w,h=a['window_rect'];im=Image.open(P/'assets/backgrounds/r03_court__structure.png').getchannel('A');check(im.crop((x,y,x+w,y+h)).getbbox() is not None,'visible-annex-window-'+a['id'])
    a,b,c,d=court['optional_central_zone'];cs=cells(court)-{(x,y) for x in range(a,c+1) for y in range(b,d+1)};cs-= {tuple(next(o for o in court['objects'] if o['id']=='r03_feed_lever')['cell'])};seen=reach(cs,tuple(court['exits'][0]['cell']))
    for e in court['exits'][1:]:check(tuple(e['cell']) in seen,'D05-perimeter-no-central-no-feed-'+e['id'])
    mill=byid['r03_mill_common'];check(mill['bed_capacity_proposal']==2 and sum(o['id']=='r03_bedroll' for o in mill['objects'])==2,'finite-two-bedroll-proposal')
    for key in ['r03_mill_common','r03_ration_hall','r03_scribe_room']:
        check({'r03_technical_cabinet','r03_name_cabinet'}<={o['id'] for o in byid[key]['objects']},'neutral-technical-identity-separation-'+key)
    check(not byid['r03_ration'].get('conditional_objects'),'no-second-outdoor-care-chair')
    check(len(byid['r03_ration_hall']['conditional_objects'])==1 and byid['r03_ration_hall']['conditional_objects'][0]['id']=='r03_care_chair','single-care-chair-only-conditional')
    check(sum(o['id']=='r03_care_chair' for s in m['scenes'] for o in s['objects']+s.get('conditional_objects',[]))==1,'one-chair-placement-across-entire-batch')
    check(len(list((P/'assets').rglob('*.png')))==len(m['assets']),'no-unregistered-production-png')
    for ident in ['r03_mill_house','r03_granary','r03_low_library','r03_scribe_shed','r03_watch_shelter']:
        full=Image.open(P/f'assets/items/{ident}.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA');roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');check(ImageChops.multiply(body.getchannel('A'),roof.getchannel('A')).getbbox() is None,'body-roof-disjoint-'+ident);check(Image.alpha_composite(body,roof).tobytes()==full.tobytes(),'body-roof-reconstruct-'+ident)
    for material in ['earth','slate','boards','charred']:
        ts=[Image.open(P/f'assets/tiles/r03_{material}_v{i}.png').convert('RGBA') for i in range(9)]
        for i,t in enumerate(ts):
            for j,u in enumerate(ts):check(t.crop((0,0,26,1)).tobytes()==u.crop((0,25,26,26)).tobytes(),'tile-y-'+material+f'-{i}-{j}');check(t.crop((0,0,1,26)).tobytes()==u.crop((25,0,26,26)).tobytes(),'tile-x-'+material+f'-{i}-{j}')
    atlas=Image.open(P/'sheets/r03_buildings_props.png').convert('RGBA')
    for f in read('sheets/manifest.json')['frames']:
        x,y,w,h=f['rect'];check(atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(P/f"assets/items/{f['id']}.png").convert('RGBA').tobytes(),'atlas-copy-'+f['id'])
    reg=read('region-layout.json');source=json.loads((ROOT/'research/story-regions.json').read_text(encoding='utf-8'));r=next(x for x in source if x['id']=='R03');check(len(reg['nodes'])==12 and len(reg['edges'])==13 and {frozenset(x) for x in reg['edges']}=={frozenset(['R03-'+a,'R03-'+b]) for a,b in r['edges']},'twelve-nodes-thirteen-source-edges')
    check(len(m['inventory_requests'])==27 and m['inventory_requests']==brief['inventory_requests'],'27-view-slots')
    for n,h in m['source_sha256'].items():check(sha(ROOT/n)==h,'source-'+n)
    for n,h in m['raw_sources'].items():check(sha(P/'raw'/n)==h,'immutable-raw-'+n)
    check(log['generation_count']==10 and len(log['records'])==10,'ten-recorded-masters')
    for r in log['records']:
        check(sha(P/r['prompt'])==r['prompt_sha256'],'prompt-'+r['id']);check(sha(P/r['output'])==r['output_sha256'],'output-'+r['id']);check(sha(P/'spec_lock.md')==r['spec_lock_sha256'],'lock-'+r['id'])
        for inp in r['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'pre-call-input-'+r['id']+'-'+inp['path'])
    spec=importlib.util.spec_from_file_location('pam_r03_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):ok=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(ok,'requested-skill-validator')
    report=dict(date='2026-10-14',batch=m['batch'],scope='Static assets and authored alternative routes/separated cabinets/conditional chair/topology; no native runtime',production_pngs=len(m['assets']),scenes=18,independent_sprites=22,material_tiles=36,view_slots=27,checks_passed=len(good),errors=errors,paths=paths,passed=not errors,runtime_verified=False)
    if report['passed']:m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report['asset_manifest_sha256']=sha(P/'manifest.json')
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
