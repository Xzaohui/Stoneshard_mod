"""Shared helper: keep registry blocks owned by other phases when a generator
rewrites a note wholesale. Import and wrap the writer's note text before writing."""
from pathlib import Path
import re
BLOCK = re.compile(r'<!--\s*([A-Za-z0-9-]+):BEGIN\s*-->.*?<!--\s*\1:END\s*-->', re.S)
def extract(text):
    out = []; seen = set()
    for m in BLOCK.finditer(text):
        key = m.group(1)
        if key in seen: continue
        seen.add(key); out.append((key, m.group(0)))
    return out
def preserve_foreign(vault, rel, text):
    p = Path(vault) / rel
    if not p.exists(): return text
    old = p.read_text(encoding='utf-8-sig')
    blocks = [b for k, b in extract(old) if f'<!-- {k}:BEGIN -->' not in text]
    return text.rstrip() + '\n\n' + '\n\n'.join(blocks) + '\n' if blocks else text
