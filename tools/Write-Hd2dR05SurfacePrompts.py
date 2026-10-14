"""Author remaining R05 painted source requests without changing its execution lock."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'

def main():
    colors=json.loads((P/'palettes/ash_r05_128.json').read_text(encoding='utf-8'))['colors']
    common='Static cold temperate medieval HD2D pixel-art material source, orthographic oblique square-grid camera, upper-left soft neutral unlit matte base. Crisp restrained clusters, muted ash gray, olive, brown, gray-blue and pale cloth. NO people, animals, corpses, readable text, labels, panel borders, logos, coats of arms, tropical plants, fire, glowing crystal, magic, cure, consent or inventory status. Not a game room or confirmed collision. Do not add scenes or objects beyond the requested materials. Palette below.\n'
    prompts={
      'r05-water-v1':'1536x1024 OPAQUE RGB source divided into THREE equal vertical512x1024panels. Fill each panel edge to edge with a flat OVERHEAD calm water surface, no bank, perspective horizon or depth gradient. LEFT: ordinary cold gray-blue calm water, broad subtle ripples. MIDDLE: dull ash-gray water with sparse off-white uneven foam/scum clusters, quieter small-scale ripples, no red blood or automatic disease causality. RIGHT: low-water exposed muddy gray silt with tiny isolated puddles, no dry-path guarantee. Keep water low contrast and static, not sparkly/noisy; three different materials not copied, no seam borders.\n',
      'r05-interiors-v1':'1536x1024 OPAQUE RGB source divided into THREE512x1024vertical frontal unlit wall panels, with the same perpendicular straight-on wall camera. Each has ONE small closed unlit square window/vent at upper-center y100..350 and uninterrupted wall material y440..760. LEFT: dry high-level squared gray-brown stone masonry with modest rectangular shutter. MIDDLE: damp middle-level old regular masonry with low dark water staining and iron-barred vent. RIGHT: low-level rough old scour-worn gray stone, visibly more irregular joints, a very small high vent with plain slats. These are wall surfaces, NO ground/floor, door, pillars, arches, platforms or roofs. Three levels of one old waterworks but distinguish weathering and vent design, no active flooding or dungeon trigger.\n',
      'r05-landscape-v1':'1536x1536 OPAQUE RGB divided into FOUR equal768x768quadrants. Each is a seamless-looking flat OVERHEAD nonwalkable cold-temperate ground/bank texture filling panel edge to edge, no horizon or isometric diamond. TOP LEFT: muted gray-brown damp scrub bank with sparse small dry temperate reeds and dark soil. TOP RIGHT: gravelly dry HIGH ground with modest slate rubble and sparse gray grass, safest visual elevation is schematic only. BOTTOM LEFT: old shallow drainage ditch bank with scoured mud, short irregular dark gray water strips, sparse straw reeds. BOTTOM RIGHT: low settlement verge, worn ash-brown earth with sparse old wood chips, irregular small stone fragments, no house or furniture. Calm broad tonal regions; not tropical swamp, lush jungle, rockfield or bright white salt-and-pepper noise. No apparent global plague, painted roads, buildings, people or paths to be treated as actual walkable geometry.\n'
    }
    for ident,desc in prompts.items():
        text=desc+common+'\nAPPROVED ASH-R05-128 PALETTE:\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(list(prompts)))
if __name__=='__main__':main()
