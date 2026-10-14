from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,hashlib
d=Path(__file__).resolve().parent
cfg=json.loads((d/'build_config.json').read_text())
raw=Image.open(d/cfg['raw']).convert('RGBA')
a=np.array(raw); low=a[:,:,3]<=8
clean=a.copy();clean[low]=0
assert np.array_equal(clean[~low],a[~low])
im=Image.fromarray(clean);im.save(d/cfg['transparent'])
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
for name,bg,fg in [('light','#f4eedf','#302d27'),('dark','#282b2e','#ece8db')]:
 board=Image.new('RGBA',(1200,1600),bg)
 draw=ImageDraw.Draw(board);draw.text((50,28),cfg['name']+' · 静态概念',font=ImageFont.truetype(font,38),fill=fg)
 draw.text((50,86),'原创美术候选｜单帧待机｜尚未接入游戏',font=ImageFont.truetype(font,24),fill=fg)
 crop=im.crop(im.getbbox());scale=min(1050/crop.width,1320/crop.height)
 size=(round(crop.width*scale),round(crop.height*scale))
 crop=crop.resize(size,Image.Resampling.NEAREST)
 board.alpha_composite(crop,((1200-size[0])//2,145+(1320-size[1])//2))
 draw.text((50,1536),cfg['caption'],font=ImageFont.truetype(font,23),fill=fg)
 board.convert('RGB').save(d/(cfg['slug']+'_'+name+'_board.png'))
stats={'raw_mode':raw.mode,'size':raw.size,'raw_sha256':hashlib.sha256((d/cfg['raw']).read_bytes()).hexdigest(),'raw_alpha_min':int(a[:,:,3].min()),'raw_alpha_max':int(a[:,:,3].max()),'alpha_zero_pixels':int((a[:,:,3]==0).sum()),'alpha_1_to_8_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum()),'alpha_9_to_254_pixels':int(((a[:,:,3]>8)&(a[:,:,3]<255)).sum()),'alpha_255_pixels':int((a[:,:,3]==255).sum()),'changed_pixels':int(np.any(a!=clean,axis=2).sum()),'alpha_above_8_unchanged':bool(np.array_equal(clean[~low],a[~low])),'body_redraw':False,'quantized':False,'final_bbox':im.getbbox(),'processing':'Only set RGBA=0 where raw alpha<=8. No crop/scale to transparent master; board proportional nearest-neighbor only.'}
(d/'alpha_QA.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
print(json.dumps(stats,ensure_ascii=False))
