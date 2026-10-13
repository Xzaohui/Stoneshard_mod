# Stoneshard 装备组合：公开源码证据
核实日期：2026-10-13。仅公开源码只读调查；未运行 StoneForge，也未读取用户本地 vanilla.win 或原版函数体。

## 可支持的结论
玩家外观由预先画好的身体、头、头发及装备部件在运行时组合。公开 Mod 实现直接读取游戏的部件数组，调用游戏的 scr_playerSpriteUpdate，取回生成的角色精灵。因此不需要穷举每种人物×全部装备组合的整身图片。更准确的描述是“部件合成角色精灵”，不宜未经核实说每帧都逐层直接画到屏幕。

## 核心实现与定位
来源：StoneForge.API/Characters/CharacterLook.cs
固定链接：https://github.com/StoneForgeTeam/StoneForge/blob/df8d667273a6124be7692a6aab7863e0c8c65d52/StoneForge.API/Characters/CharacterLook.cs
仓库commit：df8d667273a6124be7692a6aab7863e0c8c65d52；GitHub commit API返回日期2026-10-13T03:37:27Z；提交标题StoneForge 0.9.6。此0.9.6是加载器版本，不是Stoneshard游戏版本。
文件blob SHA：d410c08daccd01ba25036ed9626ecfc1cae249d9。

以下仅必要接口短片段，行号对应上述固定版本：
```csharp
26:         using GmArray? parts = Game.Global["playerSpritePartsArray"].AsArray;
27:         GmValue height = Game.Global["playerSpritePartsArrayHeight"];
28:         GmValue framesX = Game.Global["playerSpriteImageNumberX"], framesY = Game.Global["playerSpriteImageNumberY"];
111:             Game.Global["playerSpriteArray"] = built;
112:             Game.Global["playerSpritePartsArray"] = partsArray;
113:             Game.Global["playerSpritePartsArrayHeight"] = parts.Count;
114:             Game.Global["playerSpriteImageNumberX"] = FramesX;
115:             Game.Global["playerSpriteImageNumberY"] = FramesY;
116:             Game.Global["playerSpriteGround"] = Ground;
117:             Game.Global["playerSpriteBody"] = Body;
118:             Game.Global["playerSpriteUpdate"] = true;
124:             Game.CallScript("scr_playerSpriteUpdate", default);
125:             // (Read back from the global: writing into the array we gave it, the game copies it first - copy on write.)
126:             using GmArray? result = Game.Global["playerSpriteArray"].AsArray;
```

同文件5–10行注释明确说明body/head/hair/各装备的sprite按偏移、裁剪和蒙版组成frame grid；83–87行说明Build调用游戏自己的合成器，并引用scr_itemCharSpritesInit按穿戴者调整原点；93行说明部件数据布局来自scr_playerSpriteInit。它们是Mod作者的接口解释；上面的实际函数调用是更强证据。

## 图标、掉落与穿戴资源分开
固定链接：https://github.com/StoneForgeTeam/StoneForge/blob/df8d667273a6124be7692a6aab7863e0c8c65d52/StoneForge.API/Items/ModItem.cs
实际API属性区分InventorySprite、LootSprite、EquippedSprite、WornSprite、WornSpriteFemale、WornUpperSprite、CorpseSprite。注意EquippedSprite是装备槽里的图片；角色身上的图片是WornSprite。
源码注释提到原版穿戴资源命名s_char_，叠在甲上面的额外披风/领口资源s_char_upper_；SetWornSprite(character,file)允许头盔按具体角色头部适配。
该版注释描述胸甲三帧为站立、持双手武器、休息，头盔/靴/披风两帧为站立和休息，护甲画布48×40。它支持“部件仍有预绘姿态变体”，但没有核对用户0.9.4.25安装，不能直接冻结为本项目正式规格；也不代表完整行走/挥击动画。

## 对齐入口
https://github.com/StoneForgeTeam/StoneForge/blob/df8d667273a6124be7692a6aab7863e0c8c65d52/StoneForge.Patcher/GML/Items/scr_stonemod_item_sprite_like.gml
该Mod辅助函数读取原资源sprite_get_xoffset/yoffset，并从global.customizationAnchors按资源ID查询锚点，写到新资源对应项。注释将每次穿戴时的原点设置定位到原版scr_itemCharSpritesInit。它是Mod适配代码，并非原版函数体。

