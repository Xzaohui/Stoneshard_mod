from pathlib import Path
import json, base64, hashlib, subprocess, sys
W=Path(__file__).resolve().parent
for v in ['portrait_v1','portrait_v2']:
    payload=json.loads((W/'tool_returns'/f'{v}.json').read_text())
    raw=base64.b64decode(payload['image_url'].split(',',1)[1])
    target=W/'raw'/f'{v}_raw_imagegen.png'
    assert target.read_bytes()==raw, f'{v}: raw differs from complete tool return'
    subprocess.run([sys.executable,str(W/'derive_portrait.py'),v],check=True)
selection='portrait_v2'
subprocess.run([sys.executable,str(W/'finalize_manifest.py'),selection,'selected_candidate_with_limitations'],check=True)
print('Both successful generations re-exported from byte-verified raw; no face or geometry editing.')
