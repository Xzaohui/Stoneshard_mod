from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
item=json.loads((ROOT/'sources/brief_item_v1.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(version):
 raw=next((ROOT/'raw').glob('*_v'+str(version)+'_raw_imagegen.png'));im=Image.open(raw).convert('RGBA');ar=np.array(im);alpha=ar[:,:,3];hidden=int(np.sum((alpha==0)&np.any(ar[:,:,:3]!=0,axis=2)))
 # Solid non-spectral character: deterministic alpha cleanup only, no RGB/body editing.
 ar[:,:,3]=np.where(alpha>=128,255,0).astype('uint8');ar[ar[:,:,3]==0,:3]=0
 clean=Image.fromarray(ar,'RGBA');pad=Image.new('RGBA',(clean.width+128,clean.height+128));pad.alpha_composite(clean,(64,64));candidate=ROOT/(item['slug']+'_'+item['pose_id']+'_v'+str(version)+'_transparent.png');pad.save(candidate)
 audit={'raw_sha256':sha(raw),'candidate_sha256':sha(candidate),'raw_size':list(im.size),'candidate_size':list(pad.size),'raw_alpha_bbox':im.getchannel('A').getbbox(),'candidate_alpha_bbox':pad.getchannel('A').getbbox(),'raw_hidden_rgb_alpha0_count':hidden,'alpha_cleanup':'alpha >= 128 becomes 255; alpha < 128 becomes 0; zero RGB only where alpha=0; add 64 transparent pixels on every side','rgb_visible_body_redrawn':False,'geometry_transformed':False,'raw_preserved':True}
 (ROOT/('alpha_audit_v'+str(version)+'.json')).write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',19);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',15)
 refs=[ROOT/'sources/files'/a['source_path'] for a in item['source_images']]+[candidate];labels=['母图（身份锚）',item['source_images'][1]['pose_id'],item['source_images'][2]['pose_id'],'新增：'+item['label']]
 board=Image.new('RGB',(1440,870),(222,218,208));draw=ImageDraw.Draw(board);draw.text((20,10),item['concept_id']+' '+item['working_name']+'｜相邻关键阶段比较 v'+str(version),font=font,fill=(30,30,30));draw.text((20,40),'浅/深底为真实RGBA合成；等比最近邻展示。仅关键阶段概念，未验证连续动画、锚点、装备或运行。',font=small,fill=(45,45,45))
 for row,bg in enumerate([(236,231,219),(32,35,40)]):
  for col,(path,label) in enumerate(zip(refs,labels)):
   src=Image.open(path).convert('RGBA');bbox=src.getchannel('A').getbbox();crop=src.crop(bbox);scale=min(320/crop.width,315/crop.height);sz=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(sz,Image.Resampling.NEAREST);cell=Image.new('RGBA',(360,385),bg+(255,));cell.alpha_composite(crop,((360-sz[0])//2,345-sz[1]));dt=ImageDraw.Draw(cell);dt.text((12,10),label,font=small,fill=((32,32,32,255) if row==0 else (230,230,230,255)));board.paste(cell.convert('RGB'),(col*360,80+row*385))
 board.save(ROOT/'review'/('adjacent_light_dark_v'+str(version)+'.png'))
 for label,bg in [('light',(236,231,219,255)),('dark',(32,35,40,255))]:
  comp=Image.new('RGBA',pad.size,bg);comp.alpha_composite(pad);comp.convert('RGB').save(ROOT/'review'/('candidate_v'+str(version)+'_'+label+'.png'))
 return audit
if __name__=='__main__':
 import sys;print(json.dumps(build(int(sys.argv[1])),ensure_ascii=False))
