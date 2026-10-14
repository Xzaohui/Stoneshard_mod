"""Create the remaining R06 unlit wall and nonwalkable terrain prompts."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def main():
    colors=json.loads((P/'palettes/hig_r06_128.json').read_text(encoding='utf-8'))['colors']
    common='Cold mountain medieval HD2D pixel-art source. Crisp restrained low-noise clusters, top-left neutral matte UNLIT base, no lightgradient, castshadow, glow or flames. No people, animals, corpses, readable text/numbers, labels, panel borders, crests, religious symbols, magic, tropical flora or extra objects. Reserved violet NOT used for these ordinary structural/terrain materials. All colors only from locked HIG-R06-128 below.\n'
    prompts={
      'r06-interiors-v1':'1536x1024 OPAQUE source, THREE equal512x1024vertical FRONTAL wall-material panels, same perpendicular straight-on camera, NOT room perspective. Each has ONE SMALL CLOSED UNLIT window/vent at upper-center y100..350 and uninterrupted wall material y440..760. LEFT old cold regular squared gray masonry with modest rectangular iron-bar shutter. MIDDLE old mountain timber wall with plain small wood shutter window, narrow worn plank joints. RIGHT wind-scoured rough gray old masonry with a small plain stone vent and thin horizontal iron slats. NO floor, ground, doors, columns, staircases, roofs or furniture. Dense relatively small masonry joints, warm-brown muted wood. Three distinct wall themes, no prologue cathedral or magicalarchitecture.\n',
      'r06-landscape-v1':'1536x1536 OPAQUE flat OVERHEAD terrain/water material master, FOUR equal768square quadrants, no horizon or diamond projection. TOP LEFT cold dark-gray mountain rock/cliff verge with modest sparse dry grass, small weathered stone faces, not huge boulders or snowy white noise. TOP RIGHT subdued dry high-ground gray-brown gravel bank with sparse tiny mountain shrubs, no roads or buildings. BOTTOM LEFT worn old slate/masonry rubble bank with occasional modest low scrub, little timber fragments, not a ruined cathedral or fixed gameplay walls. BOTTOM RIGHT pure calm dim GRAY-BLUE still-water surface edge to edge, short quiet broad irregular ripples, no banks, foam, ice, white sparkles or depth-gradient. Each panel fills edges, not a full game room; roads, exactwalkable floors, buildings and water masks added independently. NO purple in ordinary terrain, no active dangerous water or globalweather claim.\n'
    }
    for ident,desc in prompts.items():
        text=desc+common+'\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(list(prompts)))
if __name__=='__main__':main()
