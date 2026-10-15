"""Copy original read-only inputs and build QA-only NN comparison boards."""
from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slugs=['luoshan','ruiyin','vasen','yaduo']; paths={str((P/'campaign_roster.json').relative_to(R)):'campaign roster','AGENTS.md':'repository rules','design/AGENTS.md':'design rules'}
for s in slugs:
 m=json.loads((P/s/'sources/source_manifest.json').read_text())
 for x in m.get('items',m.get('sources',[])): paths[x.get('original_path',x.get('source'))]=x['role']
rows=[]
for path,role in sorted(paths.items()):
 src=R/path;dst=Q/'source_snapshots'/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 assert src.read_bytes()==dst.read_bytes()
 rows.append({'path':path,'role':role,'snapshot':str(dst.relative_to(Q)),'sha256':sha(src),'bytes':src.stat().st_size})
(Q/'independent_source_manifest.json').write_text(json.dumps({'checked_utc':datetime.now(timezone.utc).isoformat(),'independent_original_file_count':len(rows),'sources':rows},ensure_ascii=False,indent=2)+'\n')
board=Image.new('RGB',(1216,420),(78,78,78));d=ImageDraw.Draw(board)
for i,s in enumerate(['mara','iwo','leiya','tore']):
 im=Image.open(P/'luoshan/sources'/f'{s}_style_reference.png').convert('RGBA').resize((296,400),Image.Resampling.NEAREST)
 board.paste(im,(i*304,20),im);d.text((i*304+4,5),s,fill='white')
board.save(Q/'core_style_4x_NN.png')
board=Image.new('RGB',(1200,520),(90,90,90));d=ImageDraw.Draw(board)
for i,s in enumerate(slugs):
 im=Image.open(P/s/'sources/identity_reference.png').convert('RGBA');scale=min(280/im.width,480/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
 board.paste(im,(300*i+(300-im.width)//2,30),im);d.text((300*i+4,8),s,fill='white')
board.save(Q/'mother_overview_NN.png')
print('source files',len(rows))
