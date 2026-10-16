// Approved east-layout rows, x40..47 / y22..40. Ordinary cells remain native
// generated wilderness. G1/F1/Q2 scene migration is deliberately separate.
var _eao_rows = EAO_REGION_ROWS;
var _eao_coast_rows = EAO_REGION_COAST_ROWS;
var _eao_source = ds_grid_get(global.terrainGrid, 39, 35);
var _eao_ss = ds_map_find_value(_eao_source, "SpawnerSettings");
var _eao_master_seed = real(global.seed);
for (_eao_x = 40; _eao_x < _eao_nw; _eao_x++) {
    for (_eao_y = 0; _eao_y < _eao_h; _eao_y++) {
        var _eao_cell = _eao_y < 22 ? "^" : "~";
        if (_eao_x < 48 && _eao_y >= 22 && _eao_y <= 40)
            _eao_cell = string_char_at(_eao_rows[_eao_y-22], _eao_x-39);
        if (_eao_x >= 48) _eao_cell = _eao_y < 35 ? "^" : "~";
        var _eao_coast_frame=string_pos(string_char_at(_eao_coast_rows[_eao_y],_eao_x-39),"0123456789abcdef")-1;
        // A one-cell inlet with no water corners is dry land in both the map
        // and the actual room; never leave an invisible blocked sea cell.
        if(_eao_cell=="~" && _eao_coast_frame==0) _eao_cell="s";
        _eao_p = ds_grid_get(global.terrainGrid, _eao_x, _eao_y);
        ds_map_set(_eao_p,"EAO_coast_frame",_eao_coast_frame);
        var _eao_land = _eao_cell != "^" && _eao_cell != "~";
        var _eao_biome = "Middle";
        var _eao_room = r_field;
        switch (_eao_cell) {
            case "^": _eao_biome="Mount"; _eao_room=r_field; break;
            case "~": _eao_biome="Sea"; _eao_room=r_sea; break;
            case "p": _eao_biome="Pine"; _eao_room=r_pineforest; break;
            case "s": _eao_biome="Steppe"; _eao_room=r_steppe; break;
            case "r":
                if (_eao_y >= 33) { _eao_biome="Steppe"; _eao_room=r_steppe; }
                break;
        }
        ds_map_set(_eao_p,"Collision",!_eao_land);
        ds_map_set(_eao_p,"Biome",_eao_biome);
        ds_map_set(_eao_p,"room_type",room_get_name(_eao_room));
        ds_map_set(_eao_p,"Type","Wild"); ds_map_set(_eao_p,"Subtype","WildFree");
        ds_map_set(_eao_p,"Preset","N/A");
        ds_map_set(_eao_p,"Forest",_eao_cell=="p" ? 2 : 0);
        ds_map_set(_eao_p,"Road",["None",false,false,-4]);
        ds_map_set(_eao_p,"Water",[_eao_cell=="r" ? "River" : _eao_cell=="~" ? "Sea" : "None",_eao_cell=="r" && _eao_y>29,false]);
        ds_map_set(_eao_p,"DecorationType","N/A"); ds_map_set(_eao_p,"Decoration","N/A");
        ds_map_set(_eao_p,"MapZone","map_brynn");
        ds_map_set(_eao_p,"EAO_east",2);
        if (_eao_x >= _eao_ow) {
            // Stable per-world seeds without consuming the original RNG stream.
            ds_map_set(_eao_p,"seed",abs(_eao_master_seed+_eao_x*131+_eao_y*17) mod 10001);
            ds_map_set(_eao_p,"Trade_Seed",abs(_eao_master_seed+_eao_x*37+_eao_y*101) mod 10001);
            ds_map_set(_eao_p,"presetSeed",abs(_eao_master_seed+_eao_x*53+_eao_y*7) mod 10001);
            ds_map_set(_eao_p,"growSeed",abs(_eao_master_seed+_eao_x*11+_eao_y*29) mod 10001);
            ds_map_set(_eao_p,"mobsSeed",abs(_eao_master_seed+_eao_x*19+_eao_y*3) mod 10001);
            ds_map_set(_eao_p,"containersSeed",abs(_eao_master_seed+_eao_x*23+_eao_y*41) mod 10001);
            var _eao_spawn=ds_map_create();
            ds_map_add(_eao_spawn,"AmbushChance",_eao_land ? ds_map_find_value(_eao_ss,"AmbushChance") : 0);
            var _eao_range=ds_map_find_value(_eao_ss,"LevelRange");
            ds_map_add(_eao_spawn,"LevelRange",new Range(_eao_land ? _eao_range.Min : 0,_eao_land ? _eao_range.Max : 0));
            ds_map_add(_eao_spawn,"Wilderness",ds_map_find_value(_eao_ss,"Wilderness"));
            ds_map_add(_eao_spawn,"Influence",_eao_land ? ds_map_find_value(_eao_ss,"Influence") : 0);
            var _eao_npc=ds_map_create();
            if (_eao_land) ds_map_copy(_eao_npc,ds_map_find_value(_eao_ss,"NpcSpawnChance"));
            ds_map_add_map(_eao_spawn,"NpcSpawnChance",_eao_npc);
            ds_map_add_map(_eao_p,"SpawnerSettings",_eao_spawn);
        }
        else if (_eao_land) {
            // The two old border columns may have had mountain/sea spawners.
            // Reuse their owned child maps, avoiding shared child ownership.
            var _eao_spawn=ds_map_find_value(_eao_p,"SpawnerSettings");
            var _eao_range=ds_map_find_value(_eao_ss,"LevelRange");
            ds_map_set(_eao_spawn,"AmbushChance",ds_map_find_value(_eao_ss,"AmbushChance"));
            ds_map_set(_eao_spawn,"LevelRange",new Range(_eao_range.Min,_eao_range.Max));
            ds_map_set(_eao_spawn,"Wilderness",ds_map_find_value(_eao_ss,"Wilderness"));
            ds_map_set(_eao_spawn,"Influence",ds_map_find_value(_eao_ss,"Influence"));
            ds_map_copy(ds_map_find_value(_eao_spawn,"NpcSpawnChance"),ds_map_find_value(_eao_ss,"NpcSpawnChance"));
        }
    }
}
// Preserve the pilot's actual world save/indoor origin. No duplicate G1 is added.
_eao_p=ds_grid_get(global.terrainGrid,41,37);
ds_map_set(_eao_p,"room_type","r_eao_n2_world");

