from pathlib import Path
import json,hashlib,sys
W=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v2'
status=sys.argv[2] if len(sys.argv)>2 else 'awaiting_independent_qa'
load=lambda p:json.loads((W/p).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entry=load('sources/roster_entry.json'); metrics=load(f'qa/{version}_metrics.json')
candidate=metrics['candidate']['path']; held=status.startswith('held')
files=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']]
manifest={'schema_version':1,'actor_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_portrait':None if held else candidate,'selected_sha256':None if held else sha(W/candidate),'status':status,'delivery_eligible':False if held else status.startswith('selected_candidate'),'generation_calls':len(list((W/'raw').glob('*_raw_imagegen.png'))),'max_imagegen_calls':2,'generation_closed':True,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_preserved':True,'method':'Built-in imagegen substantive redraw; entire-canvas isotropic NEAREST fit, alpha threshold 128 and <=32 visible-color MAXCOVERAGE/no-dither export are derived candidates, not native authored pixel final. No geometry or facial redrawing by script.','color_budget_note':'Temporary working ceiling, not native pixel art approval.','source_manifest':'sources/source_manifest.json','spec_lock':'spec_lock.md','author_qa':'qa/author_visual_review.json','independent_qa_acceptance':'qa/independent_review_acceptance.json','reproduction':[f"python derive_portrait.py {version.removesuffix('_inset')}"+(' inset' if version.endswith('_inset') else ''),f'python finalize_manifest.py {version} {status}'],'assets':[load(str(p.relative_to(W))) for p in sorted((W/'qa').glob('portrait*_metrics.json'))],'files':files}
if held:
 manifest['held_evidence']={'path':candidate,'sha256':sha(W/candidate),'review_evidence_only':True,'not_a_selected_deliverable':True}
 manifest['held_reason']='V2 retains large bright sclera, cartoon-like eye shape and relatively thin long bare neck despite improved vertical face framing. Inset does not repair these core visual issues; no third generation.'
else:
 manifest['limitations']=['Original subject complete, but tight raw lateral margin (13/11 pixels) remains below requested 2-logical-pixel clearance.','Derived 32-color candidate is not a native hand-authored pixel final.','Minor fine facial color steps and hair striping remain.']
(W/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
all_files=[p for p in sorted(W.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(W/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(W)}\n' for p in all_files))
print(entry['name'],manifest['selected_portrait'],manifest['selected_sha256'],status)
