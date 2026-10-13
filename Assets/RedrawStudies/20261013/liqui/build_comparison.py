from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent; R=D.parents[3]
refs=[('Frid','s_npc_herbalist_0.png'),('Bert','s_npc_merchant01_0.png'),('Jurg','s_npc_carpenter_0.png'),('Gunda','s_peasantfemale_09_0.png')]
b=Image.new('RGB',(1260,600),'#787878'); d=ImageDraw.Draw(b)
for i,(name,path) in enumerate([('LIQUI candidate',None)]+refs):
 p=D/'liqui_native_v1.png' if path is None else R/'Assets/ReferenceAudit/20261013/originals'/path
 im=Image.open(p).convert('RGBA').resize((245,308),Image.Resampling.NEAREST); b.paste(im,(i*250,50),im);d.text((i*250+8,20),name,fill='white')
d.text((10,385),'Same 7x nearest scale. Native refs are copyrighted game comparison evidence, not mod outputs.',fill='white');d.text((10,410),'LIQUI: 35x44 study canvas; visible 20x34. One pose only. Style/runtime NOT approved.',fill='white');b.save(D/'liqui_native_reference_comparison.png')
b=Image.new('RGB',(1400,940),'#787878');d=ImageDraw.Draw(b)
old=Image.open(R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch47/177_trade_liqui_cast.png').crop((230,15,700,990));old.thumbnail((350,810));b.paste(old,(20,70));d.text((20,25),'OLD 177: identity only; not native pixels',fill='white')
co=Image.open(D/'liqui_structure_concept_v2.png').convert('RGBA');co.thumbnail((430,810));b.paste(co,(390,70),co);d.text((390,25),'IMAGEGEN structural redraw v2',fill='white')
na=Image.open(D/'liqui_native_v1.png').resize((525,660),Image.Resampling.NEAREST);b.paste(na,(855,70),na);d.text((855,25),'NATIVE candidate + explicit pixel edits 15x',fill='white')
d.text((20,900),'Non-runtime appearance study. Old/source images unchanged. Concept detail and native geometry are different review stages.',fill='white');b.save(D/'liqui_old_concept_native_comparison.png')
