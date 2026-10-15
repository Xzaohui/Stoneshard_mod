from pathlib import Path
import json,hashlib,sys
r=Path(__file__).resolve().parent
v=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1_maxcoverage'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entry=json.loads((r/'sources/roster_entry.json').read_text())
qa=r/'qa/independent_review.json'
sel=r/'candidates'/f'{v}_74x100_candidate.png'
assert sel.exists()
files=[{'path':str(p.relative_to(r)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(r.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']]
m={'schema_version':1,'actor_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_portrait':str(sel.relative_to(r)),'selected_sha256':sha(sel),'status':'independent_visual_pass_candidate_awaiting_batch_hash_audit','generation_calls':len(list((r/'tool_returns').glob('portrait_v*.json'))),'max_attempts':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'independent_qa':'../independent_qa/batch07/FINAL_SELECTION.json','independent_technical_audit':'../independent_qa/batch07/technical_audit.json','independent_feedback_record':'qa/independent_feedback_record.json','independent_final_artifacts_pending_at_freeze':True,'old_assets_preserved':True,'method':'Built-in imagegen substantive redraw. Entire-canvas NEAREST resize, binary alpha threshold 128 and no-dither 32-color quantization are explicitly derived candidates, not native authored pixel finals. No geometry redrawn by script.','color_budget_note':'At most 32 visible RGB colors is a temporary working ceiling, not proof of native pixel art.','source_manifest':'sources/source_manifest.json','spec_lock':'spec_lock.md','reproduction':['python derive_portrait.py']+['python export_maxcoverage.py '+p.stem.replace('_maxcoverage_metrics','') for p in sorted((r/'qa').glob('portrait_v*_maxcoverage_metrics.json'))]+['python finalize_manifest.py '+v],'assets':[json.loads(p.read_text()) for p in sorted((r/'qa').glob('portrait_v*_metrics.json'))],'selected_metrics':'qa/'+v+'_metrics.json','files':files}
if qa.exists():
 q=json.loads(qa.read_text());m['independent_review_decision']=q.get('decision',q.get('status'))
(r/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
paths=[p for p in sorted(r.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(r/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(r))+'\n' for p in paths))
print(json.dumps({'slug':r.name,'selected':str(sel),'sha256':sha(sel),'files':len(paths),'status':m['status']}))
