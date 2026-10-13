"""Validate native art geometry and export data independently of the packer."""
from pathlib import Path
from collections import deque
import hashlib
import json
import re
import sys
from PIL import Image, ImageDraw, ImageChops

ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'

def main():
    manifest=json.loads((P/'manifest.json').read_text(encoding='utf-8'))
    palette=json.loads((P/'palettes/den_n1_128.json').read_text())['colors']
    palette={tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in palette}
    code=(ROOT/'src/EmbersAndOaths/NightRooms.cs').read_text(encoding='utf-8-sig')
    checks=[]
    def check(name,ok,detail=None):checks.append(dict(name=name,passed=bool(ok),detail=detail))
    def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
    check('source-code-hash',sha(ROOT/'src/EmbersAndOaths/NightRooms.cs')==manifest['source_code_sha256'])
    check('native-dimensions',bool(re.search(r'Columns=40, Rows=30, Tile=26',code)))
    identifiers=[a['id'] for a in manifest['assets']]
    check('unique-assets',len(identifiers)==len(set(identifiers)))
    indexed_paths={a['path'] for a in manifest['assets']}
    actual_paths={p.relative_to(P).as_posix() for p in (P/'assets').rglob('*.png')}
    check('no-unlisted-or-missing-exports',indexed_paths==actual_paths)
    for a in manifest['assets']:
        path=P/a['path'];ident=a['id'];ok=path.exists()
        check(ident+':present',ok)
        if not ok:continue
        im=Image.open(path).convert('RGBA');pixels=list(im.get_flattened_data())
        opaque={p[:3] for p in pixels if p[3]}
        check(ident+':sha',sha(path)==a['sha256'])
        check(ident+':size',list(im.size)==a['size'] and im.width%26==0 and im.height%26==0)
        check(ident+':binary-alpha',all(p[3] in (0,255) for p in pixels))
        check(ident+':palette',opaque<=palette and len(opaque)<=128,{'colors':len(opaque)})
        check(ident+':transparent-rgb-clean',all(p[:3]==(0,0,0) for p in pixels if p[3]==0))
        if a.get('role')=='independent_sprite':
            check(ident+':alpha-cutout',im.getchannel('A').getextrema()==(0,255))
            ox,oy=a['sprite_origin'];check(ident+':origin',0<=ox<im.width and 0<=oy<im.height)
        check(ident+':runtime-not-claimed',a['runtime_verified'] is False)
    for room,key in zip(manifest['rooms'],['Yard','Bellhouse','Underpass']):
        rid=room['id']
        match=re.search(r'\['+key+r'\]=new\[\]\{(.*?)\}',code)
        rects=[list(map(int,v.split(','))) for v in re.findall(r'\(([^)]+)\)',match.group(1))]
        check(rid+':native-rectangles',room['walkable_rectangles']==rects)
        expected=Image.new('L',(1040,780));d=ImageDraw.Draw(expected)
        cs=set()
        for a,b,c,e in rects:
            d.rectangle((a*26,b*26,(c+1)*26-1,(e+1)*26-1),fill=255)
            cs|={(x,y) for y in range(b,e+1) for x in range(a,c+1)}
        actual=Image.open(P/'assets/backgrounds'/f'{rid}__floor.png').convert('RGBA').getchannel('A')
        check(rid+':floor-equals-native-mask',ImageChops.difference(expected,actual).getbbox() is None,{'walkable_cells':len(cs)})
        guide=Image.open(P/'guides'/f'{rid}_walkable.png').convert('L')
        check(rid+':mask-export',ImageChops.difference(expected,guide).getbbox() is None)
        first=next(iter(cs));seen={first};queue=deque([first])
        while queue:
            x,y=queue.popleft()
            for nb in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                if nb in cs and nb not in seen:seen.add(nb);queue.append(nb)
        check(rid+':connected',seen==cs)
        check(rid+':safe-room-margin',all(2<=x<38 and 2<=y<28 for x,y in cs))
        for kind in ['doors','spawns','story']:
            for name,x,y in room['anchors'][kind]:
                check(rid+':'+kind+':'+name,(x,y) in cs,{'cell':[x,y],'pixel':[x*26+13,y*26+13]})
        for layer in ['structure','foreground']:
            alpha=Image.open(P/'assets/backgrounds'/f'{rid}__{layer}.png').convert('RGBA').getchannel('A')
            check(rid+':'+layer+'-outside-floor',ImageChops.multiply(expected,alpha).getbbox() is None)
        check(rid+':all-layer-canvases',all(Image.open(P/'assets/backgrounds'/f'{rid}__{part}.png').size==(1040,780) for part in ['backing','floor','structure','foreground','plan','environment']))
        check(rid+':preview-present',(P/'previews'/f'{rid}__preview.png').exists())
    check('raw-generation-sources-intact',all(sha(P/'raw'/n)==h for n,h in manifest['raw_sources'].items()))
    failed=[c for c in checks if not c['passed']]
    report=dict(date='2026-10-13',passed=not failed,check_count=len(checks),failed_count=len(failed),
                checks=checks,scope='PNG integrity, alpha, palette, native geometry, origins and connectivity; not runtime or literary acceptance')
    (P/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'checks':len(checks),'failures':failed},ensure_ascii=False))
    return 1 if failed else 0

if __name__=='__main__':sys.exit(main())
