"""Recover byte-identical PNG from a stored complete built-in imagegen response."""
from pathlib import Path
import json, base64, hashlib, sys
W=Path(__file__).resolve().parent
v=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
r=json.loads((W/'tool_returns'/f'{v}.json').read_text())
png=base64.b64decode(r['image_url'].split(',',1)[1])
out=W/'raw'/f'{v}_raw_imagegen.png'
if out.exists() and out.read_bytes()!=png:
    raise SystemExit('Existing raw differs from stored return; refusing overwrite.')
out.write_bytes(png)
print(hashlib.sha256(png).hexdigest(),out.name)
