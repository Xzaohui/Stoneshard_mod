from pathlib import Path
import json, hashlib, shutil, zipfile, datetime

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'Assets/CharacterActions/20261013/new_story').is_dir())
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
source_review=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_second_new_character_actions_20261014.json'
packages=[]
for slug in ['deru','hoer']:
    d=BASE/slug/'noncombat_basics_v1'
    qa=json.loads((d/'QA-independent.json').read_text())
    assert qa['accepted_count']==2 and all(not x['hard_errors'] for x in qa['records'])
    cat=json.loads((d/'asset_catalog.json').read_text())
    for a in cat:
        rec=next(x for x in qa['records'] if x['key']==a['key'])
        assert a['export_sha256']==rec['transparent_sha256']==sha(d/a['export'])
        a['independent_review']='accepted_independent_static_keypose'
    (d/'asset_catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
    author=json.loads((d/'QA-author.json').read_text())
    author['status']='author_pass_and_independent_visual_provenance_pass'
    author['actually_viewed'].append('sources/'+slug+'_expression_board.png')
    author['duplicate_check']='Mother and expression reference boards viewed; two new poses change real hand/prop contact or hip/knee support. Existing expressions not counted as new actions.'
    (d/'QA-author.json').write_text(json.dumps(author,ensure_ascii=False,indent=2)+'\n')
    shutil.copyfile(source_review,d/'sources/independent_action_plan_review.json')
    support=d/'delivery_support';support.mkdir(exist_ok=True)
    shutil.copyfile(HERE/'delivery/deru_hoer_four_actions_light_dark_board.png',support/'deru_hoer_four_actions_light_dark_board.png')
    shutil.copyfile(HERE/'build_board.py',support/'build_board.py')
    (support/'README.md').write_text('共享四姿态浅深板只是比较图，每列上下两格是同一动作，不是新增八帧或连续动画。build_board.py的原执行位置为second_noncombat_deru_hoer_delivery_v1；重建整板须将两个人物完整树都放回原目录，使用同级交付脚本。\n')
    with (d/'README.md').open('a') as f:
        f.write('\n本ZIP保存本人物完整生产树，另一个ZIP保存另一人物完整树；二者都能独立解压，不是分卷压缩。共享四姿态对照板也在delivery_support中。sources内brief与独审计划为原始历史快照，其planned状态不覆盖本次FINAL_STATUS；包内独审保留验包前状态，最终包装复核另由父任务记录。\n')
    status={'schema_version':1,'writer':'draw_deru_hoer_actions','status':'frozen_independent_visual_and_provenance_pass','frozen':True,'frozen_utc':now,'selected_independent_keyposes':2,'initial_generations':2,'hard_error_revisions':1,'revision_budget_exceeded':False,'unselected_raw_retained':True,'complete_original_tool_results_retained':True,'qa_independent':'QA-independent.json','qa_independent_sha256':sha(d/'QA-independent.json'),'selected_assets':[{'key':a['key'],'path':a['export'],'sha256':a['export_sha256']} for a in cat],'scope':'独立静态非战斗动作概念；非连续动画、非装备组合、非runtime或剧情完成证据。','sent':False,'uploaded':False,'git_operations':False,'package_verification':'Author package verification follows in delivery_manifest.json; independent packaging verification external to this frozen tree.'}
    (d/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
    files=[{'path':str(p.relative_to(d)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(d.rglob('*')) if p.is_file() and p.name!='manifest.json']
    manifest={'schema_version':1,'character':slug,'created_utc':now,'scope':'Complete character production tree; manifest self excluded to avoid circular hash.','accepted_independent_keyposes':2,'files':files}
    (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    out=HERE/'delivery'/f'{slug}_complete_source_v1.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(d.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(ROOT)))
    assert out.stat().st_size < 18*1024*1024
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        names=set(z.namelist()); disk=[p for p in d.rglob('*') if p.is_file()]
        assert names=={str(p.relative_to(ROOT)) for p in disk}
        for p in disk:assert hashlib.sha256(z.read(str(p.relative_to(ROOT)))).hexdigest()==sha(p)
    packages.append({'character':slug,'path':str(out.relative_to(HERE)),'bytes':out.stat().st_size,'sha256':sha(out),'complete_source_tree':str(d.relative_to(ROOT)),'files':len(disk),'crc_pass':True,'every_archived_byte_matches_frozen_tree':True,'below_18_mib':True,'manifest_sha256':sha(d/'manifest.json'),'final_status_sha256':sha(d/'FINAL_STATUS.json')})
files=[{'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((HERE/'delivery').iterdir()) if p.is_file()]
assert len(files)==7
delivery={'schema_version':1,'frozen_utc':now,'status':'frozen_author_verified_pending_independent_package_check','attachment_count':7,'transparent_pngs':4,'comparison_board':1,'complete_source_zip_packages':2,'accepted_independent_keyposes':4,'initial_generations':4,'hard_error_revisions':2,'runtime_verified':False,'animation':False,'uploaded':False,'sent':False,'files':files,'packages':packages}
(HERE/'delivery_manifest.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(delivery,ensure_ascii=False,indent=2))
