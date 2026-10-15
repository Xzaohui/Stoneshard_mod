from pathlib import Path
import json,base64,hashlib,sys
from PIL import Image,ImageDraw
b=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterActions/20261013/new_story');s=sys.argv[1];n=sys.argv[2] if len(sys.argv)>2 else '1';p=b/s/'gap_repair_v2'
r=json.loads((p/f'raw/attempt{n}_tool_return.json').read_text());data=base64.b64decode(r['image_url'].split(',',1)[1]);f=p/f'raw/attempt{n}.png';f.write_bytes(data);(p/f'exports/attempt{n}_transparent.png').write_bytes(data)
im=Image.open(f); assert im.mode=='RGBA'; audit={'raw_sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'size':im.size,'mode':im.mode,'alpha_extrema':im.getchannel('A').getextrema(),'raw_matches_payload':True,'export_identical_to_raw':True,'postprocess':'none'}
for name,c in [('light',(239,234,221,255)),('dark',(33,37,41,255))]: Image.alpha_composite(Image.new('RGBA',im.size,c),im).convert('RGB').save(p/f'review/attempt{n}_{name}.png')
(p/f'review/attempt{n}_byte_audit.json').write_text(json.dumps(audit,indent=2)); print(json.dumps(audit))
