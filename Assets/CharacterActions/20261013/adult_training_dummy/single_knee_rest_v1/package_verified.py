from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
assert (D/'QA-independent.json').exists(), 'Independent review required before packaging'
assert (D/'FINAL_STATUS.json').exists(), 'Final status required before packaging'
exclude={'single_knee_rest_v1_source_evidence.zip','PACKAGE_VERIFICATION.json','SHA256.json'}
files=sorted(p for p in D.rglob('*') if p.is_file() and p.name not in exclude)
hashes={str(p.relative_to(D)):sha(p.read_bytes()) for p in files}
(D/'SHA256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n')
files.append(D/'SHA256.json')
out=D/'single_knee_rest_v1_source_evidence.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,'single_knee_rest_v1/'+str(p.relative_to(D)))
with zipfile.ZipFile(out) as z:
 bad=z.testzip();assert bad is None,bad
 members=[]
 for info in z.infolist():
  relative=info.filename.split('/',1)[1];actual=sha(z.read(info.filename));assert actual==sha((D/relative).read_bytes())
  members.append({'name':info.filename,'size':info.file_size,'crc32':f'{info.CRC:08x}','sha256':actual})
assert out.stat().st_size<18*1024*1024
report={'zip':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'crc_test':'pass','member_sha256_test':'pass','member_count':len(members),'members':members,'uploaded':False}
(D/'PACKAGE_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
