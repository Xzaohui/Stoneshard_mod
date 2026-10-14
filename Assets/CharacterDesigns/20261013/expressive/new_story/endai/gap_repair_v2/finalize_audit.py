from pathlib import Path
import json,hashlib,shutil,zipfile,base64,datetime
from PIL import Image,ImageDraw
import numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); p=r/'Assets/CharacterDesigns/20261013/expressive/new_story/endai/gap_repair_v2'; parent=p.parent
sources=[r/'AGENTS.md',r/'Assets/CharacterDesigns/20261013/expressive/reference/pixel-asset-master/SKILL.md',r/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md',parent/'concept_v1/spec_lock.md',parent/'concept_v1/manifest.json',parent/'concept_v1/endai_v1_raw_imagegen.png',parent/'expressions_v1/README.md']
sources+=list((parent/'expressions_v1/prompts').glob('*E2*'))+list((parent/'expressions_v1/raw').glob('*E2*'))
sources += list((parent/'expressions_v1/sources').glob('人物_FX-BST*'))+list((parent/'expressions_v1/sources').glob('台本_FX*'))
records=[]
for src in sources:
 rel=src.relative_to(r); dst=p/'sources/files'/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst); records.append({'source':str(rel),'snapshot':str(dst.relative_to(p)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
(p/'sources/source_manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
shutil.copyfile('/tmp/endai_review.py',p/'review/prepare_review.py'); shutil.copyfile('/tmp/finalize_endai.py',p/'finalize_audit.py')
out=p/'selected/endai_E2_no_order_no_entry_transparent.png'
for name,col in [('light',(232,225,211,255)),('dark',(30,34,43,255))]:
 board=Image.new('RGBA',(1024,800),col); d=ImageDraw.Draw(board)
 for i,f in enumerate([p/'sources/mother.png',out]):
  x=Image.open(f).convert('RGBA').resize((512,768),Image.Resampling.NEAREST);board.alpha_composite(x,(i*512,32)); d.text((i*512+12,10),['MOTHER / CONCEPT V1','E2 / NO ORDER, NO ENTRY'][i],fill=(128,128,128,255))
 board.convert('RGB').save(p/f'review/endai_mother_E2_{name}.png')
raw=(p/'raw/E2_initial.png').read_bytes(); response=json.loads((p/'raw/E2_initial_tool_return.json').read_text()); decoded=base64.b64decode(response['image_url'].split(',',1)[1]); original=Path('/workspace/scratch/5ed8df2c5d81/generated_images/exec-935626c3-99bb-4c9d-b73b-77be6bdc234b.png').read_bytes(); a=np.array(Image.open(p/'raw/E2_initial.png')); b=np.array(Image.open(out))
qa={'character':'恩岱 Endai FX-BST','asset':'E2 无令不允','status':'author_pass_concept_only','generation_calls':1,'revision_calls':0,'original_failed_E2_preserved':True,'raw_payload_decoded_matches_png':decoded==raw,'raw_matches_generated_original':raw==original,'rawSHA256':hashlib.sha256(raw).hexdigest(),'size':[1024,1536],'mode':'RGBA','alpha_le8_cleared':int((a[:,:,3]<=8).sum()),'visible_RGBA_alpha_above8_unchanged':bool(np.array_equal(a[a[:,:,3]>8],b[a[:,:,3]>8])),'visual_review':{'mother_viewed':True,'raw_viewed':True,'selected_RGBA_viewed':True,'light_and_dark_boards_viewed':True,'single_complete_person':'pass','mother_compact_proportions':'pass','three_cloak_patches_and_local_armor':'pass','face_identity_age':'pass','expression':'压眉、闭嘴、向右警醒拒绝；无怒吼、无放行。','pixel_style':'清楚粗像素簇与阶梯边缘；为概念图，非原生像素网格验证。','edge_background':'浅深底轮廓完整，无可见残留光晕。'},'runtime_verified':False,'user_acceptance_claimed':False,'independent_review':'not performed at author freeze','limitations':['不代表原生尺寸、装备部件、遮罩、锚点、动画或游戏运行验收。','保留原右手低伸而非旧prompt建议的腰侧低收，以最小脸部变化锁住母图比例。','未改旧manifest、图册、回执或Git，未上传。']}
(p/'review/author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(p/'FINAL.md').write_text('# 恩岱 E2 无令不允｜gap_repair_v2\n\n作者验收：通过，限人物表情概念；非用户确认或游戏落地验收。\n\n一次新绘，无修订。实际查看母图、raw、选稿RGBA及浅/深对照板：单人全身、紧凑头身和原服装道具保留；眉压平收紧，嘴由开口转闭合，目光向右警醒。三处赭补片、灰发短须、局部亮甲保留。双人、小头长肢的旧失败均未覆盖。\n\nPNG只清理alpha≤8及其隐藏RGB，alpha>8逐像素不变；没有脚本绘人、拉伸、调色或量化。板只等比nearest排版。完整原始工具返回含payload、预写精确prompt/params、原始PNG、母图与旧失败来源一并归档。raw由payload解码并与工具生成文件SHA核对一致。\n\n选稿：selected/endai_E2_no_order_no_entry_transparent.png\n\n审计数值、边界和源哈希见review/author_QA.json、manifest.json与sources/source_manifest.json。独审可以另写报告，但不得修改本FINAL。\n')
files=[]
for f in sorted(p.rglob('*')):
 if f.is_file() and 'exports' not in f.relative_to(p).parts and f.name not in ['manifest.json','DELIVERY_FILES.json']:
  files.append({'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(p/'manifest.json').write_text(json.dumps({'schema_version':1,'status':'author_pass_concept_only','files':files},ensure_ascii=False,indent=2))
z=p/'exports/endai_E2_gap_repair_v2_audit.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as arc:
 for f in sorted(p.rglob('*')):
  if f.is_file() and 'exports' not in f.relative_to(p).parts and f.name!='DELIVERY_FILES.json':arc.write(f,str(Path('endai_E2_gap_repair_v2')/f.relative_to(p)))
assert z.stat().st_size<18*1024*1024
with zipfile.ZipFile(z) as arc: assert arc.testzip() is None
items=[]
for f in [out,p/'review/endai_mother_E2_light.png',p/'review/endai_mother_E2_dark.png',z]:
 items.append({'path':str(f.relative_to(r)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(p/'DELIVERY_FILES.json').write_text(json.dumps(items,ensure_ascii=False,indent=2));print(json.dumps(items,ensure_ascii=False,indent=2))
