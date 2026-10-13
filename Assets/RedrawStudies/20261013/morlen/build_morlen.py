from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
P={'o':'201b21','h':'484149','g':'716c70','G':'99908a','w':'b8aea0','s':'aa6754','S':'d98c6a','f':'f5b486','e':'312426','n':'8e5044','c':'c9b899','C':'a7967c','d':'766b58','a':'414331','b':'5c5d3e','B':'79774c','l':'3d2928','L':'644437','r':'896046','k':'a9864f'}
P={k:tuple(bytes.fromhex(v))+(255,) for k,v in P.items()}
im=Image.new('RGBA',(35,44));ops=[]
def put(x,y,k,why):
 old=im.getpixel((x,y));v=P[k] if k!='.' else (0,0,0,0)
 if old!=v: im.putpixel((x,y),v);ops.append({'x':x,'y':y,'before':list(old),'after':list(v),'cluster':why})
def row(y,x,s,why):
 for dx,c in enumerate(s):put(x+dx,y,c,why)
# Native topology is authored row-by-row from fresh concept, NOT resized original.
head=[(13,'ooooooo'),(11,'ooggGGggoo'),(10,'ogGGgGggGggo'),(9,'ogGgghggGggggo'),(9,'ogghhSSSffhggo'),(9,'oghhSfffffShggo'),(9,'ohhSfffffffShgo'),(10,'ohSfffffffSggo'),(10,'oSoooffoooSgho'),(10,'oSeefSfSeeSgho'),(10,'oSfSfSfSfSSsgo'),(10,'osSffnffSSsgho'),(11,'ogSnnSnnSggo'),(11,'oggGhhnGgggo'),(11,'ogGggsGgggo'),(12,'ogGGgggggo'),(13,'oogggggoo')]
for y,(x,s) in enumerate(head,4):row(y,x,s,'wide swept gray hair / face / close beard')
# Scarf overlaps lower beard; shoulder and chest are compact.
body=[(9,'ooCcooooooogooo'),(8,'oabCccccccCCLbo'),(8,'obBCccccCCCLLbo'),(8,'obBbCCCcCLLbbBbo'),(7,'oabBboCCoLLabbBbo'),(7,'obBBboCdoLaoBbBbo'),(7,'obBaboCcoLaofSbo'),(7,'oaabooCCoLaoSSbo'),(8,'oggoLllllllooSoo'),(8,'osfoLlklllloLLLLLo'),(8,'oSfoaboCboLoLrrLLo'),(8,'osooaboCboLoLLLLLo'),(9,'oabBboCboLoLkLLLo'),(9,'obBBboodoLboLLLLLo'),(9,'oabBbooobBbooLLoo'),(10,'ooooo.ooooo')]
for y,(x,s) in enumerate(body,20):row(y,x,s,'cream scarf / olive coat / hands / closed medicine satchel')
# Five-row lower region overlaps coat hem; short separate boots.
for y,x,s in [(34,12,'ollLo.ollLo'),(35,12,'oLllo.oLllo'),(36,11,'oLrLlo.oLrLlo'),(37,10,'oolLloo.oolLloo')]:row(y,x,s,'short separated legs and dark boot soles')
im.save(D/'morlen_native_structural_baseline.png')
for x,y,k,why in [(12,13,'e','left pupil retained below brow'),(13,13,'w','one-pixel left sclera'),(18,13,'e','right pupil retained below brow'),(19,13,'w','one-pixel right sclera'),(15,14,'f','nose bridge highlight'),(16,14,'S','nose side plane'),(15,15,'f','nose tip distinct from beard'),(16,15,'n','nose side shadow')]:put(x,y,k,why)
im.save(D/'morlen_native_v1.png');im.resize((280,352),Image.Resampling.NEAREST).save(D/'morlen_native_v1_8x.png')
(D/'pixel_log_v1.json').write_text(json.dumps({'method':'Every native nontransparent pixel is authored by deterministic row operations; no image resample enters final native raster. All changed assignments logged in order.','palette':P,'operations':ops},indent=2))
R=D.parents[2]/'ReferenceAudit'/'20261013'/'originals'
items=[('Morlen redraw',D/'morlen_native_v1.png'),('Gunda original',R/'s_peasantfemale_09_0.png'),('Jurg original',R/'s_npc_carpenter_0.png'),('Frid original',R/'s_npc_herbalist_0.png'),('Bert original',R/'s_npc_merchant01_0.png')]
b=Image.new('RGB',(1400,418),(83,83,88));dr=ImageDraw.Draw(b)
for i,(name,p) in enumerate(items):
 a=Image.open(p).convert('RGBA');b.paste(a,(i*280+120,28),a);a=a.resize((280,352),Image.Resampling.NEAREST);b.paste(a,(i*280,65),a);dr.text((i*280+15,7),name,fill='white')
b.save(D/'comparison_native_v1.png')
# Old figure same displayed height; diagnostic only, original background retained.
old=Image.open(D/'old_morlen_crop.png');old=old.resize((202,352),Image.Resampling.NEAREST)
c=Image.new('RGB',(1680,418),(83,83,88));c.paste(b,(280,0));c.paste(old,(39,65));ImageDraw.Draw(c).text((20,7),'OLD concept (display only)',fill='white');c.save(D/'comparison_old_native_originals_v1.png')
# geometry facts
alpha=im.getchannel('A');bbox=alpha.getbbox();colors=len(set(im.getdata())-{(0,0,0,0)})
(D/'geometry_v1.json').write_text(json.dumps({'canvas':im.size,'alpha_bbox_half_open':bbox,'visible_size':[bbox[2]-bbox[0],bbox[3]-bbox[1]],'opaque_colors':colors,'alpha_values':sorted(set(alpha.getdata())),'landmarks':{'hair_crown_y':4,'eyes_y':[12,13],'nose_y':[14,15],'beard_bottom_y':20,'scarf_overlap_y':[20,24],'belt_y':[27,28],'coat_hem_y':[33,35],'feet_y':[34,37]},'note':'Beard, scarf and coat overlap. No universal 16/8/10 partition; no engine geometry assumed.'},indent=2))
