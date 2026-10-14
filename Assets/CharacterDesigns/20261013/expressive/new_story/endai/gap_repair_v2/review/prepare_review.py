from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,base64
p=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive/new_story/endai/gap_repair_v2')
im=Image.open(p/'raw/E2_initial.png').convert('RGBA'); a=np.array(im); b=a.copy(); b[b[:,:,3]<=8]=0
out=p/'selected/endai_E2_no_order_no_entry_transparent.png'; Image.fromarray(b).save(out)
for name,col in [('light',(232,225,211,255)),('dark',(30,34,43,255))]:
 board=Image.new('RGBA',(1024,800),col)
 for i,f in enumerate([p/'sources/mother.png',out]):
  x=Image.open(f).convert('RGBA').resize((512,768),Image.Resampling.NEAREST);board.alpha_composite(x,(i*512,32))
 ImageDraw.Draw(board).text((10,10),'MOTHER                                               E2 GAP REPAIR',fill=(128,128,128,255));board.convert('RGB').save(p/f'review/endai_mother_E2_{name}.png')
print(json.dumps({'size':im.size,'mode':im.mode,'visible_unchanged':bool(np.array_equal(a[a[:,:,3]>8],b[a[:,:,3]>8])),'alpha_le8':int((a[:,:,3]<=8).sum()),'raw_sha':hashlib.sha256((p/'raw/E2_initial.png').read_bytes()).hexdigest(),'generated_file_sha':hashlib.sha256(Path('/workspace/scratch/5ed8df2c5d81/generated_images/exec-935626c3-99bb-4c9d-b73b-77be6bdc234b.png').read_bytes()).hexdigest()},indent=2))
