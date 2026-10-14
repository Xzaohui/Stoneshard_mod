from pathlib import Path
import json, hashlib, shutil, datetime, subprocess
from PIL import Image
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
B=R/'Assets/EnemyDesigns/20261013/second_six'
D=B/'action_continuation_sources_v1'
OUT=B/'action_continuation_brief_v1.json'
assert not OUT.exists() and not D.exists(), 'New planning paths must not overwrite existing work'
D.mkdir()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
H=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
J=lambda p: json.loads(Path(p).read_text())
W=lambda p,x: Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=J(R/'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json')
production=J(R/'Assets/EnemyDesigns/reference/20261013/production_brief_second_six.json')
source_files={}
def record(p, role='source', view=None):
 p=Path(p); p=p if p.is_absolute() else R/p
 rel=p.relative_to(R).as_posix(); dest=D/'files'/rel
 if rel not in source_files:
  dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
  assert H(p)==H(dest)
  source_files[rel]={'source_path':rel,'snapshot_path':dest.relative_to(R).as_posix(),'sha256':H(p),'bytes':p.stat().st_size,'role':role}
 out=dict(source_files[rel])
 if p.suffix.lower()=='.png':
  im=Image.open(p);out['size']=list(im.size);out['mode']=im.mode
  if 'A' in im.getbands():out['alpha_bbox']=im.getchannel('A').getbbox()
 if view:out['current_planner_visual_inspection']=view
 return out
base_refs=[
 'AGENTS.md',
 'Assets/EnemyDesigns/reference/20261013/production_brief_second_six.json',
 'Assets/EnemyDesigns/reference/20261013/sources_second_six.json',
 'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief.json',
 'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json',
 'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_supersession.json',
 'Assets/EnemyDesigns/20261013/second_six/ROOT_STYLE_REVIEW.json',
 'Assets/EnemyDesigns/20261013/second_six/INDEX.md',
 'Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md',
 'Assets/EnemyDesigns/20261013/first_six/border_spear_rebel/action_continuation_v1/sources/pixel_asset_master_SKILL.md',
 'Assets/EnemyDesigns/20261013/second_six/swollen_throat_bloodkin/idle_v1/spec_lock.md'
]
base_records=[record(p,'read_planning_rule_or_historical_reference') for p in base_refs]
style_records=[record(p,'style_comparison_only',{'actually_viewed':True,'viewed_utc':'2026-10-14T04:11:02Z','scope':'Actual individual full image viewed in this planning task; not an identity or fixed-ratio template.'}) for p in [
 'Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png',
 'Assets/CharacterDesigns/20261013/expressive/mia/ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png']]
