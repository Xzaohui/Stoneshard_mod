"""Create an authored topology guide and prompt; never treat it as native world coordinates."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
def main():
    r=json.loads((P/'region-layout.json').read_text(encoding='utf-8'));colors=json.loads((P/'palettes/ash_r05_128.json').read_text(encoding='utf-8'))['colors']
    im=Image.new('RGB',tuple(r['size']),(49,45,43));d=ImageDraw.Draw(im)
    d.polygon([(1050,260),(1530,350),(1480,960),(1130,1100),(780,650)],fill=(59,74,79))
    d.polygon([(0,0),(740,0),(650,660),(120,850),(0,900)],fill=(99,94,64))
    for a,b in r['edges']:d.line([tuple(r['art_anchor_pixels'][a]),tuple(r['art_anchor_pixels'][b])],fill=(158,141,115),width=18)
    for n in r['nodes']:
        x,y=r['art_anchor_pixels'][n['id']];d.ellipse((x-52,y-39,x+52,y+39),fill=(125,117,104),outline=(209,183,151),width=4)
    im.save(P/'guides/r05_region_topology.png')
    prompt='Edit this authored topology guide into a1664x1248 medieval HD2D flat OVERHEAD regional terrain painting. Preserve EXACTLY8 open modest node pads at guide positions and all9 thin road connections. Do not make a ninth pad, merge pads or remove roads. Replace colored geometric fields with muted COLD TEMPERATE ash-brown basin, small gray-blue marshwater strips to the east, sparse dry reeds, low old drainage banks, dry high gravel and low hills west; never tropical forest or fantasy global plague. The bright circles are GUIDE ONLY: replace them with discreet bare ground pads, no rings/markers/frame labels. Road guide: upper-left outer road to north camp; north camp to upper-right village; village to eastern reed bank; reed bank to lower-east drain; drain to bottom-center ward; ward to southwest shelter; shelter to north camp; drain to bottom-left well; well to upper-left outer road. Locations only schematic Mod-original topology, not official geographical placement or world-engine grids. No buildings (independent sprites added later), people, creatures, NPCs, ruins beyond small ground stones, readable text, labels, compass, legend, grid, fire, magical effects, lit lights or faction claims. Crisp low-noise textured pixel art, subdued olive/brown/gray-blue with calm medium broad clusters, upper-left neutral matte UNLIT base. Opaque full canvas.\n\nAPPROVED ASH-R05-128 PALETTE:\n'+', '.join(colors)+'\n'
    f=P/'notes/prompt-r05-region-v1.txt'
    if f.exists():assert f.read_text(encoding='utf-8')==prompt
    else:f.write_text(prompt,encoding='utf-8')
    print('R05 topology guide:8nodes,9edges; no native world authority')
if __name__=='__main__':main()
