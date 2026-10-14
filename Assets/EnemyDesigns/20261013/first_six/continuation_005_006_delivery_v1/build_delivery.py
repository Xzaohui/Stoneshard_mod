from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, shutil

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'Assets/EnemyDesigns/20261013/first_six'
OUT = Path(__file__).resolve().parent
BRIEF = json.loads((BASE / 'action_continuation_brief_v1.json').read_text())
SCALE = 0.30
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def font(size): return ImageFont.truetype(FONT,size)
def main():
    board = Image.new('RGB',(1620,2160),(247,244,235))
    draw = ImageDraw.Draw(board)
    draw.text((28,15),'005—006 动作补缺｜相邻阶段浅深对照',font=font(33),fill=(31,35,41))
    draw.text((28,61),'仅两张新增独立关键姿势；旧帧只排版。统一 30% 最近邻等比，未作身体同高或精确锚点配准。',font=font(21),fill=(75,79,85))
    entries=[]
    for n,i in enumerate(BRIEF['items'][-2:]):
        role=i['role']; pose=i['proposed_keypose']['pose_id']
        d=ROOT/i['planned_generation']['output_directory_if_later_executed']
        selected=d/f'{role}_{pose}_transparent.png'
        refs=i['planned_generation']['reference_order']
        sequence=[(ROOT/refs[1]['path'],'旧选稿：低伏蓄势'),(ROOT/refs[0]['path'],'旧选稿：短爪前伸 v2'),(selected,'新增：回爪后承重')] if n==0 else [(ROOT/refs[0]['path'],'旧选稿：横杖防备'),(selected,'新增：侧移换重心'),(ROOT/refs[1]['path'],'旧选稿：侧步守势')]
        y=100+n*1010
        draw.text((28,y),f"{i['id']}  {i['working_name']}",font=font(28),fill=(31,35,41))
        for row,(bg,label,fg) in enumerate([((233,229,215),'浅底',(40,43,48)),((35,39,47),'深底',(235,234,225))]):
            yy=y+48+row*468
            for col,(p,caption) in enumerate(sequence):
                x=20+col*535
                draw.rectangle((x,yy,x+523,yy+453),fill=bg)
                draw.text((x+13,yy+8),caption+' · '+label,font=font(21),fill=fg)
                im=Image.open(p).convert('RGBA'); resized=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.NEAREST)
                dest=Image.new('RGBA',(523,411),bg+(255,))
                dest.alpha_composite(resized,((523-resized.width)//2,411-resized.height))
                board.paste(dest.convert('RGB'),(x,yy+42))
                entries.append({'role':role,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'scale':SCALE,'composition':'RGBA alpha_composite; no RGB flattening before composite','background':label})
        # Copy exact selected output; no alpha, color, crop, or anatomy processing.
        shutil.copy2(selected,OUT/selected.name)
        # Snapshot original evidence behind the mother; artwork is unchanged.
        for p in (BASE/role/'idle_v1/sources').rglob('*'):
            if p.is_file():
                target=d/'sources/mother_evidence'/p.relative_to(BASE/role/'idle_v1/sources');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        shutil.copy2(BASE/'action_continuation_sources_v1/source_manifest.json',d/'sources/planning_source_manifest_full.json')
        alpha=Image.open(selected).getchannel('A');hist=alpha.histogram()
        rgba=Image.open(selected).convert('RGBA')
        thresholds={str(t):alpha.point(lambda v,t=t:255 if v>=t else 0).getbbox() for t in [1,16,64,128,240]}
        audit={'dimensions':list(rgba.size),'mode':'RGBA','alpha_zero':hist[0],'alpha_partial':sum(hist[1:255]),'alpha_opaque':hist[255],'bbox_by_threshold':thresholds,'cleanup':'none; original generated alpha and RGB preserved byte-for-byte','visibility_note':'Hidden RGB and near-zero-alpha background are not visible contamination. Both raw and correct light/dark RGBA composites actually viewed. Numerical alpha>0 bbox is not a visible clipping test.'}
        (d/'alpha_evidence.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
    draw.text((28,2125),'美术候选已审不等于连续动画：脚底基准、轨迹、帧时序、装备合成与游戏运行均未验证。',font=font(22),fill=(57,61,67))
    board.save(OUT/'continuation_005_006_adjacent_light_dark_zh.png')
    (OUT/'board_manifest.json').write_text(json.dumps({'entries':entries,'body_painting':False,'stretching':False,'scale_policy':'same scalar for every image; no alpha-bbox normalization','continuous_animation_verified':False},ensure_ascii=False,indent=2))
    print('Board and selected copies created; no artwork edits. Root:',ROOT)
if __name__=='__main__':main()
