from pathlib import Path
import hashlib,json,zipfile
D=Path(__file__).resolve().parent;E=D.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
files=[]
for c in ['nell','sel']:
 o=E/c/'turnaround_v1'
 assert (o/'FINAL_STATUS.json').exists(),f'{c}: FINAL_STATUS missing'
 m=json.loads((o/'manifest.json').read_text())
 for f in m['files']:assert sha((o/f['path']).read_bytes())==f['sha256']
 files += sorted(p for p in o.rglob('*') if p.is_file())
files += [D/'nell_sel_turnaround_joint_zh_light.png',D/'build_joint.py',D/'package.py']
zp=D/'nell_sel_turnaround_v1_complete.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,str(p.relative_to(E)))
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 members=[]
 for p in files:
  n=str(p.relative_to(E));info=z.getinfo(n);b=z.read(n);assert b==p.read_bytes()
  members.append({'member':n,'bytes':info.file_size,'crc32':f'{info.CRC:08x}','sha256':sha(b)})
assert zp.stat().st_size<18*1024*1024
report={'zip':zp.name,'bytes':zp.stat().st_size,'sha256':sha(zp.read_bytes()),'member_count':len(members),'crc_test':'pass','disk_vs_member_bytes':'all_equal','members':members}
(D/'PACKAGE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='members'},indent=2))
