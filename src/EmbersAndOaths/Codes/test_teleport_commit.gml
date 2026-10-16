// Runs AFTER the original saver event 4 and BEFORE native room_goto.
if (!ds_map_exists(global.characterDataMap, "EAO_test_map_commit") || ds_map_find_value(global.characterDataMap, "EAO_test_map_commit") != 1) exit;
ds_map_set(global.characterDataMap, "EAO_test_map_commit", 0);
if (ds_map_find_value(global.characterDataMap, "EAO_test_map_restore") == 1) {
    global.playerGridX = ds_map_find_value(global.characterDataMap, "EAO_test_map_source_grid_x");
    global.playerGridY = ds_map_find_value(global.characterDataMap, "EAO_test_map_source_grid_y");
    scr_atr_set_simple("localX", ds_map_find_value(global.characterDataMap, "EAO_test_map_source_x"));
    scr_atr_set_simple("localY", ds_map_find_value(global.characterDataMap, "EAO_test_map_source_y"));
    global.position_tag = "NA";
    ds_map_set(global.characterDataMap, "EAO_test_map_restore", 0);
    ds_map_set(global.characterDataMap, "EAO_test_map_arrival", 0);
    exit;
}
// Explicit Shift+F8 return, after saving the current location. Exact original
// room/local coordinates also support departure from an ordinary interior.
if (ds_map_exists(global.characterDataMap,"EAO_test_map_home") && ds_map_find_value(global.characterDataMap,"EAO_test_map_home") == 1) {
    global.playerGridX = ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_grid_x");
    global.playerGridY = ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_grid_y");
    scr_atr_set_simple("localX",ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_x"));
    scr_atr_set_simple("localY",ds_map_find_value(global.characterDataMap,"EAO_dev_warp_origin_y"));
    global.position_tag = "NA";
    ds_map_set(global.characterDataMap,"EAO_test_map_home",0);
    ds_map_set(global.characterDataMap,"EAO_test_map_arrival",0);
    exit;
}
global.playerGridX = ds_map_find_value(global.characterDataMap, "EAO_test_map_x");
global.playerGridY = ds_map_find_value(global.characterDataMap, "EAO_test_map_y");
scr_atr_set_simple("localX", undefined);
scr_atr_set_simple("localY", undefined);
// Outdoor generation creates its abstract player at (-50,-50), without a
// universal "global" starter. Resolve the generated collision grid before spawn.
global.position_tag = "NA";
ds_map_set(global.characterDataMap, "EAO_test_map_arrival", 1);
// Retire an old guide journey only after the new world transition succeeds.
ds_map_set(global.characterDataMap, "EAO_test_trip_active", 0);
ds_map_set(global.characterDataMap, "EAO_test_return_pending", 0);
