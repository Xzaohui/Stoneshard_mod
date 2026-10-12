"""Record the single selected S75 diagram viewed this turn; never imply all SVGs were viewed."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];target=ROOT/'research/city-space-visual-review.json'
svg='design/12_美术参考/城市示意/BRY-layout.svg';png='artifacts/city-visual-review/BRY-layout-s75-selected.png'
data=dict(date='2026-10-12',reviewer='Codex via view_image',render_tool='Edge headless with task-local profile',
 source=svg,source_sha256=hashlib.sha256((ROOT/svg).read_bytes()).hexdigest(),screenshot=png,
 screenshot_sha256=hashlib.sha256((ROOT/png).read_bytes()).hexdigest(),
 inspected=['Full board and Chinese labels visible without clipping.','Independent D-to-B and satellite-scene return curves do not pass through middle node boxes.','Selected curve placement avoids the title and legend.'],
 limits='Only BRY was rendered and visually inspected this turn; all other SVGs receive XML/path checks. This topology image is not a scaled or playable map.')
if target.exists() and json.loads(target.read_text(encoding='utf-8'))!=data:raise SystemExit('Preserve earlier review; record a new version instead.')
target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Selected BRY diagram view and exact hashes recorded.')
