# 摩珥：两种独立表情概念

身份：摩珥 / FX-WIL / 工作slug moer。

- 旧账自嘲：提起曾收过一次假凭证，短暂流露对自己那次吃亏的无奈自嘲；这是对原句口气的可逆美术解读，不新增损失数额、骗局细节或责任判定。
- 免账正色：听到想免一次账的请求，快速生意口吻收紧成一句平静而坚决的“不行”。

## 制作与可核证据

本轮使用 builtin image_gen.imagegen，每张一稿，无修订。生成前逐字prompt先写入prompts/，完整参数与输入SHA一并保存。raw/*_tool_return.json 是逐次原始工具返回完整对象，含原image_url与output_hint，不以派生日志覆盖；其中data URL解码SHA与同名raw PNG一致。generation-log.json列出时间、实际参数、输入、raw及selected哈希。

全部原图保留。selected仅将alpha≤8归零并清理alpha0隐藏RGB，alpha>8的RGBA字节全部保留；无身体绘制、拉伸、重采样或调色量化。review浅深板只对完整全身做等比最近邻排版，文字只在展示背景。实际尺寸1118×1407。

母图、当前卡、对白、相关任务、brief、风格和规则在sources/files，source_index列原路径和SHA。母图衣色与表情仍为可逆美术提案，不提升为剧情canon。

作者实看记录在QA-author.json，独审结果在QA-independent-raw-visual.json和QA-independent.json；最终选稿与冻结状态由manifest.json和FINAL_STATUS.json收口。日志内待独审字样只记录生成时点。

## 边界

两图不是连续动画或前后结局，仅本人存活、在场、愿谈且有相应有限见闻时适用。不新增付款、任务结算、治疗、授权、关系或承诺。不声称原生像素网格、part/frame/mask/origin、装备兼容或runtime通过。

只用摩珥 / FX-WIL / moer；谟珥 / FX-TRS / moer_trs是另一人，不借短铲、赭黄外衣、崖灰或同伴剧情。
