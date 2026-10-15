from pathlib import Path
import shutil,json,hashlib
from PIL import Image,ImageDraw
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); b=r/'Assets/CharacterActions/20261013/new_story'
selected={'turi':1,'cuoer':2,'weier':1,'lier':1}
for s,n in selected.items():
 p=b/s/'gap_repair_v2'; old=b/s/'noncombat_basics_v1'
 shutil.copy2(r/'AGENTS.md',p/'sources/repository_rules_snapshot.txt');shutil.copy2(r/'Assets/CharacterDesigns/20261013/expressive/reference/pixel-asset-master/SKILL.md',p/'sources/pixel_asset_master_snapshot.txt');shutil.copy2('/tmp/process_gap.py',p/'sources/process_gap.py');shutil.copy2('/tmp/setup_gap.py',p/'sources/setup_gap.py')
 for f in [old/'QA-independent.json',old/'review/independent_visual_gate.json',old/'review/independent_sixth_new_character_actions_weier_fouer_visual_gate_20261014.json']:
  if f.exists():shutil.copy2(f,p/'sources'/('previous_'+f.name))
 failures=list(old.glob('raw/*A1*v2*raw.png'))
 if failures:shutil.copy2(failures[0],p/'sources/previous_failed_v2.png')
 # True background comparisons, complete canvases, nearest equal-aspect scaling only.
 board=Image.new('RGB',(1600,1060),(240,236,227));d=ImageDraw.Draw(board)
 paths=[p/'sources/mother.png',p/f'exports/attempt{n}_transparent.png']
 layout=[]
 for row,c in enumerate([(239,234,221,255),(33,37,41,255)]):
  for col,f in enumerate(paths):
   im=Image.open(f).convert('RGBA'); comp=Image.alpha_composite(Image.new('RGBA',im.size,c),im).convert('RGB');sc=min(780/im.width,490/im.height); wh=(round(im.width*sc),round(im.height*sc));comp=comp.resize(wh,Image.Resampling.NEAREST);x=col*800+(800-wh[0])//2;y=row*530+30;board.paste(comp,(x,y));d.text((col*800+12,row*530+8),s+(' mother' if col==0 else f' A1 repair attempt{n}'),fill=(0,0,0));layout.append({'source':str(f.relative_to(r)),'position':[x,y],'size':wh,'resampling':'NEAREST','background':c})
 board.save(p/'review/mother_action_comparison.png');(p/'review/board_layout.json').write_text(json.dumps(layout,indent=2))
