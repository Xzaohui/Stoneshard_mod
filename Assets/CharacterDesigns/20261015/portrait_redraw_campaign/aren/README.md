# aren 74×100 头像重绘候选

本目录为 2026-10-15 全体头像重绘批次04的独立新稿，旧角色图、设计卡、代码均未覆盖。

## 方法与边界

使用内置 imagegen 实质重绘。完整请求保存在 prompts/，完整返回在 tool_returns/；raw/ 是返回 image_url 解码后的逐字节原图。74×100 candidate 是全画布最近邻缩放、alpha 128 阈值二值化和不抖动 MAXCOVERAGE ≤32 可见色量化的派生候选。它不是原生逐像素手工终稿，不是游戏整合验收。

## 查看

- manifest.json：当前选稿、来源及 SHA
- previews/：1x 多底与 8x 最近邻对照
- sources/：最新卡、旧图、旧 QA/manifest、台本与四个风格锚的快照
- spec_lock.json：身份优先级与差异
- qa/：数值检查与作者初观；独立 QA 已接入 qa/independent_final_review.json

## 复现

在仓库根执行：

    python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/aren/derive_portrait.py Assets/CharacterDesigns/20261015/portrait_redraw_campaign/aren portrait_v2 maxcoverage

Pillow 12.3.0；原图不裁切、不补绘、不移动五官；派生程序明确记录 palette 和 alpha 方法。初稿+最多一次必要图像修订。

## 选稿

v2 MAXCOVERAGE 派生候选已选，首稿与唯一修订完整保留。作者 QA 可查 qa/author_v2_review.json；独立终目视通过候选，保留非阻断备注；独立复现已报告 PNG 字节完全相同。所有可见色≤32、二值 alpha 与尺寸结果是技术检查，不替代视觉判断。

## 独立终检备注

艾伦眼白仍有一定亮度，但比首稿明显减弱；无新增修订。
