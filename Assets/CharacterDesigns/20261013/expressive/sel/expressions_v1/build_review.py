from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
BASE=ROOT/'Assets/CharacterDesigns/20261013/expressive'
BRIEF=BASE/'briefs/next_main_cast_expressions_nell_sel_01.json'
b=json.loads(BRIEF.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=lambda n:ImageFont.truetype(font,n)
for c in b['characters']:
 out=BASE/c['slug']/'expressions_v1'; (out/'selected').mkdir(exist_ok=True);(out/'sources').mkdir(exist_ok=True)
 shutil.copy2(BRIEF,out/'sources'/BRIEF.name)
 for s in [c['anchor']]+c['source_evidence']:
  p=ROOT/s['path'];shutil.copy2(p,out/'sources'/p.name)
  assert sha(p)==s['sha256'],p
 shutil.copy2(__file__,out/'build_review.py')
 selected=[]
 for e in c['expressions']:
  raw=out/'raw'/(e['key']+'_raw_imagegen.png');im=Image.open(raw).convert('RGBA')
  # Authorized alpha cleanup only. Preserve every RGB value, all shape and native dimensions.
  alpha=im.getchannel('A'); im.putalpha(alpha.point(lambda x:0 if x<32 else x))
  p=out/'selected'/(e['key']+'.png');im.save(p);selected.append(im)
 for theme,bg,fg,sub in [('light','#eee8dc','#312922','#695b4e'),('dark','#202630','#f3e5d0','#b9afa0')]:
  board=Image.new('RGB',(1410,700),bg);d=ImageDraw.Draw(board)
  d.text((30,22),f"{c['name']} · 三态表情设定",font=F(32),fill=fg)
  d.text((30,70),'成熟大头像素概念｜保持原身份衣装｜独立情绪研究，未接入游戏',font=F(21),fill=sub)
  for i,(e,im) in enumerate(zip(c['expressions'],selected)):
   thumb=im.resize((418,418),Image.Resampling.NEAREST);board.paste(thumb,(25+i*465,120),thumb)
   d.text((40+i*465,550),f"E{i+1}  {e['label']}",font=F(27),fill=fg)
   notes={'nell':['侧目 · 非对称眉 · 闭口','忧眉 · 小幅开口 · 设界','正视 · 平压眉 · 克制申明'],'sel':['偏侧抬眉 · 试探开口','压眉直视 · 紧绷反问','忧眉偏侧 · 闭口盘算']}[c['slug']]
   d.text((40+i*465,595),notes[i],font=F(19),fill=sub)
  d.text((30,657),'不代表作证、认罪、签约、清债或任何路线已经完成。',font=F(20),fill=sub)
  board.save(out/f"{c['slug']}_expressions_review_zh_{theme}.png")
 qa={'character':c['slug'],'status':'author_visual_review_pending_independent','raw_actually_viewed':True,'revision_count':0,'generation':'six separate built-in imagegen calls; no scripted body/face drawing or nonuniform stretching','processing':'selected alpha <32 cleared only; RGB, native 1254×1254 geometry and remaining alpha preserved; boards use uniform 1/3 nearest scale','findings':{'nell':['成熟脸型、深棕侧后束髻、深蓝领与米白流苏披巾保持。','E1闭口侧目与不对称眉；E2忧眉小开口；E3更正面、较平压眉、横向申明口型。','E1/E2头姿差较轻；E2眼睑打开幅度有限，依靠眉嘴区分。'],'sel':['灰棕银灰发束、成熟棱鼻、灰白下巴须、红翻领及双肩带保持。','E1单眉试探小笑开口；E2眉内端压低、反问开口；E3闭嘴浅忧眉偏侧。','E1笑意稍明显；E3下倾偏轻，低垂方向需要独审；袖口在裁切底缘略见。']}[c['slug']],'runtime_integrated':False,'narrative_limits':'No new story decisions or outcomes.'}
 (out/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 (out/'README.md').write_text(f"# {c['name']} 三态表情设定\n\n三张新绘胸像，内置 imagegen 生成。原稿完整保留；selected 仅清除低 alpha 外缘，未绘制或拉伸身体与脸。浅深中文板以统一 nearest 排版。\n\n这是独立设定素材，不代表游戏帧、剧情结果或已接入游戏。身份、衣装与来源以 sources 内原卡、brief 和 v2 锚为准。\n\n独立审查前不封包，不改 roster。\n")
 manifest={'character':c['slug'],'canonical_id':c['canonical_id'],'generator':'built-in image_gen.imagegen','source_anchor':c['anchor'],'source_evidence':c['source_evidence'],'expressions':c['expressions'],'runtime_integrated':False,'independent_review':'pending','files':[]}
 for p in sorted(out.rglob('*')):
  if p.is_file() and p.name!='manifest.json' and p.suffix!='.zip':manifest['files'].append({'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)})
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print(out)
