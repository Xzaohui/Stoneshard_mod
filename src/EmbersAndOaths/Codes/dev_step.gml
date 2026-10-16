if (!global.EAO_dev_enabled) exit;
// Shift+F11 return: the native return may swap characterDataMap and briefly
// have no player. Keep the observer (panel/grid/fog/art) across that one
// transition only; any other character change still resets as before.
var _warp_keep = variable_global_exists("EAO_dev_warp_keep") && global.EAO_dev_warp_keep;
var _keep = (variable_global_exists("EAO_dev_return_keep") && global.EAO_dev_return_keep) || _warp_keep;
if (variable_global_exists("characterDataMap") && global.characterDataMap != dev_character_map) {
    if (_keep) dev_character_map = global.characterDataMap;
    else { event_user(0); exit; }
}
if (!instance_exists(o_player) && !instance_exists(o_smoothRoomChanger) && !instance_exists(o_abstract_player) && !instance_exists(o_fastTurnController)) { if (!_keep) event_user(0); exit; }
// The native normal map registers right press (5) and callback User15 only.
// Route its focused interactions through our existing User10 while DEV owns it.
// User10 forwards every non-left interaction to native User15 unchanged.
with (o_globalmapInteractiveNormal) {
    if ((!variable_instance_exists(id,"EAO_dev_map_owned") || !EAO_dev_map_owned) && guiInteractiveEvent==15) {
        EAO_dev_map_left_before=ds_list_find_index(guiInteractiveStatesList,2)!=-1;
        EAO_dev_map_owned=true;
        scr_guiInteractiveStateUpdate(id,2);
        scr_guiInteractiveEventUpdate(id,10);
    }
}
if (_keep && instance_exists(o_player) && !instance_exists(o_smoothRoomChanger) && room == global.EAO_dev_return_room) global.EAO_dev_return_keep = false;
// Two world cells can share r_steppe. Require the newly created player as well
// as room/world coordinates; the old player's final frame must not end keep.
if (_warp_keep && instance_exists(o_player) && !instance_exists(o_smoothRoomChanger) && instance_find(o_player,0) != global.EAO_dev_warp_player && room == global.EAO_dev_warp_room && global.playerGridX == global.EAO_dev_warp_grid_x && global.playerGridY == global.EAO_dev_warp_grid_y) global.EAO_dev_warp_keep = false;
if (dev_reveal && variable_global_exists("fog")) {
    if (!dev_fog_owned) { dev_fog_before = global.fog; dev_fog_owned = true; }
    global.fog = false;
} else if (dev_fog_owned) {
    global.fog = dev_fog_before;
    dev_fog_owned = false;
}
with (o_globalmapFogRender) {
    if (other.dev_reveal) {
        if (!variable_instance_exists(id,"EAO_dev_visible_owned") || !EAO_dev_visible_owned) EAO_dev_visible_before = visible;
        EAO_dev_visible_owned = true;
        visible = false;
    } else if (variable_instance_exists(id,"EAO_dev_visible_owned") && EAO_dev_visible_owned) {
        visible = EAO_dev_visible_before;
        EAO_dev_visible_owned = false;
    }
}
