from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
palette=json.loads((P/'pixel_edit_log.json').read_text())['palette']
source=P/'liqui_native_v1.png';original=Image.open(source).convert('RGBA');im=original.copy();edits=[]
def row(x,y,s,reason):
 for n,c in enumerate(s):
  if c=='_':continue
  pos=(x+n,y);before=im.getpixel(pos);after=tuple(bytes.fromhex(palette[int(c,18)]))+(255,) if c!='.' else (0,0,0,0)
  if before!=after:im.putpixel(pos,after);edits.append({'x':pos[0],'y':pos[1],'before':before,'after':after,'reason':reason})
# Local hand-pixel edits, no geometric rescale and no new image generation.
row(13,10,'256666632','Merge forehead into one warm plane with one shaded border')
row(13,11,'233663322','Retain readable adult brow band')
row(13,12,'650665052','Retain two single-pixel eyes and broad cheek')
row(13,13,'566566652','Merge cheek planes; nose one functional shadow')
row(13,14,'566756652','Retain angular nose edge without extra bright island')
row(13,15,'255335522','Move small mouth and jaw upward to shorten bright face')
row(13,16,'225555220','Shorter broad chin; continuous shadow border')
row(14,17,'2075708','Single short neck below chin, collar at sides')
row(14,18,'89099899','Replace old low jaw with green collar, isolate brief neck')
row(14,19,'880BC899','Close low skin wedge with collar, retain adult face proportions')
# Smooth two tiny hair highlights while retaining auburn swept shape and braid.
row(17,6,'22','Merge small auburn crown highlight into larger hair plane')
row(20,8,'22','Merge isolated small side-hair highlight')
# One stepped tan strap passes in front of a low-contrast belt. Remove the bright gray buckle block.
row(15,21,'CCCC1E089','Continuous ochre chest and single strap boundary')
row(15,22,'CCCB1E899','Merge chest noise beside strap')
row(15,23,'CCB1E1C99','Stepped strap with dark separation from tunic')
row(15,24,'BB1E1CB99','Connect diagonal strap through upper waist')
row(15,25,'111E11G99','Dark belt behind tan strap; reduce competing gray buckle to one subdued pixel')
row(15,26,'11E1CCB99','Strap exits belt and meets closed bag, ochre tunic stays separate')
row(12,27,'4FEE2','One broad closed bag flap, remove duplicate bright highlight')
row(12,28,'E44E2','Retain closed flap plane')
# Explicit 1px dark divider keeps empty hand separate from single bag.
row(11,28,'0','Empty hand and closed bag edge separation')
row(11,29,'0','Continue hand/bag separator')
im.save(D/'liqui_native_v2.png');im.resize((280,352),Image.Resampling.NEAREST).save(D/'liqui_native_v2_8x.png')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
log={'input':'../liqui_native_v1.png','input_sha256':sha(source),'method':'explicit pixel-coordinate edits only; same 18-color palette, no rescale','edits':edits,'operation_count':len(edits),'unique_coordinates':len({(e['x'],e['y']) for e in edits}),'net_changed_pixels':sum(a!=b for a,b in zip(original.getdata(),im.getdata()))}
(D/'pixel_edit_log_v2.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
# Composite native 1x strip; this file itself is inspected at original pixel dimensions.
refs=[('Frid','s_npc_herbalist_0.png'),('Bert','s_npc_merchant01_0.png'),('Jurg','s_npc_carpenter_0.png'),('Gunda','s_peasantfemale_09_0.png')]
figs=[('LIQUI v1',original),('LIQUI v2',im)]+[(n,Image.open(R/'Assets/ReferenceAudit/20261013/originals'/f).convert('RGBA')) for n,f in refs]
b=Image.new('RGB',(len(figs)*45,50),'#777777')
for j,(name,a) in enumerate(figs):b.paste(a,(j*45,3),a)
b.save(D/'native_1x_strip.png')
b=Image.new('RGB',(6*300,460),'#777777');d=ImageDraw.Draw(b)
for j,(name,a) in enumerate(figs):
 a=a.resize((280,352),Image.Resampling.NEAREST);b.paste(a,(j*300+10,40),a);d.text((j*300+10,14),name,fill='white')
d.text((10,420),'8x nearest. Same native scale. Structure/style review only; runtime and production unverified.',fill='white');b.save(D/'comparison_v1_v2_refs_8x.png')
print(json.dumps({'operations':len(edits),'net_pixels':log['net_changed_pixels'],'bbox':im.getbbox(),'sha256':sha(D/'liqui_native_v2.png')},indent=2))
