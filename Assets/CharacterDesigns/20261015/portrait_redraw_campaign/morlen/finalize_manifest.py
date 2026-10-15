from pathlib import Path
import json, hashlib, sys

root=Path(sys.argv[1]); selected=sys.argv[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((root/'sources/source_manifest.json').read_text())
assets=[json.loads(p.read_text()) for p in sorted((root/'qa').glob('portrait_v*_metrics.json'))]
review_path=root/'qa/independent_selection_summary.json'
review=json.loads(review_path.read_text()) if review_path.exists() else {'status':'pending'}
files=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]
target=root/'candidates'/f'{selected}_74x100_candidate.png'
m={'canonical_id':source['character']['canonical_id'],'name':source['character']['name'],'slug':root.name,'date':'2026-10-15','dispatch_revision':2,'selected_portrait':str(target.relative_to(root)),'selected_portrait_sha256':sha(target),'selected_preview':f'previews/{selected}_1x_8x.png','generation_calls':len(assets),'max_generation_calls':2,'native_authored':False,'runtime_integrated':False,'runtime_verified':False,'image_generation_frozen':review.get('status')!='pending','method':'Built-in imagegen substantial redraw; whole-canvas NEAREST downsample, alpha threshold 128, MAXCOVERAGE <=32 colors without dither. No manual pixel painting or geometry edits.','color_budget_note':'32 colors is only this batch temporary ceiling, not a project-wide art rule.','independent_qa':review,'assets':assets,'files':files}
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'))
print(json.dumps({'root':str(root),'selected':str(target),'sha256':sha(target),'files':len(files)},ensure_ascii=False))
