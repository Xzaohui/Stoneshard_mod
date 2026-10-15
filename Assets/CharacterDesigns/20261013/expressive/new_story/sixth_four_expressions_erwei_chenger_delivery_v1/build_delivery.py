from pathlib import Path
from PIL import Image
import json,hashlib,shutil,zipfile,datetime
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
ROOT=HERE.parents[5]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
frozen={};attachments=[];archive_inventory=[];board_inputs=[]
for slug in ['erwei','chenger']:
    src=BASE/slug/'expressions_v1'
    manifest=json.loads((src/'manifest.json').read_text())
    qa=json.loads((src/'QA-independent.json').read_text())
    rawqa=json.loads((src/'QA-independent-raw-visual.json').read_text())
    assert qa['status']=='two_expressions_passed_independent_review'
    assert rawqa['status']=='two_expressions_passed_independent_review'
    assert not qa['integrity_checks']['mismatches']
    assert all(qa['presentation_verdict'].values())
    assert qa['manifest_binding']['sha256']==sha(src/'manifest.json')
    assert qa['raw_review_binding']['sha256']==sha(src/'QA-independent-raw-visual.json')
    for row in manifest['files']:
        assert sha(src/row['path'])==row['sha256']
        assert (src/row['path']).stat().st_size==row['bytes']
    final=src/'FINAL_STATUS.json'
    assert not final.exists(),str(final)
    status={'schema_version':1,'status':'frozen_pass_for_concept_expression_artwork','character':slug,'name':manifest['name'],'canonical_id':manifest['canonical_id'],'frozen_utc':now(),'writer':'producer','manifest_binding':{'path':'manifest.json','sha256':sha(src/'manifest.json')},'independent_reviews':[{'path':n,'sha256':sha(src/n)} for n in ['QA-independent-raw-visual.json','QA-independent.json']],'selected':[{'key':e['key'],'label_zh':e['label_zh'],'path':e['selected'],'sha256':e['selected_sha256']}for e in manifest['expressions']],'files_frozen':[{'path':str(p.relative_to(src)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(src.rglob('*'))if p.is_file()],'initial_calls':2,'revisions_used':0,'hard_error_revision_needed':False,'independent_review_passed':True,'user_approval_claimed':False,'runtime_integrated':False,'not_verified':['native_pixel_grid','part/frame/mask/origin','equipment_compatibility','animation_continuity','runtime'],'freeze_rule':'No source changes after this status. Delivery packaging is read-only against this frozen directory. Manifest remains its reviewed historical candidate hash.'}
    write(final,status)
    frozen[slug]={str(p.relative_to(src)):sha(p) for p in sorted(src.rglob('*'))if p.is_file()}
    for e in manifest['expressions']:
        source=src/e['selected']; dest=HERE/(e['key']+'_transparent.png');shutil.copyfile(source,dest);assert sha(dest)==e['selected_sha256']
        attachments.append({'file':dest.name,'kind':'selected_transparent','character':slug,'key':e['key'],'label_zh':e['label_zh'],'source':str(source.relative_to(ROOT)),'bytes':dest.stat().st_size,'sha256':sha(dest)})
    dest=HERE/(slug+'_expressions_v1_complete_source.zip')
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
        for rel in frozen[slug]:z.write(src/rel,arcname=slug+'/expressions_v1/'+rel)
    assert dest.stat().st_size<18*1024*1024
    members=[]
    with zipfile.ZipFile(dest)as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(frozen[slug])
        for rel,h in frozen[slug].items():
            name=slug+'/expressions_v1/'+rel;b=z.read(name);assert hashlib.sha256(b).hexdigest()==h
            members.append({'member':name,'bytes':len(b),'sha256':h})
    archive_inventory.append({'file':dest.name,'sha256':sha(dest),'member_count':len(members),'members':members})
    attachments.append({'file':dest.name,'kind':'complete_source_archive','character':slug,'bytes':dest.stat().st_size,'sha256':sha(dest),'member_count':len(members),'all_members_sha_verified':True})
for variant in ['light','dark']:
    for slug in ['erwei','chenger']:
        p=BASE/slug/'expressions_v1/review'/f'{slug}_expressions_{variant}_board.png'
        board_inputs.append({'source':str(p.relative_to(ROOT)),'sha256':sha(p)})
board=Image.new('RGB',(2304,2040))
for j,variant in enumerate(['light','dark']):
    for i,slug in enumerate(['erwei','chenger']):
        p=BASE/slug/'expressions_v1/review'/f'{slug}_expressions_{variant}_board.png'
        im=Image.open(p).convert('RGB').resize((1152,1020),Image.Resampling.NEAREST)
        board.paste(im,(i*1152,j*1020))
dest=HERE/'珥薇_埕珥_四种表情_浅深对照.png';board.save(dest)
attachments.append({'file':dest.name,'kind':'light_dark_contact_sheet','bytes':dest.stat().st_size,'sha256':sha(dest),'dimensions':[2304,2040],'source_boards':board_inputs,'processing':'Only nearest-neighbor layout of reviewed boards. No generated-art edits.'})
assert len(attachments)==7
for slug,mapping in frozen.items():
    src=BASE/slug/'expressions_v1'
    assert mapping=={str(p.relative_to(src)):sha(p)for p in sorted(src.rglob('*'))if p.is_file()}
write(HERE/'archive_inventory.json',{'archives':archive_inventory})
write(HERE/'delivery.json',{'schema_version':1,'status':'prepared_not_uploaded','created_utc':now(),'characters':['erwei','chenger'],'selected_count':4,'initial_generation_calls':4,'revisions_used':0,'attachment_count':7,'attachments':attachments,'source_freeze_files':{slug:{'path':str((BASE/slug/'expressions_v1/FINAL_STATUS.json').relative_to(ROOT)),'sha256':sha(BASE/slug/'expressions_v1/FINAL_STATUS.json')}for slug in frozen},'not_claimed':['user_approval','game_integration','runtime'],'archive_inventory_sha256':sha(HERE/'archive_inventory.json')})
(HERE/'INDEX.md').write_text('# 珥薇与埕珥｜第六批四种表情\n\n共4张透明选稿、1张浅深对照板、2个完整源包。珥薇：谈路莞尔、敛笑拒托。埕珥：顾灯忧警、守口不下。\n\n源包保留实际prompt、每次工具调用、全部raw、母图及来源快照、作者与独立审查、manifest及冻结状态。每张首稿一次，未修订。\n\n这是可逆表情概念，不是任务顺序结局，不证明修桥、付款、托管、遗物认领、余烬归属或游戏运行。\n\n交付文件路径、SHA与源包逐成员核对见delivery.json、archive_inventory.json及FINAL_DELIVERY_QA.json。\n')
write(HERE/'FINAL_DELIVERY_QA.json',{'schema_version':1,'status':'mechanical_checks_pass_pending_visual_contact_sheet_review','checked_utc':now(),'selected_sha_matches_frozen_sources':True,'all_source_manifest_entries_verified':54,'source_directories_unchanged_during_packaging':True,'archive_count':2,'archive_member_count':sum(x['member_count']for x in archive_inventory),'zip_crc_and_member_sha_all_pass':True,'archives_each_below_18_MiB':True,'all_7_attachment_paths_exist':True,'delivery_json_sha256':sha(HERE/'delivery.json'),'archive_inventory_sha256':sha(HERE/'archive_inventory.json'),'contact_sheet':{'file':dest.name,'sha256':sha(dest),'actual_viewed':False},'not_uploaded':True,'git_not_run':True})
print(json.dumps({'status':'packaged_pending_contact_sheet_view','attachments':[{'file':a['file'],'bytes':a['bytes'],'sha256':a['sha256']}for a in attachments],'members':sum(x['member_count']for x in archive_inventory)},ensure_ascii=False,indent=2))