plans=[
{
 'pose_id':'axe_forward_cut','label':'短斧前送斜劈','phase':'攻击释放中后段，向空处斜下送斧',
 'observations':['母图双靴站稳，短斧手低垂，圆盾在画面右胸腹侧。','shield_brace是宽步沉身、盾高斧低；斧臂仍沿身体向下。','shield_recover_axe_ready直身收步，短斧在左肩外上斜，斧肘仍明显弯。'],
 'gap':'三图都有持斧但没有把肩、斧肘和前脚一起向空处送出的攻击释放轮廓。新增前送斜劈，不能把旧举盾低斧仅加深蹲后改名为攻击。',
 'adjacent':['shield_recover_axe_ready','shield_brace'],
 'relation':'从收盾提斧的预备关系出发，补斧臂向前下送出的释放阶段；可向举盾防线重新收回。旧两图并非已证实的前后逐帧，不承诺直接连接或闭环。',
 'mechanics':{
  'line_of_action':'面向画面左的轻三分之四保持，胸肩向左前转送，髋随之偏向前脚，头仍可见；不是只把斧贴图旋转。',
  'arms_and_grips':'延续画面左斧臂、右盾臂。斧手前送至胸下外前，肘展开但不锁死；短柄由拳斜向左下，斧头降到腰腹高度的空处，握拳后仍见短柄尾。盾收在近侧胸肋，前臂与盾背联系能解释。',
  'support_and_contacts':'画面左靴为前承重点，整底落在同一想象支撑平面，左膝屈向脚尖；右靴留后方，前掌至脚跟自然支撑形成宽基底。胸髋的前送由腿承接，不前倾到必然扑倒。武器、盾均不撑地。',
  'negative_space':'斧手和斧头在盾外左侧，斧刃不切进前腿；斧臂与身体形成明确前送空隙。脸在盾顶之上。',
  'readability_priority':'前送的肩肘链、前脚承重和向下斜切的短斧共同读成一阶段；不要求某一个像素坐标或盾脐点严格对齐。'},
 'pass':['缩小到约原图四分之一、按头躯干尺度对照时，能读出斧臂前送而非旧brace的低垂斧。','左前承重与胸肩前转相互支持；单手握短斧、另一臂连盾，不为伸远而拉长手臂或斧柄。','完整灰鬓成熟脸、蓝灰肩巾、绗缝背心、右肩铁甲、圆盾和两靴保留。'],
 'fail':['仅复制brace宽蹲和低斧，身体/斧肘未前送，核心缺口仍未补。','斧头或斧臂穿盾/腿、斧换手、无支撑的极端前倒，或短斧变长柄巨斧。'],
 'risk':['攻击尾段容易退化成已有低斧护挡，须优先检验整个前送动势。','盾遮住斧肘并不自动失败，只有肩肘腕连线无法解释才是硬错。'],
 'pose_prompt':'将此角色画成短斧前送斜劈的一个清晰关键阶段：从第三张收盾提斧预备向画面左前斜下释放，斧臂从肩向左前送出，拳在胸下外前、肘近伸但不过伸；同一短柄向左下延续，斧头在腰腹高度的左侧空处，刃与腿、盾分开。上身随斧臂转送，画面左前靴整底承重、膝自然弯，右后靴稳定形成基底。圆盾由原盾臂收在右侧胸肋，脸仍在盾上方。动作重点是肩肘前送和重量移到前脚，绝不是第二张沉身举盾低垂斧的再版。没有对手或接触目标。'
},
{
 'pose_id':'crossbow_backstep_load','label':'低姿撤步换重心','phase':'持弩移位的后脚接重阶段，不表示发射或装填',
 'observations':['母图双手前托后握，弩床斜向左下，膝轻屈。','crossbow_aim双脚展开，高平弩贴近肩胸，头低顺床瞄准。','crossbow_low_ready较直身、脚收近，弩床压向左下；并没有低姿撤离中的前后脚负重差。'],
 'gap':'已有的是高位瞄准与直立低持，缺少保持器具控制同时撤开站位的承重阶段。新增低姿后坐与前脚卸重，不使用未经证实的弦、扳机、踏环操作或装填细节来制造差异。',
 'adjacent':['crossbow_low_ready','crossbow_aim'],
 'relation':'以low_ready为最近持握邻帧，提出撤步接重后重新找瞄准站位的动作空隙；aim只用于对照识别。此图不暗示此前射击或此后完成装填。',
 'mechanics':{
  'line_of_action':'仍朝左三分之四，髋向画面右后方下沉，躯干小幅前倾抵消后坐，头不贴弩床；高低与后移均来自关节。',
  'arms_and_grips':'原前手托弩床下、后手握床后段，双手不离开原功能握区。双肘屈收将弩靠近下胸腹外侧，弩前仍向左下，与膝留空间。整具弩刚体随手臂移动。',
  'support_and_contacts':'画面右后靴整底为主要承重点，膝明显屈且髋在其上方附近；左前靴卸重、跟抬而前掌轻触同一想象平面。脚不交叉、不跪地；前脚仍有接触不被画成双脚悬空跳步。',
  'crossbow_state_boundary':'仅沿low_ready选稿可见弩的横弓、纵床、单弦与踏环拓扑；无拉弦、脚踩踏环、取矢、放矢、松弦或发射箭。单弦透视分段不算第二弦，遮挡处不发明机构。',
  'negative_space':'弩前踏环/弓翼与前膝、靴不相碰，脸与弩床分开；手掌不跨到弦上。',
  'readability_priority':'首看应是低姿撤步接重，弩依旧完整可控；不能只画相同直立low_ready而改眼神。'},
 'pass':['髋后下沉、右后膝承重、左前跟抬三者协同，明显不同于旧aim宽站或旧low_ready收脚直身。','握点分开且仍在床上，弩种类体量及单弦关系保留，不新增装填推断。','披帽、皮胸护、灰短衣、右腰单矢袋、绑腿双靴仍一致。'],
 'fail':['把旧低持弩原姿缩小、平移或只弯一点膝，撤步关系无法辨读。','为了接重画交叉双腿、弩翼穿膝或脚踏踏环；前托后握变摸弦，或弦态/矢状态被擅改。'],
 'risk':['浅角度撤步容易只像普通蹲姿，必须从髋、两膝、脚跟和持弩回收一起判断。','该阶段可读性比机械装填更可靠，但不能据此声称原版已有此闪避技能。'],
 'pose_prompt':'新增一个低姿撤步接重阶段，不画发射或装填。保持角色朝画面左三分之四，髋明确向画面右后下沉；右后靴整底承重，右膝明显屈，左前靴卸重且脚跟抬起、前掌轻触想象支撑平面。身体为保持平衡略向前收，头抬离弩床。两手始终在原来的前托床下与后握床段，双肘收弯，把同一具横弩收近胸腹外侧，前端仍左下斜并与膝留开。保留第二张瞄准图和第三张低持图中同一弩的双轴、单弦、踏环及体量；机构维持原可见关系，不增加箭，不拉弦、不踩踏环、不抓矢袋。新意由后坐接重、前脚跟抬与身体低姿共同产生，不能成为直立low_ready换表情。'
},
{
 'pose_id':'axe_high_load','label':'双手斧高位蓄劈','phase':'重斧举高、后脚接重的释放前蓄势',
 'observations':['新idle_style_v2为粗簇短胸腹、肉脸肉腿，双手低横握长斧。','axe_set的斧头在左肩外，最高接近盔顶，近头端手约胸肩高，另一手在腰附近。','axe_recover斧头在左下足旁，柄近水平，双手低收，躯体前压。'],
 'gap':'现有set还只是肩外准备，recover已回到低收；没有双肘举高、长斧重心抬到盔顶以上而身体向后脚蓄住的强蓄势轮廓。新增高位承载，不把已有肩外set仅旋转几度。',
 'adjacent':['axe_set','axe_recover'],
 'relation':'最近邻帧是axe_set，补更高的蓄劈准备；axe_recover作为未来下行后可能回收状态的对照，不声称中间挥落已被绘出。',
 'mechanics':{
  'line_of_action':'保留亡卒塌肩和紧凑胸腹，胸廓微转、髋回到后脚上方；抬臂不变成活人士兵挺胸军姿或拉长腰身。',
  'arms_and_grips':'沿原图画面左侧近头端手、右侧近柄尾手的分工；双手均提高，近头端手至额侧上方，后手至上胸侧，双肘共同举起支撑。长柄从左上斧头连到右下柄尾，双拳分开且腕向可解释；允许自然握距小调，不颠倒承载顺序。',
  'support_and_contacts':'画面右后足整底承载更多，右膝屈、髋在两足基底之内；左前残靴/露趾足仍接触平面做平衡。两足分开，重斧不以头盔或肩甲硬托，不能单手悬举。',
  'prop_path':'整个斧头高于盔顶且偏左外空，宽刃、长柄和尾箍仍同一尺寸级别；柄不穿脸，斧头不靠裁切显示高度。',
  'readability_priority':'高斧、大幅双肘上提、后脚接重形成统一的蓄势；斧高于盔是易读证据，不以一个像素高度差替代动作。'},
 'pass':['与axe_set并排能明确看见双手上提和重斧过盔高位，而非沿旧肩外姿微调。','两手一柄、腕肘肩承载闭合，后脚支撑成立，完整斧刃与尾箍留边。','保留idle_style_v2粗簇紧凑肉体和缺损甲，绝不回退旧idle_v1的长腹密纹。'],
 'fail':['一手离柄、柄折断/穿头、斧头缩成007短斧，或两臂不可能承载高位。','只提高斧头贴图、手臂/重心基本照抄axe_set，或者以裁切掩盖斧头与柄尾。'],
 'risk':['高举巨斧的画幅需求较大，要扩画幅留完整性，不压短斧柄。','头端手和尾端手的拓扑应保留，但允许正常透视遮挡及自然握距，不立超出可见证据的单点刚性规则。'],
 'pose_prompt':'基于新的idle_style_v2锈甲斧亡卒，画一个双手斧高位蓄劈关键阶段。两只手连同双肘都从第二张肩外axe_set进一步抬起：原靠斧头的画面左侧手提高至额侧上方，原靠柄尾的画面右侧手提高至上胸侧，双手依旧分开握同一连续长柄。宽重斧头完整处于盔顶上方的画面左外空，柄向右下延续至清楚尾箍，斧与脸留空。胸廓微转但维持塌重亡卒体态，髋向右后足接重，右后膝屈、双足仍稳触想象平面。真实变化是高位双臂承载和后脚蓄重，不能只把原axe_set的斧贴图抬高。保留新锚粗簇短胸腹、灰蜡肉脸和肉腿、缺盔裂甲、左叠肩甲与右破赭布，不能变纯骨骷髅或修长写实士兵。不要向任何对象挥砍；不添加新伤或飞溅。'
},
{
 'pose_id':'spectral_sword_retract','label':'探剑后屈肘回收','phase':'探出之后的收剑与悬浮后撤阶段',
 'observations':['母图剑低斜左下、盾在右胸侧，下面两条短钝幽尾分离。','选中guard首稿仍是低剑，盾较贴胸前，变化保守。','选中probe首稿是左臂外伸与近水平探剑，盾收近侧；不是后生成的未选revision。'],
 'gap':'旧两姿都没有把探出的剑臂折回胸肋、剑尖抬到左上外空的回收轮廓。新增回收配合胸廓后倾和短尾轻微反向滞留，不能仅把probe整体向右平移。',
 'adjacent':['spectral_sword_probe','spectral_shield_guard'],
 'relation':'以已选probe首稿为最近动作邻帧；收剑后可回到guard的低剑防线，但新图与旧两图仍只是分离的关键阶段概念。',
 'mechanics':{
  'line_of_action':'脸仍朝左三分之四；胸廓从前探转为小幅向右后收，肩与腰关系改变而不是整图位移。',
  'arms_and_grips':'原画面左剑臂肘折回身旁，剑拳回到左侧胸肋，短直剑由拳指向左上外空，与脸留缝；原右盾臂保持盾背连接，长盾仍护近侧胸腹。剑柄、拳、护手、剑身链连续。',
  'support_and_contacts':'无脚、无地面接触。两条短钝分叉尾由同一个腰下幽体相连，尾端可轻向左滞留而胸肩向右收；保持选中母图的短尾级别及中间透空，不画长飘带、第三尾或实体落地腿。',
  'negative_space':'回收剑仍在身体左外侧，斜上剑身不得穿过脸/盔/盾；盾的外上缺口和尖底保持可辨。',
  'readability_priority':'折肘、举剑回收、胸廓后收共同读阶段；尾的轻偏只辅助，不以加光雾或大幅尾旋转制造动作。'},
 'pass':['可见probe伸肘到新稿折肘的明确功能变化，剑从平探转为胸侧斜上回收。','冷色成熟面腔、破盔肩甲、同一缺口长盾及短直剑一致；两短尾自然接腰且无落地足。','真实alpha浅深底合成可读；透明像素的隐藏RGB不作为可见光晕证据。'],
 'fail':['仍画低剑guard，或只将probe整体平移，回收核心不存在。','回收剑穿脸/盾、变长剑或掉握；增脚或第三尾、两尾变扫地长袍。'],
 'risk':['剑抬回胸侧可能和脸/盾挤在一起，要保留有视觉意义的空隙，不强求所有边完全分离。','010历史多余revision未选，不能因文件更新时间新就替代正选首稿；alpha=0隐藏RGB不得再触发返工。'],
 'pose_prompt':'只沿母图和已选的两张首稿动作制作一个探剑后屈肘回收阶段，不参考未选revision。角色仍朝左三分之四，原画面左持剑肘明显折回身旁，剑拳从第三张水平探出回到左侧胸肋；同一短直剑斜向左上外空，护手与握拳连续、剑不穿脸。胸肩稍向右后收，原右侧缺口长盾仍贴近胸腹护身并由盾后臂支撑。腰下只保留两条短钝分叉幽尾，尾端可略向左滞留，与后收胸廓形成小幅方向差；两尾之间透明，绝无腿靴或地面支撑。新姿必须由折肘收剑和胸廓后收读出，不能重画第二张低剑guard，也不能平移第三张probe。保留冷蓝灰同色幽体，无光束、光墙、烟云、粒子或拖影。'
},
{
 'pose_id':'throat_forward_release','label':'喉胸前送释放','phase':'蓄势后的身体前送关键阶段，口前空白无投射物',
 'observations':['母图喉胸形成竖长椭圆，头抬、短臂垂腹侧。','throat_gather胸喉更高、双臂屈收腹侧，双足展开。','throat_lower屈膝很低但头仍抬，上臂下放外展；喉胸仍多为竖直大体块。'],
 'gap':'已有一高一低两个储备姿，但没有把喉胸整体向左前送、使头与前肩越向前方而腿承接的释放方向。新增整体前送，不依赖张嘴/眼神，也不画喷吐效果。',
 'adjacent':['throat_gather','throat_lower'],
 'relation':'gather为最近蓄势邻帧，新图拟表达其后向空处释放的身体阶段；lower为低身回稳的对照。不是在补验已发生的喷吐、命中或技能机制。',
 'mechanics':{
  'line_of_action':'从后收竖立改为髋、胸、头共同指向左前的斜线；头下颌略收且跟随喉胸前送，不能保持旧抬头蹲姿。脖颈不单独拉成长管。',
  'arms_and_grips':'双短厚臂仍连接同侧肩；一臂略后收、一臂外下平衡，手不着地、不变长爪，不让双臂覆盖喉胸主轮廓。',
  'support_and_contacts':'画面左前爪足整掌着地承担前送重心，左膝弯；右后足前掌仍接触、跟可轻卸重。髋不冲出两足可支持范围，胸大体块由腿接住，无跪地或四足化。',
  'organ_shape':'喉胸仍为单个连续的大椭圆体，随躯干前倾和小幅回缩改变方向，不能夸张瘪袋或充气增倍。原小头完整、短尖耳与原短牙保留；嘴可自然小张但口内简单无新器官。',
  'negative_space':'口前完全空白，不画液体、血、气雾、射线、音波、目标或受害者；前手不遮头脸。',
  'readability_priority':'即使遮住嘴部，新稿也应靠头胸前送、单侧接重与双短臂平衡看出阶段；表情不是主要差异。'},
 'pass':['与旧lower相比不是同一深蹲：头胸明显前送、前腿接重，整体力线转向左前。','只有两短臂、两短腿和原喉胸体块，原非人脸与右肩破布身份保持。','口前无喷吐物，重心与接触清楚，未以怪异肌体/口器增生替代动作。'],
 'fail':['只张嘴而旧gather或lower姿势照搬；释放方向在缩小后无法读出。','头或颈拉长、喉胸倍增/崩塌、额外舌/嘴/触手、手撑地成四足，或新增血液投射。'],
 'risk':['无投射特效时释放最易与前倾蹲混淆，必须检查从支撑足到喉胸/头的整体送出。','生物体块只做有限姿态压缩，不声称真实生理或任何原版技能。'],
 'pose_prompt':'新增喉胸前送释放的一个身体关键阶段，口前必须空白，没有任何喷出物。原非人怪物从第二张抬喉蓄势向画面左前送出头与胸，整个喉胸椭圆随躯干倾向左前，头下颌略收并跟随前送，而不是第三张抬头低蹲的重复。画面左前爪足整掌接重、左膝自然屈，右后足前掌仍触想象支撑平面、脚跟可轻卸重；髋随前腿接住重量。双短厚臂一侧稍后收、另一侧外下平衡，两手均离地。单个硕大喉胸只有限回缩、不倍增也不瘪塌，头与短颈不被拉长。可轻张原口但不是靠嘴表情表现动作，原短牙和耳保留。保留灰紫褐非人皮肉、主要暗鳞状簇、原右肩与腰下破布，只有两臂两腿，不增舌、额外嘴或触手。无受害者、血液、飞沫、气雾或法术特效。'
},
{
 'pose_id':'bell_outward_swing','label':'手铃外摆端点','phase':'提铃与低收之间的外摆释放端点',
 'observations':['新idle_style_v2低帽成熟脸、粗簇短袍，铃在画面左手低垂。','bell_raise持铃肘弯、手在脸侧外方，铃悬在胸旁，铃口大体朝下。','bell_settle同手低收近腰腿、站步稍撤，另一空手在带扣附近。'],
 'gap':'已有提起与落低，但没有把持铃臂主动向外展开、铃体随手腕小倾的摆动端点。新增外展前臂与身体接重，而不是再提高/降低同一竖直持铃姿。',
 'adjacent':['bell_raise','bell_settle'],
 'relation':'以bell_raise为最近邻帧，提出向左外摆后可收向bell_settle的关键端点；没有验证声响、铃舌碰撞、帧序或连续动画。',
 'mechanics':{
  'line_of_action':'胸廓稍向持铃侧转，左前脚接重、另一脚后稳，肩线跟随外摆但头仍朝左三分之四。',
  'arms_and_grips':'原画面左手继续包握同一木柄，肩肘向外展开，手位于身体左侧、胸腹之间；肘比raise明显展开但不锁死。铃柄与手腕同向自然斜转，钟体在手的左下外侧，钟口斜下，原单铃舌可自然偏而不增殖。空手在右胸腹斜带附近，不触铃。',
  'support_and_contacts':'画面左前靴整底落地、膝微屈接住侧前重量；右后靴同样稳触平面，站距略开而非settle收步。不需要跨步夸张扭腰或双脚腾空。',
  'negative_space':'持铃手腕必须从袖口连续伸出，铃与袍、脸、膝有清楚空隙，完整木柄和钟体同一轴系，不将手铃改为链坠。',
  'readability_priority':'外展的肩肘链、斜下钟体和前脚接重一起读成外摆端点；单独改变铃口几个像素或微表情不算新动作。'},
 'pass':['与raise弯肘高提、settle低垂收铃形成第三种明确外伸姿，整个手臂与铃的轮廓在缩小后仍可读。','袖口—腕—握拳—木柄—钟肩连续，单手小铃体量不漂移；另一手保持空手。','沿idle_style_v2大头短身与成熟五官，不回退旧长身；低帽、污白左肩至右腰斜带和双靴一致。'],
 'fail':['重画高提或低收，只换眼神/铃口倾角；外摆没有肩肘与承重变化。','铃改手/脱柄/增加链条、复制第二铃或铃舌，或袖口断腕，钟体粘脸腿。'],
 'risk':['外摆容易被画成拿铃当武器前刺，应读作自然单手摆动端点，手腕不过折。','铃舌的精确碰壁时刻没有参考，不把它规定成单点接触硬门槛，也不以声波代替动作。'],
 'pose_prompt':'基于新的idle_style_v2缄声执铃者，画同一手铃向左外摆的清晰端点。原画面左持铃手始终包握同一木柄，肩肘主动向画面左外展开，肘比第二张bell_raise明显展开但不锁死，手在胸腹之间的外侧，不能仍举在脸旁。手腕自然小幅斜转，木柄与同一钟肩连续，钟体位于手的左下外空，铃口斜向下，只有原单铃舌。胸廓微随持铃侧转，左前靴整底接重、膝稍屈，右后靴稳住且站距略开；另一只空手仍在右胸腹斜带附近。动作必须靠外展肩肘、斜下铃体和脚下接重一起读成外摆端点，不是第三张低收姿或第二张高提姿的微调。保留成熟脸、低圆帽、粗簇紧凑短身、灰膝袍、左肩至右腰污白斜带和双靴。铃不碰人、不触衣腿，不画声波、残影、法阵或召唤物。'
}
]
view_times=['04:08:31','04:08:49','04:09:06','04:09:23','04:09:39','04:09:56']
items=[];checks=[];inspection=[]
common_prompt='生成一张完整单角色的原创低魔中世纪像素美术动作关键阶段概念，原生透明背景。参考1是当前唯一选中母图，用于身份、衣具、道具、身体比例和像素组织；参考2、3是当前已选的两张旧动作，用于理解阶段与避免重复，不是拼图模板。保持同一角色朝左轻三分之四，不镜像、不换手或换装备，不复制第二角色。脸、头顶、手、脚或短幽尾、所有道具末端完整留透明余量，按动作需要扩展画幅，不能靠压缩身体或缩短武器塞进画布。保持有组织的像素簇和有限色阶，不加摄影级微纹、不以模糊或滤镜掩盖问题。'
common_end='这是一张新的可读关键阶段，不是连续三帧循环、游戏内动画或装备绑定证明。单独重画真实姿态，不将参考整体平移、旋转、缩放，也不以微表情作为主要变化。没有环境、地面投影、文字、边框、受害者、碰撞命中、血液飞溅、魔法粒子、速度线或拖影。衣褶和像素小差异允许自然发生；优先保证整体动作、支撑、肢体连接和道具握持可读，不追求逐像素复制。'
for c,p,t in zip(old['characters'],plans,view_times):
 slug=c['slug'];anchor=R/c['anchor']['path'];dirs=[anchor.parent]+[B/slug/'action_v1'/q['pose_id'] for q in c['poses']]
 refs=[];meta=[]
 for i,dd in enumerate(dirs):
  st=J(dd/'FINAL_STATUS.json');qa=J(dd/'QA_INDEPENDENT.json');man=J(dd/'manifest.json')
  if i==0:ip=anchor;expected=c['anchor']['sha256'];pose='selected_static'
  else:
   pose=c['poses'][i-1]['pose_id'];ip=dd/(slug+'_'+pose+'_transparent.png');expected=qa['selected_sha256']
  assert H(ip)==expected
  frame=record(ip,'selected_mother' if i==0 else 'selected_existing_action',{'actually_viewed':True,'viewed_utc':'2026-10-14T'+t+'Z','scope':'Actual individual selected transparent PNG opened with view_image during this planning task; entire subject inspected.'})
  frame['pose_id']=pose;frame['observation']=p['observations'][i]
  frame['selection_authority']=record(dd/'FINAL_STATUS.json','final_selection_authority')
  frame['candidate_manifest']=record(dd/'manifest.json','frozen_or_final_candidate_manifest')
  frame['independent_review']=record(dd/'QA_INDEPENDENT.json','historical_independent_review')
  frame['historical_independent_result']=qa['result']
  for name in ['final_manifest.json','source_snapshot.json','sources.json','alpha_audit.json','alpha_QA.json']:
   if (dd/name).exists():record(dd/name,'historical_metadata')
  for prompt in dd.glob('prompt*.txt'):record(prompt,'historical_prompt_not_for_execution')
  for g in dd.glob('*call*.json'):record(g,'historical_generation_evidence')
  if (dd/'generation_record.json').exists():record(dd/'generation_record.json','historical_generation_evidence')
  selected_in_status=st.get('selected_sha256') or st.get('candidate_sha256') or (st.get('selected_image') or (st.get('selected') if isinstance(st.get('selected'),dict) else {})).get('sha256')
  assert selected_in_status==H(ip)
  stat_m=st.get('manifest_sha256') or st.get('frozen_manifest_sha256')
  if stat_m:assert stat_m==H(dd/'manifest.json')
  qa_key=st.get('independent_qa_sha256') or st.get('independent_QA_sha256') or (st.get('independent_review') or {}).get('sha256')
  if qa_key:assert qa_key==H(dd/'QA_INDEPENDENT.json')
  checks.append({'source':ip.relative_to(R).as_posix(),'actual_sha256':H(ip),'selected_status_sha_match':True,'selected_qa_sha_match':expected==H(ip),'status_manifest_sha_match':True if stat_m else 'not_declared_by_status','status_review_sha_match':True if qa_key else 'not_declared_by_status','historical_manifest_status':man.get('status'),'final_status':st.get('status'),'note':'FINAL_STATUS is selection authority. Earlier candidate manifest/QA snapshots stay historical; their pending labels or earlier manifest hash do not override later freeze.'})
  refs.append(frame);inspection.append({'path':frame['source_path'],'sha256':frame['sha256'],'pose_id':pose,'view':frame['current_planner_visual_inspection'],'observation':frame['observation']})
 identity=c['identity_lock'];canon=next(x for x in production['concepts'] if x['concept_id']==c['concept_id'])
 prompt='\n\n'.join([common_prompt,'角色身份与装备保持：'+' '.join(identity.values()),p['pose_prompt'],common_end])
 promptfile=D/'planned_prompts'/f"{c['concept_id'][-3:]}_{p['pose_id']}_prompt_v1_NOT_EXECUTED.txt";promptfile.parent.mkdir(exist_ok=True);promptfile.write_text(prompt+'\n')
 output_dir=B/slug/'action_continuation_v1'/p['pose_id']
 items.append({'concept_id':c['concept_id'],'slug':slug,'working_name':c['working_name'],'pose_id':p['pose_id'],'label':p['label'],'status':'planned_not_executed_pending_independent_review','phase':p['phase'],'generation_started':False,'generation_calls':0,'first_draft_budget':1,'hard_error_revision_budget':1,'selected':False,'source_images':refs,'identity_lock':identity,'gap_reason':p['gap'],'conceptual_neighbors':{'nearest_old_pose':p['adjacent'][0],'comparison_or_possible_settle_pose':p['adjacent'][1],'relationship':p['relation'],'contiguous_frames_verified':False},'pose_mechanics':p['mechanics'],'pass_conditions':p['pass'],'hard_fail_conditions':p['fail'],'risk_notes':p['risk'],'canon_exclusions':canon['must_not_infer_or_draw'],'planned_prompt':{'status':'not_executed','text':prompt,'file':promptfile.relative_to(R).as_posix(),'sha256':H(promptfile),'sha256_scope':'UTF-8 prompt file including final newline'},'planned_tool_call':{'tool':'image_gen.imagegen','executed':False,'arguments':{'prompt':prompt,'referenced_image_paths':[str(R/x['snapshot_path']) for x in refs],'transparent_background':True},'reference_order':['selected_mother',c['poses'][0]['pose_id'],c['poses'][1]['pose_id']],'must_reverify_snapshot_sha_and_view_each_reference_before_execution':True},'planned_output_directory':output_dir.relative_to(R).as_posix(),'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False})
manifest={'schema_version':1,'created_utc':now,'scope':'Second-six continuation planning source snapshots. Copies only; no old sources changed. No original commercial game artwork copied.','files':list(source_files.values()),'source_count':len(source_files),'selected_images_count':18,'style_images_count':2,'reference_selection_notes':['009/012 only idle_style_v2; prior idle_v1 images not inputs.','010 static is the selected short-tail transparent file in idle_v1 (derived from static v2); both action inputs are selected v1 first drafts, not the unused revisions.','008 aim input is its selected transparent image derived from v2 framing correction.','Historical briefs describe then-unstarted statuses; selection is resolved through current FINAL_STATUS plus selected image SHA and independent QA.']}
W(D/'source_manifest.json',manifest);W(D/'existing_selection_validation.json',checks);W(D/'actual_view_log.json',inspection)
brief={'schema_version':1,'title':'第二组六敌人各一动作补缺规划 v1','created_utc':now,'snapshot_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'status':'planned_not_executed_pending_independent_review','scope':{'concept_ids':[x['concept_id'] for x in items],'new_keypose_concepts_planned':6,'new_images_generated':0,'animation_frames_produced':0,'changes':'Only this new brief and its new source-snapshot directory. No old brief, image, QA, selected status, story, runtime, Git commit or upload changed.'},'evidence_policy':{'current_task_actual_view':'All six selected mothers plus twelve selected old action images individually opened and inspected with view_image; Sela G and Mia v2 also individually viewed. See actual_view_log.json.','original_game_boundary':'No original game full animation was newly viewed; public-source facts are inherited, attributed historical notes only, not current-version or timing proof. No new runtime claims.','source_authority':['Latest selected FINAL_STATUS and matching image SHA','Historical independent review and candidate manifest, interpreted with their recorded freeze scope','action_pilot_second_six_brief_v2 and style supersession for 009/012','Actual visible selected images for current posture and prop continuity'],'visual_judgment':'Judge overall action, support and continuous limb/prop topology first. Use whole-subject and head/torso-normalized comparison, not whole-canvas box or weapon-inclusive scale. A numerical anchor/grip point, small cloth change or tiny clapper position is not an automatic failure. Requirements below each have a visible function; no inherited first-batch single-point hard gate.','alpha_rule':'Inspect actual RGBA composites on light and dark. Hidden RGB at alpha=0 is invisible and cannot prove a visible glow. Do not threshold away genuine spectral contours or re-generate because alpha>0 bbox alone hits an edge. Body/prop crop must be visually established.','claims_limits':['Key-stage concepts only; adding this one to two old poses does not establish a continuous three-frame cycle.','Pivot/anchor coordinates, timings, sprite grid, collision, layered equipment and engine integration are unverified.','Working enemy names are reversible original art labels, not confirmed canon faction membership or identified deceased persons.']},'execution_limits':{'generation_authorized_now':False,'generation_started':False,'start_condition':'Parent must arrange independent planning review and explicitly release generation afterward; this planning task does not generate.','first_drafts_per_item':1,'hard_error_revisions_per_item_max':1,'revision_scope':'Only documented identity, anatomy, topology, support/pose-core readability, material prop mismatch, crop or visible transparency hard error. One optional revision after an exact cause is identified; cosmetic preference is not a reason.','after_budget':'If still failing, mark needs_review and stop that item; do not silently count it selected or launch another candidate.','safety_block':'If generation or another action is safety-blocked, stop and report exact action/target/reason. Do not paraphrase prompts, change tools or alter route to evade that block.','not_performed':['image generation','old source changes','Git commit or upload','runtime editing or deployment'],'expected_future_review':'Author and independent actual-view review of mother, both old poses, new full pose and reduced light/dark composites before selection. Compare core action first, then grips/support and technical integrity.'},'source_manifest':{'path':(D/'source_manifest.json').relative_to(R).as_posix(),'sha256':H(D/'source_manifest.json')},'existing_selection_validation':{'path':(D/'existing_selection_validation.json').relative_to(R).as_posix(),'sha256':H(D/'existing_selection_validation.json'),'selected_image_checks_passed':18},'rules_and_history_read':base_records,'style_comparisons':style_records,'items':items,'remaining_after_this_plan':['Independent planning review and parent generation start are pending.','All six first drafts remain unexecuted; no output image, selection or delivery claim is made.','Any future animation continuity, anchors, equipment compatibility or runtime acceptance requires separate actual evidence.']}
W(OUT,brief)
D.joinpath('README.md').write_text('# 第二组动作补缺规划来源\n\n本目录仅封存规划输入与六条未执行提示词。source_manifest.json 保存每份来源原路径、快照路径、字节数与真实 SHA-256。18张正选图已逐张实际查看，记录见 actual_view_log.json。009/012用idle_style_v2，010动作只用正选首稿，008瞄准用正选修订透明图。\n\n不修改旧源，不生图、不Git上传。新增阶段不等于连续循环、锚点验收或runtime通过。planned_prompts是完整拟用文本，均为未执行；planned_tool_call只是供审阅的参数记录。\n')
shutil.copy2('/tmp/plan_second_six.py',D/'build_planning_record.py')
assert len(items)==6 and all(x['generation_calls']==0 for x in items)
assert all(H(R/x['source_path'])==x['sha256']==H(R/x['snapshot_path']) for x in source_files.values())
val={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'pass_planning_structure_and_source_integrity_only','brief_path':OUT.relative_to(R).as_posix(),'brief_sha256':H(OUT),'items':6,'selected_sources_sha_checked':18,'individual_selected_images_actually_viewed':18,'all_source_copies_match':True,'source_files_originals_unchanged_after_copy':True,'source_file_count':len(source_files),'prompt_files_nonempty_and_equal_to_planned_tool_text':all((R/x['planned_prompt']['file']).read_text()==x['planned_prompt']['text']+'\n' for x in items),'generation_calls_this_task':0,'old_files_written':0,'runtimeVerified':False,'independent_planning_review':'pending','notes':'Structural checks do not substitute for independent planning or generated-image review.'}
W(D/'planning_validation.json',val)
print(json.dumps(val,ensure_ascii=False,indent=2))
