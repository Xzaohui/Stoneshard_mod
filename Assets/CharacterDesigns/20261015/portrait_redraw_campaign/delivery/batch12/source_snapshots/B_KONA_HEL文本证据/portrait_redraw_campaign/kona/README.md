# 科纳 KONA 头像重绘候选

独立QA选择 portrait_v2，结论 candidate_with_notes；总共两次实际 imagegen 调用，不再生成。

选稿：candidates/portrait_v2_74x100_candidate.png
SHA256：8a1a2530fa2a7fbba9943de3ac2b4334bf63603f9b37200ca27bfbcef8f9f442

## 方法与边界

原始返回1079×1458，未改动的PNG在raw，完整返回在tool_returns；通过完整画布单标量等比fit、nearest-neighbor、alpha 128二值化和无抖动量化派生74×100候选。Kona v2用72×98安全框等比fit，整数落点72×97，置于74×100的(1,1)；避免NN采样贴右边，不是裁切或补画。 选稿30种可见RGB色，二值alpha。

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

现卡明确30余岁成年兄长：保暗波发短须和宽眉眼，领口由旧母版棕衣纠为深蓝短褂；不画替妹妹署名/决定的动作。

- 内眉与颈斜亮面仍略谨慎，非阻断。
- 少量发部平行细亮带与像素过渡。
- 右侧仅1px透明安全边，轮廓未切。
