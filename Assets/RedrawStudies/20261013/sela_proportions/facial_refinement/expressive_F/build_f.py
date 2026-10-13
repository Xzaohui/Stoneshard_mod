from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
S=P.parent/'before_native.png';a=np.array(Image.open(S).convert('RGBA'));b=a.copy()
col={'.':(0,0,0,0),'B':(32,27,26,255),'E':(53,39,31,255),'D':(73,48,40,255),'C':(102,67,51,255),'H':(129,86,56,255),'I':(179,102,65,255),'F':(219,148,97,255),'G':(239,187,130,255)}
# Rebuild planes, compact the feature triangle, lift the near mouth corner.
rows={11:'BDGGFFICB',12:'BHGGGFCIC',13:'BIFGGCFII',14:'BIBFGBBII',15:'BIGGGFFII',16:'BIFIFFFII',17:'.BFGFIFFI',18:'.BFIIGFFI',19:'.BFGGFFIB'}
for y,row in rows.items():
 for dx,key in enumerate(row):b[y,10+dx]=col[key]
im=Image.fromarray(b);im.save(P/'sela_face_F_native.png');im.resize((280,352),Image.Resampling.NEAREST).save(P/'sela_face_F_8x.png')
C=Image.open(P.parent/'c_reorganized/sela_face_C_native.png').convert('RGBA')
board=Image.new('RGB',(600,600),(180,183,172));d=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for i,(name,sprite) in enumerate([('C',C),('F - knowing smile',im)]):
 x=i*300;d.text((x+40,20),name,font=font,fill=(28,28,28));sp=sprite.resize((210,264),Image.Resampling.NEAREST);board.paste(sp,(x+45,55),sp);sp=sprite.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(sp,(x+40,370),sp)
board.save(P/'comparison_C_F_mobile.png')
mask=np.any(a!=b,axis=2);allowed=np.zeros(mask.shape,bool);allowed[11:20,10:19]=True
qa={'changed_pixels':int(mask.sum()),'outside_face_equal':bool(np.array_equal(a[~allowed],b[~allowed])),'body_y20_onwards_equal':bool(np.array_equal(a[20:],b[20:])),'hair_above_y11_equal':bool(np.array_equal(a[:11],b[:11])),'palette_added':list(set(map(tuple,b.reshape(-1,4)))-set(map(tuple,a.reshape(-1,4)))),'sha256':hashlib.sha256((P/'sela_face_F_native.png').read_bytes()).hexdigest()}
(P/'QA-F.json').write_text(json.dumps(qa,indent=2)+'\n')
(P/'pixel_edits_F.json').write_text(json.dumps([{'x':int(x),'y':int(y),'before':a[y,x].tolist(),'after':b[y,x].tolist()} for y,x in zip(*np.where(mask))],indent=2)+'\n')
print(qa)
