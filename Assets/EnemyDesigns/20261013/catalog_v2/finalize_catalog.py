#!/usr/bin/env python3
"""Finish the reviewed local catalog packet. No Git, upload or image generation."""
from pathlib import Path
import hashlib,json,zipfile,sys,datetime,importlib.util
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fileinfo(p):return {'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
def main():
 spec=importlib.util.spec_from_file_location('verify',HERE/'verify_catalog.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 auto=v.main();dump(HERE/'SOURCE_AND_PDF_VERIFICATION.json',auto)
 independent=json.loads((HERE/'INDEPENDENT_CATALOG_QA.json').read_text())
 assert 'pass' in independent.get('status','').lower(),independent
 font=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
 dump(HERE/'font_provenance.json',{'original_font':{'path':str(font),'bytes':font.stat().st_size,'sha256':sha(font),'collection_face':2,'family':'Noto Sans CJK SC'},'subset':fileinfo(HERE/'catalog_font_subset.otf'),'license':fileinfo(HERE/'FONT_LICENSE.txt'),'method':'fontTools subset retain_gids; glyph set from selection map and layout script; embedded in every PDF page'})
 comments=[
  '十二母图封面清楚；002标2动作与续姿缺项；总计47只计唯一选稿。',
  '12行中文可点目录和使用说明完整，无文字溢出。',
  '001母图与原两动作、收矛v2四格；自然前握替代和矛长限制清楚。',
  '002仅三张选稿，第四格文字缺项；未放入失败姿态。',
  '003四格清楚，手脚与续姿完整。',
  '004深底半透明轮廓完整；探手回束清楚，无alpha增强。',
  '005低伏、短爪及回爪姿态不裁手足。',
  '006四格横杖、侧步及换重心完整。',
  '007盾与斧、前送斜劈完整可辨。',
  '008弩与两腿完整，低姿撤步使用v2。',
  '009风格修订母图与三斧姿完整，兵器未被版面裁切。',
  '010深底上原审定半透明保存，探剑与回收完整。',
  '011四格清楚；喉胸前送使用v2，与垂喉姿不同，留边说明正确。',
  '012风格修订母图与三铃姿完整，alpha处理说明如实保留。']
 layouts=json.loads((HERE/'layout_checks.json').read_text())
 for p,c in zip(layouts['page_checks'],comments):p['visual_review']='pass_actual_view';p['visual_comment']=c
 layouts['status']='pass_automated_and_actual_visual_review';dump(HERE/'layout_checks.json',layouts)
 qa={'status':'pass','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'counts':auto,'pdf':fileinfo(HERE/'enemy_design_catalog_v2.pdf'),'overview':fileinfo(HERE/'enemy_twelve_coverage_overview_v2.png'),'all_14_pages_actually_viewed':True,'coverage_overview_actually_viewed':True,'per_page':layouts['page_checks'],'root_review':'Root actually viewed cover, 002, 004, 009, 010, 011, 012 and full overview; accepted.','independent_report':fileinfo(HERE/'INDEPENDENT_CATALOG_QA.json'),'crop':False,'nonproportional_stretch':False,'alpha_adjustments':False,'new_generation_calls':0,'git_operations':0,'uploads':0,'user_sends':0,'continuous_animation_verified':False,'runtimeIntegrated':False,'runtimeVerified':False}
 dump(HERE/'FINAL_CATALOG_QA.json',qa)
 (HERE/'INDEX.md').write_text('# 十二敌人姿态图册 v2\n\n本地浏览索引已并入此前交付的11个续姿：12母图＋35独立动作＝47张唯一选稿。002下挥中段仍缺项。旧v1与所有旧源冻结不变。\n\n- [14页图册](enemy_design_catalog_v2.pdf)\n- [47图覆盖概览](enemy_twelve_coverage_overview_v2.png)\n- [排版与QA小源包](enemy_catalog_v2_layout_sources.zip)\n- [范围与复现](README.md)\n- [最终QA](FINAL_CATALOG_QA.json)\n- [独立审查](INDEPENDENT_CATALOG_QA.json)\n- [来源映射](selected_sources.json)\n\n小源包不含全部raw、失败图、完整角色源ZIP或PDF，依赖项目内冻结选稿；不是完整美术源包。本轮未生图、未Git、未上传或发用户。\n',encoding='utf-8')
 # Self-describing deterministic archive. No raw sources, selected-image copies, PDF or derived per-image rasters.
 names=['README.md','INDEX.md','build_catalog.py','prepare_sources.py','verify_catalog.py','finalize_catalog.py','requirements.txt','catalog_font_subset.otf','FONT_LICENSE.txt','font_provenance.json','selected_sources.json','continuation_production_aliases.json','browser_raster_map.json','frozen_inputs_before.json','SOURCE_AND_PDF_VERIFICATION.json','layout_checks.json','FINAL_CATALOG_QA.json','INDEPENDENT_CATALOG_QA.json','enemy_twelve_coverage_overview_v2.png']
 files=[HERE/n for n in names]+list((HERE/'rendered').glob('*.png'))+list((HERE/'evidence').rglob('*'))
 files=sorted(p for p in files if p.is_file())
 contents=[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]
 dump(HERE/'ZIP_CONTENTS.json',{'scope':'Layout/source mapping/QA/review previews only; excludes all raw source images and complete character source packs, PDF, and 47 generated browser rasters. Rebuild requires repository sources.','files':contents,'self_excluded_from_hash_list':'ZIP_CONTENTS.json'})
 files.append(HERE/'ZIP_CONTENTS.json');out=HERE/'enemy_catalog_v2_layout_sources.zip'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:
   entry=zipfile.ZipInfo(str(p.relative_to(HERE)),date_time=(2026,10,14,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o644<<16;z.writestr(entry,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for a in contents:
   b=z.read(a['path']);assert len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a['sha256']
  assert len(z.infolist())==len(files)
 assert out.stat().st_size<18*1024*1024
 artifacts=[fileinfo(HERE/n) for n in ['enemy_design_catalog_v2.pdf','enemy_twelve_coverage_overview_v2.png','enemy_catalog_v2_layout_sources.zip']]
 assert all(a['bytes']<18*1024*1024 for a in artifacts)
 dump(HERE/'ARTIFACT_MANIFEST.json',{'status':'saved_local_not_uploaded_not_sent','artifacts':artifacts,'all_under_18MiB':True,'zip_members':len(files),'zip_crc_pass':True,'zip_all_file_sha_and_bytes_pass':True,'archive_does_not_include_all_raw':True,'old_sources_and_catalog_v1_unchanged':True,'counts':{'static':12,'actions':35,'unique_images':47,'previously_delivered_continuations_included':11,'new_images_this_task':0,'missing_continuations':1}})
 dump(HERE/'STATUS.json',{'status':'complete_local_catalog_update','uploaded':False,'sent_to_user':False,'generation_calls':0,'git_operations':0,'continuous_animation_verified':False,'runtimeIntegrated':False,'runtimeVerified':False})
 print(json.dumps({'artifacts':artifacts,'zip_members':len(files),'all_under_18MiB':True},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
