from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import json,hashlib,shutil,sys,datetime
ROOT=Path(__file__).resolve().parents[7]
HERE=Path(__file__).resolve().parent
SLUG=HERE.parent.name
BRIEF=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/sixth_four_expression_brief.json'
B=json.loads(BRIEF.read_text()); C=next(c for c in B['characters'] if c['slug']==SLUG)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for e in C['expressions']:
    key=e['key']; src=HERE/'raw'/f'{key}_v1_raw.png'; dst=HERE/'selected'/f'{key}.png'
    shutil.copyfile(src,dst)
    im=Image.open(dst).convert('RGBA'); counts=Counter(im.getchannel('A').getdata())
    call=json.loads((HERE/'raw'/f'{key}_v1_call.json').read_text())
    prompt=HERE/'prompts'/f'{key}_v1.txt'; assert call['args']['prompt']==prompt.read_text()
    assert call['args']['prompt']==e['prompt_text']
    records.append({'key':key,'label_zh':e['label_zh'],'iteration':'initial','selected':True,'selection_reason':'首稿身份、道具与情绪成立；待独立复核。','prompt_path':str(prompt.relative_to(HERE)),'prompt_sha256':sha(prompt),'actual_call':call,'input_sha256':[{'path':v['path'],'sha256':v['sha256']} for k,v in C['source_anchor'].items() if k in ['selected_raw','selected_transparent']], 'raw':{'path':str(src.relative_to(HERE)),'sha256':sha(src)},'selected_artifact':{'path':str(dst.relative_to(HERE)),'sha256':sha(dst)},'postprocess':'Byte-for-byte copy. No alpha/RGB/geometry edits.','image':{'mode':im.mode,'size':list(im.size),'alpha_bbox':list(im.getchannel('A').getbbox()),'alpha_zero_pixels':counts[0],'alpha_opaque_pixels':counts[255],'alpha_partial_pixels':sum(v for k,v in counts.items() if k not in [0,255])}})
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for variant,bg,fg in [('light','#eee8db','#2d2b25'),('dark','#22272b','#ede7da')]:
    board=Image.new('RGB',(1536,1360),bg);d=ImageDraw.Draw(board)
    d.text((45,25),f"{C['name']} {C['canonical_id']}｜两种可逆表情",font=ImageFont.truetype(font,40),fill=fg)
    d.text((45,85),'人物表情概念 · 两图并非顺序结局',font=ImageFont.truetype(font,24),fill=fg)
    for i,e in enumerate(C['expressions']):
        im=Image.open(HERE/'selected'/f"{e['key']}.png").convert('RGBA')
        im.thumbnail((700,1050),Image.Resampling.NEAREST)
        board.paste(im,(i*768+(768-im.width)//2,160+(1050-im.height)//2),im)
        d.text((i*768+80,1225),f"{e['id']}  {e['label_zh']}",font=ImageFont.truetype(font,34),fill=fg)
    d.text((45,1300),'仅概念；不证明任务完成、付款、认领、托管或游戏运行。',font=ImageFont.truetype(font,24),fill=fg)
    board.save(HERE/'review'/f'{SLUG}_expressions_{variant}_board.png')
(HERE/'generation-log.json').write_text(json.dumps({'generator':'built-in image_gen.imagegen','brief_sha256':sha(BRIEF),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raws_retained':True,'budget':{'initial_per_expression':1,'revision_per_expression_max':1,'actual_calls':len(records),'revisions_used':0},'calls':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slug':SLUG,'records':len(records),'boards':[f'review/{SLUG}_expressions_{v}_board.png' for v in ['light','dark']]},ensure_ascii=False))
