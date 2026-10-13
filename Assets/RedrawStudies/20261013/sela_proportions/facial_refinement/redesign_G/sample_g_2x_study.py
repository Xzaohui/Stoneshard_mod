from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
raw=Image.open(P/'sela_G_raw_imagegen.png').convert('RGBA');r=np.array(raw)
base=Image.open(P.parent/'before_native.png').convert('RGBA').resize((70,88),Image.Resampling.NEAREST);b=np.array(base);b[:42]=0
# Generated head region, excluding neck/body. Preserve geometry at 34px height.
# Generated blocks are approx 31px; facial shapes include half-grid/curved details.
# Sample small center patches, retaining raw color rather than forced source palette.
source=(278,127,891,650);target=(16,8,56,42)
for y in range(8,42):
 sy=127+(y-8+.5)*(650-127)/34
 for x in range(16,56):
  sx=278+(x-16+.5)*(891-278)/40
  patch=r[max(0,round(sy)-2):round(sy)+3,max(0,round(sx)-2):round(sx)+3]
  if np.median(patch[:,:,3])<128:continue
  solid=patch[patch[:,:,3]>=128];rgb=np.median(solid[:,:3],axis=0).round().astype(np.uint8);b[y,x]=[*rgb,255]
im=Image.fromarray(b);im.save(P/'sela_G_70x88_working_study.png');im.resize((420,528),Image.Resampling.NEAREST).save(P/'sela_G_70x88_working_study_6x.png')
board=Image.new('RGB',(760,750),(180,183,172));d=ImageDraw.Draw(board);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);s=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
d.text((50,18),'G - GENERATED CONCEPT',font=f,fill=(28,28,28));d.text((422,18),'G - 2x WORKING STUDY',font=f,fill=(28,28,28))
sp=raw.resize((280,352),Image.Resampling.LANCZOS);board.paste(sp,(50,55),sp);sp=im.resize((280,352),Image.Resampling.NEAREST);board.paste(sp,(430,55),sp)
sp=raw.crop((247,96,922,681)).resize((300,260),Image.Resampling.LANCZOS);board.paste(sp,(40,440),sp);sp=im.crop((14,6,58,44)).resize((308,266),Image.Resampling.NEAREST);board.paste(sp,(416,440),sp)
d.text((40,720),'Original generated design, not native',font=s,fill=(35,35,35));d.text((416,720),'70 x 88; head 34 px; NOT original native',font=s,fill=(35,35,35));board.save(P/'comparison_Gconcept_G2xstudy.png')
q={'canvas':[70,88],'head_y_span':[8,41],'head_height':34,'body_y_span':[42,75],'body_height':34,'body_exact_nearest_2x':bool(np.array_equal(b[42:],np.array(base)[42:])),'source_head_crop':source,'target_head_rect':target,'sampling':'5x5 center-patch median, alpha>=128, original generated colors retained; no palette mapping','unique_opaque_head_colors':len(np.unique(b[:42][b[:42,:,3]>0],axis=0)),'sha256':hashlib.sha256((P/'sela_G_70x88_working_study.png').read_bytes()).hexdigest()};(P/'QA-G-2xstudy.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
