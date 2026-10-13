from PIL import Image, ImageDraw
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
# Retain v1 palette, explicit original native structural edit; no stretching.
PAL=['211a1d','39312e','514b46','75665c','554231','87664b','ad7153','d69970','f1ba86','9d9984','41432c','60613b','80804e','d9c5a1','704827','aa7743']
colors=[tuple(bytes.fromhex(x))+(255,) for x in PAL]; sy='0123456789ABCDEF'
# 23x29 authored grid. Larger 10px-wide head, short torso, lateral thighs,
# raised knees, short shins, horizontal seat, separate two supports.
rows=[
'.........00000.........',
'.......04455540........',
'......0455555540.......',
'......45555554440......',
'......45554788740......',
'......04557888780......',
'......04477070880......',
'.......06778878880.....',
'.......0677988760......',
'........069979960......',
'.......002699920.......',
'.....0033326D0330......',
'....0333330D023330.....',
'...033333FA02333330....',
'...03332200A0223330....',
'...032ABBBDAAA02330....',
'...032ABBBBAAABBD30....',
'...03DDBB00000BB780....',
'...0077870AAAAB7880....',
'...03377870AA007780....',
'..033333330A033333330..',
'.0FF03333330033333330..',
'.0FE00333300003333300..',
'..FE..03330.F003330....',
'..FE..03330.F003330....',
'..FE..00440.F004400....',
'..FE..04540.F045440....',
'..00..045550.0455550...',
'......000000.0000000...'
]
assert len(rows)==29 and all(len(s)==23 for s in rows),[(i,len(s)) for i,s in enumerate(rows) if len(s)!=23]
n=Image.new('RGBA',(35,44));x0,y0=6,9
for y,row in enumerate(rows):
 for x,c in enumerate(row):
  if c!='.':n.putpixel((x+x0,y+y0),colors[sy.index(c)])
n.save(P/'native.png');n.resize((280,352),Image.Resampling.NEAREST).save(P/'native_8x.png')
v1=Image.open(P.parent/'native.png').convert('RGBA'); diff=[{'xy':[x,y],'before':list(v1.getpixel((x,y))),'after':list(n.getpixel((x,y)))} for y in range(44) for x in range(35) if v1.getpixel((x,y))!=n.getpixel((x,y))]
(P/'pixel_edits_from_v1.json').write_text(json.dumps(diff,indent=2)+'\n')
board=Image.new('RGB',(840,388),(95,103,110));d=ImageDraw.Draw(board)
for x,im,label in [(0,v1,'V1: REJECTED'),(280,n,'V2: STRUCTURAL REVISION')]:
 im=im.resize((280,352),Image.Resampling.NEAREST);board.paste(im,(x,30),im);d.text((x+8,10),label,fill='white')
concept=Image.open(P.parent/'new_concept.png').convert('RGBA');concept=concept.crop(concept.getbbox());concept.thumbnail((270,330),Image.Resampling.NEAREST);board.paste(concept,(565,35),concept);d.text((567,10),'GENERATED STRUCTURE REF',fill='white');board.save(P/'v1_v2_comparison.png')
qa={'canvas':[35,44],'bbox':list(n.getbbox()),'height':29,'feet_y':37,'colors':len({p[:3] for p in n.getdata() if p[3]}),'alpha_values':sorted(set(n.getchannel('A').getdata())),'manual_edits_vs_v1':len(diff),'runtimeVerified':False,'visual_pass':False,'status':'pending independent review, do not expand frames'}
assert qa['alpha_values']==[0,255] and n.getbbox()[3]-n.getbbox()[1]==29
assert n.getpixel((14,37))[3] and n.getpixel((22,37))[3]
(P/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(qa)
