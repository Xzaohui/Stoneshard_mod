from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent;R=D.parents[3]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch32/124_hers_white_debt_controller_cast.png'
ref=R/'Assets/ReferenceAudit/20261013/originals'
items=[('OLD 124 (normalized only)',Image.open(old).crop((89,47,403,634)).resize((18,34),Image.Resampling.NEAREST)),('Hers v1',Image.open(D/'hers_native_v1.png')),('Frid',Image.open(ref/'s_npc_herbalist_0.png')),('Bert',Image.open(ref/'s_npc_merchant01_0.png')),('Jurg',Image.open(ref/'s_npc_carpenter_0.png'))]
board=Image.new('RGB',(1300,470),(113,117,119));draw=ImageDraw.Draw(board)
for i,(name,im) in enumerate(items):
 x=i*260;draw.text((x+7,6),name,fill='white')
 if i==0:
  canv=Image.new('RGBA',(35,44));canv.paste(im,(8,4));im=canv
 im=im.convert('RGBA');board.paste(im,(x+110,30),im)
 big=im.resize((280,352),Image.Resampling.NEAREST);board.paste(big,(x-10,96),big)
 draw.line((x,400,x+259,400),fill=(150,153,155))
board.save(D/'comparison_native_and_8x.png')
# Native ledger against light and dark: no scene, movement or carrying implied.
im=Image.open(D/'ledger_native_v1.png');b=Image.new('RGB',(280,112),(110,110,110));dr=ImageDraw.Draw(b);dr.text((5,5),'Closed ledger / separate study',fill='white');b.paste(im,(12,35),im);big=im.resize((72,48),Image.Resampling.NEAREST);b.paste(big,(65,33),big);b.save(D/'ledger_comparison.png')
sources=['design/04_人物/人物_赫斯·白.md','design/04_人物/城市人物/人物_NPC-HERS_赫斯·白.md','design/05_主线/台本/台本_N17_残光之井.md','src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch32/manifest.json','src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch66/hers_prompt.txt','Assets/ReferenceAudit/20261013/character_redraw_triage.json','Assets/ReferenceAudit/20261013/character_landmark_appendix.json','Assets/ReferenceAudit/20261013/original-reference-metadata.json',str(old.relative_to(R))]+[str((ref/p).relative_to(R)) for p in ['s_npc_herbalist_0.png','s_npc_merchant01_0.png','s_npc_carpenter_0.png']]
manifest={'date':'2026-10-13','identity':'NPC10 / Hers White / 赫斯·白','status':'experimental structural redraw; not engine ready','generation':{'tool':'built-in image_gen','intent':'new structural redraw from appearance + native style reference','prompt_file':'prompt.txt','generated_original':'/workspace/scratch/5ed8df2c5d81/generated_images/exec-5c02e964-2af8-4cd6-88f3-6e27c7d3edbb.png','references':[str(old.relative_to(R)),'Assets/ReferenceAudit/20261013/character_native_refs_contact.png']},'sources':{s:sha(R/s) for s in sources},'narrative_scope':'Single neutral empty-handed pose. Ledger separately isolated; no carrying, retreat or escape event. No N17 state change. Appearance remains original proposal.','processing':'build_hers_study.py: alpha>=128, new generated strips into head16/torso9/lower9, fixed20-color palette, nearest-neighbor and no dithering; explicit logged face/hand/key/boot pixels. Not old art shrink.','runtimeVerified':False,'style_pass':False,'engine_standard_claim':False,'files':{p.name:sha(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in ['manifest.json','QA.json']}}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
q=Image.open(D/'hers_native_v1.png');a=np.array(q); colors=np.unique(a[a[:,:,3]>0,:3],axis=0);ed=json.loads((D/'pixel_edit_log.json').read_text());qa={'canvas':list(q.size),'alpha_bbox_half_open':q.getbbox(),'visible_size':[q.getbbox()[2]-q.getbbox()[0],q.getbbox()[3]-q.getbbox()[1]],'opaque_colors':len(colors),'palette_budget':20,'alpha_values':np.unique(a[:,:,3]).tolist(),'sole_y':int(np.where(a[:,:,3]>0)[0].max()),'feet_have_gap_on_sole':all(a[37,x,3]==0 for x in range(17,21)),'manual_pixel_operations':len(ed),'head_visual_rows':[4,19],'waist_rows':[26,28],'below_waist_rows':[29,37],'ledger_canvas':list(im.size),'source_integrity':all(sha(R/p)==h for p,h in manifest['sources'].items()),'native_grid_verified':True,'visual_style_and_runtime_pass':False,'limits':['35x44 experimental canvas; visible size not engine standard.','Head mass includes hair/short stubble; anatomical landmark estimate overlaps collar.','Imagegen concept still adds modern-looking lapel angles and texture; native cleanup reduces but does not fully eliminate them.','1x face conveys brow/eye and warm nose cluster, not precise individual likeness. Key at native size is symbolic.','Community native references not verified individually against local vanilla.','No animation, collision, anchor metadata or runtime validation.']}
(D/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa,ensure_ascii=False,indent=2))
