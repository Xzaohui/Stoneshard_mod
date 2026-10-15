from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
QA=Path(__file__).resolve().parent
ROOT=QA.parents[1]
entries=[('MIA','mia/candidates/portrait_v2_maxcoverage_74x100_candidate.png'),('ENA','ena/candidates/portrait_v2_74x100_candidate.png'),('NARA','nara/candidates/portrait_v2_74x100_candidate.png'),('NELL','nell/candidates/portrait_v2_74x100_candidate.png'),('SEL','sel/candidates/portrait_v2_mediancut_74x100_candidate.png')]
board=Image.new('RGB',(1630,620),(108,108,108));draw=ImageDraw.Draw(board)
draw.text((20,12),'BATCH 01 INDEPENDENT QA | CANDIDATES ONLY | NN + PALETTE DERIVATIVES | NOT NATIVE FINAL / NOT IN GAME',fill='white')
placements=[]
for i,(name,rel) in enumerate(entries):
 x=20+i*322;im=Image.open(ROOT/rel).convert('RGBA'); draw.text((x,39),name+' | 1x dark, gray, light',fill='white')
 for j,bg in enumerate([(20,20,23),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+j*90,62))
 draw.text((x,178),'4x nearest neighbor',fill='white')
 big=im.resize((296,400),Image.Resampling.NEAREST);board.paste(big,(x,198),big)
 placements.append({'actor':name,'path':rel,'sha256':hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),'native_dimensions':list(im.size),'zoom':4,'no_pixel_painting':True})
board.save(QA/'selected_candidates_1x_4x.png')
(QA/'comparison_manifest.json').write_text(json.dumps(placements,indent=2)+'\n')
