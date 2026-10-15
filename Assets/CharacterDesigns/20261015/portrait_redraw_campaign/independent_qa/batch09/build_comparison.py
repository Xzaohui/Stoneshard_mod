from pathlib import Path
from PIL import Image, ImageDraw
import json,hashlib
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
selection=json.loads((OUT/'final_selection.json').read_text())
board=Image.new('RGB',(1304,1000),(91,91,91));d=ImageDraw.Draw(board)
d.text((16,12),'Batch09 independent visual QA | imagegen redraw derivatives, NOT native-pixel finals',fill='white')
records=[]
for i,row in enumerate(selection['characters']):
 p=CAMP/row['slug']/row['selected_candidate'];im=Image.open(p).convert('RGBA');x=16+i*324
 d.text((x,40),row['slug']+' '+row['selected_version'],fill='white')
 for j,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
  tile=Image.new('RGBA',im.size,bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+j*96,66))
 large=im.resize((296,400),Image.Resampling.NEAREST);board.paste(large,(x,190),large)
 d.text((x,606),row['decision'],fill='white')
 records.append({'slug':row['slug'],'source':str(p.relative_to(CAMP)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for i,s in enumerate(['mara','iwo','leiya','tore']):
 p=CAMP/'sela/sources'/f'{s}_style_reference.png';im=Image.open(p).convert('RGBA');x=16+i*324
 d.text((x,650),s+' core style / 3x nearest',fill='white');large=im.resize((222,300),Image.Resampling.NEAREST);board.paste(large,(x,676),large)
board.save(OUT/'selected_candidates_1x_4x.png')
(OUT/'comparison_manifest.json').write_text(json.dumps({'sources':records,'output':'selected_candidates_1x_4x.png','purpose':'Review-only layout; source pixels preserved; no editing or image generation.'},ensure_ascii=False,indent=2)+'\n')
