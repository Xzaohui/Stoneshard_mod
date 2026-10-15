from pathlib import Path
import json,hashlib,datetime,base64,subprocess,sys
root=Path(__file__).resolve().parent
repo=root.parents[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
selected=sys.argv[1]
review=json.loads((root/'qa/visual_self_review.json').read_text())
sources=json.loads((root/'sources/source_manifest.json').read_text())
source_checks=[]
for s in sources['sources']:
 p=repo/s['source'];c=root/s['copy']
 source_checks.append({'source':s['source'],'expected_sha256':s['sha256'],'current_sha256':sha(p),'copy_sha256':sha(c),'matches':sha(p)==sha(c)==s['sha256']})
before={str(p.relative_to(root)):sha(p) for p in (root/'candidates').glob('*.png')}
subprocess.run([sys.executable,str(root/'derive_portrait.py')],check=True,capture_output=True)
for v in sorted((root/'raw').glob('portrait_v*_raw_imagegen.png')):
 name=v.stem.replace('_raw_imagegen','');subprocess.run([sys.executable,str(root/'export_maxcoverage.py'),name],check=True,capture_output=True)
after={str(p.relative_to(root)):sha(p) for p in (root/'candidates').glob('*.png')}
returns=[]
for p in sorted((root/'tool_returns').glob('portrait_v*.json')):
 x=json.loads(p.read_text());raw=root/'raw'/f'{p.stem}_raw_imagegen.png'
 returns.append({'return':str(p.relative_to(root)),'raw':str(raw.relative_to(root)),'raw_sha256':sha(raw),'full_return_sha256':sha(p),'bytes_match':base64.b64decode(x['image_url'].split(',',1)[1])==raw.read_bytes()})
validation={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reproducibility':{'candidate_before':before,'candidate_after':after,'all_identical':before==after},'source_integrity':source_checks,'all_source_hashes_match':all(x['matches'] for x in source_checks),'raw_tool_return_integrity':returns,'all_raw_return_bytes_match':all(x['bytes_match'] for x in returns)}
(root/'qa/reproducibility_and_source_integrity.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
entry=json.loads((root/'sources/roster_entry.json').read_text());metric=json.loads((root/'qa'/f'{selected}_metrics.json').read_text())
m={'schema_version':1,'canonical_id':entry['canonical_id'],'name':entry['name'],'slug':entry['suggested_slug'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'portrait_candidate_pending_parent_final_audit','selected_candidate':f'candidates/{selected}_74x100_candidate.png','selected_candidate_sha256':sha(root/'candidates'/f'{selected}_74x100_candidate.png'),'selected_raw':metric['raw']['path'],'selected_raw_sha256':metric['raw']['sha256'],'selection_reason':review['selection_reason'],'generation':{'mode':'built-in image_gen substantive portrait redraw','attempts':len(returns),'model':'not exposed by built-in tool','size_control':'prompt aspect ratio only; actual raw size recorded in metrics','parameters':[str(p.relative_to(root)) for p in sorted((root/'prompts').glob('portrait_v*.json'))],'complete_tool_returns':[x['return'] for x in returns]},'identity_lock':'spec_lock.md','source_manifest':'sources/source_manifest.json','method':{'native_authored_74x100':False,'native_pixel_approved':False,'runtime_integrated':False,'description':'Substantive imagegen redraw then entire-canvas NEAREST resize to 74x100, alpha threshold 128, opaque-color quantization <=32 and zero RGB for transparency. Not native pixel authorship.','derivation':metric['derivation'],'color_budget_is_temporary':True,'no_manual_pixel_repainting':True},'qa':{'technical':f'qa/{selected}_metrics.json','visual_author':'qa/visual_self_review.json','source_and_reproduction':'qa/reproducibility_and_source_integrity.json','independent_qa':'../independent_qa/batch09/'},'previews':{'one_x':f'candidates/{selected}_74x100_candidate.png','eight_x':f'previews/{selected}_8x.png','review_board':f'previews/{selected}_1x_8x.png'},'old_assets_preserved':True,'cards_and_code_changed':False,'commit_or_push_performed':False,'limitations':['Concept dialogue portrait candidate only, not game-integrated or runtime accepted.','Palette is provisional; numerical compliance does not prove visual or native-pixel acceptance.'],'files':[]}
for p in sorted(root.rglob('*')):
 if p.is_file() and p.name not in ['manifest.json','SHA256SUMS']: m['files'].append({'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size})
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(root/'SHA256SUMS').write_text(''.join(sha(p)+'  '+str(p.relative_to(root))+'\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
print(json.dumps({'slug':entry['suggested_slug'],'selected':m['selected_candidate'],'sha256':m['selected_candidate_sha256'],'sources_ok':validation['all_source_hashes_match'],'reproducible':before==after,'returns_ok':validation['all_raw_return_bytes_match']},ensure_ascii=False))
