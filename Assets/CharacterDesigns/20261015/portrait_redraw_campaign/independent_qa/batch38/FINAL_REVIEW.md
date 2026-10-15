# Batch38 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## vila · accepted_with_notes_as_NN_derived_candidate
选稿：`vila/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`49f48179cf94d2aaef4db5e5362b0c752a64a861573ef9acb43ef8b620949627`
限制：性别仍未定，不据中性外观冻结身份canon；夹镜边及眼白仍较亮，面部仍有imagegen细簇；仅有注记NN派生候选；源边余量偏窄；inset不是重绘或原生像素验收；未逐像素原生绘制，未集成或实机验收。

## hepo · accepted_with_notes_as_NN_derived_candidate
选稿：`hepo/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`a95180b96ffa8cdae43fdfa4b4b42e0bb5d338fdc00b2c71ce7e08894df088be`
限制：白眼仍偏浅，绿披及下颈占比仍略大于核心；仅有注记NN派生候选；源右边只留很窄的主要轮廓余量，边缘alpha5噪点仍记录；不把inset说成裁断修复；未逐像素原生绘制，未集成或实机验收。

## siyu · accepted_with_notes_as_NN_derived_candidate
选稿：`siyu/candidates/portrait_v2_74x100_candidate.png`
SHA256：`b1fb37e69591762d7d868b20e9367b29f6a0abe49618decfd8871d3645fe696d`
限制：末S91他与正文她的代词不一致留痕，沿正文及女性母图，不修改源卡；眼白仍偏浅，额部有细碎簇；仅有注记NN派生候选；未逐像素原生绘制，未集成或实机验收。

## buxi · accepted_with_notes_as_NN_derived_candidate
选稿：`buxi/candidates/portrait_v2_74x100_candidate.png`
SHA256：`f9b70515f015f28b7fa4b004d14abab888b245287c5ac572aec7b54171879ddd`
限制：现卡S91孤立他与旧女性母设定歧义，经git/brief/prompt及剧情核对后协调保女性继续，未改源卡；少量眼白及鼻粉仍浅、面簇偏柔；仅有注记NN派生候选；未逐像素原生绘制，未集成或实机验收。

## 证据与边界
- 35份原始源/历史git证据独立快照与终检SHA一致；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 维菈约40岁中性可逆提案，性别未定，人物左眼放大夹不反向。司榆遵最新正文女性，末段单他记录为歧义。布希旧卡未定、母brief/prompt女性与现卡S91孤立他经历史核对后由协调保女性继续，未改源卡；最新年龄衣装细描优先。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
