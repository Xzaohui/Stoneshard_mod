# 奇恩 KIEN 头像重绘候选

独立QA选择 portrait_v2，结论 candidate_with_notes；总共两次实际 imagegen 调用，不再生成。

选稿：candidates/portrait_v2_74x100_candidate.png
SHA256：0f2832c722d560640d35ff63ae30296a717ae9911d4529a60c9802748a55973d

## 方法与边界

原始返回1079×1458，未改动的PNG在raw，完整返回在tool_returns；通过完整画布单标量等比fit、nearest-neighbor、alpha 128二值化和无抖动量化派生74×100候选。Kien v2等比fit至74×100。 选稿32种可见RGB色，二值alpha。

这是实际imagegen重绘后的技术派生候选，不是原生74×100逐像素创作；不代表游戏集成、运行验收或用户终稿认可。临时≤32色上限不是全项目锁色。未改旧图片、人物卡或代码，未commit/push。

## 文件

- sources：现卡、精确母版、四核心风格、旧QA/manifest、台本和逐文件来源SHA
- spec_lock.md：身份/构图/风格锁定
- prompts/portrait_v1.json、portrait_v2.json：完整实际工具参数和prompt
- tool_returns：完整imagegen工具返回
- raw：无损解码原始返回
- candidates：74×100候选
- previews：1x深/灰/浅底及整数8x nearest预览，四核心对照
- qa：来源核对、作者审图、修订请求、技术统计
- selection.json：独立QA选择与备注
- manifest.json、SHA256SUMS.txt：选稿SHA、全文件清单、输入指纹

## 复现

在本目录运行 python derive_portrait.py portrait_v2，然后 python finalize_manifest.py。前者从完整已存工具返回重建原始PNG、候选与预览，后者恢复独立选稿结论并刷新manifest/全SHA。此流程复现技术派生物；重跑imagegen不是确定性复现。所有几何采用完整画布等比NN，无局部变形或人工像素补画。

## 身份对齐与剩余备注

现卡明确40岁敦实：保沙发无须与蓝灰/棕身份，拓宽下颌和成熟颊面，缩短粗颈；肩披按工作粗巾解释，围裙与哨子位于紧头裁幅外。

- 残余沙发平行细簇。
- 嘴角略急而下弯，未完全达到平静干练。
- 左右与底边仅1px透明安全边，轮廓未切。
