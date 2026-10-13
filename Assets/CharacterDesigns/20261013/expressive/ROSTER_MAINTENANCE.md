# 人物清单维护

本目录管理表情化概念候选，不改变剧情卡、旧图或游戏资源。

## 数量依据

- 基线：`src/EmbersAndOaths/Assets/ConceptDrafts/20261012/coverage-cast-through-batch47.json` 的156条城市／聚落卡记录。
- 只追加7名未重复的根级主线人物卡、5名台本新增具名配角、开篇人物表4人。当前172名，局限于这个明确范围。
- 角色卡frontmatter、现行台本ID、城市ID都保留在sources/aliases；例如凯姆、莉德、米娅不能按ID各生一身体。
- 同名不能直接合并：布林装帧师艾伦／逃兵艾伦、聚落艾娜／灰堤艾娜各自保留。瑟拉与塞娜也不是同一人。
- 角色组、章节标题、普通泛称、板数不得当新人物。未做所有任务全文演员穷举，不声称全体人物完备。

## 继续批次

1. 阅读候选的源卡和当前约束；原作人物须核实原版身份外貌，不以风格参考替代事实。葛文涅尔暂停。
2. 在briefs下每3人写brief：ID、姓名、source、旧设计、衣装道具、性格情绪、剧情约束。外形提案不要反写成剧情事实。
3. 给有任务的记录设置work_directory、generation_assigned。新图产生后可运行`python Assets/CharacterDesigns/20261013/expressive/refresh_roster.py`更新PNG清单和索引。
4. 脚本不会从QA文件存在或PNG数量自动判通过；reviewer必须看实际图，记录具体文件名、审看记录和状态。旧版退修不妨碍新版另审，但不能把新版文件出现当修好。
5. 手工更新roster.json的status、visual_review、review_record、reviewed_artifact，再运行脚本同步INDEX；脚本保留这些人工判断。
6. `--check`只校验，不落盘。校验稳定ID唯一、源卡和旧图路径存在，不代替审美审查。

所有新概念runtime_integrated保持false。用户认可仅登记实际认可的文件和范围；不得把一个人的美感认可推广到全清单。

## 身份别名校验（2026-10-13修复）

alias_identity.py只读当前人物自身源卡ID、精确台本section ID和有明确归属的组卡别名。不能从视觉参考、其他人物brief或文件名猜别名。refresh_roster.py --check会拒绝不符源证据或跨人物重复的别名。初建脚本曾使用共享默认aliases=[]造成污染，已改None并逐记录复制，禁止重新执行历史初建器覆盖当前名册。修前后差异见ALIAS_REPAIR_AUDIT.json。

## 选稿路径基址

`reviewed_artifact`忠实记录独审QA的artifact字段，基址为`Path(review_record).parent`，不是work_directory。Mia的独审位于mia/ratio_1_to_1_5/，因此其basename在该子目录解析；普通主QA中的rework_v2/等相对路径同理。proposal与送达artifact使用完整项目路径，并核实际字节SHA。work_directory只供原稿库存扫描，不能作为所有独审选稿的统一基址。
