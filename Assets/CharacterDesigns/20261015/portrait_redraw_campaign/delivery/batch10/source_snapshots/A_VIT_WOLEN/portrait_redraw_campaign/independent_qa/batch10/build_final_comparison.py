from pathlib import Path
from PIL import Image, ImageDraw
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
BOARD=Image.new('RGB',(1300,920),(105,105,105));d=ImageDraw.Draw(BOARD)
d.text((20,12),'BATCH 10 / independently selected candidates / NOT native-pixel or runtime-approved',fill='white')
for i,n in enumerate(['vit','wolen','yani','rukan']):
 file='portrait_v2_74x100_candidate.png' if n in ['vit','wolen'] else 'portrait_v2_containment_mediancut_74x100_candidate.png'
 im=Image.open(CAMP/n/'candidates'/file).convert('RGBA'); x=20+320*i
 d.text((x,40),f'{n.upper()} / v2'+(' / aspect-fit MC' if n in ['yani','rukan'] else ''),fill='white')
 for k,bg in enumerate([(10,10,12),(105,105,105),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(im);BOARD.paste(tile.convert('RGB'),(x+94*k,60))
 large=im.resize((296,400),Image.Resampling.NEAREST);BOARD.paste(large,(x,180),large)
d.text((20,610),'Selected core style anchors at 2x nearest neighbor; identities are not copied.',fill='white')
for i,n in enumerate(['mara','iwo','leiya','tore']):
 im=Image.open(CAMP/'vit'/'sources'/f'{n}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST)
 x=40+320*i;BOARD.paste(im,(x,650),im);d.text((x,865),n.upper(),fill='white')
BOARD.save(OUT/'final_selected_comparison.png')
