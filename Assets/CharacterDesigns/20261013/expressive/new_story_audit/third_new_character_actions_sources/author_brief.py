import json, hashlib, shutil
from pathlib import Path
from datetime import datetime, timezone
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
O=A/'third_new_character_actions_sources'
B=R/'Assets/CharacterDesigns/20261013/expressive/new_story'
sha=lambda b:hashlib.sha256(b).hexdigest()
rel=lambda p:str(p.relative_to(R))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
src=[]
def snap(i,p,role):
 p=R/p if isinstance(p,str) else p
 b=p.read_bytes(); dest=O/'files'/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 assert sha(dest.read_bytes())==sha(b)
 x={'source_id':i,'path':rel(p),'sha256':sha(b),'bytes':len(b),'role':role,'snapshot_path':rel(dest)};src.append(x);return x
for i,p,role in [
 ('root_agents','AGENTS.md','项目规则只读快照'),('design_agents','design/AGENTS.md','设计规则只读快照；本轮不改剧情'),
 ('pixel_asset_skill','Assets/CharacterDesigns/20261013/expressive/reference/pixel-asset-master/SKILL.md','归档pixel asset工作流；当前阶段只做计划'),
 ('style_direction','Assets/CharacterDesigns/20261013/expressive/STYLE_DIRECTION.md','当前成年紧凑粗像素方向'),
 ('roster44',rel(A/'new_characters_44.json'),'44人稳定ID与当前卡来源；历史production status不作完成数'),
 ('mother_qa',rel(A/'independent_visual_qa_second_four_20261013.json'),'四人已审母图raw/透明SHA绑定'),
 ('first_actions_brief',rel(A/'first_new_character_actions_brief.json'),'第一批动作语义去重与结构参照'),
 ('second_actions_brief',rel(A/'second_new_character_actions_brief.json'),'第二批动作语义去重与结构参照'),
 ('action_coverage','Assets/CharacterActions/20261013/ACTION_COVERAGE.md','历史动作、研究与非连续边界'),
 ('master_supplements','Assets/CharacterActions/20261013/MASTER_SUPPLEMENT_INDEX.md','旧角色已交动作语义去重'),
 ('action_delivery_index','Assets/CharacterActions/20261013/new_story/ACTION_DELIVERY_INDEX.md','当前8人14张已交；图里/锉珥A1缺项不自动续画'),
 ('care02','design/06_支线/城市支线/台本_CS-ASH-02_陪护者也会累.md','读取当前枯恩普通护理/帮助/自主性边界'),
 ('care03','design/06_支线/城市支线/台本_CS-ASH-03_冷苇的空碗.md','读取当前苏奈记录许可与普通物资分离边界'),
 ('home01','design/06_支线/城市支线/台本_CS-ASH-01_安息村的旧钥匙.md','读取当前缇安共同居住权/不以钥换物边界'),
 ('guide01','design/06_支线/城市支线/台本_CS-HIG-01_回风驿的停牌.md','读取当前蕾因客约责任/停牌/退款边界'),
 ('old_doro_prompt','Assets/CharacterActions/20261013/doro/empty_bowl_present_v1/prompts/D1.txt','旧双手向外递空碗动作去重'),
 ('old_mia_prompt','Assets/CharacterActions/20261013/mia/blanket_adjust_v1/prompts/adjust.txt','旧站立理独立叠毯动作去重'),
 ('old_nisha_prompt','Assets/CharacterActions/20261013/nisha/ledger_page_check_v1/prompts/N2.txt','旧翻簿动作去重')]:snap(i,p,role)
