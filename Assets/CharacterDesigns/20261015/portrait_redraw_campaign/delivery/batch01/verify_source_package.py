from pathlib import Path
import sys,json,hashlib,zipfile
p=Path(sys.argv[1])
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None,'ZIP CRC failed'
 inv=json.loads(z.read('package_inventory.json'))
 for x in inv['files']:
  data=z.read(x['path'])
  assert len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'],x['path']
 print('PASS:',p.name,len(inv['files']),'file hashes; all ZIP CRCs')
