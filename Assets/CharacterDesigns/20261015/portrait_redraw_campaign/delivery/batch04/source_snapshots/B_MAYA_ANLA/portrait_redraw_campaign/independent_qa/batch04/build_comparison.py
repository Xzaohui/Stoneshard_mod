from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
OUT=Path(__file__).resolve().parent
C=OUT.parent.parent
R=C.parents[3]
slugs=['aren','rowen','maya','anla']
board=Image.new('RGB',(1320,750),(65,65,65));d=ImageDraw.Draw(board)
d.text((20,12),'Batch04 independent QA / selected candidates: 1x and 4x nearest-neighbor. Not native-pixel final.',fill='white')
items=[]
for i,s in enumerate(slugs):
 m=json.loads((C/s/'manifest.json').read_text());p=C/s/m['selected_portrait'];im=Image.open(p).convert('RGBA')
 x=20+i*325;d.text((x,40),s+' / '+p.stem.replace('_74x100_candidate',''),fill='white')
 for j,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+95*j,65))
 big=im.resize((296,400),Image.Resampling.NEAREST);board.paste(big,(x,190),big)
 h=hashlib.sha256(p.read_bytes()).hexdigest();d.text((x,610),h[:32],fill='white');d.text((x,630),h[32:],fill='white')
 items.append({'slug':s,'path':str(p.relative_to(R)),'sha256':h})
styles=[('Mara v2','Assets/CharacterDesigns/20261015/native_style_pilot/mara/assets/portrait_v2_74x100.png'),('Iwo v1','Assets/CharacterDesigns/20261015/native_style_pilot/iwo/candidates/portrait_v1_74x100_candidate.png'),('Leiya v2','Assets/CharacterDesigns/20261015/native_style_continuation/leiya/candidates/portrait_v2_maxcoverage_74x100_candidate.png'),('Tore v1','Assets/CharacterDesigns/20261015/native_style_continuation/tore/candidates/portrait_v1_74x100_candidate.png')]
# The actual reviewed style images are separate source files; no style is painted into candidates.
board.save(OUT/'selected_candidates_1x_4x.png')
(OUT/'comparison_manifest.json').write_text(json.dumps({'candidate_files':items,'output':'selected_candidates_1x_4x.png','style_references':[{'name':n,'path':p} for n,p in styles]},indent=2)+'\n')
