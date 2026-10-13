"""Regional schematic art guide; display coordinates are not game world cells."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-streets-v1'
def main():
    nodes=[dict(id=k,cell=c,name_zh=n) for k,c,n in [
      ('R01-salt',[8,30],'盐车道'),('R01-port',[20,30],'港街复核亭'),
      ('R01-camp',[20,12],'灰堤工营'),('R01-hearing',[42,22],'听审棚与熄灯租屋'),
      ('R01-canal',[38,8],'旧渠检修墓室'),('R01-workshop',[52,12],'堤外工坊与弃置驿站')]]
    edges=[['R01-salt','R01-port'],['R01-port','R01-camp'],['R01-camp','R01-hearing'],
      ['R01-camp','R01-canal'],['R01-canal','R01-workshop'],['R01-workshop','R01-hearing'],['R01-hearing','R01-port']]
    lookup={n['id']:n['cell'] for n in nodes};im=Image.new('RGB',(1664,1248),'#20363A');d=ImageDraw.Draw(im)
    d.polygon([(0,0),(1663,0),(1663,1050),(1280,1080),(920,1080),(720,1050),(440,1030),(0,1030)],fill='#6F6153')
    for a,b in edges:d.line([tuple(v*26+13 for v in lookup[a]),tuple(v*26+13 for v in lookup[b])],fill='#A39277',width=52)
    for n in nodes:
        x,y=[v*26+13 for v in n['cell']];d.rectangle((x-78,y-52,x+78,y+52),fill='#4C3C2F')
    im.save(P/'guides/r01_region_geometry.png')
    data=dict(id='r01_region',size=[1664,1248],display_cells=[64,48],display_cell_pixels=26,nodes=nodes,edges=edges,
      authority='Seven R01 design topology edges; schematic display coordinates, not official geography or native world grid',runtime_verified=False)
    (P/'region-layout.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data,ensure_ascii=False))
if __name__=='__main__':main()
