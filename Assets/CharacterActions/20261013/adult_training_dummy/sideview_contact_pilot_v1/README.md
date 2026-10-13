# 真侧视接触位试验 v1

全试验3张新图已用尽，停止生图及补救。S0先通过独立相机／比例／衣装／近靴审查（QA-independent-S0.json），随后各生成1张S1/S2；接触位整组独审未通过，S1靴尖卷翘／靴长改变原设计，S2腰扣移到身体后侧；S0侧视门槛仍通过。

角色是同一成年训练样板。原锚interaction_v1/raw/I0_stand.png，锚及所有原稿SHA见manifest.json。新侧视仅是原创设计推定，不是Stoneshard实际规格。prompts保留每次完整内置imagegen提示词。

raw内S0_stand.png、S1_contact_right_front.png、S2_contact_left_front.png均为完整未修改工具原稿，没有脚本拼腿、镜像、修身体或逐帧拉伸。S1和S2均使用通过的S0为唯一图像锚。

sideview_contact_review_zh.png使用整张画布统一0.5倍最近邻排版，未按人物包围框分别拉伸；只贴图及说明文字，不修改身体。原稿画布都是1254²，但各图人物覆盖范围仍略有差别。

自检：S1近亮腿向前、近臂向后；S2近亮腿向后、近臂向前，髋部遮挡方向有变化。S1前靴翘尖与鞋长可能漂移；S2前靴较平，腰扣位置从前侧漂到后侧。独审确认这些是整组未通过的硬错；不再追加修图，保留失败研究。S0可单独作为侧视概念候选，不计新完整角色。

只交静态研究原稿与对照，不制作步行GIF，不宣称完整自然步行已解决，不做引擎落地。

## 最终独审存档

QA-independent.json已确认整组为research_only_contact_pair_not_accepted；SHA256：76502bac946e7917777c3e80fc4ef335ce9897edbda028569640b2a23fbb5387。S0此前侧视门槛通过仍保留，S1/S2只作失败研究。审查后未修改raw或静态板，不追加生图，不上传。build_review.py为审查前排版来源，勿重新执行覆盖冻结状态；最终状态以manifest及QA为准。
