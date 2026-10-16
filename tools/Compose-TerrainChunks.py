"""Compose native-scale terrain from independent images in global pixel space.

The user requested deterministic image stitching. Raw AI images are immutable;
this production step resamples diffuse materials, joins them and exports chunks.
No source panorama is enlarged, and image alpha never defines collision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/Art/terrain-chunks-v1"
ART = ROOT / "src/Art/hd2d_26x26_20261013"
CELL, CHUNK_CELLS, PAD = 26, 30, 2
CORE = CELL * CHUNK_CELLS
MATERIAL_SIZE = 20 * CELL  # Each generated patch describes 20x20 gameplay cells.
REGION_SIZE = (270, 180)  # Six full native outdoor cells, not six small rooms.
REGIONS = {
    "R01": ("r03-pine", "r01-earth", [(39, 48), (112, 75), (159, 38), (207, 66), (171, 131), (76, 135)]),
    "R02": ("r03-pine", "r02-gravel", [(98, 49), (185, 45), (61, 85), (100, 116), (177, 94), (212, 125), (142, 142), (42, 140)]),
    "R03": ("r03-pine", "r01-earth", [(47, 37), (96, 42), (163, 31), (217, 63), (51, 86), (108, 92), (155, 78), (205, 114), (54, 142), (108, 138), (164, 145), (231, 150)]),
    "R04": ("r04-grit", "r01-earth", [(42, 45), (139, 36), (83, 81), (203, 44), (46, 131), (113, 129), (167, 83), (216, 120), (163, 142), (237, 155)]),
    "R05": ("r05-damp", "r02-gravel", [(51, 43), (113, 37), (190, 48), (67, 91), (140, 88), (208, 109), (111, 139), (218, 149)]),
    "R06": ("r06-rock", "r04-grit", [(46, 137), (182, 35), (223, 73), (36, 53), (87, 90), (132, 44), (147, 107), (214, 139), (104, 144), (47, 167)]),
}
BATCHES = ["R01-streets-v1", "R01-camp-canal-v2", "R02-river-v2", "R03-maen-v1", "R04-pass-v1", "R05-basin-v1", "R06-highland-v1"]
LANDMARKS = {
    "R01-port":"r01_port_kiosk", "R01-camp":"r01_worker_shed", "R01-hearing":"r01_hearing_canopy",
    "R01-workshop":"r01_forge_building", "R01-canal":"r01_canal_entry", "R01-salt":"r01_abandoned_post",
    "R02-ferryold":"n1_bellhouse_exterior", "R02-tax":"r02_tax_house", "R02-inn":"r02_ferry_inn",
    "R02-well":"r02_filter_shelter", "R02-tracks":"r02_crate_corner", "R02-repair":"r02_repair_canopy",
    "R02-ford":"r02_road_sign", "R02-fork":"r02_road_sign", "R03-mill":"r03_mill_house",
    "R03-ration":"r03_granary", "R03-library":"r03_low_library", "R03-burnt":"r03_burned_frame",
    "R03-watch":"r03_watch_shelter", "R03-scribe":"r03_scribe_shed", "R04-inn":"r04_neutral_inn",
    "R04-cellar":"r04_store_house", "R04-scale":"r04_beam_scale", "R04-mason":"r04_mason_shed",
    "R04-camp":"r04_windbreak", "R04-drug":"r04_drug_pavilion", "R04-seal":"r04_seal_shelter",
    "R05-care":"r05_care_lodge", "R05-ward":"r05_ward_house", "R05-well":"r05_well_drain_shed",
    "R05-village":"r05_filter_well", "R05-shelter":"r05_voluntary_hut", "R06-station":"r06_bell_station",
    "R06-echo":"r06_echo_gatehouse", "R06-residual":"r06_residual_well_house", "R06-sign":"r06_return_board",
    "R06-shed":"r06_maintenance_shed", "R06-trial":"r06_trial_canopy", "R06-table":"r06_station_table_canopy",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scene_specs():
    n1 = read(ART / "native_layouts.json")
    n2 = read(ROOT / "src/Art/native-n2-hd2d-v1/manifest.json")["scenes"]
    result = []
    bases = {"r_eao_n1_yard": "stone", "r_eao_n1_bellhouse": "wood", "r_eao_n1_underpass": "stone",
             "r_eao_n2_camp": "wood", "r_eao_n2_winch": "stone", "r_eao_n2_side": "stone"}
    for source in n1 + n2:
        room = source.get("room", source.get("id"))
        if room not in bases:
            continue
        result.append(dict(room=room, size_cells=[40, 30], base=bases[room], overlay=False,
                           walkable_rectangles=source["walkable_rectangles"], blocked_rectangles=source.get("blocked_rectangles", []),
                           paths=[], ground_regions=[], role="interior" if room != "r_eao_n1_yard" else "legacy_exterior"))
        if room=="r_eao_n1_yard":
            result[-1]["secondary"]="r02-gravel"
    old = read(ROOT / "src/Art/native-n2-built-v1/layout.json")
    result.append(dict(room=old["room"], size_cells=[old["columns"], old["rows"]], base="r01-earth", overlay=False,
                       walkable_rectangles=old["walkable_rectangles"], blocked_rectangles=[b["blocked"] for b in old["buildings"]],
                       paths=[], ground_regions=[], role="legacy_exterior",secondary="r02-gravel"))
    # Same independent native building footprints and door cells as the live preset.
    # The large ground is transparent outside work yards and their irregular footpaths.
    result.append(dict(room="r_eao_n2_world", size_cells=[90, 90], base="r01-earth", overlay=True,
                       walkable_rectangles=[], blocked_rectangles=[], role="native_world_surface",secondary="r02-gravel",
                       paths=[dict(points=[[19, 49], [29, 46], [45, 47], [61, 46], [71, 51]], radius=1.6),
                              dict(points=[[29, 42], [29, 46]], radius=1.3),
                              dict(points=[[45, 42], [45, 47]], radius=1.3),
                              dict(points=[[61, 42], [61, 46]], radius=1.3)],
                       ground_regions=[dict(rect=[24, 36, 34, 45], feather=2.0),
                                       dict(rect=[41, 37, 49, 45], feather=2.0),
                                       dict(rect=[56, 36, 66, 45], feather=2.0)],
                       native_doors=[[29, 42], [45, 42], [61, 42]],
                       origin_note="Existing temporary world cell 41,37 retained. Planned G1 43,37 is not migrated by artwork."))
    if len(result) != 8 or len({s["room"] for s in result}) != 8:
        raise ValueError("Expected six current story rooms, one legacy court and one native surface")
    return result


def regional_plans():
    plans = []
    for ident, (base, trail, positions) in REGIONS.items():
        files = list((ROOT / "design/02_世界与地图").glob(f"区域_{ident}_*.md"))
        if len(files) != 1:
            raise ValueError(f"Ambiguous story region: {ident}")
        text = files[0].read_text(encoding="utf-8")
        matches = re.findall(r"(?m)^\| (" + ident + r"-[a-z]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", text)
        if len(matches) != len(positions):
            raise ValueError(f"Narrative budget changed: {ident}, {len(matches)}")
        nodes = [dict(id=m[0], title=m[1].strip(), kind=m[2].strip(), purpose=m[3].strip(), cell=list(p))
                 for m, p in zip(matches, positions)]
        by_name = {n["title"]: n for n in nodes}
        edges, unresolved = [], []
        for left, right in re.findall(r"(?m)^- ([^\n↔]+) ↔ ([^\n↔]+)", text):
            left, right = left.strip(), right.strip().rstrip("。；")
            if left in by_name and right in by_name:
                edges.append([by_name[left]["id"], by_name[right]["id"]])
            else:
                unresolved.append([left, right])
        for node in nodes:
            if node["id"] in LANDMARKS:
                node["landmark"]=LANDMARKS[node["id"]]
        river = None
        if ident == "R01":
            river = dict(points=[[179, 180], [183, 143], [190, 115], [223, 105], [270, 112]], radius=2.6)
        if ident == "R02":
            river = dict(points=[[134, -10], [144, 40], [131, 90], [148, 140], [134, 190]], radius=5.5)
        plans.append(dict(id=ident, size_cells=list(REGION_SIZE), base=base, trail=trail, nodes=nodes, edges=edges, river=river,
                          external_or_unresolved_edges=unresolved, source=str(files[0].relative_to(ROOT)).replace("\\", "/"),
                          source_sha256=sha(files[0]), status="authoring_plan_not_installed_world_geography",
                          coordinate_space="relative region authoring cells, no political or global world coordinates"))
    return plans


def graded_material(key,path):
    image=Image.open(path).convert("RGB")
    if key=="r03-pine":
        # Match the dusty olive hue of the inspected native grass reference,
        # while preserving the immutable AI source and all object proportions.
        pixels=np.asarray(image,dtype=np.float32)*np.array([0.88,1.06,0.96])
        image=Image.fromarray(np.clip(np.rint(pixels),0,255).astype(np.uint8))
    return image


def production_palette(sources):
    # The old harbor-only palette erased grass greens. Build one shared palette
    # from all actual production materials, so soil, grass and water keep hue.
    colors=[]
    budgets={"r03-pine":24,"r05-damp":16,"wood":16}
    for key,path in sources.items():
        quant=graded_material(key,path).resize((128,128),Image.Resampling.BOX).quantize(colors=budgets.get(key,12),method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
        values=quant.getpalette()
        for i in range(0,budgets.get(key,12)*3,3):
            color=values[i:i+3]
            if color not in colors:
                colors.append(color)
    if len(colors)>128:
        raise ValueError("Shared production palette budget exceeded")
    colors += [colors[-1]]*(128-len(colors))
    palette=Image.new("P",(1,1))
    palette.putpalette([v for color in colors+[colors[-1]]*128 for v in color])
    return palette,colors


def periodic_material(key,path,palette):
    """Equal edge samples across a narrow wrap band, preserving raw source files."""
    raw=graded_material(key,path)
    if "n1-surfaces-v1" in path.parts:
        # These existing diffuse panels were authored for 1040x780 native
        # pixels. Sample a local 20-cell patch; do not shrink the whole panel.
        native=raw.resize((1040,780),Image.Resampling.NEAREST)
        im=native.crop((260,130,260+MATERIAL_SIZE,130+MATERIAL_SIZE))
    elif path.stem=="n1_water_base":
        im=raw.crop((260,130,260+MATERIAL_SIZE,130+MATERIAL_SIZE))
    else:
        im=raw.resize((MATERIAL_SIZE,MATERIAL_SIZE),Image.Resampling.NEAREST)
    a = np.asarray(im, dtype=np.float32).copy()
    band = 22
    for axis in (1, 0):
        b = np.swapaxes(a, 0, axis)
        for k in range(band):
            weight = (1.0 - k / band) * 0.5
            before, after = b[k].copy(), b[-1-k].copy()
            b[k] = before * (1-weight) + after * weight
            b[-1-k] = after * (1-weight) + before * weight
        a = np.swapaxes(b, 0, axis)
    return np.asarray(Image.fromarray(np.clip(np.rint(a), 0, 255).astype(np.uint8)).quantize(palette=palette, dither=Image.Dither.NONE).convert("RGB"))


def noise(x, y):
    # Integer global coordinates, without global/random state or chunk seeds.
    value = (x.astype(np.uint64) * np.uint64(73856093)) ^ (y.astype(np.uint64) * np.uint64(19349663))
    # Half-open [0,1): full coverage must never leave a one-in-256 pinhole.
    return ((value ^ (value >> 13)) % 256).astype(np.float32) / 256


def distance_to_paths(x, y, paths):
    dist = np.full(np.broadcast_shapes(x.shape, y.shape), 1e6, dtype=np.float32)
    for path in paths:
        for a, b in zip(path["points"], path["points"][1:]):
            ax, ay, bx, by = a[0]*CELL, a[1]*CELL, b[0]*CELL, b[1]*CELL
            dx, dy = bx-ax, by-ay
            t = np.clip(((x-ax)*dx + (y-ay)*dy) / max(1, dx*dx+dy*dy), 0, 1)
            d = np.hypot(x-(ax+t*dx), y-(ay+t*dy)) - path["radius"]*CELL
            dist = np.minimum(dist, d)
    return dist


def render(spec, materials, box):
    """Sample any pixel rectangle; adjacent chunks share identical overlap pixels."""
    left, top, width, height = box
    x = np.arange(left, left+width, dtype=np.int64)[None, :]
    y = np.arange(top, top+height, dtype=np.int64)[:, None]
    grain = noise(x, y)
    base = materials[spec["base"]]
    rgb = base[y % MATERIAL_SIZE, x % MATERIAL_SIZE].copy()
    # Mix two phases under a broad, coherent field. A chunk never restarts the
    # pattern, and the eye does not see a ten-cell repeated square carpet.
    phase = 0.5 + 0.22*np.sin(x/173.0+y/211.0) + 0.20*np.cos(x/293.0-y/137.0)
    alternate=base[(y+113) % MATERIAL_SIZE, (x+83) % MATERIAL_SIZE]
    rgb=np.where((phase > grain)[...,None],rgb,alternate)
    if spec.get("secondary"):
        secondary=materials[spec["secondary"]][(y+19)%MATERIAL_SIZE,(x+53)%MATERIAL_SIZE]
        variation=0.18+0.12*np.sin(x/277.0+y/193.0)
        rgb=np.where((variation>grain)[...,None],secondary,rgb)
    alpha = np.full((height, width), 255, dtype=np.uint8)
    paths = spec.get("paths", [])
    coverage=np.zeros(alpha.shape,dtype=np.float32)
    if paths:
        distance = distance_to_paths(x, y, paths)
        for region in spec.get("ground_regions", []):
            a, b, c, d = [v*CELL for v in region["rect"]]
            outside = np.maximum.reduce([np.broadcast_to(a-x, alpha.shape), np.broadcast_to(x-c, alpha.shape),
                                         np.broadcast_to(b-y, alpha.shape), np.broadcast_to(y-d, alpha.shape)])
            distance = np.minimum(distance, outside / max(0.2, region.get("feather", 1)))
        # Coherent waves and pixel dither make the dirt/grass boundary irregular,
        # with no rectangle on a chunk edge. This never changes a collision grid.
        distance += 5*np.sin(x/19.0) + 4*np.cos(y/23.0)
        coverage = np.clip(0.5-distance/24.0, 0, 1)
        if spec.get("overlay"):
            alpha = np.where(coverage > grain, 255, 0).astype(np.uint8)
        elif spec.get("trail"):
            trail = materials[spec["trail"]][(y+73) % MATERIAL_SIZE, (x+41) % MATERIAL_SIZE]
            rgb = np.where((coverage > grain)[..., None], trail, rgb)
    if spec.get("river"):
        distance=distance_to_paths(x,y,[spec["river"]])
        water_coverage=np.clip(0.5-distance/32.0,0,1)
        water=materials["water"][(y+31)%MATERIAL_SIZE,(x+17)%MATERIAL_SIZE]
        water_pixels=water_coverage>grain
        rgb=np.where(water_pixels[...,None],water,rgb)
        # A separate timber deck spans actual path/water intersections; the
        # ford node stays gravel. This is authoring art, not native collision.
        crossing=water_pixels & (coverage>grain)
        wood=materials["wood"][(y+41)%MATERIAL_SIZE,(x+23)%MATERIAL_SIZE]
        if spec["id"]=="R02":
            ford=((x-142*CELL)**2+(y-142*CELL)**2)<(15*CELL)**2
            wood=np.where(ford[...,None],materials["r02-gravel"][(y+41)%MATERIAL_SIZE,(x+23)%MATERIAL_SIZE],wood)
        rgb=np.where(crossing[...,None],wood,rgb)
    if not spec.get("overlay") and "walkable_rectangles" in spec:
        cells = np.zeros((height, width), dtype=bool)
        for a, b, c, d in spec["walkable_rectangles"]:
            cells |= (x >= a*CELL) & (x < (c+1)*CELL) & (y >= b*CELL) & (y < (d+1)*CELL)
        for a, b, c, d in spec.get("blocked_rectangles", []):
            cells &= ~((x >= a*CELL) & (x < (c+1)*CELL) & (y >= b*CELL) & (y < (d+1)*CELL))
        alpha = np.where(cells, 255, 0).astype(np.uint8)
    bounds = (x >= 0) & (y >= 0) & (x < spec["size_cells"][0]*CELL) & (y < spec["size_cells"][1]*CELL)
    alpha = np.where(bounds, alpha, 0).astype(np.uint8)
    rgb = np.where((alpha > 0)[..., None], rgb, 0)
    return Image.fromarray(np.dstack([rgb, alpha]))


def export_scenes(scenes, materials):
    assets = []
    for scene in scenes:
        scene["chunks"] = []
        width, height = [v*CELL for v in scene["size_cells"]]
        for top in range(0, height, CORE):
            for left in range(0, width, CORE):
                ident = f'{scene["room"]}__{left//CORE}_{top//CORE}'
                path = OUT / "chunks" / (ident + ".png")
                path.parent.mkdir(parents=True, exist_ok=True)
                render(scene, materials, (left-PAD, top-PAD, CORE+2*PAD, CORE+2*PAD)).save(path)
                chunk = dict(id=ident, path="chunks/"+path.name, x=left, y=top,
                             width=min(CORE, width-left), height=min(CORE, height-top),
                             image_size=[CORE+2*PAD, CORE+2*PAD], origin=[0, 0], sha256=sha(path))
                scene["chunks"].append(chunk)
                assets.append(chunk)
    return assets


def vegetation_stamps():
    records=[]; result={}
    for name,size,origin in [("oak-tree",(104,156),(52,148)),("pine-tree",(104,156),(52,148)),("low-rocks",(78,52),(39,47))]:
        path=OUT/"raw"/(name+".png")
        if not path.exists():
            raise ValueError("Missing independently generated vegetation: "+str(path))
        raw=Image.open(path).convert("RGBA")
        if raw.getchannel("A").getextrema()[0]!=0:
            raise ValueError("Vegetation must have genuine transparency: "+name)
        alpha=raw.getchannel("A").point(lambda v:255 if v>=128 else 0)
        box=alpha.getbbox(); raw.putalpha(alpha); crop=raw.crop(box)
        scale=min((size[0]-6)/crop.width,(origin[1]-2)/crop.height)
        fitted=(max(1,round(crop.width*scale)),max(1,round(crop.height*scale)))
        sprite=Image.new("RGBA",size)
        sprite.alpha_composite(crop.resize(fitted,Image.Resampling.NEAREST),((size[0]-fitted[0])//2,origin[1]-fitted[1]))
        target=OUT/"props"/(name+".png"); target.parent.mkdir(exist_ok=True); sprite.save(target)
        result[name]=(sprite,origin)
        records.append(dict(id=name,path="props/"+target.name,origin=list(origin),size=list(size),source="raw/"+path.name,
                            source_sha256=sha(path),sha256=sha(target),crop=list(box),fitted_size=list(fitted),resample="nearest",
                            collision="not supplied; region authoring preview only",runtime_verified=False))
    write(OUT/"props/manifest.json",dict(assets=records,runtime_verified=False))
    return result


def scatter(plan,paths):
    density={"R01":0.18,"R02":0.23,"R03":0.72,"R04":0.18,"R05":0.36,"R06":0.35}[plan["id"]]
    result=[]
    for row in range(5,176,5):
        for column in range(5,266,5):
            value=(column*73856093 ^ row*19349663 ^ int(plan["id"][1:])*83492791)&0xffffffff
            value=((value^(value>>13))*1274126177)&0xffffffff
            if value/4294967296>=density:
                continue
            cx=column+((value>>8)%5)-2; cy=row+((value>>16)%5)-2
            if any((cx-n["cell"][0])**2+(cy-n["cell"][1])**2<100 for n in plan["nodes"]):
                continue
            px,py=np.array([[cx*CELL]]),np.array([[cy*CELL]])
            if distance_to_paths(px,py,paths)[0,0]<3.2*CELL:
                continue
            if plan.get("river") and distance_to_paths(px,py,[plan["river"]])[0,0]<3.5*CELL:
                continue
            kind="pine-tree" if plan["id"] in ["R03","R06"] else "oak-tree"
            if (value>>25)%5==0 or plan["id"]=="R04" and (value>>24)%3!=0:
                kind="low-rocks"
            result.append((cx,cy,kind))
    return result


def export_plans(plans, materials, preview_dir):
    preview_dir.mkdir(parents=True, exist_ok=True)
    stamps={}
    for parent in [ART]+[ART/"batches"/b for b in BATCHES]:
        for a in read(parent/"manifest.json")["assets"]:
            if a["id"] in LANDMARKS.values():
                stamps[a["id"]]=(parent/a["path"],a.get("sprite_origin",a["origin"]))
    plan_records=[]; vegetation=vegetation_stamps()
    for plan in plans:
        nodes = {n["id"]: n for n in plan["nodes"]}
        paths=[]
        for index,(a,b) in enumerate(plan["edges"]):
            ax,ay=nodes[a]["cell"]; bx,by=nodes[b]["cell"]
            # Keep endpoints, bend the intervening country lane gently.
            length=max(1,math.hypot(bx-ax,by-ay)); bend=3*math.sin(index*1.7)
            mid=[(ax+bx)/2-(by-ay)/length*bend,(ay+by)/2+(bx-ax)/length*bend]
            paths.append(dict(points=[[ax,ay],mid,[bx,by]],radius=1.8))
        clearings=[dict(rect=[n["cell"][0]-6,n["cell"][1]-4,n["cell"][0]+6,n["cell"][1]+2],feather=2) for n in plan["nodes"]]
        recipe = dict(plan, paths=paths,ground_regions=clearings)
        width, height = [v*CELL for v in plan["size_cells"]]
        image = Image.new("RGBA", (width, height))
        for top in range(0, height, CORE):
            for left in range(0, width, CORE):
                tile = render(recipe, materials, (left, top, min(CORE, width-left), min(CORE, height-top)))
                image.alpha_composite(tile, (left, top))
        image.convert("RGB").save(preview_dir / f'{plan["id"]}-ground-7020x4680.png')
        # Only individual object sprites, at their existing 26px grid scale.
        # Never paste a whole room, and never scale a village to fit one tile.
        used=[]; placements=[]
        for node in sorted(plan["nodes"],key=lambda n:n["cell"][1]):
            if "landmark" not in node:
                continue
            path,origin=stamps[node["landmark"]]
            stamp=Image.open(path).convert("RGBA")
            px=node["cell"][0]*CELL+13-origin[0]
            py=node["cell"][1]*CELL+13-origin[1]
            placements.append((node["cell"][1]*CELL,stamp,px,py))
            used.append(dict(node=node["id"],asset=node["landmark"],source=str(path.relative_to(ROOT)).replace("\\","/"),
                             source_sha256=sha(path),pixel_anchor=[node["cell"][0]*CELL+13,node["cell"][1]*CELL+13],scale=1))
        ecology=scatter(plan,paths)
        for cx,cy,kind in ecology:
            stamp,origin=vegetation[kind]
            placements.append((cy*CELL,stamp,cx*CELL+13-origin[0],cy*CELL+13-origin[1]))
        for _,stamp,px,py in sorted(placements,key=lambda p:p[0]):
            image.alpha_composite(stamp,(px,py))
        image.convert("RGB").save(preview_dir/f'{plan["id"]}-assembly-7020x4680.png')
        # Labels are a separate authoring guide, never baked into a game image.
        guide = image.resize((1800, 1200), Image.Resampling.NEAREST).convert("RGB")
        draw = ImageDraw.Draw(guide)
        for n in plan["nodes"]:
            px, py = n["cell"][0]*1800/270, n["cell"][1]*1200/180
            draw.ellipse((px-5, py-5, px+5, py+5), fill="#f1d78e", outline="#252320", width=2)
            draw.text((px+8, py+4), n["id"], fill="#f1d78e", stroke_width=2, stroke_fill="#252320")
        guide.save(preview_dir / f'{plan["id"]}-authoring-guide.png')
        plan_records.append(dict(region=plan["id"],native_cell_size=CELL,image_pixels=[width,height],
                                 independent_landmarks=used,vegetation_placements=[dict(cell=[cx,cy],asset=kind) for cx,cy,kind in ecology],
                                 status=plan["status"],collision_verified=False))
    write(preview_dir/"preview-manifest.json",dict(regions=plan_records,runtime_verified=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--previews", action="store_true")
    parser.add_argument("--preview-only", action="store_true",help="Only write ignored authoring previews; leave package inputs unchanged")
    args = parser.parse_args()
    scenes, plans = scene_specs(), regional_plans()
    plan = dict(schema=1, cell_size=CELL, chunk_cells=CHUNK_CELLS, gutter=PAD, scenes=scenes, regions=plans,
                rules=["Global pixel sampling, never per-chunk randomness", "Raw materials are local diffuse patches, never full scenes",
                       "Scene geometry and native doors own collision", "Region authoring grids are not installed global geography"])
    if not args.preview_only:
        write(OUT / "layout.json", plan)
    if args.plan_only:
        print(json.dumps(dict(scenes=len(scenes), regions=len(plans), nodes=sum(len(p["nodes"]) for p in plans),
                              edges=sum(len(p["edges"]) for p in plans), unresolved={p["id"]: p["external_or_unresolved_edges"] for p in plans if p["external_or_unresolved_edges"]}), ensure_ascii=False))
        return
    sources = {key: OUT / "raw" / (key+".png") for base, trail, _ in REGIONS.values() for key in (base, trail)}
    sources.update(wood=ROOT / "src/Art/scene-style-repairs-20261015/n1-surfaces-v1/raw/bellhouse-wood-continuous-v2.png",
                   stone=ROOT / "src/Art/scene-style-repairs-20261015/n1-surfaces-v1/raw/quay-stone-continuous-v2.png",
                   water=ART/"assets/backgrounds/n1_water_base.png")
    palette,colors=production_palette(sources)
    materials = {key: periodic_material(key,path,palette) for key, path in sources.items()}
    if args.preview_only:
        export_plans(plans,materials,ROOT/"artifacts/terrain-chunks-0327/plans")
        print(json.dumps(dict(regions=len(plans),preview_only=True,runtime_verified=False)))
        return
    write(OUT/"production-palette.json",dict(colors=colors,material_patch_pixels=MATERIAL_SIZE,native_cells_per_patch=20,
          method="One shared 128-color palette with per-material hue budgets; grass 24, damp/wood 16, other surfaces 12",
          color_calibration={"r03-pine":[0.88,1.06,0.96]},existing_diffuse_panels_native_pixels=[1040,780]))
    assets = export_scenes(scenes, materials)
    inputs=list(sources.values())+[Path(__file__).resolve(),OUT/"prompts-and-provenance.json",
            ART/"native_layouts.json",ROOT/"src/Art/native-n2-hd2d-v1/manifest.json",
            ROOT/"src/Art/native-n2-built-v1/layout.json",OUT/"production-palette.json"]
    inputs += [ROOT/p["source"] for p in plans]
    manifest = dict(schema=1, cell_size=CELL, chunk_cells=CHUNK_CELLS, gutter=PAD, scenes=scenes, assets=assets,
                    source_sha256={str(path.relative_to(ROOT)).replace("\\", "/"): sha(path) for path in inputs},
                    layout_sha256=sha(OUT/"layout.json"), runtime_verified=False,
                    scope="Eight existing room/surface floor renderers; six regional authoring plans remain separate from installed geography")
    write(OUT / "manifest.json", manifest)
    if args.previews:
        export_plans(plans, materials, ROOT / "artifacts/terrain-chunks-0327/plans")
    print(json.dumps(dict(assets=len(assets), scenes=len(scenes), regions=len(plans), native_world_pixels=90*CELL,
                          largest_regional_plan_pixels=[v*CELL for v in REGION_SIZE], runtime_verified=False)))


if __name__ == "__main__":
    main()
