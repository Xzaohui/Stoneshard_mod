from PIL import Image
from pathlib import Path
import json,hashlib
r=Path.cwd();base=r/'Assets/CharacterActions/20261013/new_story';d=base/'endai/noncombat_basics_v1';out=Image.new('RGB',(2496,1362));panels=[]
for i,(slug,name) in enumerate([('endai','恩岱'),('wadun','瓦顿')]):
 p=base/slug/'noncombat_basics_v1/review'/f'{name}_母图动作浅深对照.png';im=Image.open(p);assert im.size==(1664,1816);s=im.resize((1248,1362),Image.Resampling.NEAREST);out.paste(s,(i*1248,0));panels.append({'source':str(p.relative_to(r)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'render_dimensions':[1248,1362],'uniform_scale':0.75,'resize':'NEAREST','placement_xy':[i*1248,0],'cropped':False,'body_modified':False})
p=d/'review/恩岱_瓦顿_母图动作浅深对照.png';out.save(p);(d/'review/joint_board_layout.json').write_text(json.dumps({'board':str(p.relative_to(r)),'board_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'canvas':[2496,1362],'panels':panels},ensure_ascii=False,indent=2));print(p)
