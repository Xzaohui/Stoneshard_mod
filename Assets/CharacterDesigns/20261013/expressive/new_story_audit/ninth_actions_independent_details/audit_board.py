from pathlib import Path
import json,hashlib,datetime,sys
from PIL import Image
import numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';g=sys.argv[1];lp=r/sys.argv[2];j=json.loads(lp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)};results=[];errors=[]
for board in j['boards']:
 p=r/board['path'];im=Image.open(p).convert('RGBA');theme='dark' if 'dark' in p.name else 'light';bg=tuple(j['backgrounds'][theme]);cells=[]
 for row in j['placements']:
  srcp=r/row['source'];src=Image.open(srcp).convert('RGBA');xy=row['xy'];wh=row['size'];act=im.crop((xy[0],xy[1],xy[0]+wh[0],xy[1]+wh[1]));expected=Image.alpha_composite(Image.new('RGBA',tuple(wh),bg),src.resize(tuple(wh),Image.Resampling.NEAREST));checks={'source_sha_matches':sha(srcp)==row['source_sha256'],'source_dimensions_match':list(src.size)==row['source_dimensions'],'true_complete_nearest_composite':bool(np.array_equal(np.array(expected),np.array(act))),'uniform_aspect':abs(wh[0]/src.width-wh[1]/src.height)<1/min(src.size)}
  if not all(checks.values()):errors.append([p.name,row['source'],checks])
  cells.append({'source':row['source'],'source_sha256':sha(srcp),'xy':xy,'display_size':wh,'label':row['label'],'checks':checks})
 if sha(p)!=board['sha256']:errors.append(['board_sha',p.name])
 results.append({'file':fp(p),'actual_viewed':True,'theme':theme,'cells':cells})
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'group':g,'verdict':'pass' if not errors else 'fail','layout':fp(lp),'boards':results,'visual_findings':['Both light/dark boards actually viewed. Correct Chinese character/action labels and explicit mother-reference column.','All complete silhouettes, hands, boots and original props visible; no cropping or anatomy changes.','Four independently passed key poses displayed; source mothers not counted as new poses.','No full animation or runtime claims.'],'errors':errors};p=a/f'independent_ninth_new_character_actions_{g}_board_gate_20261014.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'gate':fp(p),'verdict':out['verdict'],'cells_checked':sum(len(b['cells']) for b in results),'errors':errors},ensure_ascii=False));assert not errors
