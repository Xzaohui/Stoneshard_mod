from pathlib import Path
import json,hashlib,datetime,argparse
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[5]; B=R/'Assets/CharacterDesigns/20261013/expressive'; O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--include-final-pair',action='store_true');arg=ap.parse_args()
names='mia sela mara ivo tor rhea nell sel sena kaem nara ena morlen leo'.split()
if arg.include_final_pair:names+=['lyd','hers']
labels={
'lyd':['从容核述','坚定发言'],'hers':['反问辩护','受挫停顿'],
'mia':['关切询问','认真倾听','温和鼓励'],'sela':['亲切招呼','认真解释','疑惑审视'],
'mara':['克制询问','警惕保留','稍松口气'],'ivo':['戒备倾听','艰难解释','坚定请求'],
 'tor':['压眉审视','开口质询','迟疑权衡'],'rhea':['警惕倾听','坚定提醒','柔和坚定'],
'nell':['戒备询问','不安发言','克制申明'],'sel':['试探劝说','紧绷反驳','忧虑侧望'],
'sena':['审慎立界','难过沉思','放松倾听'],'kaem':['防御辩解','紧张停顿','不满但克制'],
'nara':['警觉审视','疲惫求缓','克制申明'],'ena':['忧虑质问','担忧侧望','克制申明'],
'morlen':['疲惫关切','谨慎自述','克制异议'],'leo':['警觉质疑','迟疑权衡','平稳申明']}
notes={'lyd':'两态不代表证词获认可','hers':'第二态实际为短横口缝','mara':'表情克制，缩小时差异较小','ivo':'短胡茬较原锚略密','tor':'采用已交衣装修订选稿','rhea':'第三态脸颏和目光稍柔和','nell':'前两态头姿接近','sel':'第三态为侧望，不称明显低头','sena':'第三态眼型偏柔圆','kaem':'第三态仍保留不满感','nara':'第二态实际为短横气口','ena':'第三态颈巾与衣边轻漂','morlen':'第二态采用修订选稿','leo':'第三态采用粗簇修订选稿'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
roster=json.loads((B/'roster.json').read_text()); records=[]
for n in names:
 qa_path=B/n/'expressions_v1/QA-independent.json'; qa=json.loads(qa_path.read_text());status=qa['status']; assert status.startswith('pass')
 a=[];receipt=None
 for rp in sorted(B.glob('delivery*expressions*receipt.json')):
  rd=json.loads(rp.read_text())
  for item in rd.get('attachments',[]):
   p=Path(item['path']);p=R/p if not p.is_absolute() else p
   delivered_path=p
   if n in ['lyd','hers'] and p.parent.name=='lyd_hers_expressions_v1_delivery' and p.name.startswith(n+'_E'):
    assert sha(p)==item['sha256']
    p=B/n/'expressions_v1/selected'/p.name
   if f'/{n}/expressions_v1/' in str(p) and p.suffix=='.png' and not any(k in p.name for k in ['review','expressions_','white','black']):
    assert rd['state']=='sent';assert sha(p)==item['sha256'];receipt=(rp,rd)
    im=Image.open(p);assert im.mode=='RGBA' and im.getextrema()[3][0]==0
    a.append({'path':str(p.relative_to(R)),'delivered_path':str(delivered_path.relative_to(R)),'sha256':sha(p),'library_file_id':item.get('library_file_id'),'dimensions':list(im.size),'mode':im.mode,'receipt_state':'sent','approved_selection_basis':'delivered transparent PNG with independent QA pass'})
 assert len(a) in [2,3],(n,len(a))
 if n!='mia':a.sort(key=lambda x:x['path'])
 if n not in labels:
  man=json.loads((B/n/'expressions_v1/manifest.json').read_text()); labels[n]=[x.get('label',x.get('label_zh','条件表情')) for x in man['expressions']]
 for i,e in enumerate(a):e['actual_emotion_label']=labels[n][i]
 matches=[x for x in roster['characters'] if x.get('id')==qa.get('canonical_id',qa.get('character_id'))]
 if not matches:matches=[x for x in roster['characters'] if any('/'+n+'/' in p for p in x.get('new_design_paths',[]))]
 assert len(matches)==1,(n,len(matches));rr=matches[0]
 if receipt:
  rp,rd=receipt
  qrs=rd.get('qa_records',[])
  qr=next((q for q in qrs if q.get('path')==str(qa_path.relative_to(R))),None)
  expected=qr['sha256'] if qr else rd.get('qa_sha256')
  assert not expected or expected==sha(qa_path),(n,'QA hash mismatch')
 records.append({'slug':n,'display_name':rr['name'],'display_roman':{'morlen':'Morren','leo':'Rey'}.get(n,n.title()),'canonical_id':rr['id'],'roster_status':rr['status'],'qa':{'path':str(qa_path.relative_to(R)),'sha256':sha(qa_path),'status':status,'notes':qa.get('limitations',qa.get('visual_findings',qa.get('actual_visual_review',[])))},'receipt':{'path':str(rp.relative_to(R)),'sha256':sha(rp),'state':rd['state'],'message_id':rd['message_id']},'expressions':a,'page':2+len(records)//4})
W,H=1800,2600;BG='#f6f3ed';INK='#252b2d';MUT='#606763';ACC='#36544a'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def txt(d,pos,s,size=32,color=INK,b=False):d.text(pos,s,font=ImageFont.truetype(bold if b else font,size,index=2),fill=color)
def base(page,title,sub):
 im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im);txt(d,(85,68),title,52,b=True);txt(d,(85,145),sub,27,MUT);d.line((85,205,1715,205),fill='#b8c2bc',width=2);txt(d,(85,2520),'概念表情 · 条件备选 · 原稿未改变 · 已交范围',26,MUT);txt(d,(1550,2518),f'{page} / 5',28,MUT);return im,d
count=sum(len(r['expressions']) for r in records);final=arg.include_final_pair
im,d=base(1,'人物表情总览','现行已交选稿  /  2026.10.13  /  '+('冻结版' if final else '整理草稿'))
txt(d,(85,285),f'{len(records)} 位人物   {count} 张表情',66,ACC,b=True)
txt(d,(85,400),'按人物查找，横向比较眉眼与嘴形。',36)
txt(d,(85,470),'本册汇总已交概念表情，不是游戏原版资源或对齐动画。',31,MUT)
txt(d,(85,520),'条件备选互不串成剧情结局；不据此认定痊愈、认罪或授权。',31,MUT)
for group in range(4):
 y=680+group*330;rs=records[group*4:group*4+4]
 txt(d,(85,y),f'0{group+2}',62,ACC,b=True)
 txt(d,(265,y+6),' / '.join(r['display_roman'] for r in rs),44,b=True)
 txt(d,(265,y+90),'、'.join(r['display_name'] for r in rs),34,MUT)
 txt(d,(265,y+160),f'{len(rs)} 人 · {sum(len(r["expressions"]) for r in rs)} 张已交表情',29,MUT)
 if group==3 and not final:txt(d,(265,y+210),'预留 Lyd / Hers：等待最终核验与送达',29,MUT)
 d.line((85,y+280,1715,y+280),fill='#d6d9d2',width=2)
txt(d,(85,2220),'阅读说明',36,b=True)
txt(d,(85,2280),'使用已核验透明选稿，整图等比最近邻排版，不裁脸、不磨皮。',29,MUT)
txt(d,(85,2330),'原透明PNG保持原路径与字节；本册仅作便览，源稿不变。',29,MUT)
txt(d,(85,2380),'人物发簇、衣褶及头姿的既有概念差异与限制仍保留。',29,MUT)
im.save(O/'cover_index.png'); pages=[O/'cover_index.png'];placements=[]
for group in range(4):
 rs=records[group*4:group*4+4];im,d=base(group+2,' / '.join(r['display_roman'] for r in rs),'现行选稿  ·  每行同一人物  ·  情绪标签依据实际图像及独审')
 for row,r in enumerate(rs):
  top=235+row*555
  txt(d,(85,top+30),r['display_roman'],37,b=True);txt(d,(85,top+85),r['display_name'],28)
  txt(d,(85,top+142),'概念已交',25,ACC)
  note=notes.get(r['slug'],'保留既有人物与衣装')
  # Wrap the narrow left notes column deliberately.
  for z in range(0,len(note),7):txt(d,(85,top+205+(z//7)*36),note[z:z+7],24,MUT)
  for col,e in enumerate(r['expressions']):
   src=Image.open(R/e['path']).convert('RGBA');scale=min(442/src.width,440/src.height);size=(round(src.width*scale),round(src.height*scale));scaled=src.resize(size,Image.Resampling.NEAREST)
   x=350+col*455+(442-size[0])//2;y=top+10+(440-size[1])//2
   im.paste(scaled,(x,y),scaled);txt(d,(365+col*455,top+463),e['actual_emotion_label'],31)
   placements.append({'source':e['path'],'page':group+2,'position':[x,y],'size':list(size),'scale':scale,'resampling':'NEAREST','crop':None})
  d.line((85,top+539,1715,top+539),fill='#d6d9d2',width=2)
 if group==3 and not final:
  for row,n in enumerate(['Lyd','Hers'],2):
   y=235+row*555;txt(d,(85,y+60),n,37,b=True);txt(d,(350,y+70),'预留位置',39,MUT);txt(d,(350,y+135),'最终QA与实际送达确认后纳入，不展示在审素材。',29,MUT)
 path=O/f'page_{group+2:02d}.png';im.save(path);pages.append(path)
pdf=O/'expression_catalog_v1.pdf';c=canvas.Canvas(str(pdf),pagesize=(W/2,H/2));c.setTitle('人物表情总览');c.setAuthor('Character design project')
for p in pages:c.drawImage(ImageReader(str(p)),0,0,width=W/2,height=H/2);c.showPage()
c.save();assert pdf.stat().st_size<18*1024**2
idx={'schema_version':1,'status':'frozen_pending_catalog_visual_QA' if final else 'draft_pending_Lyd_Hers_final_QA_and_delivery','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Delivered supplementary expression concepts only; not original game resources, animation, new characters or narrative outcomes. Original transparent source files are unchanged.','counts':{'characters':len(records),'expressions':count,'pages':5},'source_indexes':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in [B/'roster.json',R/'Assets/CharacterActions/20261013/MASTER_SUPPLEMENT_INDEX.md']],'characters':records,'reserved':[] if final else [{'slug':n,'status':'excluded_pending_final_QA_and_delivery'} for n in ['lyd','hers']],'render_policy':{'full_selected_canvas':True,'cropped':False,'aspect_ratio':'preserved','resampling':'NEAREST','original_sources_mutated':False},'placements':placements,'outputs':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size} for p in [pdf,*pages]]}
(O/'reference_index.json').write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(idx['counts']),pdf.stat().st_size)
