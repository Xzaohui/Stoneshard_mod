#!/usr/bin/env python3
"""Build a read-only-source enemy concept catalog from selected_sources.json.
Requires Python 3, PyMuPDF, Pillow and NotoSansCJK-Regular.ttc.
"""
import argparse, hashlib, io, json
from pathlib import Path
import fitz
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
W,H=842,595
BG=(0.965,0.953,0.926); INK=(0.12,0.14,0.13); MUTED=(0.39,0.41,0.38); LINE=(0.79,0.79,0.74)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--final',action='store_true'); ap.add_argument('--font',default=FONT); args=ap.parse_args()
 data=json.loads((HERE/'selected_sources.json').read_text()); rows=data['enemies']
 from fontTools.ttLib import TTFont
 from fontTools.subset import Subsetter, Options
 font=TTFont(args.font,fontNumber=2 if args.font.endswith('.ttc') else -1)
 options=Options(); options.retain_gids=True; subset=Subsetter(options=options); subset.populate(text=(HERE/'selected_sources.json').read_text()+Path(__file__).read_text()+''.join(chr(n) for n in range(32,127)))
 subset.subset(font); font.save(HERE/'catalog_font_subset.otf'); args.font=str(HERE/'catalog_font_subset.otf')
 if args.final:
  assert data['status']=='approved_selected_sources_locked', 'Final build blocked: approved selection lock required'
  assert all(len(e['actions'])==2 for e in rows), '24 selected actions required'
 doc=fitz.open(); checks=[]
 def text(pg,x,y,s,size=12,color=INK):
  assert x+fitz.Font(fontfile=args.font).text_length(s,fontsize=size)<W-20, s
  pg.insert_text((x,y),s,fontname='cn',fontsize=size,color=color)
 def page(section,n):
  pg=doc.new_page(width=W,height=H);pg.insert_font(fontname='cn',fontfile=args.font)
  pg.draw_rect(pg.rect,color=None,fill=BG)
  text(pg,36,31,'原创敌人设定集',10,MUTED);text(pg,641,31,section,10,MUTED)
  pg.draw_line((36,554),(806,554),color=LINE,width=.5)
  text(pg,36,574,'2026.10.13  /  静态概念与独立关键姿势',9,MUTED)
  text(pg,753,574,f'{n:02d} / 14',9,MUTED)
  return pg
 def art(pg,src,box):
  p=ROOT/src['path']; assert sha(p)==src['sha256'], f'SHA mismatch: {p}'
  im=Image.open(p).convert('RGBA'); bbox=im.getchannel('A').getbbox(); assert bbox
  crop=im.crop(bbox); rect=fitz.Rect(box); scale=min(rect.width/crop.width,rect.height/crop.height)
  # Rasterize at 144 dpi, nearest neighbor only; preserve original artwork on disk.
  ww=max(1,round(crop.width*scale*2));hh=max(1,round(crop.height*scale*2))
  scaled=crop.resize((ww,hh),Image.Resampling.NEAREST);buf=io.BytesIO();scaled.save(buf,format='PNG')
  rw=crop.width*scale;rh=crop.height*scale
  target=fitz.Rect(rect.x0+(rect.width-rw)/2,rect.y1-rh,rect.x0+(rect.width+rw)/2,rect.y1)
  xref=pg.insert_image(target,stream=buf.getvalue(),keep_proportion=True);doc.xref_set_key(xref,'Interpolate','false')
  checks.append({'page':pg.number+1,'path':src['path'],'sha256':src['sha256'],'alpha_bbox':bbox,'layout_rect':list(target),'raster_size':[ww,hh],'source_unchanged':True})
 pg=page('十二种敌人总览',1)
 text(pg,36,66,'十二种敌人概念',26)
 text(pg,36,88,'Mod 原创外观与职能提案，供浏览和选稿。',11,MUTED)
 for i,e in enumerate(rows):
  x=36+(i%4)*196;y=106+(i//4)*146
  art(pg,e['idle'],[x+35,y,x+151,y+110]);text(pg,x+3,y+127,f"{e['id']}  {e['name']}",11)
  text(pg,x+3,y+141,e['category'],8,MUTED)
 for i,e in enumerate(rows):
  pg=page(f"{e['id']}  /  {e['category']}",i+2)
  text(pg,36,76,e['name'],28);text(pg,36,101,e['tagline'],12,MUTED)
  pg.draw_line((287,132),(287,488),color=LINE,width=.5);pg.draw_line((555,132),(555,488),color=LINE,width=.5)
  figures=[{'label':'静态选稿',**e['idle']}]+e['actions']
  for j in range(3):
   x=36+j*268
   if j<len(figures):
    art(pg,figures[j],[x+8,137,x+230,465]);text(pg,x+14,505,figures[j]['label'],14)
   else:text(pg,x+32,310,'动作选稿待确认',14,MUTED)
  text(pg,36,534,'各图为独立概念姿势，展示比例不代表游戏尺寸。',10,MUTED)
 pg=page('使用说明',14);text(pg,36,86,'使用范围与限制',28)
 lines=[('原创提案','本册汇总十二种敌人的外观与职能提案，不作为原作剧情或身份事实。'),('姿势范围','每种敌人展示一张静态选稿和两个独立关键姿势，不是连续动画。'),('游戏验证','游戏网格、帧间对位、碰撞、装备组合与运行效果尚未验证。'),('浏览版图像','为便于浏览，透明选稿按版面等比缩放；高清母图已分别交付。'),('制作记录','制作日期：2026年10月13日。选稿路径、版本与 SHA-256 见配套清单。')]
 for n,(title,body) in enumerate(lines):
  y=143+n*68;text(pg,36,y,title,14);text(pg,36,y+25,body,12,MUTED)
 text(pg,36,514,'选稿提示：009 锈甲斧亡卒与 012 缄声执铃者的静态图采用风格修订版。',10,MUTED)
 doc.set_metadata({'title':'原创敌人设定集','author':'Stoneshard Mod 原创概念','subject':'十二种敌人静态与独立关键姿势浏览版','keywords':'原创概念,非连续动画,未进行游戏内验证'})
 doc.set_toc([[1,'十二种敌人总览',1]]+[[1,f"{e['id']} {e['name']}",i+2] for i,e in enumerate(rows)]+[[1,'使用范围与限制',14]])
 out=HERE/('enemy_design_catalog.pdf' if args.final else 'catalog_layout_pending.pdf');doc.save(out,garbage=4,deflate=True);doc.close()
 doc=fitz.open(out); render=HERE/'rendered';render.mkdir(exist_ok=True)
 for i,p in enumerate(doc):p.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(render/f'page-{i+1:02d}.png')
 doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False).save(HERE/'enemy_twelve_overview.png')
 write_json(HERE/'layout_checks.json',{'status':'awaiting_visual_review','pdf':out.name,'pages':len(doc),'bytes':out.stat().st_size,'image_layouts':checks,'source_hashes_verified':True,'continuous_animation':False,'runtimeVerified':False})
 print(out, out.stat().st_size)
if __name__=='__main__':main()
