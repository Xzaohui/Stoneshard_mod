from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent;P=D.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.open(P/'hers_native_v1.png').convert('RGBA');original=im.copy();edits=[]
def px(x,y,c,why):
 before=list(im.getpixel((x,y)));after=tuple(bytes.fromhex(c))+(255,) if c else (0,0,0,0)
 if before!=list(after):im.putpixel((x,y),after);edits.append(dict(x=x,y=y,before=before,after=list(after),reason=why))
# Consolidate generated hair into three connected ash shades, keeping hairline.
for y in range(5,11):
 for x in range(11,24):
  r,g,b,a=im.getpixel((x,y))
  if not a or max(r,g,b)<45:continue
  if y==10 and x<20:continue # forehead begins here
  lum=(r+g+b)/3
  px(x,y,'a08e7b' if lum>123 else '887a6e' if lum>78 else '5a5050','Consolidate ash-grey hair into broad clusters')
# Flatten central forehead and cheeks, preserving two dark eyes/nose bridge.
for x,y,c in [(14,10,'d79968'),(15,10,'d79968'),(16,10,'d79968'),(17,10,'d79968'),(14,11,'efb581'),(15,11,'efb581'),(16,11,'efb581'),(17,11,'efb581'),(18,11,'d79968'),(16,12,'efb581'),(17,12,'efb581'),(18,14,'d79968'),(18,15,'d79968'),(19,15,'d79968'),(15,17,'887a6e'),(16,17,'887a6e'),(17,17,'887a6e'),(18,17,'887a6e')]:px(x,y,c,'Merge forehead/cheek and restrained stubble clusters; preserve eye/bridge separation')
# Remove upper coat lapel points as a flat wool front around a plain linen neck.
for y in range(20,26):
 for x in range(12,23):
  if im.getpixel((x,y))[3]:px(x,y,'2d292e' if x in (12,22) else '443d40','Remove V-shaped lapel triangles into plain charcoal wool')
# Narrow squared linen collar; no long V-shaped shirtfront or suit lapel.
for x,y,c in [(15,20,'c1aa8c'),(16,20,'dfc4a0'),(17,20,'dfc4a0'),(18,20,'c1aa8c'),(19,20,'887a6e'),(15,21,'887a6e'),(16,21,'c1aa8c'),(17,21,'c1aa8c'),(18,21,'887a6e'),(17,22,'5a5050'),(17,23,'5a5050'),(17,24,'5a5050'),(17,25,'5a5050')]:px(x,y,c,'Plain short bone-linen standing collar and closed straight wool fastening')
# Two broad coat planes rather than lapel edge speckles.
for x,y in [(13,23),(13,24),(13,25),(14,24),(14,25),(19,23),(19,24),(19,25),(20,23),(20,24),(20,25)]:px(x,y,'443d40','Merge unnecessary isolated coat highlights')
im.save(D/'hers_native_v2.png');im.resize((280,352),Image.Resampling.NEAREST).save(D/'hers_native_v2_8x.png')
# Local native redraw of the same ordinary CLOSED ledger: no writing or symbol.
# 12x8 is an experimental readability budget, not an engine requirement.
rows=['..OOOOOOOO..','.OTTTTTTTTO.','OSTTTTTTTTTO','OSTTTTTTTTTO','OSBBBBBBBBBO','OSEEEEEEEEEO','OSEEEEEEEEEO','.OOOOOOOOOO.']
colors={'O':'17151c','T':'956347','S':'49372f','B':'634634','E':'c1aa8c'}
b=Image.new('RGBA',(12,8));bed=[]
for y,row in enumerate(rows):
 assert len(row)==12
 for x,c in enumerate(row):
  if c!='.':b.putpixel((x,y),tuple(bytes.fromhex(colors[c]))+(255,));bed.append(dict(x=x,y=y,after=list(b.getpixel((x,y))),plane={'O':'outline','T':'closed cover','S':'dark straight spine','B':'cover edge','E':'light page edge'}[c]))
b.save(D/'ledger_native_v2.png');b.resize((96,64),Image.Resampling.NEAREST).save(D/'ledger_native_v2_8x.png')
board=Image.new('RGB',(820,470),(113,117,119));draw=ImageDraw.Draw(board)
for i,(name,q) in enumerate([('Hers v1',original),('Hers v2',im)]):
 x=280*i;draw.text((x+15,8),name,fill='white');board.paste(q,(x+110,32),q);q8=q.resize((280,352),Image.Resampling.NEAREST);board.paste(q8,(x,96),q8)
for i,(name,q) in enumerate([('Ledger v1 9x6',Image.open(P/'ledger_native_v1.png')),('Ledger v2 12x8',b)]):
 y=20+i*200;draw.text((580,y),name,fill='white');board.paste(q,(620,y+24),q);q8=q.resize((q.width*8,q.height*8),Image.Resampling.NEAREST);board.paste(q8,(595,y+72),q8)
board.save(D/'v1_v2_native_and_8x.png')
(D/'pixel_edit_log.json').write_text(json.dumps({'hers_changes':edits,'ledger_redraw':bed},ensure_ascii=False,indent=2)+'\n')
a=np.array(im);q={'canvas':list(im.size),'bbox_half_open':im.getbbox(),'opaque_colors':len(np.unique(a[a[:,:,3]>0,:3],axis=0)),'alpha_values':np.unique(a[:,:,3]).tolist(),'foot_y':37,'hers_changed_pixels':len(edits),'ledger_canvas':list(b.size),'ledger_redraw_pixels':len(bed),'runtimeVerified':False,'style_pass':False,'v1_sha256':sha(P/'hers_native_v1.png'),'v1_ledger_sha256':sha(P/'ledger_native_v1.png')};(D/'QA.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
