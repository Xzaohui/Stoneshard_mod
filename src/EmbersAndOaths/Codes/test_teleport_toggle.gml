if (!instance_exists(o_player) || instance_exists(o_smoothRoomChanger) || !variable_global_exists("characterDataMap")) exit;
if (!ds_exists(global.characterDataMap, ds_type_map)) exit;
var _enabled = ds_map_exists(global.characterDataMap, "EAO_test_teleport_enabled") && ds_map_find_value(global.characterDataMap, "EAO_test_teleport_enabled") == 1;
ds_map_set(global.characterDataMap, "EAO_test_map_schema", 1);
ds_map_set(global.characterDataMap, "EAO_test_teleport_enabled", !_enabled);
ds_map_set(global.characterDataMap, "EAO_test_map_pending", 0);
ds_map_set(global.characterDataMap, "EAO_test_pending", "");
scr_actionsLogAddMessage(global.language == 3 ? (_enabled ? "测试传送已关闭（F8开启）。" : "测试传送已开启：打开地图，左键点击方块；F8关闭。") : (_enabled ? "Test teleport OFF (F8)." : "Test teleport ON: open the map and left-click a tile. F8 disables it."));
audio_play_sound(_enabled ? snd_checkbox_off : snd_checkbox_on, 4, false);