## 合成结果与绘制
https://github.com/StoneForgeTeam/StoneForge/blob/df8d667273a6124be7692a6aab7863e0c8c65d52/StoneForge.API/Characters/CharacterSprites.cs
CharacterSprites包装五个生成资源：Normal、Blinking、FlashNegative、FlashPositive、Mask。For按flash/blinking选择；Dispose使用sprite_delete销毁。支持运行时生成资源解释。不能由这五个资源误推五个动作或五个朝向。

## 部件数据、更新与缓存证据边界
- LookLayer.cs固定版本同上：ValueCount=13；Sprite取Values[0]、Frame取Values[1]、Mask取Values[11]，另有SpriteOrigin与MaskOrigin。注释说明其余值包含offset、clipping、clip sprite和mask colour。此处没有凭空为所有索引命名。
- CharacterLook.OfPlayer逐层读取前13个值并记录精灵/蒙版原点；Build恢复这些值，额外加两个false标志。由此确认部件不只是“裁一张PNG”，还有帧选择、原点、遮挡信息。
- Build设置playerSpriteUpdate=true后调用游戏函数，并从playerSpriteArray取结果；最终恢复原全局和资源原点。源码注释指出原版合成器会删除被替换的旧结果。
- 文档示例在Draw回调里以_twin ??= _look.Build()生成并保留缓存；普通Draw随后只画选中的合成精灵。这是Mod示例可验证的缓存行为，不直接证明原版所有状态变化的更新时机。
- 原版穿脱何时置更新标记、是否延迟到某个Draw、切武器组/姿态/休息分别何时重建，当前没有原版函数体证据。只可称“运行时按部件生成精灵”，不写成已经完全追踪到每个重建触发条件。

## 对当前绘图生产的直接影响
1. 先停止按“人物×武器×所有动作”扩展整身成图；先核玩家部件接口，再制作一个体型的换装部件小样。固定外观NPC可另走整身路线，不能强制其全部拆层。
2. 分开交付库存/装备槽图标、地面图、身上穿戴部件；不要直接把漂亮的武器图标缩小当持握图。
3. 保留底体、头发、衣甲、头盔、武器的独立素材与被遮住部分，记录Sprite/Frame/origin/mask契约；披风领口等允许额外上层。
4. 只画经目标版确认确需的姿态变体。公开代码支持站立、双手持握、休息等有限变体，不支持把之前假设的完整行走/挥击序列当原版要求。
5. 大头或不同身材需逐项验证头盔、握点和遮挡。公开API已有按角色头部适配头盔及女性护甲变体，不能承诺同一装备无条件适配全部概念角色。

## 同项目官方文档（该Mod作者的一手文档）
https://github.com/StoneForgeTeam/StoneForgeDocs/blob/83b2e9db4eedab8c962bbb43eddade59da166408/docs/world/character-look.md
文档说明CharacterLook读取玩家分层外观，Build在Draw事件里绘制到surface，再生成可重复使用的角色精灵。示例用_twin ??= _look.Build()保留结果，随后draw_sprite_ext绘制_twin.For(...)。
docs提交日期2026-10-11T13:54:48Z；提交标题说明文档更新至StoneForge 0.9.4。该数字仍是加载器版本。
https://github.com/StoneForgeTeam/StoneForgeDocs/blob/83b2e9db4eedab8c962bbb43eddade59da166408/docs/content/items.md
文档分别说明库存、地面、装备槽、身上、尸体图。

## 适用范围及尚未确认
- 证据来自公开StoneForge源码/作者文档，不是Ink Stains Games发布的原版源码；但可看到其读取原版global、调用原版命名脚本的具体操作，强于泛引擎教程。
- 分支文档表明StoneForge支持Steam默认YYC与VM modbranch：https://github.com/StoneForgeTeam/StoneForgeDocs/blob/83b2e9db4eedab8c962bbb43eddade59da166408/docs/getting-started/game-branches.md
- 本轮未找到明确绑定Stoneshard 0.9.4.25的兼容声明；仓库内该版本字符串搜索无结果。不把加载器版本冒充游戏版本。
- 用户项目记录的目标是modbranch 0.9.4.25、MSL 0.13.2.0，需以后对本地原版函数体及资源元数据核实。
- 尚不能断言原版每种朝向、各动作帧数、是否所有战斗主要使用刚性位移+特效，或所有NPC都走玩家换装通道。
- 未采用本项目自制固定剑层示范作为原版证据。本次只增此调查摘要，不改游戏包、运行代码或美术规格。

