from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np, json, hashlib
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
# Explicit authored sixteen-color palette, no diffusion or dithering.
PAL=['211a1d','39312e','514b46','75665c','554231','87664b','ad7153','d69970','f1ba86','9d9984','41432c','60613b','80804e','d9c5a1','704827','aa7743']
colors=np.array([tuple(bytes.fromhex(x)) for x in PAL],dtype=np.int32)
im=Image.open(P/'new_concept.png').convert('RGBA')
a=np.array(im)[:,:,3]; bbox=Image.fromarray((a>=128).astype('uint8')*255).getbbox()
im=im.crop(bbox).resize((20,29),Image.Resampling.NEAREST)
a=np.array(im); idx=(((a[:,:,:3].astype(np.int32)[:,:,None,:]-colors)**2).sum(3)).argmin(2)
rgba=np.dstack((colors[idx].astype('uint8'),np.where(a[:,:,3]>=128,255,0).astype('uint8')))
auto=Image.new('RGBA',(35,44)); auto.paste(Image.fromarray(rgba),(7,9)); auto.save(P/'native_initial.png'); auto.resize((280,352),Image.Resampling.NEAREST).save(P/'initial_8x.png')
# Manual pixel-cluster reconstruction, explicitly authored from viewed generated concept.
# Symbols palette 0..9,A..F; '.' is fully transparent. This is not face-preserving resampling.
rows=[
'...........0........',
'.......045554.......',
'......45555340......',
'.....045555740......',
'.....045578870......',
'.....044780780......',
'......0778876.......',
'.....032699960......',
'....03322999320.....',
'....23330D6D0330....',
'...0333320D023330...',
'...33332FA0233330...',
'..03220000A0233320..',
'..032ABBAAA0033200..',
'..032ABBDABAA0BBA0..',
'..032ABBBAAA0ABBD0..',
'..032DDA00000ABD80..',
'..03078770AAAA07880.',
'.0320337870AA00780..',
'.032033330AAA033330.',
'.030F033330AA033330.',
'.030FE033300003330..',
'..00F003330.F03330..',
'...0F003300.F03300..',
'...0FE00440.F0EE0...',
'...0F0.0440.F0E40...',
'...000.0450..0E450..',
'.......04550.045550.',
'.......00000.000000.'
]
assert len(rows)==29 and all(len(r)==20 for r in rows)
symbols='0123456789ABCDEF'; native=Image.new('RGBA',(35,44))
for yy,row in enumerate(rows):
 for xx,s in enumerate(row):
  if s!='.': native.putpixel((7+xx,9+yy),tuple(int(v) for v in colors[symbols.index(s)])+(255,))
# Fully covered legs; no exposed limb anatomy is implied by boot shapes.
native.save(P/'native.png'); native.resize((280,352),Image.Resampling.NEAREST).save(P/'native_8x.png')
diff=[]
for y in range(44):
 for x in range(35):
  b=auto.getpixel((x,y)); n=native.getpixel((x,y))
  if b!=n: diff.append({'xy':[x,y],'before':list(b),'after':list(n)})
(P/'pixel_edits.json').write_text(json.dumps(diff,indent=2)+'\n')
# Comparison: old concept and generated new concept shown at common display height;
# old reduced thumbnail included only to demonstrate limitations, not as a candidate.
oldpath=ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/02_yani_dialogue_poses.png'
old=Image.open(oldpath).convert('RGBA').crop((0,0,565,916)); old=old.crop(old.getbbox())
concept=Image.open(P/'new_concept.png').convert('RGBA').crop(bbox)
board=Image.new('RGB',(940,410),(94,100,107)); d=ImageDraw.Draw(board)
for pic,x,label in [(old,15,'OLD CONCEPT'),(concept,285,'NEW STRUCTURE'),(native.resize((280,352),Image.Resampling.NEAREST),590,'NATIVE 35x44 / 8x')]:
 if x!=590: pic=pic.resize((round(pic.width*320/pic.height),320),Image.Resampling.NEAREST)
 board.paste(pic,(x,40),pic); d.text((x,12),label,fill='white')
d.text((590,395),'Study only: 29px seated bbox. No runtime claim.',fill='white')
board.save(P/'old_new_comparison.png')
# Neutral/dark backgrounds to inspect transparent holes and clusters.
bg=Image.new('RGB',(560,352));
for x,c in [(0,(105,111,116)),(280,(38,39,42))]:
 bg.paste(c,(x,0,x+280,352)); big=native.resize((280,352),Image.Resampling.NEAREST);bg.paste(big,(x,0),big)
bg.save(P/'native_background_QA.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[oldpath,ROOT/'design/04_人物/城市人物/人物_BRY-NPC-YANI_雅尼.md',ROOT/'design/06_支线/城市支线/台本_CS-BRY-15_招募告示的背面.md',ROOT/'Assets/ReferenceAudit/20261013/character_redraw_triage.json',ROOT/'Assets/ReferenceAudit/20261013/character_native_refs_contact.png',ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/PROMPTS.md']
qa={'canvas':[35,44],'alpha_bbox':list(native.getbbox()),'visible_height':native.getbbox()[3]-native.getbbox()[1],'opaque_colors':len(set(p[:3] for p in native.getdata() if p[3])),'alpha_values':sorted(set(native.getchannel('A').getdata())),'feet_ground_y':37,'experiment_only':True,'runtimeVerified':False,'style_approved':False,'reference_local_engine_verified':False,'manual_pixel_changes':len(diff),'source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sources},'outputs':{p.name:sha(p) for p in P.glob('*.png')}}
assert qa['alpha_values']==[0,255] and qa['visible_height']==29 and qa['opaque_colors']<=16
# Both boots have opaque bottom pixels at the same ground row.
assert native.getpixel((16,37))[3] and native.getpixel((23,37))[3]
# Central gap and left stool aperture remain transparent.
assert native.getpixel((18,34))[3]==0 and native.getpixel((13,34))[3]==0
(P/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k not in ['source_hashes','outputs']},ensure_ascii=False))
