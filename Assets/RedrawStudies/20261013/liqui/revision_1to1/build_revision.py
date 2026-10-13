from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
palette=json.loads((P/'pixel_edit_log.json').read_text())['palette'];pal=np.array([tuple(bytes.fromhex(c)) for c in palette])
a=np.array(Image.open(P/'liqui_structure_concept_v2.png').convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>128,255,0);src=Image.fromarray(a)
# Re-sample HIGH RES regenerated concept in anatomical sections, never stretch the old 13-row native head.
# Concept forehead/chin boundary inspected at y644; braid is not used to define chin.
head=src.crop((215,124,902,644)).resize((20,17),Image.Resampling.NEAREST)
body=src.crop((215,644,902,1354)).resize((20,17),Image.Resampling.NEAREST)
im=Image.new('RGBA',(35,44));im.paste(head,(8,4));im.paste(body,(8,21));b=np.array(im)
id=((b[:,:,:3,None].astype(int)-pal.T[None,None,:,:])**2).sum(2).argmin(2);b[:,:,:3]=pal[id];b[b[:,:,3]==0,:3]=0;im=Image.fromarray(b);im.save(D/'segmented_before_edits.png')
log=[]
def row(x,y,s,reason):
 for j,c in enumerate(s):
  if c=='_':continue
  p=(x+j,y);old=im.getpixel(p);new=tuple(bytes.fromhex(palette[int(c,18)]))+(255,) if c!='.' else (0,0,0,0)
  if old!=new:im.putpixel(p,new);log.append({'x':p[0],'y':p[1],'before':old,'after':new,'reason':reason})
# Mature adult face rebuilt on the newly sampled 17-row head, not stretched v2.
row(13,11,'266666632','Broad forehead with auburn edge')
row(13,12,'256666632','Merge forehead into coherent light plane')
row(13,13,'233663322','Small adult brow clusters')
row(13,14,'650665052','Two one-pixel eyes, no anime white islands')
row(13,15,'566566652','Broad cheek plane around one nose shadow')
row(13,16,'566756652','Angular nose shade; preserve warm adult skin')
row(13,17,'556665552','Coherent lower cheeks without mottled highlight')
row(13,18,'255335522','Small closed mouth, no exaggerated smile')
row(13,19,'025555220','Four-pixel skin lower jaw, actual head not braid')
row(13,20,'002575288','Three-pixel visible chin at y20, side jaw border distinct from collar')
row(14,21,'89079899','Single neck pixel at y21 nested between green collar')
row(14,22,'880BC89E','Close old long-neck wedge; strap starts on left shoulder')
# Preserve one closed satchel and clear belt/strap/hand separation from v2.
row(15,23,'CCCC1E089','Ochre chest with one stepped strap')
row(15,24,'CCCB1E899','Strap boundary from chest')
row(15,25,'CCB1E1C99','Diagonal strap one pixel at x19')
row(15,26,'BB1E1CB99','Diagonal strap crosses upper waist at x18')
row(15,27,'111E11G99','Dark belt behind strap; no bright gray buckle mass')
row(15,28,'11E1CCB99','Strap exits belt toward closed bag')
row(12,28,'4FEE2','One closed satchel flap')
row(12,29,'E44E2','Broad closed flap plane')
row(12,30,'E12E2','Closed clasp, not open contents')
row(12,31,'12221','Closed bag base')
row(9,29,'650','Left empty palm with dark separator from bag')
row(9,30,'700','Left palm/thumb shadow and separator')
row(25,29,'650','Right empty palm')
row(25,30,'700','Right empty hand shadow')
row(13,36,'D4D20','Short left boot readable toe')
row(13,37,'2211.','Left outsole')
row(20,36,'1D4D2','Short right boot readable toe')
row(20,37,'12221','Right outsole')
im.save(D/'liqui_native_1to1.png');im.resize((280,352),Image.Resampling.NEAREST).save(D/'liqui_native_1to1_8x.png')
(D/'pixel_edit_log.json').write_text(json.dumps({'method':'high-resolution concept separately sampled head17/body17 followed by explicit pixels','head_source_box':[215,124,902,644],'body_source_box':[215,644,902,1354],'head_target_box':[8,4,28,21],'body_target_box':[8,21,28,38],'palette':palette,'edits':log},ensure_ascii=False,indent=2))
print('bbox',im.getbbox(),'edits',len(log))
