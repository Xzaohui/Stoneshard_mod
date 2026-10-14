# 场景补画与导入说明 v2

本批包含43张生产PNG，对应原清单5项视图。502项静态检查通过；原生游戏装配和运行未验收。

基于R01-camp-canal-v1补画观察物件。旧版本完整保留；地面、阻挡、门口、屋顶及浅滩/回程提案逐字节保持。基础空间导入详见BASE_IMPORT-v1.md。

打开preview.html切换平面地图、建筑外观、屋顶下空间和有条件回访道具。所有生产路径相对本目录，导入assets/，不要导入raw/。关闭平滑和mipmap，比例1像素=1房间像素。

绘制顺序：backing → floor → structure → story_underlay → 按脚底Y排序的原独立物件/body与原生人物 → story_details → 对应条件的conditional_cues → foreground → roof。预览合成图仅供检查，不能和独立物件重复绘制。

scene_cues在manifest.json及layouts.json中登记。pixel_anchor=(cell*26+13)+pixel_offset；PNG左上角=pixel_anchor-origin。灰圈为地面观察贴花，借据位于轴座下；这两个锚点是贴图基准，不是角色脚底。所有新增PNG均不提供碰撞，alpha不能作为碰撞。

scene_cues不是已实现游戏事件，condition为接入契约。N18绳鞋摊只在对应回访显示；SQ04字条须拒绝强运并进入对应回访，不抹除transport_harm。两者默认隐藏、分别切换，不代表家属同意或伤害结清。

井牌留空供引擎绘字，红桶为准确两只且不作库存/饮用性结论；借据小印仅作观察线索，不认证采购链。灰圈没有亡者、符文或魔法效果。人物与对白由另一模型负责。

共享新增母图保存在cue-source/raw/，六格拆图和区域128色量化见cue-source/manifest.json；其生成锁、完整提示词与SHA另存cue-source/。继承母图的原锁不改，generation-log.json区分records与external_generation_records。两批共享同一新增母图，全项目按输出SHA去重。

本次更新复核N2/N5/N9/N18/SQ04；N9变化为文字与知识交叉条件，现有公共桌、河窗、分柜仍适用，没有新增栅格物件。源文件从未被本工具修改。

复现：Export-Hd2dSceneCueSync.py → Validate-Hd2dSceneCueSync.py → Package-Hd2dSceneCueSync.py --preview-only → 浏览器检查 → Package-Hd2dSceneCueSync.py。复制的旧原稿、基础提示词与v1包不覆盖。
