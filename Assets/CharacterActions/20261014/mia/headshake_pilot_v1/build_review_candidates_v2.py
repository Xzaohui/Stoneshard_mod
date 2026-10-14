from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,base64
d=Path(__file__).resolve().parent
files=[d/'sources/4_mia_ratio_1_to_1_5_v2_raw_imagegen.png',d/'raw/K1_v1.png',d/'raw/K2_v2.png',d/'raw/K3_v2.png']
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
rows=[]
for p in (d/'raw').glob('*.png'):
 rr=d/'returns'/f'{p.stem}.json';b=base64.b64decode(json.loads(rr.read_text())['image_url'].split(',')[1]);assert b==p.read_bytes()
 params=d/'prompts'/f'{p.stem}.params.json';prompt=d/'prompts'/f'{p.stem}.txt';assert json.loads(params.read_text())['prompt'].rstrip('\n')==prompt.read_text().rstrip('\n')
 rows.append({'raw':str(p.relative_to(d)),'sha256':hashlib.sha256(b).hexdigest(),'return':str(rr.relative_to(d)),'payloadMatch':True,'params':str(params.relative_to(d)),'paramsSavedBeforeReturn':params.stat().st_mtime<rr.stat().st_mtime,'size':Image.open(p).size})
(d/'PROVENANCE_VERIFICATION.json').write_text(json.dumps(rows,indent=2))
labels=['K0 起势｜复用母图','K1 轻摇头｜新绘左转','K2 反向｜新绘近正面','K3 回稳｜新绘收势']
for theme,bg,fg in [('light',(233,229,218),(35,37,43)),('dark',(32,37,46),(239,235,222))]:
 board=Image.new('RGB',(2240,800),bg);draw=ImageDraw.Draw(board)
 for i,p in enumerate(files):
  im=Image.open(p).convert('RGBA');im=im.resize((559,704),Image.Resampling.NEAREST)
  board.paste(im,(i*560,48),im);draw.text((i*560+16,12),labels[i],font=font,fill=fg)
 draw.text((18,763),'米娅抱毯轻摇头·四阶段小样｜3张新绘＋1张母图复用｜非完整循环，仍有细微重绘漂移',font=font,fill=fg)
 board.save(d/f'mia_headshake_candidates_v2_{theme}_zh.png')
print('candidate v2 review ready')
