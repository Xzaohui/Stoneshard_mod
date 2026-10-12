event_inherited();
// Foreground parts are depth -1000 in the native Customs House. The added
// entrance must draw in front of them while keeping the native interaction grid.
depth = -1100;
is_lock = true;
if (variable_global_exists("characterDataMap") && is_real(global.characterDataMap) && ds_exists(global.characterDataMap, ds_type_map)) {
    is_lock = !(ds_map_exists(global.characterDataMap, "EAO_MQ01") && ds_map_find_value(global.characterDataMap, "EAO_MQ01") >= 2 && ds_map_exists(global.characterDataMap, "EAO_read_eao_copy") && ds_map_find_value(global.characterDataMap, "EAO_read_eao_copy") == 1);
}
LVL = 100;
speech_key = "door_barred";
name = global.language == 3 ? "封账仓入口" : "Sealed warehouse entrance";
