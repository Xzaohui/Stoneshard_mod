"""Master prompts follow explicit Brynn spaces, not generic ordinal room substitutions."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
def main():
    b=json.loads((P/'brief.json').read_text(encoding='utf-8'));specs={s['id']:s for s in b['sprites']};colors=json.loads((P/'palettes/bry_core_128.json').read_text(encoding='utf-8'))['colors'];groups={
      'bry-architecture-v1':[
        ('print_arcade','wide modest city print/public-notice arcade, gray stone footing and old timber frame, rust-colored low tiled roof, TWO distinct plain front doorways with a low open gallery between. No bank, coins, imperial columns, newspaper text or official government crest'),
        ('rental_block','two-storey old rental building with TWO narrow timber/stone wings connected above a clearly OPEN ground-level central public passage, TWO independent lower doorways flanking the passage; modest public stair frame to one side. No beds/interior occupants or extra private-room inventory. Central ground-level passage must remain visibly open, not filled by a solid wall'),
        ('rope_shed','one modest shore-side rope tally shed, old dark timber over gray stone footings, low worn plank/slate roof, ONE plain front opening, no boat or actual ropes/chits added (independent props later)'),
        ('berth_canopy','one SMALL freestanding empty berth pavilion with FOUR wood posts and low dull pale cloth/plank roof, OPEN underneath, no boat, seating/person, water plane, bollard, cargo or absent-person outcome'),
        ('workshop_house','wide modest new-guild auxiliary workshop facade, gray stone fire-separating lower wall, old timber upper frame, worn tile/slate roof, TWO independent normal visitor entry doorways and a small separate plain staff-side hatch. No visible furnace/fire or tools (props separate), body experiment or commercial workshop crest'),
        ('water_observation_house','modest old river-side water observation lodge, low gray stone base, worn timber walls and dull slate roof, ONE plain front entry and a broad UNLIT closed river-facing shutter. No readable measurements, enormous dam or royal water authority'),
        ('gate_house','a modest low old stone/timber dual-gate maintenance house with TWO clearly separate SOUTH/front return doorways, plain low slate/plank roof; no exposed machinery, water, open sluice or modern hydroelectric plant. Both doorways distinct and visible'),
        ('neutral_meeting_hall','wide modest neutral meeting hall, worn gray stone footing, restrained timber frame and faded rust-tile roof, TWO ordinary return-street doors, small plain shutter windows. No throne/coronation/high dais, flags, noble coats of arms, feast, lit lamps or people')],
      'bry-props-a-v1':[
        ('printing_bench','one modest manual wooden type-setting/correction bench, low timber frame with a BLANK type bed and plain simple hand screw/clamp, no giant printing machine or readable newspaper'),
        ('movable_type_case','small shallow wooden movable-type case with little plain EMPTY block slots, no letters, numbers, signs or corrected street name'),
        ('blank_proof_sheet','one small irregular BLANK pale proof sheet, plain curled edge, no printing, writing, signature or stamp'),
        ('account_witness_table','low modest neutral account witness table with three separated EMPTY shallow token recesses, no ledger writing, money numbers or already accepted sponsorship'),
        ('sealed_change_pouch','one modest CLOSED tied change pouch with plain dull cord and unmarked cloth/leather, no coins spilling or money amount'),
        ('three_sponsor_chits','EXACTLY THREE separate small anonymous sponsorship chits arranged in one short row: round, square and plain notched wood pieces. No identities, currency counts, party affiliation or accepted agreement'),
        ('patched_rent_board','one modest narrow patched rental plaque/board on a plain short support, old nail repairs and a BLANK inset face for engine dates, no readable rent/year/tenant name'),
        ('blocked_old_door','one old plain closed doorway wall-patch: clearly BOARDED/SEALED with two rough cross boards and gray infill, a few shallow unnumbered old scratches in frame, no readable dates or secretly open new exit')],
      'bry-props-b-v1':[
        ('soot_hand_left','a FLAT abstract faded charcoal wall TRACE/DECAL, one irregular group of old fragmented palm-shaped soot smudges and short broken finger-like strokes. Not a living hand/body, not blood, no realistic anatomy, no rectangular wall backing; genuine transparent gaps between soot patches'),
        ('soot_hand_right','a DIFFERENT FLAT abstract old charcoal hand-trace group/DECAL, off-center fragmented dark palm smudge with short uneven broken finger-like marks angled differently. No living hand/body, no blood, no realistic anatomy or wall background; transparent gaps, not identical/mirrored copy of first'),
        ('unlit_memorial_lantern','ONE modest ordinary unlit iron memorial lantern, dark glass, no flame, glow, religious crest, person or actual mourning/forgiveness result'),
        ('rope_tally_rack','one small old timber rack with several short ordinary rope tally loops and BLANK tied name-tag plates, no readable names, person, shackles or automatic release/pledge result'),
        ('cargo_pledge_hook','ONE separate plain iron cargo-only pledge hook on a small timber upright with ONE small neutral rope tally and blank flat plate. No person, readable name, giant hook weapon or body restraint'),
        ('mooring_nail','ONE small worn ordinary mooring peg/nail on a short plain square wood foot, no boat or person, no claimed occupied berth'),
        ('termination_knot','one small loose old visibly retied termination rope knot with two short cord ends, BLANK tiny cloth tag, no printed termination date, signature or automatic agreement'),
        ('reserved_old_seat_board','one small worn detached old seat/berth name board with BLANK inset face and two old nail holes, low support, no readable missing-person name, body, boat or death/return claim')],
      'bry-props-c-v1':[
        ('unlit_furnace','one modest compact old gray-stone forge/furnace with a dark inactive-looking opening and plain iron grate, no flame, embers, glow, smoke, modern smelter, person or story shutdown marker. UNLIT base sprite; operational heat belongs to engine'),
        ('riveting_bench','a modest low old timber riveting/sample bench with EMPTY plain nonhuman support jig and little dull steel anvil head, no person, injury procedure, giant machine or readable maker mark'),
        ('maker_mark_sample','two small detached plain buckle/sample metal pieces on a neutral flat tray, one has an EMPTY maker inset, other one shallow independent short notch. No readable family crest, apprentice name or ownership verdict'),
        ('broken_rivet','ONE small clearly fractured/scuffed old metal rivet and tiny separate broken head fragment, no whole machinery, human injury, blood or forensic verdict'),
        ('detached_padding','one small detached empty protective gear lining/padding cloth sample, faded dull pale fabric with a few worn stitched edges, not clothing on body, not a wound, cure or medical experiment'),
        ('closed_medicine_bottle','ONE small modest CLOSED clean ordinary medicine bottle with plain dull cork and BLANK pale label, no dosage, readable logo, drug claim, needles, glow or person'),
        ('blank_instruction_tag','ONE small unused BLANK pale instruction tag with modest tied string, no letters, signatures, approved outcome or medical identity'),
        ('paired_water_scales','EXACTLY TWO distinct narrow old water-level measuring posts side-by-side, one taller/one shorter, modest plain short notch marks and BLANK inset panels. No readable numeric measurements or current gate/water-state verdict')],
      'bry-props-d-v1':[
        ('sluice_lever','ONE modest freestanding old manual sluice lever on a small iron/timber frame, neutral stopped position, no giant gate, water, selected open/closed outcome or labels'),
        ('segmented_stop_plug','one small ordinary segmented timber/iron water-stop plug with visible fitted plain sections, not a magical seal or opened actual sluice'),
        ('drain_sand_model','one modest DRY wooden tabletop sand model with TWO shallow branch troughs separated by a small central sand bank. Dry ordinary sand, no water/people/buildings, no chosen scheme, arrows or claimed actual damage; contents wholly independent from real waterworks'),
        ('short_meeting_table','ONE short modest neutral timber discussion table, clear top with only one tiny EMPTY document recess, no long council table, throne, people or papers/signatures'),
        ('three_nomination_chits','EXACTLY THREE separate neutral nomination tokens on a small shallow holder: plain triangular, round-notched and small rectangular wood pieces, no names, fixed faction roles or proof of authorization'),
        ('empty_tenant_bench','ONE modest EMPTY worn low tenant bench with narrow pale wood seat and two plain feet, no person/body/blanket or accepted participation'),
        ('privacy_screen','one freestanding modest opaque muted cloth privacy screen on TWO timber posts, no hidden person silhouette, glow or locked door'),
        ('blank_invitation','ONE small folded BLANK unposted invitation sheet with a plain unmarked tie, no readable names, accepted invitation, signatures or religious seal')]
    }
    common='1536x1024 genuinely TRANSPARENT RGBA pixel-art source. Serious muted medieval coastal-city HD2D, square-grid orthographic OBLIQUE camera, front edges horizontal, vertical posts, modest top surfaces, neutral top-left matte UNLIT base, crisp textured pixel clusters. Complete isolated silhouettes and transparent margins/bottom baseline, NO backdrop/ground plane/cast shadow/halo. No NPCs, people, animals, corpses, living hands, readable text/numbers, crests, banners, flames, magic, glow, cure/consent/quest/sponsorship outcome. Use locked regional128palette; no extra item beyond named components.\n'
    for ident,items in groups.items():
        text=common+'EXACTLY EIGHT isolated '+('buildings' if ident=='bry-architecture-v1' else 'props')+' in FOURcolumns and TWOrows, nominal384x512slots, clear generous spacing.\n'
        for i,(key,desc) in enumerate(items):
            s=specs['bry_'+key];text+=f'ROW{i//4+1} COLUMN{i%4+1}: {s["id"]}: {desc}. Final{s["size"][0]}x{s["size"][1]},origin{s["origin"]}.\n'
        text+='\nAPPROVED BRY-CORE-128:\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(list(groups)))
if __name__=='__main__':main()
