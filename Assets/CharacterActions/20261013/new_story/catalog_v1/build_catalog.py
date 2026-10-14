#!/usr/bin/env python3
"""Build the 44-character browse catalogue without changing any source artwork.

Inputs: source_audit/selection_audit.json and the original repository assets.
Portable rebuild: use --use-embedded with this catalogue's production package.
Only nearest-neighbour proportional resizing is used for browse derivatives.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, os, re, sys, struct
from pathlib import Path
from collections import defaultdict
import fitz
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

HERE=Path(__file__).resolve().parent
ROOT=next((p for p in HERE.parents if (p/'AGENTS.md').exists()), None)
PAPER=(0.957,0.945,0.918)
INK=(0.145,0.180,0.173)
MUTED=(0.365,0.388,0.349)
ACCENT=(0.580,0.337,0.200)
BORDER=(0.797,0.812,0.757)
PANELS=[(0.885,0.910,0.840),(0.926,0.922,0.877),(0.926,0.922,0.877)]
W,H=720,1020
M=44
PANEL_W=(W-2*M-24)/3
BODY_TOPS=[101,538]
FONT_FILE=HERE/'production/fonts/NotoSansCJKsc-catalog.otf'
LAYOUT=[]
IMAGES=[]
FONTS={}
MISSING={
('turi','A1'):('持锤姿态未通过','暂缺，不展示失败稿'),
('cuoer','A1'):('钳具动作未通过','暂缺，不展示失败稿'),
('weier','A1'):('脚尖点地未通过','暂缺，不展示失败稿'),
('lier','A1'):('双绳尾收拢未通过','暂缺，不展示失败稿'),
}
NOTE_BY_SLUG={
'turi':'A1暂缺；A2采用通过审查的最终修订选稿。',
'cuoer':'A1暂缺；本页不展示两版未通过的试钳动作。',
'weier':'苇珥 FX-HOM：A1暂缺；与韦珥 FX-INK 为不同人物。',
'lier':'A1暂缺；双绳尾未同时收妥的失败稿不收入图册。',
'kuen':'保留坐姿与原有支撑；动作不代表病情或照护结果。',
'chenger':'保留坐姿支撑；动作不代表恢复行走或剧情完成。',
'wuer':'沿用母图短截状指端，不新增具体指位设定。',
'kuqi':'保留原斜背钩杆与腰绳；动作不代表伤势康复。',
'seer':'本页两张为动作；旧表情缺项不属于本册范围。',
'endai':'本页两张动作均已收录；旧表情缺项不属于本册范围。',
'weier_ink':'韦珥 FX-INK，与苇珥 FX-HOM 分人；旧钥匙在人物左腰。',
'suier':'燧珥 FX-CP1，与绥珥 FX-LOT 为不同人物。',
'suier_lot':'绥珥 FX-LOT，与燧珥 FX-CP1 分人；A1采用短尺修订稿。',
'moer':'摩珥 FX-WIL，与谟珥 FX-TRS 为不同人物。',
'moer_trs':'谟珥 FX-TRS，沿用最终v2背铲母图；裤膝浅斑为原崖灰。',
'fx_cv4_nier':'佴珥 FX-CV4，按独立人物身份与母图选稿。',
}
CAPTION_OVERRIDES={
'anni_A1':'调整袖口扣带','anni_A2':'合上当班簿子','kuen_A1':'轻拢披肩两缘','kuen_A2':'坐稳侧转身',
'sune_A1':'按稳槽中炭笔','sune_A2':'木板向内转抱','gura_A1':'折拢分段纸条','gura_A2':'收稳袋内短撬',
'turi_A2':'转看原角尺','vila_A1':'量规托架自检','vila_A2':'将量规收回袋中','tila_A1':'按稳外侧兜帽缘','tila_A2':'轻拢左侧裙摆',
'endai_A1':'理稳左腕甲','endai_A2':'按平右肩披风补片','kuqi_A1':'握稳上段背带','kuqi_A2':'托住垂挂绳圈',
'luomin_A1':'低位提灯','luomin_A2':'俯身放灯落地','wuer_A1':'轻理左上袖','wuer_A2':'半蹲右掌扶腿',
'fx_cv4_nier_A1':'轻拢毛褂前襟','fx_cv4_nier_A2':'抬右臂舒展','lier_A2':'右脚低抬回步','huier_A1':'右掌眉前遮光','huier_A2':'双手理稳背带',
'teman_A1':'轻理右皮袖','teman_A2':'轻扶原帽冠','kelin_A1':'横胸理左上袖','kelin_A2':'双手扶腰暂歇',
'hoer_A1':'按揉劳作手掌','hoer_A2':'双手扶腿倾听','erde_A1':'托住背篓底部','erde_A2':'按稳左护膝',
'cuoer_A2':'蹲姿轻叩轨条','deru_A1':'检查原钝凿','deru_A2':'拢围裙浅蹲','wadun_A1':'低握原短铲','wadun_A2':'扶膝调整蹲姿',
'suoda_A1':'双手托起原空篮','suoda_A2':'右掌轻扶头巾顶','weier_ink_A1':'双手提托原空杯','weier_ink_A2':'轻理右侧围裙',
'moer_A1':'抬旧账册至胸前','moer_A2':'旧账册垂至右腿旁',
}


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save_json(p,obj): Path(p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def read_json(p): return json.loads(Path(p).read_text(encoding='utf8'))
def rgb_hex(c): return tuple(round(v*255) for v in c)

def prepare_font(all_text, use_embedded=False):
    FONT_FILE.parent.mkdir(parents=True,exist_ok=True)
    if not use_embedded and not FONT_FILE.exists():
        f=TTFont('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',fontNumber=2)
        o=Options(); o.retain_gids=True; o.layout_features=['*']; o.notdef_glyph=True; o.notdef_outline=True; o.recalc_bounds=True
        sub=Subsetter(options=o); sub.populate(text=''.join(all_text)); sub.subset(f); f.recalcTimestamp=False; f.save(FONT_FILE)
    assert FONT_FILE.exists(),FONT_FILE
    FONTS['cjk']=fitz.Font(fontfile=str(FONT_FILE))
    FONTS['latin']=fitz.Font('helv')


def text(p,s,x,y,size=12,color=INK,font='cjk',align='left',max_width=None,role='body'):
    s=str(s)
    w=FONTS[font].text_length(s,fontsize=size)
    if max_width is not None and w>max_width+0.1:
        raise ValueError(f'Text exceeds allotted width: {s!r} ({w:.1f}>{max_width:.1f})')
    if align=='right': x-=w
    if align=='center': x-=w/2
    p.insert_text((x,y),s,fontname=font,fontsize=size,color=color)
    rect=[x,y-size*1.2,x+w,y+size*0.3]
    assert rect[0]>=-0.1 and rect[2]<=W+0.1 and rect[1]>=-0.1 and rect[3]<=H+0.1,(s,rect)
    LAYOUT.append({'page':p.number+1,'type':'text','role':role,'text':s,'rect':rect,'font_size':size})


def wrap(s,max_width,size):
    out=[]; line=''
    for ch in s:
        if FONTS['cjk'].text_length(line+ch,fontsize=size)>max_width:
            out.append(line); line=ch
        else: line+=ch
    if line: out.append(line)
    return out


def paragraph(p,s,x,y,width,size=12,leading=20,color=MUTED,max_lines=3):
    lines=wrap(s,width,size)
    assert len(lines)<=max_lines,(s,lines)
    for i,line in enumerate(lines): text(p,line,x,y+i*leading,size,color,max_width=width)
    return y+len(lines)*leading


def new_page(doc,n,total,section='基础动作'):
    p=doc.new_page(width=W,height=H)
    p.insert_font(fontname='cjk',fontfile=str(FONT_FILE))
    p.insert_font(fontname='latin',fontname_alias='latin') if False else None
    p.insert_font(fontname='latin',fontbuffer=FONTS['latin'].buffer)
    p.draw_rect(p.rect,fill=PAPER,color=None)
    if n>2:
        text(p,'新增剧情人物',M,39,12,INK,role='header')
        text(p,section,W-M,39,10,MUTED,align='right',role='header')
        text(p,'基础母图  +  两种独立关键姿态',M,66,10,MUTED)
    text(p,'动作浏览版 · 2026.10.14',M,H-24,9,MUTED,role='footer')
    text(p,f'{n:02d} / {total:02d}',W-M,H-24,10,MUTED,font='latin',align='right',role='footer')
    if n>2:
        text(p,'返回目录',W-M-84,H-24,9,ACCENT,align='right',role='footer')
        p.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(W-M-134,H-38,W-M-82,H-18),'page':1})
    return p


def prepare_images(assets,max_px,use_embedded=False):
    entries=[]
    emb=HERE/'production/embedded'; emb.mkdir(parents=True,exist_ok=True)
    old={a['key']:a for a in read_json(HERE/'production/embedded_manifest.json')['assets']} if use_embedded else {}
    for a in assets:
        key=f"{a['slug']}__{'M' if a['kind']=='concept' else a['action_id']}"
        target=emb/f'{key}.png'
        if use_embedded:
            r=old[key]
            assert sha(target)==r['embedded_sha256']
            with Image.open(target) as im: size=list(im.size)
        else:
            source=ROOT/a['path']
            assert sha(source)==a['sha256'],str(source)
            with Image.open(source) as source_im:
                im=source_im.convert('RGBA'); source_size=list(im.size)
                factor=min(1,max_px/max(im.size))
                size=[max(1,round(im.width*factor)),max(1,round(im.height*factor))]
                im=im.resize(size,Image.Resampling.NEAREST)
                im.save(target,compress_level=9)
            r={'key':key,'source_path':a['path'],'source_sha256':a['sha256'],'source_size':source_size,'embedded_size':size,'embedded_path':str(target.relative_to(HERE)),'embedded_sha256':sha(target),'resampling':'PIL.Image.Resampling.NEAREST','proportional_scale':factor,'visible_crop':False,'source_modified':False}
        a['embedded_path']=target; a['key']=key
        entries.append(r)
    save_json(HERE/'production/embedded_manifest.json',{'mode':'browse_derivatives_only','not_complete_original_source_collection':True,'max_dimension_px':max_px,'count':len(entries),'assets':entries})
    return entries


def png_idat(im):
    out=io.BytesIO(); im.save(out,format='PNG',compress_level=9)
    data=out.getvalue(); pos=8; chunks=[]
    while pos<len(data):
        n=struct.unpack('>I',data[pos:pos+4])[0]; tag=data[pos+4:pos+8]
        if tag==b'IDAT': chunks.append(data[pos+8:pos+8+n])
        pos+=n+12
    return b''.join(chunks)

OPTIMIZED=set()
def optimize_image_stream(doc,xref,path):
    if xref in OPTIMIZED: return
    OPTIMIZED.add(xref)
    im=Image.open(path).convert('RGBA'); w,h=im.size
    smask=doc.xref_get_key(xref,'SMask')
    doc.update_stream(xref,png_idat(im.convert('RGB')),compress=False)
    doc.xref_set_key(xref,'Filter','/FlateDecode')
    doc.xref_set_key(xref,'ColorSpace','/DeviceRGB')
    doc.xref_set_key(xref,'BitsPerComponent','8')
    doc.xref_set_key(xref,'DecodeParms',f'<< /Predictor 15 /Colors 3 /BitsPerComponent 8 /Columns {w} >>')
    if smask[0]=='xref':
        sx=int(smask[1].split()[0])
        doc.update_stream(sx,png_idat(im.getchannel('A')),compress=False)
        doc.xref_set_key(sx,'Filter','/FlateDecode')
        doc.xref_set_key(sx,'ColorSpace','/DeviceGray')
        doc.xref_set_key(sx,'BitsPerComponent','8')
        doc.xref_set_key(sx,'DecodeParms',f'<< /Predictor 15 /Colors 1 /BitsPerComponent 8 /Columns {w} >>')


def figure(p,a,rect,usage='body'):
    rect=fitz.Rect(rect)
    im=Image.open(a['embedded_path']); iw,ih=im.size
    scale=min(rect.width/iw,rect.height/ih)
    w,h=iw*scale,ih*scale
    actual=fitz.Rect(rect.x0+(rect.width-w)/2,rect.y0+(rect.height-h)/2,rect.x0+(rect.width+w)/2,rect.y0+(rect.height+h)/2)
    xref=p.insert_image(actual,filename=str(a['embedded_path']),keep_proportion=True)
    # Nearest-neighbour display preference, in addition to the nearest-only derivative.
    p.parent.xref_set_key(xref,'Interpolate','false')
    optimize_image_stream(p.parent,xref,a['embedded_path'])
    IMAGES.append({'page':p.number+1,'key':a['key'],'kind':a['kind'],'source_path':a['path'],'source_sha256':a['sha256'],'rect':list(actual),'allotted_rect':list(rect),'usage':usage,'xref':xref,'no_clipping':True,'preserved_aspect':True})


def cover(doc,chars,by_slug,total):
    p=new_page(doc,1,total)
    text(p,'STONESHARD MOD  /  CHARACTER COLLECTION',M,62,10,MUTED,font='latin')
    text(p,'新增剧情人物',M,139,40,INK,role='title')
    text(p,'基础动作图册',M,188,25,INK,role='subtitle')
    text(p,'44',M,305,84,INK,font='latin')
    text(p,'位人物',M+125,295,21,INK)
    text(p,'44 张基础母图',330,266,15,INK)
    text(p,'84 张合格动作',330,299,15,INK)
    paragraph(p,'收录44位人物的基础母图与84张合格非战斗姿态，便于逐人对照、浏览与检索。',M,356,W-2*M,14,24,max_lines=2)
    # Four existing mother images only; no new illustration.
    heroes=['anni','gura','luomin','moer_trs']
    for j,slug in enumerate(heroes):
        a=by_slug[slug]['concept']; x=M+j*158
        figure(p,a,[x,411,x+152,646],'cover')
        text(p,by_slug[slug]['character']['name'],x+76,666,12,INK,align='center')
    text(p,'阅读说明',M,729,17,INK)
    lines=[
      '40 人各有 2 张合格动作；另 4 人各有 1 张。',
      '缺项仅以文字占位，未收入未通过审查的图像。',
      '本册为独立关键姿态，未组成连续动画或完成装备适配。',
      '本册为浏览尺寸，原始透明图与完整素材见各批交付。',
      '制作审查通过不代表用户审美确认或游戏运行验收。',
    ]
    for j,s in enumerate(lines): text(p,s,M,764+j*27,12,MUTED,max_width=W-2*M)
    text(p,'点击目录中的姓名，可跳转至相应人物页。',M,944,11,ACCENT)


def contents(doc,chars,total):
    p=new_page(doc,2,total)
    text(p,'人物目录',M,89,29,INK,role='title')
    text(p,'按人物清单顺序收录 · 姓名与稳定 ID 双重定位',M,121,11,MUTED)
    colw=304
    for i,c in enumerate(chars):
        col=0 if i<22 else 1; row=i%22
        x=M+col*(colw+24); y=174+row*31.5
        no=i+1; page=3+i//2
        text(p,f'{no:02d}',x,y,10,ACCENT,font='latin')
        text(p,c['name'],x+28,y,13,INK)
        text(p,c['canonical_id'],x+92,y,9,MUTED,font='latin',max_width=146)
        text(p,f'{page:02d}',x+colw-8,y,11,INK,font='latin',align='right')
        p.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(x,y-18,x+colw,y+7),'page':page-1})
    text(p,'同音近名请以稳定 ID 为准。目录页码与 PDF 物理页码一致。',M,925,11,MUTED)
    text(p,'图里、锉珥、苇珥、栎珥的 A1 暂缺；不计入 84 张。',M,950,11,ACCENT)


def character_section(p,c,items,index,top):
    slug=c['slug']; name=c['name']; role=c.get('story_role') or ''
    text(p,f'{index:02d}',M,top+25,13,ACCENT,font='latin')
    text(p,name,M+31,top+25,25,INK,role='character_name')
    text(p,c['canonical_id'],W-M,top+21,11,MUTED,font='latin',align='right',role='canonical_id')
    text(p,role,M,top+52,11,MUTED,max_width=W-2*M)
    imgs=[items['concept'],items.get('A1'),items.get('A2')]
    for j,a in enumerate(imgs):
        x=M+j*(PANEL_W+12)
        box=fitz.Rect(x,top+76,x+PANEL_W,top+354)
        p.draw_rect(box,fill=PANELS[j],color=None)
        if a:
            figure(p,a,[x+4,top+78,x+PANEL_W-4,top+352])
            if j==0: label='M  基础母图'
            else: label=f"A{j}  {CAPTION_OVERRIDES.get(a['asset_id']) or a.get('label_zh') or '独立动作'}"
            text(p,label,x+PANEL_W/2,top+380,12,INK,align='center',max_width=PANEL_W-2,role='figure_label')
        else:
            missing=MISSING[(slug,f'A{j}')]
            text(p,f'A{j}  暂缺',x+PANEL_W/2,top+180,19,ACCENT,align='center')
            text(p,missing[0],x+PANEL_W/2,top+218,12,MUTED,align='center')
            text(p,missing[1],x+PANEL_W/2,top+244,11,MUTED,align='center')
            text(p,f'A{j}  未收录',x+PANEL_W/2,top+380,12,MUTED,align='center',role='figure_label')
    note=NOTE_BY_SLUG.get(slug,'原有身份、服装与随身物以基础母图为对照。')
    text(p,note,M,top+408,10,MUTED,max_width=W-2*M,role='character_note')


def build_pdf(chars,by_slug):
    doc=fitz.open(); total=2+math.ceil(len(chars)/2)
    # Precreate pages to make forward links valid, then work via temporary pages.
    for _ in range(total): doc.new_page(width=W,height=H)
    doc.delete_pages(0,total-1)
    cover(doc,chars,by_slug,total)
    # Forward links are attached after pages have been created.
    contents_link_specs=[]
    # create placeholders for remaining pages before contents links are inserted
    for _ in range(total-1): doc.new_page(width=W,height=H)
    # author contents and body in another document, preserving links only once complete
    contentdoc=fitz.open()
    # Simpler: use actual pages already created and replace new_page to consume them.
    global new_page
    original_new_page=new_page
    def existing_page(d,n,t,section='基础动作'):
        p=d[n-1]
        p.insert_font(fontname='cjk',fontfile=str(FONT_FILE))
        p.insert_font(fontname='latin',fontbuffer=FONTS['latin'].buffer)
        p.draw_rect(p.rect,fill=PAPER,color=None)
        if n>2:
            text(p,'新增剧情人物',M,39,12,INK,role='header')
            text(p,section,W-M,39,10,MUTED,align='right',role='header')
            text(p,'基础母图  +  两种独立关键姿态',M,66,10,MUTED)
        text(p,'动作浏览版 · 2026.10.14',M,H-24,9,MUTED,role='footer')
        text(p,f'{n:02d} / {t:02d}',W-M,H-24,10,MUTED,font='latin',align='right',role='footer')
        if n>2:
            text(p,'返回目录',W-M-84,H-24,9,ACCENT,align='right',role='footer')
            p.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(W-M-134,H-38,W-M-82,H-18),'page':1})
        return p
    new_page=existing_page
    contents(doc,chars,total)
    for i in range(0,len(chars),2):
        p=new_page(doc,3+i//2,total)
        for row,c in enumerate(chars[i:i+2]): character_section(p,c,by_slug[c['slug']],i+row+1,BODY_TOPS[row])
    new_page=original_new_page
    toc=[[1,'封面',1],[1,'人物目录',2]]
    for i in range(0,len(chars),2): toc.append([1,' / '.join(c['name'] for c in chars[i:i+2]),3+i//2])
    doc.set_toc(toc)
    doc.set_metadata({'title':'新增剧情人物基础动作图册','author':'Stoneshard Mod','subject':'44位人物 44张基础母图 84张合格动作','keywords':'角色,概念,动作,浏览版','creator':'catalog_v1/build_catalog.py','producer':'PyMuPDF','creationDate':'D:20261014031600Z','modDate':'D:20261014031600Z'})
    # CFF CID fonts are already subset with retained glyph IDs; a second subset can remap glyphs.
    out=HERE/'output/pdf/新增剧情人物44人_基础动作图册_v1.pdf'
    doc.save(out,garbage=4,deflate=True,deflate_images=True,deflate_fonts=True,no_new_id=True)
    doc.close()
    return out


def overview(chars,by_slug):
    cols=8; rows=math.ceil(len(chars)/cols); cw,ch=330,458; margin=60; head=180; foot=130
    im=Image.new('RGB',(cols*cw+margin*2,rows*ch+head+foot),rgb_hex(PAPER)); d=ImageDraw.Draw(im)
    font=lambda n: ImageFont.truetype(str(FONT_FILE),n)
    d.text((margin,35),'新增剧情人物 44人动作覆盖概览',font=font(48),fill=rgb_hex(INK))
    d.text((margin,106),'44基础母图 / 84合格动作 / 4处暂缺 · 编号与PDF目录对应',font=font(27),fill=rgb_hex(MUTED))
    for i,c in enumerate(chars):
        x=margin+(i%cols)*cw; y=head+(i//cols)*ch
        a=by_slug[c['slug']]['concept']
        d.rectangle((x+6,y+4,x+cw-10,y+310),fill=rgb_hex(PANELS[0]))
        src=Image.open(a['embedded_path']).convert('RGBA'); factor=min((cw-32)/src.width,296/src.height)
        src=src.resize((round(src.width*factor),round(src.height*factor)),Image.Resampling.NEAREST)
        im.paste(src,(round(x+(cw-src.width)/2),round(y+12+(296-src.height)/2)),src)
        d.text((x+cw/2,y+321),f'{i+1:02d}  {c["name"]}',anchor='mt',font=font(29),fill=rgb_hex(INK))
        d.text((x+cw/2,y+360),c['canonical_id'],anchor='mt',font=font(18),fill=rgb_hex(MUTED))
        for j,aid in enumerate(['A1','A2']):
            ok=aid in by_slug[c['slug']];bx=x+10+j*155
            d.rounded_rectangle((bx,y+394,bx+145,y+430),radius=5,fill=(218,232,216) if ok else (245,221,199))
            d.text((bx+72,y+399),aid+(' 已收录' if ok else ' 暂缺'),anchor='mt',font=font(22),fill=rgb_hex(INK if ok else ACCENT))
    d.text((margin,im.height-93),'图里、锉珥、苇珥、栎珥的A1暂缺，失败稿不展示、不计数。',font=font(27),fill=rgb_hex(ACCENT))
    d.text((margin,im.height-48),'仅展示母图与动作覆盖；独立姿态不代表连续动画、装备适配或游戏运行验收。',font=font(24),fill=rgb_hex(MUTED))
    out=HERE/'output/新增剧情人物44人_动作覆盖概览_v1.png'; im.save(out,compress_level=9); return out


def verify(pdf,assets,chars):
    doc=fitz.open(pdf); errors=[]; page_info=[]
    assert len(doc)==24
    body=[x for x in IMAGES if x['usage']=='body']
    assert len(body)==128 and len({x['key'] for x in body})==128
    for a in assets:
        if (a['slug'],a.get('action_id')) in MISSING:errors.append('Missing pose was included: '+a['asset_id'])
    if pdf.stat().st_size>=18*1024**2:errors.append('PDF too large')
    for p in doc:
        for t in p.get_text('dict')['blocks']:
            if t['type']!=0:continue
            for line in t['lines']:
                for span in line['spans']:
                    if not p.rect.contains(fitz.Rect(span['bbox'])):errors.append(f'out-of-page text page{p.number+1}: {span["text"]}')
        page_info.append({'page':p.number+1,'body_figures':sum(x['page']==p.number+1 for x in body),'text_characters':len(p.get_text()),'link_count':len(p.get_links())})
    assert len(doc[1].get_links())==44
    assert all(len(doc[n].get_links())==1 for n in range(2,24))
    report={'status':'AUTOMATED_PASS_PENDING_ALL_PAGE_VISUAL_REVIEW' if not errors else 'FAIL','errors':errors,'pdf_pages':24,'unique_source_images':128,'concepts':44,'actions':84,'people':44,'people_with_two_actions':40,'missing':[{'slug':s,'action':a} for s,a in MISSING],'originals_modified':False,'image_policy':'proportional nearest-neighbour browse derivative; no visible crop, redraw, stretch, colour adjustment or sharpening','qa_is_not_user_approval':True,'runtime_verified':False,'page_checks':page_info,'manual_review_required':'Every final page must be rendered and actually viewed before delivery.'}
    save_json(HERE/'LAYOUT_VERIFICATION.json',report)
    save_json(HERE/'production/layout_objects.json',{'text_objects':LAYOUT,'image_placements':IMAGES})
    doc.close(); assert not errors,errors
    return report


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--audit',type=Path,default=HERE/'source_audit/selection_audit.json'); ap.add_argument('--max-px',type=int,default=520); ap.add_argument('--use-embedded',action='store_true'); args=ap.parse_args()
    for rel in ['output/pdf','review','production/fonts','production/embedded']: (HERE/rel).mkdir(parents=True,exist_ok=True)
    data=read_json(args.audit); assets=data['assets']; chars=data['characters']
    if len(chars)!=44 or len(assets)!=128: raise ValueError('Final build requires exactly 44 people and 128 selected images.')
    by_slug=defaultdict(dict)
    for c in chars: by_slug[c['slug']]['character']=c
    for a in assets: by_slug[a['slug']]['concept' if a['kind']=='concept' else a['action_id']]=a
    for c in chars:
        assert by_slug[c['slug']]['concept']['canonical_id']==c['canonical_id']
    all_text=[Path(__file__).read_text(),json.dumps(data,ensure_ascii=False)]
    prepare_font(all_text,args.use_embedded)
    prepare_images(assets,args.max_px,args.use_embedded)
    pdf=build_pdf(chars,by_slug); ov=overview(chars,by_slug); report=verify(pdf,assets,chars)
    output={'pdf':{'path':str(pdf.relative_to(HERE)),'bytes':pdf.stat().st_size,'sha256':sha(pdf),'pages':24},'overview':{'path':str(ov.relative_to(HERE)),'bytes':ov.stat().st_size,'sha256':sha(ov)}}
    save_json(HERE/'OUTPUTS.json',output)
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
