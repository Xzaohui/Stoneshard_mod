from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
M=json.loads((D/'manifest.json').read_text())
for row in M['frozen_files']:
 p=D/row['path']; assert sha(p.read_bytes())==row['sha256'],row['path']
assert (D/'FINAL_STATUS.json').exists()
S=json.loads((D/'FINAL_STATUS.json').read_text());assert S['status']=='passed_independent_review'
assert (D/'QA-independent.json').exists()
zipname='reclined_rest_v1_source_evidence.zip'
excluded={zipname,'PACKAGE_VERIFICATION.json','PACKAGE_CONTENTS.json'}
files=sorted(p for p in D.rglob('*') if p.is_file() and p.name not in excluded and '__pycache__' not in p.parts)
rows=[{'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]
(D/'PACKAGE_CONTENTS.json').write_text(json.dumps({'note':'Exact ZIP payload excluding this inventory itself; verification gives complete exact members including this file.','members':rows},ensure_ascii=False,indent=2))
files.append(D/'PACKAGE_CONTENTS.json');files.sort()
with zipfile.ZipFile(D/zipname,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(D).as_posix())
with zipfile.ZipFile(D/zipname) as z:
 assert z.testzip() is None
 assert z.namelist()==[p.relative_to(D).as_posix() for p in files]
 members=[]
 for p in files:
  n=p.relative_to(D).as_posix();b=z.read(n);assert b==p.read_bytes();members.append({'path':n,'bytes':len(b),'crc32':f'{z.getinfo(n).CRC:08x}','sha256':sha(b)})
assert (D/zipname).stat().st_size<18*1024*1024
report={'status':'verified','zip':zipname,'bytes':(D/zipname).stat().st_size,'sha256':sha((D/zipname).read_bytes()),'crc_test':'pass','exact_member_set':True,'all_member_bytes_match':True,'all_frozen_hashes_match':True,'members':members}
(D/'PACKAGE_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
