"""Author fixed R06 master requests from its locked sprite table; serial generation elsewhere."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def main():
    b=json.loads((P/'brief.json').read_text(encoding='utf-8'));specs={s['id']:s for s in b['sprites']};colors=json.loads((P/'palettes/hig_r06_128.json').read_text(encoding='utf-8'))['colors'];groups={
      'r06-architecture-v1':[
        ('bell_station','modest old cold-mountain waystation: squat timber/stone hall with a low plain slate gable and ONE small wooden bell belfry attached, ONE ordinary front door, two small unlit square windows. Low simple practical station, not grand church or fortified castle. Belfry plain small stopped iron bell, no light, statues, crosses or crests'),
        ('echo_gatehouse','small independent old gray-stone echo hall gatehouse with a low worn slate roof and plain tall front entry, asymmetric small side shutter, no copied prologue cathedral, religious icon, glowing crystal or magical entrance'),
        ('residual_well_house','small low old-stone well-access house with modest slate roof and a plain recessed dark entrance, understated weathered iron fittings; NOT immense cosmic well, laboratory, glowing portal, crystal-shaped dome or second original gemstone'),
        ('maintenance_shed','small simple mountain maintenance shed, old worn timber walls over low stone footing, plain plank roof and one front opening, a single blank exterior map holder, no readable map or extra furniture'),
        ('trial_canopy','modest isolated FOUR-post low timber canopy with an old dull pale cloth roof, empty area underneath, no table, people, labs, tubes or contents; for small ordinary samples, never human experiments'),
        ('station_table_canopy','a DISTINCT modest public courtyard awning inside the same safe bell-station complex, FOUR plain wooden posts and worn slate/plank roof, open underneath, no table or seats drawn, not a separate inn/house/cathedral')],
      'r06-props-a-v1':[
        ('bell_frame','a freestanding narrow old stopped bell frame, TWO timber uprights, crossbeam and one small dull iron bell, no toll motion, hanging person, flags or roof'),
        ('return_board','one simple return-route board on TWO short wood posts, BLANK broad face with only a single plain fork-shaped engraved route mark; no writing, readable map, distances or mandatory quest destination'),
        ('maintenance_diagram','a modest broad fixed-diagram frame on TWO short feet, BLANK dark slate face with three tiny neutral inset tabs only. Actual lines, numbers and source evidence engine-rendered, no readable diagram or text'),
        ('tool_rack','a small old timber tool rack, a few ordinary modest dull wrenches/tongs and a plain short hand lever, no magical staff, weapon collection or modern laboratory equipment'),
        ('public_table','a plain wide low neutral public discussion table with a few empty document holders and several timber legs, no writing or signatures, people or chairs'),
        ('sealed_sample_tray','one small closed sample tray with THREE closed neutral containers, no needles, fluid hooked to a person, readable contents or cure'),
        ('ordinary_material_crate','one plain modest mountain supply crate with rough neutral offcut pieces, no promised infinite supplies, labels or printed quantities'),
        ('unlit_lantern','ONE small ordinary dull iron lantern with dark unlit glass, no visible flame, glow, bright aura or light on the background')],
      'r06-props-b-v1':[
        ('cooling_gauge','one small manual cooling measurement stand with an EMPTY unmarked circular gauge face and short closed coiled copper return tube below it, low timber frame. No readable numbers, needle/readout, snow frost or actual cooling-state certification'),
        ('return_valve','one DIFFERENT manual return-valve stand: compact dull metal valve wheel on a short angular pipe, small EMPTY unmarked vertical rectangle indicator, timber foot. No needle, numbers or actual selected open/closed quest state'),
        ('residual_gauge','one DISTINCT residual-response measurement stand with a small unmarked BLANK semicircular dial and a short stopped iron pendulum holder below, narrow timber foot. Not identical to cooling stand, no readout/needle/glow or hearing source verdict'),
        ('medium_niche','one small high-wall old-gray-stone niche as freestanding wall patch, plain shutters and a tiny CLOSED dull-violet inset material compartment under a simple iron retaining cover. Violet limited to that SMALL compartment, no gemstone silhouette, original crystal copy, purple light, magic or beams'),
        ('bypass_ruler','a horizontal modest fixed bypass measuring rule with a few plain short notch marks, worn dull slate and iron feet, no readable numbers or complete-source certification'),
        ('remote_lock','a small freestanding old mechanical branch lock with a dull plain latch and closed ring clamp on a timber foot, no person, operating hand, certification seal, readable key text or modern console'),
        ('closed_discard_tank','one small CLOSED rectangular plain old-metal discard trough/tank on short feet, modest tight cover and a capped outlet, no glowing sludge, human connection, blood or open chemical process'),
        ('empty_isolation_table','one modest EMPTY isolation/sample work table, plain slate top over four low timber legs, no pillow, restraint, person, creature, tubes or readable records')],
      'r06-props-c-v1':[
        ('empty_carrier_trough','one narrow EMPTY old iron-and-stone carrier trough, elongated recessed slot with modest frame and short feet, plain neutral surface. NO person, corpse, body outline, straps, pillow, bed blanket, needles, glowing gem or magic; stopped historical housing only'),
        ('ledger_table','one plain low side ledger table with ONE closed anonymous bound ledger and a BLANK empty adjacent holder, no debt names, signatures, currency, magical contract or readable writing'),
        ('aux_coupling','one modest HORIZONTAL old-metal auxiliary coupling between TWO short straight pipe fittings, CONNECTED central clamp, dull neutral iron on short wood feet; no active liquid or beam. Final104x78, fixed outer length and foot'),
        ('aux_coupling_capped','matching HORIZONTAL auxiliary coupling with TWO capped ends and a visible small CENTRAL GAP, exact same outer length, silhouette baseline and camera as connected version, dull neutral fittings. No spill or purified/solved quest claim; illustration-only state'),
        ('safe_confirmation_table','one distinct modest neutral safety confirmation desk, plain timber with two closed BLANK record holders and a simple recess for an EMPTY frame, no checkmark, signatures, ending seal or forced selection'),
        ('neutral_receipt_cabinet','one narrow neutral record cabinet with several unmarked CLOSED shelves/drawers, no signed receipt, readable names/addresses or inventory quantity'),
        ('blank_seal_plate','one small plain DETACHED rectangular metal maintenance seal plate with empty inset panel and a tiny clamp screw, lying neutral on two small feet; no wax crest, already installed ending seal or readable label'),
        ('warning_marker','one modest small triangular gray stone/iron warning board with a plain off-white diagonal-bar pictogram, upright short stand, no words, religious rune, actual active combat boundary or glaring light')],
      'r06-props-d-v1':[
        ('empty_bench','one low EMPTY worn timber bench, no person, bed blanket, second seat clone or capacity claim'),
        ('rope_pulley','one small old stationary cargo pulley frame with a modest coil of rope, no moving hoist, dangling person or load'),
        ('cargo_crate','one plain low closed cargo crate with simple worn bands, no readable destination, goods quantity or corpse'),
        ('wear_bolt_pair','EXACTLY TWO little maintenance bolts side-by-side: one worn dull broken/thread-scuffed bolt and one intact plain bolt, no readable dates, whole machine or forensic certification'),
        ('maintenance_valve','one modest small stopped maintenance pipe valve with a plain manual wheel, dull old iron on low wood foot, no active water, glow or already chosen shutdown outcome'),
        ('waste_casks','TWO modest closed ordinary discard casks, plain old wood/metal bands, no text or spilling, no giant alchemical apparatus'),
        ('line_of_sight_pier','one short upright thick weathered gray-stone rectangular masonry pier with irregular fine joints, simple stepped stone base, no statue, heraldry, magical barrier or extra ruin'),
        ('high_record_cabinet','one small dry fixed-copy cabinet, distinct closed modest wood upper shutter over one lower horizontal drawer, all BLANK, no readable NE5 label or consent')]
    }
    common='1536x1024 genuinely TRANSPARENT RGBA pixel-art environment sprite master. Cold medieval HD2D, square-grid orthographic OBLIQUE view, all front edges horizontal, posts vertical, modest upper surface visible, neutral top-left matte UNLIT base, crisp clustered pixels. Complete independent silhouettes with transparent margins and bottom baselines, no backdrop/groundplane/castshadow/halo. NO NPCs/people/animals/corpses/readable writing or numbers/crests/religious claims/flames/magic beams/cure/consent/verifiedreadings/finalquestorendingstatus. Violet ONLY tiny closed medium compartment if explicitly specified, never elsewhere or as glow. No extra item beyond specified components. Exact locked regional128palette below.\n'
    for ident,items in groups.items():
        arch=ident=='r06-architecture-v1';cols=3 if arch else 4;text=common+('EXACTLY SIX buildings in THREEcolumns and TWOrows, nominal512x512slots.\n' if arch else 'EXACTLY EIGHT isolated props in FOURcolumns and TWOrows, nominal384x512slots.\n')
        for i,(key,desc) in enumerate(items):
            s=specs['r06_'+key];text+=f'ROW{i//cols+1} COLUMN{i%cols+1}: {s["id"]}: {desc}. Final{s["size"][0]}x{s["size"][1]},origin{s["origin"]}.\n'
        text+='\nAPPROVED HIG-R06-128 PALETTE:\n'+', '.join(colors)+'\n';f=P/'notes'/f'prompt-{ident}.txt'
        if f.exists():assert f.read_text(encoding='utf-8')==text,'Do not change a used generation prompt'
        else:f.write_text(text,encoding='utf-8')
    print(json.dumps(list(groups)))
if __name__=='__main__':main()
