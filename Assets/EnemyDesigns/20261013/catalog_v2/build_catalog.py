#!/usr/bin/env python3
"""Create v2 PDF, 14 review pages, 12-enemy coverage overview and lossless browser rasters.
No generation or retouch: nearest-neighbor resizing of the entire selected RGBA canvas.
RGB and alpha are embedded independently and verified byte-for-byte after PDF save.
"""
import argparse,hashlib,io,json
from pathlib import Path
import fitz
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter,Options
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
W,H=1100,1400
BG=(0.965,0.957,0.937);INK=(.16,.20,.19);MUTED=(.40,.44,.42);LINE=(.78,.80,.76)
CARD=(.985,.979,.962);ACCENT=(.30,.43,.35);WARN=(.63,.32,.23);DARK=(.16,.20,.22);LIGHT=(.90,.94,.92)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def pngbytes(im):
 b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--font',default='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');args=ap.parse_args()
 data=json.loads((HERE/'selected_sources.json').read_text());rows=data['enemies']
 assert data['status']=='approved_selected_sources_locked'
 sources=[a for e in rows for a in [e['idle']]+e['actions']+([e['continuation']] if e['continuation'] else [])]
 assert len(sources)==len({s['sha256'] for s in sources})==47
 fontout=HERE/'catalog_font_subset.otf'
 if Path(args.font).resolve()!=fontout.resolve():
  ft=TTFont(args.font,fontNumber=2 if args.font.endswith('.ttc') else -1)
  options=Options();options.retain_gids=True
  sub=Subsetter(options=options);sub.populate(text=(HERE/'selected_sources.json').read_text()+Path(__file__).read_text()+''.join(chr(i) for i in range(32,127)));sub.subset(ft);ft.save(fontout)
 font=fitz.Font(fontfile=str(fontout));rasters={};rasterfiles=[]
 rdir=HERE/'browser_rasters';rdir.mkdir(exist_ok=True)
 for e in rows:
  for a in [e['idle']]+e['actions']+([e['continuation']] if e['continuation'] else []):
   p=ROOT/a['path'];assert sha(p)==a['sha256'];im=Image.open(p).convert('RGBA')
   scale=min(1,700/max(im.size));size=(max(1,round(im.width*scale)),max(1,round(im.height*scale)))
   im=im.resize(size,Image.Resampling.NEAREST)
   outfile=rdir/f"{e['id']}_{a['slot']}.png";im.save(outfile)
   rasters[a['sha256']]=im;rasterfiles.append({'id':e['id'],'slot':a['slot'],'source_path':a['path'],'source_sha256':a['sha256'],'raster_path':str(outfile.relative_to(HERE)),'raster_sha256':sha(outfile),'raster_dimensions':list(im.size),'rgb_decoded_sha256':hashlib.sha256(im.convert('RGB').tobytes()).hexdigest(),'alpha_decoded_sha256':hashlib.sha256(im.getchannel('A').tobytes()).hexdigest(),'crop':False,'resize':'nearest_neighbor_entire_canvas','alpha_adjustment':False})
 doc=fitz.open();layout=[];pendinglinks=[];xrefcache={}
 def text(pg,x,y,s,size=15,color=INK):
  length=font.text_length(s,fontsize=size);assert x+length<=pg.rect.width-20,(s,x,length)
  pg.insert_text((x,y),s,fontname='cn',fontsize=size,color=color)
 def newpage(section,n):
  pg=doc.new_page(width=W,height=H);pg.insert_font(fontname='cn',fontfile=str(fontout));pg.draw_rect(pg.rect,color=None,fill=BG)
  text(pg,48,40,'原创敌人设定集  /  v2',12,MUTED);text(pg,780,40,section,12,MUTED)
  pg.draw_line((48,1350),(1052,1350),color=LINE,width=.7)
  text(pg,48,1375,'2026.10.14  ·  独立关键姿态概念  ·  未进行游戏内验证',12,MUTED)
  text(pg,960,1375,f'{n:02d} / 14',12,MUTED)
  if n>2:
   text(pg,915,81,'返回目录',14,ACCENT);pendinglinks.append((n-1,fitz.Rect(909,60,1048,90),1))
  return pg
 def art(pg,a,box):
  im=rasters[a['sha256']];rect=fitz.Rect(box);scale=min(rect.width/im.width,rect.height/im.height)
  rw,rh=im.width*scale,im.height*scale;target=fitz.Rect(rect.x0+(rect.width-rw)/2,rect.y0+(rect.height-rh)/2,rect.x0+(rect.width+rw)/2,rect.y0+(rect.height+rh)/2)
  if a['sha256'] in xrefcache:xref=pg.insert_image(target,xref=xrefcache[a['sha256']])
  else:
   xref=pg.insert_image(target,stream=pngbytes(im.convert('RGB')),mask=pngbytes(im.getchannel('A')),keep_proportion=True)
   doc.xref_set_key(xref,'Interpolate','false');xrefcache[a['sha256']]=xref
  layout.append({'page':pg.number+1,'source_sha256':a['sha256'],'source_path':a['path'],'raster_dimensions':list(im.size),'target_rect':list(target),'cell_rect':list(rect),'proportional':abs(target.width/target.height-im.width/im.height)<1e-5,'crop':False})
  return target
 pg=newpage('十二种敌人  /  浏览合订',1)
 text(pg,48,111,'十二种敌人 · 姿态图册',38)
 text(pg,48,150,'12 张静态母图 + 35 个通过的独立动作姿态 = 47 张选稿',20,ACCENT)
 text(pg,48,184,'本版并入此前已交付的 11 个续姿；本轮没有新增生成。',15,MUTED)
 for i,e in enumerate(rows):
  x=48+(i%3)*341;y=215+(i//3)*258
  pg.draw_rect(fitz.Rect(x,y,x+322,y+242),color=LINE,fill=CARD,width=.6)
  art(pg,e['idle'],[x+30,y+10,x+292,y+184])
  text(pg,x+16,y+208,f"{e['id']}  {e['name']}",18)
  text(pg,x+16,y+231,f"{e['category']}  ·  {e['independent_action_count']} 个动作"+('  ·  续姿缺项' if e['id']=='002' else ''),12,WARN if e['id']=='002' else MUTED)
  pendinglinks.append((0,fitz.Rect(x,y,x+322,y+242),i+2))
 text(pg,48,1283,'002 下挥中段仍未通过，第四格保留缺项。点击角色卡或目录即可跳转。',14,WARN)
 text(pg,48,1310,'各图为独立概念，不是连续动画；重复展示的母图不重复计数。',14,MUTED)
 pg=newpage('可点击目录  /  阅读说明',2)
 text(pg,48,112,'目录与范围',38)
 text(pg,48,155,'点击任意一行进入对应敌人；每页右上角可返回本页。',16,MUTED)
 for i,e in enumerate(rows):
  y=195+i*65
  pg.draw_rect(fitz.Rect(48,y,1052,y+57),color=None,fill=CARD if i%2==0 else BG)
  text(pg,65,y+37,f"{e['id']}   {e['name']}",19)
  text(pg,430,y+35,e['category'],15,MUTED)
  text(pg,565,y+35,f"1 母图 + {e['independent_action_count']} 动作"+(' / 缺下挥中段' if e['id']=='002' else ''),15,WARN if e['id']=='002' else MUTED)
  text(pg,980,y+35,f"{i+3:02d}",17,ACCENT)
  pendinglinks.append((1,fitz.Rect(48,y,1052,y+57),i+2))
 text(pg,48,1020,'选稿与使用说明',22)
 notes=[
 '001 原两动作沿用自然前握替代；009、012 母图使用风格修订版。',
 '续姿选用 001 / 008 / 011 的 v2，其余通过项沿用 v1。002 两版均失败。',
 '保留完整画布、原 RGB 与 alpha；仅做等比 nearest-neighbor 浏览缩放。',
 '姿态之间尚未完成精确锚点、尺度或连续性验收；不代表完整动画循环。',
 '装备组合、碰撞、游戏内集成与实机效果仍未验证。',
 '配套小 ZIP 含排版、字体、来源 SHA、证据与逐页预览，不含全部 raw。']
 for i,s in enumerate(notes):text(pg,48,1061+i*38,s,16,MUTED)
 for i,e in enumerate(rows):
  pg=newpage(f"{e['id']}  /  {e['category']}",i+3)
  text(pg,48,108,e['name'],38);text(pg,48,139,e['tagline'],16,MUTED)
  figs=[e['idle']]+e['actions']+[e['continuation']]
  for j,a in enumerate(figs):
   x=48+(j%2)*514;y=168+(j//2)*538
   isghost=e['id'] in ['004','010'];bg=DARK if isghost and a else CARD;fg=LIGHT if isghost and a else INK
   pg.draw_rect(fitz.Rect(x,y,x+490,y+512),color=LINE,fill=bg,width=.7)
   slot=['静态母图','原动作 01','原动作 02','已交付续姿'][j]
   text(pg,x+20,y+34,slot,14,LIGHT if isghost and a else MUTED)
   if a:
    art(pg,a,[x+20,y+54,x+470,y+444]);text(pg,x+20,y+477,a['label'],21,fg)
    sub='风格修订版' if a.get('version')=='idle_style_v2' else (f"通过选稿 v{a['version']}" if a['slot']=='continuation' else '原已交付选稿')
    text(pg,x+20,y+500,sub,12,LIGHT if isghost and a else MUTED)
   else:
    text(pg,x+30,y+200,'下挥中段 · 缺项',27,WARN)
    text(pg,x+30,y+247,'v1、v2 均未通过',19,MUTED)
    text(pg,x+30,y+283,'失败稿未纳入本册，也不计入完成。',17,MUTED)
    text(pg,x+30,y+319,'本角色保留原有 2 个合格动作。',17,MUTED)
  text(pg,48,1281,e['selection_caveat'],16,WARN if e['id'] in ['001','002'] else MUTED)
  text(pg,48,1317,'完整画布等比展示；本页各姿势的显示大小不代表同一游戏尺度。',15,MUTED)
 for p,rect,target in pendinglinks:doc[p].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':target,'to':fitz.Point(0,0)})
 doc.set_toc([[1,'封面与十二种敌人',1],[1,'目录与使用说明',2]]+[[1,f"{e['id']} {e['name']}",i+3] for i,e in enumerate(rows)])
 doc.set_metadata({'title':'原创敌人设定集 v2 - 12母图与35独立动作','author':'Stoneshard Mod 原创概念','subject':'仅并入此前交付的11续姿；002缺项保留；非连续动画','keywords':'47唯一选稿,12母图,35独立动作,未进行游戏内验证'})
 out=HERE/'enemy_design_catalog_v2.pdf';doc.save(out,garbage=3,deflate=True);doc.close()
 # Verify saved PDF unassociated RGB and alpha, not merely a flattened visual rendering.
 doc=fitz.open(out);imagechecks=[];seen=set()
 for pg in doc:
  for img in pg.get_images(full=True):
   xref,smask=img[0],img[1]
   if xref in seen:continue
   seen.add(xref);rgb=Image.open(io.BytesIO(doc.extract_image(xref)['image'])).convert('RGB');alpha=Image.open(io.BytesIO(doc.extract_image(smask)['image'])).convert('L')
   rh=hashlib.sha256(rgb.tobytes()).hexdigest();ah=hashlib.sha256(alpha.tobytes()).hexdigest()
   matches=[r for r in rasterfiles if r['rgb_decoded_sha256']==rh and r['alpha_decoded_sha256']==ah]
   assert len(matches)==1,('RGB/alpha mismatch',xref)
   assert doc.xref_get_key(xref,'Interpolate')[1]=='false'
   imagechecks.append({'xref':xref,'smask':smask,'source_sha256':matches[0]['source_sha256'],'raster_path':matches[0]['raster_path'],'rgb_exact':True,'alpha_exact':True,'interpolate':False})
 assert len(imagechecks)==47
 # Decode validation primes MuPDF image caches; render in a fresh document for reproducible default viewing.
 doc.close();fitz.TOOLS.store_shrink(100);doc=fitz.open(out)
 rendered=HERE/'rendered';rendered.mkdir(exist_ok=True)
 pagechecks=[]
 for i,pg in enumerate(doc):
  outfile=rendered/f'page-{i+1:02d}.png';pg.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(outfile)
  spans=[s for b in pg.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
  assert all(pg.rect.contains(fitz.Rect(s['bbox'])) for s in spans)
  pagechecks.append({'page':i+1,'png':str(outfile.relative_to(HERE)),'sha256':sha(outfile),'bytes':outfile.stat().st_size,'all_text_in_page':True,'link_count':len(pg.get_links()),'visual_review':'pending'})
 # Coverage overview: all 47 selections in 12 cards, no old-only overview reused.
 ov=fitz.open();p=ov.new_page(width=1800,height=2040);p.insert_font(fontname='cn',fontfile=str(fontout));p.draw_rect(p.rect,color=None,fill=BG)
 text(p,45,70,'十二敌人 · 已选姿态覆盖概览',38);text(p,45,112,'12 母图 + 35 动作 = 47 张唯一选稿  |  并入此前已交付续姿 11 张  |  002 仍缺 1 项',21,ACCENT)
 for i,e in enumerate(rows):
  x=45+(i%3)*580;y=150+(i//3)*455
  p.draw_rect(fitz.Rect(x,y,x+550,y+428),color=LINE,fill=CARD,width=1)
  text(p,x+15,y+36,f"{e['id']}  {e['name']}",23)
  for j,a in enumerate([e['idle']]+e['actions']+[e['continuation']]):
   xx=x+10+j*135;box=fitz.Rect(xx,y+60,xx+125,y+330)
   if a:
    im=rasters[a['sha256']];scale=min(box.width/im.width,box.height/im.height);rw,rh=im.width*scale,im.height*scale
    target=fitz.Rect(box.x0+(box.width-rw)/2,box.y0+(box.height-rh)/2,box.x0+(box.width+rw)/2,box.y0+(box.height+rh)/2)
    if e['id'] in ['004','010']:p.draw_rect(box,color=None,fill=DARK)
    xr=p.insert_image(target,stream=pngbytes(im.convert('RGB')),mask=pngbytes(im.getchannel('A')));ov.xref_set_key(xr,'Interpolate','false')
   else:
    text(p,xx+18,y+190,'缺项',23,WARN);text(p,xx+9,y+218,'两版未过',15,WARN)
   text(p,xx+5,y+355,['母图','原动作 01','原动作 02','续姿'][j],15,MUTED)
  text(p,x+16,y+394,f"1 母图 / {e['independent_action_count']} 合格动作"+(' / 下挥中段缺项' if e['id']=='002' else ''),18,WARN if e['id']=='002' else ACCENT)
 text(p,45,2010,'本图是覆盖索引，非动作连续性或游戏实机验收。完整四格请查阅配套 14 页图册。',19,MUTED)
 p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(HERE/'enemy_twelve_coverage_overview_v2.png');ov.close()
 dump(HERE/'browser_raster_map.json',{'method':'full_canvas_proportional_nearest_neighbor_no_alpha_adjustment','images':rasterfiles})
 dump(HERE/'layout_checks.json',{'status':'automated_checks_pass_visual_review_pending','pages':14,'unique_source_images':47,'pdf_image_xobjects':47,'pdf_rgb_alpha_verification':imagechecks,'image_layouts':layout,'page_checks':pagechecks,'all_layouts_proportional':all(x['proportional'] for x in layout),'clickable_links':len(pendinglinks),'outline_entries':len(doc.get_toc()),'font_embedded':True,'crop':False,'stretch':False,'continuous_animation_verified':False,'runtimeIntegrated':False,'runtimeVerified':False})
 print(out,out.stat().st_size,'bytes; 47 embedded RGB+alpha checks pass; 14 pages rendered')
if __name__=='__main__':main()
