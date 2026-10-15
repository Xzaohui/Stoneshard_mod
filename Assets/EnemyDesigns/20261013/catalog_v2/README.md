# 原创敌人设定集 v2

本版仅把此前已经交付的 11 个合格续姿并入图册，不增加本轮生图数量，不改动 catalog_v1 或任何旧角色资产。

## 浏览产物

- `enemy_design_catalog_v2.pdf`：14 页，封面、可点击目录、十二名敌人各一页四格。
- `enemy_twelve_coverage_overview_v2.png`：12 个角色、47 张唯一选稿的覆盖概览，002 第四格显示缺项。
- `enemy_catalog_v2_layout_sources.zip`：可复现排版的小源包，详见下述范围。
- `rendered/page-01.png` 至 `page-14.png`：逐页实际视觉检查预览。

## 计数与选稿

12 张静态母图 + 原有 24 个合格独立动作 + 已交付的 11 个续姿 = 47 张唯一选稿。其中合格独立动作总数为 35。首六续姿 5 张，第二组六续姿 6 张；002 的下挥中段 v1、v2 均未通过，仍为缺项，不展示失败稿，也不以旧姿势代替或重复计数。

原 36 图保持 v1 的路径和 SHA-256。001 原动作沿用已通过的自然前握替代方案，不能声称原 brief 握法已通过；跨姿矛长尚未验收。009、012 静态图使用 idle_style_v2。续姿选用 001 / 008 / 011 v2，其他通过项为 v1。

004、010 半透明不作重涂或 alpha 增强；011 v2 原始可见 RGBA 和 64 像素透明边保留；012 原交付 alpha 阈值处理与留边保持。

## 图像方法与复现

完整源画布只读，最大边 700 像素的浏览栅格仅采用 Pillow NEAREST 等比缩放，无画面裁切、抠边、非等比拉伸、重绘或 alpha 修改。整数像素舍入仅用于栅格尺寸。PDF 明确关闭 Interpolate；RGB 与 alpha 分开无损嵌入，保存后提取并逐字节核对。`browser_raster_map.json` 给出源 SHA、RGB 解码 SHA、alpha 解码 SHA 及逐图浏览栅格 SHA。逐页 PNG 在 fresh-open PDF 后渲染，避免先提取图像导致的 MuPDF 解码缓存差异。

项目内复现：安装 `requirements.txt` 的 Python 依赖，然后运行：

`python Assets/EnemyDesigns/20261013/catalog_v2/build_catalog.py --font Assets/EnemyDesigns/20261013/catalog_v2/catalog_font_subset.otf`

运行构建要求本项目中 `selected_sources.json` 所列的 47 个冻结选稿仍然存在。重新构建会重写本目录的 PDF、浏览栅格及逐页预览，不写旧源。`prepare_sources.py` 记录最初的来源装配过程，平时无需重跑。

`verify_catalog.py` 复验源文件、旧资产冻结、完整画布 nearest 浏览栅格和 PDF 的 RGB/alpha。PDF 文件字节可能因 PDF ID 等元数据而在重建后变化；像素及来源必须保持一致。

## 小 ZIP 的实际范围

小 ZIP 含排版及验证脚本、字体子集与许可、字体来源 SHA、47 图来源映射、138 份原有验收/交付证据副本、旧源冻结清单、QA、14 张逐页 PNG 及覆盖概览。`ZIP_CONTENTS.json` 列出包内每个文件的 SHA 与字节数。

小 ZIP 不含全部角色 raw、提示词全集、失败图、完整角色源 ZIP，也不重复包含 PDF 或 47 张中间浏览栅格。它是依赖项目内冻结选稿的排版源包，不是独立的完整美术源包。完整角色素材与生成历史仍在既有角色目录及此前交付包中。002 失败情况只以文字和证据记录保留。

部分冻结交付 manifest 中的 pending 或 delivered=false 是当时打包快照；选稿通过与发送状态按 FINAL、独审、最终交付索引及回执交叉确认，不改写旧快照。

## 验收边界

本册是 Mod 原创独立关键姿态概念，不是连续动画、补间或完整循环。公共锚点、帧间尺度、武器长度、装备组合、碰撞、游戏集成及实机效果未验收。`continuous_animation_verified=false`、`runtimeIntegrated=false`、`runtimeVerified=false`。

本轮仅保存项目产物：无生图调用、无 Git、无上传、无用户发送。
