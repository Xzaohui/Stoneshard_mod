"""QA-only raw right boundary magnification and multilevel alpha evidence."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;P=Q.parent.parent
for s in ['vila','hepo']:
 p=P/s/'raw/portrait_v2_raw_imagegen.png';im=Image.open(p).convert('RGBA');w,h=im.size;a=im.getchannel('A')
 region=(w-120,350,w,900);crop=im.crop(region)
 board=Image.new('RGB',(120*3*2,550*3),(95,95,95))
 for i,bg in enumerate([(35,35,35),(235,231,220)]):
  tile=Image.new('RGBA',crop.size,(*bg,255));tile.alpha_composite(crop);board.paste(tile.convert('RGB').resize((360,1650),Image.Resampling.NEAREST),(i*360,0))
 board.save(Q/f'{s}_v2_right_edge_3x_NN.png')
 edge=[(y,a.getpixel((w-1,y))) for y in range(h) if a.getpixel((w-1,y))]
 report={'slug':s,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'raw_size':im.size,'right_edge_max_alpha':max([x[1] for x in edge],default=0),'right_edge_nonzero_pixels':edge,'rightmost_twelve_columns_max_alpha':[max(a.getpixel((x,y)) for y in range(h)) for x in range(w-12,w)],'right_edge_crop_region':region,'preview_scale':3,'preview_nearest_neighbor':True,'no_raw_edits':True}
 (Q/f'{s}_v2_boundary_evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(s,report['right_edge_max_alpha'],report['rightmost_twelve_columns_max_alpha'])
