from PIL import Image
import numpy as np,json
from pathlib import Path
p=Path(__file__).parent
palette={'.':'00000000','X':'18141aff','h':'292025ff','H':'493630ff','j':'654b3cff','s':'aa5847ff','S':'dc7c62ff','p':'f2a17bff','P':'ffc096ff','o':'303021ff','O':'4d4b32ff','g':'65613fff','G':'80764cff','b':'48281fff','B':'71422dff','l':'97613bff','L':'bd8646ff','a':'773c12ff','A':'bd6b1dff','t':'e1a650ff','c':'e4c994ff'}
a=np.array(Image.open(p/'native_nearest_base.png')); keys=list(palette)[1:]; colors=np.array([tuple(bytes.fromhex(palette[k]))[:3] for k in keys]); out=[]
for row in a:
 out.append(''.join('.' if v[3]<128 else keys[np.argmin(np.sum((colors.astype(float)-v[:3])**2,axis=1))] for v in row))
print('\n'.join(f'{i:02} {x}' for i,x in enumerate(out)));(p/'base_grid.json').write_text(json.dumps({'palette':palette,'rows':out},indent=2)+'\n')
