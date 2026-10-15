from pathlib import Path
import json,hashlib,sys,datetime
W=Path(__file__).resolve().parent; version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'; status=sys.argv[2] if len(sys.argv)>2 else 'awaiting_independent_qa'
load=lambda p:json.loads((W/p).read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest(); entry=load('sources/roster_entry.json')
metrics=load(f'qa/{version}_metrics.json'); selection=metrics['candidate']['path']
files=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']]
manifest={'schema_version':1,'actor_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_portrait':selection,'selected_sha256':sha(W/selection),'status':status,'generation_calls':len(list((W/'raw').glob('*_raw_imagegen.png'))),'max_imagegen_calls':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_preserved':True,'method':'Built-in imagegen substantive redraw; entire-canvas isotropic NEAREST fit, alpha threshold 128 and <=32 visible-color MAXCOVERAGE/no-dither export are derived candidates, not native authored pixel final. No geometry or facial redrawing by script.','color_budget_note':'Temporary working ceiling, not native pixel art approval.','source_manifest':'sources/source_manifest.json','spec_lock':'spec_lock.md','reproduction':[f"python derive_portrait.py {version.removesuffix('_inset')}" + (' inset' if version.endswith('_inset') else ''),f'python finalize_manifest.py {version} {status}'],'assets':[load(str(p.relative_to(W))) for p in sorted((W/'qa').glob('portrait*_metrics.json'))],'files':files}
if status.startswith('held'):
    manifest['held_evidence_portrait']=manifest['selected_portrait']
    manifest['held_evidence_sha256']=manifest['selected_sha256']
    manifest['selected_portrait']=None
    manifest['selected_sha256']=None
    manifest['deliverable_approved']=False
    manifest['historical_fallback_portrait']='candidates/portrait_v1_inset_74x100_candidate.png'
    manifest['historical_fallback_sha256']=sha(W/manifest['historical_fallback_portrait'])
    manifest['hold_reason']='V2 raw left hair contour is clipped at x=0, y=523..534 (12 opaque pixels). Technical containment does not restore source hair. V1 has complete source silhouette but failed style goals; retained as historical fallback only, not approved.'
(W/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
all_files=[p for p in sorted(W.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(W/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(W)}\n' for p in all_files))
print(entry['name'],selection,manifest['selected_sha256'],status)
