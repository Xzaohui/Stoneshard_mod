namespace EmbersAndOaths;

internal static class TestTeleport
{
    internal const string MapHook = "gml_Object_o_globalmapInteractiveNormal_Other_20";
    internal const string Active = "ds_map_exists(global.characterDataMap, \"EAO_test_trip_active\") && ds_map_find_value(global.characterDataMap, \"EAO_test_trip_active\") == 1";
    // Called by the warehouse's ordinary exit AFTER the original transition
    // scheduled its saver, so native position keys are written only on success.
    internal static string ReturnAlarm => "var _test_return = false;\n" +
        "if ("+Active+" && ds_map_exists(global.characterDataMap, \"EAO_test_origin_room\")) {\n" +
        "var _origin_room = asset_get_index(ds_map_find_value(global.characterDataMap, \"EAO_test_origin_room\"));\n"+
        "if (room_exists(_origin_room) && global.playerGridX == ds_map_find_value(global.characterDataMap, \"EAO_test_origin_grid_x\") && global.playerGridY == ds_map_find_value(global.characterDataMap, \"EAO_test_origin_grid_y\")) { target = _origin_room; position_tag = \"NA\"; _test_return = true; }\n}\n"+
        "event_inherited();\nif (_test_return && instance_exists(o_smoothRoomChanger)) {\n"+
        "scr_atr_set_simple(\"localX\", ds_map_find_value(global.characterDataMap, \"EAO_test_origin_x\"));\n"+
        "scr_atr_set_simple(\"localY\", ds_map_find_value(global.characterDataMap, \"EAO_test_origin_y\"));\n"+
        "ds_map_set(global.characterDataMap, \"EAO_test_return_pending\", 1);\n}\n";
}

