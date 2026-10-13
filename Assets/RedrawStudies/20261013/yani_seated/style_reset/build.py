from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, json, hashlib
D=Path(__file__).resolve().parent
R=D.parents[4]
source=Image.open(D/'new_concept.png').convert('RGBA')
a=np.array(source); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); source=Image.fromarray(a)
crop=(269,158,874,1262)
q=source.crop(crop).resize((21,29),Image.Resampling.NEAREST)
a=np.array(q); opaque=a[:,:,3]>0
# Fixed 18-color material palette sampled/selected from the new source; no anatomy overpainting.
pal=np.array([[22,15,20],[48,30,29],[80,49,37],[110,74,51],[247,181,129],[199,128,99],[143,85,67],[120,109,101],[78,69,68],[104,92,88],[72,76,42],[106,114,63],[207,194,161],[76,65,65],[97,81,79],[164,105,43],[111,70,36],[69,43,31]],dtype=np.int32)
rgb=a[:,:,:3].astype(np.int32); ix=((rgb[:,:,None,:]-pal[None,None,:,:])**2).sum(3).argmin(2); a[:,:,:3]=pal[ix]; a[~opaque]=0
out=Image.new('RGBA',(35,44));out.alpha_composite(Image.fromarray(a),(7,9))
out.save(D/'native.png');out.resize((280,352),Image.Resampling.NEAREST).save(D/'native_8x.png')
items=[('Yani v2 / previous',D.parent/'v2/native.png'),('Yani / style reset',D/'native.png'),('Gunda / original',R/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png'),('Jurg / original',R/'Assets/ReferenceAudit/20261013/originals/s_npc_carpenter_0.png'),('Bert / original',R/'Assets/ReferenceAudit/20261013/originals/s_npc_merchant01_0.png')]
board=Image.new('RGB',(280*len(items),405),(75,75,79)); dr=ImageDraw.Draw(board)
for i,(name,p) in enumerate(items):
 im=Image.open(p).convert('RGBA'); im=im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST);board.paste(im,(i*280,30),im); dr.text((i*280+8,8),name,fill='white');dr.line((i*280,334,i*280+279,334),fill=(105,105,110))
board.save(D/'old_new_original_comparison_8x.png')
# Identity sheet: full legacy concept (identity only, not image generation input) and new concept.
legacy=Image.open(R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/02_yani_dialogue_poses.png').convert('RGBA').crop((40,100,560,830));new=source.crop(crop)
board=Image.new('RGB',(1100,720),(73,73,78));dr=ImageDraw.Draw(board)
for im,x in [(legacy,10),(new,570)]:
 im.thumbnail((520,670),Image.Resampling.NEAREST);board.paste(im,(x,40),im)
dr.text((10,10),'Legacy neutral seated / identity only',fill='white');dr.text((570,10),'New source / native style references only',fill='white');board.save(D/'source_identity_comparison.png')
check=Image.new('RGB',(560,352),(222,215,196));check.paste((60,57,63),(280,0,560,352));im=out.resize((280,352),Image.Resampling.NEAREST);check.paste(im,(0,0),im);check.paste(im,(280,0),im);check.save(D/'background_QA.png')
qa={'canvas':[35,44],'bbox':out.getbbox(),'alpha_values':sorted(set(out.getchannel('A').getdata())),'opaque_colors':len(set(px[:3] for px in out.getdata() if px[3])),'crop':crop,'sampling':[21,29],'offset':[7,9],'filter':'NEAREST','palette':pal.tolist(),'pixel_edits':[],'visual_status':'candidate_pending_independent_review','runtime_verified':False}
(D/'qa.json').write_text(json.dumps(qa,indent=2))
