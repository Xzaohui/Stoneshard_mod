"""QA contact sheet only; nearest-neighbor compositing, no asset edits."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib,json
OUT=Path(__file__).resolve().parent;CAMPAIGN=OUT.parent.parent;REPO=CAMPAIGN.parents[3]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
slugs=['avi','daran','elen','hase'];canvas=Image.new('RGB',(1320,720),(92,92,92));draw=ImageDraw.Draw(canvas)
draw.text((20,14),'Batch05 - selected portrait candidates (not native-authored finals)',font=font,fill='white')
draw.text((20,40),'1x on dark / gray / light, then 4x nearest neighbor. Temporary <=32 visible RGB colors.',font=small,fill='white')
records=[]
for i,slug in enumerate(slugs):
 root=CAMPAIGN/slug;m=json.loads((root/'manifest.json').read_text());path=root/m['selected_portrait'];im=Image.open(path).convert('RGBA');x=20+i*325
 draw.text((x,74),slug.upper()+' / '+path.name.split('_74x100')[0],font=font,fill='white')
 for j,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',im.size,bg+(255,));tile.alpha_composite(im);canvas.paste(tile.convert('RGB'),(x+j*95,104))
 big=im.resize((296,400),Image.Resampling.NEAREST);canvas.paste(big,(x,225),big)
 h=hashlib.sha256(path.read_bytes()).hexdigest();draw.text((x,644),h[:24],font=small,fill='white')
 records.append({'slug':slug,'path':str(path.relative_to(REPO)),'sha256':h,'native_dimensions':list(im.size),'display_scales':[1,4]})
out=OUT/'selected_candidates_1x_4x.png';canvas.save(out)
(OUT/'comparison_manifest.json').write_text(json.dumps({'comparison':str(out.relative_to(REPO)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_assets':records,'method':'Technical nearest-neighbor QA sheet; no redraw, no interpolation, no changes to production candidates.'},ensure_ascii=False,indent=2)+'\n')
print(out)
