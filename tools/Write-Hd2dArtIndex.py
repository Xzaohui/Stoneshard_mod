"""Write the scene-art library entrance from current verified batch counts."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'
def main():
    s=json.loads((P/'artwork-state.json').read_text(encoding='utf-8'))
    groups=[('BRY-outskirts-v1','布林卫星聚落、低潮侧泊与六处续篇','batches/BRY-outskirts-v1/preview.html','batches/BRY-outskirts-v1/previews/bryo_x11_work_browser.png','batches/BRY-outskirts-v1/exports/HD2D-BRY-Outskirts-v1.zip'),
      ('BRY-core-v1','布林公告廊、老楼、船工街与夜会馆','batches/BRY-core-v1/preview.html','batches/BRY-core-v1/previews/bry_d01_front_browser.png','batches/BRY-core-v1/exports/HD2D-BRY-Core-v1.zip'),
      ('R06-highland-v1','修院山地、回声前室与残光双环','batches/R06-highland-v1/preview.html','batches/R06-highland-v1/previews/r06_echo_front_browser.png','batches/R06-highland-v1/exports/HD2D-R06-Highland-v1.zip'),
      ('R05-basin-v1','灰烬湿地、疫所与沉水档案井','batches/R05-basin-v1/preview.html','batches/R05-basin-v1/previews/r05_well_lower_default_browser.png','batches/R05-basin-v1/exports/HD2D-R05-Basin-v1.zip'),
      ('R04-pass-v1','柏石关、军需地窖与退役驿道','batches/R04-pass-v1/preview.html','batches/R04-pass-v1/previews/r04_cellar_main_browser.png','batches/R04-pass-v1/exports/HD2D-R04-Pass-v1.zip'),
      ('R01-camp-canal-v2','灰堤与旧渠 · 观察道具补画v2','batches/R01-camp-canal-v2/preview.html','batches/R01-camp-canal-v2/previews/r01_camp.png','batches/R01-camp-canal-v2/exports/HD2D-R01-Camp-Canal-v2.zip'),
      ('R02-river-v2','渡口与税栈 · 井牌及回访道具v2','batches/R02-river-v2/preview.html','batches/R02-river-v2/previews/r02_tax_main.png','batches/R02-river-v2/exports/HD2D-R02-River-v2.zip'),
      ('R03-maen-v1','曼恩边地、迁藏书库与试验庭','batches/R03-maen-v1/preview.html','batches/R03-maen-v1/previews/r03_court.png','batches/R03-maen-v1/exports/HD2D-R03-Maen-v1.zip'),
      ('R02-river-v1','丹布里西路、渡口与断桥税栈','batches/R02-river-v1/preview.html','batches/R02-river-v1/previews/r02_tax_main.png','batches/R02-river-v1/exports/HD2D-R02-River-v1.zip'),
      ('R01-streets-v1','港街、听审棚、工坊与盐路','batches/R01-streets-v1/preview.html','batches/R01-streets-v1/previews/r01_hearing.png','batches/R01-streets-v1/exports/HD2D-R01-Streets-v1.zip'),
      ('R01-camp-canal-v1','灰堤工营与旧渠两层','batches/R01-camp-canal-v1/preview.html','batches/R01-camp-canal-v1/previews/r01_camp.png','batches/R01-camp-canal-v1/exports/HD2D-R01-Camp-Canal-v1.zip'),
      ('N1','无钟之夜 · 现有三个场景','preview.html','previews/r_eao_n1_yard__preview.png','exports/HD2D-N1-v1.zip')]
    cards=[]
    for key,title,preview,thumb,package in groups:
        if key not in s['batches']:continue
        b=s['batches'][key]
        for rel in [preview,thumb,package]:assert (P/rel).is_file(),rel
        cards.append(f'<article><a href="{preview}"><img src="{thumb}" alt="{title}"></a><div><h2>{title}</h2><p>{b["production_pngs"]}张生产PNG · 可导入分层素材</p><a class="button" href="{preview}">打开空间预览</a> <a href="{package}" download>下载素材包</a></div></article>')
    out=f'''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>紫色晶石 · HD-2D场景素材库</title><style>*{{box-sizing:border-box}}body{{background:#151a1c;color:#e4ded1;font:16px "Microsoft YaHei",sans-serif;margin:0}}main{{max-width:1180px;margin:auto;padding:38px 30px}}h1{{font-size:30px;margin:0 0 12px}}p{{line-height:1.7;color:#bcb7aa}}.stats{{display:flex;gap:40px;margin:28px 0;padding:20px 0;border-top:1px solid #48504d;border-bottom:1px solid #48504d}}.stats strong{{display:block;font-size:30px;color:#d6b879}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px}}article{{background:#202728;border:1px solid #48504d;border-radius:7px;overflow:hidden}}article img{{width:100%;height:220px;object-fit:contain;image-rendering:pixelated;background:#101619}}article div{{padding:20px}}h2{{font-size:20px;line-height:1.5;margin:0}}a{{color:#d6b879;text-underline-offset:3px}}.button{{display:inline-block;background:#3c453e;border:1px solid #777961;border-radius:4px;padding:9px;text-decoration:none;margin:8px 8px 8px 0}}footer{{margin-top:32px;border-top:1px solid #48504d;padding:18px 0;color:#aab2ad;font-size:14px}}</style><main><h1>紫色晶石 · HD-2D场景素材库</h1><p>平面地图、建筑外观与室内工作空间。原稿、分层PNG、脚底原点及导入说明随各批素材保留。</p><div class="stats"><div><strong>{s['fulfilled_view_slots']} / {s['initial_view_slots']}</strong>已制作视图</div><div><strong>{s['production_pngs']}</strong>生产PNG</div><div><strong>{s['remaining_view_slots']}</strong>待制作视图</div></div><div class="cards">{''.join(cards)}</div><footer>当前完成N1和R01清单视图。R01素材通过静态验收，原生房间装配仍待测试。<br>各批PNG数量包含分层、独立物件及检查合成图，和视图数分别统计。<br><a href="inventory.csv">全部制作清单</a> · <a href="artwork-state.json">当前进度</a></footer></main></html>'''
    covered='、'.join(['N1',*sorted({k.split('-')[0] for k in s['batches'] if k!='N1'})])
    out=out.replace('当前完成N1和R01清单视图。R01素材通过静态验收，原生房间装配仍待测试。',f'已制作视图覆盖{covered}；各批可导入素材通过静态验收，新增场景的原生房间装配仍待测试。')
    for key,title,preview,thumb,package in groups:
        b=s['batches'].get(key,{})
        if b.get('needs_revalidation_view_slots',0):out=out.replace(f'<h2>{title}</h2>',f'<h2>{title}</h2><p style="color:#e5bd83">{b["needs_revalidation_view_slots"]}项视图待同步当前台本新增道具</p>')
    out=out.replace('已制作视图</div>','已匹配当前台本的视图</div>').replace('待制作视图</div>','待制作或复核视图</div>')
    out=out.replace('全部制作清单</a>', '全部制作清单</a> · <a href="source-sync-queue.json">台本更新与待补画物件</a>')
    out=out.replace('<div class="cards">',f'<p>此前已导出{s.get("exported_view_slots",s["fulfilled_view_slots"])}项视图；其中{s.get("needs_revalidation_view_slots",0)}项因台本更新待补画/复核。尚未绘制{s.get("not_drawn_view_slots",s["remaining_view_slots"])}项。</p><div class="cards">')
    for key,b in s.get('work_in_progress_batches',{}).items():
        preview=b['path']+'/'+b['preview']
        if (P/preview).is_file():out=out.replace('<footer>',f'<p style="margin-top:28px">制作中：<a href="{preview}">{html.escape(key)}建筑与地面预览</a> · {b["partial_pngs"]}张已拆分PNG · {b["planned_view_slots"]}项地图视图尚未完成，未计入以上进度。</p><footer>')
    (P/'index.html').write_text(out,encoding='utf-8');print(json.dumps(dict(path=str(P/'index.html'),view_slots=s['fulfilled_view_slots'],pngs=s['production_pngs']),ensure_ascii=False))
if __name__=='__main__':main()
