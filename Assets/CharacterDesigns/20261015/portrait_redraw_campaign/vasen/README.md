# vasen portrait redraw candidate

状态：待修订、未通过，当前v1证据包冻结。按协调者转达的用户当前合并推送要求，不启动v2或任何新生图。此工作包不自行执行git。

候选：candidates/portrait_v1_74x100_candidate.png。仅1次实质内置image_gen，最多1次必要修订的额度尚未使用。完整实参在prompts/portrait_v1.json，完整回包在tool_returns/portrait_v1.json；raw与回包解码逐字节一致。

待核/修订：
- Right contour has only 1 logical pixel true clearance; hair/hat intact but margin below requested safety target.
- Eye whites brighter than requested; beard/gray hair retain more fine detail than four-core target.

技术：整张raw按比例NEAREST包含到74×100，alpha阈值128，MAXCOVERAGE最多32可见色、不抖动。候选、1x原尺寸、8x整数NN和三底预览独立保留。技术派生不等于原生像素终稿，未游戏集成或验证。

复现：python derive_portrait.py portrait_v1
清单：python finalize_manifest.py portrait_v1 pending_revision_not_approved_frozen

身份与来源：约50岁男性磨租人；棕色软布帽、灰眉灰侧发/完整短灰胡、厚鼻、锈红圆开衩工衣与暗围裙带，沉思迟疑；最新卡的面粉旧围裙作为下沿小提示，胸部以下物件不入肖像。 来源当前SHA、历史SHA变更与母QA见sources/source_manifest.json和源快照；四核心与母图已实看，无身份硬冲突。QA40初审要求修订，反馈见qa/independent_initial_feedback.json；冻结后不执行v2，不冒称终审通过。manifest的selected_portrait与selected_sha256均为null，delivery_eligible=false，仅保留provisional_candidate用于追踪。

无脚本画脸/几何修脸，不修改旧图、人物卡、代码、冻结索引，不commit/push。
