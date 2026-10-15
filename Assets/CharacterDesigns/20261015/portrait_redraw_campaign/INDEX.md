# 全人物对白头像重绘计划

快照：2026-10-15T08:07:30Z

当前核得 **217 个唯一身份**：旧172＋后续44＋S200坎沃1。222是人物目录Markdown文件数，211是历史送达概念口径，都不是本轮人数。

本轮只做74×100对白头像。旧图原样保留，新图独立存放；地图失败单列，不把表情、动作、返修稿或合图重复计人。

## 当前状态

- completed_portrait_candidate: 4
- assigned_in_progress: 7
- ready_for_identity_preflight: 199
- blocked_reference_verification: 3
- blocked_source_conflict: 1
- blocked_missing_master: 1
- blocked_safety: 1
- needs_scope_review: 1

已选4核心候选：玛拉、伊沃、蕾雅、托雷；只是候选头像完成，非原生逐像素/入游戏验收。

## 派工入口

- [当前五人](batch_01_active.json)：米娅、灰堤艾娜、纳拉、妮尔、塞尔
- [第二批冻结r2](batch_02_next.json)：已派托曼/塞娜，待派莉德/莫伦
- [完整名册与证据](campaign_roster.json)
- [后续逐批队列](queue_batches.json)
- [阻断与待定](blocked_and_held.json)
- [身份去重核验](identity_reconciliation.json)

下一批恢复当前台本实说顺序；赫斯在S200新增N4具名出场，所以优先补入。凯姆在合集链接N6，但现行具名发言首先在N10，已纠正，不以链接代替首演。

## 边界与待定

- 维安：旧安全阻断，禁止重试/改词/换工具。
- 瑟珥：精确封存E1表情修订；静态概念与普通动作不全是安全阻断。本轮头像按父任务暂挂needs_scope_review。
- 维伦、葛文涅尔、Darrel：原作参考未核，不能用风格图代造身份。
- 欧达：现卡男性代词/40多与旧女性年长母版有冲突，暂挂。
- 坎沃：有新卡但无旧母版/外观设定，不凭空补脸。
- 朔娅：旧稿是视觉研究未通过，不是安全阻断，可按新风格重新预检重绘。

## 校验口径

本次只核卡、ID/别名、母版选稿来源、文件存在与SHA；没有重新逐像素视觉验收212份母版。生产前仍需实际看母版/现卡/风格锚，发现身份冲突另报，不悄改。当前卡SHA变化只提示重读，不自动判全员失败。

## 逐人队列

