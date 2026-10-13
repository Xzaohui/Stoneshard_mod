"""Only alpha cleanup and uniform nearest-neighbor preview layout. No anatomy generation."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json
D=Path(__file__).resolve().parent
R=D.parents[5]
old=D.parent/'tor_raw_imagegen.png'
raw=D/'tor_period_costume_v2_raw_imagegen.png'
def clean(path):
    im=Image.open(path).convert('RGBA')
    a=im.getchannel('A'); im.putalpha(a.point(lambda x:0 if x<=5 else x))
    return im
new=clean(raw)
new.save(D/'tor_period_costume_v2_transparent.png')
for name,color in [('black',(0,0,0,255)),('white',(255,255,255,255))]:
    bg=Image.new('RGBA',new.size,color); bg.alpha_composite(new);bg.convert('RGB').save(D/f'tor_period_costume_v2_{name}.png')
# Both full source canvases share exact dimensions and are scaled at 0.5x identically.
ims=[clean(old),new]
W,H=559,704
board=Image.new('RGB',(W*2+60,H+80),(231,228,219));draw=ImageDraw.Draw(board)
for k,(im,label) in enumerate(zip(ims,['TOR / OLD COSTUME','TOR / PERIOD COSTUME V2'])):
    draw.text((20+k*(W+20),16),label,fill=(35,30,28))
    im=im.resize((W,H),Image.Resampling.NEAREST)
    board.paste(im,(20+k*(W+20),50),im)
board.save(D/'tor_old_new_same_scale.png')
# Full-canvas black/white presentation at the same 0.5x scale.
board=Image.new('RGB',(W*2+60,H+80),(210,210,210));draw=ImageDraw.Draw(board)
for k,name in enumerate(['black','white']):
    draw.text((20+k*(W+20),16),f'TOR V2 / {name.upper()} BACKGROUND',fill=(25,25,25))
    board.paste(Image.open(D/f'tor_period_costume_v2_{name}.png').resize((W,H),Image.Resampling.NEAREST),(20+k*(W+20),50))
board.save(D/'tor_period_costume_v2_black_white.png')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[old,D.parent/'QA-independent.json',R/'design/04_人物/人物_玛拉与伊沃.md',R/'design/05_主线/台本/台本_N1_无钟之夜.md',D.parents[1]/'STYLE_DIRECTION.md']
manifest={'actor':'n1_tor','version':'period_costume_v2','createdAt':'2026-10-13','change':'Costume-only historical-direction revision of previously delivered Tor. No selected roster replacement.','generation':'built-in image_gen identity-preserve edit; one generation; raw preserved','inputImage':str(old.relative_to(R)),'sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in sources],'prompt':'prompt.txt','raw':'tor_period_costume_v2_raw_imagegen.png','candidate':'tor_period_costume_v2_transparent.png','postprocessing':'Candidate only: alpha values <=5 set to zero; no RGB/shape/face/anatomy edits. Preview sheets use identical full-canvas 0.5x nearest-neighbor scale. Raw untouched.','independentReview':'pending','selectedInRoster':False,'concept_only':True,'runtimeIntegrated':False,'runtimeVerified':False,'equipment_compatibility_verified':False,'equipment_mechanism':'unknown','all_old_outputs_preserved':True,'outputs':[]}
for p in sorted(D.iterdir()):
    if p.suffix not in ['.png','.txt','.py']:continue
    o={'path':p.name,'sha256':sha(p)}
    if p.suffix=='.png':
        im=Image.open(p);o.update(size=list(im.size),mode=im.mode)
        if im.mode=='RGBA':o.update(alphaRange=list(im.getchannel('A').getextrema()),alphaBounds=im.getchannel('A').getbbox())
    manifest['outputs'].append(o)
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
