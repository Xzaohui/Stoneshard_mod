from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
im=Image.open(P/'sela_G_head_composite_native.png').convert('RGBA');a=np.array(im);b=a.copy()
col={'.':(0,0,0,0),'B':(32,27,26,255),'E':(53,39,31,255),'D':(73,48,40,255),'C':(102,67,51,255),'H':(129,86,56,255),'I':(179,102,65,255),'F':(219,148,97,255),'G':(239,187,130,255),'K':(159,94, 64,255)}
# One targeted cleanup pass. Eyebrow and eye axes from generated concept;
# dark one-pixel gaze cores, skin instead of white, slight asymmetric smile.
edits={(16,13):'H',(17,13):'H',(16,14):'G',(17,14):'F',(18,14):'H',(16,15):'B',(17,15):'C',(12,15):'B',(13,15):'D',
(13,16):'G',(14,16):'G',(15,16):'G',(16,16):'F',(17,16):'F',
(13,17):'I',(14,17):'G',(15,17):'F',(16,17):'I',
(12,18):'F',(13,18):'G',(14,18):'K',(15,18):'K',(16,18):'F',
(10,18):'.',(11,18):'D',(11,19):'.',(12,19):'D'}
for (x,y),v in edits.items():b[y,x]=col[v]
out=Image.fromarray(b);out.save(P/'sela_G_refined_native.png');out.resize((280,352),Image.Resampling.NEAREST).save(P/'sela_G_refined_8x.png')
C=Image.open(P.parent/'c_reorganized/sela_face_C_native.png').convert('RGBA');raw=Image.open(P/'sela_G_raw_imagegen.png').convert('RGBA');board=Image.new('RGB',(900,660),(180,183,172));d=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for i,(name,sp) in enumerate([('C - native',C),('G - CONCEPT',raw),('G - refined native',out)]):
 x=i*300;d.text((x+35,20),name,font=font,fill=(28,28,28))
 if i==1:
  s=sp.resize((210,264),Image.Resampling.LANCZOS);board.paste(s,(x+45,55),s)
  h=sp.crop((int(7*1118/35),int(3*1407/44),int(29*1118/35),int(23*1407/44))).resize((220,200),Image.Resampling.LANCZOS)
 else:
  s=sp.resize((210,264),Image.Resampling.NEAREST);board.paste(s,(x+45,55),s);h=sp.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST)
 board.paste(h,(x+40,370),h)
 d.text((x+35,600),'Generated concept; not native' if i==1 else '35 x 44 native; head 17 px',font=small,fill=(45,45,40))
board.save(P/'comparison_C_Gconcept_Gnative.png')
base=np.array(Image.open(P.parent/'before_native.png').convert('RGBA'));diff=np.any(a!=b,axis=2)
q={'changed_vs_G_composite':int(diff.sum()),'body_y21_and_below_equal':bool(np.array_equal(b[21:],base[21:])),'all_changes_inside_head':bool(not diff[21:].any()),'new_color':[159,94,64,255],'visible_y':[int(np.where(b[:,:,3]>0)[0].min()),int(np.where(b[:,:,3]>0)[0].max())],'sha256':hashlib.sha256((P/'sela_G_refined_native.png').read_bytes()).hexdigest()};(P/'QA-G-refined.json').write_text(json.dumps(q,indent=2)+'\n');(P/'pixel_edits_G_refined.json').write_text(json.dumps([{'x':x,'y':y,'before':a[y,x].tolist(),'after':b[y,x].tolist()} for x,y in edits],indent=2)+'\n');print(q)
