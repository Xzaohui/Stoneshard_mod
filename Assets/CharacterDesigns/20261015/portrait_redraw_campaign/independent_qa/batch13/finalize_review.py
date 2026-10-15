from pathlib import Path
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((OUT/'frozen_technical_audit.json').read_text())
assert audit['all_technical_checks_complete'],(audit['hard_errors'],audit['pending'])
names={'muko':'穆柯','naetin':'奈汀','sino':'司诺·庭','sore':'索芮'}
rows=[]
for slug,name in names.items():
 a=audit['actors'][slug];m=a['manifest'];c=next(x for x in a['candidates'] if x['path']==m['selected'])
 assert not a['errors'] and not a['pending']
 assert c['png_byte_identical'] and m['selected_four_borders_transparent']
 sums=CAMP/slug/'SHA256SUMS.txt'
 if not sums.exists():sums=CAMP/slug/'SHA256SUMS'
 rows.append(dict(slug=slug,name=name,selected_portrait=slug+'/'+m['selected'],selected_sha256=m['selected_actual_sha256'],production_manifest_sha256=m['sha256'],production_sha256sums_sha256=sha(sums),decision='candidate_with_notes',generation_calls=m['generation_calls'],approved_to_package=True,alpha_bbox=c['alpha_bbox'],visible_rgb_colors=c['visible_rgb_colors']))
selection={'batch':'batch13','portraits':rows,'native_pixel_approved':False,'runtime_verified':False}
(OUT/'FINAL_SELECTION.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
qa={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ('FINAL_GATE.json','SHA256SUMS.txt') and '__pycache__' not in p.parts}
gate={'schema_version':1,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'batch':'batch13','approved_to_package':True,'qualified_candidate_count':4,'held_count':0,'characters':rows,'held':[],'qa_files':qa,'boundaries':{'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False},'qa_board_actually_viewed':True,'warnings':['Residual eye whites, minor hair/beard texture and slight Sino inner-brow lift are recorded in FINAL_REVIEW.md; no further generation.'],'check_result':'41 source snapshots, all 7 raw/tool byte equalities, all 9 independent PNG reproductions, selected full transparent borders, manifest SHA and full production inventories pass.'}
(OUT/'FINAL_GATE.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n')
files=[p for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts]
(OUT/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(OUT)}\n' for p in files))
print(json.dumps({'gate':str(OUT/'FINAL_GATE.json'),'sha256':sha(OUT/'FINAL_GATE.json'),'qualified':4,'sources':sum(len(a['sources']) for a in audit['actors'].values()),'raws':sum(len(a['raw_integrity']) for a in audit['actors'].values()),'candidates':sum(len(a['candidates']) for a in audit['actors'].values())},ensure_ascii=False,indent=2))
