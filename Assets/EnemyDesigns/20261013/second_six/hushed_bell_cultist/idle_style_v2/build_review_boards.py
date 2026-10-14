from PIL import Image
from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');d=R/'Assets/EnemyDesigns/20261013/second_six/hushed_bell_cultist/idle_style_v2';old=d.parent/'idle_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();slug='hushed_bell_cultist'
raw=Path('/workspace/scratch/5ed8df2c5d81/generated_images/exec-0394a25b-0644-4482-b7b2-8ac227bd7d2c.png');shutil.copy2(raw,d/f'{slug}_style_v2_raw_imagegen.png')
im=Image.open(raw).convert('RGBA');px=list(im.getdata());clean=[(0,0,0,0) if a<=8 else (r,g,b,a) for r,g,b,a in px];cl=Image.new('RGBA',im.size);cl.putdata(clean);cl.save(d/f'{slug}_style_v2_transparent.png')
for kind,color in [('light',(238,231,216,255)),('dark',(29,34,40,255))]:
 board=Image.new('RGBA',im.size,color);board.alpha_composite(cl);board.convert('RGB').save(d/f'{slug}_style_v2_review_{kind}.png')
thumb=cl.crop(cl.getbbox());thumb.thumbnail((240,300),Image.Resampling.NEAREST);board=Image.new('RGBA',(600,340),(238,231,216,255));board.paste(Image.new('RGBA',(300,340),(29,34,40,255)),(300,0))
for x in [0,300]:board.alpha_composite(thumb,(x+(300-thumb.width)//2,(340-thumb.height)//2))
board.convert('RGB').save(d/'reduced_readability.png')
refs=[old/'hushed_bell_cultist_idle_transparent.png',R/'Assets/EnemyDesigns/20261013/second_six/border_roundshield_rebel/idle_v1/border_roundshield_rebel_idle_transparent.png',R/'Assets/CharacterDesigns/20261013/expressive/mia/ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png']
snapshot={'concept_id':'EAO-CONCEPT-ENEMY-012','revision':'sole_style_hard_error_revision','authorization':'Root rejected naturalistic tall v1 after six-character overview and explicitly requested one builtin style/proportion edit.','input_images':[{'path':str(p.relative_to(R)),'sha256':sha(p),'role':'edit_target' if i==0 else 'style_proportion_reference','actually_viewed':True} for i,p in enumerate(refs)],'history_preserved':{'idle_v1_manifest_sha256':sha(old/'manifest.json'),'idle_v1_FINAL_STATUS_sha256':sha(old/'FINAL_STATUS.json'),'idle_v1_QA_sha256':sha(old/'QA_INDEPENDENT.json')},'constraints':'011 unchanged; v1 unchanged; no third generation; no script body drawing/stretching.','proportion_note':'Prompt asked head:remaining body approximately 1:1.5; actual output must be visually assessed and not claimed to match by prompt alone.'}
(d/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
call={'tool':'builtin image_gen.imagegen','prompt_file':'prompt_v2.txt','prompt_sha256':sha(d/'prompt_v2.txt'),'referenced_image_paths':[str(p) for p in refs],'transparent_background':True,'returned_saved_path':str(raw),'raw_sha256':sha(raw),'concept_total_generation_calls':2,'hard_error_revisions_used':1,'revision_cap':1}
(d/'generation_call.json').write_text(json.dumps(call,ensure_ascii=False,indent=2)+'\n')
audit={'mode':im.mode,'size':im.size,'alpha_extrema':im.getchannel('A').getextrema(),'cleaning':'Only alpha<=8 cleared and hidden RGB zeroed. No visible RGB changes, no body drawing, no stretching.','all_alpha_above_8_preserved':all(p==q for p,q in zip(px,clean) if p[3]>8),'zero_alpha_pixels':sum(p[3]==0 for p in clean),'bbox':cl.getbbox(),'review_layout':'Full size shallow/deep backgrounds and nearest aspect-preserving reduced preview.'}
(d/'alpha_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(d/'authorQA.md').write_text('# 012唯一风格硬错修订作者QA\n\n已明确重绘为大像素簇、短身大头成年男性，旧低帽/露脸/膝袍/绳肩带/腰带/手铃身份保留。成人清晰鼻口、严肃侧听表情、无幼儿脸。木柄单拳到钟肩连续，小铃舌可见；两臂两手两腿两靴完整。\n\n比例比v1显著紧凑，但并未严格达到prompt所求头:余身1:1.5；不可把文字要求当实际测量。须交root与独审按Mia/007并排实看，未经共同确认不selected。已经用完唯一修订，无第三抽图。\n\n脚本仅alpha<=8/隐藏RGB清理和等比nearest预览，未拉伸身体；旧稿和011未改。\n')
shutil.copy2('/tmp/build_bell_v2.py',d/'build_review_boards.py')
files={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in d.iterdir() if p.is_file()}
(d/'manifest.json').write_text(json.dumps({'status':'frozen_candidate_pending_root_and_independent_style_review','selected':False,'delivered':False,'concept_total_calls':2,'hard_error_revisions_used':1,'hard_error_revision_cap':1,'runtimeIntegrated':False,'runtimeVerified':False,'files':files},ensure_ascii=False,indent=2)+'\n')
print(str(d));print('transparent_sha',sha(d/f'{slug}_style_v2_transparent.png'))
