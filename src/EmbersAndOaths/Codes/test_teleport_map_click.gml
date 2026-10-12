// GUI state 2 is the native focused LEFT press, not a screen-wide mouse poll.
if (guiInteractiveState == 2 && ds_map_exists(global.characterDataMap, "EAO_test_teleport_enabled") && ds_map_find_value(global.characterDataMap, "EAO_test_teleport_enabled") == 1) {
    if (drag || edge || !enter || !instance_exists(guiParent) || global.contract_test) exit;
    var _cell = 52 * guiParent.mapScale;
    var _grid_x = floor((guiParent.mapOffsetX + global.guiMouseX - x) / _cell);
    var _grid_y = floor((guiParent.mapOffsetY + global.guiMouseY - y) / _cell);
    if (scr_globalmapIsBorder(_grid_x, _grid_y) || !room_exists(scr_globaltile_get_room(_grid_x, _grid_y))) {
        scr_actionsLogAddMessage(global.language == 3 ? "这个方块没有可进入的地图。" : "This tile has no enterable map.");
        exit;
    }
    ds_map_set(global.characterDataMap, "EAO_test_map_x", _grid_x);
    ds_map_set(global.characterDataMap, "EAO_test_map_y", _grid_y);
    ds_map_set(global.characterDataMap, "EAO_test_map_pending", 1);
    exit;
}
// Right-click markers, middle drag, wheel and hover retain native behavior.
event_user(15);
