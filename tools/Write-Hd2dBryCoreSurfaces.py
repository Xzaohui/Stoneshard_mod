"""Remaining unlit source surfaces for the Brynn core scene batch."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
def main():
    colors=json.loads((P/'palettes/bry_core_128.json').read_text(encoding='utf-8'))['colors'];common='Serious muted medieval coastal-city HD2D pixel-art source. Crisp calm textured clusters, neutral top-left matte UNLIT base, no glow/flames/cast shadow/lightgradient. No people, animals, readable text/numbers, crests, labels/panel borders, extra objects, magic, cure/consent/quest outcome. Exact locked BRY-CORE-128 palette below.\n'
    prompts={
      'bry-interiors-v1':'1536x1024 OPAQUE source with THREE equal512x1024vertical FRONTAL wall panels. Same straight-on wall camera, NOT room perspective. Each has ONE small CLOSED UNLIT window/shutter y100..350 at upper-center, uninterrupted material y440..760. LEFT old regular gray masonry with a small plain iron-bar shutter, subtle fine joints. MIDDLE worn dark-brown city timber framing and narrow plain planks, modest wood shutter window, no heraldry. RIGHT dull pale patched lime/plaster over low gray stone, small closed plain square shutter, no clinical signs. NO floor, ground, roof, door, columns, furniture, wall paintings or hands/handprints (separate decals).\n',
      'bry-landscape-v1':'1536x1536 OPAQUE flat OVERHEAD material master, FOUR equal768square quadrants, no horizon/diamond perspective or room layout. TOP LEFT restrained city stone verge and low mossy soil cracks, sparse tiny old fragments, no roads/buildings. TOP RIGHT muted wet gray-brown river bank with sparse dull reed stubble and little driftwood, no boat, bright water marks or shore horizon. BOTTOM LEFT calm packed courtyard earth with a few small gray stone fragments and muted short moss, no white salt-and-pepper noise. BOTTOM RIGHT pure calm dim gray-blue river WATER surface edge to edge, broad irregular quiet small ripples, no bank, foam, bright sparkles, boat or tide verdict. Full edges, calm detail, not a copied commercial/game map; precise floors/structures/water masks composed separately.\n'
    }
    for ident,desc in prompts.items():
        text=desc+common+'\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(list(prompts)))
if __name__=='__main__':main()