roster=json.loads((A/'new_characters_44.json').read_text())['characters'];qa=json.loads((A/'independent_visual_qa_second_four_20261013.json').read_text())['results']
byid={c['canonical_id']:c for c in roster};byqa={c['slug']:c for c in qa}
common='以所附本人的已审透明全身母图为唯一人物身份、脸型、年龄、比例、衣装、配色及已有器物造型锚，用内置imagegen重新绘制一张独立非战斗全身动作关键姿态。保留母图成熟大头、短自然颈、紧凑成年身体与有组织的粗像素簇，不幼化、不拉成长身、不统一四人的脸。不镜像；下文左右均为人物自身解剖侧，并附画面侧。必须有真实手臂、身体或原道具接触变化，不能只改表情、低头或平移母图。完整头发、双手、双脚和全部保留器物，四周留透明边距。单人、单个瞬间、纯alpha透明背景，无背景、地板、投影、光晕、文字、数字、图标、边框、UI、第二个人、箭头、残影或多格。所有原物件只保一件，取出后原位置不再复制同件。不用脚本绘制人体、旋转肢体、插值、拉伸、拼接或强量化修错。没有动作结果、治疗、康复、付款、授权、所有权转移、任务结案或新剧情事实。'
transition='起止只是文字供以后制作参考；本轮只计划pose描述的一张独立静态关键姿态，未制作起止帧、过渡或连续循环。A1/A2不构成默认先后顺序。'
char_data={
'kuen':{
 'id':'ASH-NPC-KUEN','name':'枯恩','identity':'三十多岁成年男性、清醒能自主表达的患者；深棕短乱发、少量胡茬、烟灰蓝布衫、厚暖灰褐织披肩、深灰褐裤、松袜口与软便鞋。',
 'observation':'母图右手（画面左）摊掌说明，左手（画面右）有旧青并落左膝。低木椅有靠背，布卷位于背部并在画面右露卷端；单独矮木凳、温水杯及无字布条在人物右侧（画面左）。E1双手低放，E2右掌举起拒绝，均未操作披肩或侧转靠椅。',
 'side':'旧青固定人物左手背（画面右），不得改侧或新增病灶。木椅、背部布卷、双脚原落点不挪；右侧（画面左）小凳、杯、布条原位不动，杯始终未触碰、未端起。',
 'guards':['成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。','不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。','原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。'],
 'risks':['A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。','A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。'],
 'plans':[
  {'key':'kuen_A1_draw_shawl_edges_in','title':'坐稳合拢胸前披肩','evidence':[('kuen_card','衣着与磨损','病号布衫外披厚披肩，是奥娅织的'),('kuen_card','体貌','坐时背垫着布卷')],
   'start':'臀部坐实原椅，背仍靠布卷；两手从说明/落膝位置移向自己披肩两前缘，杯与凳不动。',
   'pose':'两肘收近身体，右手（画面左）捏住同一披肩右前缘在下胸处向中线轻拉；左手（画面右）托住并捏稳左前缘，位置略低于右手。两条仍连着肩背的前缘在胸腹中央形成清楚的小重叠与受牵折褶，两个手腕与指组各有真实布料接点。肩胸仍朝母图方向，头稍低看自己的手；臀部全落原椅面、背后布卷不滑出，双脚原落地。',
   'end':'放松捏握，让同一披肩仍披在肩背并垂回膝前；不增脱衣、起身、取水或照护步骤。',
   'contact':['两手各捏同一披肩一条前缘，布料从两肩连续到接点，不浮空、不互穿','双肘有弯曲与袖口相接，左手背旧青不移到右手','臀部在椅面、后背布卷与双脚构成原坐姿支撑，椅凳杯布条仍全可见'],
   'props':['同一披肩仍穿披于身上，只合拢前缘；不新增独立毯子','椅、布卷、小凳、杯水、布条保持母图位置和数量'],
   'diff':'相对母图及E1/E2，两手均转为捏衣接触，披肩前缘重叠可读；与Mia站立抚平独立叠毯不同，也不是Osin袖口或Vasen围裙整理。','risk':'medium'},
  {'key':'kuen_A2_seated_turn_with_seat_contact','title':'坐稳轻侧转并搭椅沿','evidence':[('kuen_card','举止','喝水要人扶，翻身不用'),('kuen_card','体貌','坐时背垫着布卷'),('care02','CS-ASH-02-S1-needs','这个时段帮我起身和准备普通水。')],
   'start':'仍在原椅上坐稳，双脚和臀部不移动；右手准备落右大腿，左手准备轻搭左侧椅面边缘。',
   'pose':'保持原臀部落点和双脚地面接触，肩胸小幅向人物左侧（画面右、远离水杯）转约十五至二十度，头跟随看向左前方，不能只转头。右掌（画面左）实贴自己的右大腿膝上；左掌（画面右）从左膝移到左髋旁原木椅座面的外缘轻搭，手指沿座面边向下自然弯，左肘仍弯曲而不锁直推撑。肩线因侧转可读地改变，但臀部不抬、躯干不前冲，后腰仍与原布卷保持支撑接触，布卷不抽出也不移位。衣摆随小幅转体自然跟随。',
   'end':'肩胸可回母图朝向、左手可回左大腿；这只是文字，不补转回帧，不表示可以自行起立。',
   'contact':['臀部整个承重区仍贴椅面，不露离座空隙，双脚完全留在原落点','右掌贴右大腿，左掌接原左侧椅座外缘；不造扶手、不抓椅背、不锁肘撑起','后腰与布卷接触未断，重心留在椅座支撑区；椅凳腿和杯不挪动'],
   'props':['厚披肩仍覆肩背、前缘自然落膝，不新增动作道具','杯、凳、布条不触碰；左手旧青仍只在原侧'],
   'diff':'上身真正侧转，加左手与椅座的新接点；区别本人E1落膝/E2拒绝抬掌及Nara坐姿对话、训练样板起坐/地坐/侧卧。','risk':'high_seated_support'}]},
'sune':{
 'id':'ASH-NPC-SUNE','name':'苏奈','identity':'二十多岁成年女性记录员；灰棕低短辫、窄长成年脸、退色暗李紫罩衫、米麻系绳袖、深褐腰带和工作鞋。',
 'observation':'母图左手（画面右）抱竖向两空栏木板，右手（画面左）摊掌；两支短炭笔同在右前腰笔插（画面左）。E1右手垂下、E2右手停腹前，均未取笔或将木板转向。',
 'side':'原木记录板由人物左手（画面右）持，双炭笔笔插位于人物右前腰（画面左）。A1只右手操作原两笔之一；A2两笔都留原笔插，双手转同一木板。',
 'guards':['手里有笔不等于获许可：笔尖不触木板、纸或人体，不画书写/数据/签名；普通物资与观察资格不捆绑。','A1/A2只整理自有器物，不表示开始或停止本批、删改旧记录、得到谅解或得到患者许可。','保持原两空栏/简单分隔线；无可读姓名、数字、病情、普通/观察字样或新栏目。'],
 'risks':['两笔数量须始终恰好2；A1一笔半入插、一笔已收；不能在笔插再留两支并加手中第三支。','A2板背母图未见，只允许同色朴素木板背的可逆推断，不加背夹、夹纸器、扣、图案或新页。'],
 'plans':[
  {'key':'sune_A1_reseat_charcoal_in_slot','title':'把一支炭笔收回原笔插','evidence':[('sune_card','衣着与磨损','口袋缝着笔插'),('sune_card','随身物','记录板与两支炭笔'),('sune_card','举止','问数之前先问许可')],
   'start':'左手按母图贴身抱木板；右手仅为整理而从原笔插轻提一支炭笔，另一支留插，未书写。',
   'pose':'右肘收回腰边，右拇指与食指明确捏住一支原短炭笔上端，将它竖直向下重新插回人物右前腰的原笔插，停在半支入插、指尖仍接触笔身的瞬间；另一支原炭笔已在旁边完整收妥，两支数量可辨。左臂继续贴身抱住竖直两空栏木板，板不向外展示，笔尖与板至少有一掌宽间隔。头略低看笔插接点，双脚原位站稳。',
   'end':'松开右指后两支炭笔都可回笔插；未画松手帧，不表示曾记录任何人的数据。',
   'contact':['右拇指/食指接一支笔上段，笔下段真实进入原插口而非刺进罩衫','另一支笔留插，总数2；不把笔画成羽毛笔、现代笔帽或长刀','左掌与前臂支撑木板下/侧缘，双足承重居中，不增加桌面'],
   'props':['单木板两栏仍为空，除分隔线无任何书写','原右侧笔插与两支笔保持形状、侧别；不挪到左腰'],
   'diff':'本人E2只有空手停腰，本姿手与炭笔/插口有清楚操作接点和一进一留的物件状态；不同于旧翻簿、签字或摊掌。','risk':'medium_high_small_prop'},
  {'key':'sune_A2_turn_board_inward_carry','title':'双手转板横收在腹前','evidence':[('sune_card','随身物','记录板与两支炭笔'),('care03','CS-ASH-03-S3-scope','未准的空着，不能拿旧表复制本人一句愿。')],
   'start':'两支炭笔全在原右前腰笔插；左手抱竖板，右手收回去接木板的另一短边。',
   'pose':'双手真实握住同一木记录板左右两端，把原竖板转成横向，贴在自己下腹前；板长边近水平，原有两栏正面朝自己且略朝上，外侧仅见同色朴素木背与上缘极窄空白正面。左掌（画面右）托住右侧短边下缘，右掌（画面左）握左侧短边，双肘自然低垂略向外，板与身体间留可读的小间隙，不能像没有手的悬空板。头看向板的上缘，肩部自然跟随，双脚稳站。',
   'end':'仍以双手自行持板，之后可回竖向收身；未作交板、关账、删记录或收工结案。',
   'contact':['两手分置同一刚性木板两端，下缘受支撑，手腕不反折','板只旋转方向而不折叠、不变成书本/卷纸/两板；尺寸厚度沿母图','双笔仍各一支在右前腰原插口，不能消失或出现在手里'],
   'props':['保留同一朴素单木板和两支短炭笔，无新页、夹具、袋或桌','板背未审造型只按同色平整木面作最小可逆推断；不补可读文字'],
   'diff':'本人母图/表情都是单手竖抱；本姿双臂变位、板由竖转横且正面向内。与Anni/Nisha翻簿及Gura折单不同，不加纸页工序。','risk':'medium'}]},
 'tian':{
 'id':'ASH-NPC-TIAN','name':'缇安','identity':'三十多岁成年女性、妮蔻的姐姐及另一合法共住者；暖棕后束发、窄肩、缺觉眼影、陶红厚布衫、灰麻旧围裙、深茶褐长裙和实用鞋。',
 'observation':'母图及E1/E2均右手（画面左）在围裙袋口抓短钥绳，单小铁钥垂于袋前；左手（画面右）托同一备用空碗靠腹。两表情没有改变道具操作。',
 'side':'围裙袋与原钥绳/小钥匙在人物右侧（画面左）；空碗由人物左手（画面右）持。两姿都不交换持物手，不换钥匙侧别。',
 'guards':['只操作母图这枚原钥匙，不指称为妮蔻的钥匙或拿走别人旧权；不出现收件人、门锁、交钥或换物。','空碗始终自己拿着，无食物/水/蒸汽/药效；不表示递碗已获接收、长期照护、住房或共住协议成立。','钥绳只做日常收整，不能被图示当成同意、放弃旧权、敲定返家或扣留条件。'],
 'risks':['A1不能把短钥绳拉成长绳或变项链；钥匙半入原袋须有清楚袋口/手/绳遮挡，不复制第二钥。','A2单左手仍能托稳小空碗：掌底接触、指组扣外壁，倾角小，不把碗悬空或只捏碗唇。'],
 'plans':[
  {'key':'tian_A1_stow_key_at_pocket','title':'将原钥匙半收入围裙袋','evidence':[('tian_card','体貌','右手总揣在围裙口袋里'),('tian_card','随身物','系着钥绳的旧钥匙与一只备用碗')],
   'start':'右手在原右侧袋口抓钥绳，小钥在袋前垂着；左手维持备用空碗靠腹。',
   'pose':'右肘略向外，右手从单纯抓绳改为拇指与食指/中指直接捏稳原小铁钥的环端，把钥匙齿端朝下送入人物右侧（画面左）原围裙袋口，停在钥匙下半被袋口遮住而环端与手指仍可辨的瞬间。原短钥绳形成一条松小弧连着同一环端，不拉紧成限制物，也不变长。头略低看袋口，右腕有真实内转，左掌仍托原空碗紧靠左腹，碗口近水平。双鞋稳站。',
   'end':'可放松手让原钥匙回自己原袋内；不表示收缴、扣留或接收别人的钥匙，未画后续帧。',
   'contact':['右指捏同一小钥环端，齿部确实经过原袋口，不穿袋布、不悬空','原短绳只一条连一匙；可自然弯曲，不能绳断或凭空接到碗','左掌托碗底/外壁，碗不移动给右手；身体重心在两鞋之间'],
   'props':['单匙、短绳、原围裙袋、单空碗，均无新增','袋前不另留一枚完整悬挂钥匙；可见环端属入袋中的同一匙'],
   'diff':'母图/两表情都是抓绳让钥垂下，本姿直接捏钥并与袋口发生遮挡接触；不是只低头，也不是赫斯腰钥装饰或转交钥匙。','risk':'medium_high_small_prop'},
  {'key':'tian_A2_tilt_bowl_toward_self','title':'抬左肘向内查看空碗','evidence':[('tian_card','随身物','一只备用碗'),('home01','共住边界','缇安不能用取物换放弃旧钥。')],
   'start':'左手托原空碗靠腹，右手在原袋口稳住短钥绳，原小钥垂在袋前。',
   'pose':'左肘明显弯高，把同一备用小空碗从腹前抬到下胸近身处；左掌托住碗底、指组扣住外壁，碗口轻向人物自己倾约二十度，使她低眼能看见空的碗底。碗不伸向观者，身体轻微前倾看碗但不过度弯腰，右手仍在右袋口握短钥绳，小钥仍只有一枚并垂在原袋前。肩肘高度和碗朝向需明显区别母图的低位水平托碗。双脚稳站、裙摆不改变长度。',
   'end':'左臂可放回腹前原持碗高度；不倒水、不加食物、不喂人、不递出。',
   'contact':['左手底掌承重并用指组稳住外壁，拇指在碗沿外，不穿碗腔','碗仅小角度向自己倾，空腔没有液体或隐藏物；不翻到倒扣','右手、绳、钥仍留右袋口原侧；双足支撑和小幅前倾重心合理'],
   'props':['仍是原小碗、原小钥和短钥绳，没有擦布/勺/水壶或新容器','碗材质、口径、厚度与母图一致，不变成深锅或杯'],
   'diff':'与Doro双手向外伸送水平空碗的动作相反：本姿单左手近身抬碗、口朝自己、目检碗内；与Tian母图/表情的腹前水平托碗区分。','risk':'medium'}]},
 'lein':{
 'id':'HIG-NPC-LEIN','name':'蕾因','identity':'三十多岁成年女向导；暖风晒肤色、较宽颧面、外翻短棕发、低棕软帽、深松绿短披、沙棕短衣、灰赭绑腿、补旧棕皮靴及小背包。',
 'observation':'母图右手（画面左）摊掌说明，左手（画面右）握左肩背包带；原一截白粉笔横夹人物左帽檐（画面右），中段被帽带小环遮挡；左后侧背包外侧袋（画面右）插一卷客约。E1右手收腹、E2右掌低摊，均未操作帽上粉笔或腿部绑带。',
 'side':'白粉笔在人物左帽檐（画面右）横穿原帽带小环；背包和客约侧袋在人物左后（画面右）。A1左手碰粉笔、右手扶帽右缘；A2右手（画面左）碰自己右小腿绑带。',
 'guards':['客约始终卷在原左侧背包袋中，不展开、不改写、不盖章、不退费/收款/再订约，也不暗示责任解除。','粉笔只收稳，不画地图、路标、通行标记、路线许可或免等承诺；安全道路和停牌状态均不由姿态改变。','绑腿只作服装日常按平，不画擦伤、包扎、诊断、疗效或实际越过阻断。'],
 'risks':['母图白粉笔被小环挡住中段，仍是一截；不能按两端误画两根、香烟或羽毛。','A2半蹲需臀后移、两膝屈曲、双靴着地和手到右绑腿的可达接点；不能短腿消失、凭空坐凳或变单膝跪姿。'],
 'plans':[
  {'key':'lein_A1_reseat_chalk_in_hat_loop','title':'扶帽沿并按稳原粉笔','evidence':[('lein_card','衣着与磨损','帽檐别着一截粉笔'),('lein_card','衣着与磨损','背包侧袋插着客约卷')],
   'start':'原粉笔仍横在左帽檐小环里，左手从背包带抬向帽侧，右手从说明位置抬向帽右前缘。',
   'pose':'两肘抬起但避开脸，右手（画面左）轻扶原软帽的右前帽沿稳定帽子；左手（画面右）拇指与食指在左帽檐处接触同一短白粉笔的露出端，把它沿原横向小环轻轻按回约一点点，停在手指仍接触粉笔而粉笔中段仍穿在原环里的瞬间。粉笔不拔出，帽子仍戴在头上，露出端保持短钝，不遮双眼。肩臂形成明显高于母图的双接触姿态，躯干直立、双脚稳站。左肩背包带仍套肩承重；卷客约原袋不动。',
   'end':'双手可从帽边降回自然位置；不把这一步称行前许可、完成整备或引路已出发。',
   'contact':['右指轻贴帽沿而不穿帽，左两指明确碰同一粉笔露端，不能捏空气','粉笔中段始终穿原小环，总共一截；帽仍在头上，不变脱帽礼','背包仍由原肩带承重，左手离带不让包悬空分离；双靴着地'],
   'props':['帽、帽环、单粉笔、背包、卷客约全部原物，无新扣件','不拿出客约、不添加地图、杖、绳或笔盒'],
   'diff':'与自身空手说话/抓背带不同，两臂明显抬高到帽缘并操作原粉笔；旧库无同类帽环粉笔接触，不是通用举掌。','risk':'medium_high_small_prop'},
  {'key':'lein_A2_crouch_smooth_right_calf_wrap','title':'半蹲按平右小腿绑带','evidence':[('lein_card','体貌','小腿有常年走山路的紧实'),('lein_card','衣着与磨损','向导短披配耐磨绑腿')],
   'start':'在平稳位置双脚分开站住，粉笔与客约均留原处，双手由说明和背带位置移向自己腿部。',
   'pose':'两膝弯曲、髋向后落成稳定半蹲，双靴分开且整个鞋底都着地；右膝（画面左）略前，躯干从髋部向前折而头低看自己的右小腿。右手（画面左）掌指贴住右小腿前外侧上部的一圈原灰赭绑带，按平它原已存在的叠边；左掌（画面右）贴左大腿膝上辅助稳身，左肘弯曲。绑带不解开、不拉成长条、不新增一圈；右靴仍在右脚。背包仍靠原肩带贴背、客约留左侧袋，粉笔留左帽环。',
   'end':'右手可离开绑带、身体可回原站姿；仅文字，不补站起帧，不表示走完山路或衣物已检验合格。',
   'contact':['右掌实际接右绑腿上部叠边，左掌贴左大腿，不能手臂跨错腿','髋向后、双膝顺脚尖弯，重心在双鞋支撑区，双靴完整不踮脚、不跪地','包带连续且包贴背，原客约不滑出；披风不挡住关键的掌/绑腿接点'],
   'props':['单原绑腿系统不解开或复制；无新布、绷带、伤处或工具','粉笔、客约、帽与背包保持母图侧别及数量'],
   'diff':'本人母图/表情全站姿，本姿有髋膝变化及右掌/绑腿接点；不同于训练样板单膝休息、Luomin放灯或Cuoer敲轨，不新增地面目标。','risk':'high_crouch_contact'}]}}
