var _changing = instance_exists(o_smoothRoomChanger);
event_inherited();
if (!_changing && instance_exists(o_smoothRoomChanger) && instance_exists(o_player)) {
    ds_map_set(global.characterDataMap, "EAO_N1_origin_room", room_get_name(room));
    ds_map_set(global.characterDataMap, "EAO_N1_origin_x", o_player.x);
    ds_map_set(global.characterDataMap, "EAO_N1_origin_y", o_player.y);
    ds_map_set(global.characterDataMap, "EAO_N1_origin_grid_x", global.playerGridX);
    ds_map_set(global.characterDataMap, "EAO_N1_origin_grid_y", global.playerGridY);
}
