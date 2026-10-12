var _changing = instance_exists(o_smoothRoomChanger);
event_inherited();
if (!_changing && instance_exists(o_smoothRoomChanger) && ds_map_exists(global.characterDataMap, "EAO_N1_origin_x")) {
    scr_atr_set_simple("localX", ds_map_find_value(global.characterDataMap, "EAO_N1_origin_x"));
    scr_atr_set_simple("localY", ds_map_find_value(global.characterDataMap, "EAO_N1_origin_y"));
}
