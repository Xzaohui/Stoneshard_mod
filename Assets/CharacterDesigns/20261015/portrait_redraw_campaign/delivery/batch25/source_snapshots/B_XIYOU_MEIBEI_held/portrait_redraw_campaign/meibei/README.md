# 梅蓓 / YOS-S01-NPC 头像重绘保留稿

状态：`held_composition_scale_and_eye_sclera`，`delivery_eligible=false`。没有生产选择，manifest的selected字段为null。保留稿：`candidates/portrait_v2_inset_74x100_candidate.png`，SHA256 `9e0fa488360f5d334e1d8c2fc52438159256534350d6c12bccbfd30ee8963b70`。

两份内置imagegen成功输出（初稿＋一次集中QA后修订）均完整归档；另一次六参照请求在参数校验阶段拒绝、未产图，原实参与错误独立留档。不做第三次生成。

独立QA认为v2虽缩短颈部，但白巾/横发仍挤小脸，轮廓仅78px高，眼白偏亮偏大；溪悠衣领仍过宽。源轮廓闭合、未证实裁断，但不能以技术inset称构图已修复。保留稿不交生产，详见`qa/independent_review_acceptance.json`及独立batch25对照。

74×100 RGBA、32个可见临时色、alpha0/255。inset从同一v2 raw整个画布等比NEAREST缩入72×98框后居中；阈值128、MAXCOVERAGE无抖动限色、透明RGB归零只作技术派生。不裁脸发、不脚本绘脸、不改变面部几何。不是逐像素原生终稿、审美通过或游戏运行验收。

预览：1x、8x最近邻及三底色1x/4x。源卡/母图/母QA/母manifest/剧情和四核心风格图快照及SHA见sources；按最新卡保年龄衣着，母版和四核心均实际查看。完整prompt实参与工具原始回包见prompts、tool_returns。

复现：`python derive_portrait.py portrait_v2 inset`；清单：`python finalize_manifest.py portrait_v2_inset held_composition_scale_and_eye_sclera`。

旧图、角色卡、代码、冻结索引未改；未commit/push。
