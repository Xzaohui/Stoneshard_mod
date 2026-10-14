# 新增剧情人物44人基础动作图册 v1

## 本册范围

24页：封面1页、可点击人物目录1页、人物页22页。按既有人物清单排序，每页两人，每人依次展示基础母图、A1、A2。收录44张基础母图与84张通过独立审查的非战斗关键姿态，共128张不同源图。

40人各有两张合格姿态，图里、锉珥、苇珥、栎珥各只有A2，四个A1以文字占位，未收入未通过的首稿或修订。未收入人物表情。A1与A2是独立关键姿态，不保证构成连续动画，也不代表装备适配、引擎实现或游戏运行验收。制作或独审通过不等于用户审美确认。

姓名以44人人物清单为准，并保留稳定ID。苇珥/韦珥、燧珥/绥珥、摩珥/谟珥分人；佴珥使用FX-CV4身份。谟珥沿用最终v2背铲母图，裤膝浅斑沿用原崖灰。

## 输出

- output/pdf/新增剧情人物44人_基础动作图册_v1.pdf
- output/新增剧情人物44人_动作覆盖概览_v1.png
- output/新增剧情人物44人_动作图册制作资料_v1.zip

总览展示44张母图、姓名与稳定ID、A1/A2覆盖状态。图册与总览是新的整合浏览产物，未重新发送任何既有附件，不改变原批次发送结果记录。

## 浏览图像处理

最长边520像素，以最近邻等比例缩放，宽高仅作整数像素取整；保留完整画布，不裁人物、不拉伸、不重绘、不调色、不锐化。PDF嵌入图RGB及透明通道必须与浏览PNG逐像素解码一致。PDF声明Interpolate=false。全部128张原始选图保持不变，制作前后检查旧人物/敌人图册与全部44人动作工作树。

字体为Noto Sans CJK SC的子集，附许可；保留原字形ID，避免CFF字体子集重映射导致中文错字。目录44个跳转链接、人物页22个返回目录链接、24个书签，页码与PDF物理页码一致。

## 制作资料ZIP的边界

资料ZIP只含布局脚本、源路径与SHA索引、字体子集及许可、排版数据和核验报告。它不包含128张原始PNG、浏览PNG、raw、废稿、完整生图工具返回、每页PNG或各批完整素材源ZIP。不能称为完整原画源集，也不能在缺少原项目素材时独立重建图片。

## 复现

需已有Stoneshard_mod项目及source_audit/selection_audit.json列出的128张源图，按本目录原路径放回制作资料。Python依赖见requirements.txt。先逐项核对来源SHA，再运行：

    python build_catalog.py --max-px 520
    python verify_catalog.py

源审计脚本source_audit/build_selection_audit.py根据作者FINAL/manifest、独审SHA和第11批冻结handoff提取最终选图。再次运行会更新审计时间，不会改变原图；如要严格复现本次成品，应使用资料包内已冻结的selection_audit.json。

如果本目录production/embedded已有128张SHA匹配的浏览PNG，可使用：

    python build_catalog.py --max-px 520 --use-embedded

验证脚本核对所有原选图与工作树指纹、PDF内图像资源、链接/书签并生成24页预览。页面渲染后仍需实际逐页视觉检查，不能用自动计数代替视觉验收。package_production.py只打包本次制作资料，检查ZIP逐成员SHA/CRC与18MiB上限。

## 关键核验资料

- source_audit/selection_audit.json：128张实际选图、人物ID、作者终态、母图绑定、独审与冻结证据。
- source_audit/old_catalog_fingerprints.json：旧人物/敌人图册只读基线。
- source_audit/old_source_fingerprints.json：前40人全部动作树与44母图基线。
- source_audit/eleventh_source_fingerprints.json：最后4人最终冻结后动作树基线。
- production/embedded_manifest.json：浏览PNG尺寸、缩放方法、前后SHA。
- production/layout_objects.json：文字与图像的排版坐标。
- LAYOUT_VERIFICATION.json：结构、边界、缺项、页数与大小。
- review/PDF_IMAGE_DECODE_QA.json：128图RGB与alpha逐像素一致。
- review/RENDER_MANIFEST.json：最终PDF及24页渲染PNG的SHA。
- review/ALL_PAGE_VISUAL_QA.json：制作方24页实际查看记录。
- REPRODUCTION_QA.json：同源重建产物SHA一致性。
- FINAL_SOURCE_FREEZE_QA.json：旧图册/源文件/原选图保留性。
- OUTPUTS.json / SOURCE_PACKAGE_MANIFEST.json：最终输出与资料包内容。

来源与核验记录保留历史边界；不将内部生成、上传或发送状态当成用户审美批准，也不声称已运行游戏。
