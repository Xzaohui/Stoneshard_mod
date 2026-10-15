# 蕾因 LEIN 暂缓说明

蕾因当前 selected_portrait=null、selected_sha256=null，独立QA判定 held_source_contour_margin_and_style。她不在三人总览中展示头像，没有单独成功PNG，不计入本批成功候选或累计已发送数。

v2右侧源边界（x=1085）alpha最大47；alpha≥128边界计数0，alpha≥16计数69，alpha≥5计数108。不是“整段全不透明像素已被切断”。源外轮廓是否完整、真实透明余量未获独立确认：x=1084有近不透明深发，边缘半透明发沿延到最后源列，不能用alpha≥128的零计数证明真实余量安全。inset只改变目标网格边距，不能恢复未知源外内容。

眼白仍不全暗、上眼线与平行发层仍强；v1也未通过风格门槛，不能回退v1冒充成功。每人仅一次集中必要反馈、两次成功生图，不做第三次。

证据：lein/candidates/portrait_v2_inset_74x100_candidate.png
证据SHA256：7e1d2ba859c3656cd812b6e3f318665b4faf295c8cc14c422f113aa63a4298a6
v2 raw SHA256：0049e04b3eb10f19dac6a098e57676abe47842c9fdf0a4c7ee33bf369987274b

源包B保留蕾因完整制作目录：两张成功raw、完整回包、完整提示词与真实参数、v1/v2/v2_inset历史派生及全部QA，包括多阈值边界数值与3倍最近邻边缘图。历史与暂缓图只作证据。
