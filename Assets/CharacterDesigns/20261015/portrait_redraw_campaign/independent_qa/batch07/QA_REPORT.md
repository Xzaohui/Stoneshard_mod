# Batch07 独立头像候选QA

冻结结论：4/4通过候选门槛；并非原生逐像素终稿、用户最终认可或游戏集成。

## 选稿

- 麦勒 / BRY-NPC-MALER：`maler/candidates/portrait_v1_maxcoverage_74x100_candidate.png`
  - SHA256：`cf121c74bdb20d919f966bd46cec266fbed040f8672c305bba4a12e914f52ac3`
  - 74×100，32可见RGB，alpha仅0/255。六十余岁男性老楼房主；低帽、灰发修须、瘦高年长骨相、长鼻与防备计算侧望。深色磨亮呢外套依最新卡，不扩胸展示异色扣。
  - 限制：灰须纵向亮暗条仍稍细；旧眼镜压痕只作为鼻侧微小暗面，不声称74×100可逐条证实。
- 玛莉丝 / BRY-NPC-MARIS：`maris/candidates/portrait_v2_maxcoverage_74x100_candidate.png`
  - SHA256：`41cc2ec1ce6fcf93ceabcfe3eae90ca281198044760cf30e129ed966ef055d36`
  - 74×100，32可见RGB，alpha仅0/255。成年女性精灵匠商；成熟长脸、细直鼻、棕辫、长尖耳与深色紫褐窄领明确。v2去掉眉间忧折，内眉更平稳，窄眼与闭嘴轻笑转为自持精明。
  - 限制：1x笑意很轻，仍偏克制；不赋确切年龄，不扩大为族群代表。
- 米罗·账 / BRY-NPC-MIRO：`miro/candidates/portrait_v2_74x100_candidate.png`
  - SHA256：`2313b1f4817818e8c5e745533d8916259ccf4583ddd57eaced7a8e0c8c0c5998`
  - 74×100，29可见RGB，alpha仅0/255。约50岁男性商户联络员；深色商褂好料窄内衬、周正鼻颧、整齐深色短须与眼尾成熟面成立。v2头脸占比上升、长颈压短、严虑眉间减弱。
  - 限制：礼貌眼笑仍很含蓄，灰鬓不明显；年龄通过眼尾、鼻侧与下颊成熟骨面表达，不能当逐像素终审。
- 奥德 / BRY-NPC-ODER：`oder/candidates/portrait_v2_74x100_candidate.png`
  - SHA256：`d560db07ffb8c3634f06b8a37d6d810500b86ea31a8c752b2bd662f4062086a6`
  - 74×100，29可见RGB，alpha仅0/255。BRY-NPC-ODER五十余岁靠泊席位船主，使用latest_card_alignment_v1身份母版。宽脸宽钝鼻、旧木色晒肤、深发短须、务实担忧侧望及短打水手褂窄领正确。v2压短颈领、保留成熟厚重骨相。
  - 限制：胡须仍有少量细条；眉盐霜未能逐点确认。手不在头像内，不声称左小指缺半截已核验。不是held欧达，也不是旧工匠。

## 独立核验

- 已实际查看四人身份母版、四核心风格、v1/v2对应1x/8x与两种量化对照（适用时）、最终四人同屏。
- 51条live source与snapshot逐字节/SHA一致；旧卡历史SHA变化按当前卡重读，未当作身份错误。奥德明确使用latest_card_alignment_v1船主母版。
- 7份成功生图的完整tool data payload、保存raw、工具原输出均逐字节一致；3次参考图数量校验失败没有生成图，单列不计成功稿数。
- 全10份74×100候选通过尺寸、≤32临时可见RGB与二值alpha检查；透明像素RGB归零。独立实现整幅NN采样、alpha128、无抖动MEDIANCUT/MAXCOVERAGE，像素及PNG字节全部复现。
- 全10份8x预览精确对应目标图的最近邻整数放大。四个producer manifest及SHA清单全部复核，选稿hash与最终清单相符，manifest文件无遗漏。
- 只写本独立QA目录，未修改生产卡/母版/脚本/代码，未生成新图、未提交或推送。

## 边界与剩余制作工作

- 74×100由高分辨率imagegen整图NN缩放、二值alpha与暂定调色板量化而来；没有原生逐像素手工修整。32色只是工作上限，不证明原生像素风。
- 未核引擎专用调色板、对白UI放置、装备分层与游戏实际显示。
- 画外手部、道具与剧情结果不声称已核验。玛莉丝无确切年龄；奥德小指未出画面，不能写为细节全通过。

证据：FINAL_SELECTION.json；technical_audit.json；preflight_source_checks.json；INITIAL_VISUAL_REVIEW.json；selected_candidates_1x_4x.png。
复跑：在仓库根目录执行 python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/independent_qa/batch07/audit_batch07.py（只写QA目录）。
