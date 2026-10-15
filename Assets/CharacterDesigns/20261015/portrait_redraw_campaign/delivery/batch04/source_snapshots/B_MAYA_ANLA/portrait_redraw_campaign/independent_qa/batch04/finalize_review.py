from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
O=Path(__file__).resolve().parent;C=O.parent.parent;R=C.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={'aren':('portrait_v2_maxcoverage','0dfc2f9c23157214e2f59e73d37835d67f8588ac1de37959f01a0b9dd749a8d3'),'rowen':('portrait_v2_maxcoverage','66ee0fa16a00746902e58378860d1a913aff4d69904596ef235ae21b6cde1af3'),'maya':('portrait_v2','e06ed0869cd087f630b8f36838f21ec47203f7079e36caf01a71565c1f45cec1'),'anla':('portrait_v2_maxcoverage','6dea4e1244a606c17a0999ba0090b935e204a0495017a384b6d81c3250e05bd7')}
visual={
'aren':{'improvements':['颏至衣领露颈明显缩短，肩领靠头下，鼻颧与下颌以大块面成立。','乱短棕发由碎刺合为较大束，灰补披风和成年男性身份保持。','暖暗小眼白比v1改善，警觉侧目符合逃兵自保处境。'],'notes':['眼白仍略亮，未来原生像素清理可继续收窄。'],'identity':'NPC-N-AREN；原卡未定确切年龄，本稿保持年轻成年男性，不新定数字年龄。'},
'rowen':{'improvements':['上唇和下巴灰绿胡茬式带已去，按现卡保清洁面容。','眉头放平、眼尾收窄与轻嘴角笑，区别于全员忧眉。','灰发高光宽束化，深色混搭外套/围巾保持，未戴帽。'],'notes':['发束仍有规则斜纹；骨感与灰发不用于声称明确年龄。'],'identity':'NPC11；男性有限信息商，确切年龄不明。按现卡移除旧母版胡茬是有记录的优先级修正。'},
'maya':{'improvements':['脸扩大、颧颊与下颌更结实，露颈收至很窄，头巾折合大块。','闭口轻笑和稳定眉形保温厚坚定，中年身份与安菈明显区分。','同raw的MEDIANCUT比MAXCOVERAGE少额头/颊/下颏碎斑，选择30色版本而非机械偏好32色。'],'notes':['眼白与皮肤略同色，局部轮廓偏柔。','紧头像裁切使厚围裙不入镜；本图不代替全身服装交付。'],'identity':'NPC-MAYA / NPC06 同一人；四十多岁女性民粮代理，紧扎灰头巾，无军徽或全国领袖身份。'},
'anla':{'improvements':['露颈缩短、鼻颧/下颌成熟明确，保二十出头成年女性身份。','棕发束和肩前辫节变大，红色工装领与眉骨浅旧疤可识别。','MAXCOVERAGE保暖灰眼白与暗虹膜区分，优于MEDIANCUT压成同肤色。'],'notes':['视线偏侧、表情较初稿严肃；眼白仍稍宽，皮肤残少量碎斑。','紧头像只保留上部服装，不证明完整围裙/空工具套已在画面中交付。'],'identity':'BRY-NPC-ANLA；明确二十出头成年学徒，不幼态、不天才少女化；不画完成离坊或签约。'}}
a=json.loads((O/'independent_measurements.json').read_text());assert all(x['hash_match'] for x in a['source_checks'])
records=[]
for c in a['characters']:
 s=c['slug'];stem,want=expected[s];p=C/s/'candidates'/f'{stem}_74x100_candidate.png';m=json.loads((C/s/'manifest.json').read_text())
 assert m['selected_portrait']==str(p.relative_to(C/s)),(s,'selected mismatch')
 assert sha(p)==want
 assert c['manifest_all_file_hashes_match'] and c['source_copies_all_match'] and c['sha256sums_all_match']
 assert not m['native_authored'] and not m['native_pixel_approved'] and not m['runtime_integrated'] and not m['runtime_verified']
 assert c['tool_return_count']==2 and c['within_two_generation_limit']
 selected=next(x for x in c['candidates'] if x['target']['sha256']==want)
 assert all(x['technical_pass'] and x['independent_PNG_bytes_equal'] for x in c['candidates'])
 assert c['manifest_sha256']==sha(C/s/'manifest.json'),(s,'manifest changed after measurement')
 records.append({'slug':s,'canonical_id':c['canonical_id'],'name':c['name'],'status':'selected_candidate_with_nonblocking_notes','selected_portrait':str(p.relative_to(R)),'selected_sha256':want,'manifest_path':str((C/s/'manifest.json').relative_to(R)),'manifest_sha256':sha(C/s/'manifest.json'),'colors':selected['target']['visible_rgb_colors'],'alpha_values':selected['target']['alpha_values'],'bbox':selected['target']['alpha_bbox'],'generation_calls':c['tool_return_count'],'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'independent_export_png_byte_equal':True,'raw_equals_complete_tool_return_bytes':True,**visual[s]})
sel={'batch':'batch04','frozen_review_utc':datetime.now(timezone.utc).isoformat(),'status':'independently_selected_candidates_not_native_or_runtime_approval','selected':records,'all_10_exports_reproduced_png_byte_equal':True,'raw_output_image_count':8,'source_entries_checked':len(a['source_checks']),'native_pixel_final':False,'review_basis':'review_basis.json','measurements':'independent_measurements.json','report':'QA_REPORT.md'}
(O/'selection.json').write_text(json.dumps(sel,ensure_ascii=False,indent=2)+'\n')
lines=['# 头像重绘 batch04 独立 QA','',f"核验时间：{sel['frozen_review_utc']}",'','## 结论','','选用四张 v2 候选。四人各一次首稿及一次必要修订；没有第三次生成。全部通过独立技术复现及 1× / 最近邻放大目视复查，并保留以下非阻断风格备注。','本结论只支持候选收录，不等于用户最终认可、原生逐像素创作、原版风格完美匹配或已导入/运行游戏。','', '## 选稿']
for c in records:
 lines += ['',f"### {c['name']} / {c['canonical_id']}",f"- 选稿：`{c['selected_portrait']}`",f"- 候选 SHA256：`{c['selected_sha256']}`",f"- 冻结 manifest SHA256：`{c['manifest_sha256']}`",f"- 74×100 RGBA；{c['colors']} 个可见 RGB 色；alpha 仅 0/255。",f"- 身份核对：{c['identity']}"]
 lines += ['- '+x for x in c['improvements']]+['- 保留备注：'+x for x in c['notes']]
lines+=['','## 核验过程和证据','','- 阅读仓库 AGENTS.md、design/AGENTS.md 与四人当前独立卡。实际查看四张历史身份母版；四母版及五卡的实时 SHA 与 campaign_roster 快照一致。相关剧情只用于限制角色知识/结局，不将未发生剧情画成事实。','- 实际以 1× 查看 Mara v2、Iwo v1、Leiya v2 MAXCOVERAGE、Tore v1 四核心风格图；不是只看文字描述或文件名。全部首稿与终选均实际 1×/放大检查。','- 技术 QA 未运行作者导出脚本，单独按其声明重写导出：整幅 NEAREST → alpha 阈值128 → 只用不透明采样色建32色临时调色板 → 无抖动 MEDIANCUT/MAXCOVERAGE → 透明RGB归零。未修改人物几何、未画新像素。','- 8张 raw PNG均与完整 tool_returns.image_url 解码后的字节相同；10张导出（含未选备选）独立重建后的 RGBA 和完整 PNG 字节均相同。raw 为大尺寸 imagegen 图，74×100是显式技术派生，不标 native final。','- 10张派生均74×100、可见色≤32、alpha二值；32为临时上限，不代表调色品质或原作统一色板已经验收。','- 四生产 manifest 库存哈希、SHA256SUMS、所有来源快照的实时哈希及字节均通过；已选候选 SHA 已在 selection.json 冻结。','- 新旧资产分开。QA仅写本 independent_qa/batch04 目录；未改生产候选、人物卡、代码，未生成新图、未 push、未游戏集成。','','## 文件','','- `selection.json`：终选身份、候选/manifest哈希、逐人判断。','- `independent_measurements.json`：raw/返回字节、独立导出、色数/alpha/尺寸、来源/manifest/SHA检查。','- `audit_measurements.py` 和 `reproduction_config.json`：独立可复跑校验。','- `preflight_source_checks.json`、`review_basis.json`：读卡、母版/风格基准。','- `revision_feedback.md`：每人唯一一次集中修订意见。','- `selected_candidates_1x_4x.png`：黑/灰/白三背景1×及4×对照。','']
(O/'QA_REPORT.md').write_text('\n'.join(lines))
print(json.dumps({'selection':str(O/'selection.json'),'report':str(O/'QA_REPORT.md'),'characters':[{k:c[k] for k in ['slug','selected_sha256','manifest_sha256','colors']} for c in records]},ensure_ascii=False,indent=2))
