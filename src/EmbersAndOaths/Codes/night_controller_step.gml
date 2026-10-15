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
if (room == r_eao_n2_camp || room == r_eao_n2_winch || room == r_eao_n2_side) exit;
if (room == r_eao_fx_quarry) exit;
if (room == r_eao_d01_warehouse || room == r_eao_d01_archive) exit;
// CS-BRY-01 (evt_CS_BRY_01_entry, engine event 50576): the lease case, the
// SVC-BRY desk and the street speakers live in the native Brynn quarters.
// The pilot wires the system layer next to the player; district geography
// and proportions stay open (OI-06). Independent of the caravan state.
if (room == r_Brynn_NW || room == r_Brynn_SW || room == r_Brynn_SE || room == r_Brynn_NE) {
    var _cp = instance_find(o_player, 0);
    var _actors = [[o_eao_cs_rena, 1, -3], [o_eao_cs_pelan, 3, -3], [o_eao_cs_maler, 5, -3], [o_eao_cs_lukan, 1, 0], [o_eao_svc_milo, 3, 0], [o_eao_cs_street, 5, 0]];
    for (var _a = 0; _a < array_length(_actors); _a++) {
        if (instance_exists(_actors[_a][0])) continue;
        for (var _b = 0; _b < 4; _b++) {
            var _cx = floor(_cp.x / 26) + _actors[_a][1] + (_b mod 2);
            var _cy = floor(_cp.y / 26) + _actors[_a][2] + floor(_b / 2);
            var _px = _cx * 26 + 13; var _py = _cy * 26 + 13;
            if (_cx < 2 || _cy < 2 || _px > room_width - 52 || _py > room_height - 52) continue;
            if (astar_get_cell(o_controller.newgrid, _cx, _cy) != 0 || scr_check_collision_not_enemy_around(_px, _py)) continue;
            instance_create_depth(_px, _py, -_py, _actors[_a][0]);
            break;
        }
    }
    // FX pilot (evt_FX_QRY_field_intro, engine event 71920): the quarry path
    // stands in the south-west quarter, separate from the case actors.
    if (!instance_exists(o_eao_fx_entry)) {
        for (var _k = 0; _k < 16; _k++) {
            var _fx = floor(_cp.x / 26) + 7 + (_k mod 2);
            var _fy = floor(_cp.y / 26) + 2 + floor(_k / 2);
            var _fqx = _fx * 26 + 13; var _fqy = _fy * 26 + 13;
            if (_fx < 2 || _fy < 2 || _fqx > room_width - 52 || _fqy > room_height - 52) continue;
            if (astar_get_cell(o_controller.newgrid, _fx, _fy) != 0 || scr_check_collision_not_enemy_around(_fqx, _fqy)) continue;
            instance_create_depth(_fqx, _fqy, -_fqy, o_eao_fx_entry);
            break;
        }
    }
    exit;
}
if (!scr_quest_get_complete("questGuinnelAnswers") || scr_caravanPositionGetX() < 0 || scr_caravanPositionGetY() < 0 || scr_caravanPositionGetDistance() != 0) {
    instance_destroy(o_eao_n1_mara); instance_destroy(o_eao_n1_entry); instance_destroy(o_eao_n2_entry); exit;
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
// N2 (evt_N2_entry, engine event 10640): the ash embankment path appears at
// the caravan once the bell case is closed (N1 lead: ash_embankment).
if (!ds_map_exists(global.characterDataMap, "EAO_N1_stage") || ds_map_find_value(global.characterDataMap, "EAO_N1_stage") < 5) {
    instance_destroy(o_eao_n2_entry);
} else if (!instance_exists(o_eao_n2_entry)) {
    for (var _j = 0; _j < 16; _j++) {
        var _dx = floor(_player.x / 26) + 2 + (_j mod 4);
        var _dy = floor(_player.y / 26) - 2 + floor(_j / 4);
        var _ex = _dx * 26 + 13; var _ey = _dy * 26 + 13;
        if (_dx < 2 || _dy < 2 || _ex > room_width - 52 || _ey > room_height - 52) continue;
        if (astar_get_cell(o_controller.newgrid, _dx, _dy) != 0 || scr_check_collision_not_enemy_around(_ex, _ey)) continue;
        instance_create_depth(_ex, _ey, -_ey, o_eao_n2_entry);
        break;
    }
}
