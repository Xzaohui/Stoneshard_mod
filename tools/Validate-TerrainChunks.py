"""Check actual exported pixels and story budgets without importing the compositor."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"src/Art/terrain-chunks-v1"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main():
    checks=[]
    def check(value,name):
        if not value:
            raise AssertionError(name)
        checks.append(name)
    manifest=read(FOLDER/"manifest.json")
    layout=read(FOLDER/"layout.json")
    provenance=read(FOLDER/"prompts-and-provenance.json")
    check((manifest["cell_size"],manifest["chunk_cells"],manifest["gutter"])==(26,30,2),"native-grid-and-sampling-gutter")
    check(sha(FOLDER/"layout.json")==manifest["layout_sha256"],"frozen-layout-sha")
    palette=read(FOLDER/"production-palette.json")
    check(palette["material_patch_pixels"]==520 and palette["native_cells_per_patch"]==20,"generated-local-patch-is-twenty-native-cells")
    check(len(palette["colors"])==128,"one-shared-128-color-production-palette")
    check(sum(g>=r*0.95 and g>b*1.25 for r,g,b in palette["colors"])>=4,"grass-olive-hues-retained-in-production-palette")
    check(any("bellhouse-wood-continuous-v2.png" in path for path in manifest["source_sha256"]),"current-native-scale-horizontal-board-source-retained")
    check(len(provenance["files"])==6,"six-independent-generated-materials")
    for record in provenance["files"]:
        path=FOLDER/record["final_relative_path"]
        check(sha(path)==record["sha256"],"immutable-raw-"+record["file"])
        check(record["intent"]=="generate" and record["exact_prompt"] and not record["transparent_background"],"generation-prompt-and-opaque-surface-"+record["file"])
    for name,expected in manifest["source_sha256"].items():
        check(sha(ROOT/name)==expected,"source-current-"+name)
    check([len(p["nodes"]) for p in layout["regions"]]==[6,8,12,10,8,10],"six-current-story-node-budgets-total-54")
    check(sum(len(p["edges"]) for p in layout["regions"])==60,"sixty-declared-local-story-links")
    for region in layout["regions"]:
        nodes={n["id"] for n in region["nodes"]}
        check(not region["external_or_unresolved_edges"] and all(a in nodes and b in nodes for a,b in region["edges"]),"resolved-story-links-"+region["id"])
        check(region["size_cells"]==[270,180] and region["status"]=="authoring_plan_not_installed_world_geography","region-scale-and-honest-runtime-boundary-"+region["id"])
        reached=set(); todo=[next(iter(nodes))]
        while todo:
            at=todo.pop()
            if at in reached:
                continue
            reached.add(at)
            for a,b in region["edges"]:
                if a==at: todo.append(b)
                if b==at: todo.append(a)
        check(reached==nodes,"story-node-graph-connected-"+region["id"])
    for scene in manifest["scenes"]:
        name=scene["room"]; width,height=[v*26 for v in scene["size_cells"]]
        coverage=np.zeros((height,width),dtype=np.uint8)
        cells=np.zeros((height,width),dtype=bool)
        for a,b,c,d in scene["walkable_rectangles"]:
            cells[b*26:(d+1)*26,a*26:(c+1)*26]=True
        for a,b,c,d in scene["blocked_rectangles"]:
            cells[b*26:(d+1)*26,a*26:(c+1)*26]=False
        chunks={}
        assembled=Image.new("RGBA",(width,height))
        for chunk in scene["chunks"]:
            path=FOLDER/chunk["path"]
            check(sha(path)==chunk["sha256"],"chunk-sha-"+chunk["id"])
            image=Image.open(path).convert("RGBA"); pixels=np.asarray(image)
            check(image.size==(784,784),"fixed-native-core-plus-gutter-"+chunk["id"])
            x,y,w,h=[chunk[k] for k in ("x","y","width","height")]
            check(x%780==0 and y%780==0 and x+w<=width and y+h<=height,"chunk-native-alignment-"+chunk["id"])
            coverage[y:y+h,x:x+w]+=1
            alpha=pixels[2:2+h,2:2+w,3]
            check(np.all((alpha==0)|(alpha==255)),"no-soft-or-double-alpha-"+chunk["id"])
            if not scene["overlay"]:
                check(np.array_equal(alpha==255,cells[y:y+h,x:x+w]),"independent-geometric-floor-mask-"+chunk["id"])
            assembled.alpha_composite(image.crop((2,2,2+w,2+h)),(x,y))
            chunks[x,y]=pixels
        check(np.all(coverage==1),"every-pixel-drawn-once-no-gap-or-overlap-"+name)
        for (x,y),pixels in chunks.items():
            if (x+780,y) in chunks:
                check(np.array_equal(pixels[:,780:784],chunks[x+780,y][:,:4]),"identical-shared-horizontal-band-"+name+f"-{x}-{y}")
            if (x,y+780) in chunks:
                check(np.array_equal(pixels[780:784,:],chunks[x,y+780][:4,:]),"identical-shared-vertical-band-"+name+f"-{x}-{y}")
        if scene["overlay"]:
            check(scene["size_cells"]==[90,90] and len(chunks)==9,"real-90x90-native-surface-is-nine-images")
            for cx,cy in scene["native_doors"]:
                patch=np.asarray(assembled)[cy*26:(cy+1)*26,cx*26:(cx+1)*26,3]
                check(np.all(patch==255),f"opaque-doorstep-{cx}-{cy}")
        preview=ROOT/"artifacts/terrain-chunks-0327/scenes"/(name+"-ground.png")
        preview.parent.mkdir(parents=True,exist_ok=True); assembled.save(preview)
    report=dict(passed=True,checks=checks,count=len(checks),runtime_verified=False,
                manifest_sha256=sha(FOLDER/"manifest.json"),scope="actual chunk bytes, crop coverage, shared sampling bands, geometric masks and narrative plans; game runtime is separate")
    path=ROOT/"artifacts/terrain-chunks-0327/stitch-validation.json"
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(dict(passed=True,checks=len(checks),chunks=len(manifest["assets"]),story_nodes=54,native_world_size=2340,runtime_verified=False)))


if __name__=="__main__":
    main()
