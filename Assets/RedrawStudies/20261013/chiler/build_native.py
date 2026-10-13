#!/usr/bin/env python3
"""Non-destructive reconstruction. --out must be a new or existing output directory.
Source concept and references are read only. No runtime files touched.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, json, hashlib, argparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE);args=p.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
def save(im,name):im.save(out/name)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=HERE/'chiler_concept_v1.png'
a=np.array(Image.open(source).convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
# Dominant opaque figure; no inferred alpha bbox includes the generator's almost-transparent dust.
crop=(373,174,922,1079)
base=Image.new('RGBA',(35,44));base.alpha_composite(Image.fromarray(a).crop(crop).resize((21,34),Image.Resampling.NEAREST),(5,4));save(base,'native_base.png')
# Palette chosen by material, not generated universal templates. No dithering.
hexes=['251011','452523','623A2D','764733','895039', 'F9BD8E','F3786D','BE5960','76434C', 'D6922D','B87823','8B571D','68401D', '77704A','625D3B','4E4B32','383628', '9A5430','77422C','543024','342024']
palette=np.array([tuple(bytes.fromhex(s)) for s in hexes],dtype=np.int32)
b=np.array(base);vis=b[:,:,3]>0;rgb=b[:,:,:3].astype(np.int32);idx=np.argmin(((rgb[:,:,None,:]-palette[None,None,:,:])**2).sum(3),axis=2);b[vis,:3]=palette[idx[vis]]
quant=b.copy()
# Local silhouette/anatomy cleanup: make actual skin chin explicit at y20;
# no beard-tail measurement. Merge patchy jaw, close immediately onto collar.
edits=[(16,19,6,'left jaw skin'),(17,19,5,'chin skin continuous'),(18,19,5,'chin skin continuous'),(19,19,5,'right chin skin'),(17,20,6,'lower jaw skin'),(18,20,5,'visible chin skin'),(19,20,1,'right jaw border'),(17,21,1,'short stubble/collar boundary'),(18,21,1,'short stubble/collar boundary'),(15,20,1,'hair/left jaw edge')]
log=[]
for x,y,c,why in edits:
 old=b[y,x].tolist();new=palette[c].tolist()+[255];b[y,x]=new;log.append({'xy':[x,y],'before':old,'after':new,'reason':why})
im=Image.fromarray(b);save(im,'chiler_native_v1.png');save(im,'chiler_native_v1_1x.png');save(im.resize((280,352),Image.Resampling.NEAREST),'chiler_native_v1_8x.png')
# Auditable source row/column view.
zoom=20;sheet=Image.new('RGB',(760,950),(110,110,110));sheet.paste(im.resize((700,880),Image.Resampling.NEAREST),(40,35),im.resize((700,880),Image.Resampling.NEAREST));d=ImageDraw.Draw(sheet)
for y in range(44):d.text((4,35+y*20+4),str(y),fill='white')
for x in range(35):d.text((40+x*20,15),str(x),fill='white')
for y,color in [(4,'cyan'),(20,'lime'),(21,'yellow'),(37,'orange')]:d.line((30,35+y*20,745,35+y*20),fill=color,width=1)
save(sheet,'chiler_landmarks_20x.png')
refs=[('Gunda','s_peasantfemale_09_0.png'),('Bert','s_npc_merchant01_0.png')]
panels=[('Chiler new',im)]+[(n,Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals'/f).convert('RGBA')) for n,f in refs]
comparison=Image.new('RGB',(960,435),(115,115,115));d=ImageDraw.Draw(comparison)
for i,(name,pic) in enumerate(panels):
 x=i*320+20;d.text((x,10),name,fill='white');big=pic.resize((280,352),Image.Resampling.NEAREST);comparison.paste(big,(x,35),big)
 for y,col in [(4,'cyan'),(20,'lime'),(21,'yellow'),(37,'orange')]:d.line((x,35+y*8,x+280,35+y*8),fill=col)
 d.text((x,393),'top4 | chin20..21 | sole37',fill='white')
save(comparison,'comparison_landmarks_8x.png')
old=Image.open(ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch35/136_ald_chiler_buya_cast.png').crop((150,15,550,580));old.thumbnail((400,565),Image.Resampling.NEAREST)
review=Image.new('RGB',(1280,640),(100,100,100));d=ImageDraw.Draw(review);review.paste(old,(10,40));d.text((10,10),'OLD concept: gesture only, not native',fill='white')
for i,(name,pic) in enumerate(panels):
 x=420+i*285;big=pic.resize((280,352),Image.Resampling.NEAREST);review.paste(big,(x,130),big);d.text((x,95),name+' / 8x',fill='white')
save(review,'old_new_refs_comparison.png')
(out/'pixel_edits.json').write_text(json.dumps({'binary_alpha_threshold':128,'crop_source':crop,'sampling':'nearest to 21x34 at 5,4; no full-body horizontal fattening','palette':hexes,'quantization_changed_visible_pixels':int(np.any(quant!=np.array(base),axis=2).sum()),'local_changes':log},indent=2))
qa={'actor':'ALD-NPC-CHILER','candidate':'v1 study only','canvas':[35,44],'bbox':im.getbbox(),'crown_y':4,'visible_skin_chin_y':20,'dark_chin_collar_y':21,'sole_y':37,'head_height':17,'remainder':17,'boundary_tolerance':'skin-end 17/17; border-end18/16. Not beard tip.','head_core_x':[9,24],'cape_shoulders_x':[9,24],'neck':'no independent free neck row; y21 dark jaw meets collar','pose':'neutral standing; both hands closed/lowered; pointer diagonally down','identity':'mustard short cape, olive short tunic, brown satchel, brown tousled hair, small moustache and stubble','not_certified':['runtime','collision','other directions','animation','installed vanilla equivalence','final user visual approval'],'style_status':'candidate pending independent visual QA; palette count is not acceptance','alpha_values':np.unique(b[:,:,3]).tolist(),'opaque_colors':int(len(np.unique(b[vis,:3],axis=0)))}
(out/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
sources=[source,HERE/'prompt.txt',HERE/'style_reference_16x.png',ROOT/'Assets/ReferenceAudit/20261013/one_to_one_proportion_review.json',ROOT/'Assets/ReferenceAudit/20261013/character_redraw_triage_round2.json',ROOT/'design/04_人物/城市人物/人物_ALD-NPC-CHILER_齐勒.md',ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch35/136_ald_chiler_buya_cast.png']+[ROOT/'Assets/ReferenceAudit/20261013/originals'/f for _,f in refs]+[ROOT/'Assets/ReferenceAudit/20261013/originals/s_npc_carpenter_0.png']
manifest={'tool':'built-in image_gen.imagegen','prompt_file':'prompt.txt','generation_inputs':['style_reference_16x.png'],'identity_input':'old board viewed, identity supplied as text; old proportions not sent to image generator','source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sources},'outputs_sha256':{p.name:sha(p) for p in [out/n for n in ['native_base.png','chiler_native_v1.png','chiler_native_v1_1x.png','chiler_native_v1_8x.png','chiler_landmarks_20x.png','comparison_landmarks_8x.png','old_new_refs_comparison.png','pixel_edits.json','qa.json']]},'script_sha256':sha(__file__),'preserved':'old source unchanged; no Buya edit; no runtime/global/install/push; no extra direction'}
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(qa,ensure_ascii=False))
