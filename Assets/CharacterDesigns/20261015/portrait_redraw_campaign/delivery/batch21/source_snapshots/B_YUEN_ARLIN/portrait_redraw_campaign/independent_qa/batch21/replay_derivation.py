#!/usr/bin/env python3
"""Replay the fully reviewed, digest-locked author script only inside this QA folder."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
REVIEWED_SCRIPT_SHAS=('338febc664682900e78901a9b6ecb24df118d9d0de3e66b82c1a7859fce0e4c4',)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_read_before_execution':True,'allowed_script_sha256':REVIEWED_SCRIPT_SHAS,'inputs_read_only':True,'sandbox':'independent_qa/batch21/replay','actors':{},'errors':[]}
for slug in ('tafei', 'xielan', 'yuen', 'arlin'):
 source=CAMP/slug; destination=OUT/'replay'/slug
 script=source/'derive_portrait.py'
 if not script.exists():
  report['errors'].append(slug+': script not ready');continue
 if sha(script) not in REVIEWED_SCRIPT_SHAS:
  report['errors'].append(slug+': script changed; must be read before execution');continue
 destination.mkdir(parents=True,exist_ok=True)
 shutil.copy2(script,destination/script.name)
 for folder in ('raw','tool_returns','candidates','previews','qa'):(destination/folder).mkdir(exist_ok=True)
 versions=[]
 for file in sorted((source/'candidates').glob('*_74x100_candidate.png')):
  tag=file.stem.removesuffix('_74x100_candidate'); version=tag.removesuffix('_inset').removesuffix('_safe'); profile='safe' if tag.endswith('_safe') else ('inset' if tag.endswith('_inset') else 'full')
  for folder,name in [('raw',version+'_raw_imagegen.png'),('tool_returns',version+'.json')]:
   shutil.copy2(source/folder/name,destination/folder/name)
  proc=subprocess.run([sys.executable,str(destination/script.name),version,profile],capture_output=True,text=True)
  checks=[]
  for folder,names in [('candidates',[tag+'_74x100_candidate.png']),('previews',[tag+'_1x.png',tag+'_8x.png',tag+'_1x_backgrounds.png',tag+'_4x_backgrounds.png']),('qa',[tag+'_metrics.json'])]:
   for name in names:
    orig=source/folder/name; test=destination/folder/name
    ok=orig.exists() and test.exists() and orig.read_bytes()==test.read_bytes()
    checks.append({'path':folder+'/'+name,'source_sha256':sha(orig) if orig.exists() else None,'replay_sha256':sha(test) if test.exists() else None,'byte_identical':ok})
    if not ok:report['errors'].append(slug+': replay mismatch '+folder+'/'+name)
  versions.append({'version':tag,'command':['python','derive_portrait.py',version,profile],'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'checks':checks})
  if proc.returncode:report['errors'].append(slug+': replay failed '+tag)
 report['actors'][slug]={'script_sha256':sha(script),'versions':versions}
report['pass']=not report['errors']
path=OUT/(sys.argv[1] if len(sys.argv)>1 else 'derivation_replay.json')
path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pass':report['pass'],'errors':report['errors'],'versions':{k:len(v['versions']) for k,v in report['actors'].items()}},ensure_ascii=False))
