from pathlib import Path
import json,hashlib,sys
from PIL import Image
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slug=root.name;selected=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1';roster=json.loads((root/'sources/roster_entry.json').read_text())
qa_path=root/'qa/independent_selection_summary.json'
independent=json.loads(qa_path.read_text()) if qa_path.exists() else {'status':'pending','native_pixel_final_approved':False}
source=json.loads((root/'sources/source_manifest.json').read_text())
repo=root.parents[4]
source_verification=[]
for r in source['sources']:
 snapshot=root/r['snapshot']; live=repo/r['source']
 source_verification.append({'source':r['source'],'snapshot':r['snapshot'],'snapshot_hash_match':sha(snapshot)==r['sha256'],'live_hash_match':live.exists() and sha(live)==r['sha256']})
(root/'qa/source_verification.json').write_text(json.dumps(source_verification,ensure_ascii=False,indent=2))
reports=[json.loads(p.read_text()) for p in sorted((root/'qa').glob('portrait_v*_metrics.json'))]
out=root/'candidates'/f'{selected}_74x100_candidate.png'
m={'schema_version':1,'canonical_id':roster['canonical_id'],'name':roster['name'],'date':'2026-10-15','status':'candidate_selected' if qa_path.exists() else 'candidate_pending_independent_qa','selected_portrait':str(out.relative_to(root)),'selected_portrait_sha256':sha(out),'selected_preview':f'previews/{selected}_1x_8x.png','generation_calls':len(reports),'max_attempts':2,'successful_image_generations':len(reports),'input_validation_failures_without_image':1,'input_validation_failure_record':'tool_returns/portrait_v2_input_validation.json','imagegen_tool':'tools.image_gen__imagegen','generation_mode':'built-in reference-guided substantive redraw; one call per version','native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'image_generation_frozen':True,'selected_export_frozen':True,'source_identity_master':source['selected_identity_master'],'latest_card_priority':True,'independent_qa':independent,'method':'Raw and full tool return retained. Explicit whole-canvas nearest-neighbor 74x100 scaling, MEDIANCUT temporary 32-color palette and alpha >= 128 binary export. No manually drawn character geometry.','color_budget_note':'32 visible RGB colors is this batch temporary ceiling only. Quantization is not proof of authored ramps or native pixel final.','generation_reproducibility':'Exact tool arguments and full tool returns preserved; generative model calls are not guaranteed byte-deterministic. Export is reproducible from saved raw/tool returns using derive_portrait.py.','pillow_version':Image.__version__,'assets':reports,'scope_boundaries':['No source card, historical image, old selection, code, runtime asset, git commit or push changed.','This selected candidate is not user final approval or engine integration.'],'files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]}
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(slug,'sources all match',all(x['snapshot_hash_match'] and x['live_hash_match'] for x in source_verification),'selected',sha(out))
