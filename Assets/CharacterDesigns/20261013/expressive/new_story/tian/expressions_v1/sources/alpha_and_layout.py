from pathlib import Path
import json,hashlib,shutil,re,datetime
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/CharacterDesigns/20261013/expressive/new_story'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
for s in ['tian','lein']:
 o=B/s/'expressions_v1';c=json.loads((o/'brief.json').read_text());calls=json.loads((o/'generation-calls.json').read_text());rows=[]
 for e,call in zip(c['expressions'],calls):
  key=e['key'];source=Path(re.search(r'as (/\S+\.png) by default',call['output_hint']).group(1));raw=o/'raw'/f'{key}_v1.png';shutil.copyfile(source,raw)
  assert call['args']['prompt']==(o/'prompts'/f'{key}_v1.txt').read_text().strip()
  a=np.array(Image.open(raw).convert('RGBA'));assert (a[:,:,3]==0).any();before=a.copy();a[a[:,:,3]<16]=0;a[a[:,:,3]==0,:3]=0
  selected=o/'selected'/f'{key}_transparent.png';im=Image.fromarray(a);im.save(selected)
  rows.append({'id':e['id'],'label_zh':e['label_zh'],'raw':str(raw.relative_to(o)),'raw_sha256':sha(raw),'selected':str(selected.relative_to(o)),'selected_sha256':sha(selected),'size':im.size,'bbox':im.getbbox(),'alpha_zero_pixels':int((a[:,:,3]==0).sum()),'hidden_RGB_nonzero_after':int(np.count_nonzero(a[a[:,:,3]==0,:3])),'cleanup':'Only zero RGBA where alpha<16 and hidden RGB where alpha=0; no visible RGB/body edits.','prompt':f'prompts/{key}_v1.txt','revision_count':0})
  call.update({'tool':'builtin image_gen.imagegen','generation_stage':'initial_v1','raw':str(raw.relative_to(o)),'raw_sha256':sha(raw),'selected_reason':'身份/脸部差别/道具侧别与剧情边界通过作者实看，待独审','recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'references':[{'path':p,'sha256':sha(Path(p))} for p in call['args']['referenced_image_paths']]})
 dump(o/'generation-log.json',calls)
 font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 for theme,bg,fg in [('light',(237,230,215),(47,40,35)),('dark',(31,36,42),(240,231,211))]:
  board=Image.new('RGB',(1700,1650),bg);dr=ImageDraw.Draw(board);dr.text((60,28),c['name']+' · 双情绪概念',font=ImageFont.truetype(font,52),fill=fg)
  for i,row in enumerate(rows):
   im=Image.open(o/row['selected']).convert('RGBA');im.thumbnail((800,1390),Image.Resampling.NEAREST);x=25+i*850+(800-im.width)//2;board.paste(im,(x,130),im);dr.text((65+i*850,1540),row['id']+' · '+row['label_zh'],font=ImageFont.truetype(font,40),fill=fg)
  board.save(o/'review'/f'{s}_expressions_{theme}.png')
 qa={'status':'author_pass_pending_independent','source_hashes_verified':True,'actual_viewed':['source raw','source transparent','each generated raw'],'face_findings':(['E1原微笑退去，内眉忧虑、小幅开口坦露害怕。','E2闭口中性唇线，稳眼倾听而非承诺。'] if s=='tian' else ['E1低眼闭口停顿、右手收腰，自省未画退款或获谅解。','E2抬眼闭口、右手较小幅摊掌，专注听路况未画放行。']),'identity':'保持母图成年女性脸型、发型、比例、材质与配色。','sides':c['fixed_prop_sides'],'story_limits':[e['condition_and_limit'] for e in c['expressions']],'selected_bindings':rows,'used_revision_count':0,'limit':'概念图，非原生网格、动画、装备兼容或游戏实现。'};dump(o/'QA-author.json',qa)
 (o/'README.md').write_text(f"# {c['name']}双情绪概念\n两张独立条件情绪，不是顺序剧情与完成结果。真实生成提示见prompts与generation-log；首稿、母图、卡/台本快照、浅深底与SHA均保留。实际使用builtin imagegen。处理仅透明低alpha及隐藏RGB清理、NEAREST等比排板。未修改原图、roster、游戏包或上传Git。\n")
 shutil.copyfile('/tmp/build_tian_lein.py',o/'sources/alpha_and_layout.py')
 shutil.copyfile(R/'AGENTS.md',o/'sources/AGENTS.md')
 print(s,rows)
