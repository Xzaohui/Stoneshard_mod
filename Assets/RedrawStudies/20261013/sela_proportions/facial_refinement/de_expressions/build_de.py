from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,sys
HOME=Path(__file__).resolve().parent;OUT=Path(sys.argv[1]) if len(sys.argv)>1 else HOME;OUT.mkdir(parents=True,exist_ok=True);ROOT=HOME.parents[5]
base=HOME.parent.parent/'revision_1to1/sela_structural_idle_view01_f000.png';a=np.array(Image.open(base).convert('RGBA'))
P={'.':(0,0,0,0),'B':(32,27,26,255),'E':(53,39,31,255),'D':(73,48,40,255),'C':(102,67,51,255),'H':(129,86,56,255),'I':(179,102,65,255),'F':(219,148,97,255),'G':(239,187,130,255),'m':(220,160,116,255),'s':(184,120,87,255),'l':(157,104,84,255)}
# x10..18. Exposed facial planes are gently rounded; crown, outer bun and chin fixed.
rows={
'D':{11:'BDGGGmmCB',12:'BImGGmHmI',13:'BImGGGGmI',14:'BmEGGmEmI',15:'BsmGGGGms',16:'BsmFGGGGs',17:'.BmFGGmms',18:'.BmGllmms',19:'.BmGGGGmB'},
'E':{11:'BDGGGmmCB',12:'BImGGmHmI',13:'BImGGHmmI',14:'BmEGGmEmI',15:'BsmGGGmms',16:'BsmFGGGms',17:'.BmFGGmms',18:'.BmGllFms',19:'.BmGGGmmB'}
}
# D uses a raised outer lip corner and relaxed raised brow; E firm mouth and angled inner brow.
results={}; records={}; qa={}; allowed=np.zeros(a.shape[:2],bool);allowed[11:20,10:19]=True
for k,rs in rows.items():
 b=a.copy()
 for y,row in rs.items():
  assert len(row)==9,(y,row)
  for i,c in enumerate(row):b[y,10+i]=P[c]
 if k=='D':
  b[17,16]=P['s'];b[18,15]=P['s']
  b[14,12]=P['B'];b[14,15]=P['D'];b[14,16]=P['B']
 else:
  b[13,15]=P['m'];b[12,15]=P['H'];b[12,16]=P['H']
  b[14,12]=P['B'];b[14,15]=P['B'];b[14,16]=P['D']
 mask=np.any(a!=b,axis=2);img=Image.fromarray(b);results[k]=img;img.save(OUT/f'sela_face_{k}_native.png');img.resize((280,352),Image.Resampling.NEAREST).save(OUT/f'sela_face_{k}_8x.png');Image.fromarray((mask*255).astype('uint8')).save(OUT/f'face_mask_{k}.png')
 records[k]=[{'x':int(x),'y':int(y),'before':a[y,x].tolist(),'after':b[y,x].tolist(),'reason':('Forehead and brow plane' if y<=13 else 'Compact separated eyes' if y==14 else 'Softer cheek/nasal plane' if y<=16 else 'Visible skin and coordinated mouth expression' if y<=18 else 'Rounded lip-to-chin plane')}for y,x in zip(*np.where(mask))]
 qa[k]={'changed_pixels':int(mask.sum()),'outside_predefined_face_mask_identical':bool(np.array_equal(a[~allowed],b[~allowed])),'crown_and_bun_rows_above11_identical':bool(np.array_equal(a[:11],b[:11])),'chin_body_hands_rows20plus_identical':bool(np.array_equal(a[20:],b[20:])),'new_colors':list(set(map(tuple,b.reshape(-1,4)))-set(map(tuple,a.reshape(-1,4))))}
Image.fromarray((allowed*255).astype('uint8')).save(OUT/'face_allowed_envelope.png')
items=[('C',Image.open(HOME.parent/'c_reorganized/sela_face_C_native.png').convert('RGBA'))]+[(k,results[k])for k in ['D','E']]+[('Gunda',Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png').convert('RGBA'))]
for scale in [1,8]:
 board=Image.new('RGB',(44*scale*len(items),44*scale+24),(180,183,172));d=ImageDraw.Draw(board)
 for i,(name,img) in enumerate(items):
  d.text((i*44*scale+3,4),name,fill=(20,20,20));spr=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST);board.paste(spr,(i*44*scale+(44*scale-spr.width)//2,24),spr)
 board.save(OUT/f'comparison_CDE_{scale}x.png')
board=Image.new('RGB',(220*len(items),250),(180,183,172));d=ImageDraw.Draw(board)
for i,(name,img) in enumerate(items):
 d.text((220*i+4,5),name,fill=(20,20,20));spr=img.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(spr,(220*i,30),spr)
board.save(OUT/'face_CDE_closeups_10x.png')
for n,obj in [('pixel_edits.json',records),('QA-producer.json',qa),('palette.json',P)]: (OUT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda v:int(v))+'\n')
