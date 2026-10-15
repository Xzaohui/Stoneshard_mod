var _changing=instance_exists(o_smoothRoomChanger);
event_inherited();
if (_changing || !instance_exists(o_smoothRoomChanger) || !instance_exists(o_player)) exit;
if (dev_return) {
    scr_atr_set_simple("localX",ds_map_find_value(global.characterDataMap,"EAO_N1_origin_x"));
    scr_atr_set_simple("localY",ds_map_find_value(global.characterDataMap,"EAO_N1_origin_y"));
} else if (room != r_eao_n1_yard && room != r_eao_n1_bellhouse && room != r_eao_n1_underpass && room != r_eao_n2_camp && room != r_eao_n2_winch && room != r_eao_n2_side && room != r_eao_n2_sites && room != r_eao_fx_quarry) {
    ds_map_set(global.characterDataMap,"EAO_N1_origin_room",room_get_name(room));
    ds_map_set(global.characterDataMap,"EAO_N1_origin_x",o_player.x);
    ds_map_set(global.characterDataMap,"EAO_N1_origin_y",o_player.y);
    ds_map_set(global.characterDataMap,"EAO_N1_origin_grid_x",global.playerGridX);
    ds_map_set(global.characterDataMap,"EAO_N1_origin_grid_y",global.playerGridY);
}
