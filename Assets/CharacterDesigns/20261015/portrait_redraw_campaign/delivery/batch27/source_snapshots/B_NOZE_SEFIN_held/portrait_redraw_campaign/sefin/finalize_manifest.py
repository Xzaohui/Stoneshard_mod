from pathlib import Path
import json,hashlib,sys
W=Path(__file__).resolve().parent
load=lambda p:json.loads((W/p).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entry=load('sources/roster_entry.json')
review=load('qa/independent_review_acceptance.json') if (W/'qa/independent_review_acceptance.json').exists() else {}
version=sys.argv[1] if len(sys.argv)>1 else review.get('reviewed_version','portrait_v2')
status=sys.argv[2] if len(sys.argv)>2 else review.get('status','awaiting_final_independent_qa')
metrics=load(f'qa/{version}_metrics.json')
evidence=metrics['candidate']['path']
held=status.startswith('held')
files=[{'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(W.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']]
commands=['python derive_portrait.py portrait_v1','python derive_portrait.py portrait_v2']
if (W/'qa/portrait_v2_inset_metrics.json').exists():commands.append('python derive_portrait.py portrait_v2 inset')
commands.append('python finalize_manifest.py')
manifest={'schema_version':1,'actor_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_portrait':None if held else evidence,'selected_sha256':None if held else sha(W/evidence),'status':status,'deliverable_approved':review.get('deliverable_approved',False),'delivery_eligible':review.get('delivery_eligible',False),'exclude_from_pass_gallery':held,'generation_calls':len(list((W/'raw').glob('*_raw_imagegen.png'))),'max_imagegen_calls':2,'no_further_imagegen':True,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_preserved':True,'tool':'image_gen.imagegen built-in','model_size_quality_seed':'Not exposed; no fabricated values.','method':'Built-in imagegen substantive redraw; entire-canvas isotropic NEAREST fit, alpha threshold 128 and <=32 visible-color MAXCOVERAGE/no-dither export are derived candidates, not native authored pixel final. No geometry or facial redrawing by script. Containment never restores source-clipped hair.','color_budget_note':'Temporary working ceiling, not native pixel art approval.','source_manifest':'sources/source_manifest.json','spec_lock':'spec_lock.md','author_visual_review':'qa/author_visual_review.json','independent_review':'qa/independent_review_acceptance.json' if review else None,'independent_batch_review':'../independent_qa/batch27/','source_integrity':'qa/source_hash_recheck.json','reproduction_audit':'qa/reproducibility.json','raw_edge_audits':['qa/portrait_v1_raw_edges.json','qa/portrait_v2_raw_edges.json'],'reproduction':commands,'limitations':review.get('limitations',[]),'raw_provenance':load('qa/reproducibility.json')['raw_provenance'],'assets':[load(str(p.relative_to(W))) for p in sorted((W/'qa').glob('portrait*_metrics.json'))],'files':files}
if held:manifest.update({'held_evidence_portrait':evidence,'held_evidence_sha256':sha(W/evidence),'hold_reason':review.get('reason','Pending review.')})
(W/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
all_files=[p for p in sorted(W.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(W/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(W)}\n' for p in all_files))
print(entry['name'],manifest['selected_portrait'],manifest['selected_sha256'],status)
