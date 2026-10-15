"""Record reviewed S77 artwork without replacing an existing candidate or game file."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil,sys,re
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=Path(sys.argv[1]).resolve()
dest=ROOT/'design/12_美术参考/城市概念/BRY-任务场所-v2.png'
if dest.exists():
 if sha(dest)!=sha(source):raise SystemExit('Refusing to overwrite existing v2.')
else:shutil.copy2(source,dest)
v1=ROOT/'design/12_美术参考/城市概念/BRY-任务场所-v1.png'
references=['stoneshard-assets-sample/atlas-020.png','stoneshard-assets-sample/atlas-099.png','stoneshard-assets-sample/atlas-088.png','design/12_美术参考/城市概念/BRY-概念-v1.png']
prompts=['research/brynn-task-space-art-prompt-s77.txt','research/brynn-task-space-art-edit-s77.txt']
record=dict(date='2026-10-12',status='draft',canon='mod-original',tool='built-in image_gen',
 scope='One six-panel reference board linked to Brynn tasks; no runtime asset or canon map.',
 output=dest.relative_to(ROOT).as_posix(),sha256=sha(dest),dimensions=list(Image.open(dest).size),source_path=str(source),
 references=[dict(path=p,sha256=sha(ROOT/p),role='style only') for p in references],
 prompts=[dict(path=p,sha256=sha(ROOT/p)) for p in prompts],
 edit_input=dict(path=v1.relative_to(ROOT).as_posix(),sha256=sha(v1)),
 v1=dict(path=v1.relative_to(ROOT).as_posix(),sha256=sha(v1),source_path=r'C:\Users\83912\.codex\generated_images\01a128a4-4af2-7493-b41e-9b162279a019\exec-5df7de88-0bd9-498a-8847-8772a9a7b761.png',review='Viewed: six distinct locations; F initially lacked a clearly empty berth; retained as earlier candidate.'),
 note='design/12_美术参考/布林任务场所概念与台本映射.md',
 review='Viewed generated v2: six labelled scenes; F has distinct empty water berth, separate occupied skiff berth and land access. Doors, geometry, small marks and object identities still require production correction.',
 runtimeVerified=False)
(ROOT/'research/brynn-task-space-art-s77.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/record['note'];t=p.read_text(encoding='utf-8')
t=t.replace('城市概念/BRY-任务场所-v1.png','城市概念/BRY-任务场所-v2.png')
t=t.replace('目视检查待生成结果保存后记录。','已查看v1与v2：六处场所可区分，标签A—F清晰。v1的泊位被船占据，v2仅针对F补出空泊位与另侧停船；v1保留作修订对照。小刻痕、扣样、两扇返街门及实际水位不据画面认定已完成。')
p.write_text(t,encoding='utf-8')
rule='\n<!-- CITY-TASK-ART-S77:BEGIN -->\n2026-10-12 S77：布林六处任务场所概念见design/12_美术参考/布林任务场所概念与台本映射.md，输出v1/v2与完整提示词、输入/输出哈希见research/brynn-task-space-art-s77.json。v2定向修改F空泊位，旧稿保留；A—F非任务顺序，图不定官方地理、NPC身份、门数、碰撞或库存。不覆盖十五城总览，不修改游戏包。后续修改按文字空间/台本核验并更新图文关联。\n<!-- CITY-TASK-ART-S77:END -->\n'
for p in [ROOT/'CHANGELOG.md',ROOT/'design/AGENTS.md',ROOT/'CHANGELOG.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-TASK-ART-S77:BEGIN -->.*?<!-- CITY-TASK-ART-S77:END -->\n','',t,flags=re.S)
 p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(output=record['output'],sha256=record['sha256'],dimensions=record['dimensions'],status='draft'),ensure_ascii=False))