// Connect to an existing west-edge road only when the native seed generated one.
// Never paint a road into an original grass cell merely to fake a connection.
var _eao_join_y=-1;
for (_eao_y=35;_eao_y<=38;_eao_y++) {
    if (scr_glmap_hasRoad(39,_eao_y)) { _eao_join_y=_eao_y; break; }
}
for (_eao_x=40;_eao_x<=47;_eao_x++) {
    _eao_p=ds_grid_get(global.terrainGrid,_eao_x,36);
    ds_map_set(_eao_p,"Road",["Road",_eao_x==42,_eao_x>40 || _eao_join_y==36,-4]);
}
if (_eao_join_y!=-1) for (_eao_y=min(36,_eao_join_y);_eao_y<=max(36,_eao_join_y);_eao_y++) {
    _eao_p=ds_grid_get(global.terrainGrid,40,_eao_y);
    var _eao_rd=ds_map_find_value(_eao_p,"Road");
    _eao_rd[0]="Road"; _eao_rd[1]=_eao_y>min(36,_eao_join_y);
    _eao_rd[2]=_eao_y==_eao_join_y; ds_map_set(_eao_p,"Road",_eao_rd);
}
// Quarry approach, a west approach to the retained task surface, and greybank coast.
for (_eao_y=32;_eao_y<=35;_eao_y++) ds_map_set(ds_grid_get(global.terrainGrid,42,_eao_y),"Road",["Road",_eao_y>32,_eao_y==33,-4]);
ds_map_set(ds_grid_get(global.terrainGrid,41,33),"Road",["Road",false,false,-4]);
ds_map_set(ds_grid_get(global.terrainGrid,40,37),"Road",["Road",true,_eao_join_y==37,-4]);
ds_map_set(ds_grid_get(global.terrainGrid,41,37),"Road",["Road",false,true,-4]);
ds_map_set(ds_grid_get(global.terrainGrid,43,37),"Road",["Road",true,false,-4]);
for (_eao_y=37;_eao_y<=38;_eao_y++) ds_map_set(ds_grid_get(global.terrainGrid,44,_eao_y),"Road",["Road",true,false,-4]);
// Native full-size bridge carries the road across the vertical river. The ferry
// task still awaits its dedicated exterior; it is not claimed implemented here.
_eao_p=ds_grid_get(global.terrainGrid,45,36);
ds_map_set(_eao_p,"Road",["WoodBridge",false,true,-4]);
ds_map_set(_eao_p,"Subtype","Infrastructure");ds_map_set(_eao_p,"Class","Bridge");
// Native names describe RIVER orientation, not the walking direction.
ds_map_set(_eao_p,"Location","BridgeWoodV01");
ds_map_set(_eao_p,"room_type",room_get_name(r_River_BridgeWood_vertical_01));
global.EAO_east_road_join_y=_eao_join_y;
