from pathlib import Path
from PIL import Image
import json, hashlib, base64, numpy as np, shutil

ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'Assets/EnemyDesigns/20261013/first_six'
BRIEF=json.loads((BASE/'action_continuation_brief_v1.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(path,data):
 with path.open('x') as f: json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
for item in BRIEF['items']:
 if item['id'] not in ['003','004']: continue
 d=ROOT/item['planned_generation']['output_directory_if_later_executed']
 role=item['role'];pose=item['proposed_keypose']['pose_id'];stem=f'{role}_{pose}'
 raw=d/f'{stem}_raw_v1.png';selected=d/f'{stem}_transparent_v1.png'
 ret=json.loads((d/'tool_return_v1.json').read_text());args=json.loads((d/'tool_arguments_v1.json').read_text())
 assert args['prompt']==(d/'prompt_v1.txt').read_text()==item['planned_generation']['prompt']
 assert base64.b64decode(ret['image_url'].split(',',1)[1])==raw.read_bytes()
 r=np.array(Image.open(raw).convert('RGBA'));s=np.array(Image.open(selected).convert('RGBA'))
 assert np.array_equal(r[:,:,3],s[:,:,3]);assert np.array_equal(r[:,:,:3][r[:,:,3]>0],s[:,:,:3][r[:,:,3]>0])
 thresholds={}
 for t in [0,4,8,16,64,127,254]:
  yy,xx=np.where(s[:,:,3]>t)
  thresholds[str(t)]={'count':len(xx),'bbox':None if not len(xx) else [int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]}
 inputs=[]
 for f,ref in zip(args['referenced_image_paths'],item['planned_generation']['reference_order']):
  p=Path(f);assert sha(p)==ref['sha256'];inputs.append({'path':f,'sha256':sha(p),'role':ref['path']})
 outputs=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in [raw,selected,d/'review_light_v1.png',d/'review_dark_v1.png',d/'tool_arguments_v1.json',d/'tool_return_v1.json',d/'prompt_v1.txt']]
 write_new(d/'generation_record_v1.json',{'tool':'builtin image_gen.imagegen','call_version':'v1','generation_calls':1,'hard_error_revisions_used':0,'complete_original_return':'tool_return_v1.json','actual_arguments':'tool_arguments_v1.json','prompt_saved_before_call':True,'actual_tool_arguments_prompt_matches_saved_prompt':True,'raw_exactly_equals_tool_return_decoded_png':True,'inputs':inputs,'outputs':outputs,'successful_result':True,'output_hint':ret['output_hint']})
 write_new(d/'alpha_QA_v1.json',{'size':[int(s.shape[1]),int(s.shape[0])],'mode':'RGBA','all_nonzero_alpha_retained':True,'alpha_changed_pixels':0,'visible_rgb_changed_pixels':0,'hidden_rgb_zeroed_pixels':int(np.sum((r[:,:,3]==0)&np.any(r[:,:,:3]!=s[:,:,:3],axis=2))),'alpha_threshold_stats':thresholds,'correct_composite_method':'Pillow RGBA alpha_composite onto opaque backgrounds; no alpha mask double multiplication','actually_viewed':['raw_v1','transparent_v1','review_light_v1','review_dark_v1','comparison_board'],'visible_glow':False,'interpretation':'Raw RGB appearance is not the visible RGBA composite. For 004, alpha 1–4 low-opacity background traces can touch canvas edges; the actual visible tail and fragments have margins, and all partial alpha is preserved.' if item['id']=='004' else 'Raw RGB brown halo is under alpha=0 and absent in correct RGBA composite.'})
 findings = ([
 '同一瘦斜塌肩死灵、歪头与稀疏暗发、灰黄皮肉和旧麻残衣、腰绳、破裤、绑腿裸趾保持。',
 '原画面左臂肩向前、肘角打开，手指收成未闭合的空抓；原画面右臂低垂，未加第二抬臂。',
 '前膝与前足载重，后脚跟抬起而趾接触的概念可读；未新增受害者、抓持物或鲜血。',
 '相比slow_reach不仅指形变化；没有脚底／身高配准或时间轨迹验收。'
 ] if item['id']=='003' else [
 '同一尖兜帽、冷青窄面、短肩披与唯一露骨感手保持；未出现实脚、武器或新身份。',
 '露手回到下胸，袖肘折起、手指朝下；手指下方暗缝可读，原图未作手／胸几何修补。',
 '两长一短主碎尾与孔洞、小碎片仍在；尾留右后滞后弧，宽度比前漂收束。',
 '保留全部有意半透明，实际浅深合成无额外可见雾晕；头身与尾尖没有runtime锚点验证。'
 ])
 write_new(d/'author_QA_v1.json',{'status':'author_concept_pass_pending_independent_final','actually_viewed':['mother','both_selected_adjacent_poses','raw_v1','transparent_v1','review_light_v1','review_dark_v1','Chinese_comparison_board'],'findings':findings,'independent_review_required':True,'revision_budget_used':0,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False,'common_origin_verified':False})
 shutil.copy2(Path(__file__),d/'archive_execution_and_qa.py')
 print(item['id'],'evidence and author QA saved')
