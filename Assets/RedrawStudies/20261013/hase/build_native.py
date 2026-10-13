"""Reproduce Hase study: generated structural concept -> nonuniform head/body mapping -> explicit pixel cluster edits. Not engine-ready."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import numpy as np,json,hashlib
p=Path(__file__).parent
src=Image.open(p/'concept_v1_unapproved.png').convert('RGBA').crop((240,198,912,1242))
canvas=Image.new('RGBA',(35,44))
canvas.paste(src.crop((0,0,672,464)).resize((22,17),Image.Resampling.NEAREST),(7,4))
canvas.paste(src.crop((0,464,672,1044)).resize((22,17),Image.Resampling.NEAREST),(7,21))
# Threshold before palette mapping removes generated low-alpha halo, without extrapolating body bounds.
base=json.loads((p/'base_grid.json').read_text());pal=base['palette'];keys=list(pal)[1:];cols=np.array([tuple(bytes.fromhex(pal[k]))[:3] for k in keys],float)
a=np.array(canvas);grid=[]
for row in a:grid.append(['.' if v[3]<128 else keys[np.argmin(np.sum((cols-v[:3])**2,axis=1))] for v in row])
log=[]
def run(y,x,s,reason):
 for i,k in enumerate(s):
  old=grid[y][x+i]
  if old!=k:log.append({'x':x+i,'y':y,'from':old,'to':k,'reason':reason});grid[y][x+i]=k
# Clean broad hair mass, retaining authored asymmetry and crown silhouette.
for y,x,s in [(6,14,'hhHHHHHh'),(7,13,'hHHHHHhhHh'),(8,12,'hHHHhhHhhHh'),(9,12,'hHHhHHHhhHh'),(10,13,'hhhHHhjpHh')]:run(y,x,s,'coherent dark-hair crown, remove sampled speckle')
# Explicit eye/brow/nose/jaw. Anatomical chin concealed by short beard: estimated y19-20; beard ends y22.
for y,x,s in [(12,16,'pPPPPps'),(13,16,'hHpphHs'),(14,16,'PXpPPXs'),(15,16,'ppPPPPs'),(16,16,'pSPPPps'),(17,15,'hspHHhs'),(18,15,'hHhppHh'),(19,15,'hHHHhhh'),(20,15,'XhHHhhX'),(21,16,'XhHhhX'),(22,17,'oXXo')]:run(y,x,s,'readable eyes and broad adult face; compact short beard separate from inferred chin')
# Cloth and strap: no layered lapels or suit waistcoat, no long neck.
for y,x,s in [(21,12,'HHXB'),(22,11,'OOXBB'),(22,21,'OOX'),(23,10,'OOgOBBXoOOOOX'),(24,10,'OgOOOBBXOOOOX'),(25,9,'OOgOOOOBBXOOOX'),(26,9,'OOOOOOOOBBXOOX'),(27,9,'OOXXOOOOOBBXXX'),(28,12,'XOOOOOOOBBX'),(29,18,'BXOOOOX'),(30,18,'BXOOOOX'),(31,18,'BXOOgOX'),(32,18,'XOOOgOO'),(33,13,'XXXXXXXXXX')]:run(y,x,s,'merge olive cloth into material clusters and brown diagonal strap')
# Bag sits in front of the garment, with one simple flap and clasp.
for y,x,s in [(29,12,'XBBBBBX'),(30,12,'XBlllBX'),(31,12,'XBBLBBX'),(32,12,'XBBBBBX')]:run(y,x,s,'single satchel flap and small clasp, no tiny pocket/strap hardware')
# One bottle: closed cap, narrow neck, amber/label body; skin hold is distinct.
for y,x,s in [(23,25,'.XtX.'),(24,25,'.XaX.'),(25,25,'XaAcX'),(26,25,'XaAcS'),(27,25,'XXXpS'),(28,25,'XSpSX'),(29,25,'.XXX.')]:run(y,x,s,'closed bottle and separate skin mitten, no individual fingers')
# Keep short legs and separated boot masses.
for y,x,s in [(34,12,'XHHX'),(34,19,'XHHX'),(35,12,'XhhX'),(35,19,'XbhX'),(36,11,'XbBX'),(36,19,'XbBBX'),(37,11,'XbbX'),(37,19,'XXbbX')]:run(y,x,s,'short pants and two compact separated boots')
# Inspection corrections: sampled olive specks in hair and isolated skin near bottle.
for y,x,ss in [(11,15,'h'),(12,11,'h'),(15,14,'h'),(16,13,'h'),(20,14,'h'),(26,23,'OO'),(27,23,'OO')]:run(y,x,ss,'actual visual QA: remove material contamination and reconnect sleeve before hand')
arr=np.array([[tuple(bytes.fromhex(pal[k])) for k in row] for row in grid],np.uint8);im=Image.fromarray(arr,'RGBA');im.save(p/'hase_native_v1.png');im.resize((280,352),Image.Resampling.NEAREST).save(p/'hase_native_v1_8x.png');im.resize((560,704),Image.Resampling.NEAREST).save(p/'hase_native_v1_16x.png')
(p/'pixel_edits.json').write_text(json.dumps({'coordinates':'zero based x/y native canvas','preprocess':{'source_crop':[240,198,912,1242],'head_source_split_absolute_y':662,'head_target_rows':[4,20],'body_target_rows':[21,37],'resize':'nearest neighbor','alpha_threshold':127,'palette_mapping':'nearest Euclidean RGB to declared palette'},'palette':pal,'edits':log,'final_rows':[''.join(r) for r in grid]},ensure_ascii=False,indent=2)+'\n')
print('native bbox',im.getbbox(),'edits',len(log),'opaque_colors',len(np.unique(arr[arr[:,:,3]>0,:3],axis=0)))