| 顺位 | ID | 人物 | 最早主线具名对白 | 状态 |
|---|---|---|---|---|
| 1 | n1_ivo | 伊沃 | N1 | completed_portrait_candidate |
| 2 | n1_mara | 玛拉 | N1 | completed_portrait_candidate |
| 3 | n1_rhea | 蕾雅 | N1 | completed_portrait_candidate |
| 4 | n1_tor | 托雷 | N1 | completed_portrait_candidate |
| 5 | NPC-N-ENA | 艾娜 | N2 | assigned_in_progress |
| 6 | NPC-N-NARA | 纳拉 | N2 | assigned_in_progress |
| 7 | NPC-N-NELL | 妮尔 | N3 | assigned_in_progress |
| 8 | NPC-HERS | 赫斯·白 | N4 | ready_for_identity_preflight |
| 9 | NPC-N-SEL | 塞尔 | N4 | assigned_in_progress |
| 10 | NPC01 | 维伦 | N4 | blocked_reference_verification |
| 11 | NPC07 | 托曼·索 | N5 | assigned_in_progress |
| 12 | NPC09 | 欧达·苇 | N5 | blocked_source_conflict |
| 13 | NPC-LYD | 莉德 | N6 | ready_for_identity_preflight |
| 14 | NPC-SENA | 塞娜·里德 | N6 | assigned_in_progress |
| 15 | NPC-MORREN | 莫伦·海 | N7 | ready_for_identity_preflight |
| 16 | NPC-REY | 雷奥·凯斯 | N7 | ready_for_identity_preflight |
| 17 | NPC-S200-KANWO | 坎沃·岩 | N7 | blocked_missing_master |
| 18 | NPC-MIA | 米娅 | N8 | assigned_in_progress |
| 19 | NPC04 | 伊莲·沃斯 | N9 | ready_for_identity_preflight |
| 20 | MAE-NPC-KAEM | 凯姆 | N10 | ready_for_identity_preflight |
| 21 | NPC-N-AREN | 艾伦 | N11 | ready_for_identity_preflight |
| 22 | NPC11 | 罗温·雾 | N11 | ready_for_identity_preflight |
| 23 | NPC02 | 葛文涅尔 | N12 | blocked_reference_verification |
| 24 | NPC03 | 工匠 Darrel | N14 | blocked_reference_verification |
| 25 | NPC-MAYA | 玛娅·禾 | N16 | ready_for_identity_preflight |
| 26 | BRY-NPC-ANLA | 安菈 | 城镇/野外批 | ready_for_identity_preflight |
| 27 | BRY-NPC-AVI | 阿薇 | 城镇/野外批 | ready_for_identity_preflight |
| 28 | BRY-NPC-DARAN | 达兰 | 城镇/野外批 | ready_for_identity_preflight |
| 29 | BRY-NPC-ELEN | 艾伦 | 城镇/野外批 | ready_for_identity_preflight |
| 30 | BRY-NPC-HASE | 哈塞 | 城镇/野外批 | ready_for_identity_preflight |
| 31 | BRY-NPC-HERLIN | 赫林 | 城镇/野外批 | ready_for_identity_preflight |
| 32 | BRY-NPC-IVE | 伊芙 | 城镇/野外批 | ready_for_identity_preflight |
| 33 | BRY-NPC-JOTIN | 乔彤 | 城镇/野外批 | ready_for_identity_preflight |
| 34 | BRY-NPC-LODA | 洛妲 | 城镇/野外批 | ready_for_identity_preflight |
| 35 | BRY-NPC-MALER | 麦勒 | 城镇/野外批 | ready_for_identity_preflight |
| 36 | BRY-NPC-MARIS | 玛莉丝 | 城镇/野外批 | ready_for_identity_preflight |
| 37 | BRY-NPC-MIRO | 米罗·账 | 城镇/野外批 | ready_for_identity_preflight |
| 38 | BRY-NPC-ODER | 奥德 | 城镇/野外批 | ready_for_identity_preflight |
| 39 | BRY-NPC-OSIN | 奥辛·锤 | 城镇/野外批 | ready_for_identity_preflight |
| 40 | BRY-NPC-PELAN | 佩兰 | 城镇/野外批 | ready_for_identity_preflight |
| 41 | BRY-NPC-RENA | 蕾娜·维尔 | 城镇/野外批 | ready_for_identity_preflight |
| 42 | BRY-NPC-ROAN | 罗安 | 城镇/野外批 | ready_for_identity_preflight |
| 43 | BRY-NPC-SELA | 瑟拉 | 城镇/野外批 | ready_for_identity_preflight |
| 44 | BRY-NPC-SEV | 塞芙 | 城镇/野外批 | ready_for_identity_preflight |
| 45 | BRY-NPC-TAORI | 陶芮 | 城镇/野外批 | ready_for_identity_preflight |
| 46 | BRY-NPC-VIMON | 维松 | 城镇/野外批 | ready_for_identity_preflight |
| 47 | BRY-NPC-VIT | 薇特·灰 | 城镇/野外批 | ready_for_identity_preflight |
| 48 | BRY-NPC-WOLEN | 沃伦 | 城镇/野外批 | ready_for_identity_preflight |
| 49 | BRY-NPC-YANI | 雅尼 | 城镇/野外批 | ready_for_identity_preflight |
| 50 | BRY-S01-NPC | 鲁坎 | 城镇/野外批 | ready_for_identity_preflight |
| 51 | BRY-S02-NPC | 芮莎 | 城镇/野外批 | ready_for_identity_preflight |
| 52 | BRY-S03-NPC | 米蕾 | 城镇/野外批 | ready_for_identity_preflight |
| 53 | ALD-NPC-BUYA | 布娅 | 城镇/野外批 | ready_for_identity_preflight |
| 54 | ALD-NPC-CHILER | 齐勒 | 城镇/野外批 | ready_for_identity_preflight |
| 55 | ALD-NPC-EMO | 埃墨·衬 | 城镇/野外批 | ready_for_identity_preflight |
| 56 | ALD-NPC-HEL | 赫莲·金 | 城镇/野外批 | ready_for_identity_preflight |
| 57 | ALD-NPC-KIEN | 奇恩 | 城镇/野外批 | ready_for_identity_preflight |
| 58 | ALD-NPC-KONA | 科纳 | 城镇/野外批 | ready_for_identity_preflight |
| 59 | ALD-NPC-MUKO | 穆柯 | 城镇/野外批 | ready_for_identity_preflight |
| 60 | ALD-NPC-NAETIN | 奈汀 | 城镇/野外批 | ready_for_identity_preflight |
| 61 | ALD-NPC-SIN | 司诺·庭 | 城镇/野外批 | ready_for_identity_preflight |
| 62 | ALD-NPC-SORE | 索芮 | 城镇/野外批 | ready_for_identity_preflight |
| 63 | ALD-NPC-VIAN | 维安 | 城镇/野外批 | blocked_safety |
| 64 | ALD-NPC-YIRONG | 伊榕 | 城镇/野外批 | ready_for_identity_preflight |
| 65 | ALD-S01-NPC | 泊恩 | 城镇/野外批 | ready_for_identity_preflight |
| 66 | ALD-S02-NPC | 芬珂 | 城镇/野外批 | ready_for_identity_preflight |
| 67 | ALD-S03-NPC | 萝铎 | 城镇/野外批 | ready_for_identity_preflight |
| 68 | MAE-NPC-BENO | 贝诺 | 城镇/野外批 | ready_for_identity_preflight |
| 69 | MAE-NPC-DORO | 多罗 | 城镇/野外批 | ready_for_identity_preflight |
| 70 | MAE-NPC-FIL | 菲勒·火 | 城镇/野外批 | ready_for_identity_preflight |
| 71 | MAE-NPC-GULAN | 古岚 | 城镇/野外批 | ready_for_identity_preflight |
| 72 | MAE-NPC-NIV | 尼芙 | 城镇/野外批 | ready_for_identity_preflight |
| 73 | MAE-NPC-OURAN | 欧岚 | 城镇/野外批 | ready_for_identity_preflight |
| 74 | MAE-NPC-VERE | 维芮 | 城镇/野外批 | ready_for_identity_preflight |
| 75 | MAE-NPC-ZAHO | 扎禾 | 城镇/野外批 | ready_for_identity_preflight |
| 76 | MAE-S01-NPC | 缇弗 | 城镇/野外批 | ready_for_identity_preflight |
| 77 | MAE-S02-NPC | 薇榆 | 城镇/野外批 | ready_for_identity_preflight |
| 78 | MAE-S03-NPC | 艾娜 | 城镇/野外批 | ready_for_identity_preflight |
| 79 | PAS-NPC-ELON | 礼昂 | 城镇/野外批 | ready_for_identity_preflight |
| 80 | PAS-NPC-LEVAN | 列梵 | 城镇/野外批 | ready_for_identity_preflight |
| 81 | PAS-NPC-QILEN | 绮伦 | 城镇/野外批 | ready_for_identity_preflight |
| 82 | PAS-NPC-SHABO | 莎帛 | 城镇/野外批 | ready_for_identity_preflight |
| 83 | PAS-NPC-WOTIN | 沃汀 | 城镇/野外批 | ready_for_identity_preflight |
| 84 | PAS-S01-NPC | 辛娅 | 城镇/野外批 | ready_for_identity_preflight |
| 85 | PAS-S02-NPC | 乌珀 | 城镇/野外批 | ready_for_identity_preflight |
| 86 | KOR-NPC-BILUO | 碧珞 | 城镇/野外批 | ready_for_identity_preflight |
| 87 | KOR-NPC-EV | 埃文·行 | 城镇/野外批 | ready_for_identity_preflight |
| 88 | KOR-NPC-LULING | 卢绫 | 城镇/野外批 | ready_for_identity_preflight |
| 89 | KOR-NPC-NAYA | 娜娅 | 城镇/野外批 | ready_for_identity_preflight |
| 90 | KOR-NPC-NOD | 诺妲·门 | 城镇/野外批 | ready_for_identity_preflight |
| 91 | KOR-NPC-SAILUO | 赛洛 | 城镇/野外批 | ready_for_identity_preflight |
| 92 | KOR-NPC-TAFEI | 塔斐 | 城镇/野外批 | ready_for_identity_preflight |
| 93 | KOR-NPC-XIELAN | 榭兰 | 城镇/野外批 | ready_for_identity_preflight |
| 94 | KOR-NPC-YUEN | 尤恩 | 城镇/野外批 | ready_for_identity_preflight |
| 95 | KOR-S01-NPC | 阿霖 | 城镇/野外批 | ready_for_identity_preflight |
| 96 | KOR-S02-NPC | 玛迪 | 城镇/野外批 | ready_for_identity_preflight |
| 97 | SKO-NPC-BOH | 博赫·冷 | 城镇/野外批 | ready_for_identity_preflight |
| 98 | SKO-NPC-GOREN | 古烈 | 城镇/野外批 | ready_for_identity_preflight |
| 99 | SKO-NPC-NIS | 妮莎·炉 | 城镇/野外批 | ready_for_identity_preflight |
| 100 | SKO-NPC-SALER | 桑勒 | 城镇/野外批 | ready_for_identity_preflight |
| 101 | SKO-NPC-WENNO | 温诺 | 城镇/野外批 | ready_for_identity_preflight |
| 102 | SKO-S01-NPC | 布岚 | 城镇/野外批 | ready_for_identity_preflight |
| 103 | SKO-S02-NPC | 雷哈 | 城镇/野外批 | ready_for_identity_preflight |
| 104 | TRADE-NPC-LIQUI | 莉葵 | 城镇/野外批 | ready_for_identity_preflight |
| 105 | YOS-NPC-ARLO | 阿洛 | 城镇/野外批 | ready_for_identity_preflight |
| 106 | YOS-NPC-HURE | 呼蕾 | 城镇/野外批 | ready_for_identity_preflight |
| 107 | YOS-NPC-ONDO | 昂朵 | 城镇/野外批 | ready_for_identity_preflight |
| 108 | YOS-NPC-TAY | 塔雅·梭 | 城镇/野外批 | ready_for_identity_preflight |
| 109 | YOS-NPC-TIN | 缇娜·染 | 城镇/野外批 | ready_for_identity_preflight |
| 110 | YOS-NPC-XIYOU | 溪悠 | 城镇/野外批 | ready_for_identity_preflight |
| 111 | YOS-S01-NPC | 梅蓓 | 城镇/野外批 | ready_for_identity_preflight |
| 112 | YOS-S02-NPC | 尤尔 | 城镇/野外批 | ready_for_identity_preflight |
| 113 | DEN-NPC-BEVI | 蓓薇 | 城镇/野外批 | ready_for_identity_preflight |
| 114 | DEN-NPC-ELE | 艾蕾 | 城镇/野外批 | ready_for_identity_preflight |
| 115 | DEN-NPC-KAR | 卡蕾·棚 | 城镇/野外批 | ready_for_identity_preflight |
| 116 | DEN-NPC-NOZE | 娜泽 | 城镇/野外批 | ready_for_identity_preflight |
| 117 | DEN-NPC-ODO | 欧铎 | 城镇/野外批 | ready_for_identity_preflight |
| 118 | DEN-NPC-SEF | 瑟芬·网 | 城镇/野外批 | ready_for_identity_preflight |
| 119 | DEN-NPC-TANSER | 坦瑟 | 城镇/野外批 | ready_for_identity_preflight |
| 120 | DEN-NPC-VIKO | 薇柯 | 城镇/野外批 | ready_for_identity_preflight |
| 121 | DEN-S01-NPC | 伊蕾 | 城镇/野外批 | ready_for_identity_preflight |
| 122 | DEN-S02-NPC | 哈伦 | 城镇/野外批 | ready_for_identity_preflight |
| 123 | MNS-NPC-BELO | 贝洛 | 城镇/野外批 | ready_for_identity_preflight |
| 124 | MNS-NPC-FULEN | 芙伦 | 城镇/野外批 | ready_for_identity_preflight |
| 125 | MNS-NPC-JONHE | 琼荷 | 城镇/野外批 | ready_for_identity_preflight |
| 126 | MNS-NPC-MODA | 墨达 | 城镇/野外批 | ready_for_identity_preflight |
| 127 | MNS-NPC-ROS | 罗莎·藤 | 城镇/野外批 | ready_for_identity_preflight |
| 128 | MNS-NPC-TIO | 提奥·桶 | 城镇/野外批 | ready_for_identity_preflight |
| 129 | MNS-S01-NPC | 赛芙 | 城镇/野外批 | ready_for_identity_preflight |
| 130 | MNS-S02-NPC | 凯诺 | 城镇/野外批 | ready_for_identity_preflight |
| 131 | EED-NPC-BUZE | 布泽 | 城镇/野外批 | ready_for_identity_preflight |
| 132 | EED-NPC-FOLAN | 佛兰 | 城镇/野外批 | ready_for_identity_preflight |
| 133 | EED-NPC-GELI | 葛黎 | 城镇/野外批 | ready_for_identity_preflight |
| 134 | EED-NPC-LIN | 黎恩·岗 | 城镇/野外批 | ready_for_identity_preflight |
| 135 | EED-NPC-OLA | 奥菈·纹 | 城镇/野外批 | ready_for_identity_preflight |
| 136 | EED-NPC-RUYA | 芦雅 | 城镇/野外批 | ready_for_identity_preflight |
| 137 | EED-NPC-SUJIN | 苏槿 | 城镇/野外批 | ready_for_identity_preflight |
| 138 | EED-NPC-SUOYA | 朔娅 | 城镇/野外批 | ready_for_identity_preflight |
| 139 | EED-S01-NPC | 欧莎 | 城镇/野外批 | ready_for_identity_preflight |
| 140 | EED-S02-NPC | 岱里 | 城镇/野外批 | ready_for_identity_preflight |
| 141 | FOR-NPC-APE | 艾珀·风 | 城镇/野外批 | ready_for_identity_preflight |
| 142 | FOR-NPC-KEWEI | 科蔚 | 城镇/野外批 | ready_for_identity_preflight |
| 143 | FOR-NPC-LUOFU | 洛芙 | 城镇/野外批 | ready_for_identity_preflight |
| 144 | FOR-NPC-MAN | 玛诺·灯 | 城镇/野外批 | ready_for_identity_preflight |
| 145 | FOR-NPC-QIDUO | 祁铎 | 城镇/野外批 | ready_for_identity_preflight |
| 146 | FOR-NPC-XIJIE | 西婕 | 城镇/野外批 | ready_for_identity_preflight |
| 147 | FOR-S01-NPC | 艾钦 | 城镇/野外批 | ready_for_identity_preflight |
| 148 | FOR-S02-NPC | 蓓娜 | 城镇/野外批 | ready_for_identity_preflight |
| 149 | ASH-NPC-ANNI | 安妮 | 城镇/野外批 | ready_for_identity_preflight |
| 150 | ASH-NPC-KUEN | 枯恩 | 城镇/野外批 | ready_for_identity_preflight |
| 151 | ASH-NPC-LINT | 琳汀·床 | 城镇/野外批 | ready_for_identity_preflight |
| 152 | ASH-NPC-SUNE | 苏奈 | 城镇/野外批 | ready_for_identity_preflight |
| 153 | ASH-NPC-TIAN | 缇安 | 城镇/野外批 | ready_for_identity_preflight |
| 154 | ASH-S01-NPC | 妮蔻 | 城镇/野外批 | ready_for_identity_preflight |
| 155 | ASH-S02-NPC | 奥娅 | 城镇/野外批 | ready_for_identity_preflight |
| 156 | HIG-NPC-ARO | 艾萝·图 | 城镇/野外批 | ready_for_identity_preflight |
| 157 | HIG-NPC-GURA | 古菈 | 城镇/野外批 | ready_for_identity_preflight |
| 158 | HIG-NPC-LEIN | 蕾因 | 城镇/野外批 | ready_for_identity_preflight |
| 159 | HIG-NPC-TURI | 图里 | 城镇/野外批 | ready_for_identity_preflight |
| 160 | HIG-NPC-VILA | 维菈 | 城镇/野外批 | ready_for_identity_preflight |
| 161 | HIG-S01-NPC | 赫珀 | 城镇/野外批 | ready_for_identity_preflight |
| 162 | HIG-S02-NPC | 司榆 | 城镇/野外批 | ready_for_identity_preflight |
| 163 | OSB-NPC-BUXI | 布希 | 城镇/野外批 | ready_for_identity_preflight |
| 164 | OSB-NPC-DON | 多恩 | 城镇/野外批 | ready_for_identity_preflight |
| 165 | OSB-NPC-FUD | 芙朵·谷 | 城镇/野外批 | ready_for_identity_preflight |
| 166 | OSB-NPC-KOFU | 蔻芙 | 城镇/野外批 | ready_for_identity_preflight |
| 167 | OSB-NPC-LEMA | 雷玛 | 城镇/野外批 | ready_for_identity_preflight |
| 168 | OSB-NPC-LUOSHAN | 洛珊 | 城镇/野外批 | ready_for_identity_preflight |
| 169 | OSB-NPC-RUIYIN | 芮茵 | 城镇/野外批 | ready_for_identity_preflight |
| 170 | OSB-NPC-VAS | 瓦森·磨 | 城镇/野外批 | ready_for_identity_preflight |
| 171 | OSB-NPC-YADUO | 雅铎 | 城镇/野外批 | ready_for_identity_preflight |
| 172 | OSB-S01-NPC | 德娅 | 城镇/野外批 | ready_for_identity_preflight |
| 173 | OSB-S02-NPC | 沃达 | 城镇/野外批 | ready_for_identity_preflight |
| 174 | RAT-NPC-ALI | 阿莉·铃 | 城镇/野外批 | ready_for_identity_preflight |
| 175 | RAT-NPC-IME | 伊默·栅 | 城镇/野外批 | ready_for_identity_preflight |
| 176 | RAT-NPC-MILA | 米菈 | 城镇/野外批 | ready_for_identity_preflight |
| 177 | RAT-NPC-NIYE | 妮耶 | 城镇/野外批 | ready_for_identity_preflight |
| 178 | RAT-NPC-SEDUO | 瑟铎 | 城镇/野外批 | ready_for_identity_preflight |
| 179 | RAT-NPC-TUOFEI | 托斐 | 城镇/野外批 | ready_for_identity_preflight |
| 180 | RAT-S01-NPC | 芬罗 | 城镇/野外批 | ready_for_identity_preflight |
| 181 | RAT-S02-NPC | 佩菈 | 城镇/野外批 | ready_for_identity_preflight |
| 182 | FX-ABY | 缇菈 | 城镇/野外批 | ready_for_identity_preflight |
| 183 | FX-BST | 恩岱 | 城镇/野外批 | ready_for_identity_preflight |
| 184 | FX-BUR | 库奇 | 城镇/野外批 | ready_for_identity_preflight |
| 185 | FX-CAT | 洛珉 | 城镇/野外批 | ready_for_identity_preflight |
| 186 | FX-CMP | 珥泰 | 城镇/野外批 | ready_for_identity_preflight |
| 187 | FX-CP1 | 燧珥 | 城镇/野外批 | ready_for_identity_preflight |
| 188 | FX-CP5 | 缶珥 | 城镇/野外批 | ready_for_identity_preflight |
| 189 | FX-CRP | 瑟珥 | 城镇/野外批 | needs_scope_review |
| 190 | FX-CV1 | 珞珥 | 城镇/野外批 | ready_for_identity_preflight |
| 191 | FX-CV2 | 芩珥 | 城镇/野外批 | ready_for_identity_preflight |
| 192 | FX-CV3 | 俉珥 | 城镇/野外批 | ready_for_identity_preflight |
| 193 | FX-CV4 | 佴珥 | 城镇/野外批 | ready_for_identity_preflight |
| 194 | FX-CV5 | 栎珥 | 城镇/野外批 | ready_for_identity_preflight |
| 195 | FX-CV6 | 洄珥 | 城镇/野外批 | ready_for_identity_preflight |
| 196 | FX-FRM | 蓟珥 | 城镇/野外批 | ready_for_identity_preflight |
| 197 | FX-GH2 | 埕珥 | 城镇/野外批 | ready_for_identity_preflight |
| 198 | FX-GHL | 达珥 | 城镇/野外批 | ready_for_identity_preflight |
| 199 | FX-HNT | 珥兰 | 城镇/野外批 | ready_for_identity_preflight |
| 200 | FX-HNY | 忒曼 | 城镇/野外批 | ready_for_identity_preflight |
| 201 | FX-HOM | 苇珥 | 城镇/野外批 | ready_for_identity_preflight |
| 202 | FX-HRP | 妲兰 | 城镇/野外批 | ready_for_identity_preflight |
| 203 | FX-HUT | 珂琳 | 城镇/野外批 | ready_for_identity_preflight |
| 204 | FX-INK | 韦珥 | 城镇/野外批 | ready_for_identity_preflight |
| 205 | FX-LEP | 米洛珥 | 城镇/野外批 | ready_for_identity_preflight |
| 206 | FX-LOT | 绥珥 | 城镇/野外批 | ready_for_identity_preflight |
| 207 | FX-MAN | 岱珥 | 城镇/野外批 | ready_for_identity_preflight |
| 208 | FX-MIL | 霍珥 | 城镇/野外批 | ready_for_identity_preflight |
| 209 | FX-MIN | 珥德 | 城镇/野外批 | ready_for_identity_preflight |
| 210 | FX-MN2 | 锉珥 | 城镇/野外批 | ready_for_identity_preflight |
| 211 | FX-PLG | 蔻珥 | 城镇/野外批 | ready_for_identity_preflight |
| 212 | FX-QRY | 德茹 | 城镇/野外批 | ready_for_identity_preflight |
| 213 | FX-RLY | 珥薇 | 城镇/野外批 | ready_for_identity_preflight |
| 214 | FX-SGE | 瓦顿 | 城镇/野外批 | ready_for_identity_preflight |
| 215 | FX-TRS | 谟珥 | 城镇/野外批 | ready_for_identity_preflight |
| 216 | FX-WCH | 索妲 | 城镇/野外批 | ready_for_identity_preflight |
| 217 | FX-WIL | 摩珥 | 城镇/野外批 | ready_for_identity_preflight |
