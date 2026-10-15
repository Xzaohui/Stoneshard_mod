from pathlib import Path
import json,hashlib,sys,datetime
W=Path(__file__).resolve().parent; version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'; status=sys.argv[2] if len(sys.argv)>2 else 'awaiting_independent_qa'
load=lambda p:json.loads((W/p).read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); entry=load('sources/roster_entry.json')
metrics=load(f'qa/{version}_metrics.json'); selection=metrics['candidate']['path']
files=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']]
manifest={'schema_version':1,'actor_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_portrait':selection,'selected_sha256':sha(W/selection),'status':status,'generation_calls':len(list((W/'raw').glob('*_raw_imagegen.png'))),'max_imagegen_calls':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_preserved':True,'method':'Built-in imagegen substantive redraw; entire-canvas isotropic NEAREST fit, alpha threshold 128 and <=32 visible-color MAXCOVERAGE/no-dither export are derived candidates, not native authored pixel final. No geometry or facial redrawing by script.','color_budget_note':'Temporary working ceiling, not native pixel art approval.','source_manifest':'sources/source_manifest.json','spec_lock':'spec_lock.md','reproduction':[f"python derive_portrait.py {version.removesuffix('_inset')}" + (' inset' if version.endswith('_inset') else ''),f'python finalize_manifest.py {version} {status}'],'assets':[load(str(p.relative_to(W))) for p in sorted((W/'qa').glob('portrait*_metrics.json'))],'files':files}
manifest['generation_successes'] = manifest['generation_calls']
manifest['preflight_validation_failures'] = len(list((W/'tool_returns').glob('*_validation_error.json')))
manifest['tool_invocations'] = manifest['generation_calls'] + manifest['preflight_validation_failures']
manifest['independent_review'] = 'qa/independent_review_acceptance.json'
manifest['no_third_generation'] = True
(W/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
all_files=[p for p in sorted(W.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(W/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(W)}\n' for p in all_files))
print(entry['name'],selection,manifest['selected_sha256'],status)
