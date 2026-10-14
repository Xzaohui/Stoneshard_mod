from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,base64
d=Path(__file__).resolve().parent
files=[d/'sources/4_mia_ratio_1_to_1_5_v2_raw_imagegen.png',d/'raw/K1_v1.png',d/'raw/K2_v2.png',d/'raw/K3_v1.png']
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
rows=[]
for p in (d/'raw').glob('*.png'):
 rr=d/'returns'/f'{p.stem}.json';b=base64.b64decode(json.loads(rr.read_text())['image_url'].split(',')[1]);assert b==p.read_bytes()
 params=d/'prompts'/f'{p.stem}.params.json';prompt=d/'prompts'/f'{p.stem}.txt';assert json.loads(params.read_text())['prompt'].rstrip('\n')==prompt.read_text().rstrip('\n')
 rows.append({'raw':str(p.relative_to(d)),'sha256':hashlib.sha256(b).hexdigest(),'return':str(rr.relative_to(d)),'payloadMatch':True,'params':str(params.relative_to(d)),'paramsSavedBeforeReturn':params.stat().st_mtime<rr.stat().st_mtime,'size':Image.open(p).size})
(d/'PROVENANCE_VERIFICATION.json').write_text(json.dumps(rows,indent=2))
labels=['K0 / REUSED MOTHER','K1 / NEW / TURN LEFT','K2 / NEW / REVERSE','K3 / NEW / SETTLE']
for theme,bg,fg in [('light',(233,229,218),(35,37,43)),('dark',(32,37,46),(239,235,222))]:
 board=Image.new('RGB',(2240,800),bg);draw=ImageDraw.Draw(board)
 for i,p in enumerate(files):
  im=Image.open(p).convert('RGBA');im=im.resize((559,704),Image.Resampling.NEAREST)
  board.paste(im,(i*560,48),im);draw.text((i*560+16,12),labels[i],font=font,fill=fg)
 draw.text((18,763),'4-stage concept pilot | 3 new + 1 reused | NOT a complete loop | slight redraw drift remains',font=font,fill=fg)
 board.save(d/f'mia_headshake_review_{theme}.png')
(d/'CALL_RECORD.md').write_text('''# Image generation call record\nFour serial built-in image_gen__imagegen calls: K1_v1, K2_v1, K2_v2 (sole hard-error correction for reversed braid/hair), K3_v1. K1/K2/K3 v1 exact params were loaded with exec_command cat then JSON.parse and passed unmodified to the tool. K2_v2 appended a targeted correction to K2_v1 in memory, saved that object as params and text before passing the same object to the tool. The spec lock was reread before every call.\n\nFull tool-return objects are in returns/, including complete image_url base64 payload and output_hint. Tool returns do not include server parameter echoes. PROVENANCE_VERIFICATION.json independently decodes payload and checks raw bytes and saved prompt/params equality; pre-call params are author-side records. K1 first shell-based return-save attempt hit OS argument-length limit, then the same stored return was saved with apply_patch; there was no extra generation.\n\nNo script drawing, body movement, compositing heads, deformation or interpolation. Boards use entire raw canvases with the same 1/2 nearest-neighbor scale. No per-frame fitting or aligning. Raw generated alpha retained. All failed candidates retained.\n''')
print('review ready')
