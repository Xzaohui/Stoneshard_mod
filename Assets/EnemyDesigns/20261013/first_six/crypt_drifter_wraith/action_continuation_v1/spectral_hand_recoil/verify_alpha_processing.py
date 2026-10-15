"""Read-only reproduction of the allowed alpha processing used for v1 outputs.
No drawing, recoloring, thresholding, resizing, or anatomy changes are performed.
"""
from pathlib import Path
from PIL import Image
import base64, json, io, numpy as np

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'Assets/EnemyDesigns/20261013/first_six'
for role,pose in [('canal_tomb_restless','reach_clasp_end'),('crypt_drifter_wraith','spectral_hand_recoil')]:
 d=BASE/role/'action_continuation_v1'/pose
 ret=json.loads((d/'tool_return_v1.json').read_text())
 raw_bytes=base64.b64decode(ret['image_url'].split(',',1)[1])
 assert raw_bytes==(d/f'{role}_{pose}_raw_v1.png').read_bytes()
 raw=Image.open(io.BytesIO(raw_bytes)).convert('RGBA')
 pixels=np.array(raw)
 pixels[pixels[:,:,3]==0,:3]=0
 clean=Image.fromarray(pixels)
 assert np.array_equal(np.array(clean),np.array(Image.open(d/f'{role}_{pose}_transparent_v1.png')))
 for name,color in [('light',(238,235,226,255)),('dark',(29,34,40,255))]:
  bg=Image.new('RGBA',clean.size,color);bg.alpha_composite(clean)
  assert np.array_equal(np.array(bg.convert('RGB')),np.array(Image.open(d/f'review_{name}_v1.png')))
 print(role, 'raw decode, hidden-RGB-only cleanup and two correct RGBA composites verified')
