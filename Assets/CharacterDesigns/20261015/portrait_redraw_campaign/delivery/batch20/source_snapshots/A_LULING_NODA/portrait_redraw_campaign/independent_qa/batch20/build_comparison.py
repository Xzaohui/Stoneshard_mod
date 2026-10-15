#!/usr/bin/env python3
"""Build audit-only boards; preserve source pixels and use integer NN only."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
Q=Path(__file__).resolve().parent;C=Q.parent.parent
selection=json.loads((Q/'FINAL_SELECTION.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
board=Image.new('RGB',(1264,632),(32,34,38));draw=ImageDraw.Draw(board)
draw.text((16,12),'BATCH 20 | DERIVED CONCEPT CANDIDATES | NOT NATIVE PIXEL FINALS',fill=(240,240,240))
records=[]
for i,(slug,row) in enumerate(selection['actors'].items()):
 p=C/slug/(row.get('selected_candidate') or row['held_evidence_candidate']);src=Image.open(p).convert('RGBA');x=16+312*i
 draw.text((x,40),slug+' | '+row['displayed_version'],fill=(240,240,240));draw.text((x,59),row['status'],fill=(190,190,190))
 for scale,y,bg in [(1,83,(230,226,215)),(4,211,(90,92,95))]:
  tile=Image.new('RGBA',src.size,(*bg,255));tile.alpha_composite(src);tile=tile.convert('RGB');shown=tile.resize((74*scale,100*scale),Image.Resampling.NEAREST);board.paste(shown,(x,y))
  records.append({'actor':slug,'source':str(p.relative_to(C)),'source_sha256':sha(p),'scale':scale,'background':bg,'position':[x,y],'pixel_match':board.crop((x,y,x+74*scale,y+100*scale)).tobytes()==shown.tobytes()})
board.save(Q/'selected_candidates_1x_4x.png')
compare=Image.new('RGB',(1264,875),(32,34,38));d=ImageDraw.Draw(compare)
for i,(slug,row) in enumerate(selection['actors'].items()):
 for j,version in enumerate(['portrait_v1','portrait_v2']):
  candidates=sorted((C/slug/'candidates').glob(version+'*_74x100_candidate.png'));p=(C/slug/(row.get('selected_candidate') or row['held_evidence_candidate'])) if j==1 else next((x for x in candidates if '_inset_' in x.name),candidates[0]);src=Image.open(p).convert('RGBA');tile=Image.new('RGBA',(74,100),(90,92,95,255));tile.alpha_composite(src);shown=tile.convert('RGB').resize((296,400),Image.Resampling.NEAREST);x=16+312*i;y=34+432*j
  d.text((x,y-20),slug+' '+p.stem.replace('_74x100_candidate','')+(' HELD' if j==1 and not row['deliverable'] else ''),fill=(240,240,240));compare.paste(shown,(x,y));records.append({'actor':slug,'source':str(p.relative_to(C)),'source_sha256':sha(p),'scale':4,'background':[90,92,95],'comparison_position':[x,y],'pixel_match':compare.crop((x,y,x+296,y+400)).tobytes()==shown.tobytes()})
compare.save(Q/'v1_v2_comparison_4x.png')
(Q/'comparison_manifest.json').write_text(json.dumps({'boards':['selected_candidates_1x_4x.png','v1_v2_comparison_4x.png'],'all_blits_verified':all(r['pixel_match'] for r in records),'records':records},ensure_ascii=False,indent=2)+'\n')
print('Boards verified:',all(r['pixel_match'] for r in records))
