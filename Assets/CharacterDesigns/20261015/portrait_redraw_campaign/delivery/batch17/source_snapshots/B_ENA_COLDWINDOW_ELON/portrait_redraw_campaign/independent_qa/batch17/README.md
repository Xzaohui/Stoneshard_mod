# Batch17 独立 QA 冻结交接

缇弗、薇榆、冷窗艾娜、礼昂统一选择 portrait_v2_74x100_candidate.png。四张作为生成重绘/量化派生候选通过，不是原生像素终稿或游戏运行验收。

- 当前人物卡、精确母版、选版 QA 与四核心实际看图；55 条源/快照哈希通过。冷窗艾娜严格为 MAE-S03-NPC，与 NPC-N-ENA 分人。
- 每人初稿＋一次集中修订，共8次生成；8份raw逐字节等于完整工具返回，工具保存原件相同。
- 不调用作者导出脚本，在本审计目录独立复现8张候选，PNG字节、像素、8倍NN预览均一致。四张所选v2为74×100，32/32/32/31可见RGB色，alpha仅0/255，四边透明。
- 四个冻结manifest、两份SHA256SUMS和两份等价file_hashes.json完整库存通过。
- 无身份冲突held。余项：细发纹、部分暖灰眼块，礼昂少量细须和较重额纹；已如实记录，不继续第三次生成。

入口：freeze_manifest.json（精确所选路径、SHA及所有角色目录文件冻结哈希）、final_technical_audit.json、v2_visual_reviews.json、selected_v2_four_character_contact.png。早期报告为修订前快照，以final_technical_audit.json为最终技术结论。

审计只写 independent_qa/batch17，未修改生产卡、旧图、角色生产目录或代码，未生成新图、提交或推送。

复核：从仓库根运行 python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/independent_qa/batch17/audit_batch17.py final_technical_audit.json。会只重写本审计目录的报告及独立复现PNG。
