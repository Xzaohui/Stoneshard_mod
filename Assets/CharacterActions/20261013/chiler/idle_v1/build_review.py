from PIL import Image, ImageDraw
from pathlib import Path
import json,hashlib,shutil
p=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler/idle_v1')
im=Image.open(p/'originals/I1_raw_imagegen.png').convert('RGBA'); raw_size=im.size;im.putalpha(im.getchannel('A').point(lambda x:0 if x<16 else x));im=im.resize((1536,1536),Image.Resampling.NEAREST);im.save(p/'frames/I1_inhale.png');shutil.copy2(p/'frames/I0_still.png',p/'frames/I2_return_reuse_I0.png')
files=['I0_still.png','I1_inhale.png','I2_return_reuse_I0.png']; sheet=Image.new('RGB',(1536,570),(35,39,43));d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 fr=Image.open(p/'frames'/f);small=fr.resize((512,512),Image.Resampling.NEAREST);sheet.paste(small,(i*512,42),small);d.line((i*512,502,i*512+511,502),fill=(57,105,115));d.line((i*512+256,490,i*512+256,514),fill=(190,164,69));d.text((i*512+15,12),['I0  REST','I1  INHALE / IMAGEGEN','I2  RETURN / REUSE I0'][i],fill=(245,237,214))
sheet.save(p/'chiler_idle_keyframes_review.png')
seq=[]
for f in files:
 fr=Image.open(p/'frames'/f);bg=Image.new('RGBA',fr.size,(35,39,43,255));bg.alpha_composite(fr);seq.append(bg.convert('RGB').resize((768,768),Image.Resampling.NEAREST))
seq[0].save(p/'chiler_idle_preview_no_interpolation.gif',save_all=True,append_images=seq[1:],duration=[650,650,650],loop=0)
manifest={'asset_id':'ALD-NPC-CHILER_IDLE_CONCEPT_V1','logical_canvas':[1536,1536],'foot_anchor':[768,1380],'engine_origin':None,'runtime_verified':False,'equipment_compatibility_verified':False,'native_frame_count':None,'native_timing':None,'view':'single three-quarter screen-right concept','source':'../../../CharacterDesigns/20261013/expressive/chiler/chiler_raw_imagegen.png','generated_raw_size':raw_size,'processing':{'I0':'original translated (109,176); alpha<16 removed; no scale','I1':'built-in imagegen returned 1254 square; nearest-neighbor canvas normalization to1536; alpha<16 removed; no local warp','I2':'exact file reuse of I0'},'preview':'3 logical frames, 2 unique images; 650ms each for inspection only; NO interpolation; NO synthetic translation','frames':[],'limitations':['original artistic breathing proposal, not traced native frames','flattened full-body PNGs, not editable equipment layers','source and regenerated pixels have fine gradients; not native pixel-grid validated','cross-frame exact pixel identity not guaranteed; review required']}
for i,f in enumerate(files):
 fp=p/'frames'/f;manifest['frames'].append({'id':f[:2],'path':'frames/'+f,'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'reuse_of':'I0' if i==2 else None,'attachments_review_coordinates':{'head_center':[790,545],'anatomical_right_hand_pointer_grip':[549,1050],'anatomical_left_hand':[966,1080],'back_strap_attachment':[690,850]},'attachment_status':'manual approximate review markers, not runtime sockets'})
(p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
