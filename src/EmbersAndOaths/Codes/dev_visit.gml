if (!global.EAO_dev_enabled || !instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || instance_exists(o_dialogue) || instance_exists(o_globalmap)) exit;
if (o_player.HP <= 0 || instance_exists(o_dungeon_controller) || scr_getAgredMobsCount(false,false,true) != 0 || !ds_list_empty(o_player.lock_turn) || scr_unitTurnGetTime()) exit;
var _return = keyboard_check(vk_shift) || keyboard_check_pressed(vk_shift);
var _target = r_eao_n1_yard;
var _tag = "EAO_N1_yard_in";
var _inside = room == r_eao_n1_yard || room == r_eao_n1_bellhouse || room == r_eao_n1_underpass || room == r_eao_n2_sites || room == r_eao_n2_camp || room == r_eao_n2_winch || room == r_eao_n2_side || room == r_eao_fx_quarry;
if (_return) {
    if (!_inside || !ds_map_exists(global.characterDataMap,"EAO_N1_origin_room")) exit;
    _target = asset_get_index(ds_map_find_value(global.characterDataMap,"EAO_N1_origin_room"));
    if (!room_exists(_target)) exit;
    _tag = "NA";
} else if (room == r_eao_n1_yard) { _target=r_eao_n1_bellhouse; _tag="EAO_N1_house_in"; }
else if (room == r_eao_n1_bellhouse) { _target=r_eao_n1_underpass; _tag="EAO_N1_drain_in"; }
else if (room == r_eao_n1_underpass) { _target=r_eao_n2_sites; _tag="EAO_SITE_in"; }
else if (room == r_eao_n2_sites) { _target=r_eao_n2_camp; _tag="EAO_N2_camp_in"; }
else if (room == r_eao_n2_camp) { _target=r_eao_n2_winch; _tag="EAO_N2_winch_in"; }
else if (room == r_eao_n2_winch) { _target=r_eao_n2_side; _tag="EAO_N2_side_in"; }
else if (room == r_eao_n2_side) { _target=r_eao_fx_quarry; _tag="EAO_FX_quarry_in"; }
var _door=instance_create_depth(o_player.x,o_player.y,-o_player.y,o_eao_dev_portal);
with (_door) {
    target = _target; position_tag = _tag; dev_return = _return;
    event_perform(ev_alarm,7);
    instance_destroy();
}
