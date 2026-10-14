from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile,datetime
ROOT=Path(__file__).resolve().parents[5]
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
br=json.loads((ROOT/'Assets/EnemyDesigns/reference/20261013/production_brief_second_six.json').read_text())
forbidden={r['sha256_at_retrieval'] for r in json.loads((ROOT/'Assets/EnemyDesigns/reference/20261013/sources_second_six.json').read_text())['public_visual_references']}
items=[]
for c in br['concepts']:
 d=ROOT/c['output_directory'];f=d/'FINAL_STATUS.json';s=json.loads(f.read_text());assert s.get('selected')==True or s.get('status')=='selected_static_concept_independently_reviewed',(f,s)
 manifest_expected=s.get('frozen_manifest_sha256',s.get('manifest_sha256'))
 if manifest_expected:assert sha(d/'manifest.json')==manifest_expected
 qa_expected=s.get('independent_QA_sha256',s.get('independent_qa_sha256'))
 if qa_expected:assert sha(d/'QA_INDEPENDENT.json')==qa_expected
 name=s.get('candidate',s.get('selected_file',s.get('selected_artifact',s.get('selected_transparent'))));p=(ROOT/name) if name.startswith('Assets/') else (d/name)
 assert p.exists();expected=s.get('candidate_sha256',s.get('selected_sha256'));assert not expected or sha(p)==expected
 im=Image.open(p).convert('RGBA');bbox=im.getchannel('A').getbbox();assert bbox and im.getchannel('A').getextrema()[0]==0 and im.getchannel('A').getextrema()[1]>0
 items.append({'concept_id':c['concept_id'],'category':c['category'],'name':c['working_name'],'path':str(p.relative_to(BASE)),'sha256':sha(p),'size_bytes':p.stat().st_size,'dimensions':im.size,'alpha_bbox':bbox,'directory':d,'image':im,'final_status_sha256':sha(f)})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',28)
smallfont=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
for variant,bg,fg in [('light',(233,228,216,255),(43,41,38)),('dark',(31,38,44,255),(225,227,220))]:
 board=Image.new('RGBA',(1800,1570),bg);draw=ImageDraw.Draw(board)
 draw.text((42,24),'第二组敌人外观 · 007—012',font=font,fill=fg)
 draw.text((42,65),'原创静态概念｜未游戏落地｜武器、脸与轮廓审查版',font=smallfont,fill=fg)
 for i,x in enumerate(items):
  col=i%3;row=i//3;left=col*600;top=110+row*700
  art=x['image'];factor=min(548/art.width,602/art.height);sz=(round(art.width*factor),round(art.height*factor));scaled=art.resize(sz,Image.Resampling.NEAREST)
  board.alpha_composite(scaled,(left+(600-sz[0])//2,top+(612-sz[1])//2))
  label=f"{x['concept_id'][-3:]} {x['name']}";draw.text((left+300,top+628),label,font=font,fill=fg,anchor='mt');draw.text((left+300,top+668),x['category']+' · 全身透明单体',font=smallfont,fill=fg,anchor='mt')
  x['board_display_size']=sz
 board.convert('RGB').save(OUT/f'second_six_overview_{variant}_zh.png')
archives=[]
for n in range(3):
 pair=items[n*2:n*2+2];ids='_'.join(x['concept_id'][-3:] for x in pair);zpath=OUT/f'second_six_sources_{ids}.zip';members=[]
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for x in pair:
   for p in sorted(x['directory'].rglob('*')):
    if not p.is_file():continue
    assert sha(p) not in forbidden,'Original reference copied: '+str(p)
    arc=str(p.relative_to(BASE));z.write(p,arc);members.append({'path':arc,'size_bytes':p.stat().st_size,'sha256':sha(p)})
  z.write(Path(__file__),'delivery_tools/build_delivery.py')
  members.append({'path':'delivery_tools/build_delivery.py','size_bytes':Path(__file__).stat().st_size,'sha256':sha(Path(__file__))})
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={v['path'] for v in members}
  for m in members:
   data=z.read(m['path']);assert hashlib.sha256(data).hexdigest()==m['sha256'];m['crc32']=f"{z.getinfo(m['path']).CRC:08x}"
 assert zpath.stat().st_size<18*1024*1024
 archives.append({'path':zpath.name,'sha256':sha(zpath),'size_bytes':zpath.stat().st_size,'crc_test':'passed','members':members})
record={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Second six original static concepts, not animation, canon or runtime.','status':'packaged_pending_board_visual_review','concept_count':6,'selected_concepts':[{k:v for k,v in x.items() if k not in ['directory','image']} for x in items],'archives':archives,'overview_images':[{'path':f'second_six_overview_{v}_zh.png','sha256':sha(OUT/f'second_six_overview_{v}_zh.png'),'size_bytes':(OUT/f'second_six_overview_{v}_zh.png').stat().st_size} for v in ['light','dark']],'attachment_plan':[x['path'] for x in items]+['delivery_v1/second_six_overview_light_zh.png']+['delivery_v1/'+a['path'] for a in archives],'attachment_count':10,'original_artwork_in_archives':False,'runtimeIntegrated':False,'runtimeVerified':False,'delivered_to_user':False,'body_redraw_in_packaging':False,'board_resizing':'proportional nearest-neighbor only'}
(OUT/'delivery.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'root':str(ROOT),'archives':[{k:v for k,v in a.items() if k!='members'} for a in archives]},ensure_ascii=False,indent=2))
