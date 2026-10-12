"""Verify saved concept provenance and note associations; no pixel edits or runtime claims."""
from pathlib import Path
from PIL import Image
import json,hashlib,re,os
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(name):return json.loads((ROOT/'research'/name).read_text(encoding='utf-8-sig'))
art=read('city-art-manifest.json');briefs=read('city-art-briefs.json');extra=read('city-art-prompt-additions.json');model=read('city-campaign.json')
records=art['reference_based_boards'];bm={b['id']:b for b in briefs['briefs']};cm={c['id']:c for c in model['cities']}
errors=[];checks=[];dimensions={};linked=[]
def check(ok,label):(checks if ok else errors).append(label)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
check(len(records)==15 and len({r['id'] for r in records})==15,'15-unique-selected-boards')
check(set(cm)==set(bm)=={r['id'] for r in records},'all-designed-territories-covered')
check(art['pending_boards']==[] and art['completed_boards']==15,'no-pending-selected-board')
check((ROOT/'backups/city-art-20261012-015928/design').exists(),'design-backup-preserved')
gallery=V/'12_美术参考/原素材参考与城市概念图.md';text=gallery.read_text(encoding='utf-8')
for r in records:
 cid=r['id'];b=bm[cid];c=cm[cid];out=(ROOT/r['output']).resolve()
 check(out.is_relative_to(V/'12_美术参考/城市概念') and out.exists(),cid+'-project-output')
 check(sha(out)==r['sha256'],cid+'-selected-output-hash')
 try:
  with Image.open(out) as im:
   dimensions[cid]=list(im.size);check(im.format=='PNG' and im.width>im.height and im.width>=1000,cid+'-landscape-png');im.verify()
 except Exception as ex:check(False,cid+'-readable-image: '+str(ex))
 check(bool(b.get('prompt')) and len(b['prompt'])>100,cid+'-full-initial-prompt-recorded')
 check(r.get('status')=='draft' and bool(r.get('review')),cid+'-draft-and-visual-review')
 check(r['city_note']=='design/'+c['file'],cid+'-city-association')
 check(set(r['satellite_notes'])=={'design/'+s['file'] for s in c['satellites']},cid+'-satellite-associations')
 for ref in b['reference_paths']:
  path=Path(ref).resolve();check(path.is_relative_to(ROOT/'stoneshard-assets-sample'),cid+'-user-reference-location-'+path.name)
  check(sha(path)==b['reference_hashes'][path.name],cid+'-original-reference-unchanged-'+path.name)
 check(r['reference_paths']==b['reference_paths'],cid+'-style-origin-recorded')
 if r.get('revised_prompt_id'):
  edit=extra['revisions'][r['revised_prompt_id']]
  check(bool(edit['prompt']) and edit['output']==r['output'],cid+'-full-edit-prompt')
  check(r['actual_generation_reference_paths']==edit['reference_paths'],cid+'-actual-edit-input')
  prior=ROOT/r['previous_output'];check(prior.exists(),cid+'-previous-version-preserved')
  for ref in edit['reference_paths']:
   check(sha(Path(ref))==r['actual_generation_reference_hashes'][ref]==sha(prior),cid+'-edit-input-is-prior-board')
 else:
  check(r['actual_generation_reference_paths']==b['reference_paths'],cid+'-actual-generation-input')
 if r.get('prompt_addition'):check(bool(extra.get(r['prompt_addition'])),cid+'-shared-addition-recorded')
 for note in [r['city_note']]+r['satellite_notes']:
  p=ROOT/note;t=p.read_text(encoding='utf-8');linked.append(note)
  expected=Path(os.path.relpath(out,p.parent)).as_posix()
  check('('+expected+')' in t and '[[原素材参考与城市概念图]]' in t,note+'-current-embed-and-provenance-link')
  check(t.count('<!-- CITY-ART-S74:BEGIN -->')==1,note+'-single-current-art-block')
  if note in r['satellite_notes']:
   sid=p.stem.split('_')[1];check('`'+sid+'`' in t and sid in b['prompt'],sid+'-stable-panel-id-recorded')
 check(Path(os.path.relpath(out,gallery.parent)).as_posix() in text,cid+'-gallery-output')
 check('[['+Path(c['file']).stem+']]' in text and c['main_id'] in text,cid+'-gallery-city-and-task-link')
check(len(linked)==len(set(linked))==48,'48-unique-city-and-satellite-notes-linked')
check(sum(len(c['satellites']) for c in model['cities'])==33,'33-satellite-vignettes-associated')
for p in V.rglob('*.md'):
 for raw in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8-sig')):
  if not raw.startswith(('http:','https:','data:')):check((p.parent/raw).resolve().exists(),str(p.relative_to(V))+'-image-path')
for rel,h in read('city-generated-note-hashes.json').items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S74 image integrity, recorded reference hashes and Obsidian associations; no automatic artistic-quality or game-runtime validation',
 boards=len(records),satellite_vignettes=33,linked_notes=len(linked),dimensions=dimensions,checks_passed=len(checks),errors=errors,passed=not errors)
(ROOT/'research/city-art-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='dimensions'},ensure_ascii=False));raise SystemExit(1 if errors else 0)
