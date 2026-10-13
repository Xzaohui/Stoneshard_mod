"""Validate importable art, authored paths and provenance, never game behavior."""
from pathlib import Path
from collections import deque
import hashlib,json,importlib.util,contextlib,io
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=read('manifest.json');layouts=read('layouts.json');log=read('generation-log.json')
    checks=[];errors=[]
    def check(v,k):(checks if v else errors).append(k)
    colors={tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in read('palettes/bry_r01_128.json')['colors']}
    check(len(colors)==128,'128-colors')
    check(len(m['assets'])==len({a['id'] for a in m['assets']}),'unique-assets')
    for a in m['assets']:
        rel=Path(a['path']);p=P/rel;check(not rel.is_absolute() and '..' not in rel.parts,'relative-'+a['id'])
        check(p.is_file() and sha(p)==a['sha256'],'sha-'+a['id']);im=Image.open(p)
        check(im.format=='PNG' and im.mode=='RGBA','format-'+a['id']);check(list(im.size)==a['size'],'size-'+a['id'])
        pixels=set(im.get_flattened_data());check(all(px[3] in (0,255) for px in pixels),'binary-alpha-'+a['id'])
        check(all(px[:3] in colors for px in pixels if px[3]),'palette-'+a['id'])
        check(0<=a['origin'][0]<im.width and 0<=a['origin'][1]<im.height,'origin-'+a['id'])
        if a.get('foot_anchor'):
            box=im.getchannel('A').getbbox();check(box is not None and abs(box[3]-a['origin'][1])<=1,'foot-baseline-'+a['id'])
    paths=[]
    for s in layouts:
        rid=s['id'];cs={(x,y) for a,b,c,d in s['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
        for a,b,c,d in s['blocked_rectangles']:cs-={(x,y) for y in range(b,d+1) for x in range(a,c+1)}
        check(s['size']==[v*26 for v in s['cells']],'grid-size-'+rid)
        mask=Image.open(P/f'guides/{rid}_walkable.png').convert('L')
        floor=Image.open(P/f'assets/backgrounds/{rid}__floor.png').getchannel('A')
        check(ImageChops.difference(mask,floor).getbbox() is None,'exact-floor-mask-'+rid)
        for layer in ['structure','foreground']:
            a=Image.open(P/f'assets/backgrounds/{rid}__{layer}.png').getchannel('A')
            check(ImageChops.multiply(a,mask).getbbox() is None,'no-floor-obstruction-'+rid+'-'+layer)
        start=tuple(s['exits'][0]['cell']);seen={start};queue=deque([start])
        while queue:
            x,y=queue.popleft()
            for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if q in cs and q not in seen:seen.add(q);queue.append(q)
        check(seen==cs,'all-walkable-connected-'+rid)
        for e in s['exits']+s['reserved']:check(tuple(e['cell']) in seen,'reachable-'+rid+'-'+e['id'])
        for o in s['objects']:
            check(tuple(o['cell']) in seen,'prop-foot-on-land-'+rid+'-'+o['id'])
            if o.get('plane_bounds'):
                a,b,c,d=o['plane_bounds'];check(all(not(a<=e['cell'][0]<=c and b<=e['cell'][1]<=d) for e in s['exits']),'building-clear-exits-'+rid+'-'+o['id'])
        paths.append(dict(scene=rid,walkable_cells=len(cs),reachable_cells=len(seen),exits=[e['id'] for e in s['exits']]))
    pump=next(s for s in layouts if s['id']=='r01_canal_pump')
    check(pump['cells']==[52,34] and next(s for s in layouts if s['id']=='r01_canal_tomb')['cells']==[36,28],'D02-screenplay-dimensions')
    check(len(pump['water_rectangles'])==2,'two-channel-footprints')
    check(all(o['id']!='r01_shelter_bedroll' for s in layouts if s['id']=='r01_canal_tomb' for o in s['objects']),'living-room-separate-from-tomb')
    for ident in ['r01_worker_shed','r01_winch_shed','r01_canal_entry']:
        full=Image.open(P/f'assets/items/{ident}.png').convert('RGBA')
        roof=Image.open(P/f'assets/items/{ident}__roof.png').convert('RGBA');body=Image.open(P/f'assets/items/{ident}__body.png').convert('RGBA')
        check(ImageChops.multiply(roof.getchannel('A'),body.getchannel('A')).getbbox() is None,'disjoint-roof-body-'+ident)
        check(Image.alpha_composite(body,roof).tobytes()==full.tobytes(),'roof-body-reconstruct-'+ident)
    for p,h in m['source_sha256'].items():check((ROOT/p).is_file() and sha(ROOT/p)==h,'source-'+p)
    for p,h in m['raw_sources'].items():check(sha(P/'raw'/p)==h,'immutable-raw-'+p)
    for rec in log['records']:
        check(sha(P/rec['prompt'])==rec['prompt_sha256'],'prompt-'+rec['id'])
        check(sha(P/rec['output'])==rec['output_sha256'],'generated-output-'+rec['id'])
        for inp in rec['inputs']:check(sha(ROOT/inp['path'])==inp['sha256'],'generated-input-'+rec['id']+'-'+inp['path'])
    check(set(m['inventory_requests'])=={'R01-camp__plan','R01-camp__exterior_or_site','R01-canal__plan','R01-canal__exterior_or_site','R01-canal__interior_or_working_space'},'five-distinct-view-slots')
    for key,path in m['inventory_requests'].items():check((P/path).exists(),'request-'+key)
    spec=importlib.util.spec_from_file_location('pam_r01_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py')
    pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');check(passed,'requested-skill-validator')
    report=dict(date='2026-10-13',batch=m['batch'],scope='PNG geometry/palette/alpha/provenance, proposed route connectivity and roof splits; no native game/NPC/runtime test',
      production_pngs=len(m['assets']),new_generated_masters=log['generation_count'],view_slots=5,checks_passed=len(checks),errors=errors,paths=paths,passed=not errors,runtime_verified=False,
      visual_review=['Three architectural silhouettes and empty-coat coffin reviewed at native size.',
        'Living side-room has a two-cell maintenance opening and stays apart from the tomb.',
        'Generated water strip repeat replaced with full existing AI-painted nonrepeating water master.',
        'Blocked shed rear footprints use dirt/stone, not visible water.',
        'Funerary niche material retained in the tomb boundary layer.'])
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if report['passed']:
        m['status']='static_export_verified_runtime_unverified';(P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
if __name__=='__main__':main()
