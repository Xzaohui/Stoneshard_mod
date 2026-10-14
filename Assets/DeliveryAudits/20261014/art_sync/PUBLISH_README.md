# 当前美术归档与发布审计（2026-10-14）

当前素材概况见 [ART_SUMMARY.md](ART_SUMMARY.md)，数量与状态证据见 [ART_SUMMARY.json](ART_SUMMARY.json)。这两份是当前汇总，历史图册与冻结审计不重写。

## 合并与保存范围

- 本地 main 与实际 fetch 后 origin/main 均以 `86f630cd71ecfaea3e4a3920c3045477ac0e0ed4` 为基线，ahead/behind 0/0；`git merge --ff-only origin/main` 返回 Already up to date，无冲突，无覆盖远端剧情或代码。
- 选中10,269份新增/修改散文件和156份最终源包、必要生产证据ZIP，合计10,425份、4,371,349,483字节。新增本审计自身不计入上述素材总数。
- 逐文件路径、字节数及SHA-256见 PUBLISH_MANIFEST.json；最大素材18,768,421字节，全部低于GitHub 100 MiB单文件上限。
- 189份未跟踪ZIP完整递归检查：9,426成员（含2层内嵌ZIP），CRC和内容扫描通过。156份入库，33份重复、过时及中间打包留本地；选择与排除原因见 ZIP_AUDIT.json、EXCLUDED_ZIPS.json。之前已跟踪83份ZIP保持原状。
- 原始图、完整生成返回中的图像payload、失败候选、选稿、提示词、原参数记录、QA、独审、最终状态及冻结源清单均保留。失败图不计为合格图。
- 不纳入 output/gap_repair_20261014_index_audit 的9份临时文件；两份 research/story-*-validation.json 仅换行变化，保留工作树不提交。

## 文件检查

常见凭据、私钥、签名下载URL及认证参数模式未发现真实命中；5处弱参数模式均为压缩PNG/PDF的二进制巧合，文件不含HTTP字节，PNG元数据为空。扫描覆盖实际内容与ZIP内成员，不仅检查扩展名。全部新增JSON解析通过，PNG签名正确；4份Noto字体子集均带相邻许可证。未纳入商业游戏包、DLL、玩家存档或完整原作资源。

只读复核命令：`python Assets/DeliveryAudits/20261014/art_sync/verify_publish.py`。脚本逐项检查素材大小、SHA-256、单文件上限及ZIP CRC。它不是视觉QA、文学验收、构建或游戏实测。

## 发布状态

截至本说明写入时，前三组本地提交已建立：

1. `c297501265fd283f99f4607b6c579eebef05a1ba`：人物概念、表情与修复源档。
2. `24de4f6`：职业动作、补缺与摇头小样。
3. `8d391d0`：敌人与场景选稿、失败稿及制作源档。

普通HTTPS push因当前命令行缺少GitHub登录凭据未完成；只读远端核验仍为基线86f630c。GitHub连接器能读取且报告当前账号具有仓库push权限，但不等于命令行Git已经认证。未强推、未改远端权限、未创建新密钥。后续成功发布须以远端refs/heads/main实查为准，不能从本地commit推断远端已更新。当前没有本批远端提交的CI结果，不能声称CI通过。

为避免大批Git pack超过服务端限制，恢复认证后应按本地提交顺序逐个普通快进推送，而非一次发送整个增量。最终审计提交包含156份源包与本目录文件。
