from pathlib import Path
import json,hashlib,base64,datetime,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Assets/CharacterDesigns/20261013/expressive/new_story').is_dir())
BASE=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story'
DEL=BASE/'eleventh_four_expressions_daier_moer_trs_delivery_v1'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
times={x['key']:x for x in json.loads((DEL/'generation-times.json').read_text())}
font=ImageFont.truetype(FONT,30);small=ImageFont.truetype(FONT,23)
entries=[]
for slug in ['daier','moer_trs']:
 d=BASE/slug/'expressions_v1'
 if not d.exists(): continue
 if (d/'FINAL_STATUS.json').exists(): raise RuntimeError('Frozen assets must not be overwritten. Work in a new version directory.')
 c=json.loads((d/'brief-character.json').read_text()); log=[];alpha=[]
 for e in c['expressions']:
  k=e['key'];p=d/'raw'/f'{k}_v1_raw_imagegen.png';im=Image.open(p).convert('RGBA');a=np.array(im);before=a.copy()
  # Alpha cleanup only: harden generated coverage, neutralize invisible RGB. No drawing, quantizing, resizing, or body transformation.
  a[:,:,3]=np.where(a[:,:,3]>=128,255,0).astype('uint8');a[a[:,:,3]==0,:3]=0
  out=d/'selected'/f'{k}_transparent.png';Image.fromarray(a).save(out)
  rp=d/'tool_returns'/f'{k}_v1_original_tool_return.json';r=json.loads(rp.read_text());decoded=base64.b64decode(r['image_url'].split(',',1)[1]);assert decoded==p.read_bytes()
  ap=d/'prompts'/f'{k}_v1_tool_arguments.json';args=json.loads(ap.read_text());assert args['prompt']==(d/'prompts'/f'{k}_v1.txt').read_text()
  inputs=[{'path':str(Path(x).relative_to(ROOT)),'sha256':sha(Path(x))} for x in args['referenced_image_paths']]
  item={'expression':k,'label_zh':e['label_zh'],'tool':'image_gen.imagegen','attempt':'v1_initial','arguments':args,'arguments_file':str(ap.relative_to(d)),'arguments_sha256':sha(ap),'prompt_file':f'prompts/{k}_v1.txt','prompt_sha256':sha(d/'prompts'/f'{k}_v1.txt'),'inputs':inputs,**times[k],'original_tool_return':str(rp.relative_to(d)),'original_tool_return_sha256':sha(rp),'tool_output_hint':r['output_hint'],'decoded_return_bytes_match_raw':True,'raw':str(p.relative_to(d)),'raw_sha256':sha(p),'selected':str(out.relative_to(d)),'selected_sha256':sha(out),'selection_reason':'首稿形成指定可逆面部表情，保留母图身份、道具与主要手位；透明清理后待独审。','revisions_used':0}
  log.append(item)
  alpha.append({'expression':k,'canvas':list(im.size),'raw_mode':'RGBA','raw_sha256':sha(p),'selected_sha256':sha(out),'raw_alpha0_pixels':int((before[:,:,3]==0).sum()),'raw_alpha0_nonzero_rgb_pixels':int(((before[:,:,3]==0)&(before[:,:,:3].max(2)>0)).sum()),'raw_semialpha_pixels':int(((before[:,:,3]>0)&(before[:,:,3]<255)).sum()),'selected_alpha_values':np.unique(a[:,:,3]).tolist(),'visible_pixels':int((a[:,:,3]>0).sum()),'alpha_bbox':Image.fromarray(a[:,:,3]).getbbox(),'hidden_rgb_zeroed':True,'visible_rgb_preserved':bool(np.array_equal(before[a[:,:,3]>0,:3],a[a[:,:,3]>0,:3])),'method':'alpha threshold 128; zero invisible RGB; no body redraw/rescale/quantization','imagegen_rgb_altered_on_visible_pixels':False})
  entries.append((c['name'],e['label_zh'],out,slug,k))
 (d/'generation-log.json').write_text(json.dumps({'character':slug,'tool_mode':'builtin','calls':log},ensure_ascii=False,indent=2)+'\n')
 (d/'alpha-QA.json').write_text(json.dumps(alpha,ensure_ascii=False,indent=2)+'\n')
 for theme,bg,fg in [('light',(239,235,222,255),(37,35,34,255)),('dark',(32,38,46,255),(234,230,217,255))]:
  board=Image.new('RGBA',(1180,825),bg);draw=ImageDraw.Draw(board)
  draw.text((24,16),f'{c["name"]}｜两种可逆表情 · '+('浅底' if theme=='light' else '深底'),font=font,fill=fg)
  for i,e in enumerate(c['expressions']):
   selected=Image.open(d/'selected'/f'{e["key"]}_transparent.png').convert('RGBA');selected=selected.resize((559,704),Image.Resampling.NEAREST)
   board.alpha_composite(selected,(i*580+15,65));draw.text((i*580+25,774),e['label_zh'],font=font,fill=fg)
  board.convert('RGB').save(d/'review'/f'{slug}_{theme}_board.png')
 # RGBA-visible raw proof, separate from RGB data: both backgrounds are alpha-composited.
 proof=Image.new('RGBA',(2236,790),(239,235,222,255));dr=ImageDraw.Draw(proof)
 for i,e in enumerate(c['expressions']):
  raw=Image.open(d/'raw'/f'{e["key"]}_v1_raw_imagegen.png').convert('RGBA').resize((559,704),Image.Resampling.NEAREST)
  for j,bg in enumerate([(239,235,222,255),(32,38,46,255)]):
   pan=Image.new('RGBA',(559,704),bg);pan.alpha_composite(raw);proof.alpha_composite(pan,((i*2+j)*559,56));dr.text(((i*2+j)*559+12,12),f'{e["label_zh"]} raw '+('浅' if j==0 else '深'),font=font,fill=(40,40,40,255))
 proof.convert('RGB').save(d/'review'/f'{slug}_raw_rgba_visible_composite.png')
 shutil.copyfile(__file__,d/'prepare_assets.py')
board=Image.new('RGBA',(2320,1690),(239,235,222,255))
for row,(bg,fg,name) in enumerate([((239,235,222,255),(37,35,34,255),'浅底'),((32,38,46,255),(234,230,217,255),'深底')]):
 pan=Image.new('RGBA',(2320,845),bg);dr=ImageDraw.Draw(pan);dr.text((25,15),'岱珥 · 谟珥｜四种可逆表情 · '+name,font=font,fill=fg)
 for i,(n,l,p,s,k) in enumerate(entries):
  im=Image.open(p).convert('RGBA').resize((559,704),Image.Resampling.NEAREST);pan.alpha_composite(im,(i*580+10,67));dr.text((i*580+25,780),n+'｜'+l,font=font,fill=fg)
 board.alpha_composite(pan,(0,row*845))
board.convert('RGB').save(DEL/'岱珥谟珥_四表情_中文浅深合板.png')
print('Prepared selected PNGs, logs, and boards.');print(ROOT)
for _,_,p,_,_ in entries: print(p.relative_to(ROOT),sha(p))
