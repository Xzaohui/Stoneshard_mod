# Sela C：面部重新组织，供审阅

C基于原1:1 Before独立修改，不在A/B之上反复叠加。A/B文件完整保留。根审看认为A/B仍受长侧脸读形支配、眼窝缺乏焦点，因此C允许后收遮脸的内发际边缘，把脸内五官重新组织成偏左3/4；不变的是头身17:17、头外宽高、外发髻、下颏、身体、衣装、手脚和肤色主调。

## 先看图

- `mobile_before_C_references.png`：600×1180手机对照；上排BEFORE/C，下排ORIGINAL REFERENCES（Gunda/Bert）。每个人包括完整原生画布6倍全身与10倍整头特写，无平滑插值、无边缘截断。
- `comparison_C_originals_1x.png`：Before/A/B/C/Gunda/Bert，原生尺寸，必须先看实际读形。
- `comparison_C_originals_8x.png`：同序全身8倍。
- `face_C_closeups_10x.png`：同序整头10倍。
- `sela_face_C_native.png`：35×44透明native；`sela_face_C_8x.png`为透明8倍预览。

## 具体组织

内发际后收以露出额面；远眼(12,14)为一枚暗点，近眼(15..16,14)为两枚暗点，鼻梁肤色隔开两眼。鼻为脸内部的色面，取消突出的最外侧鼻尖与其下缘两像素；y18为可辨识皮肤行，y19用暖肤阴影短标记提示嘴，避免深棕嘴线像胡茬。没有新增眼白、高光、口红色或纹理，没有整体提亮。仍用原共享色板，手部完全不变。

`face_allowed_envelope_C.png`是明确许可区域x10..18/y11..19，含需要后收的少量内发际；`face_mask_C.png`标出实际50处像素变化。改动数仅作审计，不作美感达标标准。`pixel_edits_C.json`逐像素保存RGBA前后与按功能行记录的原因。

## 实际视觉审看

制作方、根审看与独立审看均实际查看当前图。C较A/B更有清晰的双眼分工，鼻转入脸内，鼻口间皮肤可读，长侧脸读形减弱。近眼上缘仍略平，眉眼是克制合并的暗簇，表情偏沉静严肃；目前没有值得立即再改的严重问题，本轮停止像素游移。C为主展示候选，不是用户定稿或游戏运行验收。

## 验证和来源

原native SHA：53b588b17eae59d3bdebd7190f7cf96e35c297354393dcf34174c49777f41b98。

C native SHA：7176706fe53403dad1f8df41fc3da4c19488076380d06b2947d569620d6b39e2。

许可面部范围外逐像素相等；y20及以下、y10及以上整行相等。顶y4、足底y37、可见34像素、末下颏y20保持；二值alpha、透明RGB零、单8连通、零新颜色。生产QA、独立QA、重复生成QA分文件记录。原作参考只并排显示，不复制五官或服装，不采样其色板。

本轮只用已授权的现有Pillow/NumPy做显式像素编辑和排版，没有imagegen调用；上游Before来自项目既有概念提取记录。没有安装软件、改runtime/global、扩其他演员或push。

可从项目根重复生成到独立目录：

    python Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/c_reorganized/build_c.py /tmp/sela-face-c-reproduce
