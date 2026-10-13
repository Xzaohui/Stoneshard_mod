from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');bp=r/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_turnaround_toman_rey_01.json';b=json.loads(bp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for c in b['characters']:
 s=c['slug'];d=r/c['proposed_output_directory']; (d/'sources').mkdir(exist_ok=True)
 shutil.copy2(bp,d/'sources/production_brief.json')
 for x in c['source_cards']: shutil.copy2(r/x['path'],d/'sources'/Path(x['path']).name)
 a=r/c['current_anchor']['path'];shutil.copy2(a,d/'sources'/a.name)
 files=[]
 for v,stem in [('side',s+'_side_retry'),('back',s+'_back')]:
  raw=d/(stem+'_raw_imagegen.png');im=Image.open(raw).convert('RGBA');out=d/(s+'_'+v+'_transparent.png');shutil.copy2(raw,out)
  files.append({'view':v,'raw':raw.name,'transparent':out.name,'sha256':sha(raw),'canvas':im.size,'alpha_bbox':im.getbbox(),'alpha_extrema':im.getchannel('A').getextrema(),'alpha_processing':'none; original generated alpha preserved','selection':'retry1' if v=='side' else 'initial'})
 qa={'status':'author_review_complete_pending_independent','actual_viewed':['canonical anchor','all four initial views','both side retries'],'side_retry_reason':'首稿仅头部侧转，躯干仍前四分之三；一次针对性重绘后选择retry1。','new_selected_static_views':2,'new_characters':0,'raw_generations_preserved':3,'redo_limit_per_character':1,'checks':{'identity':'成熟脸与原锚大头短身、配色相近；没有机械拉伸','side':'重绘后躯干/足部侧向，远侧肩隐藏；概念近侧视非精密正交','back':'不露正脸；短衣、原持物手别保留','props':'单闭包/闭匣，未开；没有新增武器、徽号或剧情结果'},'minor_notes':['像素簇、边缘及衣片为生成概念，不是原生逐帧像素资产','匣侧视仍为斜向宽面，未冻结严格厚度；不声称精密正交'] if s=='leo' else ['侧视近手遮住部分包盖；远手行杖在轮廓前可读','兜帽背缝和肩布层次属设计推定'], 'back_design_inferences':c['back_design_inferences'],'historical_back_views_disclosure':b['historical_back_views_disclosure'],'runtime_verified':False,'equipment_compatibility_verified':False}
 (d/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 (d/'anchor_sources.json').write_text(json.dumps({'brief_sha256':sha(bp),'current_anchor':c['current_anchor'],'source_cards':c['source_cards'],'historical_reference':c['historical_reference'],'evidence_scope':c['evidence_scope']},ensure_ascii=False,indent=2))
 images=[Image.open(a).convert('RGBA'),Image.open(d/f'{s}_side_transparent.png').convert('RGBA'),Image.open(d/f'{s}_back_transparent.png').convert('RGBA')]
 for theme,bg,fg in [('light','#ece8df','#282621'),('dark','#252b34','#ece7dc')]:
  board=Image.new('RGB',(1800,1150),bg);dr=ImageDraw.Draw(board)
  def txt(x,y,t,size=26):dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=fg)
  txt(42,24,c['name']+'｜现行比例侧背补充设定',40)
  txt(42,83,'2 张新静态 · 0 新人物｜正面锚复用｜背结构为设计推定',26)
  for i,im in enumerate(images):
   # One common uniform factor preserves relative dimensions; no body deformation.
   im=im.resize((round(im.width*.53),round(im.height*.53)),Image.Resampling.NEAREST)
   board.paste(im,(i*590+(590-im.width)//2,168),im)
   txt(i*590+55,128,['已交正面锚（复用）','左侧视（补充）' if s=='toman' else '右侧视（补充）','正背视（补充）'][i],28)
  txt(42,955,'手别：右手木杖／左髋闭包；侧视近包远杖，背视右杖左包。' if s=='toman' else '手别：右手低提单个闭匣；侧视近右手，背视匣在画面右。')
  txt(42,1000,'旧比例已有背图；本次更新现行大头短身衣装，不是首次背面。')
  txt(42,1045,'仅静态概念｜非精密正交｜非动画或换装素材｜未进行游戏验证')
  if s=='leo':txt(42,1090,'观察备注：侧面闭匣仍略斜向展示；厚度与后侧连接尚未冻结。',23)
  board.save(d/f'{s}_turnaround_review_zh_{theme}.png')
 (d/'README.md').write_text(f'# {c["name"]}侧背补充设定\n\n新增2张静态，0新人物。正面锚只复用。两人旧比例均已有背面，本次更新现行成熟大头短身比例。\n\n选用side_retry原稿与back首稿；side首稿保留但不作为本次侧视交付。每人仅一次侧视针对性重绘。全部使用内置image_gen；透明件保留原始alpha、不作抠图或身体变形；检视板仅统一0.53最近邻等比缩放与排板。\n\n背面未知结构为设计推定。雷奥匣侧面仍略斜向，未冻结严格厚度。仅静态概念，不是精密正交、转身动画或已验证游戏素材。当前作者目检完成，等待独立审查。\n')
 manifest={'canonical_id':c['canonical_id'],'name':c['name'],'generator':'built-in image_gen','selected_views':files,'new_views':2,'new_characters':0,'raw_generations':3,'reference_reuse_count':1,'concept_only':True,'runtime_verified':False,'independent_review':'pending','files':[]}
 for p in sorted(d.rglob('*')):
  if p.is_file() and p.name!='manifest.json':manifest['files'].append({'path':str(p.relative_to(d)),'sha256':sha(p),'bytes':p.stat().st_size})
 (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print(s,'ready',d)
