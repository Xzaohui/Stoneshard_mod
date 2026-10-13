"""Read design sources into an art production inventory; never edit those sources.

This records requirements, not finished images or measured game geometry.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'src/Art/hd2d_26x26_20261013'
SOURCES = {}


def read(rel):
    path = ROOT / rel
    SOURCES[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    cities = read('research/city-campaign.json')
    regions = read('research/story-regions.json')
    continuation = read('research/brynn-continuation.json')
    special = read('research/special-location-inventory.json')
    satellite_profiles = read('research/satellite-space-profiles.json')
    records = []

    def add(ident, name, family, source, views, **detail):
        records.append(dict(id=ident, name_zh=name, family=family,
                            source=source, requested_views=views,
                            status='inventoried_not_drawn',
                            runtime_verified=False, **detail))

    for c in cities['cities']:
        add(c['id'], c['name'], 'city', 'research/city-campaign.json',
            ['plan'], name_en=c['english'], note='design/'+c['file'],
            visual=c['visual'], layout=c['space'], edges=c['local_edges'])
        nodes = {n['id']: n for n in c['nodes']}
        for plan in c['space_plans']:
            district = nodes[plan['district']]
            add(district['id'], district['name'], 'district',
                'research/city-campaign.json', ['plan', 'exterior'],
                parent=c['id'], note='design/'+c['space_file'],
                layout=plan['layout'], rooms=plan['rooms'],
                access=plan['access'], quests=plan['quests'])
            for room_id in plan['rooms']:
                room = nodes[room_id]
                add(room_id, room['name'], 'city_space',
                    'research/city-campaign.json', ['plan', 'interior_or_working_space'],
                    parent=district['id'], note='design/'+c['space_file'],
                    **room['space'])
        for sat in c['satellites']:
            profile = satellite_profiles['settlements'][sat['id']]
            add(sat['id'], sat['name'], 'satellite',
                'research/city-campaign.json', ['plan', 'exterior', 'interior_or_working_space'],
                parent=c['id'], note='design/'+sat['file'],
                service_name=profile[1], scene_name=profile[2],
                quests=sat['quests'], **sat['space'])
    for r in regions:
        note = next((ROOT/'design/02_世界与地图').glob('区域_'+r['id']+'_*.md'), None)
        add(r['id'], note.stem.split('_', 2)[-1] if note else r['theme'],
            'story_region', 'research/story-regions.json', ['plan'],
            note=note.relative_to(ROOT).as_posix() if note else None,
            theme=r['theme'], visual=r['mood'], layout=r['movement'],
            art=r['art'], boundary=r['boundary'], safe_return=r['return'],
            edges=r['edges'], entry=r['entry'])
        for key, name, kind, purpose in r['nodes']:
            views = ['plan', 'exterior_or_site']
            if kind == '副本':
                views.append('interior_or_working_space')
            add(r['id']+'-'+key, name, 'story_node',
                'research/story-regions.json', views,
                parent=r['id'], kind=kind, purpose=purpose,
                interior_review='Read corresponding screenplay/dungeon before defining roof, floors and doors; outdoor nodes need no invented room.')
    for s in continuation['spaces']:
        add(s['id'], s['name'], 'continuation_space',
            'research/brynn-continuation.json', ['plan', 'exterior', 'interior_or_working_space'],
            parent=s['anchor'], note='design/'+s['file'],
            layout=s['layout'], alternative=s['alternative'])
    for s in special['rumor_sites']:
        add(s['key'], s['name_zh'], 'field_site',
            'research/special-location-inventory.json', ['plan', 'exterior_or_site'],
            name_en=s.get('name_en'), local_locator=s['index'],
            boundary='Original site name is a reference only; draw the Mod encounter extension after reading its site card. Do not reconstruct or replace an official whole map.',
            interior_review='Site-specific: do not invent indoor rooms for caves, trees, camps or outdoor markers.')
    room_source = 'src/EmbersAndOaths/NightRooms.cs'
    raw = (ROOT/room_source).read_text(encoding='utf-8-sig')
    SOURCES[room_source] = hashlib.sha256((ROOT/room_source).read_bytes()).hexdigest()
    dimensions = re.search(r'Columns=(\d+), Rows=(\d+), Tile=(\d+)', raw)
    cols, rows, tile = map(int, dimensions.groups())
    for key, name, rid in [('Yard','旧渡口岸院','r_eao_n1_yard'),
                           ('Bellhouse','旧渡口钟屋','r_eao_n1_bellhouse'),
                           ('Underpass','旧渡口暗渠','r_eao_n1_underpass')]:
        shape = re.search(r'\['+key+r'\]=new\[\]\{(.*?)\}', raw).group(1)
        rectangles = [list(map(int, row.split(','))) for row in re.findall(r'\(([^)]+)\)', shape)]
        add(rid, name, 'existing_n1_room', room_source,
            ['plan', 'exterior_or_site' if key=='Yard' else 'interior_or_working_space'],
            parent='R02-ferryold', pixels=[cols*tile,rows*tile],
            cell_pixels=tile, walkable_rectangles=rectangles,
            layout_authority='Existing code rectangles; retain exact walkable geometry.',
            note='design/02_世界与地图/旧渡口_场景与通路.md')

    ids = [r['id'] for r in records]
    assert len(set(ids)) == len(ids), 'Duplicate asset location identifiers'
    for r in records:
        if r.get('note'):
            assert (ROOT/r['note']).exists(), r['note']
    requests = [dict(id=r['id']+'__'+v, location=r['id'], view=v,
                     status='not_drawn', path=None, sha256=None)
                for r in records for v in r['requested_views']]
    # Completed exports live separately from source requirements. Rebuilding
    # the inventory must retain them, but changed inputs invalidate readiness.
    progress_path = OUT/'progress.json'
    progress = json.loads(progress_path.read_text(encoding='utf-8')) if progress_path.exists() else {'requests': {}}
    for request in requests:
        prior = progress['requests'].get(request['id'])
        if not prior:
            continue
        def live_source(path):
            if path in SOURCES:
                return SOURCES[path]
            candidate=ROOT/path
            return hashlib.sha256(candidate.read_bytes()).hexdigest() if candidate.is_file() else None
        valid = all(live_source(p) == h for p,h in prior['source_sha256'].items())
        valid = valid and all((OUT/p).is_file() and hashlib.sha256((OUT/p).read_bytes()).hexdigest()==h for p,h in prior['outputs'].items())
        if valid:
            request.update(status='static_export_verified', path=prior['path'],
                           sha256=prior['outputs'][prior['path']], batch=prior['batch'])
        else:
            request.update(status='needs_revalidation', batch=prior['batch'])
    for record in records:
        states=[r['status'] for r in requests if r['location']==record['id']]
        if states and all(s=='static_export_verified' for s in states):
            record['status']='static_export_verified_runtime_unverified'
        elif any(s!='not_drawn' for s in states):
            record['status']='partially_exported_or_needs_revalidation'
    finished=sum(r['status']=='static_export_verified' for r in requests)
    payload = dict(schema=1, date='2026-10-13',
                   status='production_in_progress' if progress_path.exists() else 'requirements_only_awaiting_spec_confirmation',
                   skill_url='https://github.com/424431185/pixel-asset-master-skills',
                   skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',
                   source_sha256=SOURCES, native_tile_pixels=tile,
                   family_counts=dict(Counter(r['family'] for r in records)),
                   view_counts=dict(Counter(a['view'] for a in requests)),
                   initial_view_slots=len(requests), finished_assets=finished,
                   fulfilled_view_slots=finished, remaining_view_slots=len(requests)-finished,
                   counting_note='Source records can refer to overlapping places at different scales. View slots are production requests, not a count of distinct rooms. Source buildings, door counts, dimensions, and drawable indoor spaces require individual spatial review; layer PNGs and additional dungeon floors are not included in this baseline count.',
                   records=records, requests=requests)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'inventory.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with (OUT/'inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['id','name_zh','family','views','source','note','status'])
        for r in records:
            writer.writerow([r['id'],r['name_zh'],r['family'],' / '.join(r['requested_views']),r['source'],r.get('note',''),r['status']])
    print(json.dumps({k:payload[k] for k in ['family_counts','view_counts','initial_view_slots','finished_assets']},ensure_ascii=False))


if __name__ == '__main__':
    main()
