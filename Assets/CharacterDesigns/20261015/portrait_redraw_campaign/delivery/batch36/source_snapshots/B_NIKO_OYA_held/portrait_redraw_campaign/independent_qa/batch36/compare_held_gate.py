"""Same-scale NN-only visual comparator; no portrait pixels modified."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil
Q=Path(__file__).resolve().parent;P=Q.parent.parent
items=[
 ('sune','sune/candidates/portrait_v2_inset_74x100_candidate.png'),
 ('tian','tian/candidates/portrait_v2_containment_74x100_candidate.png'),
 ('niko','niko/candidates/portrait_v2_74x100_candidate.png'),
 ('oya','oya/candidates/portrait_v2_74x100_candidate.png'),
 ('hure HELD','hure/candidates/portrait_v2_74x100_candidate.png'),
 ('xiyou HELD','xiyou/candidates/portrait_v2_inset_74x100_candidate.png'),
 ('meibei HELD','meibei/candidates/portrait_v2_inset_74x100_candidate.png'),
 ('blank',None),
 ('taya ACCEPTED','taya/candidates/portrait_v2_inset_74x100_candidate.png'),
 ('tina ACCEPTED','tina/candidates/portrait_v2_inset_74x100_candidate.png'),
 ('blank',None),('blank',None),
 *[(n,f'sune/sources/{n}_style_reference.png') for n in ['mara','iwo','leiya','tore']]
]
board=Image.new('RGB',(1216,1680),(78,78,78));draw=ImageDraw.Draw(board);rows=[]
for i,(name,path) in enumerate(items):
 if path is None:continue
 f=P/path;im=Image.open(f).convert('RGBA');assert im.size==(74,100)
 x=(i%4)*304;y=(i//4)*420;draw.text((x+4,y+5),name,fill='white');board.paste(im.resize((296,400),Image.Resampling.NEAREST),(x,y+20),im.resize((296,400),Image.Resampling.NEAREST))
 rows.append({'label':name,'path':path,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bbox':im.getchannel('A').getbbox()})
board.save(Q/'comparison_with_held_gate_4x_NN.png')
for name,path in items:
 if path is not None and ('HELD' in name or 'ACCEPTED' in name):
  d=Q/'gate_evidence'/f"{name.split()[0]}_74x100.png";d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/path,d)
for b,s in [('batch24','hure'),('batch25','xiyou'),('batch25','meibei'),('batch25','taya'),('batch25','tina')]:
 f=P/'independent_qa'/b/f'{s}_final_visual_review.json';d=Q/'gate_evidence'/f'{s}_prior_final_visual_review.json';d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,d)
(Q/'gate_comparison_inputs.json').write_text(json.dumps({'integer_NN_factor':4,'items':rows,'not_a_new_generation':True},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rows,ensure_ascii=False,indent=2))
