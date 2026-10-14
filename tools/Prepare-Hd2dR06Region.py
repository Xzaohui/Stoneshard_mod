"""Paint an authored regional topology guide, not official/native geography."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def main():
    r=json.loads((P/'region-layout.json').read_text(encoding='utf-8'));colors=json.loads((P/'palettes/hig_r06_128.json').read_text(encoding='utf-8'))['colors'];im=Image.new('RGB',tuple(r['size']),(61,62,57));d=ImageDraw.Draw(im)
    d.polygon([(1050,0),(1664,0),(1664,1248),(1120,1100),(1150,620)],fill=(79,86,93));d.polygon([(0,0),(870,0),(840,680),(0,910)],fill=(105,100,85))
    for a,b in r['edges']:d.line([tuple(r['art_anchor_pixels'][a]),tuple(r['art_anchor_pixels'][b])],fill=(165,148,128),width=18)
    for n in r['nodes']:
        x,y=r['art_anchor_pixels'][n['id']];d.ellipse((x-52,y-39,x+52,y+39),fill=(125,122,114),outline=(188,181,176),width=4)
    im.save(P/'guides/r06_region_topology.png')
    prompt='Edit this authored topology guide into a1664x1248 medieval HD2D flat OVERHEAD cold mountain region terrain painting. Preserve EXACTLY10 modest open node pads at their guide positions and all11 thin road connections, no extra node, no missing/merged pads or road. Keep path intersections as unmarked intersections, not extra settlement nodes. Replace guide colored polygons/circles with natural worn cold gray stone terraces, low slate cliffs, sparse brown/olive mountain scrub and old dry gravel tracks, subtle cold highground; no perspective horizon, white snowy sparkles or tropical jungle. Circles are GUIDE ONLY: replace them with unobtrusive bare dry small ground pads, no circle marker/grid/symbol. Retain two loops and the ordinary retreat connection; this is a Mod-original connectivity schematic, not official geography or native world-engine coordinates. Do NOT draw buildings (independent sprite icons added later), people, NPCs, animals, originalcrystal, church icon, active purplemagic, beams, fire, glowlights, flags or readable names/labels/numbers/compass/legend. Crisp muted pixel clusters, low noise, top-left neutral matte UNLIT base, opaque fullcanvas. Reserved violet not used in ordinary terrain. Use locked HIG-R06-128 palette:\n'+', '.join(colors)+'\n';f=P/'notes/prompt-r06-region-v1.txt'
    if f.exists():assert f.read_text(encoding='utf-8')==prompt
    else:f.write_text(prompt,encoding='utf-8')
    print('R06 authored topology guide:10nodes,11edges')
if __name__=='__main__':main()
