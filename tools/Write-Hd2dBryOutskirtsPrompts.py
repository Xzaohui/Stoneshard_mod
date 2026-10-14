"""Create prompts from the approved locked style; no generation or export."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-outskirts-v1'
def main():
    lock=(P/'spec_lock.md').read_text(encoding='utf-8');b=json.loads((P/'brief.json').read_text(encoding='utf-8'));assert len(b['sprites'])==48;assert not (P/'generation-log.json').exists();colors=re.findall(r'#[0-9A-F]{6}',lock)
    common='Create a NEW production sprite master matching only the TEXTURED pixel technique/materials of the reference, NOT its old buildings. Transparent 1536x1024 canvas. EXACTLY EIGHT isolated sprites in a four-column/two-row grid, nominal slots384x512. Toprow reading left-to-right slots1-4; bottomrow slots5-8. Every complete silhouette fits inside its own slot with generous transparent margin; no touching/extra floating parts. Square-grid orthographic oblique frontal game view, not diamond isometric. Neutral top-left UNLIT matte base, no cast shadow outside silhouette, glow, fire, sunbeams or lighting gradients. HD2D medium-fine deliberate pixel clusters, restrained timber/stone/slate/metal/cloth. No people, living hands, bodies, animals, ghost, lettering, numerals, readable symbols, crests, names, completed contracts or story outcomes. Blank writable faces. No floor backdrop or camera perspective ground; prop base belonging to object allowed. Do not reproduce original game assets. EXACT eight new assets below. '
    prompts={
      'bryo-architecture-v1':[
        '1 TOPLEFT: modest communal embankment timber hut,312x234production,front low central door,small ordinary windows, patched gray roof and one modest cook chimney; no furniture/beds rendered in facade. Simple dry footing, no luxury barracks or leader bedroom.',
        '2 TOPSECOND: raised seed store312x260, timberframe warehouse on visibly high short STONE plinth with short central steps and one front door. Gray-brown roof, sealed modest side hatch, no piles of infinite grain, labels or water.',
        '3 TOPTHIRD: old-sail-village communal cottage312x234, reclaimed mismatched old shipboards as timber wall, plain gray roof with one dull canvas repair patch, one ordinary front door and small windows, no boat/hull or people.',
        '4 TOPRIGHT: low-tide SIDE-BERTH RENTAL SHED312x234, simple timber roof on front posts around one small sheltered room, EXACTLY ONE visible door, no second entrance/window resembling a door, front empty deck rail at sides, no attached boat/medical apparatus.',
        '5 BOTTOMLEFT: original small bookbinding side-workshop364x234, low timber facade with broad empty workwindow and separate plain front door, gray-red roof, blank small hanging wood tag, no press/printing logo/university symbols or book piles.',
        '6 BOTTOMSECOND: sealed original OUTER WORK SHED364x260, worn gray timber roof, closed blank front with protective crossed boards, modest weathered supportposts; not dungeon entrance, no stair/ladder/door below ground, no repaired/crumbling outcome.',
        '7 BOTTOMTHIRD: public old-tower OUTER PORTICO364x260, low aged graystone wall strip with THREE ordinary low columns and an open front public alcove, slate canopy and empty floor aperture. Do not create a tall tower, bank/military counter, throne, banner or armory.',
        '8 BOTTOMRIGHT: neutral small hearing COURTYARD PAVILION416x286, open front with short timber posts, low curved/horseshoe canopy on graystone footing, TWO visible side openings, no royal city hall/council insignia. Empty interior aperture, no table/chair/people baked in.'
      ],
      'bryo-props-a-v1':[
        '1 TOPLEFT: ONE modest empty communal SHORT-STAY BED130x78, complete narrow worn wood frame, muted rolled blanket and simple pillow, no body. Production reused exactly twice per satellite livingroom, do not draw pair together.',
        '2 TOPSECOND: ONE ordinary communal cooking stove78x104, unlit dark stone firebox with closed used POT on top, no flame, steam, contents count or unlimitedfood.',
        '3 TOPTHIRD: road-side wage TALLY CASE104x78, shallow sloped wood case with TWO visibly separated rows of blank narrow worker chits, no names, numbers, money or collective sign-off.',
        '4 TOPRIGHT: ONE small apprentice hand stamp26x26, plain short square wood stamp and tiny turned handle, worn flat stamp face without readable signature or crest, no ink/glow.',
        '5 BOTTOMLEFT: compact patched embankment GROUND TRACE104x78, low dark packedearth/stone strip with OLD joined repair seam and two short inset worn timbers, empty transparent around its low oval footprint; no grave/rune/repair successmark.',
        '6 BOTTOMSECOND: finite sealed SEED BAG pair78x78, EXACTLY TWO modest tied coarse brown sacks side by side, no grain overflowing, stampedlabels/seedownership judgement or futureharvest.',
        '7 BOTTOMTHIRD: ONE low grain WEIGHING BALANCE104x104, modest woodstand with ironbeam and two empty shallow pans, no digits/weights, measuredamount or people.',
        '8 BOTTOMRIGHT: TWO blank rectangular deposit WOOD CHITS52x26, worn flat pieces with small unequal corner notches, no coins or amount, no paid/wholeharvest certification.'
      ],
      'bryo-props-b-v1':[
        '1 TOPLEFT: low SALT-FIELD RIDGE PATCH156x104, small flat ground rectangle with THREE low parallel damp grayearth ridges and sparse dullolive straw tufts, no whiteglowing salt, ripe harvest or water. Complete stand-alone ground patch.',
        '2 TOPSECOND: DRY OLD BOAT RIBS208x104, unseaworthy salvaged hull skeleton laid on two short low wood supports, curved weathered graytimber ribs and partialplanks, no mast/sail/water/person. Clearly dry, dismantled in a shallow yard, not usable boat.',
        '3 TOPTHIRD: ONE small MOORED RENTAL SKIFF208x104, intact modest empty low wooden dinghy seen orthographic-oblique, one pair stored oars inside and plain small mooringrope coil. No water patch/sail/motor/shipname/cargo/people, no departedmotion or hullcapacity numbers.',
        '4 TOPRIGHT: ONE DETACHED EMPTY SUPPORT SET78x104, folded ordinary wood/metal support brace with muted padded straps, complete stored equipment upright on a small stand. No limb/body/skeleton/livinghands or medicalcure, no weapon, single set only.',
        '5 BOTTOMLEFT: public LOAD SCALE78x130, one slim weathered wood/metal measuring post with blank face and few short UNNUMBERED tickgrooves, short stable weighted foot, no readable tariff/shipname/body or final safe-load verdict.',
        '6 BOTTOMSECOND: ONE blocking cargo CRATE104x78, plain low closed rectangular weathered box visibly wider than tall, blank faces, horizontalcart obstruction shape, no corpse/coffin/loot-label.',
        '7 BOTTOMTHIRD: ONE sealed PRIVATE HISTORY FILE BAG52x52, folded tancloth envelope bag around a thin flat packet, sealed tie and plainblank tag, clearly flat documents NOT round money purse; no medicalhistory exposed.',
        '8 BOTTOMRIGHT: small horizontal RETURN MARKER78x26, plain old wood plank on TWO tiny ground pegs, THREE faded short diagonal gray-white slashes pointing left toward shore, no words/numbers/checkmark or officialemblem.'
      ],
      'bryo-props-c-v1':[
        '1 TOPLEFT: LOW-LOAD TRIAL FRAME156x130, low robust wooden frame with TWO small iron clamp blocks and a single low fixed plain testing block, empty safe fixture, no hanging load/person/fire/weapon or successfailure gauge.',
        '2 TOPSECOND: two finite separated MATERIAL BATCHES104x78, EXACTLY TWO shallow divided trays side by side, each contains a few short dark metal blanks, different dullmaterial tones, no endless pile/coins/readable batchlabel.',
        '3 TOPTHIRD: THREE TEST TYPES78x52, EXACTLY THREE separate plain metal testpieces on a shallow neutral tray: one rounded ring,one fork-ended buckle,one oblong bored block. No fourth sample, digits/checkmarks or infinitegold.',
        '4 TOPRIGHT: one DETACHED CRACKED BUCKLE52x26, two close dullmetal halves of one small buckle with a visible irregular fracture gap, no body/blood/drop-lootglow.',
        '5 BOTTOMLEFT: ONE blank BATCH TAG26x26, small worn pale paperlabel with one torn corner and tiny tie hole, no text or numbers.',
        '6 BOTTOMSECOND: short TRIAL FENCE156x78, THREE plain woodposts with two low horizontal rails, center spans low open area, complete freestanding silhouette, no continuous floor/warningtext/lockeddoor.',
        '7 BOTTOMTHIRD: ONE BOOKBINDING BENCH130x104, modest sloped scratched woodwork table with small EMPTY screwpress and blank workboard, no book/page/thread/furnitureoccupant baked, materialsdistinctfromprintingpress.',
        '8 BOTTOMRIGHT: HISTORIC ORIGINAL PAGE TRAY78x52, one shallow dull woodtray with a single aged page placed face DOWN, faint neutralpapertexture and few old stitch holes at edge, familyname fully hidden, no fake old text/name/certification.'
      ],
      'bryo-props-d-v1':[
        '1 TOPLEFT: ADDED PAGE TRAY78x52, one separate shallow warm graywood tray with one newer blank offwhitepaperleaf, a tiny blank folded note marker at margin and distinct stitch holes, no text/names/faked ancientink.',
        '2 TOPSECOND: LOW ARCHIVE CABINET104x104, modest squat two-door weathered wood cabinet, small simple closed latches, blankfaces, no family/officialseal labels, no bankvault or magicalglow.',
        '3 TOPTHIRD: ONE plain EMPTY BINDING/CLAIM CHAIR52x78, small complete low woodchair with low back and ordinary square seat, no throne/upholstery/identity, no actor; reused for one repairseat and five independent emptyhearingchairs.',
        '4 TOPRIGHT: small BINDING THREAD KIT52x26, one dull naturalflax thread spool and thin closed needlecase beside it, no text/hand, complete shorthorizontal silhouette.',
        '5 BOTTOMLEFT: BLANK METHOD SAMPLE PAGE52x26, single blank texturedpaperleaf with visible neutral papergrain and a short row of empty stitchholes along one edge, no letters/numbers/signature.',
        '6 BOTTOMSECOND: WEAK OLD SUPPORT FRAME130x104, complete aged wooden rectangular support with obvious SHORT MISSING diagonal supportsegment and old join marks, stable illustration not animatedcollapse, no injuredbody/confirmedrepair.',
        '7 BOTTOMTHIRD: BOWED SEALED PLANKS156x78, low sagging horizontal old planked section with visible joined seams and a small closed protective crossbar on top, no ladder/stairs/trap/people/blood, complete groundsection silhouette.',
        '8 BOTTOMRIGHT: protective SHUTTER BARRIER104x78, two plain short upright posts and one closed horizontal beam with simple woodpin, no lockkeys/successcheck/words; a safe outside boundary, not native unlockeddoor.'
      ],
      'bryo-props-e-v1':[
        '1 TOPLEFT: FIXED SAFE OUTER BRACE104x104, solid low wood/iron triangular inspection support with two visibly complete diagonals and short fixed foot, distinct intact form from missing-support frame; no repaircertificate or human trial.',
        '2 TOPSECOND: CLOSED LAST-NOTE CASE78x52, modest shallow woodbox with one flat sealed paperpacket resting under a closed tied strip, no readable note/familyname/deathproof.',
        '3 TOPTHIRD: HANDLING FEE DISH52x26, one small shallow dull iron dish containing just THREE blank flat metal counting discs, no coinheads/currency value, not huge paybag or paidstatus.',
        '4 TOPRIGHT: ONE LOW RING TABLE208x156, ordinary circular wooden ring-shaped meeting table with a clearly OPEN circular center and FOUR short modest feet, plain low tabletop, no throne/dais/people/chairs/paper/votemarks baked. Complete silhouette.',
        '5 BOTTOMLEFT: THREE-COLUMN HANDOVER TRAY104x78, low horizontal woodtray with EXACTLY THREE empty parallel compartments, blank pegheader faces; arrival/authorization/actualtransfer remain engine text, no writtennames/checkmarks.',
        '6 BOTTOMSECOND: SINGLE LIMITED STATEMENT CASE78x52, one short closed woodcase with one thin sealed blandpaperpacket and a blank tied tag, no extra speakers/actor substitute/globalcityendorsement.',
        '7 BOTTOMTHIRD: finite COUNTED PLANK STACK104x78, EXACTLY FOUR separate short weathered planks in a low neat stack, uneven exposed ends, no labels/price/unlimitedpile or completedrepair.',
        '8 BOTTOMRIGHT: EMPTY SUPPORT STORAGE104x104, small open wooden two-compartment storage stand with both compartments EMPTY and a blank panel, no second brace/person/medicalcure, not bed or infiniteequipment.'
      ]}
    for ident,items in prompts.items():
        text=common+'\n'+'\n'.join(items)+'\nPRODUCTION locked colors only: '+', '.join(colors)+'\nMotheractual spacing/size recorded; approvedcrop/nearest/palette/binaryalpha normalization later, never fake printed metadata.\n';(P/'notes'/f'prompt-{ident}.txt').write_text(text,encoding='utf-8')
    landscape='1536x1536 opaque production TEXTURED HD2D pixel landscape-surface master, FOUR equally sized768x768 quadrants, no borders/labels/buildings/props/people/animals. Square-grid orthographic flat surface, top-left neutral UNLIT matte base. TOPLEFT coarse quiet gray-brown dry embankment packedearth with sparse muted shortgrass and a fewsmall wornstones, calm lowcontrast. TOPRIGHT low damp coastal saltfield ground with thin irregulargraysoil ridges/very sparse olive straw, no ripecrop/whiteglow/pools. BOTTOMLEFT quiet shallow oldboat-yard graybrown soil with oldshortscratches and sparse mutedgravel, NO actualplanks/boats. BOTTOMRIGHT calm shallow darkblue-gray riverwater texture with tiny matte horizontal ripples, no reflections/fire/boats. Fillallpanel edges; no roads/rooms/interactiveplaces or structuralgeometry baked. LOCKED BRY-CORE-128: '+', '.join(colors)+'\n';(P/'notes/prompt-bryo-landscape-v1.txt').write_text(landscape,encoding='utf-8')
    print(json.dumps(dict(prompts=list(prompts)+['bryo-landscape-v1'],palette_colors=len(colors)),ensure_ascii=False))
if __name__=='__main__':main()
