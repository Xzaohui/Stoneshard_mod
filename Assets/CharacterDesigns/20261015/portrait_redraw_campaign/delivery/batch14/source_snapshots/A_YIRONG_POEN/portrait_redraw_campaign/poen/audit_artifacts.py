from pathlib import Path
from PIL import Image
import json,hashlib,subprocess,sys
root=Path(__file__).resolve().parent
repo=next(p for p in root.parents if (p/'AGENTS.md').exists())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((root/'sources/source_manifest.json').read_text())['sources'];checks=[]
for s in sources:
 original=repo/s['original_path'];snapshot=root/s['snapshot_path'];checks.append({'original_path':s['original_path'],'snapshot_path':s['snapshot_path'],'expected_sha256':s['sha256'],'current_original_sha256':sha(original),'snapshot_sha256':sha(snapshot),'original_unchanged':sha(original)==s['sha256'],'snapshot_identical':sha(snapshot)==s['sha256']})
files=sorted((root/'candidates').glob('*.png'))+sorted((root/'previews').glob('*.png'));before={str(p.relative_to(root)):sha(p) for p in files}
run=subprocess.run([sys.executable,str(root/'derive_portrait.py')],capture_output=True,text=True)
after={f:sha(root/f) for f in before};repro=[{'path':f,'before_sha256':before[f],'after_sha256':after[f],'identical':before[f]==after[f]} for f in before]
raw_edges=[]
for p in sorted((root/'raw').glob('*.png')):
 im=Image.open(p).convert('RGBA');a=im.getchannel('A').point(lambda x:255 if x>=128 else 0);bbox=a.getbbox();m=[bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3]] if bbox else None
 raw_edges.append({'path':str(p.relative_to(root)),'size':im.size,'alpha_128_bbox':bbox,'alpha_128_margins_left_top_right_bottom':m,'raw_touches_edge':bool(m and min(m)==0),'note':'A zero margin can indicate cropping; a positive margin is not proof of complete anatomy. Inspect visually.'})
result={'source_integrity':checks,'all_sources_unchanged':all(x['original_unchanged'] and x['snapshot_identical'] for x in checks),'reproduction_exit_code':run.returncode,'reproduction':repro,'all_exports_identical':run.returncode==0 and all(x['identical'] for x in repro),'raw_margin_analysis':raw_edges,'scope':'No source, old asset, card or runtime file written. SHA checks are technical evidence, not visual approval.'}
(root/'qa/reproducibility_and_source_integrity.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'slug':root.name,'sources_unchanged':result['all_sources_unchanged'],'exports_reproduce':result['all_exports_identical'],'raw_edges':raw_edges}))
