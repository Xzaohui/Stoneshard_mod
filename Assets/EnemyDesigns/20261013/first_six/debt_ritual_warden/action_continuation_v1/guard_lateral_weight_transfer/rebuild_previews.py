from pathlib import Path
from PIL import Image
import json,base64,io
d=Path(__file__).resolve().parent
a=json.loads((d/'tool_return_v1.json').read_text())
raw=base64.b64decode(a['image_url'].split(',',1)[1])
im=Image.open(io.BytesIO(raw)).convert('RGBA')
for name,color in [('light',(233,229,215,255)),('dark',(35,39,47,255))]:
    canvas=Image.new('RGBA',im.size,color)
    canvas.alpha_composite(im)
    canvas.convert('RGB').save(d/f'rebuilt_preview_{name}.png')
print('Only preview composites written; original pixels and alpha unchanged.')
