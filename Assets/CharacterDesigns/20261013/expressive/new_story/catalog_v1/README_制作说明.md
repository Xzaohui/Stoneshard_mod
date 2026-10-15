# 新增剧情人物概念与表情图册 v1

## 内容与范围

本图册按新增44人人物清单排列，收录44张基础母图与86张通过审查的独立表情，共130张不同选图。PDF为24页：封面1页、可点击目录1页、人物页22页，每页两人。PDF书签与目录页码均对应实际页码。

42人各有两张合格表情。恩岱（FX-BST）E2比例审查未通过、瑟珥（FX-CRP）E1首稿朝向未通过且修订未产图，因此两处只保留文字占位，没有把未通过的图收入图册。表情不是连续动画；审查通过不等于用户确认，也不代表游戏已实现或运行验收。

姓名以44人人物清单为准，并保留稳定ID。苇珥/韦珥、燧珥/绥珥、摩珥/谟珥分人；佴珥使用FX-CV4身份。谟珥沿用最终v2背铲母图。历史调用参数记录不全的限制仍保留在来源审计中，没有补造记录。

## 交付文件

- output/pdf/新增剧情人物44人_概念与表情图册_v1.pdf
- output/新增剧情人物44人_母图总览_v1.png
- output/新增剧情人物44人_图册制作资料_v1.zip

图册为便于阅读与发送的浏览版。PNG浏览副本最长边520像素，按比例取整、最近邻缩放；保留完整画布，不裁人物、不重画、不拉伸、不锐化、不改色。PDF嵌入PNG的RGB与透明通道另作逐像素解码核验。原始130张选图未修改，原始透明图及完整生成素材仍在各批原交付中。

## 制作资料包的边界

本ZIP是排版与来源核验资料包，不是完整素材源集。它含生成脚本、130图选稿与来源SHA清单、字体子集与许可、嵌入副本说明、布局数据及核验报告。为保持小体积，不包含130张原始PNG、浏览PNG、raw、历次废稿、原生工具返回或各批完整源ZIP。

从本资料包复现，需要已有Stoneshard_mod项目及selection_audit.json列出的130张原始选图。原始素材路径和SHA均已列明；缺少这些图片时，不可称资料包能独立重建整本图册。

## 在原项目中复现

把资料包内容放回 Assets/CharacterDesigns/20261013/expressive/new_story/catalog_v1/，在项目环境中运行：

    python build_catalog.py --max-px 520

需要 Python 3、Pillow、PyMuPDF、fonttools。脚本优先使用资料包附带的简体中文字体子集；仅当该字体文件缺失时，才从系统 Noto Sans CJK 的SC字体面生成。脚本只在catalog_v1内生成浏览副本与文档，读取原素材并核对SHA，不改原素材。

已有production/embedded中的130张浏览副本时，可以使用：

    python build_catalog.py --max-px 520 --use-embedded

此快速重排方式仍须核对embedded_manifest.json中的SHA。浏览副本没有包含在小型制作资料ZIP中。字体CFF子集保留原字形ID，避免PDF阅读器中文错字；PDF图像显式使用最近邻显示偏好。

## 核验记录

- source_audit/selection_audit.json：130张实际SHA、角色/标签、概念母图绑定、独审、22个表情交付包与回执定位。
- source_audit/audit_summary.json：来源核验汇总。
- production/embedded_manifest.json：浏览副本尺寸、缩放方法与前后SHA。
- production/layout_objects.json：每页文字与图像位置。
- LAYOUT_VERIFICATION.json：自动计数、出界、缺项与文件大小检查。
- review/PDF_IMAGE_DECODE_QA.json：PDF内130图解码后RGB和透明通道与浏览副本逐像素一致。
- review/QA-independent-layout.json：最终24页实际查看报告，绑定最终PDF与页面PNG的SHA。
- REPRODUCTION_QA.json：从相同来源重新生成并比较最终PDF/总览SHA。
- FINAL_SOURCE_FREEZE_QA.json：最终选图与所引来源文件只读复核。
- OUTPUTS.json / DELIVERY_MANIFEST.json：交付文件的页数、大小、SHA。

所有核验只说明当前文件、来源与版面状况，不替代用户审美确认或游戏实测。
