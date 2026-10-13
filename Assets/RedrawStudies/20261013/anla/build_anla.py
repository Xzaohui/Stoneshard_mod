from PIL import Image, ImageDraw, ImageFont
import numpy as np,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
im=Image.open(D/'anla_redraw_concept_v1.png').convert('RGBA')
palette=['#201a1b','#36282a','#513b30','#745037','#98633f','#bb7850','#6d392a','#9b4930','#c2693e','#f3ac78','#c97d5a','#dd9468','#4f4737','#6c6047','#626467','#a4a19a']
pal=np.array([tuple(bytes.fromhex(s[1:])) for s in palette],dtype=np.int32)
# Structural redraw transfer from NEW imagegen study. Separate anatomical budget,
# NOT a downscaled old 128 panel. All rows and output anchor are explicit.
regions=[('head',(336,247,691,604),(12,11),(11,2)),('torso',(255,604,772,950),(21,10),(7,13)),('apron',(314,950,739,1196),(17,7),(9,23)),('legs',(284,1196,747,1437),(19,8),(8,30))]
out=Image.new('RGBA',(35,44))
for name,box,size,pos in regions:
 p=im.crop(box).resize(size,Image.Resampling.NEAREST);a=np.array(p); rgb=a[:,:,:3].astype(np.int32); ix=((rgb[:,:,None,:]-pal[None,None,:,:])**2).sum(3).argmin(2);a[:,:,:3]=pal[ix];a[:,:,3]=np.where(a[:,:,3]>=128,255,0);p=Image.fromarray(a);out.alpha_composite(p,pos)
out.save(D/'anla_native_structural_baseline.png')
# Explicit pixel corrections: silhouette joins, braid, eye, apron flat panels,
# 2x2 clasp, cuff/mitten boundaries, split hem, two boots on the same baseline.
pixels=[]
def put(x,y,c,reason):
 out.putpixel((x,y),tuple(pal[c])+(255,) if c>=0 else (0,0,0,0));pixels.append({'x':x,'y':y,'palette':c,'reason':reason})
# Hand-retouched logical rows are explicit, reviewable pixel edits.
# Head/hair reduce broken sampling dots; face a single eye, braid a 2px cluster.
head=["...00000....","..0333300...",".033443330..",".0343332320.","03333299920.","03219A90990.",".0299B99990.",".0330B99A0..","..33009A0...","..2300990...","..3300990..."]
for yy,row in enumerate(head,2):
 for xx,c in enumerate(row,11): put(xx,yy,-1 if c=='.' else int(c,16),'head/hair/face cluster redraw')
# Remove source hair fragments outside the newly authored head.
for yy in range(2,13):
 for xx in range(35):
  if xx<11 or xx>22: put(xx,yy,-1,'clean head silhouette')
# Continue short braid over shirt, restore shoulder join.
for x,y,c in [(12,13,2),(13,13,3),(12,14,3),(13,14,2),(12,15,2),(13,15,3),(13,16,0),(14,13,6),(15,13,6),(17,13,9)]:put(x,y,c,'braid/shoulder continuity')
# Quiet apron: two flat panels with one shadow strip and clean split.
for yy in range(23,30):
 for xx in range(12,22):
  put(xx,yy,2 if xx in [12,21] else 3,'flat leather apron panels')
for yy in range(26,30): put(17,yy,1,'split apron seam')
for x,y,c in [(17,29,0),(18,29,0),(13,28,3),(20,28,3),(15,22,2),(16,22,2),(17,22,2),(18,22,2),(19,22,2)]:put(x,y,c,'apron hem and belt')
# Ordinary clasp only, 2x2 steel; mitten hands remain generated clusters.
for x,y,c in [(15,18,15),(16,18,14),(15,19,14),(16,19,15),(17,18,0),(18,18,2)]:put(x,y,c,'2x2 clasp/readable hand boundary')
# Tiny belt stamp restrained to a dark rectangular tool with one steel tip.
for x,y,c in [(23,21,14),(23,22,2),(23,23,2),(24,21,-1),(24,22,-1)]:put(x,y,c,'small belt stamp')

out.save(D/'anla_native_v1.png')
out.resize((280,352),Image.Resampling.NEAREST).save(D/'anla_native_v1_8x.png')
(D/'pixel_edits.json').write_text(json.dumps(pixels,indent=2))
(D/'geometry.json').write_text(json.dumps({'canvas':[35,44],'feet_bottom_exclusive':38,'target_visible_height':36,'regions':regions,'palette':palette,'alpha_threshold':128,'filter':'NEAREST','dither':False},indent=2))
# v2: reference-led compact head/body budget, after same-scale visual audit.
v2=Image.new('RGBA',(35,44))
v2_regions=[('head_and_braid',(11,2,23,13),(14,16),(10,4)),('shirt_and_hands',(7,13,28,23),(21,8),(7,20)),('apron',(9,23,27,30),(18,5),(9,28)),('trousers_and_boots',(8,30,27,38),(19,5),(8,33))]
for name,box,size,pos in v2_regions:v2.alpha_composite(out.crop(box).resize(size,Image.Resampling.NEAREST),pos)
# Both feet fixed on y=37; no sole pixels below anchor.
v2.save(D/'anla_native_v2.png');v2.resize((280,352),Image.Resampling.NEAREST).save(D/'anla_native_v2_8x.png')
(D/'geometry_v2.json').write_text(json.dumps({'canvas':[35,44],'feet_bottom_exclusive':38,'visible_height':34,'regions':v2_regions,'basis':'Gunda/Jurg/Frid measured visible body 33–34 px; this is reference budget, not engine standard','palette':palette,'alpha_threshold':128,'filter':'NEAREST','dither':False},indent=2))
R=D.parents[2]/'ReferenceAudit'/'20261013'/'originals'
items=[('Anla v2 / redraw',D/'anla_native_v2.png'),('Gunda / original',R/'s_peasantfemale_09_0.png'),('Jurg / original',R/'s_npc_carpenter_0.png'),('Frid / original',R/'s_npc_herbalist_0.png')]
board=Image.new('RGB',(1120,405),(77,77,82));dr=ImageDraw.Draw(board)
for i,(label,fp) in enumerate(items):
 p=Image.open(fp).convert('RGBA').resize((280,352),Image.Resampling.NEAREST);board.paste(p,(i*280,30),p);dr.text((i*280+12,9),label,fill='white');dr.line((i*280,334,(i+1)*280-1,334),fill=(96,103,103))
board.save(D/'comparison_native_v2_8x.png')
