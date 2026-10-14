"""Export usable flat R05 materials; do not count unfinished scenes as fulfilled views."""
from pathlib import Path
from functools import lru_cache
from collections import deque
import json,hashlib,importlib.util,contextlib,io
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cells(s):
    def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
    return (set(map(tuple,s['walkable_cells'])) if 'walkable_cells' in s else rc(s['walkable_rectangles']))-rc(s['blocked_rectangles'])
def reachable(cs,start):
    seen={start};todo=deque([start])
    while todo:
        x,y=todo.popleft()
        for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if q in cs and q not in seen:seen.add(q);todo.append(q)
    return seen
def main():
    b=read('brief.json');log=read('generation-log.json');chosen='r05-materials-v2' if any(r['id']=='r05-materials-v2' and r.get('output_sha256') for r in log['records']) else 'r05-materials-v1';r=next(r for r in log['records'] if r['id']==chosen);assert sha(P/r['output'])==r['output_sha256'] and sha(P/'spec_lock.md')==r['spec_lock_sha256'];assert all(sha(ROOT/n)==h for n,h in b['source_sha256'].items())
    palette=read('palettes/ash_r05_128.json');rgb=[tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in palette['colors']]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(im):
        q=Image.new('RGBA',im.size);q.putdata([(*nearest(c[:3]),255) for c in im.get_flattened_data()]);return q
    im=Image.open(P/r['output']).convert('RGBA');w,h=im.width//2,im.height//2;assets=[];ops=[];atlas=Image.new('RGBA',(234,104));frames=[]
    for i,key in enumerate(['gravel','wetstone','boards','earth']):
        x,y=i%2*w,i//2*h;box=[x+24,y+24,x+w-24,y+h-24];plate=im.crop(box).resize((312,312),Image.Resampling.NEAREST);plate=quant(plate)
        for a in range(312):plate.putpixel((a,311),plate.getpixel((a,0)));plate.putpixel((311,a),plate.getpixel((0,a)))
        def save(q,ident,category,role,**meta):
            rel=f'assets/{category}/{ident}.png';q.save(P/rel);assets.append(dict(id=ident,path=rel,size=list(q.size),origin=[0,0],role=role,material=key,palette='ASH-R05-128',sha256=sha(P/rel),runtime_verified=False,**meta))
        save(plate,'r05_'+key+'__material','backgrounds','flat_wrapped_312px_material_surface_not_room')
        tiles=[plate.crop((104+(j%3)*26,104+(j//3)*26,130+(j%3)*26,130+(j//3)*26)) for j in range(9)]
        ref=tiles[0].copy();corner=ref.getpixel((0,0));north=[ref.getpixel((a,0)) for a in range(26)];west=[ref.getpixel((0,a)) for a in range(26)];north[0]=north[-1]=west[0]=west[-1]=corner
        for j,t in enumerate(tiles):
            for a in range(26):t.putpixel((a,0),north[a]);t.putpixel((a,25),north[a]);t.putpixel((0,a),west[a]);t.putpixel((25,a),west[a])
            ident=f'r05_{key}_v{j}';save(t,ident,'tiles','flat_edge_matched_material_variant',variant=j);atlas.alpha_composite(t,(j*26,i*26));frames.append(dict(id=ident,rect=[j*26,i*26,26,26]))
        ops.append(dict(source=r['output'],material=key,box=box,target_size=[312,312],resample='nearest',quantizer='Nearest RGB squared distance; first palette entry on ties, equivalent to requested skill finalizer',macro_wrap_border=1,tiles=9,tile_boxes=[[104+j%3*26,104+j//3*26,130+j%3*26,130+j//3*26] for j in range(9)],shared_edge_border=1,note='Flat material variants, not47-state edge/boundary autotiles; no rotations/flips'))
    atlas.save(P/'sheets/r05_flat_materials.png');write('sheets/tiles.json',dict(size=[234,104],cell_pixels=26,frames=frames))
    paths=[]
    for s in read('layouts.json'):
        cs=cells(s);seen=reachable(cs,tuple(s['exits'][0]['cell']));assert seen==cs,('Disconnected proposed scene',s['id'],len(cs-seen));assert all(tuple(e['cell']) in seen for e in s['exits']+s['reserved'])
        paths.append(dict(scene=s['id'],walkable_cells=len(cs),reachable_cells=len(seen)))
    write('layout-validation.json',dict(passed=True,paths=paths,D07_dimensions=[46,34],D08_dimensions=[[38,38]]*3,scope='Proposed grid connectivity only; no game runtime',runtime_verified=False))
    manifest=dict(batch='R05-basin-v1',status='material_assets_pending_quality_scene_generation_pending',assets=assets,source_sha256=b['source_sha256'],raw_sources={Path(r['output']).name:r['output_sha256']},selected_material_master=chosen,crop_operations=ops,inventory_requests={},planned_inventory_requests=b['inventory_requests'],view_slots_fulfilled=0,runtime_verified=False);write('materials-manifest.json',manifest)
    spec=importlib.util.spec_from_file_location('r05_material_skill',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):ok=pam.validate_project(P)
    (P/'notes/materials-skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');assert ok,buf.getvalue()
    seam_checks=0
    for key in ['gravel','wetstone','boards','earth']:
        tiles=[Image.open(P/f'assets/tiles/r05_{key}_v{j}.png') for j in range(9)]
        for q in tiles:
            for other in tiles:
                assert q.crop((0,0,26,1)).tobytes()==other.crop((0,25,26,26)).tobytes();assert q.crop((0,0,1,26)).tobytes()==other.crop((25,0,26,26)).tobytes();seam_checks+=2
    manifest['status']='material_assets_verified_scene_generation_pending';write('materials-manifest.json',manifest);write('materials-validation.json',dict(passed=True,requested_skill_validator=True,assets=40,tiles=36,macro_materials=4,pairwise_seam_checks=seam_checks,source_current=True,view_slots_fulfilled=0,runtime_verified=False))
    for a in assets:
        (P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n{a["size"]}静态RGBA PNG；区域128色，二值alpha，原点(0,0)。\n\n用途：{a["role"]}；平面材质，不能当成房间或边界碰撞。母图{r["output"]}，SHA {r["output_sha256"]}；裁切与共享边缘见materials-manifest.json。\n\n材质完成，R05整批场景和视图仍未完成；不计入已交付视图。\n',encoding='utf-8')
    print(json.dumps(dict(batch=P.name,assets=40,tiles=36,seam_checks=seam_checks,layout_scenes=len(paths),view_slots_fulfilled=0,passed=True),ensure_ascii=False))
if __name__=='__main__':main()
