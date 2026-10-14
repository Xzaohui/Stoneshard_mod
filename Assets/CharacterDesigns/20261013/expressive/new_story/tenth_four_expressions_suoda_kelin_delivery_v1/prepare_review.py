import json,hashlib,re,shutil,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); B=R/'Assets/CharacterDesigns/20261013/expressive'; J=json.loads((B/'new_story_audit/tenth_four_expression_brief.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for slug in sys.argv[1:]:
 c=next(x for x in J['characters'] if x['slug']==slug);d=B/'new_story'/slug/'expressions_v1';times=json.loads((d/'prompts/invocation_times.json').read_text());calls=[];selected=[]
 for e in c['expressions']:
  stem=e['key']+'_initial';ap=d/'prompts'/(stem+'_tool_arguments.json');pp=d/'prompts'/(stem+'.txt');rp=d/'prompts'/(stem+'_tool_return.json');args=json.loads(ap.read_text());ret=json.loads(rp.read_text());assert args['prompt']==pp.read_text()==e['prompt_text'];original=Path(re.search(r'as (/.+?\.png) by default',ret['output_hint']).group(1));raw=d/'raw'/(stem+'_raw_imagegen.png');shutil.copy2(original,raw)
  im=Image.open(raw).convert('RGBA');a=np.array(im);clean=a.copy();clean[a[:,:,3]<=8]=0;sp=d/'selected'/(e['key']+'_transparent.png');Image.fromarray(clean).save(sp);assert np.array_equal(a[a[:,:,3]>8],clean[a[:,:,3]>8]);bbox=Image.fromarray((a[:,:,3]>8).astype('uint8')*255).getbbox()
  metrics={'mode':im.mode,'size':list(im.size),'alpha0_pixels':int((a[:,:,3]==0).sum()),'alpha0_nonzero_RGB_pixels':int(((a[:,:,3]==0)&(a[:,:,:3]!=0).any(axis=2)).sum()),'alpha1_8_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum()),'alpha9_254_pixels':int(((a[:,:,3]>8)&(a[:,:,3]<255)).sum()),'alpha_bbox_gt8':bbox}
  rc=d/'review/raw_composites';rc.mkdir(exist_ok=True)
  for tag,color in [('light','#ece7df'),('dark','#252a33')]:
   for ver,pic in [('raw',im),('selected',Image.open(sp).convert('RGBA'))]:Image.alpha_composite(Image.new('RGBA',pic.size,color),pic).convert('RGB').save(rc/(stem+'_'+ver+'_'+tag+'.png'))
  row={'expression':e['id'],'phase':'initial','stem':stem,**times[slug+'_'+e['id']],'prompt_path':str(pp.relative_to(d)),'prompt_sha256':sha(pp),'actual_tool_arguments_path':str(ap.relative_to(d)),'actual_tool_arguments_sha256':sha(ap),'tool_return_path':str(rp.relative_to(d)),'tool_return_sha256':sha(rp),'exact_prompt_read_from_disk_and_sent':True,'source_references':[{'path':p,'sha256':sha(Path(p))} for p in args['referenced_image_paths']],'output_original_path':str(original),'output_original_sha256':sha(original),'raw_path':str(raw.relative_to(d)),'raw_sha256':sha(raw),'selected_path':str(sp.relative_to(d)),'selected_sha256':sha(sp),'alpha_metrics':metrics,'selected_processing':'alpha <= 8 -> RGBA zero; alpha > 8 pixels unchanged; no crop, resize, quantization or anatomy edits','preserved_alpha_gt8_exact':True,'selection':'candidate_pending_author_and_independent_visual_review'};calls.append(row)
  selected.append({'key':e['key'],'label_zh':e['label_zh'],'path':str(sp.relative_to(d)),'sha256':sha(sp),'raw_path':str(raw.relative_to(d)),'raw_sha256':sha(raw),'size':list(im.size)})
 for tag,color,fg in [('light','#ece7df','#24201e'),('dark','#252a33','#eee8dc')]:
  board=Image.new('RGB',(1460,1160),color);draw=ImageDraw.Draw(board);draw.text((45,25),c['name']+' · 两种表情',font=ImageFont.truetype(font,38),fill=fg)
  for i,s in enumerate(selected):
   pic=Image.open(d/s['path']).convert('RGBA');scale=min(680/pic.width,940/pic.height);pic=pic.resize((round(pic.width*scale),round(pic.height*scale)),Image.Resampling.NEAREST);board.paste(pic,(i*730+(730-pic.width)//2,120+(940-pic.height)//2),pic);draw.text((i*730+50,1080),c['expressions'][i]['id']+' '+s['label_zh'],font=ImageFont.truetype(font,31),fill=fg)
  board.save(d/'review'/(slug+'_expressions_review_zh_'+tag+'.png'))
 write(d/'generation-log.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'generator':'builtin imagegen','calls':calls})
 write(d/'manifest.json',{'schema_version':1,'character_slug':slug,'name':c['name'],'canonical_id':c['canonical_id'],'status':'candidate_pending_independent_review','source_anchor':c['source_anchor'],'selected_count':2,'selected':selected,'all_raw':[{'path':x['raw_path'],'sha256':x['raw_sha256']} for x in calls],'generation_count':2,'revision_count':0,'not_claimed':J['delivery_plan']['not_claimed'],'files':[]})
 print(slug,[(x['key'],x['sha256']) for x in selected])
