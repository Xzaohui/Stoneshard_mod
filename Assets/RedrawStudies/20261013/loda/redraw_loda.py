from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[4]);parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args()
ROOT=args.root.resolve(); OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch34/131_bry_loda_rukan_risha_cast.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
pal={'o':'302823','hd':'352c27','hm':'48392f','hl':'5f4939','s0':'8e5438','s1':'bd7951','s2':'dda071','s3':'edb68b','bd':'343d44','bm':'4a5964','bl':'657681','cu':'87938c','ad':'543a28','am':'795337','al':'976b44','r':'bea36d','rd':'705535','pd':'403e2d','pm':'626047','pl':'7a7451','boot':'4c3829','steel':'afb1a0'}
pal={k:'#'+v for k,v in pal.items()};im=Image.new('RGBA',(35,44));d=ImageDraw.Draw(im)
def poly(pts,c):d.polygon(pts,fill=pal[c])
def rect(box,c):d.rectangle(box,fill=pal[c])
def line(pts,c,w=1):d.line(pts,fill=pal[c],width=w)
# New hand-authored compact silhouette, independent of the old whole-sprite resize.
# Trousers visibly divided below apron; boots are only three rows.
poly([(11,29),(25,29),(26,34),(25,36),(26,37),(20,37),(19,34),(16,34),(15,37),(8,37),(8,35),(11,34)],'o')
rect((11,30,16,34),'pd');rect((12,31,15,33),'pm');rect((20,30,25,34),'pd');rect((21,31,24,33),'pm');rect((22,31,24,31),'pl')
rect((10,35,15,36),'boot');rect((9,36,13,36),'am');rect((21,35,24,36),'boot');rect((22,36,25,36),'am')
# Sleeves and apron chest join immediately under jaw, with raised waist y26.
poly([(12,21),(22,21),(26,22),(28,25),(28,28),(25,29),(24,31),(11,32),(9,29),(7,28),(6,25),(9,22)],'o')
poly([(10,22),(13,22),(13,26),(10,27),(7,26),(8,24)],'bm');rect((9,23,11,24),'bl')
poly([(22,22),(25,23),(27,25),(27,26),(24,27),(22,25)],'bm');rect((24,23,25,24),'bl')
line([(7,26),(9,27),(11,27)],'cu');line([(24,26),(27,26)],'cu')
poly([(8,27),(10,28),(10,29),(8,29),(7,28)],'s1');rect((8,27,9,28),'s2')
poly([(25,27),(27,27),(27,28),(25,29),(24,28)],'s1');rect((25,27,26,27),'s2')
# Deep blue shirt remains visible around brown apron, no skirt substitution.
poly([(13,21),(15,22),(19,22),(21,21),(23,24),(22,27),(13,27),(11,24)],'bd')
poly([(12,22),(13,22),(14,24),(21,24),(22,22),(23,23),(23,27),(12,27)],'ad')
rect((13,24,21,25),'am');rect((14,24,20,24),'al');rect((12,26,24,26),'o');rect((13,26,23,26),'ad');rect((17,26,18,26),'r')
poly([(12,27),(22,27),(21,31),(11,31)],'ad');poly([(13,27),(20,27),(20,30),(12,30)],'am');rect((14,28,15,29),'al')
# One continuous hanging rope loop, not bundled strings. Hole stays distinct.
line([(24,27),(23,28),(23,31),(24,32),(26,32),(27,31),(27,29),(26,28),(24,28),(24,27)],'o')
line([(24,28),(24,31),(25,31),(26,30),(26,29),(25,28),(24,28)],'r')
rect((25,29,25,30),'ad')
# Single small work hammer on opposite waist, 2px head and short shaft.
line([(10,28),(8,32)],'o',2);line([(10,29),(9,31)],'al');rect((8,28,10,28),'steel');rect((8,29,8,29),'bd')
# Hair core width17 at x9..25; the side bun is not included in core measure.
poly([(14,4),(20,4),(20,5),(23,5),(25,7),(25,9),(27,8),(28,10),(27,12),(25,13),(25,18),(23,20),(21,21),(12,21),(10,19),(9,15),(9,9),(10,7),(12,6),(12,5)],'o')
poly([(14,5),(20,5),(23,7),(24,10),(23,13),(23,18),(21,19),(20,13),(16,10),(12,10),(10,12),(10,9),(12,7)],'hm')
poly([(14,6),(19,6),(21,7),(22,9),(19,8),(17,8),(15,9),(12,9)],'hl')
rect((25,9,26,11),'hm');rect((26,9,26,10),'hl')
# Face / chin intentionally occupy y10..20: skin, not a neck extension.
poly([(13,9),(15,10),(17,10),(18,12),(20,13),(21,15),(21,18),(19,20),(14,20),(12,19),(11,17),(10,16),(11,14),(11,11)],'s1')
poly([(13,10),(15,11),(16,11),(16,13),(19,14),(19,17),(18,19),(14,19),(12,17),(12,14)],'s2')
rect((12,11,14,12),'s3');rect((12,15,13,16),'s3');rect((15,17,18,18),'s2')
line([(11,13),(13,13)],'hm');rect((12,14,12,14),'o');line([(17,13),(19,14)],'hm');rect((18,15,18,15),'o')
rect((11,16,12,16),'s0');line([(13,18),(15,18)],'s0');rect((15,20,18,20),'s1')
# Right ear and a dark hair boundary; no long free neck below chin.
rect((21,14,22,16),'s1');rect((21,14,21,15),'s2');rect((22,17,23,19),'hd');rect((20,11,21,13),'hd')
rect((16,21,18,21),'s0')
im.save(OUT/'loda_native_v1.png');im.save(OUT/'loda_1x.png');im.resize((280,352),Image.Resampling.NEAREST).save(OUT/'loda_8x.png')
# Original front crop only, background removed only for equal-floor comparison.
src=Image.open(SOURCE).convert('RGBA');crop=src.crop((165,25,400,480));crop.save(OUT/'old_loda_front_crop.png')
pix=crop.load()
for y in range(crop.height):
 for x in range(crop.width):
  r,g,b,a=pix[x,y]
  if max(r,g,b)-min(r,g,b)<9 and r>70:pix[x,y]=(0,0,0,0)