characters=[];viewlog=[]
for slug,c in char_data.items():
 rc=byid[c['id']];q=byqa[slug];mother=B/slug/'concept_v1';expr=B/slug/'expressions_v1'
 snap(slug+'_card',rc['current_card']['path'],'当前人物卡原文与边界')
 assert sha((R/rc['current_card']['path']).read_bytes())==rc['current_card']['sha256']
 for idpart,p in [('mother_manifest',mother/'manifest.json'),('mother_spec',mother/'spec_lock.md'),('expression_manifest',expr/'manifest.json'),('expression_qa',expr/'QA-independent-second-four-expressions.json')]:snap(slug+'_'+idpart,p,'已冻结源只读快照')
 paths=[R/q['artifact'],R/q['delivery_binding']['transparent'],expr/'review'/f'{slug}_expressions_light.png']
 for j,p in enumerate(paths):
  s=snap(slug+['_mother_raw','_mother_transparent','_expressions_view'][j],p,'本轮实际view图像，只读原字节快照');viewlog.append({'path':rel(p),'sha256':s['sha256'],'actually_viewed':True,'observation':c['observation']})
 assert sha(paths[0].read_bytes())==q['sha256'];assert sha(paths[1].read_bytes())==q['delivery_binding']['transparent_sha256']
 cm=json.loads((mother/'manifest.json').read_text());mf=cm['files'];mhash={x['path']:x['sha256'] for x in mf} if isinstance(mf,list) else mf
 assert mhash[paths[0].name]==q['sha256'];assert mhash[paths[1].name]==q['delivery_binding']['transparent_sha256']
 plans=[]
 for p in c['plans']:
  ev=[]
  for sid,loc,quote in p['evidence']:
   s=next(x for x in src if x['source_id']==sid);lines=(R/s['path']).read_text().splitlines();nums=[i for i,l in enumerate(lines,1) if quote in l];assert nums,(sid,quote)
   ev.append({'source_id':sid,'locator':loc,'line_start':nums[0],'quote':quote})
  prompt=common+'\n人物：'+c['identity']+'\n原侧别与锚定：'+c['side']+'\n本张动作：'+p['title']+'。'+p['pose']+'\n接触与重心：'+'；'.join(p['contact'])+'。\n物件保留：'+'；'.join(p['props'])+'。\n剧情边界：'+'；'.join(c['guards'])+'。\n硬约束：'+'；'.join(c['risks'])+'。只画上述一个瞬间，不画文字说明的起止姿态。'
  pf=O/(p['key']+'_prompt.txt');pf.write_text(prompt)
  plans.append({'key':p['key'],'title_zh':p['title'],'status':'planned_not_generated','output_count':1,'kind':'independent_full_body_noncombat_keypose','evidence':ev,'art_inference':'源文只支持人物、物件与边界；本具体手位、物件朝向和重心是可逆日常动作提案，不冒充台本已发生的事件或医学建议。','start_pose_description_only':p['start'],'pose':p['pose'],'end_pose_description_only':p['end'],'transition_scope':transition,'contact_and_support_checks':p['contact'],'prop_state_and_retention':p['props'],'difference_from_mother_expression_and_batch':p['diff'],'risk_level':p['risk'],'reference_image_paths':[rel(paths[1])],'reference_sha256':[sha(paths[1].read_bytes())],'prompt':prompt,'prompt_sha256':sha(prompt.encode()),'prompt_file':rel(pf),'negative_constraints':c['risks']+c['guards'],'new_contact_prop':None,'animation_claim':False,'sequence_required':False,'new_story_fact':False,'generation_budget':{'initial':1,'max_hard_error_revisions':1,'revision_only_for':'明确可定位的人体/接触/道具数目侧别/身份等硬错；不是无止境美感迭代','safety_blocked':'stop; no circumvention, prompt laundering or alternate generator'},'review_status':'planning_author_checked; independent_plan_review_pending'})
 characters.append({'slug':slug,'canonical_id':c['id'],'name':c['name'],'status':'selected_planned_not_generated','selection_status':'requested_candidate_kept','source_card_hash_matches_roster44':True,'source_ids':[slug+'_card',slug+'_mother_manifest',slug+'_mother_spec',slug+'_expression_manifest',slug+'_expression_qa'],'mother_image':{'raw':rel(paths[0]),'raw_sha256':sha(paths[0].read_bytes()),'transparent':rel(paths[1]),'transparent_sha256':sha(paths[1].read_bytes()),'manifest':rel(mother/'manifest.json'),'manifest_sha256':sha((mother/'manifest.json').read_bytes()),'independent_qa_source_id':'mother_qa','actual_visual_observation':c['observation'],'fixed_sides':c['side'],'raw_and_transparent_actually_viewed':True,'expression_board_actually_viewed':rel(paths[2])},'duplicate_check':{'own_existing_branches':sorted(x.name for x in (B/slug).iterdir() if x.is_dir()),'own_action_directories_found':[],'existing_expressions_actually_viewed':True,'do_not_recount':['母图与表情小手势','sources内复用图','重复展示板/源ZIP成员','只有表情或头姿的变化']},'story_boundaries':c['guards'],'risks':c['risks'],'proposed_output_directory':f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1','plans':plans})
write(O/'actual_view_log.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'view_tool':'functions tools.view_image; original full images; no new composite fabricated','images':viewlog})
scan=json.loads((O/'action_tree_scan.json').read_text())
sem={'scope':'全CharacterActions文本和ZIP文本语义检索后人工判断；不把引用角色的他人文档或随机base64子串当动作。','candidate_match_resolution':[{'path':x['path'],'tokens':x['matching_tokens'],'classification':'source_copy_or_cross_character_reference' if x['copied_source_context'] else ('Anni护理边界提及枯恩，不是枯恩动作' if 'production_brief' in x['path'] else '生图回执base64中随机kUEn子串，不是姓名/ID/资产')} for x in scan['candidate_matches']],'zip_candidate_match_resolution':'24个命中均是上述边界/AGENTS/前批brief/台本快照或同一base64误命中；没有四人动作选稿目录。','near_duplicates_reviewed':[{'old':'Mia blanket_adjust / Osin sleeve_settle / Vasen apron_brush','decision':'不复刻；Kuen A1双手合拢身上披肩，非独立叠毯/袖口/围裙。'},{'old':'Nara seated story gestures / training rest_transition / Hers turn','decision':'Kuen A2保臀脚原位、肩胸侧转和椅沿接点，不抬掌/起坐/逃离。'},{'old':'Anni/Nisha ledger pages / Gura short note / Lyd papers','decision':'Sune不书写不翻页；A1收原炭笔，A2转同一刚性记录板自持。'},{'old':'Doro empty_bowl_present','decision':'Tian A2单手把碗抬向自己看空腔；禁止双手向外递碗。'},{'old':'Lein expression E1/E2 / general open palms','decision':'A1双手帽沿/粉笔接触，A2右绑腿接触，均不是原说话姿态。'},{'old':'Luomin lantern lowering / Cuoer crouch rail tap / training kneel','decision':'Lein A2是双足半蹲按自身右绑腿，没有地面接触物或单膝跪。'}],'selected_candidate_action_assets_found':0,'result':'8项具有不同接触/姿态目标；仍待独立计划审查，未宣称成图动作成立。'}
write(O/'semantic_dedup_review.json',sem)
shutil.copyfile('/tmp/scan_third_actions.py',O/'scan_action_tree.py')
# All original source bytes must still match after snapshotting.
for s in src:assert sha((R/s['path']).read_bytes())==s['sha256'],s['path']
sm={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'planning_sources_only_no_generated_images','source_records':src,'files':[]}
for p in sorted(O.rglob('*')):
 if p.is_file() and p.name not in ['SNAPSHOT_MANIFEST.json']:
  b=p.read_bytes();sm['files'].append({'path':rel(p),'bytes':len(b),'sha256':sha(b)})
write(O/'SNAPSHOT_MANIFEST.json',sm)
d={'schema_version':3,'created_utc':datetime.now(timezone.utc).isoformat(),'status':'planning_complete_not_generated','purpose':'第三批4名既有新剧情NPC的8个独立非战斗基础动作，仅规划；未调用生图，未改冻结源或剧情。','scope':{'selected_characters':4,'planned_new_independent_fullbody_keyposes':8,'generated_images':0,'revision_images':0,'new_characters':0,'full_animation':False,'gif_planned':False,'equipment_or_engine_work':False,'git_or_upload_performed':False,'changed_existing_assets':False},'requested_candidates':['kuen','sune','tian','lein'],'substitutions':[],'global_boundaries':['每人2张独立静态姿态；起止只写文字，不称连续、循环或默认先后。','严格使用每人的已审透明母图；本轮已实际view对应raw、透明与两表情对照板。','全部只用母图已有器物；无新人物、接触物、背景、任务条件或道具所有权。','枯恩保原椅凳杯、布卷与坐姿承重，禁止站起、自饮、治疗、痊愈或帮助需求被取消。','苏奈不写数据；缇安不交钥或换物；蕾因不展示客约/通行承诺；动作不能替代本人用途授权。','每姿首稿1次＋最多1次明确硬错修订；安全blocked立即停，不换工具、提示词洗白或绕过。','只新增本brief和sources；旧图、manifest、QA、收据、台本与人物卡全部只读。','后续生成前重读本动作spec并验母图SHA；不把旧spec的概念暂停或全员统一比例重新当门槛。'],'source_sha_snapshots':src,'coverage_audit':{'read_indexes':['action_coverage','master_supplements','action_delivery_index','first_actions_brief','second_actions_brief'],'scan_manifest':rel(O/'action_tree_scan.json'),'scan_manifest_sha256':sha((O/'action_tree_scan.json').read_bytes()),'action_tree_file_count':scan['file_count'],'metadata_scanned_count':scan['metadata_count'],'zip_scanned_count':scan['zip_count'],'zip_members_enumerated_count':sum(len(z['members']) for z in scan['zips']),'zip_text_members_read_count':sum(z['text_members_read'] for z in scan['zips']),'zip_read_errors':[],'candidate_raw_text_hits':len(scan['candidate_matches']),'candidate_non_source_raw_text_hits':2,'candidate_zip_text_or_path_hits':sum(len(z['candidate_matches']) for z in scan['zips']),'candidate_semantic_action_assets_found':0,'candidate_own_action_directories_found':0,'semantic_review':rel(O/'semantic_dedup_review.json'),'semantic_review_sha256':sha((O/'semantic_dedup_review.json').read_bytes()),'existing_delivered_status':'8位既有人物、14张通过独审静态动作；第二批8计划仅6合格，图里A1与锉珥A1仍缺项。','absence_scope':'仅本地Assets/CharacterActions全树、其45个ZIP全部文本元数据与四人new_story分支；未声称外部电脑/云源或所有图片视觉遍查。','all_four_raw_and_transparent_viewed':True,'all_four_expression_boards_viewed':True},'characters':characters,'future_acceptance_checks':['先实际view每张raw、透明和浅深底展示；alpha分析不能代替视觉检查。','逐人与自己的母图及表情并排核身份、成年年龄、比例、接触变化和道具侧别；不能按文件数凑8动作。','Kuen A1确认原披肩相连；A2臀部/双脚原支撑和后腰布卷不断，左手轻搭椅面而非撑起，杯凳布条不动。','Sune A1总笔数2且笔真入插，A2仅单木板旋转并由两手承重；全程无写字/数据。','Tian A1同匙半入原右袋，A2左手底托小空碗向内，右钥原侧；不把递碗旧动作重做。','Lein A1一截粉笔仍穿原帽环、两手各有接点；A2双足半蹲、右手达右绑腿、左掌达左腿，包带和卷客约保持。','首稿有明确硬错最多1修；修后仍失败保留缺项，不用脚本修人体或私增第三稿。','不做GIF、不填过渡、不改装备/原生方向/origin/游戏，未运行不称可用。'],'verification':{'json_parse':True,'plan_count':8,'characters_in_roster44':True,'all_evidence_quotes_found_in_current_sources':True,'all_four_anchor_hashes_match_manifest_and_independent_qa':True,'four_mothers_raw_and_transparent_actually_viewed':True,'four_expression_boards_actually_viewed':True,'copied_source_hashes_verified':True,'all_original_source_hashes_still_match':True,'prompt_files_sha_verified':True,'generated_images':0,'validation_scope':'新增计划结构、逐字引文/行号、路径、真实源SHA/原字节快照、完整动作树/ZIP文本去重；不改剧情，未声称全库剧情验证或游戏运行。'},'source_snapshot_manifest':{'path':rel(O/'SNAPSHOT_MANIFEST.json'),'sha256':sha((O/'SNAPSHOT_MANIFEST.json').read_bytes())},'independent_plan_review_status':'pending_not_generated'}
write(A/'third_new_character_actions_brief.json',d)
print('BRIEF',rel(A/'third_new_character_actions_brief.json'));print('SHA',sha((A/'third_new_character_actions_brief.json').read_bytes()));print('SNAPSHOTS',len(src),'FILES',len(sm['files']));print('SCAN',d['coverage_audit'])
for c in characters:
 for p in c['plans']:print(p['key'],p['title_zh'],p['prompt_sha256'])
