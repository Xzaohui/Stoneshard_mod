#!/usr/bin/env python3
from pathlib import Path,PurePosixPath
import hashlib,json,sys,zipfile,zlib
p=Path(sys.argv[1]); records=[]
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None,'ZIP CRC failed'
    names=z.namelist(); assert len(names)==len(set(names)),'Duplicate ZIP paths'
    assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names),'Unsafe archive path'
    inv=json.loads(z.read('package_inventory.json'))
    expected={x['path'] for x in inv['files']}|{'package_inventory.json','PACKAGE_SHA256SUMS.txt'}
    assert set(names)==expected,'Inventory members mismatch'
    for x in inv['files']:
        b=z.read(x['path']); crc=f'{zlib.crc32(b)&0xffffffff:08x}'; h=hashlib.sha256(b).hexdigest()
        assert len(b)==x['bytes'] and h==x['sha256'] and crc==x['crc32'],x['path']
        assert int(crc,16)==z.getinfo(x['path']).CRC
        records.append({'path':x['path'],'sha256':h,'CRC32':crc,'pass':True})
    for line in z.read('PACKAGE_SHA256SUMS.txt').decode().splitlines():
        h,rel=line.split('  ',1); assert hashlib.sha256(z.read(rel)).hexdigest()==h,rel
print(json.dumps({'file':p.name,'all_CRC_pass':True,'all_SHA256_pass':True,'exact_member_inventory':True,'files':records},ensure_ascii=False,indent=2))
