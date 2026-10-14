from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,datetime
root=Path(__file__).resolve().parents[5]; group=Path(__file__).resolve().parent
bp=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_brief.json';brief=json.loads(bp.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
observations={
'teman_A1_smooth_right_leather_sleeve':'左前臂跨身，左掌广面贴本人右侧皮袖，右臂低伸、右手松垂；两手分离，原帽网保持放下，双皮袖补缝绑结及双靴完整。',
'teman_A2_steady_hat_crown':'右肘抬到头旁，右掌贴原帽冠左上外表面，左手低垂；没有掀网摘帽，网后五官可读，帽网补丁、皮袖与双靴保持。',
'fx_cv4_nier_A1_gather_fur_coat_fronts':'两手分别握本侧胸下宽毛襟边，两前臂收回；两手之间的内衣与腰带可见，原短棍仍在画面左后腰，头手双靴完整。',
'fx_cv4_nier_A2_raise_right_arm_stretch':'右臂抬过头顶，松曲指组与头发留空，左掌贴本人左腰褂面；躯干轻侧倾、双靴平稳，原短棍仍收在画面左腰后。'}
items=[];count=0
for c in brief['characters']:
 if c['slug'] not in ['teman','fx_cv4_nier']:continue
 d=root/c['proposed_output_directory']; records=[]
 for p in c['plans']:
  k=p['key'];candidate=d/'review'/f'{k}_v1_transparent.png';sel=d/'selected'/f'{k}.png';shutil.copy2(candidate,sel)
  tech=json.loads((d/'review'/f'{k}_v1_technical_QA.json').read_text());args=d/'prompts'/f'{k}_v1_tool_args.json';raw=d/'raw'/f'{k}_v1_raw.png';ret=d/'raw'/f'{k}_v1_tool_return.json';prompt=d/'prompts'/f'{k}_v1.txt'; reference=root/c['mother_image']['transparent']
  provenance={'key':k,'version':'v1','mode':'builtin image_gen.imagegen','prompt_file':str(prompt.relative_to(root)),'prompt_sha256':sha(prompt),'arguments_file':str(args.relative_to(root)),'arguments_sha256':sha(args),'reference_files':[{'path':str(reference.relative_to(root)),'sha256':sha(reference),'role':'sole identity/age/style/prop anchor'}],'full_tool_return':str(ret.relative_to(root)),'full_tool_return_sha256':sha(ret),'includes_image_payload':True,'raw':str(raw.relative_to(root)),'raw_sha256':sha(raw),'selected':str(sel.relative_to(root)),'selected_sha256':sha(sel),'generation_budget':{'initial':1,'revisions':0},'prompt_saved_before_call':True,'brief_sha256':sha(bp),'technical_QA':tech}
  (d/'raw'/f'{k}_v1_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n')
  records.append({'key':k,'title_zh':p['title_zh'],'raw_actually_viewed':True,'transparent_actually_viewed':True,'light_actually_viewed':True,'dark_actually_viewed':True,'author_verdict':'pass','observation':observations[k],'revision_needed':False,'selected_path':str(sel.relative_to(root)),'selected_sha256':sha(sel)})
  items.append({'key':k,'path':str(sel.relative_to(root)),'sha256':sha(sel),'title_zh':p['title_zh']}); count+=1
 (d/'QA-author.json').write_text(json.dumps({'character':c['slug'],'schema_version':1,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'draw_teman_fx_cv4_nier_actions','scope':'Only static concepts; author check does not replace independent review','records':records,'nonblocking_notes':['忒曼raw最大alpha254为工具返回，浅深实图无可见背景穿透硬错。','细微像素与原物姿态变化只按动作可读性和身份判断，不作审美重抽。'],'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
 (d/'generation-log.json').write_text(json.dumps({'character':c['slug'],'initial_calls':2,'revision_calls':0,'blocked_calls':0,'selected_count':2,'tool':'builtin image_gen.imagegen','sequential_calls':True,'reviewer':'review_ninth_character_actions','initial_prompt_verbatim':True,'records':[{'key':p['key'],'version':'v1','tool_return':f"raw/{p['key']}_v1_tool_return.json",'raw':f"raw/{p['key']}_v1_raw.png",'selected':f"selected/{p['key']}.png"} for p in c['plans']]},ensure_ascii=False,indent=2)+'\n')
 # Full planning/source archive retained once in delivery bundle, not duplicated per character.
 # Per-character alpha-only script already archived before generation.
 (d/'README.md').write_text(f"# {c['name']}（{c['canonical_id']}）基础动作\n\n2张独立全身日常静态动作，均为内置imagegen首稿；0修订。\n\n"+'\n'.join('- '+r['title_zh']+'：'+r['observation'] for r in records)+'\n\n保持已审母图本人比例、衣装和原物件侧别。仅alpha≤8及隐藏RGB清理；无人体编辑、拉伸、量化或插帧。\n完整工具返回包含image_url payload。raw与返回payload逐字节核对。\nsource_hashes与sources保留母图、人物卡、对白、计划与来源SHA。联合交付planning_sources保留本组相关规划文本；角色sources/files按source_hashes保留相关源全文与图像。\n仅可逆美术概念；不代表连续动画、原生精灵、装备兼容、碰撞或游戏运行。\n')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';fhead=ImageFont.truetype(font,37);frow=ImageFont.truetype(font,28);flabel=ImageFont.truetype(font,24);ffoot=ImageFont.truetype(font,23)
layout={'canvas':[1800,1960],'method':'Complete source canvases, uniform nominal scale 0.5, nearest-neighbor; integer dimensions rounded only. No crop/stretch/anatomy edits.','placements':[],'backgrounds':{'light':[242,236,220,255],'dark':[31,36,44,255]}}
for kind,bg in layout['backgrounds'].items():
 board=Image.new('RGBA',(1800,1960),tuple(bg));draw=ImageDraw.Draw(board);fg=(42,40,36,255) if kind=='light' else (240,234,220,255)
 draw.text((36,26),'忒曼与佴珥 · 基础动作对照',font=fhead,fill=fg);draw.text((38,79),'本批 4 张独立静态动作 · 母图仅作身份与比例参考',font=flabel,fill=fg)
 for ri,c in enumerate([x for x in brief['characters'] if x['slug'] in ['teman','fx_cv4_nier']]):
  y=145+ri*860;draw.text((36,y),f"{c['name']} · {c['canonical_id']}",font=frow,fill=fg)
  paths=[root/c['mother_image']['transparent']]+[root/c['proposed_output_directory']/'selected'/f"{p['key']}.png" for p in c['plans']]
  labels=['已审母图（参考）']+['A'+str(i+1)+' '+p['title_zh'] for i,p in enumerate(c['plans'])]
  for ci,(p,label) in enumerate(zip(paths,labels)):
   im=Image.open(p).convert('RGBA');size=(round(im.width*.5),round(im.height*.5));thumb=im.resize(size,Image.Resampling.NEAREST);x=20+ci*600+(560-size[0])//2;iy=y+85
   draw.text((36+ci*600,y+47),label,font=flabel,fill=fg);board.alpha_composite(thumb,(x,iy))
   if kind=='light':layout['placements'].append({'source':str(p.relative_to(root)),'source_sha256':sha(p),'source_dimensions':list(im.size),'size':list(size),'xy':[x,iy],'label':label})
 draw.text((36,1905),'保留原衣装、原道具与身份 · 可逆美术提案 · 非连续动画或游戏运行验收',font=ffoot,fill=fg)
 out=group/f'teman_fx_cv4_nier_mother_actions_{kind}.png';board.convert('RGB').save(out)
layout['boards']=[{'path':str((group/f'teman_fx_cv4_nier_mother_actions_{k}.png').relative_to(root)),'sha256':sha(group/f'teman_fx_cv4_nier_mother_actions_{k}.png')} for k in ['light','dark']]
(group/'board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');(group/'selected_files.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'selected_count':count,'boards':layout['boards']},ensure_ascii=False))
