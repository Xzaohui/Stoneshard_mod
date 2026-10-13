from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
D=Path(__file__).resolve().parent
src=D.parent/'anla_native_v3.png'; im=Image.open(src).convert('RGBA'); a=np.array(im)
# Enlarge only the existing head height by two whole authored scanlines.
# Duplicate forehead y10 and lower cheek y16. Preserve x coordinates/colors.
# Remove the two original exposed-neck rows y20–21. Everything y22+ unchanged.
row_map=list(range(11))+[10]+list(range(11,17))+[16]+list(range(17,20))+list(range(22,44))
assert len(row_map)==44
b=a[row_map].copy();out=Image.fromarray(b);out.save(D/'anla_native_1to1.png');out.resize((280,352),Image.Resampling.NEAREST).save(D/'anla_native_1to1_8x.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
qa={'source':str(src.name),'source_sha256':sha(src),'result_sha256':sha(D/'anla_native_1to1.png'),'canvas':[35,44],'bbox':out.getbbox(),'actual_palette_count':len(set(map(tuple,b[b[:,:,3]>0,:3]))),'alpha_values':np.unique(b[:,:,3]).tolist(),'row_map_output_to_input':row_map,'changes':'Duplicate source forehead row10 and lower-cheek row16; source lower jaw row18 becomes output20. Remove source neck rows20–21. Preserve full body at rows22–43 exactly. No horizontal scaling or recoloring.','body_rows22_plus_identical':bool(np.array_equal(a[22:],b[22:])),'head_top_y':4,'visible_skin_chin_y':20,'jaw_dark_outline_y':21,'feet_last_y':37,'head_inclusive_skin_chin':17,'remaining_rows_below_skin_chin':17,'warning':'Chin boundary is a visually reviewed landmark, not an alpha-derived anatomical measurement. Independent review requested; not runtime verified.'}
(D/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
# Same-scale, same 35x44 canvas, same foot baseline. Geometry guides mark pixel boundaries.
for guides,name in [(False,'comparison_8x.png'),(True,'landmark_comparison_8x.png')]:
 board=Image.new('RGB',(700,425),(73,73,78));dr=ImageDraw.Draw(board)
 for i,(label,p,chin) in enumerate([('Original v3: skin chin y18',im,18),('Revision: skin chin y20',out,20)]):
  x=40+i*350;y=40;en=p.resize((280,352),Image.Resampling.NEAREST);board.paste(en,(x,y),en);dr.text((x,12),label,fill='white')
  if guides:
   for row,title,c in [(4,'top y4',(126,204,190)),(chin+1,f'after chin y{chin}',(235,190,110)),(38,'after foot y37',(165,190,220))]:
    yp=y+row*8;dr.line((x-8,yp,x+280,yp),fill=c);dr.text((x+220,yp+2),title,fill=c)
  else:dr.line((x,344,x+279,344),fill=(100,105,112))
 dr.text((40,403),'Both: 35x44 canvas, 8x nearest. Body from y22 down stays pixel-identical.',fill='white')
 board.save(D/name)
print(json.dumps(qa,ensure_ascii=False))
