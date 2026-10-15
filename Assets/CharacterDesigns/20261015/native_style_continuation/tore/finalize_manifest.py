"""Finalize traceability after candidate selection; this script writes no images."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
leiya=root.name=='leiya'
selected='portrait_v2_maxcoverage' if leiya else 'portrait_v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=root/'manifest.json';d=json.loads(p.read_text())
d['selected_portrait']=f'candidates/{selected}_74x100_candidate.png'
d['selected_portrait_sha256']=sha(root/d['selected_portrait'])
d['selected_preview']=f'previews/{selected}_1x_8x.png'
d['independent_qa']={'selection_status':'candidate_selected_after_independent_visual_review','native_art_final_approved':False,'runtime_verified':False,'formal_measurement_report':'maintained separately by independent reviewer in parent continuation task','review_summary_file':'qa/independent_selection_summary.json'}
d['generation_calls']=2 if leiya else 1
d['image_generation_frozen']=True
d['source_files_frozen_for_delivery']=True
d['selected_export']={'version':'v2' if leiya else 'v1','palette_method':'Pillow MAXCOVERAGE' if leiya else 'Pillow MEDIANCUT','dither':False,'resize':'whole-canvas NEAREST to 74x100','alpha_threshold':128,'shape_painting':False,'native_pixel_authorship_claim':False}
if leiya:
 d['mechanical_export_alternative']=json.loads((root/'qa/portrait_v2_maxcoverage_metrics.json').read_text())
 d['earlier_exports_retained']=['candidates/portrait_v1_74x100_candidate.png','candidates/portrait_v2_74x100_candidate.png']
d['files']=[{'path':str(x.relative_to(root)),'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(root.rglob('*')) if x.is_file() and x.name not in ('manifest.json','SHA256SUMS.txt')]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(x)}  {x.relative_to(root)}' for x in sorted(root.rglob('*')) if x.is_file() and x.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'name':root.name,'selected':d['selected_portrait'],'candidate_sha256':d['selected_portrait_sha256'],'manifest_sha256':sha(p),'files':len(d['files'])},ensure_ascii=False))
