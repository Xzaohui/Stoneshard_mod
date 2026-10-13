from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
p=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler/walk_v1')
im=Image.open(p/'frames/W1_swing_unregistered.png');out=Image.new('RGBA',(1536,1536));out.alpha_composite(im,(-78,-16));out.save(p/'frames/W1_swing.png')
files=['W0_support.png','W1_swing.png','W2_contact.png'];sheet=Image.new('RGB',(1536,570),(35,39,43));d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
 im=Image.open(p/'frames'/f);c=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(c,(i*512,42),c);d.line((i*512,502,i*512+511,502),fill=(57,105,115));d.line((i*512+256,490,i*512+256,514),fill=(190,164,69));d.text((i*512+15,12),['W0  SUPPORT / SOURCE','W1  SWING / ORIGINAL POSE','W2  CONTACT / ORIGINAL POSE'][i],fill=(245,237,214))
sheet.save(p/'chiler_walk_keyframes_review.png')
seq=[]
for f in files:
 im=Image.open(p/'frames'/f);bg=Image.new('RGBA',im.size,(35,39,43,255));bg.alpha_composite(im);seq.append(bg.convert('RGB').resize((768,768),Image.Resampling.NEAREST))
# Play once. Not a closed loop or full alternating gait.
seq[0].save(p/'chiler_short_step_preview_once.gif',save_all=True,append_images=seq[1:],duration=[650,650,1500])
m={'asset_id':'ALD-NPC-CHILER_SHORT_STEP_CONCEPT_V1','logical_canvas':[1536,1536],'ground_reference':[768,1380],'ground_reference_meaning':'working registration point; perspective boot soles may differ in y','native_fps':None,'native_directions':None,'engine_origin':None,'collision':None,'runtime_verified':False,'equipment_compatibility_verified':False,'animation_status':'one original partial step; not full walk cycle; contact does not reset to source','source_keyframe':'W0 reused from idle I0','original_generation_count':2,'preview':'three actual keyed images, no interpolation, no synthetic slide; one-shot inspection playback','registration':'All generated square canvases normalized to1536 using nearest-neighbor. W1 translated(-78,-16) after normalization to restore planted screen-left sole contact from imagegen drift; no local warping. W2 no per-bbox centering.','identity_handedness':'same screen-left source hand holds pointer; anatomical hand naming tentative, skeleton not verified','frames':[]}
for i,f in enumerate(files):
 m['frames'].append({'id':f[:2],'path':'frames/'+f,'sha256':hashlib.sha256((p/'frames'/f).read_bytes()).hexdigest(),'phase':['stable two-foot support','screen-left foot planted, screen-right boot swings clear','screen-right leading foot contacts, rear heel lifts'][i],'root_delta_estimate':[[0,0],[-20,-16],[50,5]][i],'marker_status':'manual coarse review estimates, not runtime sockets','head':[ [790,545],[770,529],[840,550] ][i],'pointer_grip':[[549,1050],[512,1044],[588,1057]][i],'pointer_tip':[[378,1252],[310,1257],[400,1255]][i],'bag_attachment':[[848,1000],[834,987],[901,1000]][i]})
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
