"""Attach reviewed task-art proposals without changing task state or old art choices."""
from pathlib import Path
import json,re,os

def add_task_art(root,relative,text):
    manifests=[]
    for filename in ['city-task-art-20261012.json','shore-vine-task-art-20261012.json']:
        path=root/'research'/filename
        if path.exists():manifests.append(json.loads(path.read_text(encoding='utf-8')))
    for board in [b for m in manifests for b in m['boards']]:
        if 'design/'+relative not in board['linked_notes']:continue
        marker=board.get('link_marker','CITY-TASK-ART-20261012')
        start='<!-- '+marker+':BEGIN -->';end='<!-- '+marker+':END -->'
        image=Path(os.path.relpath(root/board['selected'],root/'design'/Path(relative).parent)).as_posix()
        body=f"{start}\n## 任务场所概念图（2026-10-12）\n\n![{board['name']}六处任务场所]({image})\n\n[[{Path(board['note']).stem}]]说明A—F的任务、空间与制作约束。面板不是任务顺序或官方相邻关系；画中人物、库存和门仅为原创构图，未实现交互。\n{end}\n"
        if start in text:return re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:body,text,flags=re.S)
        return text.rstrip()+'\n\n'+body
    return text
