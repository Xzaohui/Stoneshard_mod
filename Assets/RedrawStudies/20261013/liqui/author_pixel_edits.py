from pathlib import Path
import json
D=Path(__file__).resolve().parent
palette=json.loads((D/'pixel_edit_log.json').read_text())['palette']; e=[]
def row(x,y,s,reason):
 for i,c in enumerate(s):
  if c!='_':e.append([x+i,y,palette[int(c,18)] if c!='.' else '',reason])
# Mature brows, one-pixel eyes, angular nose, jaw and ear: erase oversized generated anime eye masses.
row(13,10,'266666633','Broaden forehead, retain swept auburn hair')
row(13,11,'233663322','Two sparse brows rather than large eye masses')
row(13,12,'650665062','Single dark pixel per eye, separate face from hair')
row(13,13,'566565662','Cheek plane and angular two-tone nose')
row(13,14,'566756652','Nose shadow and ear edge')
row(13,15,'756665752','Mature cheek shading, remove oversized eye residue')
row(13,16,'256337532','Small mouth and jaw, not a smiling anime mouth')
row(14,17,'2566570','Short jaw taper')
row(15,18,'076570','One short neck nested in collar')
# Bag flap, closed clasp and strap connection; no stock or currency.
row(12,27,'4FFE2','Closed satchel broad flap highlight')
row(12,28,'E44E2','Satchel flap lower plane')
row(12,29,'E12E2','Dark closed clasp and edge separation')
row(12,30,'E4EE2','Closed bag body')
row(12,31,'12221','Bag bottom outline')
# A single clearly stepped strap remains to anatomical right hip.
for x,y in [(21,20),(20,21),(20,22),(19,23),(18,24),(18,25),(17,26),(16,27)]:row(x,y,'E','Single continuous shoulder strap')
# Hand pixels give thumbs/cuffs without drawing individual fingers.
row(9,27,'15','Left cuff and wrist')
row(9,28,'65','Left empty palm, bag outline kept distinct')
row(9,29,'70','Left thumb/palm shadow')
row(25,27,'51','Right wrist and outline')
row(25,28,'65','Right empty palm')
row(25,29,'70','Right thumb/palm shadow')
# Short boots with readable instep and toe, preserve central negative gap.
row(13,36,'D4D20','Left boot upper/heel cluster')
row(13,37,'2211.','Left outsole')
row(20,36,'1D4D2','Right boot upper/toe cluster')
row(20,37,'12221','Right outsole')
(D/'pixel_edits_spec.json').write_text(json.dumps(e,ensure_ascii=False,indent=2))
