"""Six task-space nodes reference four original city areas; art guide only."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
def main():
    r=json.loads((P/'region-layout.json').read_text(encoding='utf-8'));colors=json.loads((P/'palettes/bry_core_128.json').read_text(encoding='utf-8'))['colors'];im=Image.new('RGB',tuple(r['size']),(70,61,45));d=ImageDraw.Draw(im)
    d.rectangle((0,0,830,620),fill=(111,101,79));d.rectangle((830,0,1663,620),fill=(90,83,64));d.rectangle((830,620,1663,1247),fill=(82,68,53));d.rectangle((0,620,829,1247),fill=(80,82,63));d.polygon([(1480,0),(1664,0),(1664,1248),(1390,1248),(1320,760),(1510,620)],fill=(46,69,72))
    for a,b in r['edges']:d.line([tuple(r['art_anchor_pixels'][a]),tuple(r['art_anchor_pixels'][b])],fill=(177,157,120),width=18)
    for n in r['nodes']:
        x,y=r['art_anchor_pixels'][n['id']];d.ellipse((x-60,y-42,x+60,y+42),fill=(128,115,88),outline=(201,176,136),width=4)
    im.save(P/'guides/bry_city_topology.png');prompt='Edit this authored city topology guide into a1664x1248 medieval coastal-city HD2D flat OVERHEAD ground/bank painting. Preserve EXACTLY SIX modest task-space pads at guide positions and all SIX thin cyclic pedestrian connections. Four guide fields refer to four original city areas: upper-left restrained stone mint/public-announcement ground; upper-right old narrow-lane stone/soil; lower-right worn forge/new-guild ground; lower-left muted neutral river/courtyard verge. Two of the SIX pads are cross-area waterworks/neutral meeting task spaces, NOT new official quarters. Do NOT create six official city zones, invent banks/open original city interiors or assert native game geography. Guide bright circles are not final art: replace with small modest bare pads, no circles/markers/labels/grid/compass/legend. Replace colored rectangles with subtle natural material transitions; do not retain straight quadrant dividers. Modest calm gray-blue water verge at far-right per guide, muted fine gray/brown cobbles and timber/earth banks, no precise official whole-city coastline. Paths connect the given pads only; keep the return loop readable. No buildings (independent sprite icons added later), people, animals, boats, fires, glowing light, flags, crests, readable writing or numbers, magical crystals, live watergate outcome or quest status. Crisp calm pixel clusters, neutral top-left matte UNLIT base, opaque fullcanvas. This is a Mod-original connection schematic, not a native world map. Use locked BRY-CORE-128:\n'+', '.join(colors)+'\n';f=P/'notes/prompt-bry-city-v1.txt'
    if f.exists():assert f.read_text(encoding='utf-8')==prompt
    else:f.write_text(prompt,encoding='utf-8')
    print('Brynn city guide:6taskspaces,6corestreetedges,4originalarea reference')
if __name__=='__main__':main()
