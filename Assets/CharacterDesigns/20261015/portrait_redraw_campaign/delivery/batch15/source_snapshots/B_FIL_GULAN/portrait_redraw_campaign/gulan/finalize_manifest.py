from pathlib import Path
import sys,json,hashlib,subprocess
root=Path(sys.argv[1]);selected=sys.argv[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Verify exact deterministic target recreation; generated raw is never altered.
repro=[]
for mfile in sorted((root/'qa').glob('portrait_v*_metrics.json')):
 version=mfile.name.replace('_metrics.json','');target=root/'candidates'/f'{version}_74x100_candidate.png';before=sha(target)
 raw_version = json.loads(mfile.read_text())['raw']['path'].split('/')[-1].replace('_raw_imagegen.png','')
 p=subprocess.run([sys.executable,str(root/'derive_portrait.py'),str(root),raw_version]+(['--safe'] if version.endswith('_safe') else []),text=True,capture_output=True)
 repro.append({'version':version,'exit_code':p.returncode,'before_sha256':before,'after_sha256':sha(target),'exact_match':before==sha(target),'stderr':p.stderr})
 if p.returncode:raise RuntimeError(p.stderr)
(root/'qa/reproducibility.json').write_text(json.dumps(repro,ensure_ascii=False,indent=2))
repo=root
while not (repo/'AGENTS.md').exists():repo=repo.parent
sources=json.loads((root/'sources/source_manifest.json').read_text());checks=[]
for rec in sources:
 original=repo/rec['original_path'];snapshot=root/rec['snapshot_path'];actual=sha(original)
 checks.append({'original_path':rec['original_path'],'expected_sha256':rec['sha256'],'actual_sha256':actual,'snapshot_sha256':sha(snapshot),'unchanged':actual==rec['sha256']==sha(snapshot)})
(root/'qa/source_preservation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
assets=[json.loads(p.read_text()) for p in sorted((root/'qa').glob('portrait_v*_metrics.json'))]
unique_assets=list({a['raw']['path']:a for a in assets}.values())
ledger={'generator':'built-in image_gen__imagegen','successful_generation_calls':len(unique_assets),'maximum_allowed':2,'calls':[{'version':a['raw']['path'].split('/')[-1].replace('_raw_imagegen.png',''),'prompt':'prompts/'+a['raw']['path'].split('/')[-1].replace('_raw_imagegen.png','.json'),'full_return':'tool_returns/'+a['raw']['path'].split('/')[-1].replace('_raw_imagegen.png','.json'),'raw_sha256':a['raw']['sha256']} for a in unique_assets],'manual_painting':False,'old_assets_modified':False,'native_pixel_authored':False}
(root/'qa/generation_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
(root/'selection.json').write_text(json.dumps({'selected_version':selected,'selected_path':f'candidates/{selected}_74x100_candidate.png','selected_sha256':sha(root/'candidates'/f'{selected}_74x100_candidate.png'),'status':'candidate_frozen_pending_independent_qa','not_user_approved':True},ensure_ascii=False,indent=2))
(root/'README.md').write_text(f'''# {root.name} dialogue portrait candidate

Selected: `candidates/{selected}_74x100_candidate.png`.

Imagegen made a substantial new portrait. Raw image and exact tool return are archived. This 74×100 image is an explicitly technical nearest-neighbor and no-dither palette derivative, not native 74×100 pixel authorship and not game-ready/runtime-approved.

The exporter uses one isotropic scalar, inverse mapping destination pixel centers with nearest-neighbor sampling, transparent padding if needed, alpha threshold 128, and a maximum of 32 visible RGB colors through MAXCOVERAGE palette selection with no dithering. For the selected safety variant, the same raw canvas is contained isotropically into a 72×98 region, centered in a transparent 74×100 target. The original v2 derivative is preserved separately. This only supplies an export safety margin and does not redraw or crop the image. It performs no facial drawing, geometry repair, paintover, crop, or smoothing. The 32-color ceiling is a temporary working constraint, not a claim that all project art must use exactly 32 colors.

`previews/{selected}_1x_8x.png` contains 1x dark/gray/light composites and an integer 8x nearest-neighbor preview. Four core references are archived separately as style-only anchors.

Reproduce from the repository root:

`python {root}/derive_portrait.py {root} {selected.replace('_safe','')} {'--safe' if selected.endswith('_safe') else ''}`

Full prompts/parameters: `prompts/`. Full responses: `tool_returns/`. Raw outputs: `raw/`. Current cards, old identity, QA, manifests, story constraints and SHA registry: `sources/`. Identity, technical checks, deterministic rerun and preservation checks: `qa/`.

Two calls maximum: first draft and one targeted correction. Previous assets, cards, implementation code and global indexes remain unchanged. No commit/push or runtime integration was performed.
''')
files=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]
manifest={'actor_id':'MAE-NPC-'+root.name.upper(),'name':'菲勒·火' if root.name=='fil' else '古岚','date':'2026-10-15','stage':'candidate_frozen_pending_independent_qa','selected_portrait':f'candidates/{selected}_74x100_candidate.png','selected_sha256':sha(root/'candidates'/f'{selected}_74x100_candidate.png'),'generation_calls':len(unique_assets),'max_attempts':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'independent_qa':'pending','method':ledger,'assets':assets,'source_preservation_all_pass':all(x['unchanged'] for x in checks),'reproducibility_all_pass':all(x['exact_match'] for x in repro),'files':files}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({k:manifest[k] for k in ['actor_id','selected_portrait','selected_sha256','generation_calls','source_preservation_all_pass','reproducibility_all_pass']},ensure_ascii=False))
