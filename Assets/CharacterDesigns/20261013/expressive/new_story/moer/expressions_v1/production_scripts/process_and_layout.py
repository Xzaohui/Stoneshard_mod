from pathlib import Path
import json,hashlib,datetime,base64
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path.cwd(); B=R/'Assets/CharacterDesigns/20261013/expressive'; J=json.loads((B/'new_story_audit/eleventh_four_expression_brief.json').read_text()); D=B/'new_story/eleventh_four_expressions_weier_ink_moer_delivery_v1'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def board(c,kind,bg,fg):
 d=B/'new_story'/c['slug']/'expressions_v1'; out=Image.new('RGBA',(1440,1050),bg);dr=ImageDraw.Draw(out)
 dr.text((45,20),c['name']+' · 两种可逆表情概念',font=ImageFont.truetype(font,34),fill=fg)
 dr.text((45,72),'单人全身 | 眉眼嘴区分 | 保留本人服装与道具',font=ImageFont.truetype(font,21),fill=fg)
 for i,e in enumerate(c['expressions']):
  p=d/'selected'/f"{e['key']}_transparent.png";im=Image.open(p).convert('RGBA');s=min(670/im.width,835/im.height);im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.NEAREST); x=25+i*720+(670-im.width)//2;out.alpha_composite(im,(x,140));dr.text((55+i*720,103),e['label_zh'],font=ImageFont.truetype(font,27),fill=fg)
 dr.text((45,1008),'静态美术提案；不表示任务结果、连续动画或游戏运行通过。',font=ImageFont.truetype(font,20),fill=fg)
 p=d/'review'/f"{c['slug']}_{kind}_board.png";out.convert('RGB').save(p);return p
all_info=[]
for c in J['characters'][:2]:
 d=B/'new_story'/c['slug']/'expressions_v1'; logs=[]
 for e in c['expressions']:
  key=e['key']+'_initial';raw=d/'raw'/f'{key}_raw.png'; ret=d/'raw'/f'{key}_tool_return.json';p=d/'prompts'/f'{key}_parameters.json';tm=d/'raw'/f'{key}_invocation_time.json';args=json.loads(p.read_text());r=json.loads(ret.read_text()); img=r['image_url'];encoded=img.split(',',1)[1];decoded=base64.b64decode(encoded);assert hashlib.sha256(decoded).hexdigest()==sha(raw),'Returned image payload mismatch'
  arr=np.array(Image.open(raw).convert('RGBA'));before=arr.copy();arr[arr[:,:,3]<=8]=[0,0,0,0];im=Image.fromarray(arr,'RGBA');out=d/'selected'/f"{e['key']}_transparent.png";im.save(out)
  assert np.array_equal(arr[before[:,:,3]>8],before[before[:,:,3]>8]);bbox=im.getbbox(); rec={'expression':e['key'],'label_zh':e['label_zh'],'attempt':'initial','actual_tool':'builtin image_gen.imagegen','time':json.loads(tm.read_text()),'parameters_path':str(p.relative_to(d)),'parameters_sha256':sha(p),'prompt_path':f'prompts/{key}.txt','prompt_sha256':sha(d/'prompts'/f'{key}.txt'),'inputs':[c['source_anchor'][k] for k in ['selected_raw','transparent']],'original_tool_return':str(ret.relative_to(d)),'original_tool_return_sha256':sha(ret),'raw':str(raw.relative_to(d)),'raw_sha256':sha(raw),'returned_image_base64_decodes_to_raw':True,'selected':str(out.relative_to(d)),'selected_sha256':sha(out),'selected_reason':'首稿候选，等待独立视觉复核；最终状态另由 FINAL_STATUS 绑定。','revision_calls_used':0,'technical':{'size':list(im.size),'mode':im.mode,'alpha_bbox':list(bbox),'alpha_zero_pixels':int((arr[:,:,3]==0).sum()),'alpha_hidden_rgb_zero':True,'pixels_alpha_le8_cleared':int(np.any(before!=arr,axis=2).sum()),'opaque_and_alpha_gt8_pixels_unchanged':True,'body_drawing_or_scaling':False,'palette_quantization':False}}
  logs.append(rec);all_info.append({'slug':c['slug'],'name':c['name'],**rec})
 save(d/'generation-log.json',{'tool_return_preservation':'完整原始返回对象原样序列化，不覆盖。data URL逐字保留，解码SHA与raw一致。','entries':logs})
 for kind,bg,fg in [('light',(240,235,222,255),(47,43,37,255)),('dark',(35,42,49,255),(235,233,224,255))]:board(c,kind,bg,fg)
 # Readback every source unchanged
 src=json.loads((d/'sources/source_index.json').read_text());assert all(sha(R/a['original_path'])==a['sha256']==sha(d/a['snapshot_path']) for a in src['files'])
 save(d/'QA-technical.json',{'status':'technical_pass_visual_pending','sources_verified':len(src['files']),'alpha_processing':'仅alpha≤8设为RGBA0；其他像素逐字节保留；隐藏RGB归零后再RGBA合成检查。','entries':[{'expression':l['expression'],**l['technical']} for l in logs],'runtime_verified':False})
(d/'ignore').exists()
# Combined four expressions on two backgrounds; layout scaling only.
combined=Image.new('RGB',(2400,1750));dr=ImageDraw.Draw(combined)
for row,(bg,fg,label) in enumerate([((240,235,222),(47,43,37),'浅色底'),((35,42,49),(235,233,224),'深色底')]):
 dr.rectangle((0,row*875,2400,row*875+874),fill=bg);dr.text((25,row*875+18),'韦珥 · 摩珥 | 表情概念 · '+label,font=ImageFont.truetype(font,30),fill=fg)
 for i,a in enumerate(all_info):
  dr.text((25+i*600,row*875+66),a['name']+' · '+a['label_zh'],font=ImageFont.truetype(font,25),fill=fg);p=B/'new_story'/a['slug']/'expressions_v1'/a['selected'];im=Image.open(p).convert('RGBA');s=min(565/im.width,720/im.height);im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.NEAREST);combined.paste(im,(i*600+(600-im.width)//2,row*875+109),im)
 dr.text((25,row*875+840),'仅静态可逆美术提案；非动画帧表或游戏运行验收。',font=ImageFont.truetype(font,19),fill=fg)
combined.save(D/'韦珥摩珥_四表情_中文浅深合板.png')
save(D/'review_candidate_index.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expressions':all_info,'boards':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for c in J['characters'][:2] for p in sorted((B/'new_story'/c['slug']/'expressions_v1/review').glob('*.png'))],'combined_board':{'path':str((D/'韦珥摩珥_四表情_中文浅深合板.png').relative_to(R)),'sha256':sha(D/'韦珥摩珥_四表情_中文浅深合板.png')}})
print([(a['expression'],a['raw_sha256'],a['selected_sha256'],a['technical']) for a in all_info])
