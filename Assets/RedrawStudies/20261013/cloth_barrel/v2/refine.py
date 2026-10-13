from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[4]
C={'O':'26242b','s':'352b29','d':'49332b','w':'604331','m':'79553b','h':'906d4b','H':'a08058','i':'383741','j':'565358','k':'78777a','K':'aaaeb0','L':'c2cbc9','c':'746957','b':'9c8d72','a':'b9ad8e','l':'d6c8a4','r':'675036','t':'a18a59'}
C={k:tuple(bytes.fromhex(v))+(255,) for k,v in C.items()}
im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
def p(pts,c):d.polygon(pts,fill=C[c])
def l(pts,c):d.line(pts,fill=C[c])
def box(b,c):d.rectangle(b,fill=C[c])
# Original v1 silhouette and ground datum retained. Not copied from reference pixels.
p([(8,5),(23,5),(26,8),(27,14),(27,22),(25,26),(21,28),(10,28),(6,26),(4,22),(4,14),(5,8)],'O')
p([(8,7),(23,7),(25,10),(26,15),(26,22),(24,25),(20,27),(11,27),(7,25),(5,21),(5,14),(6,10)],'d')
# Curved stave widths, staggered short lit grain clusters.
p([(7,11),(9,10),(9,16),(8,19),(9,24),(10,26),(8,25),(6,21),(6,15)],'w')
p([(10,10),(12,9),(12,16),(11,19),(12,27),(10,26),(9,21),(9,16)],'m')
p([(13,10),(15,10),(15,16),(14,20),(15,27),(13,27),(12,22),(12,17)],'w')
p([(16,10),(18,10),(18,15),(17,19),(18,26),(16,27),(15,23),(15,17)],'m')
p([(19,10),(21,11),(22,17),(21,20),(21,26),(19,27),(18,22),(19,18)],'w')
p([(22,12),(24,13),(25,17),(24,21),(24,24),(22,26),(22,21),(23,18)],'s')
# Highlights form elongated, broken stair-step clusters rather than full-height flat stripes.
l([(10,16),(10,18),(9,19),(9,21)],'h');l([(11,20),(11,23),(12,24)],'h')
l([(13,17),(13,19),(14,20)],'m');l([(14,22),(14,24)],'m')
l([(16,16),(16,18),(17,19),(17,21)],'h');box((16,23,17,24),'w')
l([(19,16),(20,17),(20,19)],'m');l([(20,22),(20,24)],'m')
l([(7,17),(7,20)],'m');l([(8,22),(8,23)],'h');box((23,16,23,18),'d')
l([(11,26),(12,27)],'w');l([(16,27),(17,27)],'h');box((20,26,21,26),'m')
# Thin hoop: 1px upper highlight, 1px body on front; dark occlusion tucked underneath.
p([(5,12),(8,14),(12,15),(20,15),(24,13),(26,12),(26,14),(23,16),(19,17),(12,17),(8,16),(5,14)],'O')
l([(5,12),(8,14),(12,15),(20,15),(24,13),(26,12)],'j')
l([(5,13),(8,15),(12,16),(19,16),(23,15),(26,13)],'i')
l([(6,13),(8,14),(11,15)],'k');l([(8,14),(9,14)],'K');l([(12,15),(14,15)],'k');l([(20,15),(23,14)],'j')
# Lower hoop compressed to 2px ribbon with restrained cool glint; no wide rubber band.
l([(6,22),(9,24),(13,25),(20,25),(24,23),(25,22)],'j')
l([(6,23),(9,25),(13,26),(20,26),(24,24),(25,23)],'i')
l([(7,23),(9,24),(12,25)],'k');l([(9,24),(10,24)],'L');l([(13,25),(15,25)],'k')
# Supple linen: asymmetrical short folded hem and a gently sagging top, no hard cylindrical lip.
p([(9,3),(21,3),(24,4),(26,6),(27,8),(27,9),(29,12),(28,14),(25,13),(23,12),(21,14),(19,14),(17,12),(14,13),(12,12),(9,14),(7,13),(6,12),(3,13),(3,10),(5,8),(5,6),(7,4)],'O')
p([(6,7),(25,7),(26,9),(28,11),(28,12),(25,12),(23,11),(21,13),(19,13),(17,11),(14,12),(12,11),(9,13),(7,11),(4,12),(4,10)],'c')
p([(6,6),(10,4),(20,4),(23,5),(25,6),(25,8),(23,9),(18,9),(15,8),(12,9),(8,8)],'a')
p([(8,6),(11,4),(18,4),(19,5),(16,6),(16,7),(12,7),(10,8),(8,7)],'l')
p([(19,6),(22,5),(24,6),(24,7),(21,8),(18,8),(17,7)],'b')
p([(12,8),(14,7),(17,8),(19,9),(16,9)],'b')
p([(5,9),(7,8),(8,9),(7,11),(4,12)],'a')
p([(10,9),(11,9),(12,11),(10,12),(9,13),(8,11)],'b')
p([(14,9),(16,9),(16,11),(14,12),(13,11)],'a')
p([(20,10),(22,9),(23,10),(21,12),(20,13),(19,11)],'b')
p([(25,9),(26,10),(28,12),(26,12),(25,11)],'a')
# One tied cord, deliberately no paper tag or certificate. Rope follows curved rim discontinuously behind knot.
l([(5,8),(8,9),(12,10),(21,10),(25,9),(27,8)],'d')
l([(6,8),(9,9),(13,10),(20,10),(25,9)],'r')
l([(10,9),(12,10),(17,10)],'t')
p([(7,9),(9,9),(10,10),(9,11),(9,13),(8,13),(8,11),(6,11),(6,10)],'d')
l([(7,10),(8,10),(8,12)],'t');l([(9,10),(10,11)],'r')
im.save(P/'candidate_water_container_native.png');im.resize((256,256),Image.Resampling.NEAREST).save(P/'candidate_water_container_8x.png')
v1=Image.open(P.parent/'candidate_water_container_native.png').convert('RGBA');ref=Image.open(R/'Assets/ReferenceAudit/20261013/originals/Barrel_0.png').convert('RGBA')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
board=Image.new('RGB',(820,360),'#383a3e');bd=ImageDraw.Draw(board)
for x,img,title in [(10,ref,'Historical reference / 8x'),(275,v1,'V1 / 8x'),(550,im,'V2 / 8x')]:
 bd.text((x+8,12),title,font=font,fill='white');big=img.resize((img.width*8,img.height*8),Image.Resampling.NEAREST);board.paste(big,(x,44),big);board.paste(img,(x+100,315),img)
board.save(P/'v1_v2_reference_comparison.png')
qa=Image.new('RGB',(768,288));qd=ImageDraw.Draw(qa)
for n,bg in enumerate(['#f1eddd','#66665e','#171821']):
 qd.rectangle((n*256,0,n*256+255,287),fill=bg);big=im.resize((256,256),Image.Resampling.NEAREST);qa.paste(big,(n*256,24),big)
qa.save(P/'native_background_QA.png')
a=np.array(im);v=np.array(v1);coords=np.argwhere(np.any(a!=v,axis=2));ed=[{'x':int(x),'y':int(y),'before_rgba':v[y,x].tolist(),'after_rgba':a[y,x].tolist()}for y,x in coords]
(P/'pixel_edits_v1_to_v2.json').write_text(json.dumps({'baseline':'../candidate_water_container_native.png','changes':ed,'changed_pixels':len(ed)},indent=2)+'\n')
print('changed',len(ed),'colors',len(np.unique(a[a[:,:,3]>0],axis=0)),'bbox',im.getbbox())