bb=crop.getbbox();old=crop.crop(bb);old.thumbnail((18,34),Image.Resampling.NEAREST);oldframe=Image.new('RGBA',(35,44));oldframe.alpha_composite(old,(17-old.width//2,38-old.height));oldframe.save(OUT/'old_normalized_comparison_only.png')
refs=[('Old: proportional fit',oldframe),('LODA v1',im),('Gunda (reference)',Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png').convert('RGBA')),('Jurg (reference)',Image.open(ROOT/'Assets/ReferenceAudit/20261013/originals/s_npc_carpenter_0.png').convert('RGBA'))]
for scale in [1,8]:
 w=max(160,35*scale+40);sheet=Image.new('RGB',(w*len(refs),44*scale+90),'#ddddda');sd=ImageDraw.Draw(sheet)
 for i,(name,a) in enumerate(refs):
  x=i*w+20;sheet.paste(a.resize((35*scale,44*scale),Image.Resampling.NEAREST),(x,38),a.resize((35*scale,44*scale),Image.Resampling.NEAREST));sd.text((i*w+4,8),name,fill='#202020');sd.line((i*w,38+38*scale,(i+1)*w-1,38+38*scale),fill='#aa4b48');sd.text((i*w+4,44*scale+43),'Sole boundary y38',fill='#202020')
 sheet.save(OUT/f'comparison_floor_{scale}x.png')
# Separate marked sheet, with exact inclusive pixel-row conventions.
a=Image.new('RGB',(560,440),'#ddddda');a.paste(im.resize((280,352),Image.Resampling.NEAREST),(28,40),im.resize((280,352),Image.Resampling.NEAREST));ad=ImageDraw.Draw(a)
for row,label,c in [(4,'y4 crown (hair core)', '#356657'),(21,'after skin chin y20: H17', '#94613d'),(38,'after sole y37: B17', '#a24949')]:
 yy=40+row*8;ad.line((25,yy,315,yy),fill=c);ad.text((320,yy-4),label,fill=c)
ad.text((20,405),'Core width 17px; shoulders 18px; neck 0-1 row. Boundary +/-1px.',fill='#202020');a.save(OUT/'loda_landmarks_8x.png')
meta={'actor':'BRY-NPC-LODA','method':'Original front reviewed; explicit hand-authored pixel-cluster structural redraw, not whole-image reduction. Pillow permitted by user. No image generation used.','canvas':[35,44],'alpha_bbox':im.getbbox(),'crown_y':4,'skin_chin_y':20,'dark_edge_y':21,'sole_y':37,'head_rows':17,'body_rows':17,'boundary_tolerance':'1px: 16/18 or 18/16. Bun does not define crown or cranial width. Neck skin y21 excluded.','head_core_x':[9,25],'clothed_shoulders_x':[9,26],'shoulder_measurement_row':22,'head_core_width':17,'shoulder_width':18,'independent_neck_rows':'0-1, collar joined y21-22','identity':['dark side bun','blue rolled sleeves','brown apron over trousers','one clear side rope loop','one small opposite-side hammer'],'source':str(SOURCE.relative_to(ROOT)),'source_sha256':sha(SOURCE),'card':'design/04_人物/城市人物/人物_BRY-NPC-LODA_洛妲.md','card_sha256':sha(ROOT/'design/04_人物/城市人物/人物_BRY-NPC-LODA_洛妲.md'),'runtimeIntegrated':False,'runtimeVerified':False,'sourceChanged':False,'reference_only':True,'outputs':{p.name:sha(p) for p in OUT.glob('*.png')}}
(OUT/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta,ensure_ascii=False,indent=2))
