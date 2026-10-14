"""Author the remaining sprite prompts from the locked R05 asset table."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
def main():
    brief=json.loads((P/'brief.json').read_text(encoding='utf-8'));specs={s['id']:s for s in brief['sprites']};colors=json.loads((P/'palettes/ash_r05_128.json').read_text(encoding='utf-8'))['colors']
    groups={
      'r05-props-a-v1':[
        ('water_bucket_pair','EXACTLY TWO separate ordinary water buckets side by side: one has a small muted rusty-red painted bucket-shaped glyph panel, the other a pale off-white cloth bucket glyph panel. Different visible shapes/panels as well as colors, no letters or water-purity verdict'),
        ('warning_board','plain timber warning board with TWO large simple bucket-shaped pictograms, muted rust-brown red and off-white, and one plain small crossing bar under the hazard-side glyph; no writing, numbers, heraldry or disease diagnosis'),
        ('public_table','plain low neutral meeting table, worn old timber and four legs, clear top, no documents or NPCs'),
        ('water_gauge','a slender weathered measuring post with blank short horizontal notch marks, no readable numbers or current-water-status verdict'),
        ('reed_cluster','an irregular off-center clump of sparse COLD temperate reeds and thin dry seed heads, muted olive and brown, not palm fronds, tropical flowers or giant lush leaves'),
        ('sample_bucket','ONE small plain wooden sample bucket with a modest pale tied cloth tag, no text or claimed clean water'),
        ('herb_bundle','a small loose bundle of ordinary temperate dried leaves and stems, not a magical flower, panacea or glowing herb'),
        ('filter_rack','a freestanding ordinary wooden filtering rack with modest cloth/mesh tray and empty trough, no light, alchemical apparatus or guarantee of safe water')],
      'r05-props-b-v1':[
        ('medicine_cabinet','a warm-brown ordinary medicine cabinet with several small unmarked closed drawers, no medicines displayed, no readable labels or dosage'),
        ('case_cabinet','a narrow anonymous case cabinet with THREE horizontal closed drawers and one empty upper shelf, no names or symbols'),
        ('name_cabinet','a distinct narrow identity-record cabinet with TWO tall closed doors over one short lower drawer, no readable personal names or addresses'),
        ('inspection_table','low plain examination/record comparison table with a blank flat clipboard holder only, no person, restraints or medical procedure'),
        ('closed_sample_tray','small sealed ordinary sample tray, a few closed unmarked glass/wood vials, no fluid connected to a person, no needle, dosage or active apparatus'),
        ('empty_care_bed','EXACTLY ONE empty simple ordinary care bed, old timber frame, dull cream thin blanket and one small pillow, no patient, second bed, tubes, blood or restraint'),
        ('privacy_curtain','one freestanding modest privacy curtain on TWO wooden posts, faded pale gray cloth hanging between posts, no hidden human silhouette, no glow'),
        ('schedule_board','plain small board with a few blank inset rectangular holders for engine-rendered dates, no readable writing, clock hands, cure/consent or signed outcome')],
      'r05-props-c-v1':[
        ('old_living_pipe','one HORIZONTAL straight old iron/wood living-water pipe segment with dark oxidized rings and worn fittings. End-to-end straight156wide production silhouette, no active flowing liquid'),
        ('new_waste_pipe','one HORIZONTAL straight newer dull gray waste-water pipe segment, same camera, outer length and baseline as the old segment, clean newer clamps, no colored fluid glow. This is the BASE CONNECTED pipe art'),
        ('new_waste_pipe_capped','the matching newer gray pipe segment with TWO separate capped ends and a small visible central GAP, same outer length and foot baseline as the connected new pipe. No spilled liquid or automatic purification; illustrative disconnected variant only'),
        ('valve_closed','a modest closed iron pipe valve with a small dull round control wheel, compact freestanding assembly, no glow or active flow'),
        ('clamp_pair','TWO small pipe clamps side by side, one worn dark old clamp and one cleaner dull gray new clamp, each with a tiny BLANK date-tag plate; no dates or proof certification'),
        ('low_gate','a short narrow stopped sliding sluice gate in a plain wooden/iron frame, front-facing, no enormous dam, crest, active water or people'),
        ('bypass_wheel','a freestanding modest iron-and-wood bypass control wheel on a short pipe foot, neutral stopped position, no selected quest method'),
        ('lift_platform','a modest empty wooden cargo lift platform with low rails, simple unlit pulley/rope frame, no people or goods, no motion or giant mining machine')],
      'r05-props-d-v1':[
        ('high_record_cabinet','a small dry fixed-record cabinet with a CLOSED pale inset panel and short shuttered shelf, no readable key evidence text'),
        ('optional_parameter_shelf','a separate low old wooden optional-data shelf with a few neutral blank bound folders, not the fixed safe-copy cabinet'),
        ('research_refuge_door','one plain closed SOUTH-facing refuge door in a worn timber frame with a small square shutter, narrow plank panel, no researcher visible, no text or ownership crest'),
        ('workers_refuge_door','a DIFFERENT closed EAST-side refuge door frame, broader two-plank-leaf work doorway with a simple horizontal iron latch, orthographic oblique front facade, no workers or human hands, no identical copy of research door'),
        ('maintenance_ladder','one narrow tall wooden maintenance ladder with worn rungs, no person, no stair room or ground base'),
        ('empty_crate','one empty plain wooden lift crate, open top, no cargo, body, printed numbers or document contents'),
        ('sitting_bench','one low ordinary neutral waiting bench, bare worn boards, no seated person or blanket body'),
        ('waste_casks','two neutral closed old waste casks with plain worn wood and dull bands, no readable poison labels, leaking gore or burning fluid')],
      'r05-props-e-v1':[
        ('foam_decal','a small irregular FLAT overhead gray-white foam/scum patch with off-center loose bubbles, real transparent background between ragged patches, no water plane, no red blood or pollution-cause verdict'),
        ('inactive_basin','a small modest EMPTY inactive stone/copper ritual-work basin, worn chipped rim, low simple supports and no universal machine, readable runes, flames, glowing crystal, magical beam or human-connected tube')]
    }
    common='1536x1024 genuinely transparent RGBA static pixel-art sprite master. Cold somber medieval HD2D square-grid orthographic oblique, front edges horizontal, vertical posts, upper-left neutral UNLIT matte base, crisp textured pixels, exact regional128palette. Complete separate freestanding silhouettes, transparent margins and bottom baseline, no shadow/backdrop/color halos, no labels/frame borders, no NPCs/people/creatures/corpses, readable writing or numbers, kingdoms/crests/religious claims, lit lights, fire, magic beams, cured/consenting/rescued status, inventory or actual capacity promise. No added object except the specified item components. Physical state and disease causality remain engine/story matters.\n'
    for ident,items in groups.items():
        cols=4 if len(items)==8 else 2;text=common+f'EXACTLY{len(items)} isolated objects in {cols}columns and '+('two rows, uniform384x512slots.\n' if cols==4 else 'one row, two wide evenly separated areas.\n')
        for i,(k,desc) in enumerate(items):
            s=specs['r05_'+k];text+=f'ROW{i//cols+1} COLUMN{i%cols+1}: {s["id"]}: {desc}. Final{s["size"][0]}x{s["size"][1]},origin{s["origin"]}.\n'
        text+='\nAPPROVED ASH-R05-128 PALETTE:\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text,'Do not overwrite used prompt'
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(dict(prompts=list(groups),lock_sha256=hashlib.sha256((P/'spec_lock.md').read_bytes()).hexdigest()),ensure_ascii=False))
if __name__=='__main__':main()
