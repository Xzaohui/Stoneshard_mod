from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
import json, hashlib
D=Path(__file__).resolve().parent; R=D.parent.parent; Q=R/'independent_qa/batch37'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
js=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
gate=json.loads((D/'freeze_gate.json').read_text());sm=json.loads((D/'selected_delivery_manifest.json').read_text());qs=json.loads((Q/'QA_summary.json').read_text())
raw=R/'lein/raw/portrait_v2_raw_imagegen.png';im=Image.open(raw).convert('RGBA'); edge=list(im.getchannel('A').crop((im.width-1,0,im.width,im.height)).getdata())
assert max(edge)==47 and sum(a>=128 for a in edge)==0 and sum(a>=16 for a in edge)==69 and sum(a>=5 for a in edge)==108
b=json.loads((Q/'lein_v2_boundary_evidence.json').read_text());assert sha(raw)==b['raw_sha256']
held='''# 蕾因 LEIN 暂缓说明

蕾因当前 selected_portrait=null、selected_sha256=null，独立QA判定 held_source_contour_margin_and_style。她不在三人总览中展示头像，没有单独成功PNG，不计入本批成功候选或累计已发送数。

v2右侧源边界（x=1085）alpha最大47；alpha≥128边界计数0，alpha≥16计数69，alpha≥5计数108。不是“整段全不透明像素已被切断”。源外轮廓是否完整、真实透明余量未获独立确认：x=1084有近不透明深发，边缘半透明发沿延到最后源列，不能用alpha≥128的零计数证明真实余量安全。inset只改变目标网格边距，不能恢复未知源外内容。

眼白仍不全暗、上眼线与平行发层仍强；v1也未通过风格门槛，不能回退v1冒充成功。每人仅一次集中必要反馈、两次成功生图，不做第三次。

证据：lein/candidates/portrait_v2_inset_74x100_candidate.png
证据SHA256：7e1d2ba859c3656cd812b6e3f318665b4faf295c8cc14c422f113aa63a4298a6
v2 raw SHA256：0049e04b3eb10f19dac6a098e57676abe47842c9fdf0a4c7ee33bf369987274b

源包B保留蕾因完整制作目录：两张成功raw、完整回包、完整提示词与真实参数、v1/v2/v2_inset历史派生及全部QA，包括多阈值边界数值与3倍最近邻边缘图。历史与暂缓图只作证据。
'''
(D/'HELD_LEIN_说明.md').write_text(held,encoding='utf-8')
intro='''# 第三十七批头像重绘交付说明

日期：2026-10-15。艾萝（人物卡全名艾萝·图）、古菈、图里共3名带限制候选；蕾因因源外轮廓/真实余量与风格暂缓，selected=null。所有结果仅为高分辨率生图的74×100最近邻技术派生候选，非原生手工逐像素终稿、未集成游戏、未实机验证。

## 六件附件

1. batch37_三人头像总览_1x_4x.png：680×1948中文手机纵板，每人含74×100原尺寸及4倍最近邻展示。蕾因只显示暂缓文字，不展示成功头像。
2–4. ARO_艾萝、GURA_古菈、TURI_图里各一张74×100透明PNG。
5. batch37_source_A_ARO_GURA.zip：艾萝、古菈完整制作来源。
6. batch37_source_B_TURI_LEIN_held.zip：图里完整制作来源与蕾因完整暂缓证据。
两包均小于18 MiB，每包均附完整独立QA、三人总览、3张选稿及便携复现脚本。

## 冻结选稿与限制
'''
for c in qs['characters']:
 name={'aro':'艾萝·图','gura':'古菈','lein':'蕾因','turi':'图里'}[c['slug']]
 intro+=f'\n### {name}（{c["slug"]}）\n'
 if c['delivery_eligible']:intro+=f'选稿：{c["selected_path"]}\nSHA256：{c["selected_sha256"]}\n'
 else:intro+=f'状态：源外轮廓/真实余量与风格暂缓，selected=null，不计成功。\n证据：{c["held_evidence_path"]}\n证据SHA256：{c["held_evidence_sha256"]}\n'
 intro+=''.join('- '+x+'\n' for x in c['limitations'])
