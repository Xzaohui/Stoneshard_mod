# 谟珥｜两种可逆表情

FX-TRS，工作标识 moer_trs。本目录仅含两张独立单人全身表情概念，不是连续动画，也未验证游戏运行、原生网格、part/frame/mask/origin或装备兼容。

E1眉较抬、开口讲述；E2眉内收、视线低移、紧闭口无笑意。保留二十多岁中性成年外观、赭黄衣与崖灰、右肩后D形铲把及左髋后刃，胸腹无横轴；不引入同伴下落或听审结果。

- selected：两张1118×1407透明选稿。
- raw：内置imagegen原始PNG；首稿各1次，无修订。
- prompts：调用前保存的逐字真实prompt及完整工具参数。
- tool_returns：原返回完整JSON，不覆盖；其中image_url解码逐字节等于raw。
- sources：母图完整历史目录、人物卡、台本、research与规则来源快照；历史废稿/他人style_refs只保留来源链，没有作为本次调用输入。真正引用限generation-log.json所列本人最终raw和transparent；谟珥只用最终v2。
- review：中文浅深板和raw的RGBA可见合成板。
- prepare_assets.py：仅alpha清理与最近邻排板；不画身体、不硬缩35px、不量化。
- QA-author和独审报告分开；最终状态以FINAL_STATUS.json的具体SHA绑定为准。

两种表情并无先后任务结果；本人存活、在场、愿谈及有限知情才适用，拒绝与授权仍独立。
