"""Prepare a single scene-cue master, preserving approved regional palettes."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT/'src/Art/hd2d_26x26_20261013';P=PARENT/'batches/Scene-cues-20261014-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    for n in ['raw','images','animations','sheets','assets/items','assets/ui','notes','palettes','previews','exports']:(P/n).mkdir(parents=True,exist_ok=True)
    specs=[dict(id=k,size=z,origin=o,target_batch=t,role=r) for k,z,o,t,r in [
      ('r01_ash_threshold',[104,52],[52,43],'R01-camp-canal-v2','floor_decal_no_collision_no_ghost'),
      ('r01_tool_stub',[78,52],[39,43],'R01-camp-canal-v2','independent_observation_prop_not_certified_evidence'),
      ('r02_well_notice',[52,78],[26,65],'R02-river-v2','independent_observation_prop_not_pollution_verdict'),
      ('r02_red_water_buckets',[78,78],[39,65],'R02-river-v2','two_buckets_one_sprite_not_inventory'),
      ('r02_rope_shoe_stall',[156,156],[78,140],'R02-river-v2','conditional_N18_return_visit_off_by_default'),
      ('r02_bridge_note',[52,52],[26,43],'R02-river-v2','conditional_SQ04_refusal_return_visit_off_by_default')]]
    palettes={}
    for key,rel in [('BRY-R01-128','batches/R01-camp-canal-v1/palettes/bry_r01_128.json'),('DEN-R02-128','batches/R02-river-v1/palettes/den_r02_128.json')]:palettes[key]=json.loads((PARENT/rel).read_text(encoding='utf-8'))['colors']
    colors=list(dict.fromkeys(c for p in palettes.values() for c in p));write('palettes/shared.json',dict(name='SCENE-CUES-SHARED',colors=colors,regional_palettes=palettes,note='Approved128colors per regional sprite; combined master uses their union, no new colors'))
    sources=['design/05_主线/台本/台本_N2_灰堤没有墓碑.md','design/05_主线/台本/台本_N5_渡口的三种说法.md','design/05_主线/台本/台本_N9_把证据摆上桌.md','design/05_主线/台本/台本_N18_誓约之后.md','design/06_支线/台本/台本_SQ04_一条不卖人的路.md']
    write('brief.json',dict(batch='Scene-cues-20261014-v1',sprites=specs,source_sha256={n:sha(ROOT/n) for n in sources},inventory_requests={},scope='Missing scene observations only; no NPC work',runtime_verified=False))
    lock='# Execution Lock — Scene Cue Synchronization\n\n## authorization\nUser continues scene work2026-10-14. Approved26-cell static HD2D and128colors per regional sprite continue. Shared master combines only existing BRY/DEN palettes.\n\n## canvas\n- base_size:26x26\n- format:RGBA PNG\n- cue_master:1536x1024, six512x512slots\n'
    for s in specs:lock+=f"- {s['id']}: {s['size'][0]}x{s['size'][1]}, origin {s['origin']}\n"
    lock+='\n## palette\n- name:SCENE-CUES-SHARED\n- colors:\n'+''.join('  - '+c+'\n' for c in colors)
    lock+='\n## style\n- sub_style:textured HD-2D, square-grid orthographic oblique\n- light_direction:top-left\n- lighting:static unlit base\n\n## per_sprite_budget\n- max_colors:128\n\n## invariants\n- Six separate complete silhouettes, genuine transparency, no people/children/NPCs/ghosts, no readable writing or baked conclusions.\n- Red water bucket pair represents exactly TWO buckets; no drinkability/cure/crime verdict.\n- Rope shoes: pair of small half-woven sandals hanging on a modest rope-work stall, no owner drawn; conditional/off by default.\n- Bridge note: blank paper with visible nail, no new sign post; overlays existing sign only at the specified refusal return visit, never commits or clears harm.\n- Ash mark is ordinary threshold ash, not a magical rune or undead effect. Stub/agency seal only a trace, not completed certification.\n- Raw immutable; documented crop,NN resize,exact regional palette and binary-alpha production postprocessing approved.\n'
    (P/'spec_lock.md').write_text(lock,encoding='utf-8')
    heads=['I. Project Information','II. Canvas Specification','III. Color Palette','IV. Art Style Definition','V. Asset List','VI. Animation Specification','VII. Technical Constraints','VIII. Platform Export Notes'];vals=['R01/R02台本新增观察道具同步。','六格母图1536×1024，各生产尺寸见lock。','既有BRY/DEN区域128色，无新增颜色。','延续静态正交斜俯视HD2D。','灰圈、借据、井牌、双红桶、半绳鞋摊、桥头字条。','单帧。','两项有条件道具默认关闭；不画人物，不认证事实。','各区域v2保留v1原稿与包，几何不变，原生装配待测。']
    (P/'design_spec.md').write_text('# Purple Crystal Scene Cue Sync\n\n'+'\n\n'.join('## '+a+'\n\n'+b for a,b in zip(heads,vals))+'\n',encoding='utf-8')
    print(json.dumps(dict(sprites=len(specs),master_palette_colors=len(colors)),ensure_ascii=False))
if __name__=='__main__':main()