intro+='''
## 方法与身份边界

四人各有两份成功生图、一次集中必要反馈，没有第三次。预检返回的“引用不得超过5张”错误未生成图片，原样保留，不计成功生图。采用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁脸、几何重绘或拼贴旧脸。32色只是临时技术上限，不代表原生像素美术认可。

艾萝选择v2整幅74×100 fit-box派生；古菈与图里选择同源v2的72×98 fit-box inset置入74×100透明画布。inset只调整目标网格，不修复源外未知内容、不补头发耳朵。古菈raw左右透明余量仅16/10源像素，inset不能被描述为满足原提示词的宽源边距。蕾因右源边alpha最大47、alpha≥128计数0、alpha≥16计数69、alpha≥5计数108；仍缺完整源外廓与真实余量的独立确认，不能简单称为“全不透明裁断”。蕾因v1风格也未过，不回退v1。

最新人物卡优先旧母图：艾萝约40岁，深色保管者长衣优先旧橄榄短披；古菈30多岁本班维护工，灰厚褂；蕾因30多岁女向导，棕软帽粉笔与绿披；图里约40岁精瘦男性检查匠，灰鬓短须与橄榄披。紧脸头像不能代表完整服装或随身物已制作。

## 源包保留范围

四人制作目录全量211文件：8张raw、8份完整成功工具回包、8份完整成功提示词txt与8份真实参数json、11张历史候选（艾萝2张，其余各3张）、人物卡与剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、全部预览、metrics、作者自检和反馈、脚本、manifest与SHA256SUMS。预检失败的提示词/回包按各制作目录原样保留。蕾因held完整原始材料、参数、历史QA均保留。

独立QA完整102文件全部进入两包，无省略项：包含28份原始源独立快照、技术/视觉报告、历史与选中复现图、源终检、多阈值边界与3x NN证据、selection_lock.json、manifest.json与SHA256SUMS（100清单项、101 SHA项）。唯一选稿锁为independent_qa/batch37/selection_lock.json，SHA256为67fcd44a619e4663429c40aa44e90642dd8c73a0787162eb9c5c62661f4c6edd。全部原来源与快照SHA在冻结和打包前重新核对。

商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成的身份与四核心风格参考完整保留。原始提示词绝对路径忠实保留，便携复现使用包内相对路径，不依赖旧工作区。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生无需生图服务或网络。

1. 校验ZIP：python verify_source_package.py batch37_source_A_ARO_GURA.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在。脚本只写新输出，不改冻结文件。A包复现5张、B包复现6张，共11张历史候选；蕾因3张只作证据。
4. 逐张比较完整RGBA像素、PNG字节及SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA/字节大小、成员全集、重复路径与路径穿越。PACKAGE_SHA256SUMS.txt覆盖全部实质成员及package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前实际查看手机纵板与三张独立PNG；1×/4×的6个图像区域逐像素验证。打包后实际解压两份ZIP，从解压目录复现全部11张历史候选。证据见portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json与完整独立QA。

只写delivery/batch37，未改源人物卡、旧资产、制作源目录、Mod代码或冻结索引；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py、make_freeze_gate.py为原仓库交付构建脚本；包内便携校验使用verify_source_package.py和reproduce_candidates.py。
'''
(D/'README_交付说明.md').write_text(intro,encoding='utf-8')
js(D/'delivery_visual_QA.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'actually_viewed_via_view_image':True,'viewed_files':[sm['board']['file']]+[x['delivery_file'] for x in sm['characters']],'board_sha256':sha(D/sm['board']['file']),'board_dimensions':[680,1948],'Chinese_mobile_vertical_layout_legible':True,'no_text_clipping_or_overlap_seen':True,'all_six_composited_portrait_regions_exact':all(x['composited_pixels_exact'] for x in sm['board']['portrait_checks']),'selected_images_byte_match_frozen_selection':True,'held_portrait_not_displayed':True,'held_accurate_boundary_wording':True,'held_source_boundary_independently_remeasured':{'raw_sha256':sha(raw),'right_edge_alpha_max':max(edge),'right_alpha_ge128':sum(a>=128 for a in edge),'right_alpha_ge16':sum(a>=16 for a in edge),'right_alpha_ge5':sum(a>=5 for a in edge)},'not_native_authored_or_runtime_approved':True,'all_pass':True})
print('README, held explanation and visual inspection record written')
