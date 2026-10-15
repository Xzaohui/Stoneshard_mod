# Batch30 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## tio · selected_derived_candidate_with_limitations
选稿：`tio/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`c35a5246c4fcfd150604f94b25f94ce3cf1469291095fd7bde8e90d8f8a9f2ed`
限制：颈仍稍长、发线仍偏细，未完全达到四核心的短颈粗块精修程度；同raw等比NEAREST/32色量化技术派生候选，不是原生逐像素或实机终稿。

## saifu · held_after_two_generations_style_composition
暂挂证据：`saifu/candidates/portrait_v2_74x100_candidate.png`
SHA256：`8aff97e53a78b64a6cbb510f5f204ec4a2edc9b8a8d6c383ec58d4ae2bb11a08`
限制：大脸短颈窄领目标未达，眼白/表情仍偏离小暗眼与谨慎自尊的要求；肤色仍偏暖，最新卡较浅肤色尚未充分体现在完成稿中；此是外观待改善，不构造新身份冲突；仅保留v2为held evidence，selected=null，不得纳入交付选稿。

## kaino · selected_derived_candidate_with_limitations
选稿：`kaino/candidates/portrait_v2_safe_74x100_candidate.png`
SHA256：`2c906c39e1b5e1018eba7e32cfa63e671b707b7772305746806d2b5a414c64f7`
限制：肤色仍稍暖，须保留NN技术派生/临时32色限制；只选70×96 safe导出；full与72×98 inset仅过程证据；不是原生逐像素、游戏集成或实机验收终稿。

## buze · held_after_two_generations_style_composition
暂挂证据：`buze/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`9bf8151b178c6e7b8327bc2b1e04421fa7d7cf2487c734c725109df6fffc62d6`
限制：小暗眼白、短颈窄领及个性表情目标未充分满足；v2_inset仅保留为held evidence，不可纳入交付选稿；NN派生过程图不是原生逐像素或游戏终稿。

## 证据与边界
- 30份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图：提奥20+酿酒学徒不与贝洛混同；赛芙30+较浅肤色与素巾；凯诺50岁上下；布泽40+干瘦不继承旧母版壮实。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
