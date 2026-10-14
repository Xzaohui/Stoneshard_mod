"""Author the remaining R04 sprite prompts under the existing immutable generation lock."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R04-pass-v1'
def main():
    b=json.loads((P/'brief.json').read_text(encoding='utf-8'));specs={s['id']:s for s in b['sprites']};colors=json.loads((P/'palettes/pas_r04_128.json').read_text(encoding='utf-8'))['colors']
    groups={
      'r04-props-a-v1':[
        ('beam_scale','a modest wooden balance-frame grain scale with two EMPTY metal weighing pans on two separate chains, no readable weights or numbers'),
        ('comparison_board','a freestanding wooden comparison board with two side-by-side blank pale parchment fields, no writing, no seal or emblem'),
        ('mason_bench','a low heavy carpentry-and-stone repair bench with one unfinished plain stone slab on its surface, no person or tools piled over it'),
        ('cut_stones','a small irregular pile of four cut ochre-gray rectangular masonry blocks, varied chips, not a staircase or monument'),
        ('broken_cart','a damaged small two-wheel wooden grain cart, one tilted axle and one cracked wheel, empty open wagon bed, a modest part of a cart frame rather than a whole convoy'),
        ('cargo_sacks','three plain tied grain sacks in a modest low pile; no printed marks, no quantified inventory or ownership claim'),
        ('empty_drug_crate','an empty open wooden medicine shipping crate with exposed internal partitions and one blank plain wooden tag, no numbers or bottles'),
        ('public_table','a plain low rectangular neutral meeting table with four legs and worn boards, completely clear top, no documents, no chair or backdrop')],
      'r04-props-b-v1':[
        ('drug_rack','a freestanding old wooden medicine rack with a few neutral unmarked closed earthen jars, no dosage labels or glow'),
        ('drug_cabinet','a tall medicine cabinet with a4by3array of small drawers, all fronts blank, narrow low shelf, no person or magical mechanism'),
        ('case_cabinet','a narrow plain case-record cabinet with three horizontal closed drawers and one empty shallow shelf, no names or numbers'),
        ('stop_cabinet','a narrow closed stop-log cupboard with one inset blank paper holder and short iron latch, not a machine, no dials or active light'),
        ('return_mail_cabinet','a narrow returned-mail cabinet with two small blank pigeonholes over a closed wooden lower drawer, no addresses or opened letters'),
        ('empty_bed','exactly ONE empty ordinary wooden care bed with dull cream thin blanket and one small pillow; no patient, body, restraint, second bed or treatment tubes'),
        ('two_medicine_bowls','exactly TWO separate small shallow dark clay medicine bowls side by side on the same small transparent canvas, no tray or bed, no steam/glow/cure claim'),
        ('broken_rack','a damaged and abandoned wooden medicine rack with empty shelves, one splintered rail and a leaning side post, no readable papers or bottles')],
      'r04-props-c-v1':[
        ('oil_casks','two neutral closed weathered oil storage casks, wood and dull iron bands, no flame or written warning'),
        ('oil_spill','a small flat irregular dark oily patch on transparent background, off-center droplets, top-down ground decal, matte not glowing, no fire or embers'),
        ('seal_comparison_table','a short square work table with TWO small blank test impression pads and one small closed plain rust-colored metal seal tool resting separately; no authentic emblem, letters or certified result'),
        ('drag_rope','a short frayed rope lying loosely on the ground with a dragged muddy end, irregular flat trail decal, no person, no tied limbs, no prisoner or vehicle'),
        ('blank_notice','a plain low timber notice post with one blank inset wooden board, no writing, no heraldry, no royal flag'),
        ('rolled_bedding','ONE tightly rolled gray-brown blanket with plain rope ties, no second bed, no person or entitlement signal')]
    }
    common='1536x1024 genuinely transparent RGBA pixel-art sprite master. Square-grid orthographic oblique HD2D, front edges horizontal, uprights vertical, upper-left neutral unlit base lighting, worn medieval ochre-gray stone and brown wood. Crisp pixels, no gradient halos, shadows, floor plates, panels, borders, frame lines, text, numbered labels, symbols, crests, flags, people/NPCs, animals, corpses, fire, glowing lamps or story outcomes. Objects must never touch or overlap across slots. Each object has a complete freestanding silhouette with transparent margins and bottom foot/baseline; ground decals stay flat overhead. Do not add any unrequested object, backdrop, UI or readable annotation. Native runtime item/state/collision semantics are not encoded in the artwork. Final production sprites are static, binary-alpha, exact128-color palette.\n'
    for ident,items in groups.items():
        cols=4 if len(items)==8 else 3;width=384 if cols==4 else 512
        text=common+f'EXACTLY {len(items)} objects in {cols} columns and two rows, uniform {width}x512slots. Read row-major.\n'
        for i,(k,desc) in enumerate(items):
            s=specs['r04_'+k];text+=f'ROW {i//cols+1} COLUMN {i%cols+1}: {s["id"]}: {desc}. Final canvas {s["size"][0]}x{s["size"][1]}, origin {s["origin"]}.\n'
        text+='\nAPPROVED PAS-R04-128 PALETTE ONLY:\n'+', '.join(colors)+'\n';out=P/'notes'/f'prompt-{ident}.txt'
        if out.exists():assert out.read_text(encoding='utf-8')==text,'Never silently rewrite a used prompt'
        else:out.write_text(text,encoding='utf-8')
    pair=common+'One SINGLE isolated stopped historic apparatus assembly, centered with wide transparent margins. A plain EMPTY timber treatment bed on the left and a DISTINCT EMPTY low rectangular carrier trough on the right. Exactly one bed and one trough, no people, patients, bodies, blood, restraints or tests. A dull thin copper pipe mechanically connects the lower sides through a closed small valve; the pipe has a plain seal wrapping at the valve, no authentic emblem or readable writing. The apparatus is stopped and sealed, no fluid motion, vapour, glowing crystals, electrical light, active magic, cure, or scientific proof. Bed and trough must be clearly separate silhouettes joined only by the thin inert pipe. Front edges horizontal, same orthographic camera, sparse worn cloth on bed, bare carrier trough, no foundation tile or laboratory wall. This is an observation sprite for a historical closed experiment, never a visual demand to use it again. Final260x156,origin130,140.\n\nAPPROVED PAS-R04-128 PALETTE ONLY:\n'+', '.join(colors)+'\n'
    out=P/'notes/prompt-r04-sealed-pair-v1.txt'
    if out.exists():assert out.read_text(encoding='utf-8')==pair
    else:out.write_text(pair,encoding='utf-8')
    print(json.dumps(dict(prompts=[*groups,'r04-sealed-pair-v1'],spec_lock_sha256=hashlib.sha256((P/'spec_lock.md').read_bytes()).hexdigest()),ensure_ascii=False))
if __name__=='__main__':main()
