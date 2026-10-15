# Design Specification

## Project Overview
库奇（FX-BUR）两种可逆面部表情概念。

## Asset Requirements
- kuqi_E1_wry_joke_about_fear：笑认怕死。笑话不表示危险已清、身体康复、任务完成或买卖成交；不画金币/丝货交付，不替人进洞，不把瘦小中年幼化或怪物化。
- kuqi_E2_serious_about_burrow_risk：谈洞敛笑。只演说起洞内风险的认真，不画已经探洞、拨网、救人或交付遗物；不保证蛛窝数量或通路安全，不确认N12结果、葛文涅尔去留或自己的腿已治好。

## Art Direction
本人母图单一身份参照，透明完整全身，清楚粗像素簇。

## Technical Requirements
Builtin imagegen，transparent_background=true。实际工具画布入日志；原RGBA保留，不机械改比例。

## Animation Requirements
独立静态表情概念，不称动画或运行素材。
