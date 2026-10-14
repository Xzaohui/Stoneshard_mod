from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'Assets/EnemyDesigns/20261013/first_six'
OUT = Path(__file__).resolve().parent
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(size): return ImageFont.truetype(FONT, size)
board = Image.new('RGBA', (2400, 1660), (246, 244, 238, 255))
draw = ImageDraw.Draw(board)
draw.text((42, 24), '首六敌人动作补缺  ·  003 / 004', font=font(42), fill='#22303a')
draw.text((42, 82), '相邻阶段概念对照｜每阶段浅、深背景并列｜仅等比最近邻排版，旧图未改', font=font(24), fill='#58636b')
roles = [
 ('003  渠墓腐尸', 'canal_tomb_restless', [('拖步（已有）','drag_step','action_v1/drag_step/canal_tomb_restless_drag_step_transparent.png'),('缓慢伸臂（已有）','slow_reach','action_v1/slow_reach/canal_tomb_restless_slow_reach_transparent.png'),('前压扣抓末端（新增）','reach_clasp_end','action_continuation_v1/reach_clasp_end/canal_tomb_restless_reach_clasp_end_transparent_v1.png')]),
 ('004  墓龛游魂', 'crypt_drifter_wraith', [('向前漂移（已有）','forward_drift','action_v1/forward_drift/crypt_drifter_wraith_forward_drift_transparent.png'),('幽影探手（已有）','spectral_reach','action_v1/spectral_reach/crypt_drifter_wraith_spectral_reach_transparent.png'),('探手回束（新增）','spectral_hand_recoil','action_continuation_v1/spectral_hand_recoil/crypt_drifter_wraith_spectral_hand_recoil_transparent_v1.png')])
]
layout=[]
for ri,(title,role,poses) in enumerate(roles):
 y=140+ri*730
 draw.text((42,y), title, font=font(32), fill='#22303a')
 for pi,(label,pose,path) in enumerate(poses):
  x=42+pi*782
  draw.text((x,y+53),label,font=font(27),fill='#22303a')
  draw.text((x,y+88),pose,font=font(18),fill='#58636b')
  p=BASE/role/path
  im=Image.open(p).convert('RGBA')
  assert im.size==(1024,1536)
  # Same full-canvas scale for every image; no alpha-bbox fitting or body edits.
  small=im.resize((360,540),Image.Resampling.NEAREST)
  for bi,(name,col) in enumerate([('浅底',(238,235,226,255)),('深底',(29,34,40,255))]):
   panel=Image.new('RGBA',(374,556),col)
   panel.alpha_composite(small,(7,8))
   board.alpha_composite(panel,(x+bi*378,y+123))
   draw.text((x+bi*378+10,y+130),name,font=font(17),fill=('#6a7277' if bi==0 else '#c8d0d5'))
  layout.append({'role':role,'pose':pose,'source':str(p.relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_size':list(im.size),'display_size':[360,540],'resampling':'nearest','source_modified':False})
draw.text((42,1590),'三阶段不等于完整动画；跨帧相机、尺度、锚点、时间与运行仍未验收。',font=font(26),fill='#6c4638')
board.convert('RGB').save(OUT/'003_004_相邻阶段浅深对照.png')
(OUT/'board_layout.json').write_text(json.dumps({'method':'True RGBA alpha_composite, identical proportional nearest full-canvas scaling','entries':layout},ensure_ascii=False,indent=2)+'\n')
