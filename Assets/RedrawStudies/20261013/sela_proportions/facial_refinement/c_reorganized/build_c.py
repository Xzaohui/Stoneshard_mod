from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,sys
HOME=Path(__file__).resolve().parent; P=Path(sys.argv[1]) if len(sys.argv)>1 else HOME; P.mkdir(parents=True,exist_ok=True); BASE=HOME.parent.parent/'revision_1to1'; ROOT=HOME.parents[5]
src=BASE/'sela_structural_idle_view01_f000.png'; im=Image.open(src).convert('RGBA'); a=np.array(im); b=a.copy()
colors={'.':(0,0,0,0),'B':(32,27,26,255),'E':(53,39,31,255),'D':(73,48,40,255),'C':(102,67,51,255),'H':(129,86,56,255),'I':(179,102,65,255),'F':(219,148,97,255),'G':(239,187,130,255)}
# Fixed native face work envelope, x10..18 / y11..19; does not reach external hair or bun.
rows={11:'BDGGFFICB',12:'BHGGGFFIC',13:'BHFGGFFFI',14:'BHBFG BBFI'.replace(' ',''),15:'BIFGFGIFI',16:'BIFFGGFFI',17:'.BFIFGFFI',18:'.BFGGGFFI',19:'.BFGIFFFB'}
# Explicit planned organization: far eye12,14; near eye15..16,14;
# bridge/nose14,15..17; separated mouth14,19; y18 skin-only.
reasons={11:'Recede interior fringe to provide a readable forehead plane',12:'Retain forehead and hairline context',13:'Reorganize warm brow plane and expose near-side upper face',14:'Separate far eye, nose bridge and compact near-eye dark cluster',15:'Keep clear near-eye focus and internal nasal bridge',16:'Move nasal plane inside face rather than silhouetted ledge',17:'Recess projecting nose and connect warm cheeks',18:'Reserve visible skin row between nose and mouth',19:'Low short warm mouth, softly modeled jaw transition'}
allowed=np.zeros(a.shape[:2],bool)
for y,row in rows.items():
 for dx,c in enumerate(row):
  x=10+dx;allowed[y,x]=True;b[y,x]=colors[c]
changed=np.any(a!=b,axis=2)
result=Image.fromarray(b);result.save(P/'sela_face_C_native.png');result.resize((280,352),Image.Resampling.NEAREST).save(P/'sela_face_C_8x.png')
Image.fromarray((allowed*255).astype('uint8')).save(P/'face_allowed_envelope_C.png');Image.fromarray((changed*255).astype('uint8')).save(P/'face_mask_C.png')
items=[('Before',im),('A',Image.open(HOME.parent/'sela_face_A_native.png').convert('RGBA')),('B',Image.open(HOME.parent/'sela_face_B_native.png').convert('RGBA')),('C',result),('Gunda',Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png').convert('RGBA')),('Bert',Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals/s_npc_merchant01_0.png').convert('RGBA'))]
for scale in [1,8]:
 board=Image.new('RGB',(44*scale*len(items),44*scale+24),(180,183,172));d=ImageDraw.Draw(board)
 for i,(name,img) in enumerate(items):
  d.text((i*44*scale+3,4),name,fill=(20,20,20));spr=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST);board.paste(spr,(i*44*scale+(44*scale-spr.width)//2,24),spr)
 board.save(P/f'comparison_C_originals_{scale}x.png')
board=Image.new('RGB',(220*len(items),250),(180,183,172));d=ImageDraw.Draw(board)
for i,(name,img) in enumerate(items):
 d.text((220*i+4,5),name,fill=(20,20,20));spr=img.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(spr,(220*i,30),spr)
board.save(P/'face_C_closeups_10x.png')
write=lambda n,o:(P/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
write('pixel_edits_C.json',[{'x':int(x),'y':int(y),'before':a[y,x].tolist(),'after':b[y,x].tolist(),'reason':reasons[y]} for y,x in zip(*np.where(changed))])
write('QA-producer-C.json',{'changed_pixels':int(changed.sum()),'outside_allowed_mask_equal':bool(np.array_equal(a[~allowed],b[~allowed])),'rows_y20_and_below_equal':bool(np.array_equal(a[20:],b[20:])),'rows_above_y11_equal':bool(np.array_equal(a[:11],b[:11])),'new_colors':list(set(map(tuple,b.reshape(-1,4)))-set(map(tuple,a.reshape(-1,4)))),'outside_mask_sha256':hashlib.sha256(b[~allowed].tobytes()).hexdigest(),'native_sha256':hashlib.sha256((P/'sela_face_C_native.png').read_bytes()).hexdigest(),'visual_review':'Pending; pixels changed count is not quality evidence.'})
print('Generated',P)
# Mobile sheet: entire original 35x44 canvases at 6x, plus complete heads at 10x.
board=Image.new('RGB',(600,1180),(180,183,172));d=ImageDraw.Draw(board)
from PIL import ImageFont
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for row,pair in enumerate([[items[0],items[3]],[items[4],items[5]]]):
 y0=row*590
 if row:d.text((165,y0+5),'ORIGINAL REFERENCES',font=font,fill=(28,28,28))
 for col,(name,img) in enumerate(pair):
  x0=col*300; name='BEFORE' if name=='Before' else name
  d.text((x0+100,y0+34),name,font=font,fill=(28,28,28))
  d.text((x0+22,y0+63),'6x',font=small,fill=(70,70,65))
  spr=img.resize((img.width*6,img.height*6),Image.Resampling.NEAREST);board.paste(spr,(x0+(300-spr.width)//2,y0+75),spr)
  d.text((x0+22,y0+345),'10x face',font=small,fill=(70,70,65))
  spr=img.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(spr,(x0+40,y0+365),spr)
board.save(P/'mobile_before_C_references.png')
