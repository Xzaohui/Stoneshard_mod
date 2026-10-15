"""Record independent raw/1x/NN final visual inspection for the B pair."""
from pathlib import Path
from datetime import datetime,timezone
import json
Q=Path(__file__).resolve().parent
for s in ['kewei','luofu']:
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=t['versions'][-1];d=next(x for x in v['derivatives'] if ('_inset_' in x['path'])==(s=='kewei'))
 if s=='kewei':
  visual='整齐侧梳灰发的大块取代细亮丝，短尖胡与防御紧嘴、约50岁下眼袋保持身份。v2小暗眼、大鼻颧面与短颈窄领明显改善；深棕外套和紫内领相符，不演邪恶东家或安全复工结论。'
  boundary='raw alpha>=5右留9px，>=16留11px，>=128留12px，发耳完整。选inset bbox[4,5,72,95]保有真实轮廓和目标余量，非补边。'
  limits=['须部仍留一些细纹与插值观感，仅为粗块风格候选。','NN技术派生候选，未逐像素原生精修、未集成或实机验证。']
 else:
  visual='扎紧白巾、收拢深发、宽方颌扁宽鼻、小暗眼粗眉与务实紧嘴保持30多岁女性身份，明显区别岱里的灰缕卷发和60岁下颊。v2脸面鼻颧较明确，颈段已缩短；选择full而非inset，因full的暗眼与方脸读取更明确。橄榄旧罩衣/暖褐窄肩无新道具或净水结论。'
  boundary='v1右边缘不足已由v2源图重新生成解决：alpha>=5 bbox[22,186,1064,1444]，右留15px；>=16和>=128右留17px，完整头巾结尾可见。full目标bbox[2,13,73,99]右1列/下1行透明，不是真源裁断。不把额外inset解释为修补。'
  limits=['颈与衣区仍比核心多，白巾仍带细条；只作带注候选，不宣称严格最终风格验收。','头巾所占上部较多；没有第三次生成或脚本改脸。','NN技术派生候选，未逐像素原生精修、未集成或实机验证。']
 r={'slug':s,'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'accepted_candidate_with_notes','delivery_eligible':True,'selected_path':d['path'],'selected_sha256':d['sha256'],'reviewed_raw_sha256':v['raw_sha256'],'actual_raw_and_integer_NN_viewed':True,'visual_assessment':visual,'source_boundary_assessment':boundary,'raw_boundary_thresholds':v['raw_boundary_thresholds'],'limitations':limits,'feedback_rounds':1,'successful_generations':2,'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_verified':False}
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('B pair final visual reviews recorded.')
