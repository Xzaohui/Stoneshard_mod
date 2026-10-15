from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json
out=Path(__file__).resolve().parent; camp=out.parent.parent
slugs=['osin','pelan','rena','roan']; board=Image.new('RGB',(1280,890),(106,106,106));d=ImageDraw.Draw(board)
d.text((20,12),'BATCH08 INDEPENDENT QA | selected 74x100 derivatives | 1x dark/light + exact 4x NN',fill='white')
d.text((20,32),'Concept candidates only. No native-pixel authorship or runtime approval.',fill='white')
records=[]
for i,s in enumerate(slugs):
 m=json.loads((camp/s/'manifest.json').read_text());p=camp/s/m['selected_portrait'];im=Image.open(p).convert('RGBA');x=20+i*314
 d.text((x,62),s.upper()+' / '+Path(m['selected_portrait']).name.replace('_74x100_candidate.png',''),fill='white')
 for j,bg in enumerate([(15,15,18),(235,235,229)]):
  tile=Image.new('RGBA',im.size,bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+j*94,90))
 big=im.resize((296,400),Image.Resampling.NEAREST);board.paste(big,(x,210),big)
 records.append({'slug':s,'path':str(p.relative_to(camp)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
d.text((20,638),'Style references: Mara v2 / Iwo v1 / Leiya v2 maxcoverage / Tore v1 (2x NN)',fill='white')
for i,s in enumerate(['mara','iwo','leiya','tore']):
 p=camp/'osin/sources'/f'{s}_style_reference.png';im=Image.open(p).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(im,(20+i*220,670),im)
board.save(out/'selected_candidates_1x_4x.png')
(out/'comparison_manifest.json').write_text(json.dumps({'source_files':records,'comparison_sha256':hashlib.sha256((out/'selected_candidates_1x_4x.png').read_bytes()).hexdigest(),'resize':'nearest-neighbor only; no character edits'},indent=2)+'\n')
