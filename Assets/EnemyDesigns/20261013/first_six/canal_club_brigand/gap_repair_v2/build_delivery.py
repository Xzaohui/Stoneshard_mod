from pathlib import Path
import json,base64,hashlib,shutil,zipfile
from PIL import Image,ImageDraw
p=Path(__file__).parent;b=p.parent;root=b.parents[4]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def write(n,d):(p/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
refs=[('mother',b/'idle_v1/canal_club_brigand_transparent.png'),('ready_selected',b/'action_v1/club_compact_ready/canal_club_brigand_club_compact_ready_transparent.png'),('recover_selected',b/'action_v1/club_controlled_recover/canal_club_brigand_club_controlled_recover_transparent.png')]
for label,q in refs:shutil.copy2(q,p/'sources'/f'{label}.png')
shutil.copy2(b.parent/'action_continuation_brief_v1.json',p/'sources/action_continuation_brief_v1.json')
shutil.copy2(b/'action_continuation_v1/FINAL_STATUS.json',p/'sources/previous_FINAL_STATUS.json')
checks=[]
for v in [1,2]:
 q=p/f'raw_v{v}.png';d=json.load(open(p/f'tool_return_v{v}.full.json'));payload=base64.b64decode(d['image_url'].split(',',1)[1]);im=Image.open(q);a=im.getchannel('A');hi=a.point(lambda x:255 if x>=128 else 0)
 checks.append({'version':v,'raw_sha256':sha(q),'payload_sha256':hashlib.sha256(payload).hexdigest(),'payload_matches_raw':payload==q.read_bytes(),'bytes':q.stat().st_size,'mode':im.mode,'size':im.size,'alpha_bbox_all':a.getbbox(),'alpha_bbox_128':hi.getbbox(),'transparent_pixels':a.histogram()[0],'opaque_pixels':a.histogram()[255],'partial_alpha_pixels':sum(a.histogram()[1:255]),'raw_preserved':True,'alpha_cleaning_performed':False})
 shutil.copy2(q,p/f'002_midarc_candidate_v{v}_FAILED.png')
write('raw_payload_integrity.json',checks)
items=refs+[('previous_failed_v2',b/'action_continuation_v1/club_downswing_midarc/canal_club_brigand_club_downswing_midarc_raw_v2.png'),('new_v1_FAILED',p/'raw_v1.png'),('new_v2_FAILED',p/'raw_v2.png')]
board=Image.new('RGB',(1920,1510),(238,232,217));dr=ImageDraw.Draw(board)
for i,(label,q) in enumerate(items):
 x=(i%3)*640;y=(i//3)*755;dr.text((x+16,y+12),label,fill=(20,20,20));im=Image.open(q).convert('RGBA');im.thumbnail((600,690),Image.Resampling.NEAREST);board.paste(im,(x+(640-im.width)//2,y+50),im)
board.save(p/'mother_selected_new_comparison.png')
write('author_QA_v2.json',{'status':'failed_no_selected_budget_exhausted','actually_viewed':['review_v2_light.png','review_v2_dark.png'],'observations':['棍轴已向左下，持棍前臂打开；但棍头中心约y640，与腰带同高，底部约y695已低于腰带；不满足腰以上胸腹中弧。','一根短粗钝木棍，一道灰铁箍；单手抓握连通，空手未触棍。','双靴轮廓和鞋底完整，矮壮成年及衣服左右标志保留。','本轮首稿也不选：棍头略高于拳，尚未到下挥角度。','只对原始输出作透明底合成审查；未程序修改身体、武器或补绘。'],'continuous_animation_verified':False,'runtimeVerified':False})
write('FINAL_STATUS.json',{'role':'002 canal_club_brigand','round':'gap_repair_v2','status':'failed_no_selected_budget_exhausted','generation_calls':2,'first_drafts':1,'hard_error_revisions':1,'selected_output':None,'candidate_files':['002_midarc_candidate_v1_FAILED.png','002_midarc_candidate_v2_FAILED.png'],'reason':'v1棍头高于拳；v2棍头降至腰带高度及以下，均未满足完整下挥胸腹中弧。','independent_review':'Parent coordinates separately; author does not write independent QA.','runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False,'all_previous_assets_preserved':True})
(p/'README.md').write_text('# 002短棍下挥中段：新轮补缺失败研究包\n\n本轮真实生成2次，首稿＋唯一硬错修订。两稿均不选，不能计作已补齐动作。首稿棍头高于拳，修订稿棍头又落至腰带高度及以下。独立PNG均明确标为FAILED。\n\n包含原始RGBA、完整工具返回payload、实际参数、精确提示词、浅深底审查、母图／旧选稿／新稿对比和旧失败记录。未覆盖旧索引或旧作品；未验证连续动画、配准、碰撞或游戏落地。\n')
write('source_manifest.json',[{'path':str(q.relative_to(p)),'bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted((p/'sources').rglob('*')) if q.is_file()])
