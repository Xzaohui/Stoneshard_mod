event_user(4);
var _ready = false;
if (instance_exists(o_player) && instance_exists(o_inventory) && variable_global_exists("consum_stat_data") && variable_global_exists("book_content") && variable_global_exists("characterDataMap") && variable_global_exists("questsDataMap") && variable_global_exists("caravanDataMap") && variable_global_exists("__dialogue_flow_data") && variable_global_exists("npc_lines_map")) {
    if (is_real(global.characterDataMap) && is_struct(global.__dialogue_flow_data)) {
        _ready = ds_exists(global.characterDataMap, ds_type_map) && ds_exists(global.questsDataMap, ds_type_map) && ds_exists(global.caravanDataMap, ds_type_map) && ds_exists(global.npc_lines_map, ds_type_map);
    }
}
if (!_ready) {
    event_user(0);
    event_user(1);
    state_map = -1;
    exit;
}
if (state_map != global.characterDataMap) {
    event_user(0);
    event_user(1);
    state_map = global.characterDataMap;
}
// A live native dialogue keeps its speaker until the native exit completes.
if (instance_exists(o_dialogue)) exit;
// Native port-store annex: no replacement of original world-map tiles or doors.
if (room == r_eao_d01_archive && ds_map_exists(global.characterDataMap, "EAO_MQ02") && ds_map_find_value(global.characterDataMap, "EAO_MQ02") >= 1) {
    ds_map_set(global.characterDataMap, "EAO_D01_archive_visited", 1);
}
if (room == r_eao_d01_warehouse || room == r_eao_d01_archive || room == r_DockStore1floor) {
    event_user(0);
    exit;
}
if (!scr_quest_get_complete("questGuinnelAnswers") || scr_caravanPositionGetX() < 0 || scr_caravanPositionGetY() < 0 || scr_caravanPositionGetDistance() != 0) {
    event_user(0);
    exit;
}
if (!instance_exists(courier_id)) {
    var _player = instance_find(o_player, 0);
    courier_id = instance_create_depth(_player.x + 52, _player.y, -_player.y, o_eao_courier);
}
