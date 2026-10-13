# 人物动作关键帧研究 · 2026-10-13

本目录为概念关键帧与效果研究，不是Stoneshard原生动画资源或换装实现。参考原版事实见`Assets/ReferenceAudit/20261013/actions/REFERENCE_AUDIT.md`。齐勒源卡不支持战斗，故身份动作与无身份训练攻击分开。

## 当前可查看内容

- 齐勒静站保持：`chiler/idle_v1/chiler_idle_keyframes_review.png`。3逻辑帧/2不同图，但吸息不可读，只算静站保持/极小变化研究，不计有效呼吸动画。
- 齐勒原创短步：`chiler/walk_v1/chiler_walk_review_zh.png`。支撑→摆步→接触，3不同姿态（源+2新图）。独审通过概念展示；W2后足可靠接触未证明，非无滑步/完整循环。
- 齐勒受惊回稳：`chiler/startle_v1/chiler_startle_review_zh.png`。3逻辑阶段/2不同图，复用回稳写明；非剧情受伤。独审状态以对应QA为准。
- 无身份成年训练攻击：`adult_training_dummy/attack_v1/dummy_attack_4stage_review_zh.png`。4真实新姿态，预备→蓄势→挥出→回收。身段较齐勒细长；剑长投影、握点与支撑轨迹待独审，不称同体型装备兼容。
- 无身份训练受击白闪：`adult_training_dummy/hit_fx_v1/dummy_hit_fx_review_zh.png`。1张既有主体/3显示状态，白闪为独立可关闭效果层，无新增关节姿态。颜色、透明度、时长是原创提案，红选中不当受击。

## 全局约定

所有导出逻辑画布1536²，工作足点(768,1380)不等于引擎原点。不同脚在透视/摆步中可不同高度。单次GIF是检查节奏，无插值；动作段落不伪装无缝循环。所有生成都使用内置imagegen，原输出和完整prompt保留；只用已授权像素脚本做画布归一、清淡alpha、整图配准、检查板和明确效果合成。

原始生成共8次：齐勒静站轻变1、短步2、受惊1，训练样板攻击4。不能把8次生成等同8个已通过动作。engine_origin/native_fps/collision均unknown/null；runtime_verified=false，装备兼容未验。扁平整身图不等于可换装分层母版。

## 最终安全交付

默认交付位于`delivery_safe/`，受惊、白闪、固定剑几何三组均完成独审。攻击以`delivery_safe/adult_training_dummy/attack_v2_geometry/`为当前版本：同一320px刃轴、刚性变化、独立遮挡层。原attack_v1只历史来源，不是当前默认。安全导出仅清alpha=0区RGB，29项全部保有效像素/alpha不变，避免检查器误显透明区旧色。

7件文件已保存Library，源包`action_keyframes_source_pack_safe.zip`为8.27MiB，无官方参考GIF；记录见DELIVERY_RECORD.json。当前可交的是概念关键阶段和固定剑层样板，不扩大为完整无滑步循环、native或换装系统通过。
