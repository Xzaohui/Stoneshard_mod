"""Validate the S164 navigation block on the design overview."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ov = (V / '00_导航/设计总览.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
check('## 最新入口（S125—S163）' in ov, 'block-title')
expected = ['叙事内容清单', '中英对照覆盖报告', '实现交接总表', '试玩路线与检查单', '待办与已知缺口登记', '设计阶段收束核对',
            '原作名与原创名碰撞核对', '原作契据任务与声誉结构参照', '原作声誉档位与地方状态参照',
            '质量守卫总表', '逐角色稿完成度核对', '说话人与人物卡闭合核对', '对白去重与独特性核对', 'R-X头部补齐记录',
            '验证快照依赖登记', '登记文件覆盖分类', '键名口径对账',
            '实现侧现状核对', '工具链离线自检记录', '试点批次总表', '试点实现批次N2', '试点批次验收场景N2',
            '试点实现批次CS-BRY-01', '试点实现批次FX野外层', '引擎键名前缀与遗留键登记', 'N1小样键语义与迁移建议',
            '事件号分配方案', '全链复跑演练S145']
for name in expected:
    check(name in stems, 'target-exists-' + name)
    check(f'[[{name}]]' in ov, 'listed-' + name)
for group in ('**清点与交接**', '**原作参照**', '**质量守卫**', '**实现准备**'):
    check(group in ov, 'group-' + group)
block = ov.split('## 最新入口（S125—S163）', 1)[1].split('<!-- OPEN-ITEMS-S133:END -->', 1)[0]
for lm in re.finditer(r'\[\[([^\]]+)\]\]', block):
    check(lm.group(1) in stems, 'block-link-' + lm.group(1))
check(len(re.findall(r'\[\[', block)) >= 25, 'block-size')
report = dict(date='2026-10-13', scope='S164 navigation block: S134-S163 entry pages listed on the design overview, every target resolves; documentation only',
              listed=len(expected), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'nav-block-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
