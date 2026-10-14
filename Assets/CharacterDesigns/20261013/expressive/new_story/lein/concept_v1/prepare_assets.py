from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
brief=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_four_production_brief.json'
b=json.loads(brief.read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for c in b['characters'][2:]:
 who=c['production_brief']['working_slug']; version=2 if who=='tian' else 1; d=root/c['recommended_output_directory']; raw=d/f'{who}_v{version}_raw_imagegen.png'
 im=Image.open(raw).convert('RGBA'); src=list(im.getdata()); changed=sum(0<p[3]<=8 for p in src); hidden=sum(p[3]<=8 and p[:3]!=(0,0,0) for p in src); im.putdata([(0,0,0,0) if p[3]<=8 else p for p in src]); out=d/f'{who}_transparent.png';im.save(out)
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',32); small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
 for theme,col,ink in [('light',(238,232,218,255),(42,38,33)),('dark',(36,41,43,255),(236,226,208))]:
  board=Image.new('RGBA',(im.width+120,im.height+170),col);board.alpha_composite(im,(60,100));dr=ImageDraw.Draw(board);dr.text((45,23),f'{c["name"]}  {c["canonical_id"]}',font=font,fill=ink);dr.text((45,board.height-48),'人物全身概念 · 剧情姿态研究 · 非游戏运行资源',font=small,fill=ink);board.convert('RGB').save(d/f'{who}_{theme}_board.png')
 shutil.copy2('/tmp/prepare_tian_lein.py',d/'prepare_assets.py')
 references=[]
 for x in [c['current_card'],c['fine_details_source'],*c['script_sources'],*b['style']['references']]:
  p=root/x['path'];references.append({'path':x['path'],'actual_sha256':sha(p),'brief_sha256':x['sha256'],'matches':sha(p)==x['sha256']})
 (d/'provenance.json').write_text(json.dumps({'generator':'builtin image_gen.imagegen','transparent_background':True,'brief':str(brief.relative_to(root)),'brief_sha256':sha(brief),'source_references':references,'source_read':'Actual current card, related script passages, style direction and actual image references viewed before generation.','style_reference_use':'Sela G mature expression and coarse block structure; Mia compact natural adult. No face cloning.','raw_originals_preserved':True},ensure_ascii=False,indent=2)+'\n')
 (d/'author_QA.md').write_text('# 作者检查\n\n'+('缇安v1保留但不选：长身、像素过细与背景晕影；唯一v2修订已用。v2实际查看：三十多岁成年女性、狭肩疲倦下眼睑与不安微笑；自身右手在画面左侧围裙袋附近抓钥绳，小旧钥匙可见，左手托唯一备用碗。衣装完整，未递交物品或代表权利转移。\n' if who=='tian' else '蕾因v1实际查看：三十多岁成年女性向导，粗像素紧凑比例、成熟认真解释表情。帽檐粉笔被固定带挡住中段，两白端属于同一截；背包侧袋有收起的客约卷，一手开放示意、一手扶包带。绑腿与靴清楚，无免检凭证或退款剧情。\n')+'\n透明清理只将alpha≤8置零并清掉这些透明像素的隐藏RGB；其他像素RGBA完整保留，不裁切、不重画、不量化。浅深板只同尺寸整图合成与中文标签。\n\n最终是否通过以追加的独立QA/FINAL_STATUS为准。概念不代表游戏运行、部件、装备、帧表或兼容通过。\n')
 manifest={'canonical_id':c['canonical_id'],'name':c['name'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pending_independent_review','immutable_after_freeze':True,'selected_raw':raw.name,'transparent':out.name,'boards':[f'{who}_{t}_board.png' for t in ['light','dark']],'raw_versions':[p.name for p in sorted(d.glob('*raw_imagegen.png'))],'cleanup':{'alpha_threshold':8,'alpha_nonzero_cleared_count':changed,'hidden_rgb_cleared_count':hidden,'all_pixels_alpha_gt_8_unchanged':True},'image_size':im.size,'alpha_bbox':im.getbbox(),'runtime_verified':False,'equipment_compatibility':'unknown','files':{p.name:sha(p) for p in sorted(d.iterdir()) if p.is_file() and p.name not in ('manifest.json','QA_INDEPENDENT.md','FINAL_STATUS.md')}}
 (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(who,json.dumps(manifest['cleanup']),manifest['alpha_bbox'])
