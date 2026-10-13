"""Reproducible experimental sprite processing; no engine integration.
Built-in generation provides NEW structural artwork. These explicit strip remaps
further enlarge head mass / shorten legs, then pixel-level edits are logged.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, json, hashlib
D=Path(__file__).resolve().parent
im=Image.open(D/'hers_structural_concept_v1.png').convert('RGBA')
a=np.array(im); a[:,:,3]=np.where(a[:,:,3]>=128,255,0); a[a[:,:,3]==0,:3]=0
im=Image.fromarray(a)
# Same x interval throughout; contiguous anatomical strips, no duplicated rows.
strips=[((354,100,846,442),(20,16)),((354,442,846,650),(20,9)),((354,650,846,974),(20,9))]
out=Image.new('RGBA',(35,44)); y=4
for box,size in strips:
 out.alpha_composite(im.crop(box).resize(size,Image.Resampling.NEAREST),(8,y)); y+=size[1]
# Fixed muted palette, no noise/dither. Keep dark clothing distinct from hair/skin.
palette=['17151c','2d292e','443d40','5a5050','71645c','887a6e','a08e7b','c1aa8c','dfc4a0','754c37','956347','b68058','d79968','efb581','f7cd96','49372f','634634','846043','aca59a','d4c8ae']
rgb=np.array([tuple(bytes.fromhex(x)) for x in palette],dtype=np.int32)
def quant(q):
 a=np.array(q); mask=a[:,:,3]>=128; dist=((a[:,:,:3].astype(np.int32)[:,:,None,:]-rgb)**2).sum(3); a[:,:,:3]=rgb[dist.argmin(2)];a[:,:,3]=mask*255;a[~mask,:3]=0;return Image.fromarray(a)
out=quant(out);out.save(D/'hers_native_preedit.png')
# Explicit native-pixel cleanup. Coordinates are canvas-space; mutations tracked.
edits=[]
def px(x,y,h,reason):
 old=list(out.getpixel((x,y))); new=tuple(bytes.fromhex(h))+(255,) if h else (0,0,0,0)
 out.putpixel((x,y),new);edits.append(dict(x=x,y=y,before=old,after=list(new),reason=reason))
# Explicit eye/bridge separation after native sampling collapsed the brow shadows.
for x,y,c in [(14,12,'b68058'),(15,12,'b68058'),(18,12,'b68058'),(19,12,'b68058'),(20,12,'b68058'),(14,13,'17151c'),(15,13,'17151c'),(18,13,'17151c'),(19,13,'17151c'),(20,13,'b68058'),(14,14,'d79968'),(15,14,'d79968'),(16,14,'efb581'),(17,14,'f7cd96'),(18,14,'b68058'),(19,14,'d79968'),(14,15,'d79968'),(15,15,'d79968'),(16,15,'f7cd96'),(17,15,'efb581'),(18,15,'d79968'),(19,15,'d79968'),(16,16,'754c37'),(17,16,'754c37'),(18,16,'b68058')]: px(x,y,c,'Restore two eye clusters, a nose bridge and restrained mouth; no eye whites')
for x,y in [(14,6),(15,6),(17,6),(13,7),(14,7),(16,7),(18,7),(20,8),(21,9),(22,10),(21,11)]: px(x,y,'887a6e','Ash-grey hair cluster consolidation without copied native face')
for x,y,c in [(9,29,'efb581'),(10,29,'d79968'),(9,30,'b68058'),(10,30,'d79968'),(24,29,'efb581'),(25,29,'d79968'),(24,30,'d79968'),(25,30,'b68058')]: px(x,y,c,'Separate compact empty hand from dark sleeve')
for x,y,c in [(20,27,'aca59a'),(21,27,'aca59a'),(20,28,'aca59a'),(21,28,'17151c'),(22,28,'aca59a'),(21,29,'aca59a'),(21,30,'aca59a'),(20,31,'aca59a'),(21,31,'aca59a')]: px(x,y,c,'Ordinary key loop/stem on anatomical left hip; no weapon')
for x in [11,12,13,14,15,16]: px(x,37,'49372f','Fixed left boot sole baseline y37')
for x in [21,22,23,24,25]: px(x,37,'49372f','Fixed right boot sole baseline y37')
for x,y,c in [(12,35,'634634'),(13,35,'846043'),(14,35,'634634'),(12,36,'846043'),(13,36,'846043'),(14,36,'634634'),(15,36,'49372f'),(22,35,'634634'),(23,35,'846043'),(22,36,'846043'),(23,36,'634634'),(24,36,'634634')]: px(x,y,c,'Merge noisy boot pixels into two short readable feet')
out.save(D/'hers_native_v1.png')
# Book remains an independent closed object, never attached to Hers.
book=quant(im.crop((1038,727,1283,889)).resize((9,6),Image.Resampling.NEAREST));book.save(D/'ledger_native_v1.png')
for name in ['hers_native_preedit','hers_native_v1','ledger_native_v1']:
 q=Image.open(D/(name+'.png'));q.resize((q.width*8,q.height*8),Image.Resampling.NEAREST).save(D/(name+'_8x.png'))
(D/'pixel_edit_log.json').write_text(json.dumps(edits,indent=2)+'\n')
