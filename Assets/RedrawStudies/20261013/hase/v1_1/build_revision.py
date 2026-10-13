from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json
p=Path(__file__).parent;base=p.parent
def sha(x):return hashlib.sha256(x.read_bytes()).hexdigest()
src=base/'hase_native_v1.png';oldsha=sha(src);assert oldsha=='fd63e1183f5ff81a5335e6b5ee666d20ac89cc68af8fda191d1be5e865ba9394'
im=Image.open(src).convert('RGBA');before=im.getpixel((18,11));after=(242,161,123,255);assert before==(48,48,33,255)
im.putpixel((18,11),after);im.save(p/'hase_native_v1_1.png')
for k in [8,16]:im.resize((35*k,44*k),Image.Resampling.NEAREST).save(p/f'hase_native_v1_1_{k}x.png')
# Deterministic update of the native pixel region in existing annotated comparison; all other figures and annotations remain unchanged.
c=Image.open(base/'hase_old_native_originals_comparison.png');d=ImageDraw.Draw(c);d.rectangle((15+18*8,80+11*8,15+19*8-1,80+12*8-1),fill=after[:3]);c.save(p/'hase_old_native_originals_comparison_v1_1.png')
c=Image.open(base/'hase_native_landmarks_20x.png');d=ImageDraw.Draw(c);d.rectangle((55+18*20,40+11*20,55+19*20-1,40+12*20-1),fill=after[:3]);c.save(p/'hase_native_landmarks_v1_1_20x.png')
a=np.array(im);b=np.array(Image.open(src));coords=np.argwhere(np.any(a!=b,axis=2)).tolist();assert coords==[[11,18]];assert sha(src)==oldsha
m={'character':'BRY-NPC-HASE','revision':'v1_1','scope':'one-pixel forehead material correction only','source':{'path':'../hase_native_v1.png','sha256':oldsha},'edit':{'x':18,'y':11,'before_rgba':before,'after_rgba':after,'reason':'Independent QA found isolated olive cloth palette pixel inside forehead. Replace with adjacent warm skin midtone shared by x17,y11 and x21,y11; darker than forehead highlight, appropriate to hairline edge.'},'validation':{'changed_native_pixels':1,'changed_yx':coords,'old_v1_unchanged':True,'canvas':[35,44],'bbox_exclusive':list(im.getbbox()),'alpha_unchanged':bool(np.array_equal(a[:,:,3],b[:,:,3])),'proportions_direction_and_other_pixels_unchanged':True},'landmarks':{'crown':4,'inferred_chin':[19,20],'beard_end':22,'sole':37},'limitations':['Front-biased simplified face differs from original three-quarter view; retained as aesthetic limitation, not corrected in this one-pixel revision.','Anatomical chin under beard remains inferred.','No style/production/runtime acceptance.'],'outputs':[{'path':z.name,'sha256':sha(z)} for z in sorted(p.glob('*.png'))]}
(p/'revision_manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(m,ensure_ascii=False))
