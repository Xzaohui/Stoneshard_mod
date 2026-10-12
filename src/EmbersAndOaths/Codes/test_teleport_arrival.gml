// End Step runs after native terrain/load alarms and before the NEXT alarm
// creates a real player. Never relocate an already-created player or its grids.
if (!variable_global_exists("characterDataMap") || !is_real(global.characterDataMap) || !ds_exists(global.characterDataMap, ds_type_map)) exit;
if (!ds_map_exists(global.characterDataMap, "EAO_test_map_arrival") || ds_map_find_value(global.characterDataMap, "EAO_test_map_arrival") != 1) exit;
if (instance_exists(o_player) || !instance_exists(o_controller)) exit;
if (global.playerGridX != ds_map_find_value(global.characterDataMap, "EAO_test_map_x") || global.playerGridY != ds_map_find_value(global.characterDataMap, "EAO_test_map_y") || room != scr_globaltile_get_room()) exit;
var _spawn = instance_find(o_abstract_player, 0);
if (!instance_exists(_spawn)) _spawn = instance_find(o_fastTurnController, 0);
if (!instance_exists(_spawn)) exit; // Generation has not finished yet.
var _grid = o_controller.newgrid;
var _width = floor(room_width / 26);
var _height = floor(room_height / 26);
var _center_x = floor(_width / 2);
var _center_y = floor(_height / 2);
var _best = 1000000;
var _landing_x = -1;
var _landing_y = -1;
// Keep a two-cell border; require an open cardinal neighbour for actual movement.
for (var _gx = 2; _gx < _width - 2; _gx++) {
    for (var _gy = 2; _gy < _height - 2; _gy++) {
        var _distance = abs(_gx - _center_x) + abs(_gy - _center_y);
        if (_distance >= _best || astar_get_cell(_grid, _gx, _gy) != 0) continue;
        if (astar_get_cell(_grid, _gx - 1, _gy) != 0 && astar_get_cell(_grid, _gx + 1, _gy) != 0 && astar_get_cell(_grid, _gx, _gy - 1) != 0 && astar_get_cell(_grid, _gx, _gy + 1) != 0) continue;
        var _px = _gx * 26;
        var _py = _gy * 26;
        if (scr_check_collision_not_enemy_around(_px, _py) || instance_exists(scr_tile_mark_get_instance(_gx, _gy))) continue;
        _best = _distance;
        _landing_x = _px;
        _landing_y = _py;
    }
}
if (_landing_x < 0) {
    // An unwalkable tile has no player to save. The source was already saved by
    // event 4. Return via the native changer using only our coordinate bridge.
    _spawn.alarm[0] = 2;
    _spawn.alarm[1] = 2;
    if (instance_exists(o_smoothRoomChanger)) exit;
    var _source_room = asset_get_index(ds_map_find_value(global.characterDataMap, "EAO_test_map_source_room"));
    var _return = scr_smoothRoomChange(_source_room, [10], -1, true);
    if (instance_exists(_return)) {
        ds_map_set(global.characterDataMap, "EAO_test_map_restore", 1);
        ds_map_set(global.characterDataMap, "EAO_test_map_commit", 1);
        scr_actionsLogAddMessage(global.language == 3 ? "目标没有可行走的落点，返回出发位置。" : "No walkable arrival tile; returning to the departure point.");
    }
    exit;
}
_spawn.x = _landing_x;
_spawn.y = _landing_y;
ds_map_set(global.characterDataMap, "EAO_test_map_arrival", 0);
