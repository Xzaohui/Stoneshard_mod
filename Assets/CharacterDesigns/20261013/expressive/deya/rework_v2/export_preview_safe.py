from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p/'deya_rework_v2_raw_imagegen.png';im=Image.open(s).convert('RGBA');old=list(im.getdata());new=[(0,0,0,0) if x[3]<16 else x for x in old];im.putdata(new);f=p/'deya_rework_v2_preview_safe.png';im.save(f)
assert all(a==b for a,b in zip(old,new) if a[3]>=16)
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
(p/'preview_safe.json').write_text(json.dumps({'source':s.name,'source_sha256':sha(s),'output':f.name,'sha256':sha(f),'operation':'Clear only RGBA pixels with alpha<16; all alpha>=16 pixels byte-identical','changed_pixels':sum(a!=b for a,b in zip(old,new)),'concept_only':True,'equipment_compatibility_verified':False},indent=2)+'\n')
