# 贝洛 / MNS-NPC-BELO 肖像重绘锁定

- 范围：74×100对白肖像；仅本角色新目录，不改旧素材、人物卡、代码或全局索引。
- 来源：sources/source_manifest.json；母图及四核心已实际查看。Latest card explicitly says twenties, oiled cooper apron and tied cuffs. Head-only portrait preserves black short hair, clean-shaven adult face and slate-gray shirt collar; waist apron/cuffs are out of frame.
- 哈希：当前卡与roster的当前字段核对；不把历史哈希差异静默当作身份冲突。
- 构图：完整头发和可见耳轮，真实透明余量；大脸、短颈、底部窄领，禁宽肩长胸。
- 风格：少量连续颧骨鼻梁色块、小暗眼、弱眼白、年龄个性可辨，最多32个临时可见色，二值alpha。
- 生成：built-in image_gen实质重绘，每人v1与最多一次必要v2；初稿送集中QA后再决定，不第三次。
- 技术派生：整画布等比NEAREST containment、alpha阈值、无抖动量化。不是原生像素终稿，不脚本绘脸。
- 场面：哈伦只答有限桥工/伙房与接收班次；贝洛是成人箍桶学徒，不与酿酒学徒提奥混同，不演署名和解或危险试塌。
