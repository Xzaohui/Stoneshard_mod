// Upgrade the retired guide setting once; the map switch starts OFF.
if (!ds_map_exists(global.characterDataMap, "EAO_test_map_schema")) {
    ds_map_set(global.characterDataMap, "EAO_test_map_schema", 1);
    ds_map_set(global.characterDataMap, "EAO_test_teleport_enabled", 0);
    ds_map_set(global.characterDataMap, "EAO_test_map_pending", 0);
    ds_map_set(global.characterDataMap, "EAO_test_pending", "");
}
var _test_enabled = ds_map_find_value(global.characterDataMap, "EAO_test_teleport_enabled") == 1;
// Finish a return already recorded by 0.2.1 without keeping its exit override.
if (ds_map_exists(global.characterDataMap, "EAO_test_trip_active") && ds_map_find_value(global.characterDataMap, "EAO_test_trip_active") == 1 && ds_map_exists(global.characterDataMap, "EAO_test_origin_room")) {
    if (room_get_name(room) == ds_map_find_value(global.characterDataMap, "EAO_test_origin_room") && global.playerGridX == ds_map_find_value(global.characterDataMap, "EAO_test_origin_grid_x") && global.playerGridY == ds_map_find_value(global.characterDataMap, "EAO_test_origin_grid_y")) {
        ds_map_set(global.characterDataMap, "EAO_test_trip_active", 0);
        ds_map_set(global.characterDataMap, "EAO_test_return_pending", 0);
    }
}
with (o_globalmapInteractiveNormal) {
    if (_test_enabled && guiInteractiveEvent == 15) {
        scr_guiInteractiveStateUpdate(id, 2);
        scr_guiInteractiveEventUpdate(id, 10);
    } else if (!_test_enabled && guiInteractiveEvent == 10) {
        scr_guiInteractiveEventUpdate(id, 15);
    }
}
event_user(3);
