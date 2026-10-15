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
PANELS=[(0.885,0.910,0.860),(0.926,0.922,0.877),(0.926,0.922,0.877)]
W,H=720,1020
M=44
PANEL_W=(W-2*M-24)/3
BODY_TOPS=[101,538]
FONT_FILE=HERE/'production/fonts/NotoSansCJKsc-catalog.otf'
LAYOUT=[]
IMAGES=[]
FONTS={}
MISSING={('endai','E2'):('比例审查未通过','暂缺，未收入问题稿'),('seer','E1'):('朝向审查未通过','修订未产图，暂缺')}
NOTE_BY_SLUG={
'anni':'表情为独立条件变体，护理身份与随身物沿用母图。',
'hoer':'E2变化较含蓄，可放大对照眼帘与嘴角。',
'kouer':'两张均使用最终闭口修订稿。',
'endai':'目前仅E1合格；E2比例未通过，保留文字空位。',
'fouer':'情绪变化含蓄，可放大对照眼帘与唇形。',
'lier':'E1保留窄牙色轻笑，不作大笑理解。',
'huier':'转头幅度较小，视线略向左上。',
'seer':'目前仅E2合格；E1首稿未通过，修订未产图。',
'daer':'E2保留不同画布比例，本页只作等比排版。',
'wuer':'旧短截指端不新增具体指位设定。',
'kuqi':'双腿完整不代表伤势已康复。',
'dalan':'E2警觉变化较轻，不作惊恐或攻击预备理解。',
'weier':'苇珥 FX-HOM，与韦珥 FX-INK 为不同人物。',
'weier_ink':'韦珥 FX-INK，与苇珥 FX-HOM 为不同人物。',
'suier':'燧珥 FX-CP1，与绥珥 FX-LOT 为不同人物。',
'suier_lot':'绥珥 FX-LOT，与燧珥 FX-CP1 为不同人物。',
'moer':'摩珥 FX-WIL，与谟珥 FX-TRS 为不同人物。',
'moer_trs':'沿用最终v2背铲母图；与摩珥 FX-WIL 分人。',
'fx_cv4_nier':'佴珥 FX-CV4，按独立人物身份与母图选稿。',
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


def new_page(doc,n,total,section='概念与表情'):
    p=doc.new_page(width=W,height=H)
    p.insert_font(fontname='cjk',fontfile=str(FONT_FILE))
    p.insert_font(fontname='latin',fontname_alias='latin') if False else None
    p.insert_font(fontname='latin',fontbuffer=FONTS['latin'].buffer)
    p.draw_rect(p.rect,fill=PAPER,color=None)
    if n>2:
        text(p,'新增剧情人物',M,39,12,INK,role='header')
        text(p,section,W-M,39,10,MUTED,align='right',role='header')
        text(p,'基础母图  +  两种独立表情',M,66,10,MUTED)
    text(p,'概念浏览版 · 2026.10.14',M,H-24,9,MUTED,role='footer')
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
        key=f"{a['slug']}__{'M' if a['kind']=='concept' else a['expression_id']}"
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
    text(p,'概念与表情图册',M,188,25,INK,role='subtitle')
    text(p,'44',M,305,86,INK,font='latin')
    text(p,'位人物',M+125,295,21,INK)
    text(p,'44 张基础母图',330,266,15,INK)
    text(p,'86 张合格表情',330,299,15,INK)
    paragraph(p,'收录已完成的基础概念与通过审查的独立表情，便于逐人浏览、对照和检索。',M,356,W-2*M,14,24,max_lines=2)
    # Four existing mother images only; no new illustration.
    heroes=['anni','gura','luomin','moer_trs']
    for j,slug in enumerate(heroes):
        a=by_slug[slug]['concept']; x=M+j*158
        figure(p,a,[x,411,x+152,646],'cover')
        text(p,by_slug[slug]['character']['name'],x+76,666,12,INK,align='center')
    text(p,'阅读说明',M,729,17,INK)
    lines=[
      '42 人各有 2 张合格表情；恩岱 E2 与瑟珥 E1 暂缺。',
      '缺项仅以文字占位，未收入未通过审查的图像。',
      '表情是独立条件变体，不是连续动画或剧情结果证明。',
      '本册为浏览尺寸，原始透明图与完整素材见各批交付。',
      '概念与审查通过不代表用户确认，也不代表游戏运行验收。',
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
    text(p,'恩岱 E2 · 瑟珥 E1 暂缺，其他 42 人均收录两张合格表情。',M,950,11,ACCENT)


def character_section(p,c,items,index,top):
    slug=c['slug']; name=c['name']; role=c.get('story_role') or ''
    text(p,f'{index:02d}',M,top+25,13,ACCENT,font='latin')
    text(p,name,M+31,top+25,25,INK,role='character_name')
    text(p,c['canonical_id'],W-M,top+21,11,MUTED,font='latin',align='right',role='canonical_id')
    text(p,role,M,top+52,11,MUTED,max_width=W-2*M)
    imgs=[items['concept'],items.get('E1'),items.get('E2')]
    for j,a in enumerate(imgs):
        x=M+j*(PANEL_W+12)
        box=fitz.Rect(x,top+76,x+PANEL_W,top+354)
        p.draw_rect(box,fill=PANELS[j],color=None)
        if a:
            figure(p,a,[x+4,top+78,x+PANEL_W-4,top+352])
            if j==0: label='M  基础母图'
            else: label=f"E{j}  {a.get('label_zh') or '独立表情'}"
            text(p,label,x+PANEL_W/2,top+380,12,INK,align='center',max_width=PANEL_W-2,role='figure_label')
        else:
            missing=MISSING[(slug,f'E{j}')]
            text(p,f'E{j}  暂缺',x+PANEL_W/2,top+180,19,ACCENT,align='center')
            text(p,missing[0],x+PANEL_W/2,top+218,12,MUTED,align='center')
            text(p,missing[1],x+PANEL_W/2,top+244,11,MUTED,align='center')
            text(p,f'E{j}  未收录',x+PANEL_W/2,top+380,12,MUTED,align='center',role='figure_label')
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
    def existing_page(d,n,t,section='概念与表情'):
        p=d[n-1]
        p.insert_font(fontname='cjk',fontfile=str(FONT_FILE))
        p.insert_font(fontname='latin',fontbuffer=FONTS['latin'].buffer)
        p.draw_rect(p.rect,fill=PAPER,color=None)
        if n>2:
            text(p,'新增剧情人物',M,39,12,INK,role='header')
            text(p,section,W-M,39,10,MUTED,align='right',role='header')
            text(p,'基础母图  +  两种独立表情',M,66,10,MUTED)
        text(p,'概念浏览版 · 2026.10.14',M,H-24,9,MUTED,role='footer')
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
    doc.set_metadata({'title':'新增剧情人物概念与表情图册','author':'Stoneshard Mod','subject':'44位人物 44张基础母图 86张合格表情','keywords':'角色,概念,表情,浏览版','creator':'catalog_v1/build_catalog.py','producer':'PyMuPDF','creationDate':'D:20261014031600Z','modDate':'D:20261014031600Z'})
    # CFF CID fonts are already subset with retained glyph IDs; a second subset can remap glyphs.
    out=HERE/'output/pdf/新增剧情人物44人_概念与表情图册_v1.pdf'
    doc.save(out,garbage=4,deflate=True,deflate_images=True,deflate_fonts=True,no_new_id=True)
    doc.close()
    return out


def overview(chars,by_slug):
    cols=8; rows=math.ceil(len(chars)/cols); cw,ch=330,420; margin=60; head=180; foot=100
    im=Image.new('RGB',(cols*cw+margin*2,rows*ch+head+foot),rgb_hex(PAPER)); d=ImageDraw.Draw(im)
    font=lambda n: ImageFont.truetype(str(FONT_FILE),n)
    d.text((margin,39),'新增剧情人物 44人母图总览',font=font(48),fill=rgb_hex(INK))
    d.text((margin,109),'概念浏览版 · 44基础母图 / 86合格表情 · 人物编号与PDF目录对应',font=font(24),fill=rgb_hex(MUTED))
    for i,c in enumerate(chars):
        x=margin+(i%cols)*cw; y=head+(i//cols)*ch
        a=by_slug[c['slug']]['concept']
        d.rectangle((x+6,y+4,x+cw-10,y+330),fill=rgb_hex(PANELS[0]))
        src=Image.open(a['embedded_path']).convert('RGBA'); factor=min((cw-32)/src.width,316/src.height)
        src=src.resize((round(src.width*factor),round(src.height*factor)),Image.Resampling.NEAREST)
        im.paste(src,(round(x+(cw-src.width)/2),round(y+12+(316-src.height)/2)),src)
        d.text((x+cw/2,y+342),f'{i+1:02d}  {c["name"]}',anchor='mt',font=font(29),fill=rgb_hex(INK))
        d.text((x+cw/2,y+383),c['canonical_id'],anchor='mt',font=font(18),fill=rgb_hex(MUTED))
    d.text((margin,im.height-64),'恩岱E2、瑟珥E1暂缺；此总览仅展示基础母图。概念不代表游戏运行验收。',font=font(24),fill=rgb_hex(MUTED))
    out=HERE/'output/新增剧情人物44人_母图总览_v1.png'; im.save(out,compress_level=9)
    return out


def verify(pdf,assets,chars):
    doc=fitz.open(pdf); errors=[]; page_info=[]
    text_all='\n'.join(p.get_text() for p in doc)
    for c in chars:
        if c['name'] not in text_all or c['canonical_id'] not in text_all: errors.append('missing text '+str(c))
    if len(doc)!=24: errors.append(f'page count {len(doc)}')
    if len(assets)!=130: errors.append(f'asset count {len(assets)}')
    body=[x for x in IMAGES if x['usage']=='body']
    if len(body)!=130 or len({x['key'] for x in body})!=130: errors.append('body unique image mismatch')
    if len([a for a in assets if a['kind']=='concept'])!=44: errors.append('concept count')
    if len([a for a in assets if a['kind']=='expression'])!=86: errors.append('expression count')
    if any(a['slug']=='endai' and a.get('expression_id')=='E2' for a in assets): errors.append('blocked Endai E2')
    if any(a['slug']=='seer' and a.get('expression_id')=='E1' for a in assets): errors.append('blocked Seer E1')
    if pdf.stat().st_size>=18*1024**2: errors.append(f'PDF too large: {pdf.stat().st_size}')
    for p in doc:
        for t in p.get_text('dict')['blocks']:
            if t['type']!=0: continue
            for line in t['lines']:
                for span in line['spans']:
                    r=fitz.Rect(span['bbox'])
                    if not p.rect.contains(r): errors.append(f'out-of-page text page{p.number+1}: {span["text"]}')
        page_info.append({'page':p.number+1,'body_figures':sum(x['page']==p.number+1 for x in body),'text_characters':len(p.get_text()),'link_count':len(p.get_links())})
    report={'status':'AUTOMATED_PASS_PENDING_ALL_PAGE_VISUAL_REVIEW' if not errors else 'FAIL','errors':errors,'pdf_pages':len(doc),'unique_source_images':len(assets),'concepts':44,'expressions':86,'people':44,'people_with_two_expressions':42,'missing':[{'slug':'endai','expression':'E2','reason':'proportion review failed'},{'slug':'seer','expression':'E1','reason':'first draft orientation failed; revision produced no image'}],'originals_modified':False,'image_policy':'proportional nearest-neighbour browse derivative; no visible crop, redraw, stretch, colour adjustment or sharpening','qa_is_not_user_approval':True,'runtime_verified':False,'page_checks':page_info,'manual_review_required':'Every final page must be rendered and actually viewed before delivery.'}
    save_json(HERE/'LAYOUT_VERIFICATION.json',report)
    save_json(HERE/'production/layout_objects.json',{'text_objects':LAYOUT,'image_placements':IMAGES})
    doc.close()
    if errors: raise AssertionError(errors)
    return report


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--audit',type=Path,default=HERE/'source_audit/selection_audit.json'); ap.add_argument('--max-px',type=int,default=520); ap.add_argument('--use-embedded',action='store_true'); args=ap.parse_args()
    for rel in ['output/pdf','review','production/fonts','production/embedded']: (HERE/rel).mkdir(parents=True,exist_ok=True)
    data=read_json(args.audit); assets=data['assets']; chars=data['characters']
    if len(chars)!=44 or len(assets)!=130: raise ValueError('Final build requires exactly 44 people and 130 selected images.')
    by_slug=defaultdict(dict)
    for c in chars: by_slug[c['slug']]['character']=c
    for a in assets: by_slug[a['slug']]['concept' if a['kind']=='concept' else a['expression_id']]=a
    for c in chars:
        assert by_slug[c['slug']]['concept']['canonical_id']==c['canonical_id']
    static=['新增剧情人物','概念与表情图册','人物目录','按人物清单顺序收录 · 姓名与稳定 ID 双重定位','概念浏览版 · 2026.10.14','基础母图  +  两种独立表情','返回目录','阅读说明','收录已完成的基础概念与通过审查的独立表情，便于逐人浏览、对照和检索。','42 人各有 2 张合格表情；恩岱 E2 与瑟珥 E1 暂缺。','缺项仅以文字占位，未收入未通过审查的图像。','表情是独立条件变体，不是连续动画或剧情结果证明。','本册为浏览尺寸，原始透明图与完整素材见各批交付。','概念与审查通过不代表用户确认，也不代表游戏运行验收。','点击目录中的姓名，可跳转至相应人物页。','同音近名请以稳定 ID 为准。目录页码与 PDF 物理页码一致。','恩岱 E2 · 瑟珥 E1 暂缺，其他 42 人均收录两张合格表情。','原有身份、服装与随身物以基础母图为对照。','新增剧情人物 44人母图总览','概念浏览版 · 44基础母图 / 86合格表情 · 人物编号与PDF目录对应','恩岱E2、瑟珥E1暂缺；此总览仅展示基础母图。概念不代表游戏运行验收。','0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz /+·；，。()暂缺未收录独立表情张位人物合格基础母图']
    all_text=static+list(NOTE_BY_SLUG.values())+[v for tup in MISSING.values() for v in tup]+[json.dumps(x,ensure_ascii=False) for x in chars]+[a.get('label_zh') or '' for a in assets]
    prepare_font(all_text,args.use_embedded)
    prepare_images(assets,args.max_px,args.use_embedded)
    pdf=build_pdf(chars,by_slug); ov=overview(chars,by_slug); report=verify(pdf,assets,chars)
    output={'pdf':{'path':str(pdf.relative_to(HERE)),'bytes':pdf.stat().st_size,'sha256':sha(pdf),'pages':24},'overview':{'path':str(ov.relative_to(HERE)),'bytes':ov.stat().st_size,'sha256':sha(ov)}}
    save_json(HERE/'OUTPUTS.json',output)
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
