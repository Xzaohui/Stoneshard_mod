from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,shutil
D=Path(__file__).resolve().parent; ROOT=D.parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,x):(D/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sources={'I0_stand_anchor.png':'interaction_v1/frames/I0_stand.png','I2_reach_reference.png':'interaction_v1/frames/I2_reach.png','R2_seated_reference.png':'rest_transition_v1/frames/R2_seated.png','anchor_QA-independent.json':'interaction_v1/QA-independent.json','STYLE_DIRECTION.md':'../../../CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md'}
records=[]
for out,rel in sources.items():
 p=(D.parent/rel).resolve()
 if not p.exists():
  p=ROOT/'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md'
 shutil.copy2(p,D/'sources'/out); records.append({'source':str(p.relative_to(ROOT)),'copy':'sources/'+out,'sha256':sha(p),'role':'only_generation_anchor' if out.startswith('I0') else 'reference_only_not_new'})
raw=Image.open(D/'raw/K1_single_knee_rest.png').convert('RGBA'); alpha=raw.getchannel('A'); mask=alpha.point(lambda a:255 if a>=128 else 0); clean=Image.new('RGBA',raw.size); clean.paste(raw,(0,0),mask); clean.putalpha(mask)
# Preserve RGB of visible pixels; zero RGB in fully transparent pixels. No anatomy edits.
pix=clean.load()
for y in range(clean.height):
 for x in range(clean.width):
  if pix[x,y][3]==0:pix[x,y]=(0,0,0,0)
clean.save(D/'frames/K1_single_knee_rest_alpha.png')
frame=Image.new('RGBA',(1536,1536)); offset=(117,237);frame.alpha_composite(clean,offset);frame.save(D/'frames/K1_single_knee_rest.png')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(n):return ImageFont.truetype(font,n)
imgs=[Image.open(D/'sources'/n).convert('RGBA') for n in ['I0_stand_anchor.png','I2_reach_reference.png','R2_seated_reference.png']]+[frame]
labels=['I0 原站姿｜复用锚','I2 近地伸手｜复用参考','R2 凳上坐姿｜复用参考','K1 单膝短歇｜本轮唯一新图']
for theme,bg,fg in [('light',(238,234,224),(35,35,40)),('dark',(38,43,51),(235,233,225))]:
 board=Image.new('RGB',(2080,1650),bg);dr=ImageDraw.Draw(board)
 dr.text((30,20),'成年训练样板 · 单膝落地短歇 · 静态姿态候选',font=f(34),fill=fg)
 dr.text((30,72),'仅1张新绘；旧I0 / I2 / R2只作对照。所有全身图同0.325倍最近邻展示；无地线或补画接触。',font=f(23),fill=fg)
 for i,(im,label) in enumerate(zip(imgs,labels)):
  im=im.resize((499,499),Image.Resampling.NEAREST);board.paste(im,(20+i*515,130),im);dr.text((25+i*515,645),label,font=f(22),fill=fg)
 # raw crop, independently labeled same source scale, no support guide lines
 crop=clean.crop((395,835,915,1160)).resize((1040,650),Image.Resampling.NEAREST);board.paste(crop,(40,790),crop)
 dr.text((40,720),'K1 膝—小腿—后靴 / 前靴近景（原稿局部×2，最近邻）',font=f(25),fill=fg)
 for i,(im,box,label) in enumerate([(imgs[0],(620,440,930,790),'I0 头帽原尺度局部'),(raw,(520,398,805,718),'K1 头帽原尺度局部')]):
  c=im.crop(box);board.paste(c,(1230+i*360,860),c);dr.text((1210+i*360,1230),label,font=f(22),fill=fg)
 dr.text((40,1480),'原稿1254²；透明阈值alpha≥128；仅平移到1536²，未缩放或拉伸身体。',font=f(26),fill=fg)
 dr.text((40,1525),'头帽人工估高：I0约328px，K1约308px（约−6.1%）；须看原稿判断尺度与接触。',font=f(24),fill=fg)
 dr.text((40,1570),'概念静态候选，不是原生精灵规格、动画、换装或游戏运行证据。',font=f(24),fill=fg)
 board.save(D/f'single_knee_rest_review_{theme}_zh.png')
dump('source_provenance.json',{'sources':records,'brief_sha256':sha(D/'sources/adult_basic_body_pose_gap_01.json'),'anchor_raw_ancestor':{'path':'Assets/CharacterActions/20261013/adult_training_dummy/interaction_v1/raw/I0_stand.png','sha256':'e303bedfb334dc584bcb36b7924bae15276835ddecbafe4630c469c7776f75ad','role':'ancestry_only_not_generation_input'},'generated_source':'/workspace/scratch/5ed8df2c5d81/generated_images/exec-e6921749-b45d-49bf-8c15-3a297ce6bc97.png'})
dump('processing_log.json',{'raw_size':raw.size,'raw_alpha_bbox':alpha.getbbox(),'threshold':128,'threshold_bbox':mask.getbbox(),'clean_alpha_values':[0,255],'scale':1.0,'offset':offset,'canvas':[1536,1536],'body_drawing':False,'ground_guides':False,'new_image_count':1,'tool':'built-in image_gen.imagegen','generation_calls':1,'raw_sha256':sha(D/'raw/K1_single_knee_rest.png')})
dump('manifest.json',{'status':'awaiting_independent_review','new_static_poses':1,'new_characters':0,'approved_images':0,'delivered_images':0,'gifs':0,'runtime_verified':False,'transparent_frame':'frames/K1_single_knee_rest.png','raw':'raw/K1_single_knee_rest.png','references_reused_not_new':['I0','I2','R2'],'head_hood_height_manual_estimate':{'I0':328,'K1':308,'change_percent':-6.1},'no_body_scale':True,'processing':'processing_log.json'})
dump('QA-author.json',{'status':'candidate_for_independent_review_not_final','actually_viewed':['raw/K1_single_knee_rest.png','sources/I0_stand_anchor.png'],'observations':['单膝支撑轮廓明确区别于I2俯身、R2坐凳。','前靴全底完整，后膝处于低位；后小腿向左接短靴。','一手搭前膝上方大腿，另一手空垂，双手接袖完整。','灰帽、粗眉脸、蓝绗缝衣、腰带棕裤手套短靴保持。','新图头帽约308px，比锚约328px小6.1%，未经缩放掩饰。'], 'independent_focus':['后膝落点、后小腿与靴连通是否充分明确','原成年脸、头身尺度和腿长是否可接受'],'hard_failure_policy':'If rejected preserve as research; no further generation or frames.'})
(D/'README_zh.md').write_text('单膝落地短歇：本轮仅一张内置imagegen新图。\n\nraw保原稿，frames含alpha≥128透明清理稿与只平移到1536²的候选。身体未缩放、拉伸、脚本绘制或关节拼贴。I0唯一生成锚，I2/R2仅检视对照复用。原稿工具实际输出1254²而非请求1536²。新图头帽约308px，对照约328px；不把740px跪姿主体高度拉回935px站高。\n\n浅深板不添加地线，膝靴接触按真实轮廓判断。无GIF、补帧、原生规格或游戏落地结论；独审前不计通过或交付。\n',encoding='utf-8')
print('Built',D)
