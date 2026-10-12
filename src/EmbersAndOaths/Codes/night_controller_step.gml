// Retired resources remain addressable, but their quests never spawn or advance.
if (instance_exists(o_dialogue) || instance_exists(o_smoothRoomChanger)) exit;
if (!instance_exists(o_player) || !variable_global_exists("characterDataMap") || !variable_global_exists("__dialogue_flow_data") || !variable_global_exists("npc_lines_map") || !variable_global_exists("book_content") || !variable_global_exists("consum_stat_data")) exit;
if (!is_real(global.characterDataMap) || !ds_exists(global.characterDataMap, ds_type_map) || !is_struct(global.__dialogue_flow_data)) exit;
instance_destroy(o_eao_courier);
instance_destroy(o_eao_d01_clerk);
instance_destroy(o_eao_d01_entry);
event_user(2);
if (instance_exists(o_smoothRoomChanger)) exit;
if (room == r_eao_n1_yard || room == r_eao_n1_bellhouse || room == r_eao_n1_underpass) exit;
if (room == r_eao_d01_warehouse || room == r_eao_d01_archive) exit;
if (!scr_quest_get_complete("questGuinnelAnswers") || scr_caravanPositionGetX() < 0 || scr_caravanPositionGetY() < 0 || scr_caravanPositionGetDistance() != 0) {
    instance_destroy(o_eao_n1_mara); instance_destroy(o_eao_n1_entry); exit;
}
var _player = instance_find(o_player, 0);
var _objects = [o_eao_n1_mara, o_eao_n1_entry];
for (var _n = 0; _n < array_length(_objects); _n++) {
    var _obj = array_get(_objects, _n);
    if (instance_exists(_obj)) continue;
    if (_n == 1 && (!ds_map_exists(global.characterDataMap, "EAO_N1_stage") || ds_map_find_value(global.characterDataMap, "EAO_N1_stage") < 1)) continue;
    for (var _i = 0; _i < 16; _i++) {
        var _cx = floor(_player.x / 26) + 2 + (_i mod 4);
        var _cy = floor(_player.y / 26) - 2 + floor(_i / 4);
        var _px = _cx * 26 + 13; var _py = _cy * 26 + 13;
        if (_cx < 2 || _cy < 2 || _px > room_width - 52 || _py > room_height - 52) continue;
        if (astar_get_cell(o_controller.newgrid, _cx, _cy) != 0 || scr_check_collision_not_enemy_around(_px, _py)) continue;
        instance_create_depth(_px, _py, -_py, _obj);
        break;
    }
}
